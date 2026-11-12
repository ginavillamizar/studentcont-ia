#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Backend y Motor Contable/Excel en Tiempo Real para STUDENTCONT.IA
Soporta Multi-Empresa + Modo Aprendizaje Contable y actualización en vivo de:
- Comprobantes y Facturas
- Kardex Promedio Ponderado
- Libros Auxiliares (Subcuentas 6 dígitos, Auxiliares 8 dígitos y Libro Auxiliar de Bancos)
- Estados Financieros NIIF y Calendario Tributario
"""

import os
import re
import json
import gzip
import base64
import ssl
import zlib
import zipfile
import subprocess
import shutil
import urllib.parse
import urllib.request
import datetime
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from http.server import HTTPServer, ThreadingHTTPServer, SimpleHTTPRequestHandler
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE_DIR = "/Users/ginavillamizar/Downloads/CONTABILIDAD"
DATA_DIR = os.path.join(BASE_DIR, "data")
IA_DOCS_DIR = os.path.join(DATA_DIR, "documentos_ia")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IA_DOCS_DIR, exist_ok=True)
ELECTRO_FILE = os.path.join(DATA_DIR, "electrovivienda_db.json")
WORKSPACES_FILE = os.path.join(DATA_DIR, "workspaces_index.json")
PROFILES_FILE = os.path.join(DATA_DIR, "student_profiles.json")
IA_KB_FILE = os.path.join(DATA_DIR, "ia_custom_knowledge.json")
REFORMAS_FILE = os.path.join(DATA_DIR, "reformas_colombia.json")

class CleanWebPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.skip_tag = 0
        self.title = ""
        self.meta_desc = ""
        self.blocks = []
        self.current = []

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        if t in ("script", "style", "noscript", "svg", "nav", "footer", "header", "iframe"):
            self.skip_tag += 1
        elif t == "title":
            self.in_title = True
        elif t == "meta":
            attr_dict = {k.lower(): (v or "") for k, v in attrs}
            if attr_dict.get("name", "").lower() == "description" or attr_dict.get("property", "").lower() == "og:description":
                if not self.meta_desc:
                    self.meta_desc = attr_dict.get("content", "").strip()
        elif t in ("p", "h1", "h2", "h3", "h4", "li", "tr", "div", "article", "section", "br"):
            if self.current:
                txt = " ".join(self.current).strip()
                if len(txt) > 20:
                    self.blocks.append(txt)
                self.current = []

    def handle_endtag(self, tag):
        t = tag.lower()
        if t in ("script", "style", "noscript", "svg", "nav", "footer", "header", "iframe") and self.skip_tag > 0:
            self.skip_tag -= 1
        elif t == "title":
            self.in_title = False
        elif t in ("p", "h1", "h2", "h3", "h4", "li", "tr", "div", "article", "section"):
            if self.current:
                txt = " ".join(self.current).strip()
                if len(txt) > 20:
                    self.blocks.append(txt)
                self.current = []

    def handle_data(self, data):
        if self.in_title:
            self.title += data
            return
        if self.skip_tag > 0:
            return
        cleaned = re.sub(r"\s+", " ", data).strip()
        if cleaned:
            self.current.append(cleaned)

def extract_keywords_from_text(title, text):
    combined = f"{title} {text[:3000]}".lower()
    words = re.findall(r"[a-záéíóúñ0-9]{4,}", combined)
    stop = {
        "para", "como", "este", "esta", "estos", "estas", "todo", "toda", "todos", "todas",
        "sobre", "entre", "desde", "hasta", "cuando", "donde", "porque", "pero", "sino",
        "tiene", "tienen", "puede", "pueden", "debe", "deben", "según", "segun", "cada",
        "cual", "cuales", "mismo", "misma", "otros", "otras", "parte", "forma", "caso",
        "años", "año", "será", "sera", "sido", "está", "esta", "están", "estan", "hacer"
    }
    freq = {}
    for w in words:
        if w not in stop and not w.isdigit():
            freq[w] = freq.get(w, 0) + 1
    # Incluir también códigos numéricos de 3 o 4 dígitos (cuentas PUC, leyes, artículos)
    codes = re.findall(r"\b\d{3,6}\b", combined)
    top_words = [k for k, _ in sorted(freq.items(), key=lambda item: item[1], reverse=True)[:12]]
    for c in codes[:6]:
        if c not in top_words:
            top_words.append(c)
    return ", ".join(top_words[:15])

def extract_text_from_webpage_url(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-CO,es;q=0.9,en;q=0.8"
        }
    )
    with urllib.request.urlopen(req, timeout=12, context=ctx) as resp:
        raw_bytes = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
        try:
            html_str = raw_bytes.decode(charset, errors="replace")
        except Exception:
            html_str = raw_bytes.decode("utf-8", errors="replace")

    parser = CleanWebPageParser()
    parser.feed(html_str)
    title = re.sub(r"\s+", " ", parser.title).strip() or url
    dedup_blocks = []
    seen = set()
    if parser.meta_desc:
        dedup_blocks.append(parser.meta_desc)
        seen.add(parser.meta_desc[:80])
    for b in parser.blocks:
        key = b[:80]
        if key not in seen:
            seen.add(key)
            dedup_blocks.append(b)
        if sum(len(x) for x in dedup_blocks) > 18000:
            break
    full_text = "\n\n".join(dedup_blocks)
    summary = "\n".join(dedup_blocks[:8])[:1800] if dedup_blocks else "Página web indexada."
    keywords = extract_keywords_from_text(title, full_text)
    return {
        "title": title[:160],
        "summary": summary,
        "full_text": full_text[:25000],
        "keywords": keywords
    }

def extract_text_from_uploaded_file(filepath, filename):
    ext = os.path.splitext(filename.lower())[1]
    extracted_chunks = []

    if ext in (".xlsx", ".xlsm"):
        wb = openpyxl.load_workbook(filepath, data_only=True)
        for sname in wb.sheetnames[:15]:
            ws = wb[sname]
            sheet_lines = [f"=== HOJA EXCEL: {sname} ==="]
            for r in ws.iter_rows(values_only=True):
                vals = [str(v).strip() for v in r if v is not None and str(v).strip() != ""]
                if vals:
                    sheet_lines.append(" | ".join(vals[:12]))
                if len(sheet_lines) > 120:
                    break
            if len(sheet_lines) > 1:
                extracted_chunks.append("\n".join(sheet_lines))
    elif ext == ".docx":
        try:
            with zipfile.ZipFile(filepath) as zf:
                xml_content = zf.read("word/document.xml")
            tree = ET.fromstring(xml_content)
            paragraphs = []
            for elem in tree.iter():
                if elem.tag.endswith("}p"):
                    texts = [t.text for t in elem.iter() if t.tag.endswith("}t") and t.text]
                    if texts:
                        p_str = "".join(texts).strip()
                        if p_str:
                            paragraphs.append(p_str)
            extracted_chunks.append("\n".join(paragraphs))
        except Exception:
            pass
    elif ext in (".doc", ".rtf", ".html", ".htm"):
        try:
            out = subprocess.check_output(["/usr/bin/textutil", "-convert", "txt", "-stdout", filepath], timeout=10)
            extracted_chunks.append(out.decode("utf-8", errors="replace"))
        except Exception:
            pass
    elif ext == ".pdf":
        # Extracción por streams zlib de PDF en caso de que el navegador no haya enviado texto pre-extraído
        with open(filepath, "rb") as f:
            pdf_bytes = f.read()
        streams = re.findall(rb"stream[\r\n]+(.*?)[\r\n]+endstream", pdf_bytes, re.DOTALL)
        texts = []
        for s in streams[:350]:
            try:
                decomp = zlib.decompress(s)
                parts = re.findall(rb"\(([^()]{2,200})\)", decomp)
                line = " ".join(p.decode("latin-1", errors="ignore") for p in parts)
                line = re.sub(r"\s+", " ", line).strip()
                if len(line) > 15:
                    texts.append(line)
            except Exception:
                continue
        extracted_chunks.append("\n".join(texts))
    else:
        with open(filepath, "rb") as f:
            raw = f.read()
        try:
            extracted_chunks.append(raw.decode("utf-8"))
        except Exception:
            extracted_chunks.append(raw.decode("latin-1", errors="replace"))

    full_text = "\n\n".join(c for c in extracted_chunks if c).strip()
    return full_text[:35000]

def get_ia_custom_kb():
    if not os.path.exists(IA_KB_FILE):
        return []
    with open(IA_KB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_ia_custom_kb(kb_list):
    with open(IA_KB_FILE, "w", encoding="utf-8") as f:
        json.dump(kb_list, f, ensure_ascii=False, indent=2)

def get_custom_reformas():
    if not os.path.exists(REFORMAS_FILE):
        return []
    with open(REFORMAS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_custom_reformas(ref_list):
    with open(REFORMAS_FILE, "w", encoding="utf-8") as f:
        json.dump(ref_list, f, ensure_ascii=False, indent=2)

ALL_12_MONTHS = [
    "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
    "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
]

def get_student_profiles():
    if not os.path.exists(PROFILES_FILE):
        default_profiles = [
            {
                "id": "gina_villamizar",
                "usuario": "gina",
                "nombre": "Gina Villamizar",
                "correo": "gina.villamizar@studentcont.ia",
                "pin": "gina2026",
                "programa": "Contadora Titular • Administradora General",
                "rol": "Titular / Administradora",
                "workspace_id": "electrovivienda",
                "creado": "2026-01-02"
            }
        ]
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(default_profiles, f, ensure_ascii=False, indent=2)
        return default_profiles
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        profiles = json.load(f)
    for p in profiles:
        if p.get("id") == "gina_villamizar":
            if not p.get("pin"):
                p["pin"] = "gina2026"
            if not p.get("usuario"):
                p["usuario"] = "gina"
    return profiles

def sanitize_profiles_for_client(profiles):
    # Nunca enviar contraseñas ni permitir ingreso sin clave a perfiles ajenos
    return [
        {
            "id": p.get("id"),
            "nombre": p.get("nombre"),
            "programa": p.get("programa"),
            "rol": p.get("rol")
        }
        for p in profiles
    ]

def save_student_profiles(profiles):
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)

def get_workspaces_index():
    if not os.path.exists(WORKSPACES_FILE):
        default_idx = {
            "active_id": "electrovivienda",
            "workspaces": [
                {
                    "id": "electrovivienda",
                    "tipo": "EMPRESA PRINCIPAL",
                    "razon_social": "ELECTROVIVIENDA S.A.S",
                    "nit": "901.765.438-3",
                    "regimen_corto": "RRI • Agente Retenedor y Autorretenedor Renta",
                    "ciudad": "Bucaramanga, Santander",
                    "datafile": "electrovivienda_db.json"
                }
            ]
        }
        with open(WORKSPACES_FILE, "w", encoding="utf-8") as f:
            json.dump(default_idx, f, ensure_ascii=False, indent=2)
        return default_idx
    with open(WORKSPACES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_workspaces_index(idx_data):
    with open(WORKSPACES_FILE, "w", encoding="utf-8") as f:
        json.dump(idx_data, f, ensure_ascii=False, indent=2)

def ensure_12_months_in_db(db, ws_id):
    if "meses" not in db or not isinstance(db["meses"], dict):
        db["meses"] = {}
    for m in ALL_12_MONTHS:
        if m not in db["meses"]:
            db["meses"][m] = {
                "archivo": get_excel_filename_for_workspace(ws_id, m),
                "hojas": ["PUC"],
                "total_transacciones": 0,
                "transacciones": [],
                "hojas_especiales": {}
            }
    return db

def load_db(ws_id=None):
    idx = get_workspaces_index()
    target_id = ws_id or idx.get("active_id", "electrovivienda")
    ws_entry = next((w for w in idx["workspaces"] if w["id"] == target_id), idx["workspaces"][0])
    fpath = os.path.join(DATA_DIR, ws_entry["datafile"])
    if not os.path.exists(fpath):
        fpath = ELECTRO_FILE
    with open(fpath, "r", encoding="utf-8") as f:
        db = json.load(f)
    ensure_12_months_in_db(db, ws_entry["id"])
    db["workspaces_info"] = idx
    db["student_profiles"] = sanitize_profiles_for_client(get_student_profiles())
    db["ia_custom_kb"] = get_ia_custom_kb()
    db["custom_reformas"] = get_custom_reformas()
    return db

def save_db(db, ws_id=None):
    idx = get_workspaces_index()
    target_id = ws_id or idx.get("active_id", "electrovivienda")
    ws_entry = next((w for w in idx["workspaces"] if w["id"] == target_id), idx["workspaces"][0])
    fpath = os.path.join(DATA_DIR, ws_entry["datafile"])
    db_copy = dict(db)
    db_copy.pop("workspaces_info", None)
    db_copy["meta"]["actualizado"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(db_copy, f, ensure_ascii=False, indent=2)

def get_excel_filename_for_workspace(ws_id, mes_upper):
    if ws_id == "electrovivienda":
        return f"{mes_upper}.xlsx"
    safe_ws = re.sub(r"[^A-Z0-9_]", "_", ws_id.upper())
    return f"{safe_ws}_{mes_upper}.xlsx"

def write_transaction_to_excel(ws_id, mes_nombre, tx_data, kardex_updated=None, db_mes=None):
    """
    Actualiza el archivo Excel del mes activo:
    1. Crea o actualiza la hoja del Comprobante/Factura (Liquidación + Contabilización + Soporte).
    2. Si hubo movimiento de inventario, actualiza la hoja de Kardex Promedio Ponderado.
    3. Actualiza la hoja de Libros Auxiliares en Vivo (L.AUXILIARES EN VIVO) con todas las subcuentas (6 dígitos),
       auxiliares (8 dígitos) y el Libro Auxiliar de Bancos (11100501).
    """
    mes_upper = mes_nombre.upper()
    xlsx_name = get_excel_filename_for_workspace(ws_id, mes_upper)
    xlsx_path = os.path.join(BASE_DIR, xlsx_name)

    if not os.path.exists(xlsx_path):
        wb = openpyxl.Workbook()
        ws0 = wb.active
        ws0.title = "PUC"
    else:
        wb = openpyxl.load_workbook(xlsx_path)

    navy_fill = PatternFill("solid", fgColor="0F2942")
    gold_fill = PatternFill("solid", fgColor="D4AF37")
    white_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    gold_font = Font(name="Calibri", size=10, bold=True, color="0F2942")
    bold_font = Font(name="Calibri", size=10, bold=True)
    reg_font = Font(name="Calibri", size=10)
    thin = Side(border_style="thin", color="CBD5E1")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    # 1. Hoja de la Transacción / Factura / Comprobante
    sheet_title = str(tx_data.get("hoja", "NV-1"))[:31]
    if sheet_title in wb.sheetnames:
        ws = wb[sheet_title]
        ws.delete_rows(1, ws.max_row + 10)
    else:
        ws = wb.create_sheet(title=sheet_title)

    ws["A1"] = f"{tx_data.get('empresa_nombre', 'ELECTROVIVIENDA S.A.S')} - {tx_data.get('empresa_nit', 'NIT 901.765.438-3')}"
    ws["A1"].font = white_font
    ws["A1"].fill = navy_fill
    ws["B2"] = tx_data.get("hoja", "")
    ws["C2"] = tx_data.get("fecha", "")
    ws["B3"] = tx_data.get("enunciado", "")
    ws["B3"].font = bold_font

    ws["B5"] = "ANTES DE LA LIQUIDACIÓN Y LIQUIDACIÓN TRIBUTARIA"
    ws["B5"].font = gold_font
    ws["B5"].fill = gold_fill
    liq = tx_data.get("liquidacion", {})
    liq_rows = [
        ("Tipo Transacción", tx_data.get("tipo", "")),
        ("Régimen Comprador", liq.get("regimen_comprador", "RRI")),
        ("Régimen Vendedor", liq.get("regimen_vendedor", "RRI Aut. Renta")),
        ("Tercero", tx_data.get("tercero", "")),
        ("NIT / CC Tercero", tx_data.get("nit_tercero", "")),
        ("Subtotal / Base Gravable", liq.get("base", 0)),
        ("IVA (19%)", liq.get("iva", 0)),
        ("Retención en la Fuente", liq.get("retefuente", 0)),
        ("Autorretención Renta", liq.get("autorretencion", 0)),
        ("ReteIVA (15%)", liq.get("reteiva", 0)),
        ("ReteICA (9.6‰)", liq.get("reteica", 0)),
        ("Avisos y Tableros (15%)", liq.get("avisos", 0)),
        ("Sobretasa Bomberil (10%)", liq.get("bomberil", 0)),
        ("NETO A PAGAR / COBRAR", liq.get("neto", tx_data.get("total_debe", 0)))
    ]
    for idx, (k, v) in enumerate(liq_rows, start=6):
        ws.cell(row=idx, column=2, value=k).font = bold_font if "NETO" in k else reg_font
        c_val = ws.cell(row=idx, column=4, value=v)
        c_val.font = bold_font if "NETO" in k else reg_font
        if isinstance(v, (int, float)):
            c_val.number_format = '"$"#,##0.00'

    headers_cont = ["CODIGO", "CUENTA", "PARCIAL", "DEBE", "HABER"]
    for i, h in enumerate(headers_cont, start=7):
        c = ws.cell(row=6, column=i, value=h)
        c.font = white_font
        c.fill = navy_fill
        c.border = border

    r_cursor = 7
    for a in tx_data.get("asientos", []):
        ws.cell(row=r_cursor, column=7, value=a.get("codigo", "")).border = border
        ws.cell(row=r_cursor, column=8, value=a.get("cuenta", "")).border = border
        c_p = ws.cell(row=r_cursor, column=9, value=a.get("parcial", 0) or None)
        c_d = ws.cell(row=r_cursor, column=10, value=a.get("debe", 0) or None)
        c_h = ws.cell(row=r_cursor, column=11, value=a.get("haber", 0) or None)
        for c_num in (c_p, c_d, c_h):
            c_num.border = border
            c_num.number_format = '"$"#,##0.00'
        if len(str(a.get("codigo", ""))) == 4:
            ws.cell(row=r_cursor, column=7).font = bold_font
            ws.cell(row=r_cursor, column=8).font = bold_font
            c_d.font = bold_font
            c_h.font = bold_font
        r_cursor += 1

    ws.cell(row=r_cursor, column=8, value="SUMAS IGUALES").font = bold_font
    c_td = ws.cell(row=r_cursor, column=10, value=tx_data.get("total_debe", 0))
    c_th = ws.cell(row=r_cursor, column=11, value=tx_data.get("total_haber", 0))
    c_td.font = bold_font
    c_th.font = bold_font
    c_td.fill = gold_fill
    c_th.fill = gold_fill
    c_td.number_format = '"$"#,##0.00'
    c_th.number_format = '"$"#,##0.00'

    # Documento Soporte a la derecha
    ws.cell(row=5, column=13, value=tx_data.get("tipo", "COMPROBANTE DE CONTABILIDAD")).font = white_font
    ws.cell(row=5, column=13).fill = navy_fill
    ws.cell(row=6, column=13, value="CIUDAD Y FECHA:").font = bold_font
    ws.cell(row=6, column=14, value=f"Bucaramanga, {tx_data.get('fecha', '')}")
    ws.cell(row=7, column=13, value="PAGADO A / TERCERO:").font = bold_font
    ws.cell(row=7, column=14, value=tx_data.get("tercero", ""))
    ws.cell(row=8, column=13, value="NIT / CC:").font = bold_font
    ws.cell(row=8, column=14, value=tx_data.get("nit_tercero", ""))
    ws.cell(row=9, column=13, value="LA SUMA DE (LETRAS):").font = bold_font
    ws.cell(row=9, column=14, value=tx_data.get("suma_letras", ""))
    ws.cell(row=10, column=13, value="POR CONCEPTO DE:").font = bold_font
    ws.cell(row=10, column=14, value=tx_data.get("concepto_soporte", tx_data.get("enunciado", "")))
    ws.cell(row=11, column=13, value="CHEQUE / MEDIO PAGO:").font = bold_font
    ws.cell(row=11, column=14, value=tx_data.get("cheque", "Contado / Crédito"))
    ws.cell(row=13, column=13, value="ELABORADO POR:").font = bold_font
    ws.cell(row=14, column=13, value=tx_data.get("elaborado_por", "GINA VILLAMIZAR")).font = bold_font

    for col_i, width in [(2, 26), (4, 18), (7, 14), (8, 38), (9, 16), (10, 16), (11, 16), (13, 22), (14, 34)]:
        ws.column_dimensions[openpyxl.utils.get_column_letter(col_i)].width = width

    # 2. Actualizar Kardex si aplica
    if kardex_updated:
        k_title = f"Kardex {kardex_updated.get('referencia', 'PROD')}"[:31]
        for existing_s in wb.sheetnames:
            if kardex_updated.get("referencia", "").lower() in existing_s.lower():
                k_title = existing_s
                break
        if k_title in wb.sheetnames:
            ws_k = wb[k_title]
            ws_k.delete_rows(1, ws_k.max_row + 10)
        else:
            ws_k = wb.create_sheet(title=k_title)

        ws_k["B2"] = "KARDEX PROMEDIO PONDERADO"
        ws_k["B2"].font = white_font
        ws_k["B2"].fill = navy_fill
        ws_k["B4"] = "ARTÍCULO:"
        ws_k["C4"] = kardex_updated.get("articulo", "")
        ws_k["E4"] = "REFERENCIA:"
        ws_k["F4"] = kardex_updated.get("referencia", "")

        k_headers = ["FECHA", "DESCRIPCIÓN", "DOCUMENTO", "VLR UNITARIO", "ENTRADAS CANT", "ENTRADAS VALOR", "SALIDAS CANT", "SALIDAS VALOR", "SALDO CANT", "SALDO VALOR", "COSTO PROMEDIO"]
        for ci, kh in enumerate(k_headers, start=2):
            ck = ws_k.cell(row=6, column=ci, value=kh)
            ck.font = gold_font
            ck.fill = gold_fill
            ck.border = border

        for r_i, mov in enumerate(kardex_updated.get("movimientos", []), start=7):
            vals = [
                mov.get("fecha", ""), mov.get("descripcion", ""), mov.get("doc", ""),
                mov.get("vlr_unitario", 0), mov.get("ent_cant", 0), mov.get("ent_valor", 0),
                mov.get("sal_cant", 0), mov.get("sal_valor", 0), mov.get("saldo_cant", 0),
                mov.get("saldo_valor", 0), mov.get("promedio", 0)
            ]
            for ci, v in enumerate(vals, start=2):
                cell_k = ws_k.cell(row=r_i, column=ci, value=v)
                cell_k.border = border
                if ci in (5, 7, 9, 11, 12):
                    cell_k.number_format = '"$"#,##0.00'

    # 3. Actualizar hoja de Libros Auxiliares en Vivo si tenemos las transacciones del mes
    if db_mes and db_mes.get("transacciones"):
        aux_sheet_name = "L.AUXILIARES VIVO"
        if aux_sheet_name in wb.sheetnames:
            ws_a = wb[aux_sheet_name]
            ws_a.delete_rows(1, ws_a.max_row + 10)
        else:
            ws_a = wb.create_sheet(title=aux_sheet_name)

        ws_a["B1"] = f"LIBROS AUXILIARES POR SUBCUENTA Y TERCERO EN VIVO — {mes_upper}"
        ws_a["B1"].font = white_font
        ws_a["B1"].fill = navy_fill

        headers_aux = ["CÓDIGO SUBCUENTA/AUX", "NOMBRE SUBCUENTA / TERCERO", "FECHA", "HOJA / SOPORTE", "DESCRIPCIÓN", "ENTRADA (DEBE)", "SALIDA (HABER)", "SALDO ACUMULADO"]
        for ci, h in enumerate(headers_aux, start=2):
            ca = ws_a.cell(row=3, column=ci, value=h)
            ca.font = gold_font
            ca.fill = gold_fill
            ca.border = border

        row_ptr = 4
        # Agrupar por subcuenta/auxiliar (>=6 dígitos)
        grouped = {}
        for t in db_mes["transacciones"]:
            # Identificar si la cuenta mayor fue debitada o acreditada para distribuir parciales
            last_mayor_side = "DEBE"
            for a in t.get("asientos", []):
                cod = str(a.get("codigo", ""))
                if len(cod) == 4:
                    last_mayor_side = "DEBE" if (a.get("debe", 0) or 0) > 0 else "HABER"
                elif len(cod) >= 6:
                    val_p = float(a.get("parcial", 0) or a.get("debe", 0) or a.get("haber", 0) or 0)
                    if val_p > 0:
                        grouped.setdefault(cod, {"nombre": a.get("cuenta", ""), "movs": []})["movs"].append({
                            "fecha": t.get("fecha", ""),
                            "hoja": t.get("hoja", ""),
                            "desc": t.get("enunciado", "")[:65],
                            "debe": val_p if last_mayor_side == "DEBE" else 0.0,
                            "haber": val_p if last_mayor_side == "HABER" else 0.0
                        })

        for cod in sorted(grouped.keys()):
            info = grouped[cod]
            saldo = 0.0
            is_debit_nat = cod[0] in ("1", "5", "6")
            for m in info["movs"]:
                saldo += (m["debe"] - m["haber"]) if is_debit_nat else (m["haber"] - m["debe"])
                vals = [cod, info["nombre"], m["fecha"], f"Hoja {m['hoja']}", m["desc"], m["debe"], m["haber"], saldo]
                for ci, v in enumerate(vals, start=2):
                    c = ws_a.cell(row=row_ptr, column=ci, value=v)
                    c.border = border
                    if ci in (7, 8, 9):
                        c.number_format = '"$"#,##0.00'
                row_ptr += 1

    wb.save(xlsx_path)
    if ws_id == "electrovivienda" and mes_upper == "ABRIL":
        shutil.copy2(xlsx_path, os.path.join(BASE_DIR, "ABRIL"))

    return xlsx_name

class StudentContHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, payload, status=200):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        accept_enc = self.headers.get("Accept-Encoding", "")
        if "gzip" in accept_enc and len(raw) > 1024:
            raw = gzip.compress(raw, compresslevel=5)
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Encoding", "gzip")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/db":
            qs = urllib.parse.parse_qs(parsed.query)
            ws_id = qs.get("ws", [None])[0]
            if ws_id:
                idx = get_workspaces_index()
                idx["active_id"] = ws_id
                save_workspaces_index(idx)
            db = load_db(ws_id)
            return self.send_json(db)
        elif parsed.path == "/api/version":
            idx = get_workspaces_index()
            db = load_db(idx.get("active_id", "electrovivienda"))
            return self.send_json({"ok": True, "actualizado": db.get("meta", {}).get("actualizado", "")})
        elif parsed.path.startswith("/api/ia/doc/"):
            fname = urllib.parse.unquote(parsed.path.replace("/api/ia/doc/", ""))
            safe_name = os.path.basename(fname)
            fpath = os.path.join(IA_DOCS_DIR, safe_name)
            if not os.path.exists(fpath):
                fpath = os.path.join(BASE_DIR, safe_name)
            if os.path.exists(fpath) and os.path.isfile(fpath):
                with open(fpath, "rb") as f:
                    data = f.read()
                self.send_response(200)
                if safe_name.lower().endswith(".pdf"):
                    self.send_header("Content-Type", "application/pdf")
                elif safe_name.lower().endswith((".xlsx", ".xlsm")):
                    self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                else:
                    self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            return self.send_json({"error": "Documento no encontrado"}, 404)
        elif parsed.path.startswith("/api/download/"):
            fname = urllib.parse.unquote(parsed.path.replace("/api/download/", ""))
            safe_name = os.path.basename(fname)
            fpath = os.path.join(BASE_DIR, safe_name)
            if os.path.exists(fpath) and os.path.isfile(fpath):
                with open(fpath, "rb") as f:
                    data = f.read()
                self.send_response(200)
                if safe_name.endswith(".xlsx") or safe_name == "ABRIL":
                    self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                elif safe_name.endswith(".pdf"):
                    self.send_header("Content-Type", "application/pdf")
                else:
                    self.send_header("Content-Type", "application/octet-stream")
                dl_name = safe_name if ("." in safe_name) else f"{safe_name}.xlsx"
                self.send_header("Content-Disposition", f'attachment; filename="{dl_name}"')
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            return self.send_json({"error": "Archivo no encontrado"}, 404)
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}

        if parsed.path == "/api/transaccion":
            idx = get_workspaces_index()
            active_ws = idx.get("active_id", "electrovivienda")
            db = load_db(active_ws)
            mes = body.get("mes", "ABRIL").upper()
            if mes not in db["meses"]:
                db["meses"][mes] = {
                    "archivo": get_excel_filename_for_workspace(active_ws, mes),
                    "hojas": ["PUC"],
                    "total_transacciones": 0,
                    "transacciones": [],
                    "hojas_especiales": {}
                }

            tx = body.get("transaccion", {})
            tx["empresa_nombre"] = db["empresa"]["razon_social"]
            tx["empresa_nit"] = f"NIT {db['empresa']['nit']}"
            kardex_mov = body.get("kardex_movimiento")
            nuevo_prod = body.get("nuevo_producto_kardex")
            nuevos_aux = body.get("nuevos_auxiliares_puc") or []
            factura_detalle = body.get("factura_detalle")

            # 1. Registrar automáticamente nuevos auxiliares de 8 dígitos en el PUC si no existen
            if "puc" not in db or not isinstance(db["puc"], list):
                db["puc"] = []
            existing_codes = {str(c.get("codigo", "")).strip() for c in db["puc"]}
            added_puc = False
            for aux in nuevos_aux:
                acode = str(aux.get("codigo", "")).strip()
                aname = str(aux.get("nombre", "")).strip()
                if acode and acode not in existing_codes:
                    db["puc"].append({
                        "codigo": acode,
                        "nombre": aname,
                        "nivel": "Auxiliar (8 dígitos - Automático)"
                    })
                    existing_codes.add(acode)
                    added_puc = True
            if added_puc:
                db["puc"].sort(key=lambda x: str(x.get("codigo", "")))

            # 2. Agregar o reemplazar transacción en el mes correspondiente
            existing_txs = db["meses"][mes]["transacciones"]
            replaced = False
            for idx_t, t_old in enumerate(existing_txs):
                if str(t_old.get("hoja")) == str(tx.get("hoja")):
                    existing_txs[idx_t] = tx
                    replaced = True
                    break
            if not replaced:
                existing_txs.append(tx)
            db["meses"][mes]["total_transacciones"] = len(existing_txs)
            if tx.get("hoja") not in db["meses"][mes]["hojas"]:
                db["meses"][mes]["hojas"].append(tx.get("hoja"))

            # 3. Registrar la factura encadenada a su hoja, comprobante, kardex y auxiliares
            if factura_detalle:
                if "facturas" not in db:
                    db["facturas"] = []
                db["facturas"] = [f for f in db["facturas"] if f.get("id") != factura_detalle.get("id")]
                db["facturas"].insert(0, factura_detalle)

            # 4. Crear producto Kardex automáticamente si es nuevo y actualizar saldos Promedio Ponderado
            if "kardex" not in db or not isinstance(db["kardex"], list):
                db["kardex"] = []
            kardex_prod_updated = None
            if nuevo_prod and nuevo_prod.get("id"):
                if not any(p.get("id") == nuevo_prod["id"] or p.get("referencia") == nuevo_prod.get("referencia") for p in db["kardex"]):
                    db["kardex"].append({
                        "id": nuevo_prod["id"],
                        "referencia": nuevo_prod.get("referencia", nuevo_prod["id"]),
                        "articulo": nuevo_prod.get("articulo", "Mercancía Kardex"),
                        "metodo": "PROMEDIO PONDERADO",
                        "proveedor": nuevo_prod.get("proveedor", tx.get("tercero", "")),
                        "auxiliar_puc": nuevo_prod.get("auxiliar_puc", "14353601"),
                        "movimientos": []
                    })

            if kardex_mov and kardex_mov.get("producto_id"):
                pid = kardex_mov["producto_id"]
                for prod in db["kardex"]:
                    if prod["id"] == pid or prod["referencia"] == pid:
                        prod["movimientos"].append(kardex_mov["registro"])
                        # Recalcular saldos y costo promedio ponderado encadenado
                        sc = 0.0
                        sv = 0.0
                        for mv in prod["movimientos"]:
                            ec = float(mv.get("ent_cant") or 0)
                            ev = float(mv.get("ent_valor") or 0)
                            salc = float(mv.get("sal_cant") or 0)
                            salv = float(mv.get("sal_valor") or 0)
                            if salc > 0 and salv == 0 and sc > 0:
                                prom_actual = sv / sc
                                salv = round(salc * prom_actual)
                                mv["sal_valor"] = salv
                                mv["vlr_unitario"] = round(prom_actual)
                            sc += ec - salc
                            sv += ev - salv
                            mv["saldo_cant"] = sc
                            mv["saldo_valor"] = round(sv)
                            mv["promedio"] = round(sv / sc, 2) if sc > 0 else float(mv.get("vlr_unitario") or 0)
                        kardex_prod_updated = prod
                        break

            save_db(db, active_ws)
            excel_file = write_transaction_to_excel(active_ws, mes, tx, kardex_prod_updated, db["meses"][mes])
            db["workspaces_info"] = get_workspaces_index()
            return self.send_json({
                "ok": True,
                "mensaje": f"Guardado y sincronizado en {excel_file} (Comprobante + Kardex + Libros Auxiliares en Vivo)",
                "archivo_excel": excel_file,
                "db": db
            })

        elif parsed.path == "/api/workspace/create":
            # Crear una nueva empresa o taller práctico 100% EN CERO ($0 en los 12 meses, sin arrastrar datos de otra empresa)
            idx = get_workspaces_index()
            base_electro = load_db("electrovivienda")
            razon = body.get("razon_social", "TALLER PRÁCTICO CONTABLE S.A.S").strip()
            nit = body.get("nit", "900.000.000-1").strip()
            tipo_espacio = body.get("tipo", "PRÁCTICA DE APRENDIZAJE")
            regimen = body.get("regimen", "Régimen Responsable de IVA (RRI) - Agente de Retención y Autorretenedor en Renta")
            ciudad = body.get("ciudad", "Bucaramanga, Santander")
            elaborado = body.get("elaborado_por", "Estudiante")
            aporte_inicial = float(body.get("aporte_inicial", 0) or 0)

            ws_id = re.sub(r"[^a-z0-9]+", "_", razon.lower()).strip("_")[:24] + "_" + str(len(idx["workspaces"]) + 1)
            datafile = f"db_{ws_id}.json"

            digits = re.findall(r"\d", nit.split("-")[0])
            ultimo_digito = digits[-1] if digits else "1"

            txs_enero = []
            if aporte_inicial > 0:
                txs_enero.append({
                    "hoja": "1",
                    "mes": "ENERO",
                    "fecha": datetime.date.today().strftime("%Y-%m-%d"),
                    "tipo": "COMPROBANTE DE CONTABILIDAD",
                    "comprobante_diario": "Comprobante Diario N° 1 (Apertura)",
                    "num_comprobante_diario": 1,
                    "enunciado": f"Constitución e inicio de operaciones de {razon} ({nit}).",
                    "tercero": "Socios Fundadores",
                    "nit_tercero": nit,
                    "cheque": "Aporte Inicial",
                    "concepto_soporte": "Aportes sociales iniciales",
                    "suma_letras": f"{int(aporte_inicial):,} pesos M/CTE.",
                    "elaborado_por": elaborado,
                    "total_debe": aporte_inicial,
                    "total_haber": aporte_inicial,
                    "liquidacion": {"base": aporte_inicial, "neto": aporte_inicial},
                    "asientos": [
                        {"codigo": "1105", "cuenta": "CAJA", "parcial": 0, "debe": aporte_inicial, "haber": 0},
                        {"codigo": "110505", "cuenta": "Caja general", "parcial": aporte_inicial, "debe": 0, "haber": 0},
                        {"codigo": "3105", "cuenta": "CAPITAL SUSCRITO Y PAGADO", "parcial": 0, "debe": 0, "haber": aporte_inicial},
                        {"codigo": "310505", "cuenta": "Capital Autorizado y Pagado", "parcial": aporte_inicial, "debe": 0, "haber": 0}
                    ],
                    "rows": []
                })

            new_db = {
                "meta": {
                    "plataforma": "STUDENTCONT.IA",
                    "version": "2.3.0",
                    "actualizado": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "empresa": {
                    "razon_social": razon,
                    "nit": nit,
                    "nit_sin_dv": nit.split("-")[0],
                    "dv": nit.split("-")[1] if "-" in nit else "1",
                    "ultimo_digito_nit": ultimo_digito,
                    "regimen": regimen,
                    "grupo_niif": "Grupo 2 - NIIF para las PYMES (Decreto 2420 de 2015)",
                    "sistema_inventario": "Sistema de Inventario Permanente - Método Promedio Ponderado",
                    "direccion": body.get("direccion", "Sede Principal"),
                    "ciudad": ciudad,
                    "telefono": body.get("telefono", ""),
                    "correo": body.get("correo", ""),
                    "elaborado_por": elaborado,
                    "socios": [
                        {"nombre": elaborado, "documento": nit, "aporte": aporte_inicial}
                    ] if aporte_inicial > 0 else [],
                    "parametros_2026": base_electro["empresa"]["parametros_2026"]
                },
                "puc": base_electro["puc"],
                "facturas": [],
                "kardex": [],
                "calendario_tributario": [],
                "meses": {
                    m: {
                        "archivo": get_excel_filename_for_workspace(ws_id, m),
                        "hojas": ["PUC", "1"] if (m == "ENERO" and txs_enero) else ["PUC"],
                        "total_transacciones": len(txs_enero) if m == "ENERO" else 0,
                        "transacciones": txs_enero if m == "ENERO" else [],
                        "hojas_especiales": {}
                    } for m in ALL_12_MONTHS
                }
            }

            with open(os.path.join(DATA_DIR, datafile), "w", encoding="utf-8") as f:
                json.dump(new_db, f, ensure_ascii=False, indent=2)

            idx["workspaces"].append({
                "id": ws_id,
                "owner_id": body.get("owner_id", ""),
                "tipo": tipo_espacio,
                "razon_social": razon,
                "nit": nit,
                "regimen_corto": regimen[:48],
                "ciudad": ciudad,
                "datafile": datafile
            })
            idx["active_id"] = ws_id
            save_workspaces_index(idx)

            if txs_enero:
                write_transaction_to_excel(ws_id, "ENERO", txs_enero[0], None, new_db["meses"]["ENERO"])

            new_db["workspaces_info"] = idx
            new_db["student_profiles"] = sanitize_profiles_for_client(get_student_profiles())
            return self.send_json({"ok": True, "ws_id": ws_id, "db": new_db})

        elif parsed.path == "/api/workspace/sync-student-db":
            # Guardado exclusivo y aislado para el taller personal de un estudiante
            ws_id = body.get("workspace_id") or "taller_estudiante"
            student_id = body.get("student_id") or "default"
            client_db = body.get("db")
            if client_db and isinstance(client_db, dict) and "meses" in client_db:
                safe_ws = re.sub(r"[^a-z0-9_]+", "", ws_id.lower())
                if not safe_ws.startswith("taller_"):
                    safe_ws = "taller_" + safe_ws
                datafile = f"db_{safe_ws}.json"
                fpath = os.path.join(DATA_DIR, datafile)
                with open(fpath, "w", encoding="utf-8") as f:
                    json.dump(client_db, f, ensure_ascii=False, indent=2)

                idx = get_workspaces_index()
                if not any(w.get("id") == safe_ws for w in idx.get("workspaces", [])):
                    idx.setdefault("workspaces", []).append({
                        "id": safe_ws,
                        "owner_id": student_id,
                        "tipo": "PRÁCTICA DE APRENDIZAJE",
                        "razon_social": client_db.get("empresa", {}).get("razon_social", f"TALLER CONTABLE DE {student_id.upper()}"),
                        "nit": client_db.get("empresa", {}).get("nit", "901.765.438-3"),
                        "regimen_corto": "Régimen Responsable de IVA",
                        "ciudad": "Bucaramanga, Santander",
                        "datafile": datafile
                    })
                    save_workspaces_index(idx)
                return self.send_json({"ok": True, "workspace_id": safe_ws, "message": "Taller sincronizado en archivo aislado"})
            return self.send_json({"ok": False, "error": "Datos inválidos"}, status=400)

        elif parsed.path == "/api/auth/login":
            # Inicio de sesión privado con usuario/correo/nombre + contraseña
            ident = (body.get("usuario") or "").strip().lower()
            pin = (body.get("pin") or body.get("password") or "").strip()
            profiles = get_student_profiles()
            matched = None
            is_gina_ident = ident in ("gina", "gina villamizar", "ginavillamizar", "gina.villamizar@studentcont.ia") or "gina" in ident

            for p in profiles:
                p_user = (p.get("usuario") or "").strip().lower()
                p_mail = (p.get("correo") or "").strip().lower()
                p_name = (p.get("nombre") or "").strip().lower()
                u_match = (
                    ident == p_user or
                    ident == p_mail or
                    ident == p_name or
                    (p.get("id") == "gina_villamizar" and is_gina_ident)
                )
                if u_match:
                    stored_pin = str(p.get("pin") or "").strip()
                    # Si es Gina (titular) y no había personalizado clave o usa su clave o clave maestra gina2026
                    if p.get("id") == "gina_villamizar":
                        if not p.get("custom_pin_set") or pin == stored_pin or pin.lower() in ("gina2026", "gina", "1234", "123456", "901765438", "901.765.438-3"):
                            p["pin"] = pin
                            p["custom_pin_set"] = True
                            save_student_profiles(profiles)
                            matched = p
                    elif not stored_pin or stored_pin == pin:
                        p["pin"] = pin
                        save_student_profiles(profiles)
                        matched = p
                    break
            if not matched:
                return self.send_json({"ok": False, "error": "Usuario o contraseña incorrectos. Verifica tus datos o crea tu perfil abajo."}, 401)
            ws_id = matched.get("workspace_id", "electrovivienda")
            idx = get_workspaces_index()
            idx["active_id"] = ws_id
            save_workspaces_index(idx)
            db = load_db(ws_id)
            safe_prof = {
                "id": matched["id"],
                "nombre": matched["nombre"],
                "correo": matched.get("correo", ""),
                "programa": matched.get("programa", ""),
                "rol": matched.get("rol", "Estudiante Independiente"),
                "workspace_id": ws_id
            }
            return self.send_json({"ok": True, "perfil": safe_prof, "db": db})

        elif parsed.path == "/api/auth/register":
            # Registro de perfil privado de estudiante con contraseña y taller 100% en $0
            nombre = (body.get("nombre") or "").strip()
            correo = (body.get("correo") or "").strip()
            pin = (body.get("pin") or "").strip()
            programa = (body.get("programa") or "Contaduría Pública • NIIF").strip()
            emp_nombre = (body.get("empresa_nombre") or f"TALLER CONTABLE DE {nombre.upper()}").strip()
            nit_acceso = (body.get("nit_empresa_existente") or "").strip()

            if not nombre or not pin:
                return self.send_json({"ok": False, "error": "Debes ingresar tu Nombre/Usuario y una Contraseña privada."}, 400)

            profiles = get_student_profiles()
            # Si Gina llena el formulario de registro con su nombre, actualizarle su contraseña y abrirle ELECTROVIVIENDA directo
            if nombre.lower() in ("gina", "gina villamizar", "ginavillamizar") or "gina villamizar" in nombre.lower():
                for p in profiles:
                    if p.get("id") == "gina_villamizar":
                        p["pin"] = pin
                        p["custom_pin_set"] = True
                        if correo:
                            p["correo"] = correo
                        save_student_profiles(profiles)
                        idx = get_workspaces_index()
                        idx["active_id"] = "electrovivienda"
                        save_workspaces_index(idx)
                        db = load_db("electrovivienda")
                        safe_prof = {
                            "id": p["id"],
                            "nombre": p["nombre"],
                            "correo": p.get("correo", ""),
                            "programa": p.get("programa", ""),
                            "rol": p.get("rol", "Titular / Administradora"),
                            "workspace_id": "electrovivienda"
                        }
                        return self.send_json({"ok": True, "perfil": safe_prof, "db": db})

            for p in profiles:
                if nombre.lower() == (p.get("nombre") or "").lower() or (correo and correo.lower() == (p.get("correo") or "").lower()):
                    if not p.get("pin") or p.get("pin") == pin:
                        p["pin"] = pin
                        save_student_profiles(profiles)
                        ws_existing = p.get("workspace_id", "electrovivienda")
                        db = load_db(ws_existing)
                        return self.send_json({"ok": True, "perfil": p, "db": db})
                    return self.send_json({"ok": False, "error": "Este nombre ya tiene una contraseña privada diferente. Usa el recuadro 1 de Iniciar Sesión."}, 400)

            stu_id = "stu_" + re.sub(r"[^a-z0-9]+", "_", nombre.lower()).strip("_")[:18] + "_" + str(len(profiles) + 1)

            # Crear siempre su propio taller en CERO ($0 en los 12 meses, sin información de otra empresa)
            idx = get_workspaces_index()
            base_electro = load_db("electrovivienda")
            ws_id = f"taller_{stu_id}"
            datafile = f"db_{ws_id}.json"

            empty_db = {
                "meta": {
                    "plataforma": "STUDENTCONT.IA",
                    "version": "2.3.0",
                    "actualizado": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "empresa": {
                    "razon_social": emp_nombre,
                    "nit": "900.000.000-1",
                    "nit_sin_dv": "900000000",
                    "dv": "1",
                    "ultimo_digito_nit": "0",
                    "regimen": "Régimen Responsable de IVA (RRI) - Agente de Retención y Autorretenedor en Renta",
                    "grupo_niif": "Grupo 2 - NIIF para las PYMES (Decreto 2420 de 2015)",
                    "sistema_inventario": "Sistema de Inventario Permanente - Método Promedio Ponderado",
                    "direccion": "Sede Académica",
                    "ciudad": "Bucaramanga, Santander",
                    "telefono": "",
                    "correo": correo,
                    "elaborado_por": nombre,
                    "socios": [],
                    "parametros_2026": base_electro["empresa"]["parametros_2026"]
                },
                "puc": base_electro["puc"],
                "facturas": [],
                "kardex": [],
                "calendario_tributario": [],
                "meses": {
                    m: {
                        "archivo": get_excel_filename_for_workspace(ws_id, m),
                        "hojas": ["PUC"],
                        "total_transacciones": 0,
                        "transacciones": [],
                        "hojas_especiales": {}
                    } for m in ALL_12_MONTHS
                }
            }
            with open(os.path.join(DATA_DIR, datafile), "w", encoding="utf-8") as f:
                json.dump(empty_db, f, ensure_ascii=False, indent=2)

            idx["workspaces"].append({
                "id": ws_id,
                "owner_id": stu_id,
                "tipo": "PRÁCTICA DE APRENDIZAJE (EN $0)",
                "razon_social": emp_nombre,
                "nit": "900.000.000-1",
                "regimen_corto": "RRI • Taller Práctico en $0",
                "ciudad": "Bucaramanga, Santander",
                "datafile": datafile
            })

            # Si el estudiante digitó el NIT exacto de ELECTROVIVIENDA (901.765.438-3 o 901765438), abrirle acceso a ELECTROVIVIENDA
            clean_nit_input = re.sub(r"[^0-9]", "", nit_acceso)
            target_ws_to_load = ws_id
            if clean_nit_input in ("9017654383", "901765438"):
                target_ws_to_load = "electrovivienda"

            idx["active_id"] = target_ws_to_load
            save_workspaces_index(idx)

            new_profile = {
                "id": stu_id,
                "usuario": correo or nombre,
                "nombre": nombre,
                "correo": correo,
                "pin": pin,
                "programa": programa,
                "rol": "Estudiante Independiente",
                "workspace_id": ws_id,
                "creado": datetime.date.today().strftime("%Y-%m-%d")
            }
            profiles.append(new_profile)
            save_student_profiles(profiles)

            loaded_db = load_db(target_ws_to_load)
            safe_prof = {
                "id": stu_id,
                "nombre": nombre,
                "correo": correo,
                "programa": programa,
                "rol": "Estudiante Independiente",
                "workspace_id": ws_id
            }
            return self.send_json({"ok": True, "perfil": safe_prof, "db": loaded_db})

        elif parsed.path == "/api/empresa/acceso-nit":
            # Permite que un estudiante con su perfil personal acceda a una empresa (como ELECTROVIVIENDA) únicamente ingresando su NIT exacto
            nit_raw = (body.get("nit") or "").strip()
            clean_nit = re.sub(r"[^0-9]", "", nit_raw)
            idx = get_workspaces_index()
            found_ws = None
            for w in idx["workspaces"]:
                w_nit_clean = re.sub(r"[^0-9]", "", w.get("nit", ""))
                if clean_nit and (clean_nit == w_nit_clean or (len(clean_nit) >= 9 and w_nit_clean.startswith(clean_nit[:9]))):
                    found_ws = w
                    break
            if not found_ws:
                return self.send_json({"ok": False, "error": "No se encontró ninguna empresa registrada con ese NIT. Verifica el NIT e intenta de nuevo."}, 404)
            idx["active_id"] = found_ws["id"]
            save_workspaces_index(idx)
            db = load_db(found_ws["id"])
            return self.send_json({"ok": True, "empresa": found_ws["razon_social"], "db": db})

        elif parsed.path == "/api/kardex/producto":
            db = load_db()
            nuevo = body.get("producto", {})
            if nuevo:
                db["kardex"].append(nuevo)
                save_db(db)
            db["workspaces_info"] = get_workspaces_index()
            return self.send_json({"ok": True, "db": db})

        elif parsed.path == "/api/calendario/estado":
            db = load_db()
            cal_id = body.get("id")
            nuevo_estado = body.get("estado")
            nuevo_item = body.get("nuevo_item")
            if nuevo_item:
                db["calendario_tributario"].append(nuevo_item)
            elif cal_id:
                for item in db["calendario_tributario"]:
                    if item["id"] == cal_id:
                        item["estado"] = nuevo_estado
                        if "valor_pagado" in body:
                            item["valor_pagado"] = body["valor_pagado"]
                        break
            save_db(db)
            db["workspaces_info"] = get_workspaces_index()
            db["student_profiles"] = get_student_profiles()
            return self.send_json({"ok": True, "db": db})

        elif parsed.path == "/api/perfiles":
            profiles = get_student_profiles()
            nuevo_p = body.get("perfil")
            if nuevo_p and nuevo_p.get("nombre"):
                profiles.append(nuevo_p)
                save_student_profiles(profiles)
            return self.send_json({"ok": True, "student_profiles": profiles})

        elif parsed.path == "/api/ia/conocimiento":
            kb = get_ia_custom_kb()
            item = body.get("item")
            if item and item.get("tema"):
                kb.insert(0, item)
                save_ia_custom_kb(kb)
            return self.send_json({"ok": True, "ia_custom_kb": kb})

        elif parsed.path == "/api/ia/ingest-url":
            url = (body.get("url") or "").strip()
            custom_title = (body.get("titulo") or "").strip()
            publicar_reforma = bool(body.get("publicar_reforma", False))
            categoria_ref = (body.get("categoria") or "TRIBUTARIA").strip()
            autor = (body.get("autor") or "Gina Villamizar").strip()

            if not url:
                return self.send_json({"ok": False, "error": "Por favor ingresa un link o URL válida (https://...)."}, 400)
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            try:
                info = extract_text_from_webpage_url(url)
            except Exception as e:
                return self.send_json({"ok": False, "error": f"No se pudo leer la página ({str(e)[:90]}). Verifica el enlace."}, 400)

            tema_final = custom_title or info["title"]
            kb = get_ia_custom_kb()
            new_kb_item = {
                "id": f"KB-URL-{int(datetime.datetime.now().timestamp())}",
                "tema": tema_final,
                "keywords": info["keywords"],
                "contenido": info["summary"],
                "texto_completo": info["full_text"],
                "fuente_tipo": "LINK WEB",
                "fuente_url": url,
                "autor": autor,
                "fecha": datetime.date.today().strftime("%Y-%m-%d")
            }
            kb.insert(0, new_kb_item)
            save_ia_custom_kb(kb)

            refs = get_custom_reformas()
            if publicar_reforma:
                refs.insert(0, {
                    "id": f"REF-URL-{int(datetime.datetime.now().timestamp())}",
                    "categoria": categoria_ref,
                    "norma": f"Fuente Web: {urllib.parse.urlparse(url).netloc}",
                    "titulo": tema_final,
                    "vigencia": f"Link indexado el {datetime.date.today().strftime('%Y-%m-%d')}",
                    "resumen": info["summary"][:650],
                    "impacto_contable": f"Enlace original: {url}\nPalabras clave: {info['keywords']}",
                    "fuente_url": url
                })
                save_custom_reformas(refs)

            return self.send_json({
                "ok": True,
                "item": new_kb_item,
                "ia_custom_kb": kb,
                "custom_reformas": refs
            })

        elif parsed.path == "/api/ia/ingest-document":
            filename = os.path.basename((body.get("filename") or "documento.txt").strip())
            b64_data = body.get("base64_data") or ""
            client_text = (body.get("extracted_text") or "").strip()
            custom_title = (body.get("titulo") or "").strip()
            publicar_reforma = bool(body.get("publicar_reforma", False))
            categoria_ref = (body.get("categoria") or "NIIF").strip()
            autor = (body.get("autor") or "Gina Villamizar").strip()
            local_Server_file = (body.get("local_server_file") or "").strip()

            safe_fname = re.sub(r"[^a-zA-Z0-9._()-]", "_", filename)
            saved_path = os.path.join(IA_DOCS_DIR, safe_fname)

            if local_Server_file:
                cand = os.path.join(BASE_DIR, os.path.basename(local_Server_file))
                if os.path.exists(cand):
                    saved_path = cand
                    safe_fname = os.path.basename(cand)
            elif b64_data:
                if "," in b64_data:
                    b64_data = b64_data.split(",", 1)[1]
                raw_bytes = base64.b64decode(b64_data)
                with open(saved_path, "wb") as f:
                    f.write(raw_bytes)

            server_text = ""
            if os.path.exists(saved_path):
                try:
                    server_text = extract_text_from_uploaded_file(saved_path, safe_fname)
                except Exception:
                    server_text = ""

            full_text = client_text if len(client_text) >= len(server_text) else server_text
            if not full_text:
                full_text = f"Documento cargado: {filename}. disponible para consulta en la plataforma."

            tema_final = custom_title or f"Documento: {filename}"
            keywords = extract_keywords_from_text(tema_final, full_text)
            summary = full_text[:1800]

            kb = get_ia_custom_kb()
            doc_url = f"/api/ia/doc/{urllib.parse.quote(safe_fname)}"
            new_kb_item = {
                "id": f"KB-DOC-{int(datetime.datetime.now().timestamp())}",
                "tema": tema_final,
                "keywords": keywords,
                "contenido": summary,
                "texto_completo": full_text[:35000],
                "fuente_tipo": "DOCUMENTO",
                "fuente_archivo": filename,
                "fuente_url": doc_url,
                "autor": autor,
                "fecha": datetime.date.today().strftime("%Y-%m-%d")
            }
            kb.insert(0, new_kb_item)
            save_ia_custom_kb(kb)

            refs = get_custom_reformas()
            if publicar_reforma:
                refs.insert(0, {
                    "id": f"REF-DOC-{int(datetime.datetime.now().timestamp())}",
                    "categoria": categoria_ref,
                    "norma": f"Documento: {filename}",
                    "titulo": tema_final,
                    "vigencia": f"Documento indexado el {datetime.date.today().strftime('%Y-%m-%d')}",
                    "resumen": summary[:650],
                    "impacto_contable": f"Archivo adjunto: {filename}\nPalabras clave: {keywords}",
                    "fuente_url": doc_url
                })
                save_custom_reformas(refs)

            return self.send_json({
                "ok": True,
                "item": new_kb_item,
                "ia_custom_kb": kb,
                "custom_reformas": refs
            })

        elif parsed.path == "/api/ia/delete-kb":
            target_id = body.get("id")
            kb = [k for k in get_ia_custom_kb() if k.get("id") != target_id and k.get("tema") != target_id]
            save_ia_custom_kb(kb)
            return self.send_json({"ok": True, "ia_custom_kb": kb})

        elif parsed.path == "/api/reformas":
            refs = get_custom_reformas()
            item = body.get("reforma")
            if item and item.get("titulo"):
                refs.insert(0, item)
                save_custom_reformas(refs)
            return self.send_json({"ok": True, "custom_reformas": refs})

        return self.send_json({"error": "Ruta no soportada"}, 404)

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    port = int(os.environ.get("PORT", 8090))
    server = ThreadingHTTPServer(("127.0.0.1", port), StudentContHandler)
    print(f"STUDENTCONT.IA (Base Local) ejecutándose en http://localhost:{port} desde {BASE_DIR}")
    server.serve_forever()

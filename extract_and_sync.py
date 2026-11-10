#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor y Sincronizador Contable para STUDENTCONT.IA - ELECTROVIVIENDA S.A.S
Extrae toda la información de ENERO.xlsx, FEBRERO.xlsx, MARZO.xlsx y ABRIL(.xlsx)
y genera el Calendario Tributario 2026 en Excel + base de datos JSON completa.
"""

import os
import re
import json
import shutil
import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE_DIR = "/Users/ginavillamizar/Downloads/CONTABILIDAD"
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Asegurar que ABRIL tenga también versión ABRIL.xlsx con extensión válida
abril_raw = os.path.join(BASE_DIR, "ABRIL")
abril_xlsx = os.path.join(BASE_DIR, "ABRIL.xlsx")
if os.path.exists(abril_raw) and not os.path.exists(abril_xlsx):
    shutil.copy2(abril_raw, abril_xlsx)

def clean_val(v):
    if v is None:
        return None
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        if v.is_integer():
            return int(v)
        return round(v, 2)
    return str(v).strip()

def sheet_to_rows(ws, max_rows=250, max_cols=48):
    rows = []
    for r_idx, row in enumerate(ws.iter_rows(max_row=max_rows, max_col=max_cols, values_only=True), 1):
        cleaned = [clean_val(c) for c in row]
        while cleaned and cleaned[-1] is None:
            cleaned.pop()
        if any(c is not None and c != "" for c in cleaned):
            rows.append({"row": r_idx, "cells": cleaned})
    return rows

def extract_puc(wb):
    if "PUC" not in wb.sheetnames:
        return []
    ws = wb["PUC"]
    puc_list = []
    seen = set()
    for row in ws.iter_rows(values_only=True):
        vals = [clean_val(c) for c in row if clean_val(c) is not None and clean_val(c) != ""]
        if len(vals) >= 2:
            code = str(vals[0]).strip()
            name = str(vals[1]).strip()
            if re.match(r"^\d+$", code) and code not in seen:
                seen.add(code)
                nivel = "Clase" if len(code) == 1 else "Grupo" if len(code) == 2 else "Cuenta" if len(code) == 4 else "Subcuenta" if len(code) == 6 else "Auxiliar"
                naturaleza = "Débito" if code[0] in ("1", "5", "6", "7") else "Crédito"
                puc_list.append({
                    "codigo": code,
                    "nombre": name,
                    "nivel": nivel,
                    "naturaleza": naturaleza
                })
    return puc_list

def parse_transaction_sheet(ws, sheet_name, month_name):
    rows = sheet_to_rows(ws, max_rows=140, max_cols=30)
    all_text = []
    fecha = None
    enunciado = ""
    tipo_doc = "COMPROBANTE DE CONTABILIDAD"
    cheque = ""
    pagado_a = ""
    concepto_soporte = ""
    suma_letras = ""
    asientos = []

    for r in rows:
        cells = r["cells"]
        non_empty = [(i, c) for i, c in enumerate(cells) if c is not None and str(c).strip() != ""]
        for i, c in non_empty:
            s = str(c)
            if not fecha and re.match(r"^2026-\d{2}-\d{2}$", s):
                fecha = s
            s_up = s.upper()
            if "COMPROBANTE DE EGRESO" in s_up:
                tipo_doc = "COMPROBANTE DE EGRESO"
            elif "COMPROBANTE DE INGRESO" in s_up or "RECIBO DE CAJA" in s_up:
                tipo_doc = "COMPROBANTE DE INGRESO"
            elif "NOTA CRÉDITO" in s_up or "DEVOLUCIÓN" in s_up or "DEVOLUCION" in s_up:
                tipo_doc = "NOTA CRÉDITO / DEVOLUCIÓN"
            elif "FACTURA" in s_up and ("VENDEMOS" in s_up or "VENTA" in s_up):
                tipo_doc = "FACTURA DE VENTA"
            elif "COMPRAMOS" in s_up and tipo_doc == "COMPROBANTE DE CONTABILIDAD":
                tipo_doc = "FACTURA DE COMPRA"
            elif "NOMINA" in s_up or "NÓMINA" in s_up:
                if tipo_doc == "COMPROBANTE DE CONTABILIDAD":
                    tipo_doc = "COMPROBANTE DE NÓMINA"
            elif "DEPRECIACIÓN" in s_up or "DEPRECIACION" in s_up:
                tipo_doc = "NOTA DE AJUSTE / DEPRECIACIÓN"

            if (s.startswith("El día") or s.startswith("El dia") or s.startswith("La sociedad") or
                s.startswith("Se abre") or s.startswith("Bancolombia") or s.startswith("Giramos") or
                s.startswith("Causamos") or s.startswith("Compramos") or s.startswith("Recibimos") or
                s.startswith("Vendemos") or s.startswith("Realizar") or s.startswith("Se diligencia") or
                s.startswith("No se hace")) and len(s) > len(enunciado):
                enunciado = s

            if "PAGADO A:" in s_up or "RECIBIDO DE:" in s_up:
                for j in range(i + 1, min(i + 5, len(cells))):
                    if cells[j]:
                        pagado_a = str(cells[j])
                        break
            if "POR CONCEPTO DE:" in s_up:
                for j in range(i + 1, min(i + 6, len(cells))):
                    if cells[j]:
                        concepto_soporte = str(cells[j])
                        break
            if "LA SUMA DE" in s_up:
                for j in range(i + 1, min(i + 6, len(cells))):
                    if cells[j]:
                        suma_letras = str(cells[j])
                        break
            if "CHEQUE" in s_up and not cheque:
                m = re.search(r"(?:No\.?|N°|#)\s*(\d+)", s, re.I)
                if m:
                    cheque = m.group(1)
                else:
                    for j in range(i + 1, min(i + 4, len(cells))):
                        if cells[j] and re.match(r"^\d+$", str(cells[j])):
                            cheque = str(cells[j])
                            break

        # Detectar encabezados CODIGO | CUENTA | PARCIAL | DEBE | HABER (tabla de contabilización principal usa DEBE y HABER)
        for idx in range(len(cells)):
            if cells[idx] is not None and str(cells[idx]).strip().upper() in ("CODIGO", "CÓDIGO"):
                c_cta, c_par, c_deb, c_hab = None, None, None, None
                for k in range(idx + 1, min(idx + 10, len(cells))):
                    v_str = str(cells[k]).strip().upper() if cells[k] is not None else ""
                    if v_str in ("CUENTA", "CUENTAS") and c_cta is None:
                        c_cta = k
                    elif v_str in ("PARCIAL", "PARCIALES") and c_par is None:
                        c_par = k
                    elif v_str == "DEBE" and c_deb is None:
                        c_deb = k
                    elif v_str == "HABER" and c_hab is None:
                        c_hab = k
                if c_cta is not None and c_deb is not None and c_hab is not None:
                    active_cols = (idx, c_cta, c_par, c_deb, c_hab)
                    break

        if "active_cols" in locals() and active_cols is not None:
            col_cod, col_cta, col_par, col_deb, col_hab = active_cols
            if col_cod < len(cells) and cells[col_cod] is not None:
                c_val_str = str(cells[col_cod]).strip()
                if re.match(r"^\d{4,8}$", c_val_str):
                    cta_name = str(cells[col_cta]).strip() if col_cta < len(cells) and cells[col_cta] is not None else ""
                    def num_at(col_i):
                        if col_i is not None and col_i < len(cells) and isinstance(cells[col_i], (int, float)):
                            return round(float(cells[col_i]), 2)
                        return 0.0
                    parcial = num_at(col_par)
                    debe = num_at(col_deb)
                    haber = num_at(col_hab)
                    if cta_name:
                        asientos.append({
                            "codigo": c_val_str,
                            "cuenta": cta_name,
                            "parcial": parcial,
                            "debe": debe,
                            "haber": haber
                        })

    if not enunciado and rows:
        # Buscar primera frase descriptiva
        for r in rows[:10]:
            for c in r["cells"]:
                if isinstance(c, str) and len(c) > 25 and "ELECTROVIVIENDA" not in c.upper():
                    enunciado = c
                    break
            if enunciado:
                break

    if not fecha:
        default_dates = {"ENERO": "2026-01-15", "FEBRERO": "2026-02-15", "MARZO": "2026-03-15", "ABRIL": "2026-04-15"}
        fecha = default_dates.get(month_name, "2026-03-01")

    total_debe = round(sum(a["debe"] for a in asientos if len(a["codigo"]) == 4), 2)
    total_haber = round(sum(a["haber"] for a in asientos if len(a["codigo"]) == 4), 2)

    # Mapa exacto de Comprobante Diario según L.D-C 1, LIBRO DC 2, LIBRO DC 3 y LIBRO DC 4
    cd_map = {
        ("ENERO", "1"): "Comprobante Diario N° 1 (Apertura)",
        ("ENERO", "AJU DEP"): "Comprobante Diario N° 2 (Ajuste Depreciación)",
        ("ENERO", "CIERRE"): "Comprobante Diario N° 3 (Cierre Enero)",
        ("FEBRERO", "2"): "Comprobante Diario N° 4",
        ("FEBRERO", "3"): "Comprobante Diario N° 5",
        ("FEBRERO", "4"): "Comprobante Diario N° 6 (Parte 1)",
        ("FEBRERO", "5"): "Comprobante Diario N° 6 (Parte 2)",
        ("FEBRERO", "6"): "Comprobante Diario N° 7 (CE N° 2)",
        ("FEBRERO", "7"): "Comprobante Diario N° 8",
        ("FEBRERO", "8"): "Comprobante Diario N° 9 (CE N° 3)",
        ("FEBRERO", "9"): "Comprobante Diario N° 9 (Compra Factura 75020)",
        ("FEBRERO", "10"): "Comprobante Diario N° 9 (CE N° 4)",
        ("FEBRERO", "11"): "Comprobante Diario N° 9 (Compra Factura 12501)",
        ("FEBRERO", "12"): "Comprobante Diario N° 9 (CI N° 1)",
        ("FEBRERO", "13"): "Comprobante Diario N° 10 (Venta Factura 001)",
        ("FEBRERO", "14"): "Comprobante Diario N° 10 (CI N° 2)",
        ("FEBRERO", "15"): "Comprobante Diario N° 11",
        ("FEBRERO", "16"): "Comprobante Diario N° 12 (Dev. Venta Factura 001)",
        ("FEBRERO", "17"): "Comprobante Diario N° 13 (Dev. Compra Factura 12501)",
        ("FEBRERO", "18"): "Comprobante Diario N° 14 (CE N° 5)",
        ("FEBRERO", "19"): "Comprobante Diario N° 15 (Venta Factura 002)",
        ("FEBRERO", "20"): "Comprobante Diario N° 16 (CI N° 3)",
        ("FEBRERO", "21"): "Comprobante Diario N° 17 (Compra Factura 4075)",
        ("FEBRERO", "22"): "Comprobante Diario N° 18 (Venta Factura 003)",
        ("FEBRERO", "24"): "Comprobante Diario N° 19 (Servicios Públicos)",
        ("FEBRERO", "27"): "Comprobante Diario N° 19 (CE N° 6 Reembolso CM)",
        ("FEBRERO", "28"): "Comprobante Diario N° 19 (Gasto Bancario)",
        ("FEBRERO", "29 NOM"): "Comprobante Diario N° 19 (Liquidación Nómina Feb)",
        ("FEBRERO", "30"): "Comprobante Diario N° 19 (Nómina Esperanza)",
        ("FEBRERO", "31"): "Comprobante Diario N° 19 (Nómina María)",
        ("FEBRERO", "32"): "Comprobante Diario N° 19 (Nómina Andrea)",
        ("FEBRERO", "33"): "Comprobante Diario N° 19 (CE Pago Nómina)",
        ("FEBRERO", "34"): "Comprobante Diario N° 19 (Aportes Parafiscales)",
        ("FEBRERO", "35"): "Comprobante Diario N° 19 (Provisión Prestaciones)",
        ("FEBRERO", "36"): "Comprobante Diario N° 19 (Provisión Prestaciones 2)",
        ("FEBRERO", "37"): "Comprobante Diario N° 19 (Seguridad Social)",
        ("FEBRERO", "AD1"): "Comprobante Diario N° 19 (Cartera AD1)",
        ("FEBRERO", "AJU"): "Comprobante Diario N° 20 (Ajuste Depreciación Feb)",
        ("FEBRERO", "ASIENTOS DE CIERRE"): "Comprobante Diario N° 21 (Cierre Febrero)",
        ("MARZO", "38"): "Comprobante Diario N° 22 (Cuota 1 Pagaré Bancolombia)",
        ("MARZO", "39"): "Comprobante Diario N° 23 (Liquidación Contrato Esperanza)",
        ("MARZO", "40"): "Comprobante Diario N° 24 (Pago Liquidación Esperanza)",
        ("MARZO", "41"): "Comprobante Diario N° 24 (Cuota Remodelación Rafael Suárez)",
        ("MARZO", "42"): "Comprobante Diario N° 25 (Pago EPS Nueva EPS)",
        ("MARZO", "43"): "Comprobante Diario N° 25 (Pago EPS Sanitas)",
        ("MARZO", "44"): "Comprobante Diario N° 26 (Pago Pensión Colfondos)",
        ("MARZO", "45"): "Comprobante Diario N° 27 (Pago Pensión Porvenir)",
        ("MARZO", "46"): "Comprobante Diario N° 27 (Pago ARL Sura)",
        ("MARZO", "47"): "Comprobante Diario N° 27 (Pago Parafiscales Compensar)",
        ("MARZO", "48"): "Comprobante Diario N° 28 (Pago DIAN F-350 Retefuente)",
        ("MARZO", "49"): "Comprobante Diario N° 29 (Pago DIAN F-300 IVA)",
        ("MARZO", "RETEICA"): "Comprobante Diario N° 30 (Pago Alcaldía ReteICA)",
        ("MARZO", "AD2"): "Comprobante Diario N° 31 (Cartera Marzo)",
        ("MARZO", "NOM-MARZ"): "Comprobante Diario N° 31 (Planilla Nómina Marzo)",
        ("MARZO", "AD3"): "Comprobante Diario N° 31 (Causación Nómina María)",
        ("MARZO", "AD4"): "Comprobante Diario N° 31 (Causación Nómina Andrea)",
        ("MARZO", "AD5"): "Comprobante Diario N° 31 (Pago Nómina Marzo)",
        ("MARZO", "AD6"): "Comprobante Diario N° 31 (Seguridad Social Marzo)",
        ("MARZO", "AD7"): "Comprobante Diario N° 31 (Provisión Prestaciones María)",
        ("MARZO", "AD8"): "Comprobante Diario N° 31 (Provisión Prestaciones Andrea)",
        ("MARZO", "AJ1"): "Comprobante Diario N° 32 (Ajuste Depreciación Marzo)",
        ("MARZO", "CIERRE MARZO"): "Comprobante Diario N° 33 (Cierre Marzo)",
        ("ABRIL", "51"): "Comprobante Diario N° 34 (Anticipo La Casa Orange)",
        ("ABRIL", "52"): "Comprobante Diario N° 35 (Compra Factura 55371 Orange)",
        ("ABRIL", "AD9"): "Comprobante Diario N° 35 (Cuota 2 Pagaré Bancolombia)",
        ("ABRIL", "53"): "Comprobante Diario N° 36 (Anticipo Cliente Horacio Díaz)",
        ("ABRIL", "54"): "Comprobante Diario N° 37 (Venta Factura 004 Horacio Díaz)",
        ("ABRIL", "55"): "Comprobante Diario N° 38 (Cobro Factura 004 Horacio Díaz)",
        ("ABRIL", "56"): "Comprobante Diario N° 39 (Consignación Bancaria y Pago Sobregiro)",
        ("ABRIL", "57"): "Comprobante Diario N° 40 (Dev. Venta Factura 004 Horacio Díaz)",
        ("ABRIL", "AD10"): "Comprobante Diario N° 40 (Cuota Remodelación Rafael Suárez)",
        ("ABRIL", "58"): "Comprobante Diario N° 41 (Reintegro Devolución Horacio Díaz)",
        ("ABRIL", "59"): "Comprobante Diario N° 42 (Dev. Compra Factura 55371 Orange)",
        ("ABRIL", "AD11"): "Comprobante Diario N° 42 (Pago Salud Nueva EPS Abril)",
        ("ABRIL", "AD12"): "Comprobante Diario N° 42 (Pago Salud Sanitas Abril)",
        ("ABRIL", "AD13"): "Comprobante Diario N° 43 (Pago Pensión Colfondos Abril)",
        ("ABRIL", "60"): "Comprobante Diario N° 43 (Pago Saldo La Casa Orange)",
        ("ABRIL", "AD14"): "Comprobante Diario N° 44 (Pago Pensión Porvenir Abril)",
        ("ABRIL", "AD15"): "Comprobante Diario N° 44 (Pago ARL Sura Abril)",
        ("ABRIL", "AD16"): "Comprobante Diario N° 44 (Pago Compensar Abril)",
        ("ABRIL", "NOM-ABRIL"): "Comprobante Diario N° 45 (Planilla Nómina Abril)",
        ("ABRIL", "AD17"): "Comprobante Diario N° 45 (Causación Nómina María Abril)",
        ("ABRIL", "AD18"): "Comprobante Diario N° 45 (Causación Nómina Andrea Abril)",
        ("ABRIL", "AD19"): "Comprobante Diario N° 45 (Pago Nómina Abril)",
        ("ABRIL", "AD20"): "Comprobante Diario N° 45 (Seguridad Social Abril)",
        ("ABRIL", "AD21"): "Comprobante Diario N° 45 (Provisión Prestaciones María Abril)",
        ("ABRIL", "AD22"): "Comprobante Diario N° 45 (Provisión Prestaciones Andrea Abril)",
        ("ABRIL", "AD23"): "Comprobante Diario N° 45 (Cartera Abril)",
        ("ABRIL", "AJ 1"): "Comprobante Diario N° 46 (Ajuste Depreciación Abril)",
        ("ABRIL", "CIERRE ABRIL"): "Comprobante Diario N° 47 (Cierre Abril)"
    }

    s_clean = sheet_name.strip()
    cd_label = cd_map.get((month_name, s_clean), cd_map.get((month_name, sheet_name), f"Comprobante Hoja {s_clean}"))

    return {
        "hoja": sheet_name,
        "comprobante_diario": cd_label,
        "mes": month_name,
        "fecha": fecha,
        "tipo": tipo_doc,
        "enunciado": enunciado or f"Registro contable hoja {sheet_name} ({month_name})",
        "tercero": pagado_a or "Varios / Interno",
        "cheque": cheque,
        "concepto_soporte": concepto_soporte or enunciado,
        "suma_letras": suma_letras,
        "elaborado_por": "GINA VILLAMIZAR",
        "total_debe": total_debe,
        "total_haber": total_haber,
        "asientos": asientos,
        "rows": rows[:90]
    }

def build_calendario_tributario_excel():
    """Crea CALENDARIO_TRIBUTARIO_2026_ELECTROVIVIENDA.xlsx en la carpeta CONTABILIDAD"""
    cal_items = [
        {
            "id": "CAL-01",
            "impuesto": "Retención en la Fuente (Formulario 350)",
            "entidad": "DIAN",
            "periodo": "Enero 2026",
            "periodicidad": "Mensual",
            "ultimo_digito_nit": "8 (NIT 901.765.438-3)",
            "fecha_vencimiento": "2026-02-19",
            "estado": "SIN MOVIMIENTO / INICIO OPERACIONES",
            "valor_pagado": 0,
            "hoja_soporte": "ENERO.xlsx",
            "responsable": "Gina Villamizar"
        },
        {
            "id": "CAL-02",
            "impuesto": "Retención en la Fuente (Formulario 350)",
            "entidad": "DIAN",
            "periodo": "Febrero 2026",
            "periodicidad": "Mensual",
            "ultimo_digito_nit": "8 (NIT 901.765.438-3)",
            "fecha_vencimiento": "2026-03-15",
            "estado": "PRESENTADA Y PAGADA (Cheque #20216)",
            "valor_pagado": 11037000,
            "hoja_soporte": "MARZO.xlsx -> F-350 / Hoja 48",
            "responsable": "Gina Villamizar"
        },
        {
            "id": "CAL-03",
            "impuesto": "Impuesto sobre las Ventas IVA (Formulario 300)",
            "entidad": "DIAN",
            "periodo": "Bimestre 1 (Enero - Febrero 2026)",
            "periodicidad": "Bimestral",
            "ultimo_digito_nit": "8 (NIT 901.765.438-3)",
            "fecha_vencimiento": "2026-03-18",
            "estado": "PRESENTADA Y PAGADA (Cheque #20218)",
            "valor_pagado": 2613000,
            "hoja_soporte": "MARZO.xlsx -> F-300 / Hoja 49",
            "responsable": "Gina Villamizar"
        },
        {
            "id": "CAL-04",
            "impuesto": "Retención y Autorretención ICA Bucaramanga (Formulario ReteICA)",
            "entidad": "Alcaldía de Bucaramanga",
            "periodo": "Trimestre 1 (Enero - Febrero - Marzo 2026)",
            "periodicidad": "Trimestral",
            "ultimo_digito_nit": "8 (NIT 901.765.438-3)",
            "fecha_vencimiento": "2026-03-29",
            "estado": "PRESENTADA Y PAGADA (Cheque #20217)",
            "valor_pagado": 1895000,
            "hoja_soporte": "MARZO.xlsx -> F - RETEICA / RETEICA",
            "responsable": "Gina Villamizar"
        },
        {
            "id": "CAL-05",
            "impuesto": "Retención en la Fuente (Formulario 350)",
            "entidad": "DIAN",
            "periodo": "Marzo 2026",
            "periodicidad": "Mensual",
            "ultimo_digito_nit": "8 (NIT 901.765.438-3)",
            "fecha_vencimiento": "2026-04-21",
            "estado": "EN VERIFICACIÓN / SIN VENTAS EN MARZO",
            "valor_pagado": 0,
            "hoja_soporte": "MARZO.xlsx / ABRIL.xlsx",
            "responsable": "Gina Villamizar"
        },
        {
            "id": "CAL-06",
            "impuesto": "Retención en la Fuente (Formulario 350)",
            "entidad": "DIAN",
            "periodo": "Abril 2026",
            "periodicidad": "Mensual",
            "ultimo_digito_nit": "8 (NIT 901.765.438-3)",
            "fecha_vencimiento": "2026-05-20",
            "estado": "ALERTA ACTIVA - LISTA PARA AUTOLIQUIDAR",
            "valor_pagado": 399000,
            "hoja_soporte": "ABRIL.xlsx (Compras Orange y Cia + Ventas Horacio Díaz)",
            "responsable": "Gina Villamizar"
        },
        {
            "id": "CAL-07",
            "impuesto": "Impuesto sobre las Ventas IVA (Formulario 300)",
            "entidad": "DIAN",
            "periodo": "Bimestre 2 (Marzo - Abril 2026)",
            "periodicidad": "Bimestral",
            "ultimo_digito_nit": "8 (NIT 901.765.438-3)",
            "fecha_vencimiento": "2026-05-20",
            "estado": "ALERTA ACTIVA - LISTA PARA AUTOLIQUIDAR",
            "valor_pagado": 0,
            "hoja_soporte": "ABRIL.xlsx (Saldo a favor IVA descontable compras Abril)",
            "responsable": "Gina Villamizar"
        },
        {
            "id": "CAL-08",
            "impuesto": "Retención y Autorretención ICA Bucaramanga (Formulario ReteICA)",
            "entidad": "Alcaldía de Bucaramanga",
            "periodo": "Trimestre 2 (Abril - Mayo - Junio 2026)",
            "periodicidad": "Trimestral",
            "ultimo_digito_nit": "8 (NIT 901.765.438-3)",
            "fecha_vencimiento": "2026-07-17",
            "estado": "PROGRAMADA - ACUMULANDO RETENCIONES ABRIL",
            "valor_pagado": 95000,
            "hoja_soporte": "ABRIL.xlsx (Cuenta 2468 ICA retenido Orange y Cia)",
            "responsable": "Gina Villamizar"
        },
        {
            "id": "CAL-09",
            "impuesto": "Impuesto sobre las Ventas IVA (Formulario 300)",
            "entidad": "DIAN",
            "periodo": "Bimestre 3 (Mayo - Junio 2026)",
            "periodicidad": "Bimestral",
            "ultimo_digito_nit": "8 (NIT 901.765.438-3)",
            "fecha_vencimiento": "2026-07-21",
            "estado": "PROGRAMADA",
            "valor_pagado": 0,
            "hoja_soporte": "Calendario DIAN 2026",
            "responsable": "Gina Villamizar"
        },
        {
            "id": "CAL-10",
            "impuesto": "Impuesto sobre las Ventas IVA (Formulario 300)",
            "entidad": "DIAN",
            "periodo": "Bimestre 5 (Septiembre - Octubre 2026)",
            "periodicidad": "Bimestral",
            "ultimo_digito_nit": "8 (NIT 901.765.438-3)",
            "fecha_vencimiento": "2026-11-19",
            "estado": "ALERTA PRÓXIMO VENCIMIENTO (NOVIEMBRE 2026)",
            "valor_pagado": 0,
            "hoja_soporte": "Calendario DIAN 2026",
            "responsable": "Gina Villamizar"
        },
        {
            "id": "CAL-11",
            "impuesto": "Retención en la Fuente (Formulario 350)",
            "entidad": "DIAN",
            "periodo": "Octubre 2026",
            "periodicidad": "Mensual",
            "ultimo_digito_nit": "8 (NIT 901.765.438-3)",
            "fecha_vencimiento": "2026-11-19",
            "estado": "ALERTA PRÓXIMO VENCIMIENTO (NOVIEMBRE 2026)",
            "valor_pagado": 0,
            "hoja_soporte": "Calendario DIAN 2026",
            "responsable": "Gina Villamizar"
        }
    ]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "CALENDARIO TRIBUTARIO 2026"

    header_fill = PatternFill("solid", fgColor="0F2942")
    sub_fill = PatternFill("solid", fgColor="1E4976")
    gold_fill = PatternFill("solid", fgColor="D4AF37")
    white_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=10, bold=True)
    reg_font = Font(name="Calibri", size=10)
    thin = Side(border_style="thin", color="CBD5E1")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    ws.merge_cells("A1:J1")
    ws["A1"] = "STUDENTCONT.IA — CALENDARIO TRIBUTARIO Y CONTROL FISCAL 2026 — ELECTROVIVIENDA S.A.S (NIT 901.765.438-3)"
    ws["A1"].font = title_font
    ws["A1"].fill = header_fill
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:J2")
    ws["A2"] = "Domicilio: Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga | Régimen Responsable de IVA (RRI) | Agente de Retención y Autorretenedor Renta | Último Dígito NIT: 8"
    ws["A2"].font = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    ws["A2"].fill = sub_fill
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 20

    headers = ["ID", "IMPUESTO / FORMULARIO", "ENTIDAD", "PERIODO GRAVABLE", "PERIODICIDAD", "DÍGITO NIT", "FECHA VENCIMIENTO", "ESTADO ACTUAL", "VALOR LIQUIDADO / PAGADO", "DOCUMENTO SOPORTE"]
    ws.append([])
    ws.append(headers)
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=4, column=col_idx)
        cell.font = Font(name="Calibri", size=10, bold=True, color="0F2942")
        cell.fill = gold_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
    ws.row_dimensions[4].height = 24

    for idx, item in enumerate(cal_items, start=5):
        row_vals = [
            item["id"], item["impuesto"], item["entidad"], item["periodo"],
            item["periodicidad"], item["ultimo_digito_nit"], item["fecha_vencimiento"],
            item["estado"], item["valor_pagado"], item["hoja_soporte"]
        ]
        ws.append(row_vals)
        for col_idx in range(1, len(row_vals) + 1):
            c = ws.cell(row=idx, column=col_idx)
            c.font = bold_font if col_idx in (1, 2, 8, 9) else reg_font
            c.border = border
            if col_idx == 9:
                c.number_format = '"$"#,##0'
    widths = [10, 38, 22, 28, 15, 20, 18, 34, 22, 36]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w

    out_path = os.path.join(BASE_DIR, "CALENDARIO_TRIBUTARIO_2026_ELECTROVIVIENDA.xlsx")
    wb.save(out_path)
    return cal_items

def main():
    workbooks_cfg = [
        ("ENERO", os.path.join(BASE_DIR, "ENERO.xlsx")),
        ("FEBRERO", os.path.join(BASE_DIR, "FEBRERO.xlsx")),
        ("MARZO", os.path.join(BASE_DIR, "MARZO.xlsx")),
        ("ABRIL", os.path.join(BASE_DIR, "ABRIL.xlsx"))
    ]

    special_prefixes = (
        "PUC", "CUENTAS T", "CT", "T", "T2", "LIBROS", "L.", "LIBRO", "L M&B",
        "HOJA TR", "ER", "ESF", "ECP", "F&E", "NOTAS", "ESTADO NOTAS", "ENERO",
        "kardex", "Kardex", "F-350", "F-300", "F - RETEICA", "ANEXO 1", "TA", "RET-FTE"
    )

    puc_master = {}
    meses_data = {}

    for m_name, m_path in workbooks_cfg:
        wb = openpyxl.load_workbook(m_path, read_only=True, data_only=True)
        for p in extract_puc(wb):
            puc_master[p["codigo"]] = p

        transacciones = []
        hojas_especiales = {}

        for sname in wb.sheetnames:
            ws = wb[sname]
            s_strip = sname.strip()
            is_tx = False
            if re.match(r"^\d+$", s_strip) or re.match(r"^AD\d+$", s_strip) or s_strip.startswith("AJ") or "CIERRE" in s_strip.upper() or s_strip in ("RETEICA", "29 NOM", "NOM-MARZ", "NOM-ABRIL"):
                is_tx = True

            if is_tx:
                tx = parse_transaction_sheet(ws, sname, m_name)
                transacciones.append(tx)
            else:
                hojas_especiales[sname] = sheet_to_rows(ws, max_rows=220, max_cols=46)

        meses_data[m_name] = {
            "archivo": os.path.basename(m_path),
            "hojas": wb.sheetnames,
            "total_transacciones": len(transacciones),
            "transacciones": transacciones,
            "hojas_especiales": hojas_especiales
        }
        wb.close()

    # Construir Kardex consolidado y estructurado de los 4 productos
    kardex_productos = [
        {
            "id": "TV01",
            "referencia": "TV01",
            "articulo": 'TV LG 70" Smart 3D',
            "cuenta_puc": "14350501",
            "proveedor": "Electrodomésticos Cra 13 (NIT 850.251.207)",
            "metodo": "Promedio Ponderado",
            "unidad": "UND",
            "minimo": 5,
            "maximo": 50,
            "precio_venta_sugerido": 4800000,
            "movimientos": [
                {"fecha": "2026-02-01", "mes": "FEBRERO", "tipo": "INV_INICIAL", "descripcion": "Inventario Inicial", "doc": "INI", "vlr_unitario": 0, "ent_cant": 0, "ent_valor": 0, "sal_cant": 0, "sal_valor": 0, "saldo_cant": 0, "saldo_valor": 0, "promedio": 0},
                {"fecha": "2026-02-07", "mes": "FEBRERO", "tipo": "COMPRA", "descripcion": "Compra Factura Electrodomésticos Cra 13", "doc": "Hoja 11", "vlr_unitario": 3500000, "ent_cant": 40, "ent_valor": 140000000, "sal_cant": 0, "sal_valor": 0, "saldo_cant": 40, "saldo_valor": 140000000, "promedio": 3500000},
                {"fecha": "2026-02-08", "mes": "FEBRERO", "tipo": "VENTA", "descripcion": "Venta Factura No. 001 - Industrias Super", "doc": "Hoja 13", "vlr_unitario": 3500000, "ent_cant": 0, "ent_valor": 0, "sal_cant": 15, "sal_valor": 52500000, "saldo_cant": 25, "saldo_valor": 87500000, "promedio": 3500000},
                {"fecha": "2026-02-10", "mes": "FEBRERO", "tipo": "DEV_VENTA", "descripcion": "Devolución en Venta - Industrias Super", "doc": "Hoja 16", "vlr_unitario": 3500000, "ent_cant": 0, "ent_valor": 0, "sal_cant": -2, "sal_valor": -7000000, "saldo_cant": 27, "saldo_valor": 94500000, "promedio": 3500000},
                {"fecha": "2026-02-12", "mes": "FEBRERO", "tipo": "DEV_COMPRA", "descripcion": "Devolución en Compra - Electrodomésticos Cra 13", "doc": "Hoja 17", "vlr_unitario": 3500000, "ent_cant": -2, "ent_valor": -7000000, "sal_cant": 0, "sal_valor": 0, "saldo_cant": 25, "saldo_valor": 87500000, "promedio": 3500000},
                {"fecha": "2026-02-15", "mes": "FEBRERO", "tipo": "VENTA", "descripcion": "Venta Factura No. 002 - El Marquez de la 9", "doc": "Hoja 19", "vlr_unitario": 3500000, "ent_cant": 0, "ent_valor": 0, "sal_cant": 15, "sal_valor": 52500000, "saldo_cant": 10, "saldo_valor": 35000000, "promedio": 3500000},
                {"fecha": "2026-02-20", "mes": "FEBRERO", "tipo": "VENTA", "descripcion": "Venta Factura No. 003 - Jaime Salas Mora", "doc": "Hoja 22", "vlr_unitario": 3500000, "ent_cant": 0, "ent_valor": 0, "sal_cant": 4, "sal_valor": 14000000, "saldo_cant": 6, "saldo_valor": 21000000, "promedio": 3500000}
            ]
        },
        {
            "id": "NV01",
            "referencia": "NV01",
            "articulo": "NEVERAS SAMSUNG 12 PIES",
            "cuenta_puc": "14350502",
            "proveedor": "Electrodomésticos Cra 13 / Electromenores",
            "metodo": "Promedio Ponderado",
            "unidad": "UND",
            "minimo": 5,
            "maximo": 40,
            "precio_venta_sugerido": 960000,
            "movimientos": [
                {"fecha": "2026-02-01", "mes": "FEBRERO", "tipo": "INV_INICIAL", "descripcion": "Inventario Inicial", "doc": "INI", "vlr_unitario": 0, "ent_cant": 0, "ent_valor": 0, "sal_cant": 0, "sal_valor": 0, "saldo_cant": 0, "saldo_valor": 0, "promedio": 0},
                {"fecha": "2026-02-07", "mes": "FEBRERO", "tipo": "COMPRA", "descripcion": "Compra Factura Electrodomésticos Cra 13", "doc": "Hoja 11", "vlr_unitario": 610000, "ent_cant": 30, "ent_valor": 18300000, "sal_cant": 0, "sal_valor": 0, "saldo_cant": 30, "saldo_valor": 18300000, "promedio": 610000},
                {"fecha": "2026-02-08", "mes": "FEBRERO", "tipo": "VENTA", "descripcion": "Venta Factura No. 001 - Industrias Super", "doc": "Hoja 13", "vlr_unitario": 610000, "ent_cant": 0, "ent_valor": 0, "sal_cant": 10, "sal_valor": 6100000, "saldo_cant": 20, "saldo_valor": 12200000, "promedio": 610000},
                {"fecha": "2026-02-10", "mes": "FEBRERO", "tipo": "DEV_VENTA", "descripcion": "Devolución en Venta - Industrias Super", "doc": "Hoja 16", "vlr_unitario": 610000, "ent_cant": 0, "ent_valor": 0, "sal_cant": -3, "sal_valor": -1830000, "saldo_cant": 23, "saldo_valor": 14030000, "promedio": 610000},
                {"fecha": "2026-02-12", "mes": "FEBRERO", "tipo": "DEV_COMPRA", "descripcion": "Devolución en Compra - Electrodomésticos Cra 13", "doc": "Hoja 17", "vlr_unitario": 610000, "ent_cant": -3, "ent_valor": -1830000, "sal_cant": 0, "sal_valor": 0, "saldo_cant": 20, "saldo_valor": 12200000, "promedio": 610000},
                {"fecha": "2026-02-15", "mes": "FEBRERO", "tipo": "VENTA", "descripcion": "Venta Factura No. 002 - El Marquez de la 9", "doc": "Hoja 19", "vlr_unitario": 610000, "ent_cant": 0, "ent_valor": 0, "sal_cant": 12, "sal_valor": 7320000, "saldo_cant": 8, "saldo_valor": 4880000, "promedio": 610000},
                {"fecha": "2026-02-18", "mes": "FEBRERO", "tipo": "COMPRA", "descripcion": "Compra a Electromenores NIT 75.260.210", "doc": "Hoja 21", "vlr_unitario": 500000, "ent_cant": 12, "ent_valor": 6000000, "sal_cant": 0, "sal_valor": 0, "saldo_cant": 20, "saldo_valor": 10880000, "promedio": 544000},
                {"fecha": "2026-02-20", "mes": "FEBRERO", "tipo": "VENTA", "descripcion": "Venta Factura No. 003 - Jaime Salas Mora", "doc": "Hoja 22", "vlr_unitario": 544000, "ent_cant": 0, "ent_valor": 0, "sal_cant": 5, "sal_valor": 2720000, "saldo_cant": 15, "saldo_valor": 8160000, "promedio": 544000}
            ]
        },
        {
            "id": "LvSec 03",
            "referencia": "LvSec 03",
            "articulo": "Lavadora secadora AIWA 18 libras",
            "cuenta_puc": "14350503",
            "proveedor": "LA CASA ORANGE Y CIA (NIT 820.111.222)",
            "metodo": "Promedio Ponderado",
            "unidad": "UND",
            "minimo": 3,
            "maximo": 25,
            "precio_venta_sugerido": 1560000,
            "movimientos": [
                {"fecha": "2026-04-01", "mes": "ABRIL", "tipo": "INV_INICIAL", "descripcion": "Inventario Inicial Abril", "doc": "INI", "vlr_unitario": 0, "ent_cant": 0, "ent_valor": 0, "sal_cant": 0, "sal_valor": 0, "saldo_cant": 0, "saldo_valor": 0, "promedio": 0},
                {"fecha": "2026-04-02", "mes": "ABRIL", "tipo": "COMPRA", "descripcion": "Compra Factura Orange y CIA", "doc": "Hoja 52", "vlr_unitario": 730000, "ent_cant": 10, "ent_valor": 7300000, "sal_cant": 0, "sal_valor": 0, "saldo_cant": 10, "saldo_valor": 7300000, "promedio": 730000},
                {"fecha": "2026-04-04", "mes": "ABRIL", "tipo": "VENTA", "descripcion": "Venta Factura No. 004 - Horacio Díaz Páez", "doc": "Hoja 54", "vlr_unitario": 730000, "ent_cant": 0, "ent_valor": 0, "sal_cant": 5, "sal_valor": 3650000, "saldo_cant": 5, "saldo_valor": 3650000, "promedio": 730000},
                {"fecha": "2026-04-07", "mes": "ABRIL", "tipo": "DEV_VENTA", "descripcion": "Devolución en Venta Factura No. 004 - Horacio Díaz", "doc": "Hoja 57", "vlr_unitario": 730000, "ent_cant": 1, "ent_valor": 730000, "sal_cant": 0, "sal_valor": 0, "saldo_cant": 6, "saldo_valor": 4380000, "promedio": 730000},
                {"fecha": "2026-04-09", "mes": "ABRIL", "tipo": "DEV_COMPRA", "descripcion": "Devolución en Compra - Orange y CIA", "doc": "Hoja 59", "vlr_unitario": 730000, "ent_cant": -1, "ent_valor": -730000, "sal_cant": 0, "sal_valor": 0, "saldo_cant": 5, "saldo_valor": 3650000, "promedio": 730000}
            ]
        },
        {
            "id": "HM 04",
            "referencia": "HM 04",
            "articulo": "Hornos microondas LG spleed",
            "cuenta_puc": "14350504",
            "proveedor": "LA CASA ORANGE Y CIA (NIT 820.111.222)",
            "metodo": "Promedio Ponderado",
            "unidad": "UND",
            "minimo": 4,
            "maximo": 30,
            "precio_venta_sugerido": 210000,
            "movimientos": [
                {"fecha": "2026-04-01", "mes": "ABRIL", "tipo": "INV_INICIAL", "descripcion": "Inventario Inicial Abril", "doc": "INI", "vlr_unitario": 0, "ent_cant": 0, "ent_valor": 0, "sal_cant": 0, "sal_valor": 0, "saldo_cant": 0, "saldo_valor": 0, "promedio": 0},
                {"fecha": "2026-04-02", "mes": "ABRIL", "tipo": "COMPRA", "descripcion": "Compra Factura Orange y CIA", "doc": "Hoja 52", "vlr_unitario": 92000, "ent_cant": 15, "ent_valor": 1380000, "sal_cant": 0, "sal_valor": 0, "saldo_cant": 15, "saldo_valor": 1380000, "promedio": 92000},
                {"fecha": "2026-04-04", "mes": "ABRIL", "tipo": "VENTA", "descripcion": "Venta Factura No. 004 - Horacio Díaz Páez", "doc": "Hoja 54", "vlr_unitario": 92000, "ent_cant": 0, "ent_valor": 0, "sal_cant": 4, "sal_valor": 368000, "saldo_cant": 11, "saldo_valor": 1012000, "promedio": 92000}
            ]
        }
    ]

    cal_items = build_calendario_tributario_excel()

    facturas_realizadas = [
        {
            "id": "FAC-V-001",
            "numero": "Factura de Venta N° 001",
            "hoja": "13",
            "mes": "FEBRERO",
            "fecha": "2026-02-08",
            "vencimiento": "2026-02-08",
            "categoria": "VENTA",
            "emisor_nombre": "ELECTROVIVIENDA S.A.S",
            "emisor_nit": "901.765.438-3",
            "emisor_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "emisor_tel": "3164562001",
            "emisor_regimen": "Régimen Responsable de IVA (RRI) • Autorretenedor Renta",
            "tercero_nombre": "INDUSTRIAS SUPER S.A.S",
            "tercero_nit": "950.240.208-1",
            "tercero_dir": "Zona Industrial Montevideo, Bogotá D.C.",
            "tercero_tel": "3173179285",
            "tercero_regimen": "Gran Contribuyente • Autorretenedor",
            "forma_pago": "Contado — Cheque N° 77701 Banco Colmena",
            "items": [
                {"ref": "NV01", "descripcion": "Neveras Samsung 12 Pies", "cantidad": 10, "vlr_unitario": 810000, "subtotal": 8100000, "costo_kardex": 6100000},
                {"ref": "TV01", "descripcion": 'Televisores LG LED 70" Smart 3D', "cantidad": 15, "vlr_unitario": 4900000, "subtotal": 73500000, "costo_kardex": 52500000}
            ],
            "subtotal": 81600000,
            "iva": 15504000,
            "retefuente": 0,
            "reteiva": 2325600,
            "reteica": 783360,
            "avisos": 117504,
            "bomberil": 78336,
            "autorretencion": 2040000,
            "total_neto": 93799200,
            "costo_total": 58600000,
            "observaciones": "Cancelan con Cheque No. 77701 de Colmena el mismo día."
        },
        {
            "id": "FAC-V-002",
            "numero": "Factura de Venta N° 002",
            "hoja": "19",
            "mes": "FEBRERO",
            "fecha": "2026-02-15",
            "vencimiento": "2026-03-17",
            "categoria": "VENTA",
            "emisor_nombre": "ELECTROVIVIENDA S.A.S",
            "emisor_nit": "901.765.438-3",
            "emisor_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "emisor_tel": "3164562001",
            "emisor_regimen": "Régimen Responsable de IVA (RRI) • Autorretenedor Renta",
            "tercero_nombre": "EL MARQUEZ DE LA 9",
            "tercero_nit": "880.472.209-4",
            "tercero_dir": "Avenida Cra 9 # 112-40, Bogotá D.C.",
            "tercero_tel": "3158901122",
            "tercero_regimen": "Régimen Responsable de IVA (RRI)",
            "forma_pago": "Crédito a 30 días (Cruce y abono en Hoja 20)",
            "items": [
                {"ref": "NV01", "descripcion": "Neveras Samsung 12 Pies", "cantidad": 12, "vlr_unitario": 800000, "subtotal": 9600000, "costo_kardex": 7320000},
                {"ref": "TV01", "descripcion": 'Televisores LG LED 70" Smart 3D', "cantidad": 15, "vlr_unitario": 4700000, "subtotal": 70500000, "costo_kardex": 52500000}
            ],
            "subtotal": 80100000,
            "iva": 15219000,
            "retefuente": 0,
            "reteiva": 0,
            "reteica": 768960,
            "avisos": 115344,
            "bomberil": 76896,
            "autorretencion": 2002500,
            "total_neto": 94357800,
            "costo_total": 59820000,
            "observaciones": "Plazo concedido: 30 días. Incluye autorretención en renta del 2.5%."
        },
        {
            "id": "FAC-V-003",
            "numero": "Factura de Venta N° 003",
            "hoja": "22",
            "mes": "FEBRERO",
            "fecha": "2026-02-20",
            "vencimiento": "2026-03-22",
            "categoria": "VENTA",
            "emisor_nombre": "ELECTROVIVIENDA S.A.S",
            "emisor_nit": "901.765.438-3",
            "emisor_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "emisor_tel": "3164562001",
            "emisor_regimen": "Régimen Responsable de IVA (RRI) • Autorretenedor Renta",
            "tercero_nombre": "JAIME SALAS MORA",
            "tercero_nit": "CC 35.258.211",
            "tercero_dir": "Bogotá D.C.",
            "tercero_tel": "3104458890",
            "tercero_regimen": "No Responsable de IVA • Persona Natural No Declarante",
            "forma_pago": "Crédito a 30 días (Cuenta 13050503 Clientes)",
            "items": [
                {"ref": "NV01", "descripcion": "Neveras Samsung 12 Pies", "cantidad": 5, "vlr_unitario": 850000, "subtotal": 4250000, "costo_kardex": 2720000},
                {"ref": "TV01", "descripcion": 'Televisores LG LED 70" Smart 3D', "cantidad": 4, "vlr_unitario": 5000000, "subtotal": 20000000, "costo_kardex": 14000000}
            ],
            "subtotal": 24250000,
            "iva": 4607500,
            "retefuente": 0,
            "reteiva": 0,
            "reteica": 0,
            "avisos": 0,
            "bomberil": 0,
            "autorretencion": 848750,
            "total_neto": 28857500,
            "costo_total": 16720000,
            "observaciones": "Venta a Persona Natural No Responsable de IVA. Autorretención en renta del 3.5%."
        },
        {
            "id": "FAC-V-004",
            "numero": "Factura de Venta N° 004",
            "hoja": "54",
            "mes": "ABRIL",
            "fecha": "2026-04-04",
            "vencimiento": "2026-04-05",
            "categoria": "VENTA",
            "emisor_nombre": "ELECTROVIVIENDA S.A.S",
            "emisor_nit": "901.765.438-3",
            "emisor_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "emisor_tel": "3164562001",
            "emisor_regimen": "Régimen Responsable de IVA (RRI) • Autorretenedor Renta",
            "tercero_nombre": "HORACIO DÍAZ PÁEZ",
            "tercero_nit": "CC 12.080.357",
            "tercero_dir": "Bucaramanga, Santander",
            "tercero_tel": "3187654321",
            "tercero_regimen": "No Responsable de IVA • Persona Natural",
            "forma_pago": "Anticipo $1.200.000 (Hoja 53) + Efectivo $8.943.560 (Hoja 55)",
            "items": [
                {"ref": "LvSec 03", "descripcion": "Lavadora secadora AIWA 18 libras", "cantidad": 5, "vlr_unitario": 1560000, "subtotal": 7800000, "costo_kardex": 3650000},
                {"ref": "HM 04", "descripcion": "Hornos microondas LG Spleed", "cantidad": 4, "vlr_unitario": 181000, "subtotal": 724000, "costo_kardex": 368000}
            ],
            "subtotal": 8524000,
            "iva": 1619560,
            "retefuente": 0,
            "reteiva": 0,
            "reteica": 0,
            "avisos": 0,
            "bomberil": 0,
            "autorretencion": 298340,
            "total_neto": 10143560,
            "costo_total": 4018000,
            "observaciones": "Venta de electrodomésticos línea blanca Abril 2026."
        },
        {
            "id": "FAC-C-75020",
            "numero": "Factura de Compra N° 75020",
            "hoja": "9",
            "mes": "FEBRERO",
            "fecha": "2026-02-07",
            "vencimiento": "2026-02-07",
            "categoria": "COMPRA",
            "emisor_nombre": "SUPERTIENDAS SAO",
            "emisor_nit": "880.114.206-1",
            "emisor_dir": "Bogotá D.C.",
            "emisor_tel": "6017450000",
            "emisor_regimen": "Gran Contribuyente • Autorretenedor",
            "tercero_nombre": "ELECTROVIVIENDA S.A.S",
            "tercero_nit": "901.765.438-3",
            "tercero_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "tercero_tel": "3164562001",
            "tercero_regimen": "Régimen Responsable de IVA (RRI)",
            "forma_pago": "Contado — Cancelada con Cheque N° 20204 (Hoja 10)",
            "items": [
                {"ref": "PAP-01", "descripcion": "Cajas de Formas Continuas 9 ½ x 11 Blanco (IVA 19%)", "cantidad": 20, "vlr_unitario": 65000, "subtotal": 1300000, "costo_kardex": 0},
                {"ref": "PAP-02", "descripcion": "Portaminas Faber Castell (IVA 19%)", "cantidad": 50, "vlr_unitario": 3200, "subtotal": 160000, "costo_kardex": 0},
                {"ref": "PAP-03", "descripcion": "Lapiceros Kilométricos Micropunta negros (IVA 19%)", "cantidad": 100, "vlr_unitario": 1250, "subtotal": 125000, "costo_kardex": 0},
                {"ref": "CAF-01", "descripcion": "Kilos de Café Sello Rojo (IVA 5%)", "cantidad": 20, "vlr_unitario": 6300, "subtotal": 126000, "costo_kardex": 0},
                {"ref": "CAF-02", "descripcion": "Paquetes de Azúcar Incauca (IVA 5%)", "cantidad": 20, "vlr_unitario": 5100, "subtotal": 102000, "costo_kardex": 0},
                {"ref": "ASE-01", "descripcion": "Ambientadores Frutos Verdes Frasco (IVA 19%)", "cantidad": 10, "vlr_unitario": 10600, "subtotal": 106000, "costo_kardex": 0}
            ],
            "subtotal": 1919000,
            "iva": 332690,
            "retefuente": 0,
            "reteiva": 0,
            "reteica": 0,
            "avisos": 0,
            "bomberil": 0,
            "autorretencion": 0,
            "total_neto": 2251690,
            "costo_total": 0,
            "observaciones": "Compra de elementos de aseo, cafetería y papelería. IVA registrado como mayor valor del gasto."
        },
        {
            "id": "FAC-C-12501",
            "numero": "Factura de Compra N° 12501",
            "hoja": "11",
            "mes": "FEBRERO",
            "fecha": "2026-02-07",
            "vencimiento": "2026-02-14",
            "categoria": "COMPRA",
            "emisor_nombre": "ELECTRODOMÉSTICOS CRA. 13",
            "emisor_nit": "850.251.207-5",
            "emisor_dir": "Carrera 13 # 14-50, Bogotá D.C.",
            "emisor_tel": "3165789547",
            "emisor_regimen": "Régimen Responsable de IVA (RRI)",
            "tercero_nombre": "ELECTROVIVIENDA S.A.S",
            "tercero_nit": "901.765.438-3",
            "tercero_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "tercero_tel": "3164562001",
            "tercero_regimen": "Régimen Responsable de IVA (RRI) • Agente de Retención",
            "forma_pago": "Anticipo $3.000.000 + Cheque $86.759.950 + Saldo a Crédito (Cancelado Hoja 18)",
            "items": [
                {"ref": "NV01", "descripcion": "Neveras Samsung 12 Pies", "cantidad": 30, "vlr_unitario": 610000, "subtotal": 18300000, "costo_kardex": 18300000},
                {"ref": "TV01", "descripcion": 'Televisores LG LED 70" Smart 3D', "cantidad": 40, "vlr_unitario": 3500000, "subtotal": 140000000, "costo_kardex": 140000000}
            ],
            "subtotal": 158300000,
            "iva": 30077000,
            "retefuente": 3957500,
            "reteiva": 0,
            "reteica": 1519680,
            "avisos": 227952,
            "bomberil": 151968,
            "autorretencion": 0,
            "total_neto": 182519900,
            "costo_total": 158300000,
            "observaciones": "Compra de inventario inicial para la venta. Alimenta Kardex TV01 (40 und) y NV01 (30 und)."
        },
        {
            "id": "FAC-C-4075",
            "numero": "Factura de Compra N° 4075",
            "hoja": "21",
            "mes": "FEBRERO",
            "fecha": "2026-02-18",
            "vencimiento": "2026-03-20",
            "categoria": "COMPRA",
            "emisor_nombre": "ELECTROMENORES",
            "emisor_nit": "75.260.210-1",
            "emisor_dir": "Bogotá D.C.",
            "emisor_tel": "3112233445",
            "emisor_regimen": "No Responsable de IVA • Declarante de Renta",
            "tercero_nombre": "ELECTROVIVIENDA S.A.S",
            "tercero_nit": "901.765.438-3",
            "tercero_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "tercero_tel": "3164562001",
            "tercero_regimen": "Régimen Responsable de IVA (RRI) • Agente de Retención",
            "forma_pago": "Crédito a 30 días (Cuenta 22050502 Proveedores)",
            "items": [
                {"ref": "NV01", "descripcion": "Neveras Samsung 12 Pies", "cantidad": 12, "vlr_unitario": 500000, "subtotal": 6000000, "costo_kardex": 6000000}
            ],
            "subtotal": 6000000,
            "iva": 0,
            "retefuente": 150000,
            "reteiva": 0,
            "reteica": 57600,
            "avisos": 8640,
            "bomberil": 5760,
            "autorretencion": 0,
            "total_neto": 5778000,
            "costo_total": 6000000,
            "observaciones": "Compra a No Responsable de IVA Declarante. Recalcula promedio ponderado de Neveras a $544.000/und."
        },
        {
            "id": "FAC-C-55371",
            "numero": "Factura de Compra N° 55371",
            "hoja": "52",
            "mes": "ABRIL",
            "fecha": "2026-04-02",
            "vencimiento": "2026-06-01",
            "categoria": "COMPRA",
            "emisor_nombre": "LA CASA ORANGE Y CIA",
            "emisor_nit": "890.905.290-2",
            "emisor_dir": "Bogotá D.C.",
            "emisor_tel": "6014459900",
            "emisor_regimen": "Régimen Responsable de IVA (RRI)",
            "tercero_nombre": "ELECTROVIVIENDA S.A.S",
            "tercero_nit": "901.765.438-3",
            "tercero_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "tercero_tel": "3164562001",
            "tercero_regimen": "Régimen Responsable de IVA (RRI) • Agente de Retención",
            "forma_pago": "Anticipo $3.650.000 (Hoja 51) + Saldo a 60 días (Cancelado Hoja 60)",
            "items": [
                {"ref": "LvSec 03", "descripcion": "Lavadora secadora AIWA 18 libras", "cantidad": 10, "vlr_unitario": 730000, "subtotal": 7300000, "costo_kardex": 7300000},
                {"ref": "HM 04", "descripcion": "Hornos microondas LG spleed", "cantidad": 15, "vlr_unitario": 92000, "subtotal": 1380000, "costo_kardex": 1380000}
            ],
            "subtotal": 8680000,
            "iva": 1649200,
            "retefuente": 217000,
            "reteiva": 0,
            "reteica": 83328,
            "avisos": 12499.2,
            "bomberil": 8332.8,
            "autorretencion": 0,
            "total_neto": 10008040,
            "costo_total": 8680000,
            "observaciones": "Apertura de tarjetas Kardex LvSec 03 (10 und) y HM 04 (15 und) en Abril 2026."
        },
        {
            "id": "NC-V-016",
            "numero": "Nota Crédito DV-001 (Ref. Factura 001)",
            "hoja": "16",
            "mes": "FEBRERO",
            "fecha": "2026-02-10",
            "vencimiento": "2026-02-10",
            "categoria": "DEVOLUCION",
            "emisor_nombre": "ELECTROVIVIENDA S.A.S",
            "emisor_nit": "901.765.438-3",
            "emisor_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "emisor_tel": "3164562001",
            "emisor_regimen": "Régimen Responsable de IVA (RRI)",
            "tercero_nombre": "INDUSTRIAS SUPER S.A.S",
            "tercero_nit": "950.240.208-1",
            "tercero_dir": "Bogotá D.C.",
            "tercero_tel": "3173179285",
            "tercero_regimen": "Gran Contribuyente • Autorretenedor",
            "forma_pago": "Abono / Anticipo de Clientes (Cuenta 27056501)",
            "items": [
                {"ref": "NV01", "descripcion": "Devolución Neveras Samsung 12 Pies", "cantidad": 3, "vlr_unitario": 810000, "subtotal": 2430000, "costo_kardex": 1830000},
                {"ref": "TV01", "descripcion": 'Devolución Televisores LG LED 70" Smart 3D', "cantidad": 2, "vlr_unitario": 4900000, "subtotal": 9800000, "costo_kardex": 7000000}
            ],
            "subtotal": 12230000,
            "iva": 2323700,
            "retefuente": 0,
            "reteiva": 348555,
            "reteica": 117408,
            "avisos": 17611.2,
            "bomberil": 11740.8,
            "autorretencion": 305750,
            "total_neto": 14058385,
            "costo_total": 8830000,
            "observaciones": "Devolución en venta de 3 neveras y 2 televisores de la Factura N° 001. Reingresa al Kardex."
        },
        {
            "id": "ND-C-017",
            "numero": "Nota Débito DV-C01 (Ref. Factura 12501)",
            "hoja": "17",
            "mes": "FEBRERO",
            "fecha": "2026-02-12",
            "vencimiento": "2026-02-12",
            "categoria": "DEVOLUCION",
            "emisor_nombre": "ELECTROVIVIENDA S.A.S",
            "emisor_nit": "901.765.438-3",
            "emisor_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "emisor_tel": "3164562001",
            "emisor_regimen": "Régimen Responsable de IVA (RRI)",
            "tercero_nombre": "ELECTRODOMÉSTICOS CRA. 13",
            "tercero_nit": "850.251.207-5",
            "tercero_dir": "Bogotá D.C.",
            "tercero_tel": "3165789547",
            "tercero_regimen": "Régimen Responsable de IVA (RRI)",
            "forma_pago": "Cruce con saldo por pagar Proveedores Factura 12501 (Cuenta 22050501)",
            "items": [
                {"ref": "NV01", "descripcion": "Devolución Neveras Samsung 12 Pies", "cantidad": 3, "vlr_unitario": 610000, "subtotal": 1830000, "costo_kardex": 1830000},
                {"ref": "TV01", "descripcion": 'Devolución Televisores LG LED 70" Smart 3D', "cantidad": 2, "vlr_unitario": 3500000, "subtotal": 7000000, "costo_kardex": 7000000}
            ],
            "subtotal": 8830000,
            "iva": 1677700,
            "retefuente": 220750,
            "reteiva": 0,
            "reteica": 84768,
            "avisos": 12715.2,
            "bomberil": 8476.8,
            "autorretencion": 0,
            "total_neto": 10180990,
            "costo_total": 8830000,
            "observaciones": "Devolución a proveedor de 3 neveras y 2 televisores. Descuenta existencias en Kardex."
        },
        {
            "id": "NC-V-057",
            "numero": "Nota Crédito DV-004 (Ref. Factura 004)",
            "hoja": "57",
            "mes": "ABRIL",
            "fecha": "2026-04-07",
            "vencimiento": "2026-04-08",
            "categoria": "DEVOLUCION",
            "emisor_nombre": "ELECTROVIVIENDA S.A.S",
            "emisor_nit": "901.765.438-3",
            "emisor_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "emisor_tel": "3164562001",
            "emisor_regimen": "Régimen Responsable de IVA (RRI)",
            "tercero_nombre": "HORACIO DÍAZ PÁEZ",
            "tercero_nit": "CC 12.080.357",
            "tercero_dir": "Bucaramanga, Santander",
            "tercero_tel": "3187654321",
            "tercero_regimen": "No Responsable de IVA",
            "forma_pago": "Reintegro cancelado con Cheque N° 55703 (Hoja 58)",
            "items": [
                {"ref": "LvSec 03", "descripcion": "Devolución Lavadora secadora AIWA 18 libras", "cantidad": 1, "vlr_unitario": 1560000, "subtotal": 1560000, "costo_kardex": 730000}
            ],
            "subtotal": 1560000,
            "iva": 296400,
            "retefuente": 0,
            "reteiva": 0,
            "reteica": 0,
            "avisos": 0,
            "bomberil": 0,
            "autorretencion": 54600,
            "total_neto": 1856400,
            "costo_total": 730000,
            "observaciones": "Devolución de 1 lavadora AIWA de la Factura N° 004. Reingresa al Kardex LvSec 03."
        },
        {
            "id": "ND-C-059",
            "numero": "Nota Débito DV-C02 (Ref. Factura 55371)",
            "hoja": "59",
            "mes": "ABRIL",
            "fecha": "2026-04-09",
            "vencimiento": "2026-04-09",
            "categoria": "DEVOLUCION",
            "emisor_nombre": "ELECTROVIVIENDA S.A.S",
            "emisor_nit": "901.765.438-3",
            "emisor_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "emisor_tel": "3164562001",
            "emisor_regimen": "Régimen Responsable de IVA (RRI)",
            "tercero_nombre": "LA CASA ORANGE Y CIA",
            "tercero_nit": "890.905.290-2",
            "tercero_dir": "Bogotá D.C.",
            "tercero_tel": "6014459900",
            "tercero_regimen": "Régimen Responsable de IVA (RRI)",
            "forma_pago": "Cruce con cuenta por pagar Proveedores Factura N° 55371",
            "items": [
                {"ref": "LvSec 03", "descripcion": "Devolución Lavadora secadora AIWA 18 libras", "cantidad": 1, "vlr_unitario": 730000, "subtotal": 730000, "costo_kardex": 730000}
            ],
            "subtotal": 730000,
            "iva": 138700,
            "retefuente": 18250,
            "reteiva": 0,
            "reteica": 7008,
            "avisos": 1051.2,
            "bomberil": 700.8,
            "autorretencion": 0,
            "total_neto": 841690,
            "costo_total": 730000,
            "observaciones": "Devolución en compra a La Casa Orange y Cia. Descuenta 1 unidad en Kardex LvSec 03."
        },
        {
            "id": "DOC-ENE-001",
            "numero": "Escritura / Factura Aporte Social N° 001",
            "hoja": "1",
            "mes": "ENERO",
            "fecha": "2026-01-02",
            "vencimiento": "2026-01-02",
            "categoria": "COMPRA",
            "emisor_nombre": "SOCIOS FUNDADORES ELECTROVIVIENDA S.A.S",
            "emisor_nit": "901.765.438-3",
            "emisor_dir": "Bucaramanga, Santander",
            "emisor_tel": "3164562001",
            "emisor_regimen": "Accionistas Fundadores",
            "tercero_nombre": "ELECTROVIVIENDA S.A.S",
            "tercero_nit": "901.765.438-3",
            "tercero_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "tercero_tel": "3164562001",
            "tercero_regimen": "Régimen Responsable de IVA (RRI) • Autorretenedor Renta",
            "forma_pago": "Aporte Social de Constitución (Comprobante Diario N° 1)",
            "items": [
                {"ref": "AP-EFE", "descripcion": "Aporte en Efectivo y Cheque Socio 1", "cantidad": 1, "vlr_unitario": 123000000, "subtotal": 123000000, "costo_kardex": 0},
                {"ref": "AP-EDI", "descripcion": "Aporte Edificio Comercial y Terreno Socio 3", "cantidad": 1, "vlr_unitario": 125600000, "subtotal": 125600000, "costo_kardex": 0},
                {"ref": "AP-MUE", "descripcion": "Aporte Muebles, Enseres y Equipos de Cómputo", "cantidad": 1, "vlr_unitario": 31400000, "subtotal": 31400000, "costo_kardex": 0}
            ],
            "subtotal": 280000000,
            "iva": 0,
            "retefuente": 0,
            "reteiva": 0,
            "reteica": 0,
            "avisos": 0,
            "bomberil": 0,
            "autorretencion": 0,
            "total_neto": 280000000,
            "costo_total": 0,
            "observaciones": "Constitución de ELECTROVIVIENDA S.A.S en Enero (Comprobante Diario N° 1 - Hoja 1)."
        },
        {
            "id": "DOC-ENE-002",
            "numero": "Nota Contable Depreciación N° 001 (Enero)",
            "hoja": "AJU DEP",
            "mes": "ENERO",
            "fecha": "2026-01-30",
            "vencimiento": "2026-01-30",
            "categoria": "DEVOLUCION",
            "emisor_nombre": "ELECTROVIVIENDA S.A.S",
            "emisor_nit": "901.765.438-3",
            "emisor_dir": "Bucaramanga, Santander",
            "emisor_tel": "3164562001",
            "emisor_regimen": "Régimen Responsable de IVA (RRI)",
            "tercero_nombre": "CONTABILIDAD INTERNA NIIF",
            "tercero_nit": "901.765.438-3",
            "tercero_dir": "Bucaramanga",
            "tercero_tel": "3164562001",
            "tercero_regimen": "Régimen Responsable de IVA (RRI)",
            "forma_pago": "Ajuste Mensual NIIF (Comprobante Diario N° 2)",
            "items": [
                {"ref": "DEP-01", "descripcion": "Depreciación Mensual Propiedad, Planta y Equipo (Enero)", "cantidad": 1, "vlr_unitario": 1007500, "subtotal": 1007500, "costo_kardex": 0}
            ],
            "subtotal": 1007500,
            "iva": 0,
            "retefuente": 0,
            "reteiva": 0,
            "reteica": 0,
            "avisos": 0,
            "bomberil": 0,
            "autorretencion": 0,
            "total_neto": 1007500,
            "costo_total": 0,
            "observaciones": "Nota de ajuste por depreciación de activos fijos del mes de Enero (Comprobante Diario N° 2)."
        },
        {
            "id": "FAC-S-007",
            "numero": "Factura / Cuenta de Cobro Remodelación N° 007",
            "hoja": "7",
            "mes": "FEBRERO",
            "fecha": "2026-02-05",
            "vencimiento": "2026-04-07",
            "categoria": "COMPRA",
            "emisor_nombre": "RAFAEL SUÁREZ CANO",
            "emisor_nit": "CC 70.111.205",
            "emisor_dir": "Bucaramanga, Santander",
            "emisor_tel": "3150001122",
            "emisor_regimen": "No Responsable de IVA • Declarante (Servicios 4%)",
            "tercero_nombre": "ELECTROVIVIENDA S.A.S",
            "tercero_nit": "901.765.438-3",
            "tercero_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "tercero_tel": "3164562001",
            "tercero_regimen": "Régimen Responsable de IVA (RRI) • Agente de Retención",
            "forma_pago": "50% Cheque N° 20203 (Hoja 8) y saldo en cuotas (Marzo Hoja 41 y Abril Hoja AD10)",
            "items": [
                {"ref": "SRV-REM", "descripcion": "Servicio de remodelación y adecuación de instalaciones comerciales", "cantidad": 1, "vlr_unitario": 8500000, "subtotal": 8500000, "costo_kardex": 0}
            ],
            "subtotal": 8500000,
            "iva": 0,
            "retefuente": 340000,
            "reteiva": 0,
            "reteica": 81600,
            "avisos": 12240,
            "bomberil": 8160,
            "autorretencion": 0,
            "total_neto": 8058000,
            "costo_total": 0,
            "observaciones": "Causación servicio de remodelación local comercial en Febrero (Comprobante Diario N° 8 - Hoja 7)."
        },
        {
            "id": "DOC-MAR-038",
            "numero": "Liquidación Bancaria Cuota 1 Pagaré Bancolombia",
            "hoja": "38",
            "mes": "MARZO",
            "fecha": "2026-03-02",
            "vencimiento": "2026-03-02",
            "categoria": "COMPRA",
            "emisor_nombre": "BANCOLOMBIA S.A.",
            "emisor_nit": "890.120.203-1",
            "emisor_dir": "Bucaramanga, Santander",
            "emisor_tel": "018000912345",
            "emisor_regimen": "Gran Contribuyente • Entidad Financiera",
            "tercero_nombre": "ELECTROVIVIENDA S.A.S",
            "tercero_nit": "901.765.438-3",
            "tercero_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "tercero_tel": "3164562001",
            "tercero_regimen": "Régimen Responsable de IVA (RRI)",
            "forma_pago": "Débito Automático Cuenta Corriente 123456789-111 (Hoja 38)",
            "items": [
                {"ref": "PAG-01", "descripcion": "Abono a Capital e Intereses Primera Cuota Crédito $56.000.000", "cantidad": 1, "vlr_unitario": 2989448, "subtotal": 2989448, "costo_kardex": 0}
            ],
            "subtotal": 2989448,
            "iva": 0,
            "retefuente": 0,
            "reteiva": 0,
            "reteica": 0,
            "avisos": 0,
            "bomberil": 0,
            "autorretencion": 0,
            "total_neto": 2989448,
            "costo_total": 0,
            "observaciones": "Pago primera cuota crédito bancario Bancolombia en Marzo (Comprobante Diario N° 22 - Hoja 38)."
        },
        {
            "id": "DOC-MAR-041",
            "numero": "Factura / Cuota Remodelación Local (Marzo)",
            "hoja": "41",
            "mes": "MARZO",
            "fecha": "2026-03-07",
            "vencimiento": "2026-03-07",
            "categoria": "COMPRA",
            "emisor_nombre": "RAFAEL SUÁREZ CANO",
            "emisor_nit": "CC 70.111.205",
            "emisor_dir": "Bucaramanga, Santander",
            "emisor_tel": "3150001122",
            "emisor_regimen": "No Responsable de IVA • Declarante",
            "tercero_nombre": "ELECTROVIVIENDA S.A.S",
            "tercero_nit": "901.765.438-3",
            "tercero_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "tercero_tel": "3164562001",
            "tercero_regimen": "Régimen Responsable de IVA (RRI)",
            "forma_pago": "Cheque N° 20208 Bancolombia (Comprobante Diario N° 24 - Hoja 41)",
            "items": [
                {"ref": "REM-C1", "descripcion": "Cancelación cuota remodelación del local comercial (Marzo)", "cantidad": 1, "vlr_unitario": 2014500, "subtotal": 2014500, "costo_kardex": 0}
            ],
            "subtotal": 2014500,
            "iva": 0,
            "retefuente": 0,
            "reteiva": 0,
            "reteica": 0,
            "avisos": 0,
            "bomberil": 0,
            "autorretencion": 0,
            "total_neto": 2014500,
            "costo_total": 0,
            "observaciones": "Pago cuota de remodelación a Rafael Suárez en Marzo (Hoja 41)."
        },
        {
            "id": "DOC-MAR-048",
            "numero": "Liquidación Oficial F-350 Retefuente (Marzo)",
            "hoja": "48",
            "mes": "MARZO",
            "fecha": "2026-03-15",
            "vencimiento": "2026-03-15",
            "categoria": "COMPRA",
            "emisor_nombre": "DIAN — DIRECCIÓN DE IMPUESTOS Y ADUANAS NACIONALES",
            "emisor_nit": "800.197.268-4",
            "emisor_dir": "Bucaramanga, Santander",
            "emisor_tel": "6013078064",
            "emisor_regimen": "Entidad Pública Nacional",
            "tercero_nombre": "ELECTROVIVIENDA S.A.S",
            "tercero_nit": "901.765.438-3",
            "tercero_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "tercero_tel": "3164562001",
            "tercero_regimen": "Régimen Responsable de IVA (RRI)",
            "forma_pago": "Pago Electrónico / Banco (Comprobante Diario N° 28 - Hoja 48)",
            "items": [
                {"ref": "F-350", "descripcion": "Declaración y Pago Formulario 350 Retención en la Fuente y Autorretenciones", "cantidad": 1, "vlr_unitario": 9023000, "subtotal": 9023000, "costo_kardex": 0}
            ],
            "subtotal": 9023000,
            "iva": 0,
            "retefuente": 0,
            "reteiva": 0,
            "reteica": 0,
            "avisos": 0,
            "bomberil": 0,
            "autorretencion": 0,
            "total_neto": 9023000,
            "costo_total": 0,
            "observaciones": "Pago en Marzo del Formulario 350 de Retención en la Fuente (Hoja 48)."
        },
        {
            "id": "DOC-MAR-049",
            "numero": "Liquidación Oficial F-300 IVA Bimestral (Marzo)",
            "hoja": "49",
            "mes": "MARZO",
            "fecha": "2026-03-18",
            "vencimiento": "2026-03-18",
            "categoria": "COMPRA",
            "emisor_nombre": "DIAN — DIRECCIÓN DE IMPUESTOS Y ADUANAS NACIONALES",
            "emisor_nit": "800.197.268-4",
            "emisor_dir": "Bucaramanga, Santander",
            "emisor_tel": "6013078064",
            "emisor_regimen": "Entidad Pública Nacional",
            "tercero_nombre": "ELECTROVIVIENDA S.A.S",
            "tercero_nit": "901.765.438-3",
            "tercero_dir": "Cra 21 N° 46-11 Barrio La Concordia, Bucaramanga",
            "tercero_tel": "3164562001",
            "tercero_regimen": "Régimen Responsable de IVA (RRI)",
            "forma_pago": "Pago Electrónico / Banco (Comprobante Diario N° 29 - Hoja 49)",
            "items": [
                {"ref": "F-300", "descripcion": "Declaración y Pago Formulario 300 Impuesto sobre las Ventas IVA", "cantidad": 1, "vlr_unitario": 2258500, "subtotal": 2258500, "costo_kardex": 0}
            ],
            "subtotal": 2258500,
            "iva": 0,
            "retefuente": 0,
            "reteiva": 0,
            "reteica": 0,
            "avisos": 0,
            "bomberil": 0,
            "autorretencion": 0,
            "total_neto": 2258500,
            "costo_total": 0,
            "observaciones": "Pago en Marzo del Formulario 300 de IVA (Hoja 49)."
        }
    ]

    # Enriquecer cada factura con los asientos contables reales y campos normalizados para el frontend
    for fac in facturas_realizadas:
        m_name = fac["mes"]
        h_name = str(fac["hoja"])
        tx_match = next((t for t in meses_data.get(m_name, {}).get("transacciones", []) if str(t["hoja"]) == h_name), None)
        is_venta = fac["categoria"] == "VENTA" or fac["id"].startswith("NC-V")
        fac["tercero"] = fac["tercero_nombre"] if is_venta else fac["emisor_nombre"]
        fac["nit_tercero"] = fac["tercero_nit"] if is_venta else fac["emisor_nit"]
        fac["regimen_vendedor"] = fac["emisor_regimen"]
        fac["regimen_comprador"] = fac["tercero_regimen"]
        fac["tipo_operacion"] = "FACTURA DE VENTA" if fac["categoria"] == "VENTA" else ("FACTURA DE COMPRA / DOCUMENTO SOPORTE" if fac["categoria"] == "COMPRA" else "NOTA CRÉDITO / DÉBITO / AJUSTE")
        fac["enunciado"] = (tx_match["enunciado"] if tx_match and tx_match.get("enunciado") else fac.get("observaciones", ""))
        fac["comprobante_diario"] = tx_match.get("comprobante_diario", f"Hoja {h_name}") if tx_match else f"Hoja {h_name}"
        fac["suma_letras"] = tx_match.get("suma_letras", "") if tx_match else ""
        fac["asientos"] = tx_match.get("asientos", []) if tx_match else []
        fac["total_debe"] = tx_match.get("total_debe", fac["total_neto"]) if tx_match else fac["total_neto"]
        fac["total_haber"] = tx_match.get("total_haber", fac["total_neto"]) if tx_match else fac["total_neto"]
        for it in fac.get("items", []):
            it["referencia"] = it.get("ref", "ITEM-01")
            it["valor_unitario"] = it.get("vlr_unitario", 0)

    db = {
        "meta": {
            "plataforma": "STUDENTCONT.IA",
            "version": "2.1.0",
            "actualizado": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "empresa": {
            "razon_social": "ELECTROVIVIENDA S.A.S",
            "nit": "901.765.438-3",
            "nit_sin_dv": "901765438",
            "dv": "3",
            "ultimo_digito_nit": "8",
            "regimen": "Régimen Responsable de IVA (RRI) - Agente de Retención y Autorretenedor en Renta",
            "grupo_niif": "Grupo 2 - NIIF para las PYMES (Decreto 2420 de 2015)",
            "sistema_inventario": "Sistema de Inventario Permanente - Método Promedio Ponderado",
            "direccion": "Cra 21 N° 46-11 Barrio La Concordia",
            "ciudad": "Bucaramanga, Santander",
            "telefono": "3164562001",
            "correo": "electroviviendasas@gmail.com",
            "elaborado_por": "Gina Villamizar",
            "contadora": "Gina Villamizar",
            "representante_legal": "Kevin Guerrero",
            "revisor_fiscal": "Marcela Gonzales",
            "logo": "assets/logo-electrovivienda.png",
            "socios": [
                {"nombre": "Carlos Eduardo Daza Gómez", "documento": "CC 83.540.201 de Bogotá", "aporte": 123000000},
                {"nombre": "Marco Aurelio Pedraza Díaz", "documento": "CC 83.630.202 de Tunja", "aporte": 125600000}
            ],
            "parametros_2026": {
                "uvt": 52374,
                "smlmv": 1750905,
                "auxilio_transporte": 249095,
                "iva_general": 0.19,
                "retefuente_compras_declarante": 0.025,
                "retefuente_compras_no_declarante": 0.035,
                "retefuente_servicios_declarante": 0.04,
                "autorretencion_renta_normal": 0.025,
                "autorretencion_renta_no_declarante": 0.035,
                "autorretencion_especial": 0.0055,
                "reteiva": 0.15,
                "reteica_bucaramanga_x_mil": 9.6,
                "avisos_y_tableros": 0.15,
                "sobretasa_bomberil": 0.10
            }
        },
        "puc": sorted(puc_master.values(), key=lambda x: x["codigo"]),
        "facturas": facturas_realizadas,
        "kardex": kardex_productos,
        "calendario_tributario": cal_items,
        "meses": meses_data
    }

    db_path = os.path.join(DATA_DIR, "electrovivienda_db.json")
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    print(f"OK: DB generada en {db_path}")
    print(f"PUC cuentas: {len(db['puc'])}")
    for m, d in meses_data.items():
        print(f"  {m}: {d['total_transacciones']} comprobantes/transacciones, {len(d['hojas_especiales'])} hojas de estados/libros/reportes")

if __name__ == "__main__":
    main()

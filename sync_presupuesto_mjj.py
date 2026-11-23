#!/usr/bin/env python3
"""
Extrae y sincroniza PRESUPUESTO_MAYO_JUNIO_JULIO_2026.xlsx (solo lectura data_only=True)
hacia data/presupuesto_mjj_2026.json para la plataforma web STUDENTCONT.IA.
"""
import datetime
import json
import os
import openpyxl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(BASE_DIR, "PRESUPUESTO_MAYO_JUNIO_JULIO_2026.xlsx")
OUT_PATH = os.path.join(BASE_DIR, "data", "presupuesto_mjj_2026.json")


def num(v, default=0.0):
    if v is None or isinstance(v, bool):
        return default
    if isinstance(v, (int, float)):
        return round(float(v), 2)
    return default


def txt(v, default=""):
    if v is None:
        return default
    return str(v).strip()


def split_ica(base, total_ica):
    ica = round(base * 0.0096, 2)
    avisos = round(ica * 0.15, 2)
    bomberil = round(total_ica - ica - avisos, 2)
    return ica, avisos, bomberil


def extract_month_operativo(ws, month_name):
    if month_name == "MAYO":
        v_rows = range(6, 11)
        inv_rows = range(17, 22)
        inv_tot = 22
        c_rows = range(26, 31)
        c_tot = 31
        t_rows = range(35, 41)
    else:
        v_rows = range(6, 10)
        inv_rows = range(17, 21)
        inv_tot = 21
        c_rows = range(25, 30)
        c_tot = 30
        t_rows = range(34, 40)

    ventas_filas = []
    for r in v_rows:
        vn = num(ws.cell(r, 7).value)
        ri = num(ws.cell(r, 9).value)
        v_ica, v_av, v_bom = split_ica(vn, ri)
        ventas_filas.append({
            "ref": txt(ws.cell(r, 1).value),
            "producto": txt(ws.cell(r, 2).value),
            "unidades": int(round(num(ws.cell(r, 3).value))),
            "costo_unit": num(ws.cell(r, 4).value),
            "costo_total": num(ws.cell(r, 5).value),
            "precio_venta": num(ws.cell(r, 6).value),
            "ventas_netas": vn,
            "iva": num(ws.cell(r, 8).value),
            "ica": v_ica,
            "avisos": v_av,
            "bomberil": v_bom,
            "reteica": ri,
            "neto_cobrar": num(ws.cell(r, 10).value),
            "autoret": num(ws.cell(r, 11).value),
        })

    v_tot_ica = round(sum(x["ica"] for x in ventas_filas), 2)
    v_tot_av = round(sum(x["avisos"] for x in ventas_filas), 2)
    v_tot_ri = num(ws.cell(11, 9).value)
    v_tot_bom = round(v_tot_ri - v_tot_ica - v_tot_av, 2)
    ventas_tot = {
        "unidades": int(round(num(ws.cell(11, 3).value))),
        "costo_total": num(ws.cell(11, 5).value),
        "ventas_netas": num(ws.cell(11, 7).value),
        "iva": num(ws.cell(11, 8).value),
        "ica": v_tot_ica,
        "avisos": v_tot_av,
        "bomberil": v_tot_bom,
        "reteica": v_tot_ri,
        "neto_cobrar": num(ws.cell(11, 10).value),
        "autoret": num(ws.cell(11, 11).value),
        "contado_50": num(ws.cell(12, 10).value),
        "credito_50": num(ws.cell(13, 10).value),
    }

    inv_filas = []
    for r in inv_rows:
        inv_filas.append({
            "ref": txt(ws.cell(r, 1).value),
            "producto": txt(ws.cell(r, 2).value),
            "vender": int(round(num(ws.cell(r, 3).value))),
            "inv_inicial": int(round(num(ws.cell(r, 4).value))),
            "stock_deseado": int(round(num(ws.cell(r, 5).value))),
            "comprar": int(round(num(ws.cell(r, 6).value))),
            "costo_unit": num(ws.cell(r, 7).value),
            "stock_final": int(round(num(ws.cell(r, 8).value))),
            "val_inv_final": num(ws.cell(r, 9).value),
            "val_inv_inicial": num(ws.cell(r, 10).value),
            "val_comprar": num(ws.cell(r, 11).value),
        })

    inv_totals = {
        "vender": int(round(num(ws.cell(inv_tot, 3).value))),
        "inv_inicial": int(round(num(ws.cell(inv_tot, 4).value))),
        "stock_deseado": int(round(num(ws.cell(inv_tot, 5).value))),
        "comprar": int(round(num(ws.cell(inv_tot, 6).value))),
        "stock_final": int(round(num(ws.cell(inv_tot, 8).value))),
        "val_inv_final": num(ws.cell(inv_tot, 9).value),
        "val_inv_inicial": num(ws.cell(inv_tot, 10).value),
        "val_comprar": num(ws.cell(inv_tot, 11).value),
    }

    comp_filas = []
    for r in c_rows:
        sub = num(ws.cell(r, 5).value)
        ri = num(ws.cell(r, 8).value)
        c_ica, c_av, c_bom = split_ica(sub, ri)
        comp_filas.append({
            "proveedor": txt(ws.cell(r, 1).value),
            "producto": txt(ws.cell(r, 2).value),
            "unidades": int(round(num(ws.cell(r, 3).value))),
            "costo_unit": num(ws.cell(r, 4).value),
            "subtotal": sub,
            "iva_desc": num(ws.cell(r, 6).value),
            "retefuente": num(ws.cell(r, 7).value),
            "ica": c_ica,
            "avisos": c_av,
            "bomberil": c_bom,
            "reteica": ri,
            "neto_pagar": num(ws.cell(r, 9).value),
            "contado_50": num(ws.cell(r, 10).value),
            "credito_50": num(ws.cell(r, 11).value),
        })

    c_tot_ica = round(sum(x["ica"] for x in comp_filas), 2)
    c_tot_av = round(sum(x["avisos"] for x in comp_filas), 2)
    c_tot_ri = num(ws.cell(c_tot, 8).value)
    c_tot_bom = round(c_tot_ri - c_tot_ica - c_tot_av, 2)
    comp_totals = {
        "unidades": int(round(num(ws.cell(c_tot, 3).value))),
        "subtotal": num(ws.cell(c_tot, 5).value),
        "iva_desc": num(ws.cell(c_tot, 6).value),
        "retefuente": num(ws.cell(c_tot, 7).value),
        "ica": c_tot_ica,
        "avisos": c_tot_av,
        "bomberil": c_tot_bom,
        "reteica": c_tot_ri,
        "neto_pagar": num(ws.cell(c_tot, 9).value),
        "contado_50": num(ws.cell(c_tot, 10).value),
        "credito_50": num(ws.cell(c_tot, 11).value),
    }

    trib_filas = []
    for r in t_rows:
        puc_raw = ws.cell(r, 2).value
        puc_str = str(int(puc_raw)) if isinstance(puc_raw, (int, float)) else txt(puc_raw)
        if puc_str == "2468":
            nota_m = "Pago mensual Hacienda Bucaramanga (mes siguiente)"
            trib_filas.extend([
                {
                    "concepto": "ICA retenido en compras (9,6 × 1.000)",
                    "puc": "246801",
                    "valor": comp_totals["ica"],
                    "nota": nota_m,
                },
                {
                    "concepto": "Avisos y Tableros retenidos (15% sobre ICA)",
                    "puc": "246802",
                    "valor": comp_totals["avisos"],
                    "nota": nota_m,
                },
                {
                    "concepto": "Sobretasa Bomberil retenida (10% sobre ICA)",
                    "puc": "246803",
                    "valor": comp_totals["bomberil"],
                    "nota": nota_m,
                },
                {
                    "concepto": "TOTAL RETEICA + AVISOS + BOMBERIL A PAGAR",
                    "puc": "2468",
                    "valor": comp_totals["reteica"],
                    "nota": "Declaración y pago mensual Hacienda Bucaramanga (mes siguiente)",
                },
            ])
        else:
            trib_filas.append({
                "concepto": txt(ws.cell(r, 1).value),
                "puc": puc_str,
                "valor": num(ws.cell(r, 3).value),
                "nota": txt(ws.cell(r, 4).value),
            })

    return {
        "ventas": {"filas": ventas_filas, "totales": ventas_tot},
        "inventario": {"filas": inv_filas, "totales": inv_totals},
        "compras": {"filas": comp_filas, "totales": comp_totals},
        "tributaria": trib_filas,
    }


def extract_efc(ws, month_name):
    if month_name == "MAYO":
        rows = range(5, 15)
        r_tot = 15
    elif month_name == "JUNIO":
        rows = range(3, 13)
        r_tot = 13
    else:
        rows = range(3, 14)
        r_tot = 14

    filas = []
    for r in rows:
        ent = ws.cell(r, 3).value
        sal = ws.cell(r, 4).value
        tot = ws.cell(r, 5).value
        filas.append({
            "concepto": txt(ws.cell(r, 2).value),
            "entrada": num(ent) if ent is not None else None,
            "salida": num(sal) if sal is not None else None,
            "total": num(tot),
        })

    return {
        "titulo": txt(ws.cell(3 if month_name == "MAYO" else 1, 2).value),
        "filas": filas,
        "saldo_inicial": num(ws.cell(rows.start, 5).value),
        "total_entradas": num(ws.cell(r_tot, 3).value),
        "total_salidas": num(ws.cell(r_tot, 4).value),
        "saldo_final": num(ws.cell(r_tot, 5).value),
    }


def extract_er(ws, month_name):
    # MAYO ER PROY uses cols F(6), G(7), I(9), J(10); JUNIO/JULIO ER PROY use cols B(2), C(3), E(5), F(6)
    if month_name == "MAYO":
        c_cod, c_nom, c_tot, c_par = 6, 7, 9, 10
    else:
        c_cod, c_nom, c_tot, c_par = 2, 3, 5, 6

    gastos_detalle = []
    for r in range(15, 23):
        val = num(ws.cell(r, c_par).value)
        if val != 0:
            gastos_detalle.append({
                "codigo": str(int(ws.cell(r, c_cod).value)),
                "cuenta": txt(ws.cell(r, c_nom).value),
                "valor": val,
            })

    ventas = num(ws.cell(10, c_par).value)
    costo_ventas = num(ws.cell(25, c_par).value)
    total_ingresos = num(ws.cell(13, c_tot).value)
    total_gastos = num(ws.cell(23, c_tot).value)
    total_costos = num(ws.cell(26, c_tot).value)
    utilidad_bruta = round(ventas - costo_ventas, 2)
    uai = num(ws.cell(27, c_tot).value)
    impuesto_renta = num(ws.cell(28, c_par).value)
    udi = num(ws.cell(29, c_tot).value)
    reserva_legal = num(ws.cell(30, c_par).value)
    utilidad_neta = num(ws.cell(31, c_tot).value)

    return {
        "periodo": txt(ws.cell(7, c_cod).value),
        "ingresos_4135": ventas,
        "devoluciones_4175": num(ws.cell(11, c_par).value),
        "financieros_4210": num(ws.cell(12, c_par).value),
        "total_ingresos": total_ingresos,
        "costos_6135": costo_ventas,
        "total_costos": total_costos,
        "utilidad_bruta": utilidad_bruta,
        "gastos_detalle": gastos_detalle,
        "total_gastos": total_gastos,
        "uai": uai,
        "impuesto_renta": impuesto_renta,
        "udi": udi,
        "reserva_legal": reserva_legal,
        "utilidad_neta": utilidad_neta,
    }


def extract_esf(ws):
    def item(r, col):
        return {
            "codigo": str(int(ws.cell(r, 2).value)),
            "cuenta": txt(ws.cell(r, 3).value),
            "valor": num(ws.cell(r, col).value),
        }

    act_corr = [item(r, 4) for r in (11, 12, 14, 15, 16, 18)]
    act_nocorr = [item(r, 4) for r in (22, 23, 24, 25)]
    pas_corr = [item(r, 5) for r in (31, 33, 35, 38, 39, 40, 41, 43, 44, 45, 47, 49)]
    pas_nocorr = [item(21, 5) if False else item(53, 5)]
    pat = [item(r, 5) for r in (58, 60, 62, 64, 65)]

    tot_act = num(ws.cell(27, 4).value)
    tot_pp = num(ws.cell(68, 4).value)

    return {
        "activos_corrientes": act_corr,
        "subtotal_ac": num(ws.cell(19, 4).value),
        "activos_no_corrientes": act_nocorr,
        "subtotal_anc": num(ws.cell(26, 4).value),
        "total_activos": tot_act,
        "pasivos_corrientes": pas_corr,
        "subtotal_pc": num(ws.cell(50, 5).value),
        "pasivos_no_corrientes": pas_nocorr,
        "subtotal_pnc": num(ws.cell(54, 5).value),
        "total_pasivos": num(ws.cell(55, 5).value),
        "patrimonio": pat,
        "total_patrimonio": num(ws.cell(67, 4).value),
        "total_pasivo_patrimonio": tot_pp,
        "diferencia": round(tot_act - tot_pp, 2),
    }


def main():
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)

    ws_p = wb["PARAMETROS"]
    params_lista = []
    for r in range(6, 21):
        p_nom = txt(ws_p.cell(r, 1).value)
        if "ReteICA Total" in p_nom or r == 20:
            params_lista.extend([
                {
                    "parametro": "ICA Bucaramanga — Tarifa Comercial (135518 / 246801)",
                    "valor": 0.0096,
                    "nota": "9,6 × 1.000 (0,96%) sobre base gravable — Pago mensual",
                },
                {
                    "parametro": "Avisos y Tableros (135520 / 246802)",
                    "valor": 0.15,
                    "nota": "15% liquidado sobre el valor del ICA (0,144% sobre base) — Pago mensual",
                },
                {
                    "parametro": "Sobretasa Bomberil (135525 / 246803)",
                    "valor": 0.10,
                    "nota": "10% liquidado sobre el valor del ICA (0,096% sobre base) — Pago mensual",
                },
            ])
        else:
            params_lista.append({
                "parametro": p_nom,
                "valor": num(ws_p.cell(r, 2).value),
                "nota": txt(ws_p.cell(r, 3).value),
            })

    neveras_prov = []
    for r in (6, 7, 8):
        neveras_prov.append({
            "proveedor": txt(ws_p.cell(r, 5).value),
            "precio": num(ws_p.cell(r, 6).value),
            "porcentaje": num(ws_p.cell(r, 7).value),
        })

    catalogo_precios = []
    for r in range(12, 17):
        costo = num(ws_p.cell(r, 6).value)
        precio = num(ws_p.cell(r, 7).value)
        catalogo_precios.append({
            "producto": txt(ws_p.cell(r, 5).value),
            "costo": costo,
            "precio_venta": precio,
            "ganancia_unit": round(precio - costo, 2),
        })

    tablero_comparativo = []
    for r in range(24, 39):
        tablero_comparativo.append({
            "concepto": txt(ws_p.cell(r, 1).value),
            "mayo": num(ws_p.cell(r, 2).value),
            "junio": num(ws_p.cell(r, 3).value),
            "julio": num(ws_p.cell(r, 4).value),
            "trimestre": num(ws_p.cell(r, 5).value),
        })

    ws_ta = wb["TA"]
    ta_params = {
        "t_efectiva": num(ws_ta["B3"].value),
        "t_nominal": num(ws_ta["B4"].value),
        "t_periodica": num(ws_ta["B5"].value),
        "plazo_meses": int(round(num(ws_ta["B6"].value))),
        "credito": num(ws_ta["B7"].value),
        "estudio_credito": num(ws_ta["B8"].value),
        "cuota": num(ws_ta["B9"].value),
    }
    mes_cuota = {1: "Febrero / Mar", 2: "Marzo / Abr", 3: "Mayo (Proy.)", 4: "Junio (Proy.)", 5: "Julio (Proy.)", 6: "Agosto"}
    # Nota según ER: R5=Marzo (Cuota 1), R6=Abril (Cuota 2), R7=Mayo (Cuota 3), R8=Junio (Cuota 4), R9=Julio (Cuota 5)
    cuota_mes_er = {1: "Marzo (Real)", 2: "Abril (Real)", 3: "MAYO (Proyectado)", 4: "JUNIO (Proyectado)", 5: "JULIO (Proyectado)", 6: "Agosto"}
    ta_cuotas = []
    for r in range(5, 11):
        n_c = int(round(num(ws_ta.cell(r, 4).value)))
        ta_cuotas.append({
            "cuota": n_c,
            "mes_contable": cuota_mes_er.get(n_c, ""),
            "valor_cuota": num(ws_ta.cell(r, 5).value),
            "abono_capital": num(ws_ta.cell(r, 6).value),
            "interes": num(ws_ta.cell(r, 7).value),
            "saldo_capital": num(ws_ta.cell(r, 8).value),
        })

    meses = {}
    for m in ("MAYO", "JUNIO", "JULIO"):
        op = extract_month_operativo(wb[m], m)
        op["efc"] = extract_efc(wb[f"EFC PROYECTADO {m}"], m)
        op["er"] = extract_er(wb[f"{m} ER PROY"], m)
        op["esf"] = extract_esf(wb[f"{m} ESF PROY"])
        meses[m] = op

    data = {
        "meta": {
            "empresa": "ELECTROVIVIENDA S.A.S",
            "nit": "901.765.438-3",
            "regimen": "RRI - Agente Autorretenedor de Renta",
            "archivo": "PRESUPUESTO_MAYO_JUNIO_JULIO_2026.xlsx",
            "hojas_count": len(wb.sheetnames),
            "hojas": wb.sheetnames,
            "meta_utilidad_mensual": num(ws_p["B9"].value),
            "saldo_inicial_caja_abril": num(wb["EFC PROYECTADO MAYO"]["E5"].value),
            "excel_mtime": datetime.datetime.fromtimestamp(os.path.getmtime(XLSX_PATH)).strftime("%Y-%m-%d %H:%M:%S"),
            "sincronizado_el": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        "parametros": {
            "reglas": params_lista,
            "proveedores_neveras": neveras_prov,
            "catalogo_precios": catalogo_precios,
            "tablero_comparativo": tablero_comparativo,
        },
        "amortizacion": {
            "condiciones": ta_params,
            "cuotas": ta_cuotas,
        },
        "meses": meses,
    }

    wb.close()

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Generado:", OUT_PATH)
    for m in ("MAYO", "JUNIO", "JULIO"):
        er = data["meses"][m]["er"]
        esf = data["meses"][m]["esf"]
        efc = data["meses"][m]["efc"]
        print(
            f"  {m:5s}: Ventas={er['ingresos_4135']:,.2f} | Costo={er['costos_6135']:,.2f} | "
            f"Gastos={er['total_gastos']:,.2f} | UN={er['utilidad_neta']:,.2f} | "
            f"Caja={efc['saldo_final']:,.2f} | Activos={esf['total_activos']:,.2f} | Diff={esf['diferencia']:,.2f}"
        )


if __name__ == "__main__":
    main()

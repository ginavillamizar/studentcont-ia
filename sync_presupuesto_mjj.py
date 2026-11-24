#!/usr/bin/env python3
"""
Extrae y sincroniza las 24 hojas de nuestro PRESUPUESTO_MAYO_JUNIO_JULIO_2026.xlsx
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


def extract_depreciacion(ws):
    local_anual = [
        {
            "np": int(round(num(ws.cell(r, 2).value))),
            "valor_inicial": num(ws.cell(r, 3).value),
            "dep_anual": num(ws.cell(r, 4).value),
            "dep_acumulada": num(ws.cell(r, 5).value),
            "saldo": num(ws.cell(r, 6).value),
        }
        for r in range(12, 33)
    ]
    local_mensual = [
        {
            "np": int(round(num(ws.cell(r, 2).value))),
            "valor_inicial": num(ws.cell(r, 3).value),
            "dep_mensual": num(ws.cell(r, 4).value),
            "dep_acumulada": num(ws.cell(r, 5).value),
            "saldo": num(ws.cell(r, 6).value),
        }
        for r in range(37, 50)
    ]
    carro_anual = [
        {
            "np": int(round(num(ws.cell(r, 8).value))),
            "valor_inicial": num(ws.cell(r, 9).value),
            "dep_anual": num(ws.cell(r, 10).value),
            "dep_acumulada": num(ws.cell(r, 11).value),
            "saldo": num(ws.cell(r, 12).value),
        }
        for r in range(12, 18)
    ]
    carro_mensual = [
        {
            "np": int(round(num(ws.cell(r, 8).value))),
            "valor_inicial": num(ws.cell(r, 9).value),
            "dep_mensual": num(ws.cell(r, 10).value),
            "dep_acumulada": num(ws.cell(r, 11).value),
            "saldo": num(ws.cell(r, 12).value),
        }
        for r in range(22, 35)
    ]
    return {
        "local": {
            "nombre": "ACTIVO FIJO DEPRECIABLE LOCAL (Calle 85 N° 15-80)",
            "cuenta_gasto": "52600501",
            "cuenta_acum": "15920501",
            "valor_libros": num(ws["D3"].value),
            "valor_salvamento": num(ws["D4"].value),
            "porc_salvamento": num(ws["E5"].value),
            "valor_depreciar": num(ws["D5"].value),
            "vida_util_anual": int(round(num(ws["D6"].value))),
            "vida_util_mensual": int(round(num(ws["D7"].value))),
            "porc_depreciacion": num(ws["E7"].value),
            "cuota_anual": num(ws["D13"].value),
            "cuota_mensual": num(ws["D38"].value),
            "tabla_anual": local_anual,
            "tabla_mensual": local_mensual,
        },
        "carro": {
            "nombre": "ACTIVO FIJO DEPRECIABLE CARRO (Camioneta HBA005)",
            "cuenta_gasto": "51603501",
            "cuenta_acum": "15923501",
            "valor_libros": num(ws["J3"].value),
            "valor_salvamento": num(ws["J4"].value),
            "porc_salvamento": num(ws["K5"].value),
            "valor_depreciar": num(ws["J5"].value),
            "vida_util_anual": int(round(num(ws["J6"].value))),
            "vida_util_mensual": int(round(num(ws["J7"].value))),
            "porc_depreciacion": num(ws["K7"].value),
            "cuota_anual": num(ws["J13"].value),
            "cuota_mensual": num(ws["J23"].value),
            "tabla_anual": carro_anual,
            "tabla_mensual": carro_mensual,
        },
        "comprobante_mensual": {
            "ciudad": "Bucaramanga",
            "elaborado_por": "Gina Villamizar",
            "total_mensual": num(ws["Q19"].value),
        },
    }


def extract_amortizacion(ws_ta):
    ta_params = {
        "t_efectiva": round(float(ws_ta["B3"].value or 0), 6),
        "t_nominal": round(float(ws_ta["B4"].value or 0), 6),
        "t_periodica": round(float(ws_ta["B5"].value or 0), 6),
        "plazo_meses": int(round(num(ws_ta["B6"].value))),
        "credito": num(ws_ta["B7"].value),
        "estudio_credito": num(ws_ta["B8"].value),
        "desembolso_neto": num(ws_ta["H4"].value),
        "cuota": num(ws_ta["B9"].value),
        "tir_mensual": round(float(ws_ta["K41"].value or 0), 6),
    }
    cuota_mes_er = {
        1: "Marzo 2026 (Ejecutado)",
        2: "Abril 2026 (Ejecutado)",
        3: "MAYO 2026 (Proyectado)",
        4: "JUNIO 2026 (Proyectado)",
        5: "JULIO 2026 (Proyectado)",
    }
    cuotas = [
        {
            "cuota": int(round(num(ws_ta.cell(r, 4).value))),
            "mes_contable": cuota_mes_er.get(int(round(num(ws_ta.cell(r, 4).value))), f"Mes {int(round(num(ws_ta.cell(r, 4).value)))}"),
            "valor_cuota": num(ws_ta.cell(r, 5).value),
            "abono_capital": num(ws_ta.cell(r, 6).value),
            "interes": num(ws_ta.cell(r, 7).value),
            "saldo_capital": num(ws_ta.cell(r, 8).value),
        }
        for r in range(5, 41)
    ]
    return {
        "condiciones": ta_params,
        "cuotas": cuotas,
        "totales": {
            "total_cuotas": num(ws_ta["E41"].value),
            "total_capital": num(ws_ta["F41"].value),
            "total_intereses": num(ws_ta["G41"].value),
        },
    }


def extract_nomina(ws):
    empleados = []
    for r, r_prov in [(11, 22), (12, 23)]:
        empleados.append({
            "nombre": txt(ws.cell(r, 3).value),
            "horas": int(round(num(ws.cell(r, 4).value))),
            "salario_basico": num(ws.cell(r, 5).value),
            "basico": num(ws.cell(r, 6).value),
            "aux_transporte": num(ws.cell(r, 10).value),
            "total_devengado": num(ws.cell(r, 11).value),
            "ibc": num(ws.cell(r, 12).value),
            "salud_trabajador": num(ws.cell(r, 13).value),
            "pension_trabajador": num(ws.cell(r, 14).value),
            "fsp": num(ws.cell(r, 15).value),
            "total_deducciones": num(ws.cell(r, 18).value),
            "neto_pagar": num(ws.cell(r, 19).value),
            "cesantias": num(ws.cell(r_prov, 6).value),
            "intereses_cesantias": num(ws.cell(r_prov, 7).value),
            "prima": num(ws.cell(r_prov, 8).value),
            "ibc_vacaciones": num(ws.cell(r_prov, 9).value),
            "vacaciones": num(ws.cell(r_prov, 10).value),
            "total_provisiones": num(ws.cell(r_prov, 11).value),
            "salud_empleador": num(ws.cell(r_prov, 12).value),
            "pension_empleador": num(ws.cell(r_prov, 13).value),
            "arl": num(ws.cell(r_prov, 14).value),
            "icbf": num(ws.cell(r_prov, 15).value),
            "sena": num(ws.cell(r_prov, 16).value),
            "ccf": num(ws.cell(r_prov, 17).value),
        })
    tot_prov = round(sum(e["total_provisiones"] for e in empleados), 2)
    tot_paraf = round(sum(e["pension_empleador"] + e["arl"] + e["ccf"] for e in empleados), 2)
    tot_dev = num(ws["K15"].value)
    return {
        "fecha": "2026-04-30",
        "smlmv": num(ws["D5"].value),
        "tope_4_smlmv": num(ws["E5"].value),
        "empleados": empleados,
        "totales": {
            "total_devengado": tot_dev,
            "salud_trabajador": num(ws["M15"].value),
            "pension_trabajador": num(ws["N15"].value),
            "total_deducciones": num(ws["R15"].value),
            "neto_pagar": num(ws["S15"].value),
            "cesantias": num(ws["F26"].value),
            "intereses_cesantias": num(ws["G26"].value),
            "prima": num(ws["H26"].value),
            "vacaciones": num(ws["J26"].value),
            "total_provisiones_2610": tot_prov,
            "pension_empleador": num(ws["M26"].value),
            "arl": num(ws["N26"].value),
            "ccf": num(ws["Q26"].value),
            "total_seg_social_empleador": tot_paraf,
            "total_beneficios_empleados_5105": round(tot_dev + tot_prov + tot_paraf, 2),
        },
    }


def extract_esf_abril(ws):
    def item(r, col):
        return {
            "codigo": str(int(ws.cell(r, 2).value)),
            "cuenta": txt(ws.cell(r, 3).value),
            "valor": num(ws.cell(r, col).value),
        }
    return {
        "periodo": txt(ws.cell(6, 3).value),
        "activos_corrientes": [item(r, 5) for r in (11, 12, 14, 15, 17)],
        "subtotal_ac": num(ws.cell(18, 5).value),
        "activos_no_corrientes": [item(r, 5) for r in (21, 22, 23, 24)],
        "subtotal_anc": num(ws.cell(25, 5).value),
        "total_activos": num(ws.cell(26, 5).value),
        "pasivos_corrientes": [item(r, 6) for r in (30, 32, 34, 36, 37, 38, 40, 41, 43, 45)],
        "subtotal_pc": num(ws.cell(46, 6).value),
        "pasivos_no_corrientes": [item(49, 6)],
        "subtotal_pnc": num(ws.cell(50, 6).value),
        "total_pasivos": num(ws.cell(51, 6).value),
        "patrimonio": [item(r, 6) for r in (54, 56, 58, 60, 61)],
        "total_patrimonio": num(ws.cell(62, 6).value),
        "total_pasivo_patrimonio": num(ws.cell(63, 6).value),
        "diferencia": 0.0,
    }


def extract_month_operativo(ws, month_name):
    if month_name == "MAYO":
        v_rows, inv_rows, inv_tot, c_rows, c_tot, t_rows, sr = range(6, 11), range(17, 22), 22, range(26, 31), 31, range(35, 41), 42
    else:
        v_rows, inv_rows, inv_tot, c_rows, c_tot, t_rows, sr = range(6, 10), range(17, 21), 21, range(25, 30), 30, range(34, 40), 41

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

    inv_filas = [
        {
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
        }
        for r in inv_rows
    ]
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
        if puc_str in ("2468", "2368"):
            nota_m = "Pago mensual Hacienda Bucaramanga (mes siguiente)"
            trib_filas.extend([
                {"concepto": "ICA retenido en compras (9,6 × 1.000)", "puc": "246801", "valor": comp_totals["ica"], "nota": nota_m},
                {"concepto": "Avisos y Tableros retenidos (15% sobre ICA)", "puc": "246802", "valor": comp_totals["avisos"], "nota": nota_m},
                {"concepto": "Sobretasa Bomberil retenida (10% sobre ICA)", "puc": "246803", "valor": comp_totals["bomberil"], "nota": nota_m},
                {"concepto": "TOTAL RETEICA + AVISOS + BOMBERIL A PAGAR", "puc": "2468", "valor": comp_totals["reteica"], "nota": "Declaración y pago mensual Hacienda Bucaramanga (mes siguiente)"},
            ])
        else:
            trib_filas.append({
                "concepto": txt(ws.cell(r, 1).value),
                "puc": puc_str,
                "valor": num(ws.cell(r, 3).value),
                "nota": txt(ws.cell(r, 4).value),
            })

    # Extract Section 5 (Cédula de Gastos) & Section 6 (Proyección Meta y Unidades)
    gastos_tabla = [
        {"codigo": txt(ws.cell(r, 1).value), "concepto": txt(ws.cell(r, 2).value), "valor": num(ws.cell(r, 3).value)}
        for r in range(sr + 2, sr + 7)
    ]
    tasas_meta = {
        "tasa_ea": num(ws.cell(sr + 2, 8).value),
        "tasa_nominal": round(float(ws.cell(sr + 3, 8).value or 0), 6),
        "tasa_mensual": round(float(ws.cell(sr + 4, 8).value or 0), 6),
        "capital_suscrito": num(ws.cell(sr + 5, 8).value),
        "resultado_proyectado": num(ws.cell(sr + 6, 8).value),
        "resultado_teorico": num(ws.cell(sr + 6, 8).value),
        "resultado_practico": num(ws.cell(sr + 7, 8).value),
        "diferencia_resultado": num(ws.cell(sr + 7, 11).value),
        "uai_meta": num(ws.cell(sr + 2, 11).value),
        "udi_meta": num(ws.cell(sr + 3, 11).value),
        "un_meta": num(ws.cell(sr + 4, 11).value),
        "ganancia_vender_1_und": num(ws.cell(sr + 5, 11).value),
        "unidades_a_comprar_factor": round(float(ws.cell(sr + 6, 11).value or 0), 4),
        "gastos_proyectados": num(ws.cell(sr + 6, 3).value),
    }

    return {
        "proyectado": {"tasas_meta": tasas_meta, "gastos": gastos_tabla},
        "ventas": {"filas": ventas_filas, "totales": ventas_tot},
        "inventario": {"filas": inv_filas, "totales": inv_totals},
        "compras": {"filas": comp_filas, "totales": comp_totals},
        "tributaria": trib_filas,
    }


def extract_efc(ws, month_name):
    if month_name == "MAYO":
        rows, r_tot, r_exc = range(5, 16), 16, 18
    else:
        rows, r_tot, r_exc = range(3, 14), 14, 16

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
        "excedente": num(ws.cell(r_exc, 3).value),
    }


def extract_er(ws, month_name):
    c_cod, c_nom, c_tot, c_par = (6, 7, 9, 10) if month_name == "MAYO" else (2, 3, 5, 6)
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
    return {
        "periodo": txt(ws.cell(7, c_cod).value),
        "ingresos_4135": ventas,
        "devoluciones_4175": num(ws.cell(11, c_par).value),
        "financieros_4210": num(ws.cell(12, c_par).value),
        "total_ingresos": num(ws.cell(13, c_tot).value),
        "costos_6135": costo_ventas,
        "total_costos": num(ws.cell(26, c_tot).value),
        "utilidad_bruta": round(ventas - costo_ventas, 2),
        "gastos_detalle": gastos_detalle,
        "total_gastos": num(ws.cell(23, c_tot).value),
        "uai": num(ws.cell(27, c_tot).value),
        "impuesto_renta": num(ws.cell(28, c_par).value),
        "udi": num(ws.cell(29, c_tot).value),
        "reserva_legal": num(ws.cell(30, c_par).value),
        "utilidad_neta": num(ws.cell(31, c_tot).value),
    }


def extract_esf(ws):
    def item(r, col):
        return {
            "codigo": str(int(ws.cell(r, 2).value)),
            "cuenta": txt(ws.cell(r, 3).value),
            "valor": num(ws.cell(r, col).value),
        }
    tot_act = num(ws.cell(27, 4).value)
    tot_pp = num(ws.cell(68, 4).value)
    return {
        "activos_corrientes": [item(r, 4) for r in (11, 12, 14, 15, 16, 18)],
        "subtotal_ac": num(ws.cell(19, 4).value),
        "activos_no_corrientes": [item(r, 4) for r in (22, 23, 24, 25)],
        "subtotal_anc": num(ws.cell(26, 4).value),
        "total_activos": tot_act,
        "pasivos_corrientes": [item(r, 5) for r in (31, 33, 35, 38, 39, 40, 41, 43, 44, 45, 47, 49)],
        "subtotal_pc": num(ws.cell(50, 5).value),
        "pasivos_no_corrientes": [item(53, 5)],
        "subtotal_pnc": num(ws.cell(54, 5).value),
        "total_pasivos": num(ws.cell(55, 5).value),
        "patrimonio": [item(r, 5) for r in (58, 60, 62, 64, 65)],
        "total_patrimonio": num(ws.cell(67, 4).value),
        "total_pasivo_patrimonio": tot_pp,
        "diferencia": round(tot_act - tot_pp, 2),
    }


def extract_maestro(ws):
    gastos_trim = [
        {
            "concepto": txt(ws.cell(r, 2).value),
            "mayo": num(ws.cell(r, 3).value),
            "junio": num(ws.cell(r, 4).value),
            "julio": num(ws.cell(r, 5).value),
            "total": num(ws.cell(r, 6).value),
        }
        for r in range(4, 9)
    ]
    flujo_comp = [
        {
            "concepto": txt(ws.cell(r, 2).value),
            "mayo_ent": num(ws.cell(r, 3).value) if ws.cell(r, 3).value is not None else None,
            "mayo_sal": num(ws.cell(r, 4).value) if ws.cell(r, 4).value is not None else None,
            "mayo_tot": num(ws.cell(r, 5).value),
            "junio_ent": num(ws.cell(r, 6).value) if ws.cell(r, 6).value is not None else None,
            "junio_sal": num(ws.cell(r, 7).value) if ws.cell(r, 7).value is not None else None,
            "junio_tot": num(ws.cell(r, 8).value),
            "julio_ent": num(ws.cell(r, 9).value) if ws.cell(r, 9).value is not None else None,
            "julio_sal": num(ws.cell(r, 10).value) if ws.cell(r, 10).value is not None else None,
            "julio_tot": num(ws.cell(r, 11).value),
        }
        for r in range(29, 43)
    ]
    return {"gastos_trimestre": gastos_trim, "flujo_caja_comparativo": flujo_comp}


def main():
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
    ws_p = wb["PARAMETROS"]

    params_lista = []
    for r in range(6, 21):
        p_nom = txt(ws_p.cell(r, 1).value)
        if "ReteICA Total" in p_nom or r == 20:
            params_lista.extend([
                {"parametro": "ICA Bucaramanga — Tarifa Comercial (135518 / 246801)", "valor": 0.0096, "nota": "9,6 × 1.000 (0,96%) sobre base gravable — Pago mensual"},
                {"parametro": "Avisos y Tableros (135520 / 246802)", "valor": 0.15, "nota": "15% liquidado sobre el valor del ICA (0,144% sobre base) — Pago mensual"},
                {"parametro": "Sobretasa Bomberil (135525 / 246803)", "valor": 0.10, "nota": "10% liquidado sobre el valor del ICA (0,096% sobre base) — Pago mensual"},
            ])
        else:
            params_lista.append({"parametro": p_nom, "valor": num(ws_p.cell(r, 2).value), "nota": txt(ws_p.cell(r, 3).value)})

    neveras_prov = [{"proveedor": txt(ws_p.cell(r, 5).value), "precio": num(ws_p.cell(r, 6).value), "porcentaje": num(ws_p.cell(r, 7).value)} for r in (6, 7, 8)]
    catalogo_precios = [
        {"producto": txt(ws_p.cell(r, 5).value), "costo": num(ws_p.cell(r, 6).value), "precio_venta": num(ws_p.cell(r, 7).value), "ganancia_unit": round(num(ws_p.cell(r, 7).value) - num(ws_p.cell(r, 6).value), 2)}
        for r in range(12, 17)
    ]
    tablero_comparativo = [
        {"concepto": txt(ws_p.cell(r, 1).value), "mayo": num(ws_p.cell(r, 2).value), "junio": num(ws_p.cell(r, 3).value), "julio": num(ws_p.cell(r, 4).value), "trimestre": num(ws_p.cell(r, 5).value)}
        for r in range(24, 39)
    ]

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
        "depreciacion": extract_depreciacion(wb["DEP"]),
        "amortizacion": extract_amortizacion(wb["TA"]),
        "nomina_abril": extract_nomina(wb["NOM"]),
        "esf_abril": extract_esf_abril(wb["ESF ABRIL"]),
        "maestro": extract_maestro(wb["MAESTRO"]),
        "meses": meses,
    }

    wb.close()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Generado:", OUT_PATH, "| Hojas:", data["meta"]["hojas_count"])
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

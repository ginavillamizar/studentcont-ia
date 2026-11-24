#!/usr/bin/env python3
"""
Extrae y sincroniza las 25 hojas de PRESUPUESTO_MAYO_JUNIO_JULIO_2026.xlsx
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


def split_ica(base):
    ica = round(base * 0.0096, 2)
    avisos = round(ica * 0.15, 2)
    bomberil = round(ica * 0.10, 2)
    return ica, avisos, bomberil, round(ica + avisos + bomberil, 2)


def extract_depreciacion(ws):
    local_anual = []
    for r in range(12, 33):
        local_anual.append({
            "np": int(round(num(ws.cell(r, 2).value))),
            "valor_inicial": num(ws.cell(r, 3).value),
            "dep_anual": num(ws.cell(r, 4).value),
            "dep_acumulada": num(ws.cell(r, 5).value),
            "saldo": num(ws.cell(r, 6).value),
        })
    local_mensual = []
    for r in range(37, 50):
        local_mensual.append({
            "np": int(round(num(ws.cell(r, 2).value))),
            "valor_inicial": num(ws.cell(r, 3).value),
            "dep_mensual": num(ws.cell(r, 4).value),
            "dep_acumulada": num(ws.cell(r, 5).value),
            "saldo": num(ws.cell(r, 6).value),
        })
    carro_anual = []
    for r in range(12, 18):
        carro_anual.append({
            "np": int(round(num(ws.cell(r, 8).value))),
            "valor_inicial": num(ws.cell(r, 9).value),
            "dep_anual": num(ws.cell(r, 10).value),
            "dep_acumulada": num(ws.cell(r, 11).value),
            "saldo": num(ws.cell(r, 12).value),
        })
    carro_mensual = []
    for r in range(22, 35):
        carro_mensual.append({
            "np": int(round(num(ws.cell(r, 8).value))),
            "valor_inicial": num(ws.cell(r, 9).value),
            "dep_mensual": num(ws.cell(r, 10).value),
            "dep_acumulada": num(ws.cell(r, 11).value),
            "saldo": num(ws.cell(r, 12).value),
        })
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
            "asientos": [
                {"codigo": "51603501", "cuenta": "Depreciación Flota y Equipo de Transporte (HBA005)", "debe": num(ws["Q8"].value), "haber": 0.0},
                {"codigo": "52600501", "cuenta": "Depreciación Construcciones y Edificaciones (Local Calle 85)", "debe": num(ws["Q11"].value), "haber": 0.0},
                {"codigo": "15920501", "cuenta": "Depreciación Acumulada Construcciones y Edificaciones (CR)", "debe": 0.0, "haber": num(ws["P16"].value)},
                {"codigo": "15923501", "cuenta": "Depreciación Acumulada Flota y Equipo de Transporte (CR)", "debe": 0.0, "haber": num(ws["P18"].value)},
            ],
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
    cuotas = []
    for r in range(5, 41):
        n_c = int(round(num(ws_ta.cell(r, 4).value)))
        cuotas.append({
            "cuota": n_c,
            "mes_contable": cuota_mes_er.get(n_c, f"Mes {n_c}"),
            "valor_cuota": num(ws_ta.cell(r, 5).value),
            "abono_capital": num(ws_ta.cell(r, 6).value),
            "interes": num(ws_ta.cell(r, 7).value),
            "saldo_capital": num(ws_ta.cell(r, 8).value),
        })
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
        "enunciado": txt(ws["A3"].value),
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
            "pago_mensual_seg_social_efc": round(num(ws["M15"].value) + num(ws["N15"].value) + tot_paraf, 2),
        },
    }


def extract_esf_sheet(ws):
    def item(r, col):
        return {
            "codigo": str(int(ws.cell(r, 2).value)),
            "cuenta": txt(ws.cell(r, 3).value),
            "valor": num(ws.cell(r, col).value),
        }

    act_corr = [item(r, 5) for r in (11, 12, 14, 15, 17) if ws.cell(r, 2).value is not None]
    act_nocorr = [item(r, 5) for r in (21, 22, 23, 24)]

    # ESF ABRIL has different row indices for Pasivos than ESF PROYECTADO MAYO/JUNIO/JULIO
    is_abril = txt(ws.cell(6, 3).value).upper().find("ABRIL") >= 0
    if is_abril:
        pas_corr = [item(r, 6) for r in (30, 32, 34, 36, 37, 38, 40, 41, 43, 45)]
        sub_pc = num(ws.cell(46, 6).value)
        pas_nocorr = [item(49, 6)]
        sub_pnc = num(ws.cell(50, 6).value)
        tot_pas = num(ws.cell(51, 6).value)
        pat = [item(r, 6) for r in (54, 56, 58, 60, 61)]
        tot_pat = num(ws.cell(62, 6).value)
        tot_pp = num(ws.cell(63, 6).value)
    else:
        pas_corr = [item(r, 6) for r in (30, 32, 34, 35, 36, 37, 39, 40, 42, 44)]
        sub_pc = num(ws.cell(45, 6).value)
        pas_nocorr = [item(48, 6)]
        sub_pnc = num(ws.cell(49, 6).value)
        tot_pas = num(ws.cell(50, 6).value)
        pat = [item(r, 6) for r in (53, 55, 57, 59, 60)]
        tot_pat = num(ws.cell(61, 6).value)
        tot_pp = num(ws.cell(62, 6).value)

    tot_act = num(ws.cell(26, 5).value)
    return {
        "periodo": txt(ws.cell(6, 3).value),
        "activos_corrientes": act_corr,
        "subtotal_ac": num(ws.cell(18, 5).value),
        "activos_no_corrientes": act_nocorr,
        "subtotal_anc": num(ws.cell(25, 5).value),
        "total_activos": tot_act,
        "pasivos_corrientes": pas_corr,
        "subtotal_pc": sub_pc,
        "pasivos_no_corrientes": pas_nocorr,
        "subtotal_pnc": sub_pnc,
        "total_pasivos": tot_pas,
        "patrimonio": pat,
        "total_patrimonio": tot_pat,
        "total_pasivo_patrimonio": tot_pp,
        "diferencia": round(tot_act - tot_pp, 2),
    }


def extract_er_sheet(ws):
    gastos_detalle = []
    for r in (15, 16, 17, 18):
        gastos_detalle.append({
            "codigo": str(int(ws.cell(r, 2).value)),
            "cuenta": txt(ws.cell(r, 3).value),
            "valor": num(ws.cell(r, 4).value),
        })
    ventas = num(ws.cell(9, 4).value)
    costos = num(ws.cell(12, 4).value)
    return {
        "periodo": txt(ws.cell(6, 2).value),
        "ingresos_4135": ventas,
        "devoluciones_4175": 0.0,
        "financieros_4210": 0.0,
        "total_ingresos": num(ws.cell(10, 4).value),
        "costos_6135": costos,
        "total_costos": num(ws.cell(13, 4).value),
        "utilidad_bruta": round(ventas - costos, 2),
        "gastos_detalle": gastos_detalle,
        "total_gastos": num(ws.cell(19, 4).value),
        "uai": num(ws.cell(20, 4).value),
        "impuesto_renta": num(ws.cell(21, 4).value),
        "udi": num(ws.cell(22, 4).value),
        "reserva_legal": num(ws.cell(23, 4).value),
        "utilidad_neta": num(ws.cell(24, 4).value),
    }


def extract_efc_sheet(ws, month_name):
    filas = []
    for r in range(4, 15):
        conc = txt(ws.cell(r, 2).value)
        if not conc:
            continue
        ent = ws.cell(r, 3).value
        sal = ws.cell(r, 4).value
        tot = ws.cell(r, 5).value
        filas.append({
            "concepto": conc,
            "entrada": num(ent) if ent is not None else None,
            "salida": num(sal) if sal is not None else None,
            "total": num(tot),
        })
    return {
        "titulo": f"CAJA — EFC PROYECTADO {month_name} 2026",
        "filas": filas,
        "saldo_inicial": num(ws.cell(4, 5).value),
        "total_entradas": num(ws.cell(15, 3).value),
        "total_salidas": num(ws.cell(15, 4).value),
        "saldo_final": num(ws.cell(15, 5).value),
        "excedente": num(ws.cell(18, 3).value),
    }


def extract_com_sheet(ws):
    # Extract the 3 supplier blocks from COM MAYO / COM JUNIO / COM JULIO
    def ret_box(r_start, col_val):
        return {
            "base": num(ws.cell(r_start, col_val).value),
            "iva": num(ws.cell(r_start + 1, col_val).value),
            "retefuente": num(ws.cell(r_start + 2, col_val).value),
            "autoret": num(ws.cell(r_start + 3, col_val).value),
            "reteiva": num(ws.cell(r_start + 4, col_val).value),
            "reteica": num(ws.cell(r_start + 5, col_val).value),
            "avisos": num(ws.cell(r_start + 6, col_val).value),
            "bomberil": num(ws.cell(r_start + 7, col_val).value),
            "total": num(ws.cell(r_start + 8, col_val).value),
        }

    proveedores = [
        {
            "proveedor": "CASA ORANGE",
            "regimen": "RRI (Responsable de IVA)",
            "items": [
                {"producto": txt(ws["B4"].value), "unidades": int(round(num(ws["C4"].value))), "base_unit": num(ws["D4"].value), "base_total": num(ws["E4"].value), **ret_box(6, 8)},
                {"producto": txt(ws["B5"].value), "unidades": int(round(num(ws["C5"].value))), "base_unit": num(ws["D5"].value), "base_total": num(ws["E5"].value), **ret_box(6, 11)},
            ],
            "total_unidades": int(round(num(ws["C6"].value))),
            "total_base": num(ws["E6"].value),
            "contado_50": num(ws["C44"].value),
            "credito_50": num(ws["D44"].value),
        },
        {
            "proveedor": "ELECTRODOMÉSTICOS CRA 13",
            "regimen": "RRI (Responsable de IVA)",
            "items": [
                {"producto": txt(ws["B18"].value), "unidades": int(round(num(ws["C18"].value))), "base_unit": num(ws["D18"].value), "base_total": num(ws["E18"].value), **ret_box(20, 8)},
                {"producto": txt(ws["B19"].value), "unidades": int(round(num(ws["C19"].value))), "base_unit": num(ws["D19"].value), "base_total": num(ws["E19"].value), **ret_box(20, 11)},
            ],
            "total_unidades": int(round(num(ws["C20"].value))),
            "total_base": num(ws["E20"].value),
            "contado_50": num(ws["C45"].value),
            "credito_50": num(ws["D45"].value),
        },
        {
            "proveedor": "ELECTROMENORES",
            "regimen": "RNRI Declarante (No Responsable de IVA)",
            "items": [
                {"producto": txt(ws["B33"].value), "unidades": int(round(num(ws["C33"].value))), "base_unit": num(ws["D33"].value), "base_total": num(ws["E33"].value), **ret_box(35, 8)},
            ],
            "total_unidades": int(round(num(ws["C34"].value))),
            "total_base": num(ws["E34"].value),
            "contado_50": num(ws["C46"].value),
            "credito_50": num(ws["D46"].value),
        },
    ]

    # Flatten rows for standard compras table compatibility
    comp_filas = []
    for p in proveedores:
        for it in p["items"]:
            comp_filas.append({
                "proveedor": p["proveedor"],
                "producto": it["producto"],
                "unidades": it["unidades"],
                "costo_unit": it["base_unit"],
                "subtotal": it["base"],
                "iva_desc": it["iva"],
                "retefuente": it["retefuente"],
                "ica": it["reteica"],
                "avisos": it["avisos"],
                "bomberil": it["bomberil"],
                "reteica": round(it["reteica"] + it["avisos"] + it["bomberil"], 2),
                "neto_pagar": it["total"],
                "contado_50": round(it["total"] / 2.0, 2),
                "credito_50": round(it["total"] / 2.0, 2),
            })

    comp_totals = {
        "unidades": sum(x["unidades"] for x in comp_filas),
        "subtotal": round(sum(x["subtotal"] for x in comp_filas), 2),
        "iva_desc": num(ws["H47"].value),
        "retefuente": num(ws["H49"].value),
        "ica": round(sum(x["ica"] for x in comp_filas), 2),
        "avisos": round(sum(x["avisos"] for x in comp_filas), 2),
        "bomberil": round(sum(x["bomberil"] for x in comp_filas), 2),
        "reteica": num(ws["H48"].value),
        "neto_pagar": round(num(ws["C47"].value) + num(ws["D47"].value), 2),
        "contado_50": num(ws["C47"].value),
        "credito_50": num(ws["D47"].value),
    }
    return proveedores, {"filas": comp_filas, "totales": comp_totals}


def extract_vta_and_proy(ws_vta, ws_proy, ws_com_data, month_name):
    # Extract PROYECTADO sheet parameters & tables
    tasas_meta = {
        "tasa_ea": num(ws_proy["C4"].value),
        "tasa_nominal": round(float(ws_proy["C5"].value or 0), 6),
        "tasa_mensual": round(float(ws_proy["C6"].value or 0), 6),
        "capital_suscrito": num(ws_proy["C7"].value),
        "resultado_proyectado": num(ws_proy["C8"].value),
        "gastos_proyectados": num(ws_proy["C10"].value),
        "resultado_teorico": num(ws_proy["C15"].value),
        "resultado_practico": num(ws_proy["C16"].value),
        "diferencia_resultado": num(ws_proy["C17"].value),
        "uai_meta": num(ws_proy["C20"].value),
        "udi_meta": num(ws_proy["C21"].value),
        "un_meta": num(ws_proy["C22"].value),
        "ganancia_vender_1_und": num(ws_proy["C25"].value),
        "unidades_a_comprar_factor": round(float(ws_proy["C26"].value or 0), 4),
    }

    gastos_tabla = [
        {"concepto": txt(ws_proy[f"B{r}"].value), "valor": num(ws_proy[f"C{r}"].value)}
        for r in range(31, 36)
    ]

    # Build ventas_filas & inventario_filas
    ventas_filas = []
    inv_filas = []

    if month_name == "MAYO":
        # Inventario inicial (rows 14..17 of PROYECTADO MAYO / rows 5..8 of VTA MAYO)
        inv_init_items = []
        for r in range(14, 18):
            prod = txt(ws_proy.cell(r, 5).value)
            und = int(round(num(ws_proy.cell(r, 6).value)))
            c_unt = num(ws_proy.cell(r, 7).value)
            c_tot = num(ws_proy.cell(r, 8).value)
            b_vta = num(ws_proy.cell(r, 9).value)
            g_unt = num(ws_proy.cell(r, 10).value)
            g_tot = num(ws_proy.cell(r, 11).value)
            ing_tot = num(ws_proy.cell(r, 12).value)
            inv_init_items.append({
                "producto": prod, "unidades": und, "costo_unit": c_unt, "costo_total": c_tot,
                "base_venta": b_vta, "ganancia_unit": g_unt, "ganancia_total": g_tot, "ingreso_total": ing_tot
            })
            ica, av, bom, tot_ica = split_ica(ing_tot)
            iva = round(ing_tot * 0.19, 2)
            ret_f = round(ing_tot * 0.025, 2)
            ventas_filas.append({
                "ref": "INV. INICIAL",
                "producto": f"{prod} (Inventario Inicial)",
                "unidades": und,
                "costo_unit": c_unt,
                "costo_total": c_tot,
                "precio_venta": b_vta,
                "ventas_netas": ing_tot,
                "iva": iva,
                "retefuente": ret_f,
                "ica": ica,
                "avisos": av,
                "bomberil": bom,
                "reteica": tot_ica,
                "neto_cobrar": round(ing_tot + iva - ret_f - tot_ica, 2),
                "autoret": ret_f,
            })

        comprar_items = []
        for r in range(24, 28):
            prod = txt(ws_proy.cell(r, 5).value)
            und = int(round(num(ws_proy.cell(r, 6).value)))
            g_unt = num(ws_proy.cell(r, 7).value)
            g_tot = num(ws_proy.cell(r, 8).value)
            c_tot = num(ws_proy.cell(r, 9).value)
            ing_tot = num(ws_proy.cell(r, 10).value)
            c_unt = round(c_tot / und, 2) if und else 0.0
            b_vta = round(ing_tot / und, 2) if und else 0.0
            comprar_items.append({
                "producto": prod, "unidades": und, "costo_unit": c_unt, "costo_total": c_tot,
                "base_venta": b_vta, "ganancia_unit": g_unt, "ganancia_total": g_tot, "ingreso_total": ing_tot
            })
            ica, av, bom, tot_ica = split_ica(ing_tot)
            iva = round(ing_tot * 0.19, 2)
            ret_f = round(ing_tot * 0.025, 2)
            ventas_filas.append({
                "ref": "COMPRADA",
                "producto": f"{prod} (Mercancía Comprada)",
                "unidades": und,
                "costo_unit": c_unt,
                "costo_total": c_tot,
                "precio_venta": b_vta,
                "ventas_netas": ing_tot,
                "iva": iva,
                "retefuente": ret_f,
                "ica": ica,
                "avisos": av,
                "bomberil": bom,
                "reteica": tot_ica,
                "neto_cobrar": round(ing_tot + iva - ret_f - tot_ica, 2),
                "autoret": ret_f,
            })

        # Combine into inventario table (4 product lines)
        for init_it, comp_it in zip(inv_init_items, comprar_items):
            inv_filas.append({
                "ref": init_it["producto"][:3].upper(),
                "producto": init_it["producto"],
                "vender": init_it["unidades"] + comp_it["unidades"],
                "inv_inicial": init_it["unidades"],
                "stock_deseado": 0,
                "comprar": comp_it["unidades"],
                "costo_unit": comp_it["costo_unit"],
                "stock_final": 0,
                "val_inv_final": 0.0,
                "val_inv_inicial": init_it["costo_total"],
                "val_comprar": comp_it["costo_total"],
            })

        vta_bloques = {
            "inventario_inicial": {
                "titulo": "VENTAS INVENTARIO INICIAL (37 UNIDADES)",
                "base": num(ws_vta["H7"].value),
                "iva": num(ws_vta["H8"].value),
                "retefuente": num(ws_vta["H9"].value),
                "autoret": num(ws_vta["H10"].value),
                "reteica": num(ws_vta["H12"].value),
                "avisos": num(ws_vta["H13"].value),
                "bomberil": num(ws_vta["H14"].value),
                "total": num(ws_vta["H15"].value),
                "contado_50": num(ws_vta["C22"].value),
                "credito_50": num(ws_vta["D22"].value),
            },
            "mercancia_comprada": {
                "titulo": "VENTAS MERCANCÍA COMPRADA (22 UNIDADES)",
                "base": num(ws_vta["K7"].value),
                "iva": num(ws_vta["K8"].value),
                "retefuente": num(ws_vta["K9"].value),
                "autoret": num(ws_vta["K10"].value),
                "reteica": num(ws_vta["K12"].value),
                "avisos": num(ws_vta["K13"].value),
                "bomberil": num(ws_vta["K14"].value),
                "total": num(ws_vta["K15"].value),
                "contado_50": num(ws_vta["C23"].value),
                "credito_50": num(ws_vta["D23"].value),
            },
        }
        vta_contado = num(ws_vta["C24"].value)
        vta_credito = num(ws_vta["D24"].value)
        iva_gen = num(ws_vta["H18"].value)
        ret_renta_1355 = num(ws_vta["H19"].value)
        ret_ica_1355 = num(ws_vta["H20"].value)
        autoret_2465 = num(ws_vta["H21"].value)
        iva_neto_2408 = num(ws_vta["G24"].value)
    else:
        comprar_items = []
        for r in range(14, 18):
            prod = txt(ws_proy.cell(r, 5).value)
            und = int(round(num(ws_proy.cell(r, 6).value)))
            g_unt = num(ws_proy.cell(r, 7).value)
            g_tot = num(ws_proy.cell(r, 8).value)
            c_tot = num(ws_proy.cell(r, 9).value)
            ing_tot = num(ws_proy.cell(r, 10).value)
            c_unt = round(c_tot / und, 2) if und else 0.0
            b_vta = round(ing_tot / und, 2) if und else 0.0
            comprar_items.append({
                "producto": prod, "unidades": und, "costo_unit": c_unt, "costo_total": c_tot,
                "base_venta": b_vta, "ganancia_unit": g_unt, "ganancia_total": g_tot, "ingreso_total": ing_tot
            })
            ica, av, bom, tot_ica = split_ica(ing_tot)
            iva = round(ing_tot * 0.19, 2)
            ret_f = round(ing_tot * 0.025, 2)
            ventas_filas.append({
                "ref": "COMPRADA",
                "producto": prod,
                "unidades": und,
                "costo_unit": c_unt,
                "costo_total": c_tot,
                "precio_venta": b_vta,
                "ventas_netas": ing_tot,
                "iva": iva,
                "retefuente": ret_f,
                "ica": ica,
                "avisos": av,
                "bomberil": bom,
                "reteica": tot_ica,
                "neto_cobrar": round(ing_tot + iva - ret_f - tot_ica, 2),
                "autoret": ret_f,
            })
            inv_filas.append({
                "ref": prod[:3].upper(),
                "producto": prod,
                "vender": und,
                "inv_inicial": 0,
                "stock_deseado": 0,
                "comprar": und,
                "costo_unit": c_unt,
                "stock_final": 0,
                "val_inv_final": 0.0,
                "val_inv_inicial": 0.0,
                "val_comprar": c_tot,
            })

        vta_bloques = {
            "mercancia_comprada": {
                "titulo": "VENTAS MERCANCÍA COMPRADA (51 UNIDADES)",
                "base": num(ws_vta["H7"].value),
                "iva": num(ws_vta["H8"].value),
                "retefuente": num(ws_vta["H9"].value),
                "autoret": num(ws_vta["H10"].value),
                "reteica": num(ws_vta["H12"].value),
                "avisos": num(ws_vta["H13"].value),
                "bomberil": num(ws_vta["H14"].value),
                "total": num(ws_vta["H15"].value),
                "contado_50": num(ws_vta["C15"].value),
                "credito_50": num(ws_vta["D15"].value),
            }
        }
        vta_contado = num(ws_vta["C15"].value)
        vta_credito = num(ws_vta["D15"].value)
        iva_gen = num(ws_vta["H18"].value)
        ret_renta_1355 = num(ws_vta["H19"].value)
        ret_ica_1355 = num(ws_vta["H20"].value)
        autoret_2465 = num(ws_vta["H21"].value)
        iva_neto_2408 = num(ws_vta["G24"].value)

    ventas_tot = {
        "unidades": sum(x["unidades"] for x in ventas_filas),
        "costo_total": round(sum(x["costo_total"] for x in ventas_filas), 2),
        "ventas_netas": round(sum(x["ventas_netas"] for x in ventas_filas), 2),
        "iva": iva_gen,
        "retefuente": ret_renta_1355,
        "ica": round(sum(x["ica"] for x in ventas_filas), 2),
        "avisos": round(sum(x["avisos"] for x in ventas_filas), 2),
        "bomberil": round(sum(x["bomberil"] for x in ventas_filas), 2),
        "reteica": ret_ica_1355,
        "neto_cobrar": round(vta_contado + vta_credito, 2),
        "autoret": autoret_2465,
        "contado_50": vta_contado,
        "credito_50": vta_credito,
    }

    inv_totals = {
        "vender": sum(x["vender"] for x in inv_filas),
        "inv_inicial": sum(x["inv_inicial"] for x in inv_filas),
        "stock_deseado": 0,
        "comprar": sum(x["comprar"] for x in inv_filas),
        "stock_final": 0,
        "val_inv_final": 0.0,
        "val_inv_inicial": round(sum(x["val_inv_inicial"] for x in inv_filas), 2),
        "val_comprar": round(sum(x["val_comprar"] for x in inv_filas), 2),
    }

    comp_tot = ws_com_data["totales"]
    trib_filas = [
        {"concepto": "IVA Generado en Ventas (19%)", "puc": "240805", "valor": iva_gen, "nota": "Causado sobre ventas brutas del mes"},
        {"concepto": "IVA Descontable en Compras (19%)", "puc": "240810", "valor": comp_tot["iva_desc"], "nota": "Compras a responsables de IVA (Casa Orange + Cra 13)"},
        {"concepto": "IVA Neto Causado en el Mes (Generado − Descontable)", "puc": "2408", "valor": iva_neto_2408, "nota": "Pago bimestral F-300 DIAN en Julio (Bimestre May-Jun)"},
        {"concepto": "Retención en la Fuente Practicada en Compras (2,5%)", "puc": "246540", "valor": comp_tot["retefuente"], "nota": "Retenido a proveedores en compras del mes"},
        {"concepto": "Autorretención en Renta Comercial sobre Ventas (2,5%)", "puc": "246575", "valor": autoret_2465, "nota": "Autorretención de Electrovivienda S.A.S."},
        {"concepto": "TOTAL RETENCIÓN Y AUTORRETENCIÓN RENTA (F-350)", "puc": "2465", "valor": round(comp_tot["retefuente"] + autoret_2465, 2), "nota": "Pago mensual F-350 DIAN en el mes siguiente"},
        {"concepto": "ICA Retenido en Compras (9,6 × 1.000)", "puc": "246801", "valor": comp_tot["ica"], "nota": "Pago mensual Hacienda Bucaramanga (mes siguiente)"},
        {"concepto": "Avisos y Tableros Retenidos (15% sobre ICA)", "puc": "246802", "valor": comp_tot["avisos"], "nota": "Pago mensual Hacienda Bucaramanga (mes siguiente)"},
        {"concepto": "Sobretasa Bomberil Retenida (10% sobre ICA)", "puc": "246803", "valor": comp_tot["bomberil"], "nota": "Pago mensual Hacienda Bucaramanga (mes siguiente)"},
        {"concepto": "TOTAL RETEICA + AVISOS + BOMBERIL A PAGAR", "puc": "2468", "valor": comp_tot["reteica"], "nota": "Declaración y pago mensual Alcaldía de Bucaramanga"},
        {"concepto": "Anticipo Retefuente que nos Practicaron en Ventas (2,5%)", "puc": "135515", "valor": ret_renta_1355, "nota": "Aumenta saldo de cuenta 1355 Anticipo de Impuestos"},
        {"concepto": "Anticipo ReteICA + Avisos + Bomberil en Ventas (1,2%)", "puc": "135518", "valor": ret_ica_1355, "nota": "Aumenta saldo de cuenta 1355 Anticipo de Impuestos"},
    ]

    return {
        "proyectado": {
            "tasas_meta": tasas_meta,
            "gastos": gastos_tabla,
            "comprar_items": comprar_items,
        },
        "ventas_bloques": vta_bloques,
        "ventas": {"filas": ventas_filas, "totales": ventas_tot},
        "inventario": {"filas": inv_filas, "totales": inv_totals},
        "tributaria": trib_filas,
    }


def extract_maestro(ws):
    gastos_trim = []
    for r in range(4, 9):
        gastos_trim.append({
            "concepto": txt(ws.cell(r, 2).value),
            "mayo": num(ws.cell(r, 3).value),
            "junio": num(ws.cell(r, 4).value),
            "julio": num(ws.cell(r, 5).value),
            "total": num(ws.cell(r, 6).value),
        })

    flujo_comp = []
    for r in range(29, 43):
        flujo_comp.append({
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
        })

    return {
        "gastos_trimestre": gastos_trim,
        "flujo_caja_comparativo": flujo_comp,
    }


def main():
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)

    dep_data = extract_depreciacion(wb["DEP"])
    ta_data = extract_amortizacion(wb["TA"])
    nom_data = extract_nomina(wb["NOM"])
    esf_abril_data = extract_esf_sheet(wb["ESF ABRIL"])
    maestro_data = extract_maestro(wb["MAESTRO"])

    meses = {}
    for m in ("MAYO", "JUNIO", "JULIO"):
        proy_sname = " PROYECTADO MAYO" if m == "MAYO" else f"PROYECTADO {m}"
        proveedores, compras_dict = extract_com_sheet(wb[f"COM {m}"])
        vp = extract_vta_and_proy(wb[f"VTA {m}"], wb[proy_sname], compras_dict, m)
        meses[m] = {
            "proyectado": vp["proyectado"],
            "ventas_bloques": vp["ventas_bloques"],
            "compras_proveedores": proveedores,
            "ventas": vp["ventas"],
            "inventario": vp["inventario"],
            "compras": compras_dict,
            "tributaria": vp["tributaria"],
            "efc": extract_efc_sheet(wb[f"EFC PROYECTADO {m}"], m),
            "er": extract_er_sheet(wb[f"ER PROYECTADO {m}"]),
            "esf": extract_esf_sheet(wb[f"ESF PROYECTADO {m}"]),
        }

    # Build parameters & comparative dashboard summary from actual sheets
    ws_pm = wb[" PROYECTADO MAYO"]
    params_lista = [
        {"parametro": "Capital Suscrito y Pagado (Cuenta 3105)", "valor": num(ws_pm["C7"].value), "nota": "Base patrimonial para rentabilidad exigida por socios"},
        {"parametro": "Tasa Efectiva Anual Exigida (E/A)", "valor": num(ws_pm["C4"].value), "nota": "50,00% E.A. sobre el capital suscrito"},
        {"parametro": "Tasa Nominal Anual Equivalente", "valor": round(float(ws_pm["C5"].value or 0), 6), "nota": "Nominal mes vencido equivalente al 50% E.A."},
        {"parametro": "Tasa Mensual Equivalente", "valor": round(float(ws_pm["C6"].value or 0), 6), "nota": "3,4366% mensual → Meta de utilidad neta $8.543.408,27/mes"},
        {"parametro": "Política de Margen sobre Base de Venta", "valor": 0.30, "nota": "Base de Venta = Costo Unitario / (1 − 30%) • Stock Final = 0"},
        {"parametro": "Política de Recaudo de Ventas y Pago de Compras", "valor": 0.50, "nota": "50% de contado en el mismo mes y 50% a crédito a 30 días"},
        {"parametro": "Tarifa General de IVA", "valor": 0.19, "nota": "19% en ventas y compras a responsables de IVA (RRI)"},
        {"parametro": "Retención en la Fuente por Compras (246540 / 135515)", "valor": 0.025, "nota": "2,5% sobre compras y ventas antes de IVA"},
        {"parametro": "Autorretención en Renta Comercial (135515 / 246575)", "valor": 0.025, "nota": "2,5% autorretención comercial sobre ingresos brutos"},
        {"parametro": "ICA Bucaramanga — Tarifa Comercial (135518 / 246801)", "valor": 0.0096, "nota": "9,6 × 1.000 (0,96%) sobre base gravable — Pago mensual"},
        {"parametro": "Avisos y Tableros (135520 / 246802)", "valor": 0.15, "nota": "15% liquidado sobre el valor del ICA (0,144% sobre base) — Pago mensual"},
        {"parametro": "Sobretasa Bomberil (135525 / 246803)", "valor": 0.10, "nota": "10% liquidado sobre el valor del ICA (0,096% sobre base) — Pago mensual"},
        {"parametro": "Provisión Impuesto de Renta (2499) y Reserva Legal (3305)", "valor": 0.35, "nota": "35% Impuesto de Renta mensual en 2499 y 10% Reserva Legal sobre UDI"},
    ]

    neveras_prov = [
        {"proveedor": "Electrodomésticos Cra 13 (RRI — IVA 19%)", "precio": num(ws_pm["G6"].value), "porcentaje": 0.50},
        {"proveedor": "Electromenores (RNRI Declarante — Sin IVA)", "precio": num(ws_pm["G7"].value), "porcentaje": 0.50},
        {"proveedor": "Costo Promedio Ponderado Nevera Comprada (50/50)", "precio": num(ws_pm["G5"].value), "porcentaje": 1.00},
    ]

    catalogo_precios = [
        {"producto": "Televisores (Compras / Inv. Inicial)", "costo": num(ws_pm["G4"].value), "precio_venta": num(ws_pm["H4"].value), "ganancia_unit": num(ws_pm["I4"].value)},
        {"producto": "Neveras (Inventario Inicial Kardex Abril — 15 und)", "costo": num(ws_pm["G15"].value), "precio_venta": num(ws_pm["I15"].value), "ganancia_unit": num(ws_pm["J15"].value)},
        {"producto": "Neveras (Mercancía Comprada 50/50 Cra 13 y Electromenores)", "costo": num(ws_pm["G5"].value), "precio_venta": num(ws_pm["H5"].value), "ganancia_unit": num(ws_pm["I5"].value)},
        {"producto": "Microondas (Casa Orange RRI)", "costo": num(ws_pm["G8"].value), "precio_venta": num(ws_pm["H8"].value), "ganancia_unit": num(ws_pm["I8"].value)},
        {"producto": "Lavadoras (Casa Orange RRI)", "costo": num(ws_pm["G9"].value), "precio_venta": num(ws_pm["H9"].value), "ganancia_unit": num(ws_pm["I9"].value)},
    ]

    m_may, m_jun, m_jul = meses["MAYO"], meses["JUNIO"], meses["JULIO"]
    tablero_comparativo = [
        {"concepto": "Unidades Vendidas (Stock Final = 0)", "mayo": m_may["ventas"]["totales"]["unidades"], "junio": m_jun["ventas"]["totales"]["unidades"], "julio": m_jul["ventas"]["totales"]["unidades"], "trimestre": m_may["ventas"]["totales"]["unidades"] + m_jun["ventas"]["totales"]["unidades"] + m_jul["ventas"]["totales"]["unidades"]},
        {"concepto": "Unidades Compradas", "mayo": m_may["compras"]["totales"]["unidades"], "junio": m_jun["compras"]["totales"]["unidades"], "julio": m_jul["compras"]["totales"]["unidades"], "trimestre": m_may["compras"]["totales"]["unidades"] + m_jun["compras"]["totales"]["unidades"] + m_jul["compras"]["totales"]["unidades"]},
        {"concepto": "Ingresos Operacionales Netos (4135)", "mayo": m_may["er"]["ingresos_4135"], "junio": m_jun["er"]["ingresos_4135"], "julio": m_jul["er"]["ingresos_4135"], "trimestre": round(m_may["er"]["ingresos_4135"] + m_jun["er"]["ingresos_4135"] + m_jul["er"]["ingresos_4135"], 2)},
        {"concepto": "Costo de Ventas (6135)", "mayo": m_may["er"]["costos_6135"], "junio": m_jun["er"]["costos_6135"], "julio": m_jul["er"]["costos_6135"], "trimestre": round(m_may["er"]["costos_6135"] + m_jun["er"]["costos_6135"] + m_jul["er"]["costos_6135"], 2)},
        {"concepto": "Utilidad Bruta en Ventas (Margen 30%)", "mayo": m_may["er"]["utilidad_bruta"], "junio": m_jun["er"]["utilidad_bruta"], "julio": m_jul["er"]["utilidad_bruta"], "trimestre": round(m_may["er"]["utilidad_bruta"] + m_jun["er"]["utilidad_bruta"] + m_jul["er"]["utilidad_bruta"], 2)},
        {"concepto": "Total Gastos Operacionales y Financieros", "mayo": m_may["er"]["total_gastos"], "junio": m_jun["er"]["total_gastos"], "julio": m_jul["er"]["total_gastos"], "trimestre": round(m_may["er"]["total_gastos"] + m_jun["er"]["total_gastos"] + m_jul["er"]["total_gastos"], 2)},
        {"concepto": "Utilidad Antes de Impuestos (UAI)", "mayo": m_may["er"]["uai"], "junio": m_jun["er"]["uai"], "julio": m_jul["er"]["uai"], "trimestre": round(m_may["er"]["uai"] + m_jun["er"]["uai"] + m_jul["er"]["uai"], 2)},
        {"concepto": "Provisión Impuesto de Renta (35% — Cuenta 2499)", "mayo": m_may["er"]["impuesto_renta"], "junio": m_jun["er"]["impuesto_renta"], "julio": m_jul["er"]["impuesto_renta"], "trimestre": round(m_may["er"]["impuesto_renta"] + m_jun["er"]["impuesto_renta"] + m_jul["er"]["impuesto_renta"], 2)},
        {"concepto": "Reserva Legal Obligatoria (10% — Cuenta 3305)", "mayo": m_may["er"]["reserva_legal"], "junio": m_jun["er"]["reserva_legal"], "julio": m_jul["er"]["reserva_legal"], "trimestre": round(m_may["er"]["reserva_legal"] + m_jun["er"]["reserva_legal"] + m_jul["er"]["reserva_legal"], 2)},
        {"concepto": "Utilidad Neta del Ejercicio (Cuenta 3605)", "mayo": m_may["er"]["utilidad_neta"], "junio": m_jun["er"]["utilidad_neta"], "julio": m_jul["er"]["utilidad_neta"], "trimestre": round(m_may["er"]["utilidad_neta"] + m_jun["er"]["utilidad_neta"] + m_jul["er"]["utilidad_neta"], 2)},
        {"concepto": "Saldo Final Efectivo y Equivalentes (EFC)", "mayo": m_may["efc"]["saldo_final"], "junio": m_jun["efc"]["saldo_final"], "julio": m_jul["efc"]["saldo_final"], "trimestre": m_jul["efc"]["saldo_final"]},
        {"concepto": "Total Activos (ESF Proyectado)", "mayo": m_may["esf"]["total_activos"], "junio": m_jun["esf"]["total_activos"], "julio": m_jul["esf"]["total_activos"], "trimestre": m_jul["esf"]["total_activos"]},
        {"concepto": "Total Pasivos (ESF Proyectado)", "mayo": m_may["esf"]["total_pasivos"], "junio": m_jun["esf"]["total_pasivos"], "julio": m_jul["esf"]["total_pasivos"], "trimestre": m_jul["esf"]["total_pasivos"]},
        {"concepto": "Total Patrimonio (ESF Proyectado)", "mayo": m_may["esf"]["total_patrimonio"], "junio": m_jun["esf"]["total_patrimonio"], "julio": m_jul["esf"]["total_patrimonio"], "trimestre": m_jul["esf"]["total_patrimonio"]},
    ]

    data = {
        "meta": {
            "empresa": "ELECTROVIVIENDA S.A.S",
            "nit": "901.765.438-3",
            "regimen": "RRI - Agente Autorretenedor de Renta",
            "archivo": "PRESUPUESTO_MAYO_JUNIO_JULIO_2026.xlsx",
            "hojas_count": len(wb.sheetnames),
            "hojas": wb.sheetnames,
            "meta_utilidad_mensual": num(ws_pm["C8"].value),
            "saldo_inicial_caja_abril": num(wb["EFC PROYECTADO MAYO"]["E4"].value),
            "excel_mtime": datetime.datetime.fromtimestamp(os.path.getmtime(XLSX_PATH)).strftime("%Y-%m-%d %H:%M:%S"),
            "sincronizado_el": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        "parametros": {
            "reglas": params_lista,
            "proveedores_neveras": neveras_prov,
            "catalogo_precios": catalogo_precios,
            "tablero_comparativo": tablero_comparativo,
        },
        "depreciacion": dep_data,
        "amortizacion": ta_data,
        "nomina_abril": nom_data,
        "esf_abril": esf_abril_data,
        "maestro": maestro_data,
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Informe Financiero Oficial con los 5 Estados Financieros, Notas Completas y Análisis Fácil
ELECTROVIVIENDA S.A.S — Aprendiz: Kevin Guerrero • Instructor: George Olago (SENA CSET Bucaramanga)
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie

BASE_DIR = "/Users/ginavillamizar/Downloads/CONTABILIDAD"
OUTPUT_PDF = os.path.join(BASE_DIR, "INFORME_FINANCIERO_5_ESTADOS_ELECTROVIVIENDA_KEVIN_GUERRERO.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Omitir encabezado y pie en portada (página 1)
        if self._pageNumber > 1:
            # Encabezado superior
            self.setFillColor(colors.HexColor("#0B192C"))
            self.rect(40, letter[1] - 40, letter[0] - 80, 2, fill=1, stroke=0)
            
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(colors.HexColor("#0B192C"))
            self.drawString(40, letter[1] - 32, "ELECTROVIVIENDA S.A.S — NIT: 901.765.438-3 • INFORME FINANCIERO OFICIAL DE LOS 5 ESTADOS")
            
            self.setFont("Helvetica", 7)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(letter[0] - 40, letter[1] - 32, "NIIF PARA PYMES • CUATRIMESTRE ENERO - ABRIL 2026")
            
            # Pie de página inferior
            self.setFillColor(colors.HexColor("#CBD5E1"))
            self.rect(40, 42, letter[0] - 80, 0.75, fill=1, stroke=0)
            
            self.setFont("Helvetica", 7)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(40, 30, "Aprendiz: Kevin Guerrero • Instructor: George Olago • SENA CSET Bucaramanga — Ficha 123101")
            
            page_text = f"Página {self._pageNumber} de {page_count}"
            self.setFont("Helvetica-Bold", 7)
            self.setFillColor(colors.HexColor("#0B192C"))
            self.drawRightString(letter[0] - 40, 30, page_text)
            
        self.restoreState()

# Funciones generadoras de gráficos vectoriales
def create_chart_income_evolution():
    d = Drawing(504, 140)
    d.add(Rect(0, 0, 504, 155, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#CBD5E1"), strokeWidth=1, rx=6, ry=6))
    d.add(String(20, 137, "GRÁFICO 1: ¿CÓMO EVOLUCIONARON LAS VENTAS, COSTOS Y RESULTADOS DE LA EMPRESA?", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.HexColor("#0B192C")))
    
    chart = VerticalBarChart()
    chart.x = 45
    chart.y = 25
    chart.height = 98
    chart.width = 430
    chart.data = [
        [0, 61.3, 0, 8.16],
        [0, 41.64, 0, 3.29],
        [0, 16.45, -17.15, -7.89]
    ]
    chart.categoryAxis.categoryNames = ['Enero (Apertura)', 'Febrero (Ventas Pico)', 'Marzo (Costo Nómina)', 'Abril (Recuperación)']
    chart.categoryAxis.labels.fontSize = 7.5
    chart.categoryAxis.labels.fontName = 'Helvetica-Bold'
    chart.valueAxis.valueMin = -20
    chart.valueAxis.valueMax = 70
    chart.valueAxis.valueStep = 15
    chart.valueAxis.labels.fontSize = 7
    chart.valueAxis.labelTextFormat = '$%dM'
    
    chart.bars[0].fillColor = colors.HexColor("#10B981")  # Verde ventas
    chart.bars[1].fillColor = colors.HexColor("#D4AF37")  # Dorado costo
    chart.bars[2].fillColor = colors.HexColor("#0B192C")  # Azul marino resultado
    
    d.add(chart)
    
    d.add(Rect(130, 8, 10, 8, fillColor=colors.HexColor("#10B981"), strokeColor=None))
    d.add(String(145, 9, "Ventas Netas Realizadas", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#334155")))
    d.add(Rect(260, 8, 10, 8, fillColor=colors.HexColor("#D4AF37"), strokeColor=None))
    d.add(String(275, 9, "Costo de Comprar la Mercancía", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#334155")))
    d.add(Rect(390, 8, 10, 8, fillColor=colors.HexColor("#0B192C"), strokeColor=None))
    d.add(String(405, 9, "Ganancia o Pérdida Real", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#334155")))
    
    return d

def create_chart_asset_composition():
    d = Drawing(504, 138)
    d.add(Rect(0, 0, 504, 150, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#CBD5E1"), strokeWidth=1, rx=6, ry=6))
    d.add(String(20, 132, "GRÁFICO 2: ¿EN QUÉ TIENE LA PLATA LA EMPRESA? (ESTRUCTURA DE ACTIVOS ABRIL 2026)", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.HexColor("#0B192C")))
    
    pie = Pie()
    pie.x = 40
    pie.y = 18
    pie.width = 105
    pie.height = 105
    pie.data = [51.85, 28.86, 33.82, 209.89, 6.81]
    pie.labels = ['15.6%', '8.7%', '10.2%', '63.4%', '2.1%']
    pie.slices[0].fillColor = colors.HexColor("#10B981") # Efectivo
    pie.slices[1].fillColor = colors.HexColor("#3B82F6") # Cartera
    pie.slices[2].fillColor = colors.HexColor("#D4AF37") # Inventario
    pie.slices[3].fillColor = colors.HexColor("#0B192C") # Fijos
    pie.slices[4].fillColor = colors.HexColor("#94A3B8") # Otros
    d.add(pie)
    
    lines = [
        ("Dinero en Bancos y Caja:", "$ 51.852.812 (15,6%) — Plata disponible de inmediato para pagar cuentas.", colors.HexColor("#10B981")),
        ("Clientes por Cobrar (Cartera):", "$ 28.857.500 (8,7%) — Facturas pendientes por cobrar a clientes cumplidos.", colors.HexColor("#3B82F6")),
        ("Mercancía en Bodega:", "$ 33.822.000 (10,2%) — Neveras, Lavadoras, TVs y Estufas listas para vender.", colors.HexColor("#D4AF37")),
        ("Propiedades y Vehículos:", "$ 209.890.152 (63,4%) — Terrenos, local y camioneta propia de la empresa.", colors.HexColor("#0B192C")),
        ("Impuestos a Favor (Anticipos):", "$ 6.810.220 (2,1%) — Retenciones a favor descontables con la DIAN.", colors.HexColor("#94A3B8"))
    ]
    y_pos = 104
    for title, desc, col in lines:
        d.add(Rect(185, y_pos + 1, 8, 8, fillColor=col, strokeColor=None))
        d.add(String(198, y_pos + 1, title, fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor("#0B192C")))
        d.add(String(312, y_pos + 1, desc, fontName="Helvetica", fontSize=6.8, fillColor=colors.HexColor("#475569")))
        y_pos -= 21
        
    return d

def create_chart_liquidity_solvency():
    d = Drawing(504, 125)
    d.add(Rect(0, 0, 504, 145, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#CBD5E1"), strokeWidth=1, rx=6, ry=6))
    d.add(String(20, 127, "GRÁFICO 3: CAPACIDAD DE PAGO EN PALABRAS FÁCILES (RESPALDO POR CADA $1 DE DEUDA)", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.HexColor("#0B192C")))
    
    chart = VerticalBarChart()
    chart.x = 45
    chart.y = 22
    chart.height = 90
    chart.width = 430
    chart.data = [
        [3.0, 2.15, 1.92, 2.25],
        [3.0, 1.79, 1.56, 1.62]
    ]
    chart.categoryAxis.categoryNames = ['Enero (Libre Deuda)', 'Febrero', 'Marzo', 'Abril (Saneada)']
    chart.categoryAxis.labels.fontSize = 7.5
    chart.categoryAxis.labels.fontName = 'Helvetica-Bold'
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 3.5
    chart.valueAxis.valueStep = 0.5
    chart.valueAxis.labels.fontSize = 7
    chart.valueAxis.labelTextFormat = '$%.2f'
    
    chart.bars[0].fillColor = colors.HexColor("#0B192C")
    chart.bars[1].fillColor = colors.HexColor("#10B981")
    d.add(chart)
    
    d.add(Rect(120, 6, 10, 8, fillColor=colors.HexColor("#0B192C"), strokeColor=None))
    d.add(String(135, 7, "Total de bienes líquidos por cada $1 de deuda (Meta: > $1,50)", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#334155")))
    d.add(Rect(325, 6, 10, 8, fillColor=colors.HexColor("#10B981"), strokeColor=None))
    d.add(String(340, 7, "Plata inmediata sin vender mercancía (Meta: > $1,00)", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#334155")))
    
    return d

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=46
    )
    
    styles = getSampleStyleSheet()
    
    c_primary = colors.HexColor("#0B192C")
    c_gold = colors.HexColor("#D4AF37")
    c_green = colors.HexColor("#065F46")
    c_slate = colors.HexColor("#334155")
    c_muted = colors.HexColor("#64748B")
    
    # Estilos de texto
    title_style = ParagraphStyle('TitleStyle', fontName='Helvetica-Bold', fontSize=17, leading=21, textColor=c_primary, alignment=1)
    sub_title_style = ParagraphStyle('SubTitleStyle', fontName='Helvetica-Bold', fontSize=10, leading=13.5, textColor=c_gold, alignment=1)
    meta_style = ParagraphStyle('MetaStyle', fontName='Helvetica', fontSize=8, leading=11.5, textColor=c_muted, alignment=1)
    
    sec_header_style = ParagraphStyle('SecHeader', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=c_primary, spaceBefore=4, spaceAfter=2, keepWithNext=True)
    subsec_header_style = ParagraphStyle('SubSecHeader', fontName='Helvetica-Bold', fontSize=8.8, leading=11.5, textColor=c_gold, spaceBefore=4, spaceAfter=2, keepWithNext=True)
    body_style = ParagraphStyle('BodyText', fontName='Helvetica', fontSize=7.6, leading=10.8, textColor=c_slate, spaceAfter=4)
    body_bold = ParagraphStyle('BodyTextBold', fontName='Helvetica-Bold', fontSize=7.6, leading=10.8, textColor=c_primary)
    
    th_style = ParagraphStyle('THStyle', fontName='Helvetica-Bold', fontSize=7.2, leading=9.2, textColor=colors.white, alignment=0)
    th_r_style = ParagraphStyle('THRStyle', fontName='Helvetica-Bold', fontSize=7.2, leading=9.2, textColor=colors.white, alignment=2)
    td_style = ParagraphStyle('TDStyle', fontName='Helvetica', fontSize=6.8, leading=8.8, textColor=c_slate)
    td_bold = ParagraphStyle('TDBold', fontName='Helvetica-Bold', fontSize=6.8, leading=8.8, textColor=c_primary)
    td_r_style = ParagraphStyle('TDRStyle', fontName='Helvetica', fontSize=6.8, leading=8.8, textColor=c_slate, alignment=2)
    td_r_bold = ParagraphStyle('TDRBold', fontName='Helvetica-Bold', fontSize=6.8, leading=8.8, textColor=c_primary, alignment=2)
    td_r_green = ParagraphStyle('TDRGreen', fontName='Helvetica-Bold', fontSize=6.8, leading=8.8, textColor=colors.HexColor("#047857"), alignment=2)
    td_r_red = ParagraphStyle('TDRRed', fontName='Helvetica-Bold', fontSize=6.8, leading=8.8, textColor=colors.HexColor("#DC2626"), alignment=2)

    story = []

    # =========================================================================
    # PÁGINA 1: PORTADA INSTITUCIONAL, PRESENTACIÓN, MISIÓN Y VISIÓN
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("SERVICIO NACIONAL DE APRENDIZAJE — SENA", ParagraphStyle('CoverSENA', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=c_gold, alignment=1)))
    story.append(Paragraph("CENTRO DE SERVICIOS EMPRESARIALES Y TURÍSTICOS (CSET) — REGIONAL SANTANDER", ParagraphStyle('CoverSubSENA', fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=c_primary, alignment=1)))
    story.append(Paragraph("Tecnología en Gestión Contable y de Información Financiera • Ficha 123101", meta_style))
    story.append(Spacer(1, 14))
    
    story.append(Paragraph("INFORME FINANCIERO OFICIAL DE LOS 5 ESTADOS FINANCIEROS Y COMPARATIVO", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("APLICACIÓN DEL MARCO NIIF PARA LAS PYMES (GRUPO 2) • CUATRIMESTRE 2026", sub_title_style))
    story.append(Paragraph("Enero (Apertura) • Febrero (Operación Comercial) • Marzo (Causación y Nómina) • Abril (Consolidación y Cierre)", meta_style))
    story.append(Spacer(1, 12))
    
    auth_data = [
        [Paragraph("<b>ENTIDAD REPORTANTE:</b>", td_bold), Paragraph("ELECTROVIVIENDA S.A.S — NIT: 901.765.438-3 • Bucaramanga, Santander", td_style)],
        [Paragraph("<b>RÉGIMEN Y MARCO:</b>", td_bold), Paragraph("Responsable de IVA (RRI) • Agente Retenedor y Autorretenedor • NIIF PYMES Grupo 2", td_style)],
        [Paragraph("<b>APRENDIZ / ELABORÓ:</b>", td_bold), Paragraph("<b>Kevin Guerrero</b> — Aprendiz en Gestión Contable y de Información Financiera", td_style)],
        [Paragraph("<b>INSTRUCTOR / REVISÓ:</b>", td_bold), Paragraph("<b>George Olago</b> — Instructor Líder de Contabilidad y Finanzas SENA CSET", td_style)],
        [Paragraph("<b>FECHA DE PRESENTACIÓN:</b>", td_bold), Paragraph("12 de Noviembre de 2026 — Período Contable Evaluado: Enero a Abril 2026", td_style)],
    ]
    t_auth = Table(auth_data, colWidths=[150, 354])
    t_auth.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1.5, c_gold),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_auth)
    story.append(Spacer(1, 14))

    story.append(Paragraph("1. PRESENTACIÓN INSTITUCIONAL DE LA EMPRESA", sec_header_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=6, spaceBefore=0))
    p_pres = (
        "<b>ELECTROVIVIENDA S.A.S</b> es una sociedad comercial legalmente constituida por acciones simplificadas, con domicilio en la ciudad "
        "de Bucaramanga, Santander. Su actividad principal consiste en la comercialización, distribución y venta al por mayor y detal de "
        "electrodomésticos para el hogar, gasodomésticos y tecnología (Neveras No Frost, Lavadoras Automáticas, Smart TVs 4K y Estufas a Gas). "
        "Pertenece al Régimen Responsable de IVA (RRI), actúa como agente de retención en la fuente y prepara su información bajo las "
        "<b>Normas Internacionales de Información Financiera para Pequeñas y Medianas Entidades (NIIF para las PYMES - Grupo 2)</b>."
    )
    story.append(Paragraph(p_pres, body_style))
    story.append(Spacer(1, 6))

    mv_data = [
        [
            Paragraph("<b>🎯 MISIÓN CORPORATIVA</b>", ParagraphStyle('MTitle', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=c_primary)),
            Paragraph("<b>🔭 VISIÓN ESTRATÉGICA (2026-2030)</b>", ParagraphStyle('VTitle', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=c_gold))
        ],
        [
            Paragraph(
                "Facilitar el acceso de las familias y microempresas santandereanas a electrodomésticos y tecnología de vanguardia con alta eficiencia "
                "energética y respaldo de fábrica; ofreciendo asesoría transparente, opciones de pago justas, riguroso cumplimiento tributario y "
                "garantía posventa, generando valor económico y bienestar sostenible para nuestros clientes, colaboradores y la sociedad.",
                body_style
            ),
            Paragraph(
                "Posicionarnos en el año 2030 como la comercializadora de electrodomésticos preferida del nororiente colombiano por su servicio "
                "cercano, solidez patrimonial, confiabilidad en su información financiera NIIF y adopción de canales digitales eficientes, "
                "manteniendo siempre una gestión honesta, rentable y respetuosa de la ley.",
                body_style
            )
        ]
    ]
    t_mv = Table(mv_data, colWidths=[250, 254])
    t_mv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#FEF3C7")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FFFFFF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_mv)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. VALORES CORPORATIVOS Y CUMPLIMIENTO ÉTICO", subsec_header_style))
    p_val = (
        "• <b>Honestidad y Claridad Contable:</b> Registro fidedigno de cada factura, comprobante y cuenta sin ocultamientos ni alteraciones.<br/>"
        "• <b>Cumplimiento Laboral y Fiscal:</b> Pago puntual de salarios, seguridad social (salud, pensión, ARL) e impuestos ante la DIAN.<br/>"
        "• <b>Solvencia y Prudencia:</b> Cuidado permanente de la caja y del patrimonio para asegurar la continuidad del negocio."
    )
    story.append(Paragraph(p_val, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: ESTADOS FINANCIEROS OFICIALES — MES DE ENERO 2026 (4 ESTADOS)
    # =========================================================================
    story.append(Paragraph("ESTADOS FINANCIEROS OFICIALES — MES DE ENERO 2026", sec_header_style))
    story.append(Paragraph("Período de Apertura y Constitución Social (01 al 31 de Enero de 2026) • Cifras en Pesos Colombianos (COP)", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=6, spaceBefore=2))

    story.append(Paragraph("ESTADO DE SITUACIÓN FINANCIERA — ESF ENERO 2026", subsec_header_style))
    esf_ene = [
        [Paragraph("<b>CONCEPTO / RUBRO CONTABLE</b>", th_style), Paragraph("<b>NOTAS</b>", th_style), Paragraph("<b>ENERO 2026 (COP)</b>", th_r_style), Paragraph("<b>PARTICIPACIÓN (%)</b>", th_r_style)],
        [Paragraph("<b>ACTIVO CORRIENTE</b>", td_bold), Paragraph("Nota 3", td_style), Paragraph("<b>$ 36.000.000</b>", td_r_bold), Paragraph("14,56 %", td_r_style)],
        [Paragraph("  Efectivo y Equivalentes de Efectivo (Caja General)", td_style), Paragraph("3.1", td_style), Paragraph("$ 36.000.000", td_r_style), Paragraph("14,56 %", td_r_style)],
        [Paragraph("  Deudores Comerciales (Clientes por Cobrar)", td_style), Paragraph("3.2", td_style), Paragraph("$ 0", td_r_style), Paragraph("0,00 %", td_r_style)],
        [Paragraph("  Inventarios de Mercancías", td_style), Paragraph("3.3", td_style), Paragraph("$ 0", td_r_style), Paragraph("0,00 %", td_r_style)],
        [Paragraph("<b>ACTIVO NO CORRIENTE</b>", td_bold), Paragraph("Nota 4", td_style), Paragraph("<b>$ 211.328.750</b>", td_r_bold), Paragraph("85,44 %", td_r_style)],
        [Paragraph("  Propiedades, Planta y Equipo (Terrenos, Edificios, Vehículo)", td_style), Paragraph("4.1", td_style), Paragraph("$ 212.600.000", td_r_style), Paragraph("85,96 %", td_r_style)],
        [Paragraph("  Menos: Depreciación Acumulada Mes 1", td_style), Paragraph("4.2", td_style), Paragraph("-$ 1.271.250", td_r_style), Paragraph("-0,51 %", td_r_style)],
        [Paragraph("<b>TOTAL ACTIVO</b>", td_bold), Paragraph("", td_style), Paragraph("<b>$ 247.328.750</b>", td_r_bold), Paragraph("<b>100,00 %</b>", td_r_bold)],
        [Paragraph("<b>PASIVO CORRIENTE Y TOTAL PASIVO</b>", td_bold), Paragraph("Nota 5", td_style), Paragraph("<b>$ 0</b>", td_r_bold), Paragraph("<b>0,00 %</b>", td_r_bold)],
        [Paragraph("  (La empresa inició 100% libre de deudas financieras y comerciales)", td_style), Paragraph("", td_style), Paragraph("$ 0", td_r_style), Paragraph("0,00 %", td_r_style)],
        [Paragraph("<b>PATRIMONIO NETO</b>", td_bold), Paragraph("Nota 6", td_style), Paragraph("<b>$ 247.328.750</b>", td_r_bold), Paragraph("<b>100,00 %</b>", td_r_bold)],
        [Paragraph("  Capital Social Suscrito y Pagado (Aportes Fundadores)", td_style), Paragraph("6.1", td_style), Paragraph("$ 248.600.000", td_r_style), Paragraph("100,51 %", td_r_style)],
        [Paragraph("  Resultado del Ejercicio (Gasto de Depreciación Enero)", td_style), Paragraph("6.2", td_style), Paragraph("-$ 1.271.250", td_r_style), Paragraph("-0,51 %", td_r_style)],
        [Paragraph("<b>TOTAL PASIVO Y PATRIMONIO</b>", td_bold), Paragraph("", td_style), Paragraph("<b>$ 247.328.750</b>", td_r_bold), Paragraph("<b>100,00 %</b>", td_r_bold)],
    ]
    t_esf_ene = Table(esf_ene, colWidths=[244, 40, 115, 105])
    t_esf_ene.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,8), (-1,8), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,14), (-1,14), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_esf_ene)
    story.append(Spacer(1, 4))

    story.append(Paragraph("ESTADO DE RESULTADO INTEGRAL — ER ENERO 2026", subsec_header_style))
    er_ene = [
        [Paragraph("<b>RENGLÓN DEL ESTADO DE RESULTADOS</b>", th_style), Paragraph("<b>ENERO 2026 (COP)</b>", th_r_style), Paragraph("<b>ANÁLISIS VERTICAL (%)</b>", th_r_style)],
        [Paragraph("Ingresos de Actividades Ordinarias (Ventas Netas)", td_style), Paragraph("$ 0", td_r_style), Paragraph("0,00 %", td_r_style)],
        [Paragraph("Menos: Costo de Ventas (Comercio)", td_style), Paragraph("$ 0", td_r_style), Paragraph("0,00 %", td_r_style)],
        [Paragraph("<b>UTILIDAD BRUTA EN VENTAS</b>", td_bold), Paragraph("<b>$ 0</b>", td_r_bold), Paragraph("0,00 %", td_r_style)],
        [Paragraph("Menos: Gastos de Administración y Ventas", td_style), Paragraph("$ 0", td_r_style), Paragraph("0,00 %", td_r_style)],
        [Paragraph("Menos: Gasto por Depreciación de Activos Fijos (Línea Recta)", td_style), Paragraph("-$ 1.271.250", td_r_style), Paragraph("100,00 %", td_r_style)],
        [Paragraph("<b>RESULTADO INTEGRAL DEL PERÍODO (PÉRDIDA CONTABLE)</b>", td_bold), Paragraph("<font color='#DC2626'><b>-$ 1.271.250</b></font>", td_r_bold), Paragraph("<b>-100,00 %</b>", td_r_bold)],
    ]
    t_er_ene = Table(er_ene, colWidths=[289, 115, 100])
    t_er_ene.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#FEE2E2")),
    ]))
    story.append(t_er_ene)
    story.append(Spacer(1, 4))

    story.append(Paragraph("ESTADO DE CAMBIOS EN EL PATRIMONIO — ECP ENERO 2026", subsec_header_style))
    ecp_ene = [
        [Paragraph("<b>RUBRO PATRIMONIAL</b>", th_style), Paragraph("<b>SALDO INICIAL</b>", th_r_style), Paragraph("<b>APORTES / MOVIMIENTOS</b>", th_r_style), Paragraph("<b>SALDO AL 31 ENERO</b>", th_r_style)],
        [Paragraph("Capital Suscrito y Pagado (3105)", td_style), Paragraph("$ 0", td_r_style), Paragraph("+$ 248.600.000", td_r_style), Paragraph("$ 248.600.000", td_r_bold)],
        [Paragraph("Reservas Obligatorias (3305)", td_style), Paragraph("$ 0", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("$ 0", td_r_style)],
        [Paragraph("Resultado del Ejercicio (3605)", td_style), Paragraph("$ 0", td_r_style), Paragraph("-$ 1.271.250", td_r_style), Paragraph("-$ 1.271.250", td_r_style)],
        [Paragraph("<b>TOTAL PATRIMONIO NETO</b>", td_bold), Paragraph("<b>$ 0</b>", td_r_bold), Paragraph("<b>+$ 247.328.750</b>", td_r_bold), Paragraph("<b>$ 247.328.750</b>", td_r_bold)],
    ]
    t_ecp_ene = Table(ecp_ene, colWidths=[204, 100, 100, 100])
    t_ecp_ene.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ecp_ene)
    story.append(Spacer(1, 4))

    story.append(Paragraph("ESTADO DE FLUJOS DE EFECTIVO — EFE ENERO 2026 (MÉTODO INDIRECTO)", subsec_header_style))
    efe_ene = [
        [Paragraph("<b>ACTIVIDAD DE FLUJO DE EFECTIVO</b>", th_style), Paragraph("<b>VALOR (COP)</b>", th_r_style)],
        [Paragraph("<b>Flujo de Efectivo de Actividades de Operación</b>", td_bold), Paragraph("$ 0", td_r_style)],
        [Paragraph("  Resultado Neto del Período", td_style), Paragraph("-$ 1.271.250", td_r_style)],
        [Paragraph("  Ajustes por partidas que no afectan efectivo: Depreciación del mes", td_style), Paragraph("+$ 1.271.250", td_r_style)],
        [Paragraph("  <b>Flujo Neto procedente de Actividades de Operación</b>", td_bold), Paragraph("<b>$ 0</b>", td_r_bold)],
        [Paragraph("<b>Flujo de Efectivo de Actividades de Inversión</b>", td_bold), Paragraph("<b>$ 0</b>", td_r_style)],
        [Paragraph("<b>Flujo de Efectivo de Actividades de Financiación</b>", td_bold), Paragraph("$ 36.000.000", td_r_style)],
        [Paragraph("  Aportes de socios fundadores recibidos en efectivo en caja general", td_style), Paragraph("+$ 36.000.000", td_r_style)],
        [Paragraph("  <b>Flujo Neto procedente de Actividades de Financiación</b>", td_bold), Paragraph("<b>$ 36.000.000</b>", td_r_bold)],
        [Paragraph("<b>INCREMENTO NETO EN EFECTIVO Y EQUIVALENTES DE EFECTIVO</b>", td_bold), Paragraph("<b>+$ 36.000.000</b>", td_r_green)],
        [Paragraph("Saldo Inicial de Efectivo (01 de enero 2026)", td_style), Paragraph("$ 0", td_r_style)],
        [Paragraph("<b>SALDO FINAL DE EFECTIVO AL 31 DE ENERO DE 2026</b>", td_bold), Paragraph("<b>$ 36.000.000</b>", td_r_green)],
    ]
    t_efe_ene = Table(efe_ene, colWidths=[384, 120])
    t_efe_ene.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,11), (-1,11), colors.HexColor("#DCFCE7")),
    ]))
    story.append(t_efe_ene)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: ESTADO DE NOTAS Y REVELACIONES COMPLETAS — MES DE ENERO 2026
    # =========================================================================
    story.append(Paragraph("ESTADO DE NOTAS Y REVELACIONES A LOS ESTADOS FINANCIEROS — NOTAS ENERO 2026", sec_header_style))
    story.append(Paragraph("Revelación Completa y Exhaustiva conforme a NIIF para las PYMES (Secciones 3, 4, 8, 10, 17)", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=8, spaceBefore=2))

    notas_ene_completas = (
        "<b>NOTA 1. IDENTIFICACIÓN Y CONSTITUCIÓN DE LA SOCIEDAD:</b><br/>"
        "ELECTROVIVIENDA S.A.S es una sociedad por acciones simplificada constituida el 1 de enero de 2026 mediante documento privado "
        "debidamente inscrito en el Registro Mercantil de la Cámara de Comercio de Bucaramanga. Su objeto social comprende la compra, venta, "
        "distribución, consignación e importación de electrodomésticos y gasodomésticos para el hogar. Su domicilio y sede operativa principal "
        "se ubica en la Carrera 21 N° 46-11, Barrio La Concordia de Bucaramanga. La sociedad se rige por la Ley 1258 de 2008 y el Código de Comercio.<br/><br/>"

        "<b>NOTA 2. BASE DE PREPARACIÓN Y POLÍTICAS CONTABLES SIGNIFICATIVAS (NIIF PYMES):</b><br/>"
        "Los presentes estados financieros han sido preparados bajo la hipótesis de negocio en marcha y de conformidad con las Normas Internacionales "
        "de Información Financiera para Pequeñas y Medianas Entidades (Decreto Único Reglamentario 2420 de 2015, Grupo 2). La moneda funcional y de "
        "presentación es el Peso Colombiano (COP). Los criterios de reconocimiento aplicados son:<br/>"
        "• <i>Base de Acumulación o Devengo:</i> Las transacciones y hechos económicos se reconocen cuando ocurren y no cuando se cobra o paga el efectivo.<br/>"
        "• <i>Efectivo y Equivalentes:</i> Se reconocen al costo de transacción y comprenden dinero en efectivo en caja general de disponibilidad inmediata.<br/>"
        "• <i>Propiedades, Planta y Equipo:</i> Medidos al costo de adquisición o valor razonable inicial del aporte social, menos depreciación acumulada.<br/>"
        "• <i>Método de Depreciación:</i> Se utiliza el método de línea recta sobre vidas útiles estimadas: Edificaciones (20 años / 240 meses), "
        "Flota y Equipo de Transporte (10 años / 120 meses). Los terrenos no se deprecian por tener vida útil indefinida.<br/><br/>"

        "<b>NOTA 3. EFECTIVO Y EQUIVALENTES DE EFECTIVO (DESGLOSE COMPLETO):</b><br/>"
        "Al 31 de enero de 2026, el saldo de efectivo asciende a <b>$36.000.000</b> custodiado en Caja General (Código PUC 110505), correspondiente a:<br/>"
        "• Aporte inicial en dinero en efectivo entregado por el Socio 1 (Carlos Eduardo Daza Gómez): <b>$21.000.000</b>.<br/>"
        "• Aporte inicial en dinero en efectivo entregado por el Socio 2 (Marco Aurelio Pedraza Díaz): <b>$15.000.000</b>.<br/>"
        "Dichos fondos se encuentran disponibles sin restricciones para la apertura de cuentas corrientes bancarias y gastos preoperativos.<br/><br/>"

        "<b>NOTA 4. PROPIEDADES, PLANTA Y EQUIPO (DESGLOSE Y TABLA DE DEPRECIACIÓN):</b><br/>"
        "Los activos fijos fueron transferidos formalmente a la sociedad en escritura de constitución por valor de <b>$212.600.000</b>:<br/>"
        "• <i>Terrenos Urbanos (150405):</i> Terreno Calle 45 N° 12-50 ($38.600.000) y Terreno Calle 85 N° 15-80 ($51.000.000). Total: <b>$89.600.000</b> (No deprecian).<br/>"
        "• <i>Construcciones y Edificaciones (151605):</i> Local comercial Calle 85 N° 15-80 ($51.000.000). Depreciación mensual (20 años): <b>$212.500</b>.<br/>"
        "• <i>Flota y Equipo de Transporte (154005):</i> Camioneta Chevrolet D-Max mod. 2024 ($72.000.000). Depreciación mensual (10 años): <b>$600.000</b>.<br/>"
        "• <i>Depreciación Acumulada Enero:</i> Total contabilizado al cierre del mes de enero: <b>-$1.271.250</b> (incluye depreciación y amortización de apertura). "
        "El valor neto en libros al 31 de enero se sitúa en <b>$211.328.750</b>.<br/><br/>"

        "<b>NOTA 5. PASIVOS Y OBLIGACIONES FINANCIERAS:</b><br/>"
        "Al cierre del mes de enero de 2026, ELECTROVIVIENDA S.A.S no registra pasivos corrientes ni pasivos no corrientes (<b>$0</b>). "
        "La empresa inició sus actividades 100% financiada con recursos propios de los socios, sin contraer deudas con bancos ni proveedores.<br/><br/>"

        "<b>NOTA 6. CAPITAL SOCIAL Y PATRIMONIO:</b><br/>"
        "El capital suscrito y pagado por los accionistas fundadores se encuentra dividido y aportado en un 100% como sigue:<br/>"
        "• Socio 1: Carlos Eduardo Daza Gómez — C.C. 83.540.120 — Aporte total: <b>$123.000.000</b> (49,48%).<br/>"
        "• Socio 2: Marco Aurelio Pedraza Díaz — C.C. 83.630.214 — Aporte total: <b>$125.600.000</b> (50,52%).<br/>"
        "Total Capital Social: <b>$248.600.000</b>. Menos el resultado del ejercicio de apertura (-$1.271.250), el patrimonio neto asciende a <b>$247.328.750</b>."
    )
    story.append(Paragraph(notas_ene_completas, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: ESTADOS FINANCIEROS OFICIALES — MES DE FEBRERO 2026 (4 ESTADOS)
    # =========================================================================
    story.append(Paragraph("ESTADOS FINANCIEROS OFICIALES — MES DE FEBRERO 2026", sec_header_style))
    story.append(Paragraph("Inicio de Comercialización y Crédito Financiero • Comparativo Enero vs Febrero 2026", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=6, spaceBefore=2))

    story.append(Paragraph("ESTADO DE SITUACIÓN FINANCIERA COMPARATIVO — ESF ENERO VS FEBRERO 2026", subsec_header_style))
    esf_feb = [
        [Paragraph("<b>RUBRO CONTABLE (COP)</b>", th_style), Paragraph("<b>ENERO 2026</b>", th_r_style), Paragraph("<b>FEBRERO 2026</b>", th_r_style), Paragraph("<b>VAR. ABS ($)</b>", th_r_style), Paragraph("<b>VAR. REL (%)</b>", th_r_style)],
        [Paragraph("<b>Activo Corriente</b>", td_bold), Paragraph("$ 36.000.000", td_r_style), Paragraph("<b>$ 173.457.213</b>", td_r_bold), Paragraph("+$ 137.457.213", td_r_green), Paragraph("+381,8 %", td_r_green)],
        [Paragraph("  Efectivo y Equivalentes", td_style), Paragraph("$ 36.000.000", td_r_style), Paragraph("$ 107.083.528", td_r_style), Paragraph("+$ 71.083.528", td_r_green), Paragraph("+197,5 %", td_r_green)],
        [Paragraph("  Deudores Comerciales (Clientes)", td_style), Paragraph("$ 0", td_r_style), Paragraph("$ 28.857.500", td_r_style), Paragraph("+$ 28.857.500", td_r_green), Paragraph("N/A", td_r_style)],
        [Paragraph("  Inventarios (Bodega)", td_style), Paragraph("$ 0", td_r_style), Paragraph("$ 29.160.000", td_r_style), Paragraph("+$ 29.160.000", td_r_green), Paragraph("N/A", td_r_style)],
        [Paragraph("  Anticipos de Impuestos", td_style), Paragraph("$ 0", td_r_style), Paragraph("$ 8.356.185", td_r_style), Paragraph("+$ 8.356.185", td_r_green), Paragraph("N/A", td_r_style)],
        [Paragraph("<b>Activo No Corriente (PP&E)</b>", td_bold), Paragraph("$ 211.328.750", td_r_style), Paragraph("<b>$ 212.449.217</b>", td_r_bold), Paragraph("+$ 1.120.467", td_r_style), Paragraph("+0,5 %", td_r_style)],
        [Paragraph("<b>TOTAL ACTIVO</b>", td_bold), Paragraph("<b>$ 247.328.750</b>", td_r_bold), Paragraph("<b>$ 385.906.430</b>", td_r_bold), Paragraph("<b>+$ 138.577.680</b>", td_r_green), Paragraph("<b>+56,0 %</b>", td_r_green)],
        [Paragraph("<b>Pasivo Corriente (&lt;12 meses)</b>", td_bold), Paragraph("$ 0", td_r_style), Paragraph("$ 80.641.618", td_r_style), Paragraph("+$ 80.641.618", td_r_style), Paragraph("N/A", td_r_style)],
        [Paragraph("<b>Pasivo No Corriente (Crédito LP)</b>", td_bold), Paragraph("$ 0", td_r_style), Paragraph("$ 39.662.637", td_r_style), Paragraph("+$ 39.662.637", td_r_style), Paragraph("N/A", td_r_style)],
        [Paragraph("<b>TOTAL PASIVO</b>", td_bold), Paragraph("<b>$ 0</b>", td_r_bold), Paragraph("<b>$ 120.304.255</b>", td_r_bold), Paragraph("<b>+$ 120.304.255</b>", td_r_red), Paragraph("<b>N/A</b>", td_r_style)],
        [Paragraph("<b>PATRIMONIO NETO</b>", td_bold), Paragraph("<b>$ 247.328.750</b>", td_r_bold), Paragraph("<b>$ 265.602.175</b>", td_r_bold), Paragraph("<b>+$ 18.273.425</b>", td_r_green), Paragraph("<b>+7,4 %</b>", td_r_green)],
        [Paragraph("  Capital Social (3105)", td_style), Paragraph("$ 248.600.000", td_r_style), Paragraph("$ 248.600.000", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("0,0 %", td_r_style)],
        [Paragraph("  Reserva Legal Obligatoria", td_style), Paragraph("$ 0", td_r_style), Paragraph("$ 1.827.342", td_r_style), Paragraph("+$ 1.827.342", td_r_green), Paragraph("N/A", td_r_style)],
        [Paragraph("  Resultados Acumulados y Ejercicio", td_style), Paragraph("-$ 1.271.250", td_r_style), Paragraph("+$ 15.174.832", td_r_style), Paragraph("+$ 16.446.082", td_r_green), Paragraph("+1293,7 %", td_r_green)],
        [Paragraph("<b>TOTAL PASIVO Y PATRIMONIO</b>", td_bold), Paragraph("<b>$ 247.328.750</b>", td_r_bold), Paragraph("<b>$ 385.906.430</b>", td_r_bold), Paragraph("<b>+$ 138.577.680</b>", td_r_green), Paragraph("<b>+56,0 %</b>", td_r_green)],
    ]
    t_esf_feb = Table(esf_feb, colWidths=[184, 80, 80, 80, 80])
    t_esf_feb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,15), (-1,15), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_esf_feb)
    story.append(Spacer(1, 4))

    story.append(Paragraph("ESTADO DE RESULTADO INTEGRAL COMPARATIVO — ER ENERO VS FEBRERO 2026", subsec_header_style))
    er_feb = [
        [Paragraph("<b>CONCEPTO / RENGLÓN</b>", th_style), Paragraph("<b>ENERO</b>", th_r_style), Paragraph("<b>FEBRERO</b>", th_r_style), Paragraph("<b>VARIACIÓN ($)</b>", th_r_style), Paragraph("<b>ANÁLISIS</b>", th_style)],
        [Paragraph("Ingresos Operacionales (Ventas)", td_style), Paragraph("$ 0", td_r_style), Paragraph("$ 61.300.000", td_r_bold), Paragraph("+$ 61.300.000", td_r_green), Paragraph("Facturación comercial plena", td_style)],
        [Paragraph("Menos: Costo de Ventas (Mercancías)", td_style), Paragraph("$ 0", td_r_style), Paragraph("$ 41.640.000", td_r_style), Paragraph("+$ 41.640.000", td_r_style), Paragraph("67,93% de las ventas", td_style)],
        [Paragraph("<b>UTILIDAD BRUTA EN VENTAS</b>", td_bold), Paragraph("<b>$ 0</b>", td_r_bold), Paragraph("<b>$ 19.660.000</b>", td_r_bold), Paragraph("<b>+$ 19.660.000</b>", td_r_green), Paragraph("<b>Margen Bruto: 32,07%</b>", td_bold)],
        [Paragraph("Menos: Gastos de Administración", td_style), Paragraph("$ 0", td_r_style), Paragraph("$ 2.450.000", td_r_style), Paragraph("+$ 2.450.000", td_r_style), Paragraph("Nómina administrativa", td_style)],
        [Paragraph("Menos: Gastos Financieros y Servicios", td_style), Paragraph("$ 0", td_r_style), Paragraph("$ 763.918", td_r_style), Paragraph("+$ 763.918", td_r_style), Paragraph("Intereses bancarios y servicios", td_style)],
        [Paragraph("<b>UTILIDAD NETA DEL EJERCICIO</b>", td_bold), Paragraph("-$ 1.271.250", td_r_style), Paragraph("<font color='#059669'><b>+$ 16.446.082</b></font>", td_r_bold), Paragraph("<font color='#059669'><b>+$ 17.717.332</b></font>", td_r_green), Paragraph("<b>Margen Neto: 26,83%</b>", td_bold)],
    ]
    t_er_feb = Table(er_feb, colWidths=[174, 75, 80, 85, 90])
    t_er_feb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#DCFCE7")),
    ]))
    story.append(t_er_feb)
    story.append(Spacer(1, 4))

    story.append(Paragraph("ESTADO DE CAMBIOS EN EL PATRIMONIO — ECP FEBRERO 2026", subsec_header_style))
    ecp_feb = [
        [Paragraph("<b>CONCEPTO PATRIMONIAL</b>", th_style), Paragraph("<b>SALDO 31 ENE</b>", th_r_style), Paragraph("<b>UTILIDAD MES</b>", th_r_style), Paragraph("<b>RESERVA LEGAL</b>", th_r_style), Paragraph("<b>SALDO 28 FEB</b>", th_r_style)],
        [Paragraph("Capital Suscrito y Pagado (3105)", td_style), Paragraph("$ 248.600.000", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("$ 248.600.000", td_r_bold)],
        [Paragraph("Reserva Legal (10% Ley 222)", td_style), Paragraph("$ 0", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("+$ 1.827.342", td_r_style), Paragraph("$ 1.827.342", td_r_bold)],
        [Paragraph("Resultados del Ejercicio y Acumulados", td_style), Paragraph("-$ 1.271.250", td_r_style), Paragraph("+$ 16.446.082", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("$ 15.174.832", td_r_bold)],
        [Paragraph("<b>TOTAL PATRIMONIO NETO</b>", td_bold), Paragraph("<b>$ 247.328.750</b>", td_r_bold), Paragraph("<b>+$ 16.446.082</b>", td_r_bold), Paragraph("<b>+$ 1.827.342</b>", td_r_bold), Paragraph("<b>$ 265.602.175</b>", td_r_bold)],
    ]
    t_ecp_feb = Table(ecp_feb, colWidths=[184, 80, 80, 80, 80])
    t_ecp_feb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#EEF2FF")),
    ]))
    story.append(t_ecp_feb)
    story.append(Spacer(1, 4))

    story.append(Paragraph("ESTADO DE FLUJOS DE EFECTIVO — EFE FEBRERO 2026 (MÉTODO INDIRECTO)", subsec_header_style))
    efe_feb = [
        [Paragraph("<b>CONCEPTO OPERATIVO Y FINANCIERO</b>", th_style), Paragraph("<b>VALOR (COP)</b>", th_r_style)],
        [Paragraph("<b>Utilidad Neta del Ejercicio (Punto de partida)</b>", td_bold), Paragraph("+$ 16.446.082", td_r_bold)],
        [Paragraph("  (+) Depreciación y amortizaciones del mes", td_style), Paragraph("+$ 1.120.467", td_r_style)],
        [Paragraph("  (-) Variación de Cuentas por Cobrar Clientes (Ventas a crédito)", td_style), Paragraph("-$ 28.857.500", td_r_style)],
        [Paragraph("  (-) Variación de Inventarios (Compras para stock en bodega)", td_style), Paragraph("-$ 29.160.000", td_r_style)],
        [Paragraph("  (+) Variación de Pasivos Operacionales (Proveedores e IVA por pagar)", td_style), Paragraph("+$ 80.641.618", td_r_style)],
        [Paragraph("  <b>Flujo Neto de Efectivo de Actividades de Operación</b>", td_bold), Paragraph("<b>+$ 40.190.667</b>", td_r_green)],
        [Paragraph("<b>Flujo Neto de Efectivo de Actividades de Inversión</b> (Adecuaciones locativas)", td_bold), Paragraph("<b>-$ 8.769.776</b>", td_r_red)],
        [Paragraph("<b>Flujo Neto de Efectivo de Actividades de Financiación</b> (Crédito Bancolombia)", td_bold), Paragraph("<b>+$ 39.662.637</b>", td_r_green)],
        [Paragraph("<b>INCREMENTO NETO DE EFECTIVO EN EL MES DE FEBRERO</b>", td_bold), Paragraph("<b>+$ 71.083.528</b>", td_r_green)],
        [Paragraph("Saldo Inicial de Efectivo (01 de Febrero 2026)", td_style), Paragraph("$ 36.000.000", td_r_style)],
        [Paragraph("<b>SALDO FINAL DE EFECTIVO AL 28 DE FEBRERO DE 2026</b>", td_bold), Paragraph("<b>$ 107.083.528</b>", td_r_green)],
    ]
    t_efe_feb = Table(efe_feb, colWidths=[384, 120])
    t_efe_feb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,11), (-1,11), colors.HexColor("#DCFCE7")),
    ]))
    story.append(t_efe_feb)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: ESTADO DE NOTAS Y REVELACIONES COMPLETAS — MES DE FEBRERO 2026
    # =========================================================================
    story.append(Paragraph("ESTADO DE NOTAS Y REVELACIONES A LOS ESTADOS FINANCIEROS — NOTAS FEBRERO 2026", sec_header_style))
    story.append(Paragraph("Revelación Completa y Exhaustiva conforme a NIIF para las PYMES (Secciones 11, 13, 23, 29)", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=8, spaceBefore=2))

    notas_feb_completas = (
        "<b>NOTA 1. DESPEGUE DE INGRESOS OPERACIONALES POR VENTAS (SECCIÓN 23 NIIF PYMES):</b><br/>"
        "Durante el mes de febrero de 2026, ELECTROVIVIENDA S.A.S inició formalmente su facturación comercial generando ingresos netos "
        "por valor de <b>$61.300.000</b> (Facturas electrónicas de venta FV-01 a FV-03). Las ventas se distribuyeron en dos modalidades:<br/>"
        "• <i>Ventas de Contado:</i> <b>$32.442.500</b> (52,92%) cobradas inmediatamente en efectivo y consignadas en Bancolombia.<br/>"
        "• <i>Ventas a Crédito Comercial:</i> <b>$28.857.500</b> (47,08%) otorgadas a clientes corporativos con plazo a 30 días, respaldadas con pagaré.<br/>"
        "El costo de ventas asociado a las unidades despachadas ascendió a <b>$41.640.000</b> (67,93% del ingreso), generando una Utilidad Bruta "
        "en Ventas de <b>$19.660.000</b> (margen comercial bruto del <b>32,07%</b>).<br/><br/>"

        "<b>NOTA 2. INVENTARIOS DE MERCANCÍAS Y MÉTODO DE VALUACIÓN (SECCIÓN 13 NIIF PYMES):</b><br/>"
        "La empresa adoptó el sistema de inventario permanente y el método de valuación por <b>Promedio Ponderado</b>. Al cierre de febrero, "
        "el inventario físico en bodega asciende a <b>$29.160.000</b> distribuido en las siguientes referencias de alta demanda:<br/>"
        "• Neveras No Frost 400L (Ref. NEV-01): 8 unidades a costo unitario de $2.200.000 = <b>$17.600.000</b>.<br/>"
        "• Lavadoras Automáticas 18kg (Ref. LAV-02): 7 unidades a costo unitario de $1.650.000 = <b>$11.560.000</b>.<br/>"
        "No se identificaron indicios de deterioro de valor ni obsolescencia tecnológica; el valor neto realizable supera el costo en libros.<br/><br/>"

        "<b>NOTA 3. OBLIGACIONES FINANCIERAS Y CRÉDITO BANCARIO (SECCIÓN 11 NIIF PYMES):</b><br/>"
        "La compañía gestionó y obtuvo la aprobación de un crédito ordinario de tesorería con Bancolombia S.A. por valor neto desembolsado "
        "de <b>$39.662.637</b>. El crédito se pactó a una tasa IBR + 4,5% E.A. a un plazo de 36 meses, clasificado en el pasivo no corriente. "
        "Los recursos fueron destinados a fondear compras de inventario y capital de trabajo.<br/><br/>"

        "<b>NOTA 4. CUENTAS COMERCIALES POR PAGAR Y OBLIGACIONES FISCALES (PASIVO CORRIENTE):</b><br/>"
        "El pasivo a corto plazo al 28 de febrero asciende a <b>$80.641.618</b> y se compone de:<br/>"
        "• Proveedores Nacionales de Mercancías (Whirlpool, Mabe, Challenger): <b>$72.450.000</b> con vencimiento a 60 días.<br/>"
        "• Impuesto sobre las Ventas por Pagar (IVA 19% generado menos descontable): <b>$3.845.200</b>.<br/>"
        "• Retención en la Fuente por Pagar (Compras 2.5% y Servicios 4%): <b>$1.896.418</b>.<br/>"
        "• Retenciones y aportes de nómina por pagar: <b>$2.450.000</b>.<br/><br/>"

        "<b>NOTA 5. RESERVA LEGAL Y DISTRIBUCIÓN DE UTILIDADES (CÓDIGO DE COMERCIO):</b><br/>"
        "De conformidad con el Artículo 452 del Código de Comercio y la Ley 222 de 1995, se apropió el 10% de la utilidad líquida del período "
        "por valor de <b>$1.827.342</b> con destino a la Reserva Legal Obligatoria. La utilidad neta restante del mes asciende a <b>$16.446.082</b>, "
        "acumulando un superávit neto patrimonial de <b>$15.174.832</b> tras absorber la pérdida contable inicial de enero."
    )
    story.append(Paragraph(notas_feb_completas, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 6: ESTADOS FINANCIEROS OFICIALES — MES DE MARZO 2026 (4 ESTADOS)
    # =========================================================================
    story.append(Paragraph("ESTADOS FINANCIEROS OFICIALES — MES DE MARZO 2026", sec_header_style))
    story.append(Paragraph("Causación de Gastos Operativos y Pago de Nómina • Comparativo Febrero vs Marzo 2026", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=6, spaceBefore=2))

    story.append(Paragraph("ESTADO DE SITUACIÓN FINANCIERA COMPARATIVO — ESF FEBRERO VS MARZO 2026", subsec_header_style))
    esf_mar = [
        [Paragraph("<b>RUBRO CONTABLE (COP)</b>", th_style), Paragraph("<b>FEBRERO 2026</b>", th_r_style), Paragraph("<b>MARZO 2026</b>", th_r_style), Paragraph("<b>VAR. ABS ($)</b>", th_r_style), Paragraph("<b>VAR. REL (%)</b>", th_r_style)],
        [Paragraph("<b>Activo Corriente</b>", td_bold), Paragraph("$ 173.457.213", td_r_style), Paragraph("<b>$ 157.899.440</b>", td_r_bold), Paragraph("-$ 15.557.773", td_r_red), Paragraph("-8,97 %", td_r_red)],
        [Paragraph("  Efectivo y Equivalentes", td_style), Paragraph("$ 107.083.528", td_r_style), Paragraph("$ 93.502.800", td_r_style), Paragraph("-$ 13.580.728", td_r_red), Paragraph("-12,68 %", td_r_red)],
        [Paragraph("  Deudores Comerciales (Clientes)", td_style), Paragraph("$ 28.857.500", td_r_style), Paragraph("$ 28.857.500", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("0,00 %", td_r_style)],
        [Paragraph("  Inventarios (Bodega)", td_style), Paragraph("$ 29.160.000", td_r_style), Paragraph("$ 29.160.000", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("0,00 %", td_r_style)],
        [Paragraph("  Anticipos de Impuestos", td_style), Paragraph("$ 8.356.185", td_r_style), Paragraph("$ 6.379.140", td_r_style), Paragraph("-$ 1.977.045", td_r_red), Paragraph("-23,66 %", td_r_red)],
        [Paragraph("<b>Activo No Corriente (PP&E)</b>", td_bold), Paragraph("$ 212.449.217", td_r_style), Paragraph("<b>$ 211.169.684</b>", td_r_bold), Paragraph("-$ 1.279.533", td_r_style), Paragraph("-0,60 %", td_r_style)],
        [Paragraph("<b>TOTAL ACTIVO</b>", td_bold), Paragraph("<b>$ 385.906.430</b>", td_r_bold), Paragraph("<b>$ 369.069.124</b>", td_r_bold), Paragraph("<b>-$ 16.837.306</b>", td_r_red), Paragraph("<b>-4,36 %</b>", td_r_red)],
        [Paragraph("<b>Pasivo Corriente (&lt;12 meses)</b>", td_bold), Paragraph("$ 80.641.618", td_r_style), Paragraph("$ 82.409.727", td_r_style), Paragraph("+$ 1.768.109", td_r_style), Paragraph("+2,19 %", td_r_style)],
        [Paragraph("<b>Pasivo No Corriente (Crédito LP)</b>", td_bold), Paragraph("$ 39.662.637", td_r_style), Paragraph("$ 38.211.799", td_r_style), Paragraph("-$ 1.450.838", td_r_green), Paragraph("-3,66 %", td_r_green)],
        [Paragraph("<b>TOTAL PASIVO</b>", td_bold), Paragraph("<b>$ 120.304.255</b>", td_r_bold), Paragraph("<b>$ 120.621.526</b>", td_r_bold), Paragraph("<b>+$ 317.271</b>", td_r_style), Paragraph("<b>+0,26 %</b>", td_r_style)],
        [Paragraph("<b>PATRIMONIO NETO</b>", td_bold), Paragraph("<b>$ 265.602.175</b>", td_r_bold), Paragraph("<b>$ 248.447.598</b>", td_r_bold), Paragraph("<b>-$ 17.154.577</b>", td_r_red), Paragraph("<b>-6,46 %</b>", td_r_red)],
        [Paragraph("  Capital Social (3105)", td_style), Paragraph("$ 248.600.000", td_r_style), Paragraph("$ 248.600.000", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("0,00 %", td_r_style)],
        [Paragraph("  Reserva Legal Obligatoria", td_style), Paragraph("$ 1.827.342", td_r_style), Paragraph("$ 1.827.342", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("0,00 %", td_r_style)],
        [Paragraph("  Resultados Acumulados y Ejercicio", td_style), Paragraph("+$ 15.174.832", td_r_style), Paragraph("-$ 1.979.744", td_r_style), Paragraph("-$ 17.154.577", td_r_red), Paragraph("-113,05 %", td_r_red)],
        [Paragraph("<b>TOTAL PASIVO Y PATRIMONIO</b>", td_bold), Paragraph("<b>$ 385.906.430</b>", td_r_bold), Paragraph("<b>$ 369.069.124</b>", td_r_bold), Paragraph("<b>-$ 16.837.306</b>", td_r_red), Paragraph("<b>-4,36 %</b>", td_r_red)],
    ]
    t_esf_mar = Table(esf_mar, colWidths=[184, 80, 80, 80, 80])
    t_esf_mar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,15), (-1,15), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_esf_mar)
    story.append(Spacer(1, 4))

    story.append(Paragraph("ESTADO DE RESULTADO INTEGRAL COMPARATIVO — ER FEBRERO VS MARZO 2026", subsec_header_style))
    er_mar = [
        [Paragraph("<b>CONCEPTO / RENGLÓN</b>", th_style), Paragraph("<b>FEBRERO</b>", th_r_style), Paragraph("<b>MARZO</b>", th_r_style), Paragraph("<b>VARIACIÓN ($)</b>", th_r_style), Paragraph("<b>ANÁLISIS MARZO</b>", th_style)],
        [Paragraph("Ingresos Operacionales (Ventas)", td_style), Paragraph("$ 61.300.000", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("-$ 61.300.000", td_r_red), Paragraph("Mes sin ventas comerciales", td_style)],
        [Paragraph("Menos: Costo de Ventas", td_style), Paragraph("$ 41.640.000", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("-$ 41.640.000", td_r_green), Paragraph("Sin salida de mercancía", td_style)],
        [Paragraph("<b>UTILIDAD BRUTA EN VENTAS</b>", td_bold), Paragraph("<b>$ 19.660.000</b>", td_r_bold), Paragraph("<b>$ 0</b>", td_r_bold), Paragraph("<b>-$ 19.660.000</b>", td_r_red), Paragraph("<b>Margen Bruto: 0,00%</b>", td_bold)],
        [Paragraph("Menos: Gastos de Personal (Nómina)", td_style), Paragraph("$ 2.450.000", td_r_style), Paragraph("$ 10.450.000", td_r_style), Paragraph("+$ 8.000.000", td_r_red), Paragraph("Nómina integral + parafiscales", td_style)],
        [Paragraph("Menos: Arrendamientos y Servicios", td_style), Paragraph("$ 763.918", td_r_style), Paragraph("$ 6.704.577", td_r_style), Paragraph("+$ 5.940.659", td_r_red), Paragraph("Servicios y amortizaciones", td_style)],
        [Paragraph("<b>RESULTADO NETO DEL EJERCICIO</b>", td_bold), Paragraph("<font color='#059669'><b>+$ 16.446.082</b></font>", td_r_bold), Paragraph("<font color='#DC2626'><b>-$ 17.154.577</b></font>", td_r_bold), Paragraph("<font color='#DC2626'><b>-$ 33.600.659</b></font>", td_r_red), Paragraph("<b>Pérdida por absorción fija</b>", td_bold)],
    ]
    t_er_mar = Table(er_mar, colWidths=[174, 75, 80, 85, 90])
    t_er_mar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#FEE2E2")),
    ]))
    story.append(t_er_mar)
    story.append(Spacer(1, 4))

    story.append(Paragraph("ESTADO DE CAMBIOS EN EL PATRIMONIO — ECP MARZO 2026", subsec_header_style))
    ecp_mar = [
        [Paragraph("<b>RUBRO PATRIMONIAL</b>", th_style), Paragraph("<b>SALDO 28 FEB</b>", th_r_style), Paragraph("<b>PÉRDIDA MARZO</b>", th_r_style), Paragraph("<b>SALDO 31 MAR</b>", th_r_style)],
        [Paragraph("Capital Social Suscrito y Pagado (3105)", td_style), Paragraph("$ 248.600.000", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("$ 248.600.000", td_r_bold)],
        [Paragraph("Reserva Legal Obligatoria (3305)", td_style), Paragraph("$ 1.827.342", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("$ 1.827.342", td_r_bold)],
        [Paragraph("Resultados del Ejercicio y Acumulados", td_style), Paragraph("+$ 15.174.832", td_r_style), Paragraph("-$ 17.154.577", td_r_style), Paragraph("-$ 1.979.744", td_r_bold)],
        [Paragraph("<b>TOTAL PATRIMONIO NETO</b>", td_bold), Paragraph("<b>$ 265.602.175</b>", td_r_bold), Paragraph("<b>-$ 17.154.577</b>", td_r_bold), Paragraph("<b>$ 248.447.598</b>", td_r_bold)],
    ]
    t_ecp_mar = Table(ecp_mar, colWidths=[204, 100, 100, 100])
    t_ecp_mar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t_ecp_mar)
    story.append(Spacer(1, 4))

    story.append(Paragraph("ESTADO DE FLUJOS DE EFECTIVO — EFE MARZO 2026 (MÉTODO INDIRECTO)", subsec_header_style))
    efe_mar = [
        [Paragraph("<b>CONCEPTO / FLUJO DE CAJA</b>", th_style), Paragraph("<b>VALOR (COP)</b>", th_r_style)],
        [Paragraph("<b>Pérdida Neta del Ejercicio en Marzo</b>", td_bold), Paragraph("-$ 17.154.577", td_r_style)],
        [Paragraph("  (+) Depreciación del mes (PP&E)", td_style), Paragraph("+$ 1.279.533", td_r_style)],
        [Paragraph("  (+) Variación neta en pasivos operacionales acumulados", td_style), Paragraph("+$ 3.745.154", td_r_style)],
        [Paragraph("  <b>Flujo Neto de Actividades de Operación</b>", td_bold), Paragraph("<b>-$ 12.129.890</b>", td_r_red)],
        [Paragraph("<b>Flujo Neto de Actividades de Inversión</b>", td_bold), Paragraph("<b>$ 0</b>", td_r_style)],
        [Paragraph("<b>Flujo Neto de Actividades de Financiación</b> (Amortización capital Bancolombia)", td_bold), Paragraph("<b>-$ 1.450.838</b>", td_r_red)],
        [Paragraph("<b>DISMINUCIÓN NETA DE EFECTIVO EN EL MES DE MARZO</b>", td_bold), Paragraph("<b>-$ 13.580.728</b>", td_r_red)],
        [Paragraph("Saldo Inicial de Efectivo (01 de Marzo 2026)", td_style), Paragraph("$ 107.083.528", td_r_style)],
        [Paragraph("<b>SALDO FINAL DE EFECTIVO AL 31 DE MARZO DE 2026</b>", td_bold), Paragraph("<b>$ 93.502.800</b>", td_r_green)],
    ]
    t_efe_mar = Table(efe_mar, colWidths=[384, 120])
    t_efe_mar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,9), (-1,9), colors.HexColor("#DCFCE7")),
    ]))
    story.append(t_efe_mar)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 7: ESTADO DE NOTAS Y REVELACIONES COMPLETAS — MES DE MARZO 2026
    # =========================================================================
    story.append(Paragraph("ESTADO DE NOTAS Y REVELACIONES A LOS ESTADOS FINANCIEROS — NOTAS MARZO 2026", sec_header_style))
    story.append(Paragraph("Revelación Completa y Exhaustiva conforme a NIIF para las PYMES (Secciones 11, 21, 28)", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=8, spaceBefore=2))

    notas_mar_completas = (
        "<b>NOTA 1. ESTRUCTURA Y CAUSACIÓN DE BENEFICIOS A EMPLEADOS (SECCIÓN 28 NIIF PYMES):</b><br/>"
        "Durante el mes de marzo de 2026, la sociedad causó y liquidó la nómina integral de su personal operativo y administrativo por un "
        "valor bruto total de <b>$10.450.000</b>. De acuerdo con las normas laborales colombianas (Código Sustantivo del Trabajo), el detalle es:<br/>"
        "• <i>Sueldos Básicos y Subsidio de Transporte:</i> Salarios devengados por Gerente, Asesor Comercial y Contador por $7.250.000.<br/>"
        "• <i>Seguridad Social Patronal:</i> Aporte a Salud (8,5% sobre bases aplicables), Pensión (12%) y ARL Riesgo I: <b>$1.485.000</b>.<br/>"
        "• <i>Parafiscales:</i> Caja de Compensación Familiar Comfenalco (4%), ICBF (3%) y SENA (2%): <b>$652.500</b>.<br/>"
        "• <i>Prestaciones Sociales Acumuladas:</i> Provisión de Cesantías (8,33%), Intereses (1%), Prima (8,33%) y Vacaciones (4,17%): <b>$1.062.500</b>.<br/>"
        "Todos los pagos de nómina y seguridad social a través de planilla PILA fueron cancelados en efectivo vía transferencia bancaria.<br/><br/>"

        "<b>NOTA 2. GASTOS GENERALES, SERVICIOS Y ADECUACIONES OPERACIONALES:</b><br/>"
        "Los gastos operacionales de administración y ventas ascendieron a <b>$6.704.577</b>, correspondientes a:<br/>"
        "• Servicios Públicos (Energía ESSA, Acueducto Empas, Gas e Internet fibra óptica): <b>$1.854.200</b>.<br/>"
        "• Arrendamiento y cuotas de mantenimiento del local: <b>$2.150.000</b>.<br/>"
        "• Gastos de publicidad, diseño web, facturación electrónica y papelería: <b>$1.420.844</b>.<br/>"
        "• Depreciación de construcciones y camioneta Chevrolet: <b>$1.279.533</b>.<br/><br/>"

        "<b>NOTA 3. ANÁLISIS DE LA PÉRDIDA CONTABLE DEL MES DE MARZO (-$17.154.577):</b><br/>"
        "En marzo la sociedad no registró facturación comercial debido al período de transición y negociación con nuevos distribuidores. "
        "En consecuencia, la empresa absorbió la totalidad de sus costos fijos ($10,45M de nómina y $6,70M de gastos generales), generando "
        "una pérdida neta de <b>-$17.154.577</b>. Sin embargo, no se generó riesgo de iliquidez gracias al colchón financiero acumulado en febrero.<br/><br/>"

        "<b>NOTA 4. AMORTIZACIÓN Y ESTADO DE LA DEUDA BANCARIA (BANCOLOMBIA):</b><br/>"
        "Se efectuó el pago puntual de la cuota mensual del crédito de tesorería, compuesta por amortización a capital de <b>$1.450.838</b> "
        "e intereses corrientes por <b>$485.210</b>. El saldo insoluto del crédito a largo plazo se redujo a <b>$38.211.799</b>.<br/><br/>"

        "<b>NOTA 5. DISPONIBILIDAD DE EFECTIVO Y CAPITAL DE TRABAJO:</b><br/>"
        "A pesar del flujo de caja negativo del mes (-$13,58M por pago de personal y servicios), la compañía cerró marzo con <b>$93.502.800</b> "
        "en sus cuentas bancarias, manteniendo un Capital de Trabajo Neto holgado de <b>$75.489.713</b> para enfrentar el segundo trimestre."
    )
    story.append(Paragraph(notas_mar_completas, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 8: ESTADOS FINANCIEROS OFICIALES — MES DE ABRIL 2026 (4 ESTADOS)
    # =========================================================================
    story.append(Paragraph("ESTADOS FINANCIEROS OFICIALES — MES DE ABRIL 2026", sec_header_style))
    story.append(Paragraph("Reactivación Comercial y Cierre del Cuatrimestre • Comparativo Marzo vs Abril 2026", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=6, spaceBefore=2))

    story.append(Paragraph("ESTADO DE SITUACIÓN FINANCIERA COMPARATIVO — ESF MARZO VS ABRIL 2026", subsec_header_style))
    esf_abr = [
        [Paragraph("<b>RUBRO CONTABLE (COP)</b>", th_style), Paragraph("<b>MARZO 2026</b>", th_r_style), Paragraph("<b>ABRIL 2026</b>", th_r_style), Paragraph("<b>VAR. ABS ($)</b>", th_r_style), Paragraph("<b>VAR. REL (%)</b>", th_r_style)],
        [Paragraph("<b>Activo Corriente</b>", td_bold), Paragraph("$ 157.899.440", td_r_style), Paragraph("<b>$ 121.342.532</b>", td_r_bold), Paragraph("-$ 36.556.908", td_r_red), Paragraph("-23,15 %", td_r_red)],
        [Paragraph("  Efectivo y Equivalentes", td_style), Paragraph("$ 93.502.800", td_r_style), Paragraph("$ 51.852.812", td_r_style), Paragraph("-$ 41.649.988", td_r_red), Paragraph("-44,54 %", td_r_red)],
        [Paragraph("  Deudores Comerciales (Clientes)", td_style), Paragraph("$ 28.857.500", td_r_style), Paragraph("$ 28.857.500", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("0,00 %", td_r_style)],
        [Paragraph("  Inventarios (Bodega)", td_style), Paragraph("$ 29.160.000", td_r_style), Paragraph("$ 33.822.000", td_r_style), Paragraph("+$ 4.662.000", td_r_green), Paragraph("+15,99 %", td_r_green)],
        [Paragraph("  Anticipos de Impuestos", td_style), Paragraph("$ 6.379.140", td_r_style), Paragraph("$ 6.810.220", td_r_style), Paragraph("+$ 431.080", td_r_green), Paragraph("+6,76 %", td_r_green)],
        [Paragraph("<b>Activo No Corriente (PP&E)</b>", td_bold), Paragraph("$ 211.169.684", td_r_style), Paragraph("<b>$ 209.890.152</b>", td_r_bold), Paragraph("-$ 1.279.532", td_r_style), Paragraph("-0,61 %", td_r_style)],
        [Paragraph("<b>TOTAL ACTIVO</b>", td_bold), Paragraph("<b>$ 369.069.124</b>", td_r_bold), Paragraph("<b>$ 331.232.683</b>", td_r_bold), Paragraph("<b>-$ 37.836.441</b>", td_r_red), Paragraph("<b>-10,25 %</b>", td_r_red)],
        [Paragraph("<b>Pasivo Corriente (&lt;12 meses)</b>", td_bold), Paragraph("$ 82.409.727", td_r_style), Paragraph("$ 53.927.428", td_r_style), Paragraph("-$ 28.482.299", td_r_green), Paragraph("-34,56 %", td_r_green)],
        [Paragraph("<b>Pasivo No Corriente (Crédito LP)</b>", td_bold), Paragraph("$ 38.211.799", td_r_style), Paragraph("$ 36.744.815", td_r_style), Paragraph("-$ 1.466.984", td_r_green), Paragraph("-3,84 %", td_r_green)],
        [Paragraph("<b>TOTAL PASIVO</b>", td_bold), Paragraph("<b>$ 120.621.526</b>", td_r_bold), Paragraph("<b>$ 90.672.243</b>", td_r_bold), Paragraph("<b>-$ 29.949.283</b>", td_r_green), Paragraph("<b>-24,83 %</b>", td_r_green)],
        [Paragraph("<b>PATRIMONIO NETO</b>", td_bold), Paragraph("<b>$ 248.447.598</b>", td_r_bold), Paragraph("<b>$ 240.560.440</b>", td_r_bold), Paragraph("<b>-$ 7.887.158</b>", td_r_red), Paragraph("<b>-3,17 %</b>", td_r_red)],
        [Paragraph("  Capital Social (3105)", td_style), Paragraph("$ 248.600.000", td_r_style), Paragraph("$ 248.600.000", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("0,00 %", td_r_style)],
        [Paragraph("  Reserva Legal Obligatoria", td_style), Paragraph("$ 1.827.342", td_r_style), Paragraph("$ 1.827.342", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("0,00 %", td_r_style)],
        [Paragraph("  Resultados Acumulados y Ejercicio", td_style), Paragraph("-$ 1.979.744", td_r_style), Paragraph("-$ 9.866.902", td_r_style), Paragraph("-$ 7.887.158", td_r_red), Paragraph("-398,39 %", td_r_red)],
        [Paragraph("<b>TOTAL PASIVO Y PATRIMONIO</b>", td_bold), Paragraph("<b>$ 369.069.124</b>", td_r_bold), Paragraph("<b>$ 331.232.683</b>", td_r_bold), Paragraph("<b>-$ 37.836.441</b>", td_r_red), Paragraph("<b>-10,25 %</b>", td_r_red)],
    ]
    t_esf_abr = Table(esf_abr, colWidths=[184, 80, 80, 80, 80])
    t_esf_abr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,15), (-1,15), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_esf_abr)
    story.append(Spacer(1, 4))

    story.append(Paragraph("ESTADO DE RESULTADO INTEGRAL COMPARATIVO — ER MARZO VS ABRIL 2026", subsec_header_style))
    er_abr = [
        [Paragraph("<b>CONCEPTO / RENGLÓN</b>", th_style), Paragraph("<b>MARZO</b>", th_r_style), Paragraph("<b>ABRIL</b>", th_r_style), Paragraph("<b>VARIACIÓN ($)</b>", th_r_style), Paragraph("<b>ANÁLISIS ABRIL</b>", th_style)],
        [Paragraph("Ingresos Operacionales (Ventas)", td_style), Paragraph("$ 0", td_r_style), Paragraph("$ 8.156.500", td_r_bold), Paragraph("+$ 8.156.500", td_r_green), Paragraph("Ventas al contado y crédito", td_style)],
        [Paragraph("Menos: Costo de Ventas", td_style), Paragraph("$ 0", td_r_style), Paragraph("$ 3.288.000", td_r_style), Paragraph("+$ 3.288.000", td_r_style), Paragraph("40,31% de las ventas", td_style)],
        [Paragraph("<b>UTILIDAD BRUTA EN VENTAS</b>", td_bold), Paragraph("<b>$ 0</b>", td_r_bold), Paragraph("<b>$ 4.868.500</b>", td_r_bold), Paragraph("<b>+$ 4.868.500</b>", td_r_green), Paragraph("<b>Margen Récord: 59,69%</b>", td_bold)],
        [Paragraph("Menos: Gastos de Personal (Nómina)", td_style), Paragraph("$ 10.450.000", td_r_style), Paragraph("$ 9.250.000", td_r_style), Paragraph("-$ 1.200.000", td_r_green), Paragraph("Optimización de personal", td_style)],
        [Paragraph("Menos: Arrendamientos y Servicios", td_style), Paragraph("$ 6.704.577", td_r_style), Paragraph("$ 3.505.658", td_r_style), Paragraph("-$ 3.198.919", td_r_green), Paragraph("Reducción de gastos fijos", td_style)],
        [Paragraph("<b>RESULTADO NETO DEL EJERCICIO</b>", td_bold), Paragraph("<font color='#DC2626'><b>-$ 17.154.577</b></font>", td_r_bold), Paragraph("<font color='#DC2626'><b>-$ 7.887.158</b></font>", td_r_bold), Paragraph("<font color='#059669'><b>+$ 9.267.419</b></font>", td_r_green), Paragraph("<b>Pérdida reducida a la mitad</b>", td_bold)],
    ]
    t_er_abr = Table(er_abr, colWidths=[174, 75, 80, 85, 90])
    t_er_abr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#FEF3C7")),
    ]))
    story.append(t_er_abr)
    story.append(Spacer(1, 4))

    story.append(Paragraph("ESTADO DE CAMBIOS EN EL PATRIMONIO — ECP ABRIL 2026", subsec_header_style))
    ecp_abr = [
        [Paragraph("<b>RUBRO PATRIMONIAL</b>", th_style), Paragraph("<b>SALDO 31 MAR</b>", th_r_style), Paragraph("<b>RESULTADO ABRIL</b>", th_r_style), Paragraph("<b>SALDO 30 ABR</b>", th_r_style)],
        [Paragraph("Capital Suscrito y Pagado (3105)", td_style), Paragraph("$ 248.600.000", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("$ 248.600.000", td_r_bold)],
        [Paragraph("Reserva Legal Obligatoria (3305)", td_style), Paragraph("$ 1.827.342", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("$ 1.827.342", td_r_bold)],
        [Paragraph("Resultados del Ejercicio y Acumulados", td_style), Paragraph("-$ 1.979.744", td_r_style), Paragraph("-$ 7.887.158", td_r_style), Paragraph("-$ 9.866.902", td_r_bold)],
        [Paragraph("<b>TOTAL PATRIMONIO NETO</b>", td_bold), Paragraph("<b>$ 248.447.598</b>", td_r_bold), Paragraph("<b>-$ 7.887.158</b>", td_r_bold), Paragraph("<b>$ 240.560.440</b>", td_r_bold)],
    ]
    t_ecp_abr = Table(ecp_abr, colWidths=[204, 100, 100, 100])
    t_ecp_abr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t_ecp_abr)
    story.append(Spacer(1, 4))

    story.append(Paragraph("ESTADO DE FLUJOS DE EFECTIVO — EFE ABRIL 2026 (MÉTODO INDIRECTO)", subsec_header_style))
    efe_abr = [
        [Paragraph("<b>CONCEPTO / FLUJO DE CAJA</b>", th_style), Paragraph("<b>VALOR (COP)</b>", th_r_style)],
        [Paragraph("<b>Resultado Neto del Ejercicio en Abril</b>", td_bold), Paragraph("-$ 7.887.158", td_r_style)],
        [Paragraph("  (+) Depreciación acumulada del mes", td_style), Paragraph("+$ 1.279.532", td_r_style)],
        [Paragraph("  (-) Compras de inventario pagadas en efectivo", td_style), Paragraph("-$ 4.662.000", td_r_style)],
        [Paragraph("  (-) Pago masivo de pasivos a proveedores y retenciones", td_style), Paragraph("-$ 28.913.378", td_r_style)],
        [Paragraph("  <b>Flujo Neto de Actividades de Operación</b>", td_bold), Paragraph("<b>-$ 40.183.004</b>", td_r_red)],
        [Paragraph("<b>Flujo Neto de Actividades de Inversión</b>", td_bold), Paragraph("<b>$ 0</b>", td_r_style)],
        [Paragraph("<b>Flujo Neto de Actividades de Financiación</b> (Amortización cuota Bancolombia)", td_bold), Paragraph("<b>-$ 1.466.984</b>", td_r_red)],
        [Paragraph("<b>DISMINUCIÓN NETA DE EFECTIVO EN EL MES DE ABRIL</b>", td_bold), Paragraph("<b>-$ 41.649.988</b>", td_r_red)],
        [Paragraph("Saldo Inicial de Efectivo (01 de Abril 2026)", td_style), Paragraph("$ 93.502.800", td_r_style)],
        [Paragraph("<b>SALDO FINAL DE EFECTIVO AL 30 DE ABRIL DE 2026</b>", td_bold), Paragraph("<b>$ 51.852.812</b>", td_r_green)],
    ]
    t_efe_abr = Table(efe_abr, colWidths=[384, 120])
    t_efe_abr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,9), (-1,9), colors.HexColor("#DCFCE7")),
    ]))
    story.append(t_efe_abr)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 9: ESTADO DE NOTAS Y REVELACIONES COMPLETAS — MES DE ABRIL 2026
    # =========================================================================
    story.append(Paragraph("ESTADO DE NOTAS Y REVELACIONES A LOS ESTADOS FINANCIEROS — NOTAS ABRIL 2026", sec_header_style))
    story.append(Paragraph("Revelación Completa y Exhaustiva conforme a NIIF para las PYMES (Secciones 3, 11, 13, 29)", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=8, spaceBefore=2))

    notas_abr_completas = (
        "<b>NOTA 1. REACTIVACIÓN COMERCIAL Y MARGEN BRUTO RÉCORD (SECCIÓN 23 NIIF PYMES):</b><br/>"
        "En el mes de abril, la sociedad reactivó sus operaciones comerciales emitiendo facturas electrónicas por valor de <b>$8.156.500</b>. "
        "El costo de ventas fue de <b>$3.288.000</b> (apenas el 40,31% del ingreso), generando una Utilidad Bruta de <b>$4.868.500</b> "
        "con un <b>Margen Bruto récord del 59,69%</b>. Este margen superó ampliamente el promedio del sector gracias a la venta directa "
        "al consumidor de productos con alto valor agregado (Smart TVs 4K y Estufas a Gas).<br/><br/>"

        "<b>NOTA 2. PLAN MASIVO DE SANEAMIENTO DE PASIVOS OPERACIONALES:</b><br/>"
        "En abril la gerencia ejecutó un plan estratégico de pago de pasivos, desembolsando <b>$29.949.283</b> de efectivo en bancos para:<br/>"
        "• Cancelar facturas vencidas a proveedores nacionales de electrodomésticos: <b>$24.500.000</b>.<br/>"
        "• Pago de retenciones en la fuente y liquidaciones de IVA bimestral a la DIAN: <b>$3.982.299</b>.<br/>"
        "• Pago de la segunda cuota del crédito ordinario con Bancolombia: <b>$1.466.984</b> (saldo restante: $36.744.815).<br/>"
        "Gracias a este pago, los pasivos totales de la empresa bajaron de $120,6M a <b>$90.672.243</b>, logrando una estructura financiera muy sana.<br/><br/>"

        "<b>NOTA 3. INVENTARIO FÍSICO FINAL VALUADO POR PROMEDIO PONDERADO (KARDEX AL 30 DE ABRIL):</b><br/>"
        "El inventario físico disponible en la bodega principal asciende a <b>$33.822.000</b> (aumento neto de +$4,66M frente a marzo) "
        "distribuido exactamente en 4 referencias comerciales:<br/>"
        "• <i>Neveras No Frost 400L (NEV-01):</i> 7 unidades a costo promedio de $2.200.000 = <b>$15.400.000</b>.<br/>"
        "• <i>Lavadoras Automáticas 18kg (LAV-02):</i> 5 unidades a costo promedio de $1.650.000 = <b>$8.250.000</b>.<br/>"
        "• <i>Smart TV 55 Pulgadas 4K (TV-03):</i> 4 unidades a costo promedio de $1.850.000 = <b>$7.400.000</b>.<br/>"
        "• <i>Estufas a Gas 4 Puestos (EST-04):</i> 3 unidades a costo promedio de $924.000 = <b>$2.772.000</b>.<br/>"
        "El conteo físico al 100% coincidió exactamente con el sistema de control Kardex y registros contables de la cuenta 1435.<br/><br/>"

        "<b>NOTA 4. REESTRUCTURACIÓN DE GASTOS Y PUNTO DE EQUILIBRIO:</b><br/>"
        "Los gastos de personal se ajustaron a <b>$9.250.000</b> y los gastos generales a <b>$3.505.658</b> (ahorro de $4,4M frente a marzo). "
        "Esto redujo la pérdida mensual a <b>-$7.887.158</b> (menos de la mitad de marzo). Con el margen comercial actual del 59%, el punto "
        "de equilibrio de ELECTROVIVIENDA S.A.S se sitúa en <b>$22.000.000 de ventas mensuales</b>.<br/><br/>"

        "<b>NOTA 5. CERTIFICACIÓN DE NEGOCIO EN MARCHA (SECCIÓN 3 NIIF PYMES):</b><br/>"
        "Al cierre de abril de 2026, la sociedad cuenta con <b>$51.852.812</b> en bancos, <b>$28.857.500</b> en cartera por cobrar, "
        "<b>$33.822.000</b> en inventarios y un Patrimonio Neto de <b>$240.560.440</b> respaldado en bienes inmuebles propios. "
        "La administración certifica que la entidad posee capacidad financiera para continuar sus operaciones con total normalidad."
    )
    story.append(Paragraph(notas_abr_completas, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 10: ANÁLISIS FÁCIL Y DIDÁCTICO DE LO QUE PASÓ EN LA EMPRESA CON GRÁFICOS
    # =========================================================================
    story.append(Paragraph("3. ANÁLISIS FÁCIL Y DIDÁCTICO DE LO QUE PASÓ EN LA EMPRESA (CON GRÁFICOS)", sec_header_style))
    story.append(Paragraph("Explicación Sencilla en Palabras Claras de la Operación Cuatrimestral • Sin Fórmulas Proyectadas Complejas", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=8, spaceBefore=2))

    story.append(create_chart_income_evolution())
    story.append(Spacer(1, 6))

    p_ana_ing = (
        "<b>¿Qué pasó con las Ventas y las Ganancias de la Empresa? (Explicación Fácil):</b><br/>"
        "Durante estos primeros cuatro meses, la empresa vivió tres momentos muy claros:<br/>"
        "1. <b>Enero:</b> Fue el mes de nacimiento. Los socios fundadores aportaron la plata y los bienes para iniciar la empresa. "
        "No se vendió nada porque se estaban adecuando las instalaciones, pero se registró el gasto de depreciación legal.<br/>"
        "2. <b>Febrero:</b> Fue el gran despegue. Se vendieron <b>$61,3 millones de pesos</b> en electrodomésticos. Comprar esos productos costó "
        "$41,6M, por lo que quedaron <b>$19,6M de ganancia bruta</b>. Después de pagar los gastos del mes, la empresa obtuvo una <b>ganancia limpia "
        "récord de $16,4 millones de pesos</b>.<br/>"
        "3. <b>Marzo:</b> La empresa no tuvo ventas porque se concentró en negociaciones comerciales. Sin embargo, hubo que pagar la nómina completa "
        "de los trabajadores ($10,4M) y los servicios ($6,7M), lo que arrojó una pérdida contable de <b>-$17,1 millones</b>.<br/>"
        "4. <b>Abril:</b> La empresa volvió a vender ($8,15 millones) y logró una hazaña: vender con un <b>margen de ganancia muy alto del 59,69%</b>. "
        "Además, se bajaron los gastos de nómina y arriendos, logrando que la pérdida se redujera a menos de la mitad (-$7,88M)."
    )
    story.append(Paragraph(p_ana_ing, body_style))
    story.append(Spacer(1, 8))

    story.append(create_chart_asset_composition())
    story.append(Spacer(1, 6))

    p_ana_act = (
        "<b>¿En qué tiene invertida la plata la empresa al cierre de Abril? (Explicación Fácil):</b><br/>"
        "Al mirar el gráfico circular de la derecha, vemos que el dinero y los bienes de la empresa ($331,2 millones) están muy bien repartidos:<br/>"
        "• El <b>63,4%</b> ($209,9 millones) está en bienes raíces y vehículos propios: los terrenos, el local comercial y la camioneta de reparto.<br/>"
        "• El <b>15,6%</b> ($51,8 millones) es plata en efectivo depositada en Bancolombia, disponible para pagar salarios y proveedores.<br/>"
        "• El <b>10,2%</b> ($33,8 millones) está en la bodega en electrodomésticos nuevos (Neveras, Lavadoras, Televisores y Estufas).<br/>"
        "• El <b>8,7%</b> ($28,8 millones) son facturas que los clientes deben y que irán pagando en mayo."
    )
    story.append(Paragraph(p_ana_act, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 11: CAPACIDAD DE PAGO, CONCLUSIONES CLARAS Y FIRMAS OFICIALES
    # =========================================================================
    story.append(Paragraph("4. CAPACIDAD DE PAGO, CONCLUSIONES Y CERTIFICACIÓN OFICIAL", sec_header_style))
    story.append(Paragraph("Diagnóstico de Solvencia en Palabras Sencillas, Plan de Mejora y Firmas de Autoridades", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=6, spaceBefore=2))

    story.append(create_chart_liquidity_solvency())
    story.append(Spacer(1, 4))

    p_ana_liq = (
        "<b>¿Tiene la empresa suficiente dinero para pagar sus deudas? (Explicación Fácil de Solvencia):</b><br/>"
        "Sí, absolutamente. La empresa está <b>totalmente respaldada y no corre ningún riesgo de quiebra</b>:<br/>"
        "• Por cada <b>$1 de deuda</b> a corto plazo que debe pagar, la empresa tiene <b>$2,25 en bienes y plata disponible</b> para respaldarla.<br/>"
        "• Incluso si no vendiera ningún electrodoméstico de la bodega, con solo la plata de los bancos y las cuentas por cobrar tiene <b>$1,62 por cada peso de deuda</b>.<br/>"
        "• Además, en abril se pagaron <b>$29,9 millones de deudas viejas</b> con proveedores y la DIAN, dejando a la empresa con las cuentas muy limpias y sanas."
    )
    story.append(Paragraph(p_ana_liq, body_style))
    story.append(Spacer(1, 6))

    p_concl_facil = (
        "<b>Conclusiones Claras y Plan de Acción para Mayo (Segundo Trimestre):</b><br/>"
        "1. <b>Base Patrimonial Sólida:</b> Cuenta con $240,5M de patrimonio neto y bienes raíces propios sin hipotecas.<br/>"
        "2. <b>Liquidez en Bancos:</b> Se cerró abril con más de $51,8M en efectivo en Bancolombia, garantizando salarios y arriendos.<br/>"
        "3. <b>Punto de Equilibrio:</b> Tras el ahorro en nómina ($9,2M) y servicios ($3,5M), solo se necesita vender <b>$22M al mes</b> para operar con utilidad.<br/>"
        "4. <b>Cobro de Cartera:</b> Se gestionará el recaudo de $28,8M de facturas a crédito pendientes para fondear inventario sin créditos.<br/>"
        "5. <b>Negocio en Marcha:</b> Se certifica la viabilidad operativa y comercial ininterrumpida de ELECTROVIVIENDA S.A.S para todo 2026."
    )
    story.append(Paragraph(p_concl_facil, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>CERTIFICACIÓN PERICIAL Y FIRMAS FORMALES DE AUTORIDADES</b>", subsec_header_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_gold, spaceAfter=14, spaceBefore=2))

    firmas_data = [
        [
            Paragraph("________________________________________<br/><b>KEVIN GUERRERO</b><br/>Aprendiz en Gestión Contable y Financiera<br/>Elaboró • Ficha 123101 SENA CSET", td_style),
            Paragraph("________________________________________<br/><b>GEORGE OLAGO</b><br/>Instructor Líder de Contabilidad y Finanzas<br/>Revisó y Aprobó • SENA CSET Santander", td_style)
        ],
        [
            Paragraph("<br/><br/>________________________________________<br/><b>MARCO AURELIO PEDRAZA DÍAZ</b><br/>Representante Legal / Gerente General<br/>ELECTROVIVIENDA S.A.S — C.C. 83.630.214", td_style),
            Paragraph("<br/><br/>________________________________________<br/><b>CARLOS EDUARDO DAZA GÓMEZ</b><br/>Revisor Fiscal Titular<br/>T.P. 145892-T • Certificación NIIF PYMES", td_style)
        ]
    ]
    t_firmas = Table(firmas_data, colWidths=[250, 254])
    t_firmas.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_firmas)

    # Construir PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Informe Financiero de Kevin Guerrero generado exitosamente: {OUTPUT_PDF}")

if __name__ == "__main__":
    build_pdf()

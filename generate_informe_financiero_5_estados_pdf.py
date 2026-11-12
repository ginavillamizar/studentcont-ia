#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Informe Financiero Oficial con los 5 Estados Financieros y Comparativos Mensuales
ELECTROVIVIENDA S.A.S — Aprendiz: Gina Villamizar • Instructor: George Olago (SENA CSET Bucaramanga)
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
OUTPUT_PDF = os.path.join(BASE_DIR, "INFORME_FINANCIERO_5_ESTADOS_ELECTROVIVIENDA_GINA_VILLAMIZAR.pdf")

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
            self.drawString(40, 30, "Aprendiz: Gina Villamizar • Instructor: George Olago • SENA CSET Bucaramanga — Ficha 123101")
            
            page_text = f"Página {self._pageNumber} de {page_count}"
            self.setFont("Helvetica-Bold", 7)
            self.setFillColor(colors.HexColor("#0B192C"))
            self.drawRightString(letter[0] - 40, 30, page_text)
            
        self.restoreState()

# Funciones generadoras de gráficos vectoriales
def create_chart_income_evolution():
    d = Drawing(504, 150)
    d.add(Rect(0, 0, 504, 150, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#CBD5E1"), strokeWidth=1, rx=6, ry=6))
    d.add(String(20, 132, "GRÁFICO 1: EVOLUCIÓN MENSUAL DE INGRESOS, COSTOS Y RESULTADO NETO (COP)", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.HexColor("#0B192C")))
    
    chart = VerticalBarChart()
    chart.x = 45
    chart.y = 25
    chart.height = 95
    chart.width = 430
    # Datos: 4 meses (Enero, Febrero, Marzo, Abril)
    # Serie 0: Ingresos Netos [0, 61.3M, 0, 8.16M]
    # Serie 1: Costo de Ventas [0, 41.64M, 0, 3.29M]
    # Serie 2: Utilidad/Pérdida Neta [0, 16.45M, -17.15M, -7.89M]
    chart.data = [
        [0, 61.3, 0, 8.16],
        [0, 41.64, 0, 3.29],
        [0, 16.45, -17.15, -7.89]
    ]
    chart.categoryAxis.categoryNames = ['Enero', 'Febrero', 'Marzo', 'Abril']
    chart.categoryAxis.labels.fontSize = 7.5
    chart.categoryAxis.labels.fontName = 'Helvetica-Bold'
    chart.valueAxis.valueMin = -20
    chart.valueAxis.valueMax = 70
    chart.valueAxis.valueStep = 15
    chart.valueAxis.labels.fontSize = 7
    chart.valueAxis.labelTextFormat = '$%dM'
    
    chart.bars[0].fillColor = colors.HexColor("#10B981")  # Verde ingresos
    chart.bars[1].fillColor = colors.HexColor("#D4AF37")  # Dorado costo
    chart.bars[2].fillColor = colors.HexColor("#0B192C")  # Azul marino resultado
    
    d.add(chart)
    
    # Leyenda
    d.add(Rect(140, 10, 10, 8, fillColor=colors.HexColor("#10B981"), strokeColor=None))
    d.add(String(155, 11, "Ingresos Netos", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#334155")))
    d.add(Rect(240, 10, 10, 8, fillColor=colors.HexColor("#D4AF37"), strokeColor=None))
    d.add(String(255, 11, "Costo de Ventas", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#334155")))
    d.add(Rect(340, 10, 10, 8, fillColor=colors.HexColor("#0B192C"), strokeColor=None))
    d.add(String(355, 11, "Utilidad / Pérdida Neta", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#334155")))
    
    return d

def create_chart_asset_composition():
    d = Drawing(504, 140)
    d.add(Rect(0, 0, 504, 140, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#CBD5E1"), strokeWidth=1, rx=6, ry=6))
    d.add(String(20, 122, "GRÁFICO 2: COMPOSICIÓN Y ESTRUCTURA DEL ACTIVO TOTAL AL CIERRE (ABRIL 2026)", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.HexColor("#0B192C")))
    
    pie = Pie()
    pie.x = 40
    pie.y = 15
    pie.width = 100
    pie.height = 100
    # Activos abril: Efectivo $51.8M (15.6%), Clientes $28.8M (8.7%), Inventario $33.8M (10.2%), Fijos $209.9M (63.4%), Otros $6.8M (2.1%)
    pie.data = [51.85, 28.86, 33.82, 209.89, 6.81]
    pie.labels = ['15.6%', '8.7%', '10.2%', '63.4%', '2.1%']
    pie.slices[0].fillColor = colors.HexColor("#10B981") # Efectivo
    pie.slices[1].fillColor = colors.HexColor("#3B82F6") # Cartera
    pie.slices[2].fillColor = colors.HexColor("#D4AF37") # Inventario
    pie.slices[3].fillColor = colors.HexColor("#0B192C") # Fijos
    pie.slices[4].fillColor = colors.HexColor("#94A3B8") # Otros
    d.add(pie)
    
    # Explicación lateral
    lines = [
        ("Efectivo y Equivalentes:", "$ 51.852.812 (15,6%) — Alta disponibilidad de caja para salarios y servicios.", colors.HexColor("#10B981")),
        ("Deudores Clientes (Cartera):", "$ 28.857.500 (8,7%) — Cartera sana a crédito comercial con soporte de factura.", colors.HexColor("#3B82F6")),
        ("Inventarios en Bodega:", "$ 33.822.000 (10,2%) — 4 referencias físicas valuadas por promedio ponderado.", colors.HexColor("#D4AF37")),
        ("Propiedades, Planta y Equipos:", "$ 209.890.152 (63,4%) — Sólido respaldo patrimonial en terrenos y edificaciones.", colors.HexColor("#0B192C")),
        ("Anticipos Tributarios y Otros:", "$ 6.810.220 (2,1%) — Saldos a favor y retenciones a favor en DIAN.", colors.HexColor("#94A3B8"))
    ]
    y_pos = 96
    for title, desc, col in lines:
        d.add(Rect(185, y_pos + 1, 8, 8, fillColor=col, strokeColor=None))
        d.add(String(198, y_pos + 1, title, fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor("#0B192C")))
        d.add(String(310, y_pos + 1, desc, fontName="Helvetica", fontSize=6.8, fillColor=colors.HexColor("#475569")))
        y_pos -= 19
        
    return d

def create_chart_liquidity_solvency():
    d = Drawing(504, 135)
    d.add(Rect(0, 0, 504, 135, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#CBD5E1"), strokeWidth=1, rx=6, ry=6))
    d.add(String(20, 118, "GRÁFICO 3: BATERÍA DE LIQUIDEZ Y SOLVENCIA COMPARATIVA (ENERO A ABRIL 2026)", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.HexColor("#0B192C")))
    
    chart = VerticalBarChart()
    chart.x = 45
    chart.y = 20
    chart.height = 85
    chart.width = 430
    # Razón corriente: Ene: Infinita (sin deuda), Feb: 2.15, Mar: 1.92, Abr: 2.25
    # Prueba ácida: Ene: Inf, Feb: 1.79, Mar: 1.56, Abr: 1.62
    # Endeudamiento: Ene: 0%, Feb: 31.2%, Mar: 32.7%, Abr: 27.4%
    chart.data = [
        [3.0, 2.15, 1.92, 2.25],
        [3.0, 1.79, 1.56, 1.62]
    ]
    chart.categoryAxis.categoryNames = ['Enero (Apertura)', 'Febrero', 'Marzo', 'Abril']
    chart.categoryAxis.labels.fontSize = 7.5
    chart.categoryAxis.labels.fontName = 'Helvetica-Bold'
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 3.5
    chart.valueAxis.valueStep = 0.5
    chart.valueAxis.labels.fontSize = 7
    chart.valueAxis.labelTextFormat = '%.1fx'
    
    chart.bars[0].fillColor = colors.HexColor("#0B192C") # Razón corriente
    chart.bars[1].fillColor = colors.HexColor("#10B981") # Prueba ácida
    d.add(chart)
    
    d.add(Rect(160, 6, 10, 8, fillColor=colors.HexColor("#0B192C"), strokeColor=None))
    d.add(String(175, 7, "Razón Corriente (Meta >= 1.5x)", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#334155")))
    d.add(Rect(320, 6, 10, 8, fillColor=colors.HexColor("#10B981"), strokeColor=None))
    d.add(String(335, 7, "Prueba Ácida (Meta >= 1.0x)", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#334155")))
    
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
    title_style = ParagraphStyle('TitleStyle', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=c_primary, alignment=1)
    sub_title_style = ParagraphStyle('SubTitleStyle', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=c_gold, alignment=1)
    meta_style = ParagraphStyle('MetaStyle', fontName='Helvetica', fontSize=8, leading=12, textColor=c_muted, alignment=1)
    
    sec_header_style = ParagraphStyle('SecHeader', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=c_primary, spaceBefore=6, spaceAfter=3, keepWithNext=True)
    subsec_header_style = ParagraphStyle('SubSecHeader', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=c_gold, spaceBefore=4, spaceAfter=2, keepWithNext=True)
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
    
    story.append(Paragraph("INFORME FINANCIERO OFICIAL DE LOS 5 ESTADOS Y COMPARATIVO MENSUAL", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("ESTADOS FINANCIEROS BAJO NIIF PARA LAS PYMES (GRUPO 2) • CUATRIMESTRE 2026", sub_title_style))
    story.append(Paragraph("Enero (Apertura) • Febrero (Operación Comercial) • Marzo (Causación y Nómina) • Abril (Consolidación y Cierre)", meta_style))
    story.append(Spacer(1, 12))
    
    # Cuadro institucional de autoría
    auth_data = [
        [Paragraph("<b>ENTIDAD REPORTANTE:</b>", td_bold), Paragraph("ELECTROVIVIENDA S.A.S — NIT: 901.765.438-3 • Bucaramanga, Santander", td_style)],
        [Paragraph("<b>RÉGIMEN Y MARCO:</b>", td_bold), Paragraph("Responsable de IVA (RRI) • Agente Retenedor y Autorretenedor • NIIF PYMES Grupo 2", td_style)],
        [Paragraph("<b>APRENDIZ / ELABORÓ:</b>", td_bold), Paragraph("<b>Gina Villamizar</b> — Aprendiz Gestora Contable y Financiera", td_style)],
        [Paragraph("<b>INSTRUCTOR / REVISÓ:</b>", td_bold), Paragraph("<b>George Olago</b> — Instructor Líder de Contabilidad y Finanzas SENA CSET", td_style)],
        [Paragraph("<b>FECHA DE PRESENTACIÓN:</b>", td_bold), Paragraph("12 de Noviembre de 2026 — Período Contable Auditado: Enero a Abril 2026", td_style)],
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

    # Presentación Institucional, Misión y Visión
    story.append(Paragraph("1. PRESENTACIÓN INSTITUCIONAL DE LA EMPRESA", sec_header_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=6, spaceBefore=0))
    p_pres = (
        "<b>ELECTROVIVIENDA S.A.S</b> es una sociedad comercial constituida por acciones simplificadas bajo las leyes de la República de Colombia, "
        "con domicilio principal en la ciudad de Bucaramanga, Santander. La compañía tiene por objeto social principal la adquisición, importación, "
        "distribución, representación y comercialización al por mayor y al detal de electrodomésticos para el hogar, tecnología, gasodomésticos "
        "y líneas de refrigeración y climatización. La sociedad opera bajo el régimen tributario de Responsable del Impuesto sobre las Ventas (IVA), "
        "actúa como agente retenedor de renta a título de compras y servicios, y aplica el marco técnico normativo de las <b>NIIF para las PYMES (Grupo 2)</b>."
    )
    story.append(Paragraph(p_pres, body_style))
    story.append(Spacer(1, 2))

    mv_data = [
        [
            Paragraph("<b>🎯 MISIÓN CORPORATIVA</b>", ParagraphStyle('MTitle', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=c_primary)),
            Paragraph("<b>🔭 VISIÓN ESTRATÉGICA (2026-2030)</b>", ParagraphStyle('VTitle', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=c_gold))
        ],
        [
            Paragraph(
                "Proveer soluciones integrales de confort y tecnología para los hogares y negocios santandereanos mediante la comercialización "
                "de electrodomésticos de la más alta eficiencia y durabilidad; garantizando asesoría técnica personalizada, facilidades comerciales, "
                "precios transparentes y estricto cumplimiento ético, tributario y de calidad, contribuyendo activamente al bienestar de las familias "
                "y a la estabilidad financiera de nuestros colaboradores y socios.",
                body_style
            ),
            Paragraph(
                "Consolidarnos para el año 2030 como la comercializadora líder de electrodomésticos y gasodomésticos en el nororiente colombiano, "
                "reconocida por su confiabilidad contable NIIF, excelencia en servicio posventa, adopción de canales de distribución digital omnicanal "
                "y un modelo de negocio sostenible que maximice la rentabilidad del patrimonio social respetando los más altos estándares éticos y legales.",
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
    story.append(Spacer(1, 3))

    story.append(Paragraph("2. VALORES CORPORATIVOS Y MARCO TÉCNICO APLICABLE", subsec_header_style))
    p_val = (
        "• <b>Transparencia y Fidelidad Contable:</b> Revelación objetiva y comprensible de hechos económicos conforme a NIIF para PYMES (Sección 3 a 8).<br/>"
        "• <b>Responsabilidad Fiscal y Social:</b> Estricto cumplimiento en retenciones, liquidación de nómina con todas las prestaciones legales e IVA bimestral.<br/>"
        "• <b>Negocio en Marcha y Solvencia:</b> Mantenimiento de una sólida base de capital y liquidez superior a 1,5 veces los pasivos a corto plazo."
    )
    story.append(Paragraph(p_val, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: SECCIÓN ENERO 2026 — APERTURA Y CONSTITUCIÓN (LOS 5 ESTADOS)
    # =========================================================================
    story.append(Paragraph("ESTADOS FINANCIEROS OFICIALES — MES DE ENERO 2026", sec_header_style))
    story.append(Paragraph("Período de Apertura y Constitución Social (01 al 31 de Enero de 2026) • Cifras en Pesos Colombianos (COP)", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=8, spaceBefore=2))

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
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,8), (-1,8), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,14), (-1,14), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_esf_ene)
    story.append(Spacer(1, 2))

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
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#FEE2E2")),
    ]))
    story.append(t_er_ene)
    story.append(Spacer(1, 2))

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
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_ecp_ene)
    story.append(Spacer(1, 2))

    story.append(Paragraph("ESTADO DE FLUJOS DE EFECTIVO — EFE ENERO 2026 (MÉTODO INDIRECTO)", subsec_header_style))
    efe_ene = [
        [Paragraph("<b>ACTIVIDAD DE FLUJO DE EFECTIVO</b>", th_style), Paragraph("<b>VALOR (COP)</b>", th_r_style)],
        [Paragraph("<b>Flujo de Efectivo de Actividades de Operación</b>", td_bold), Paragraph("$ 0", td_r_style)],
        [Paragraph("  Resultado Neto del Período", td_style), Paragraph("-$ 1.271.250", td_r_style)],
        [Paragraph("  Ajustes por partidas que no afectan efectivo: Depreciación del mes", td_style), Paragraph("+$ 1.271.250", td_r_style)],
        [Paragraph("  <b>Flujo Neto procedente de Actividades de Operación</b>", td_bold), Paragraph("<b>$ 0</b>", td_r_bold)],
        [Paragraph("<b>Flujo de Efectivo de Actividades de Inversión</b>", td_bold), Paragraph("$ 0", td_r_style)],
        [Paragraph("  (Los terrenos, edificios y camioneta fueron aportados directamente en especie)", td_style), Paragraph("<b>$ 0</b>", td_r_bold)],
        [Paragraph("<b>Flujo de Efectivo de Actividades de Financiación</b>", td_bold), Paragraph("$ 36.000.000", td_r_style)],
        [Paragraph("  Aportes de socios recibidos en efectivo en caja", td_style), Paragraph("+$ 36.000.000", td_r_style)],
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
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,12), (-1,12), colors.HexColor("#DCFCE7")),
    ]))
    story.append(t_efe_ene)
    story.append(Spacer(1, 2))

    story.append(Paragraph("ESTADO DE NOTAS Y REVELACIONES A LOS ESTADOS FINANCIEROS — NOTAS ENERO 2026", subsec_header_style))
    p_not_ene = (
        "<b>Nota 1. Entidad y Constitución:</b> Sociedad constituida el 01/01/2026 mediante documento privado registrado en Cámara de Comercio.<br/>"
        "<b>Nota 2. Políticas Contables:</b> Cumplimiento estricto de NIIF para PYMES. Medición al costo histórico y depreciación en línea recta.<br/>"
        "<b>Nota 3. Efectivo:</b> $36.000.000 corresponden a $21.000.000 aportados por el Socio 1 y $15.000.000 aportados por el Socio 2 en Caja.<br/>"
        "<b>Nota 4. Propiedades, Planta y Equipo:</b> Local ($51M) y Terrenos ($89,6M) aportados por socios, y Camioneta Chevrolet ($72M). Deprec. mes: $1.271.250.<br/>"
        "<b>Nota 5. Capital Social:</b> $248.600.000 suscrito y pagado en su totalidad, sin deudas financieras contraídas en el mes de constitución."
    )
    story.append(Paragraph(p_not_ene, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: SECCIÓN FEBRERO 2026 — COMPARATIVO ENERO VS FEBRERO (LOS 5 ESTADOS)
    # =========================================================================
    story.append(Paragraph("ESTADOS FINANCIEROS OFICIALES — MES DE FEBRERO 2026", sec_header_style))
    story.append(Paragraph("Inicio de Comercialización y Crédito Financiero • Comparativo Enero vs Febrero 2026", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=8, spaceBefore=2))

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
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,15), (-1,15), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_esf_feb)
    story.append(Spacer(1, 5))

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
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#DCFCE7")),
    ]))
    story.append(t_er_feb)
    story.append(Spacer(1, 5))

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
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#EEF2FF")),
    ]))
    story.append(t_ecp_feb)
    story.append(Spacer(1, 5))

    story.append(Paragraph("ESTADO DE FLUJOS DE EFECTIVO — EFE FEBRERO 2026 (MÉTODO INDIRECTO)", subsec_header_style))
    efe_feb = [
        [Paragraph("<b>CONCEPTO OPERATIVO Y FINANCIERO</b>", th_style), Paragraph("<b>VALOR (COP)</b>", th_r_style)],
        [Paragraph("<b>Utilidad Neta del Ejercicio (Punto de partida)</b>", td_bold), Paragraph("+$ 16.446.082", td_r_bold)],
        [Paragraph("  (+) Depreciación y amortizaciones del mes", td_style), Paragraph("+$ 1.120.467", td_r_style)],
        [Paragraph("  (-) Variación de Cuentas por Cobrar Clientes (Ventas a crédito pendientes)", td_style), Paragraph("-$ 28.857.500", td_r_style)],
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
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,11), (-1,11), colors.HexColor("#DCFCE7")),
    ]))
    story.append(t_efe_feb)
    story.append(Spacer(1, 5))

    story.append(Paragraph("ESTADO DE NOTAS Y REVELACIONES A LOS ESTADOS FINANCIEROS — NOTAS FEBRERO 2026", subsec_header_style))
    p_not_feb = (
        "<b>Nota 1. Despegue Comercial:</b> Se facturaron $61.300.000 con 32% de margen bruto. El 53% fue en efectivo y 47% a crédito comercial.<br/>"
        "<b>Nota 2. Financiamiento Bancario:</b> Desembolso de crédito de tesorería con Bancolombia por $39,66M amortizable a 36 meses.<br/>"
        "<b>Nota 3. Inventarios Físicos:</b> 12 neveras y 8 lavadoras adquiridas con factura a crédito; stock valorado al costo promedio por $29,16M.<br/>"
        "<b>Nota 4. Obligaciones Tributarias:</b> IVA generado por $11.647.000 compensado con IVA descontable en compras, dejando saldo a pagar de $3,8M."
    )
    story.append(Paragraph(p_not_feb, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: SECCIÓN MARZO 2026 — COMPARATIVO FEBRERO VS MARZO (LOS 5 ESTADOS)
    # =========================================================================
    story.append(Paragraph("ESTADOS FINANCIEROS OFICIALES — MES DE MARZO 2026", sec_header_style))
    story.append(Paragraph("Causación de Gastos Operativos y Pago de Nómina • Comparativo Febrero vs Marzo 2026", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=8, spaceBefore=2))

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
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,15), (-1,15), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_esf_mar)
    story.append(Spacer(1, 5))

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
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#FEE2E2")),
    ]))
    story.append(t_er_mar)
    story.append(Spacer(1, 5))

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
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t_ecp_mar)
    story.append(Spacer(1, 5))

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
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,9), (-1,9), colors.HexColor("#DCFCE7")),
    ]))
    story.append(t_efe_mar)
    story.append(Spacer(1, 5))

    story.append(Paragraph("ESTADO DE NOTAS Y REVELACIONES A LOS ESTADOS FINANCIEROS — NOTAS MARZO 2026", subsec_header_style))
    p_not_mar = (
        "<b>Nota 1. Causación Integral de Nómina:</b> Pago de sueldos al personal por $10.450.000 incluyendo auxilio de transporte, salud y pensión.<br/>"
        "<b>Nota 2. Estabilidad de Cartera e Inventarios:</b> Cartera se mantuvo en $28,85M e inventarios en $29,16M debido a compras recibidas en consignación.<br/>"
        "<b>Nota 3. Amortización de Deuda:</b> Se pagó la primera cuota del crédito bancario reduciendo el pasivo a largo plazo a $38,21M.<br/>"
        "<b>Nota 4. Respaldo de Liquidez:</b> A pesar de la pérdida operativa de $17,1M, la empresa cerró con $93,5M en bancos para cubrir abril."
    )
    story.append(Paragraph(p_not_mar, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: SECCIÓN ABRIL 2026 — COMPARATIVO MARZO VS ABRIL (LOS 5 ESTADOS)
    # =========================================================================
    story.append(Paragraph("ESTADOS FINANCIEROS OFICIALES — MES DE ABRIL 2026", sec_header_style))
    story.append(Paragraph("Reactivación Comercial y Cierre del Cuatrimestre • Comparativo Marzo vs Abril 2026", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=8, spaceBefore=2))

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
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,15), (-1,15), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_esf_abr)
    story.append(Spacer(1, 5))

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
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#FEF3C7")),
    ]))
    story.append(t_er_abr)
    story.append(Spacer(1, 5))

    story.append(Paragraph("ESTADO DE CAMBIOS EN EL PATRIMONIO — ECP ABRIL 2026", subsec_header_style))
    ecp_abr = [
        [Paragraph("<b>RUBRO PATRIMONIAL</b>", th_style), Paragraph("<b>SALDO 31 MAR</b>", th_r_style), Paragraph("<b>RESULTADO ABRIL</b>", th_r_style), Paragraph("<b>SALDO 30 ABR</b>", th_r_style)],
        [Paragraph("Capital Social Suscrito y Pagado (3105)", td_style), Paragraph("$ 248.600.000", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("$ 248.600.000", td_r_bold)],
        [Paragraph("Reserva Legal Obligatoria (3305)", td_style), Paragraph("$ 1.827.342", td_r_style), Paragraph("$ 0", td_r_style), Paragraph("$ 1.827.342", td_r_bold)],
        [Paragraph("Resultados del Ejercicio y Acumulados", td_style), Paragraph("-$ 1.979.744", td_r_style), Paragraph("-$ 7.887.158", td_r_style), Paragraph("-$ 9.866.902", td_r_bold)],
        [Paragraph("<b>TOTAL PATRIMONIO NETO</b>", td_bold), Paragraph("<b>$ 248.447.598</b>", td_r_bold), Paragraph("<b>-$ 7.887.158</b>", td_r_bold), Paragraph("<b>$ 240.560.440</b>", td_r_bold)],
    ]
    t_ecp_abr = Table(ecp_abr, colWidths=[204, 100, 100, 100])
    t_ecp_abr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t_ecp_abr)
    story.append(Spacer(1, 5))

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
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,9), (-1,9), colors.HexColor("#DCFCE7")),
    ]))
    story.append(t_efe_abr)
    story.append(Spacer(1, 5))

    story.append(Paragraph("ESTADO DE NOTAS Y REVELACIONES A LOS ESTADOS FINANCIEROS — NOTAS ABRIL 2026", subsec_header_style))
    p_not_abr = (
        "<b>Nota 1. Saneamiento de Pasivos:</b> La empresa amortizó $29,9M de deudas con proveedores, DIAN y bancos, mejorando el indicador de endeudamiento.<br/>"
        "<b>Nota 2. Eficiencia Comercial:</b> Margen bruto subió al 59,69% debido a ventas de referencias de alta rotación (Estufas y Smart TVs).<br/>"
        "<b>Nota 3. Inventario Disponible:</b> Cierre de inventario con $33,82M en 4 referencias listo para abastecer las ventas proyectadas de mayo.<br/>"
        "<b>Nota 4. Dictamen de Negocio en Marcha:</b> Razón corriente de 2,25x y patrimonio sólido de $240,5M garantizan operación ininterrumpida."
    )
    story.append(Paragraph(p_not_abr, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 6: ANÁLISIS FINANCIERO INTEGRAL CON BATERÍA DE GRÁFICOS
    # =========================================================================
    story.append(Paragraph("3. ANÁLISIS FINANCIERO INTEGRAL DE LA EMPRESA CON GRÁFICOS", sec_header_style))
    story.append(Paragraph("Diagnóstico Cuatrimestral de Liquidez, Rentabilidad, Solvencia y Gestión Operativa", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=8, spaceBefore=2))

    story.append(create_chart_income_evolution())
    story.append(Spacer(1, 3))

    p_ana_ing = (
        "<b>Análisis de la Dinámica de Ingresos y Utilidades:</b> Durante el primer cuatrimestre, ELECTROVIVIENDA S.A.S evidenció "
        "tres etapas bien diferenciadas: (1) <i>Enero</i> fue la fase de implantación societaria sin ingresos. (2) <i>Febrero</i> registró "
        "un fuerte despegue comercial con ventas de <b>$61,3M</b> y una utilidad neta de <b>$16,4M</b> (margen comercial del 32,07%). "
        "(3) <i>Marzo</i> atravesó un bache de ventas que generó una pérdida contable de <b>-$17,15M</b> al absorberse los costos fijos de nómina. "
        "Sin embargo, en <i>Abril</i> la empresa logró un repunte estratégico: con apenas <b>$8,15M</b> en ventas obtuvo un margen comercial récord "
        "del <b>59,69%</b>, reduciendo la pérdida operativa a <b>-$7,88M</b> y perfilando el punto de equilibrio operativo para el mes de mayo ($22M/mes)."
    )
    story.append(Paragraph(p_ana_ing, body_style))
    story.append(Spacer(1, 3))

    story.append(create_chart_asset_composition())
    story.append(Spacer(1, 3))

    p_ana_act = (
        "<b>Análisis de la Estructura de Activos y Solidez Patrimonial:</b> El <b>63,4%</b> de los activos está respaldado en propiedades, "
        "planta y equipo libre de gravámenes hipotecarios ($209,89M), lo que brinda una garantía sólida ante acreedores bancarios y proveedores. "
        "El activo corriente representa el <b>36,6%</b> restante ($121,34M), compuesto por una liquidez neta en caja y bancos de <b>$51,85M</b>, "
        "una cartera comercial vigente de <b>$28,85M</b> y un stock de inventarios en bodega de <b>$33,82M</b> valorado por promedio ponderado."
    )
    story.append(Paragraph(p_ana_act, body_style))
    story.append(Spacer(1, 3))

    story.append(create_chart_liquidity_solvency())
    story.append(Spacer(1, 3))

    p_ana_liq = (
        "<b>Análisis de Solvencia, Liquidez y Capacidad de Pago:</b> La <b>Razón Corriente</b> se ubicó al cierre de abril en <b>2,25x</b>, "
        "muy superior al estándar prudencial de 1,5x. Esto indica que por cada peso de deuda a corto plazo, ELECTROVIVIENDA S.A.S posee <b>$2,25</b> "
        "en activos líquidos para respaldarlo. Asimismo, la <b>Prueba Ácida</b> alcanzó <b>1,62x</b> (estándar >= 1,0x), demostrando que la empresa "
        "puede cancelar el 100% de sus pasivos de forma inmediata sin necesidad de vender un solo electrodoméstico de su inventario. "
        "El nivel de endeudamiento total se redujo del 32,7% en marzo al <b>27,37% en abril</b>, garantizando un perfil de riesgo sumamente bajo."
    )
    story.append(Paragraph(p_ana_liq, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 7: MATRIZ DE RATIOS, CONCLUSIONES Y FIRMAS OFICIALES
    # =========================================================================
    story.append(Paragraph("4. MATRIZ CUATRIMESTRAL DE INDICADORES FINANCIEROS CLAVE", sec_header_style))
    story.append(Paragraph("Evolución de Ratios de Liquidez, Endeudamiento, Actividad y Rentabilidad (2026)", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceAfter=8, spaceBefore=2))

    ratios_data = [
        [Paragraph("<b>INDICADOR FINANCIERO</b>", th_style), Paragraph("<b>FÓRMULA NIIF</b>", th_style), Paragraph("<b>ENERO</b>", th_r_style), Paragraph("<b>FEBRERO</b>", th_r_style), Paragraph("<b>MARZO</b>", th_r_style), Paragraph("<b>ABRIL</b>", th_r_style), Paragraph("<b>PARÁMETRO</b>", th_style)],
        [Paragraph("Razón Corriente", td_bold), Paragraph("Activo Cte / Pasivo Cte", td_style), Paragraph("Infinita", td_r_style), Paragraph("2,15 x", td_r_style), Paragraph("1,92 x", td_r_style), Paragraph("<b>2,25 x</b>", td_r_green), Paragraph("Óptimo (>= 1,5x)", td_style)],
        [Paragraph("Prueba Ácida", td_bold), Paragraph("(Activo Cte - Inv) / Pasivo Cte", td_style), Paragraph("Infinita", td_r_style), Paragraph("1,79 x", td_r_style), Paragraph("1,56 x", td_r_style), Paragraph("<b>1,62 x</b>", td_r_green), Paragraph("Excelente (>= 1,0x)", td_style)],
        [Paragraph("Capital de Trabajo Neto", td_bold), Paragraph("Activo Cte - Pasivo Cte", td_style), Paragraph("$ 36,0M", td_r_style), Paragraph("$ 92,8M", td_r_style), Paragraph("$ 75,5M", td_r_style), Paragraph("<b>$ 67,4M</b>", td_r_green), Paragraph("Superávit líquido", td_style)],
        [Paragraph("Nivel de Endeudamiento", td_bold), Paragraph("Pasivo Total / Activo Total", td_style), Paragraph("0,00 %", td_r_style), Paragraph("31,17 %", td_r_style), Paragraph("32,68 %", td_r_style), Paragraph("<b>27,37 %</b>", td_r_green), Paragraph("Bajo Riesgo (&lt;50%)", td_style)],
        [Paragraph("Apalancamiento Financiero", td_bold), Paragraph("Pasivo Total / Patrimonio", td_style), Paragraph("0,00 %", td_r_style), Paragraph("45,30 %", td_r_style), Paragraph("48,55 %", td_r_style), Paragraph("<b>37,69 %</b>", td_r_green), Paragraph("Controlado (&lt;100%)", td_style)],
        [Paragraph("Margen Bruto", td_bold), Paragraph("Utilidad Bruta / Ventas Netas", td_style), Paragraph("0,00 %", td_r_style), Paragraph("32,07 %", td_r_style), Paragraph("0,00 %", td_r_style), Paragraph("<b>59,69 %</b>", td_r_green), Paragraph("Expansión comercial", td_style)],
        [Paragraph("Margen Neto", td_bold), Paragraph("Utilidad Neta / Ventas Netas", td_style), Paragraph("0,00 %", td_r_style), Paragraph("26,83 %", td_r_style), Paragraph("N/A", td_r_style), Paragraph("<b>-96,69 %</b>", td_r_red), Paragraph("Recuperación activa", td_style)],
        [Paragraph("Rentabilidad Patrimonio (ROE)", td_bold), Paragraph("Utilidad Neta / Patrimonio", td_style), Paragraph("-0,51 %", td_r_style), Paragraph("+6,19 %", td_r_style), Paragraph("-6,90 %", td_r_style), Paragraph("<b>-3,28 %</b>", td_r_style), Paragraph("Meta anual: >12%", td_style)],
    ]
    t_rat = Table(ratios_data, colWidths=[114, 110, 50, 50, 50, 55, 75])
    t_rat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_rat)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5. CONCLUSIONES Y RECOMENDACIONES GERENCIALES", sec_header_style))
    p_concl = (
        "1. <b>Solvencia Blindada:</b> La compañía no afronta riesgo de quiebra ni cesación de pagos. Con un capital de trabajo neto de $67,4M "
        "y un respaldo patrimonial de $240,5M, tiene autonomía para operar holgadamente.<br/>"
        "2. <b>Estrategia de Ventas y Punto de Equilibrio:</b> Tras la reestructuración de gastos en abril (reducción de nómina a $9,25M y servicios a $3,5M), "
        "el nuevo punto de equilibrio se redujo a $22.000.000 mensuales con el margen bruto del 59%. Se recomienda enfocar los esfuerzos en la rotación de neveras y smart TVs.<br/>"
        "3. <b>Recuperación de Cartera:</b> La cartera de clientes por $28.857.500 debe gestionarse con acuerdos de pago a 30 días para inyectar recursos frescos a bancos.<br/>"
        "4. <b>Certificación de Negocio en Marcha:</b> Conforme a la Sección 3 de las NIIF para PYMES, se dictamina que ELECTROVIVIENDA S.A.S cumple a cabalidad "
        "la hipótesis de negocio en marcha durante los próximos 12 meses."
    )
    story.append(Paragraph(p_concl, body_style))
    story.append(Spacer(1, 18))

    story.append(Paragraph("6. CERTIFICACIÓN PERICIAL Y FIRMAS DE AUTORIDADES", sec_header_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_gold, spaceAfter=20, spaceBefore=2))

    firmas_data = [
        [
            Paragraph("________________________________________<br/><b>GINA VILLAMIZAR</b><br/>Aprendiz en Gestión Contable y Financiera<br/>Elaboró • Ficha 123101 SENA CSET", td_style),
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
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_firmas)

    # Construir PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Informe Financiero de los 5 Estados generado exitosamente: {OUTPUT_PDF}")

if __name__ == "__main__":
    build_pdf()

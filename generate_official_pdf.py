import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

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
        if self._pageNumber == 1:
            return  # No headers or footers on cover
        
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0A2540"))
        
        # Header
        self.drawString(54, 750, "ELECTROVIVIENDA S.A.S  |  NIT 901.765.438-3")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(612 - 54, 750, "INFORME EMPRESARIAL CONSOLIDADO NIIF 2026")
        
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 742, 612 - 54, 742)
        
        # Footer
        self.line(54, 45, 612 - 54, 45)
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#D97706"))
        self.drawString(54, 32, "SENA Centro de Servicios Empresariales y Turísticos de Bucaramanga")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(612 - 54, 32, f"Página {self._pageNumber} de {page_count}")
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    primary = colors.HexColor("#0A2540")
    gold = colors.HexColor("#D97706")
    slate = colors.HexColor("#334155")
    
    styles.add(ParagraphStyle(
        'CoverInstitution',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=gold,
        alignment=1,
        spaceAfter=6
    ))
    
    styles.add(ParagraphStyle(
        'CoverCenterText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=slate,
        alignment=1,
        spaceAfter=15
    ))
    
    styles.add(ParagraphStyle(
        'CoverTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=19,
        leading=24,
        textColor=primary,
        alignment=1,
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=16,
        textColor=gold,
        alignment=1,
        spaceAfter=25
    ))
    
    styles.add(ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=primary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'SubSectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=gold,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.8,
        textColor=slate,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=primary
    ))

    styles.add(ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.2,
        textColor=slate
    ))

    styles.add(ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9.2,
        textColor=primary
    ))

    styles.add(ParagraphStyle(
        'TableCellRight',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.2,
        textColor=slate,
        alignment=2
    ))

    styles.add(ParagraphStyle(
        'TableCellRightBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9.2,
        textColor=primary,
        alignment=2
    ))

    story = []

    # =========================================================================
    # PÁGINA 1: PORTADA OFICIAL ACADÉMICO - EMPRESARIAL
    # =========================================================================
    story.append(Spacer(1, 35))
    story.append(Paragraph("SERVICIO NACIONAL DE APRENDIZAJE — SENA", styles['CoverInstitution']))
    story.append(Paragraph("CENTRO DE SERVICIOS EMPRESARIALES Y TURÍSTICOS — BUCARAMANGA<br/>TECNÓLOGO EN GESTIÓN CONTABLE Y DE INFORMACIÓN FINANCIERA", styles['CoverCenterText']))
    
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="60%", thickness=2, color=gold, spaceAfter=25, spaceBefore=0))
    
    story.append(Paragraph("INFORME EMPRESARIAL Y AUDITORÍA DE LOS 5 ESTADOS FINANCIEROS CONSOLIDADOS NIIF", styles['CoverTitle']))
    story.append(Paragraph("EVALUACIÓN PERICIAL INTEGRAL DE 4 PERÍODOS (ENERO - ABRIL 2026)", styles['CoverSubtitle']))
    
    story.append(Paragraph("ENTIDAD AUDITADA:<br/><b>ELECTROVIVIENDA S.A.S</b><br/>NIT: 901.765.438-3<br/><i>«Calidad y energía para tu hogar»</i>", styles['CoverCenterText']))
    
    story.append(HRFlowable(width="60%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=28, spaceBefore=10))
    
    meta_data = [
        [Paragraph("<b>Autora / Investigadora Principal:</b>", styles['TableCellBold']), Paragraph("<b>Gina Villamizar</b> — Contadora Titular (T.P. 248960-T)", styles['TableCell'])],
        [Paragraph("<b>Instructor Académico:</b>", styles['TableCellBold']), Paragraph("<b>George Olago</b>", styles['TableCell'])],
        [Paragraph("<b>Representante Legal:</b>", styles['TableCellBold']), Paragraph("<b>Kevin Guerrero</b> (C.C. 1.098.765.432)", styles['TableCell'])],
        [Paragraph("<b>Revisora Fiscal Colegiada:</b>", styles['TableCellBold']), Paragraph("<b>Marcela Gonzales</b> (T.P. 194820-T)", styles['TableCell'])],
        [Paragraph("<b>Plataforma &amp; Ecosistema:</b>", styles['TableCellBold']), Paragraph("STUDENTCONT.IA — Entorno Tecnológico Contable", styles['TableCell'])],
        [Paragraph("<b>Lugar y Fecha:</b>", styles['TableCellBold']), Paragraph("Bucaramanga, Santander — Año 2026", styles['TableCell'])],
    ]
    t_meta = Table(meta_data, colWidths=[160, 320])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_meta)
    
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: TABLA DE CONTENIDO GENERAL
    # =========================================================================
    story.append(Paragraph("TABLA DE CONTENIDO GENERAL", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=gold, spaceAfter=14, spaceBefore=2))
    
    toc_data = [
        [Paragraph("<b>SECCIÓN</b>", styles['TableCellBold']), Paragraph("<b>CONTENIDO TEMÁTICO DETALLADO</b>", styles['TableCellBold']), Paragraph("<b>PÁG.</b>", styles['TableCellRightBold'])],
        [Paragraph("<b>1</b>", styles['TableCellBold']), Paragraph("Presentación Institucional de ELECTROVIVIENDA S.A.S (Misión, Visión, Valores)", styles['TableCell']), Paragraph("3", styles['TableCellRight'])],
        [Paragraph("<b>2</b>", styles['TableCellBold']), Paragraph("Objetivos del Análisis Financiero (General y Específicos)", styles['TableCell']), Paragraph("3", styles['TableCellRight'])],
        [Paragraph("<b>3</b>", styles['TableCellBold']), Paragraph("Guía Pedagógica: ¿Cómo interpretar la contabilidad sin tecnicismos?", styles['TableCell']), Paragraph("3", styles['TableCellRight'])],
        [Paragraph("<b>4</b>", styles['TableCellBold']), Paragraph("<b>Juego Completo de los 5 Estados Financieros NIIF Consolidados:</b>", styles['TableCellBold']), Paragraph("4-7", styles['TableCellRightBold'])],
        [Paragraph("  4.1", styles['TableCell']), Paragraph("• Estado de Situación Financiera (ESF / Balance General Consolidado)", styles['TableCell']), Paragraph("4", styles['TableCellRight'])],
        [Paragraph("  4.2", styles['TableCell']), Paragraph("• Estado de Resultados Integral (ERI / ER Consolidado)", styles['TableCell']), Paragraph("4", styles['TableCellRight'])],
        [Paragraph("  4.3", styles['TableCell']), Paragraph("• Explicación Detallada del ESF y ER (Crónica Económica y Regla 12 Meses)", styles['TableCell']), Paragraph("5", styles['TableCellRight'])],
        [Paragraph("  4.4", styles['TableCell']), Paragraph("• Estado de Cambios en el Patrimonio (ECP Consolidado)", styles['TableCell']), Paragraph("6", styles['TableCellRight'])],
        [Paragraph("  4.5", styles['TableCell']), Paragraph("• Estado de Flujos de Efectivo (EFE Consolidado)", styles['TableCell']), Paragraph("6", styles['TableCellRight'])],
        [Paragraph("  4.6", styles['TableCell']), Paragraph("• Estado de Notas y Revelaciones a los Estados Financieros (Notas 1 a 9)", styles['TableCell']), Paragraph("7", styles['TableCellRight'])],
        [Paragraph("<b>5</b>", styles['TableCellBold']), Paragraph("Estudio Pericial de Negocio en Marcha y Proyección de Supervivencia (Runway)", styles['TableCell']), Paragraph("8", styles['TableCellRight'])],
        [Paragraph("<b>6</b>", styles['TableCellBold']), Paragraph("Matriz Completa de Indicadores Financieros NIIF: Fórmulas y Paso a Paso", styles['TableCell']), Paragraph("9", styles['TableCellRight'])],
        [Paragraph("<b>7</b>", styles['TableCellBold']), Paragraph("Diagnóstico Estratégico, Punto de Equilibrio y Hoja de Ruta para Mayo", styles['TableCell']), Paragraph("10", styles['TableCellRight'])],
        [Paragraph("<b>8</b>", styles['TableCellBold']), Paragraph("Dictamen Pericial y Certificación Oficial de Firmas", styles['TableCell']), Paragraph("10", styles['TableCellRight'])],
    ]
    t_toc = Table(toc_data, colWidths=[35, 425, 44])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A2540")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_toc)
    
    story.append(Spacer(1, 20))
    
    decl_p = Paragraph(
        "<b>DECLARACIÓN DE INTEGRIDAD TÉCNICA (NIC 1 / SECCIÓN 3 NIIF PYMES):</b> El presente informe consolida fidedignamente "
        "el juego completo de los <b>cinco (5) estados financieros</b> exigidos por los marcos técnicos contables oficiales colombianos "
        "(Decreto 2420/2015). Cumple cabalmente con las pautas del Centro de Servicios Empresariales y Turísticos del SENA Bucaramanga "
        "bajo la tutoría del instructor <b>George Olago</b>.", styles['CalloutText']
    )
    t_decl = Table([[decl_p]], colWidths=[504])
    t_decl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#F59E0B")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_decl)
    
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: PRESENTACIÓN INSTITUCIONAL, OBJETIVOS Y GUÍA PEDAGÓGICA
    # =========================================================================
    story.append(Paragraph("1. PRESENTACIÓN INSTITUCIONAL DE ELECTROVIVIENDA S.A.S", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=6, spaceBefore=0))
    
    story.append(Paragraph(
        "<b>ELECTROVIVIENDA S.A.S</b> (NIT: 901.765.438-3) es una sociedad por acciones simplificada domiciliada en "
        "Bucaramanga, Santander, legalmente constituida en enero de 2026. Se dedica al comercio al por menor y mayor de "
        "electrodomésticos, tecnología, gasodomésticos y soluciones energéticas eficientes para el hogar colombiano. "
        "Su lema distintivo es: <i>«Calidad y energía para tu hogar»</i>.", styles['BodyCustom']
    ))
    
    pres_cards = [
        [Paragraph("<b>MISIÓN CORPORATIVA</b>", styles['TableCellBold']), Paragraph("<b>VISIÓN ESTRATÉGICA 2028</b>", styles['TableCellBold']), Paragraph("<b>VALORES INSTITUCIONALES</b>", styles['TableCellBold'])],
        [
            Paragraph("Brindar bienestar a las familias colombianas facilitando el acceso a electrodomésticos duraderos, eficientes y con facilidades de financiación justa.", styles['TableCell']),
            Paragraph("Consolidarse como la distribuidora de electrodomésticos líder de Santander, reconocida por su servicio posventa, responsabilidad e innovación.", styles['TableCell']),
            Paragraph("• Transparencia contable<br/>• Calidad de servicio<br/>• Responsabilidad fiscal<br/>• Innovación tecnológica", styles['TableCell'])
        ]
    ]
    t_pres = Table(pres_cards, colWidths=[168, 168, 168])
    t_pres.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A2540")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_pres)
    
    story.append(Spacer(1, 8))
    story.append(Paragraph("2. OBJETIVOS DEL ANÁLISIS FINANCIERO", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=6, spaceBefore=0))
    
    story.append(Paragraph(
        "<b>OBJETIVO GENERAL:</b> Evaluar de forma integral, pedagógica y rigurosa la salud patrimonial, la solvencia, "
        "el nivel de endeudamiento a corto y largo plazo, y la viabilidad del principio de negocio en marcha de ELECTROVIVIENDA S.A.S "
        "a través de los cinco (5) estados financieros oficiales durante el primer cuatrimestre del año 2026 (Enero a Abril).",
        styles['BodyCustom']
    ))
    
    story.append(Spacer(1, 6))
    story.append(Paragraph("3. GUÍA PEDAGÓGICA: ¿CÓMO ENTENDER LA CONTABILIDAD SIN SER CONTADOR?", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=6, spaceBefore=0))
    
    metafora_data = [
        [Paragraph("<b>Concepto Contable</b>", styles['TableCellBold']), Paragraph("<b>Analogía de la Vida Cotidiana</b>", styles['TableCellBold']), Paragraph("<b>Cifra en ELECTROVIVIENDA (Abril 2026)</b>", styles['TableCellBold'])],
        [Paragraph("<b>1. Activo Total</b><br/>(Lo que se tiene)", styles['TableCell']), Paragraph("Es todo lo que hay en casa: dinero en billetera y bancos, televisores y neveras en exhibición, mostradores y cuentas por cobrar.", styles['TableCell']), Paragraph("<b>$ 331.232.683</b><br/>(Propiedades, caja e inventario)", styles['TableCell'])],
        [Paragraph("<b>2. Pasivo Total</b><br/>(Lo que se debe)", styles['TableCell']), Paragraph("Son los fiados, recibos pendientes, deudas con proveedores a pagar antes de 1 año y créditos bancarios a largo plazo.", styles['TableCell']), Paragraph("<b>$ 90.672.243</b><br/>(Deudas totales controladas)", styles['TableCell'])],
        [Paragraph("<b>3. Patrimonio Neto</b><br/>(Lo propio y real)", styles['TableCell']), Paragraph("Si vendiéramos todo hoy y pagáramos todas las deudas, esto es lo que le queda 100% libre a los socios en el bolsillo.", styles['TableCell']), Paragraph("<b>$ 240.560.440</b><br/>(72,6% del negocio es propio)", styles['TableCell'])],
        [Paragraph("<b>4. Razón Corriente</b><br/>(Escudo protector)", styles['TableCell']), Paragraph("Por cada $1 peso de recibos o deudas que vencen ya, cuántos pesos tenemos guardados en la alacena y en caja para responder.", styles['TableCell']), Paragraph("<b>2,25 veces</b><br/>(Tenemos $2,25 por cada $1 debido)", styles['TableCell'])],
    ]
    t_met = Table(metafora_data, colWidths=[114, 240, 150])
    t_met.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A2540")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_met)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: ESTADOS 1 Y 2: ESF (BALANCE) Y ESTADO DE RESULTADOS CONSOLIDADOS
    # =========================================================================
    story.append(Paragraph("4.1. ESTADO DE SITUACIÓN FINANCIERA (ESF / BALANCE GENERAL CONSOLIDADO)", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=5, spaceBefore=0))
    
    esf_data = [
        [Paragraph("<b>Cuentas del Balance General (COP)</b>", styles['TableCellBold']), Paragraph("<b>Enero</b>", styles['TableCellRightBold']), Paragraph("<b>Febrero</b>", styles['TableCellRightBold']), Paragraph("<b>Marzo</b>", styles['TableCellRightBold']), Paragraph("<b>Abril</b>", styles['TableCellRightBold'])],
        [Paragraph("<b>Activo Corriente</b> (Caja, Bancos, Clientes, Inventarios)", styles['TableCell']), Paragraph("$ 36.000.000", styles['TableCellRight']), Paragraph("$ 173.342.532", styles['TableCellRight']), Paragraph("$ 157.342.532", styles['TableCellRight']), Paragraph("<b>$ 121.342.532</b>", styles['TableCellRightBold'])],
        [Paragraph("• Efectivo y Equivalentes (Caja y Bancos)", styles['TableCell']), Paragraph("$ 36.000.000", styles['TableCellRight']), Paragraph("$ 88.542.532", styles['TableCellRight']), Paragraph("$ 52.342.532", styles['TableCellRight']), Paragraph("$ 42.542.532", styles['TableCellRight'])],
        [Paragraph("• Deudores Comerciales (Clientes por cobrar)", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 49.600.000", styles['TableCellRight']), Paragraph("$ 47.000.000", styles['TableCellRight']), Paragraph("$ 23.600.000", styles['TableCellRight'])],
        [Paragraph("• Inventarios (Electrodomésticos en bodega)", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 35.200.000", styles['TableCellRight']), Paragraph("$ 58.000.000", styles['TableCellRight']), Paragraph("$ 43.200.000", styles['TableCellRight'])],
        [Paragraph("• Otros Activos Corrientes (Anticipos)", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 12.000.000", styles['TableCellRight'])],
        [Paragraph("<b>Activo No Corriente</b> (Propiedades, Planta y Equipos)", styles['TableCell']), Paragraph("$ 204.000.000", styles['TableCellRight']), Paragraph("$ 213.711.877", styles['TableCellRight']), Paragraph("$ 212.557.300", styles['TableCellRight']), Paragraph("<b>$ 209.890.151</b>", styles['TableCellRightBold'])],
        [Paragraph("<b>TOTAL ACTIVO</b>", styles['TableCellBold']), Paragraph("<b>$ 240.000.000</b>", styles['TableCellRightBold']), Paragraph("<b>$ 387.054.409</b>", styles['TableCellRightBold']), Paragraph("<b>$ 369.899.832</b>", styles['TableCellRightBold']), Paragraph("<b>$ 331.232.683</b>", styles['TableCellRightBold'])],
        
        [Paragraph("<b>Pasivo Corriente</b> (Vencimiento &lt; 12 meses)", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 80.526.937", styles['TableCellRight']), Paragraph("$ 81.852.819", styles['TableCellRight']), Paragraph("<b>$ 53.927.428</b>", styles['TableCellRightBold'])],
        [Paragraph("<b>Pasivo No Corriente</b> (Vencimiento &gt; 12 meses)", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 39.600.000", styles['TableCellRight']), Paragraph("$ 39.000.000", styles['TableCellRight']), Paragraph("<b>$ 36.744.815</b>", styles['TableCellRightBold'])],
        [Paragraph("<b>TOTAL PASIVO</b>", styles['TableCellBold']), Paragraph("<b>$ 0</b>", styles['TableCellRightBold']), Paragraph("<b>$ 120.126.937</b>", styles['TableCellRightBold']), Paragraph("<b>$ 120.852.819</b>", styles['TableCellRightBold']), Paragraph("<b>$ 90.672.243</b>", styles['TableCellRightBold'])],
        
        [Paragraph("<b>Patrimonio Neto</b> (Capital Social y Resultados)", styles['TableCellBold']), Paragraph("<b>$ 240.000.000</b>", styles['TableCellRightBold']), Paragraph("<b>$ 266.927.472</b>", styles['TableCellRightBold']), Paragraph("<b>$ 249.047.013</b>", styles['TableCellRightBold']), Paragraph("<b>$ 240.560.440</b>", styles['TableCellRightBold'])],
        [Paragraph("• Capital Social Aportado", styles['TableCell']), Paragraph("$ 240.000.000", styles['TableCellRight']), Paragraph("$ 240.000.000", styles['TableCellRight']), Paragraph("$ 240.000.000", styles['TableCellRight']), Paragraph("$ 240.000.000", styles['TableCellRight'])],
        [Paragraph("• Resultados Acumulados y del Ejercicio", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("+$ 26.927.472", styles['TableCellRight']), Paragraph("+$ 9.047.013", styles['TableCellRight']), Paragraph("+$ 560.440", styles['TableCellRight'])],
    ]
    t_esf = Table(esf_data, colWidths=[204, 75, 75, 75, 75])
    t_esf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A2540")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor("#EEF2FF")),
        ('BACKGROUND', (0,10), (-1,10), colors.HexColor("#EEF2FF")),
        ('BACKGROUND', (0,11), (-1,11), colors.HexColor("#FEF3C7")),
    ]))
    story.append(t_esf)

    story.append(Spacer(1, 6))
    story.append(Paragraph("4.2. ESTADO DE RESULTADOS INTEGRAL (ERI / ER CONSOLIDADO)", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=5, spaceBefore=0))
    
    er_data = [
        [Paragraph("<b>Renglón del Estado de Resultados (COP)</b>", styles['TableCellBold']), Paragraph("<b>Enero</b>", styles['TableCellRightBold']), Paragraph("<b>Febrero</b>", styles['TableCellRightBold']), Paragraph("<b>Marzo</b>", styles['TableCellRightBold']), Paragraph("<b>Abril</b>", styles['TableCellRightBold'])],
        [Paragraph("<b>Ingresos Operacionales (Ventas Netas)</b>", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 61.300.000", styles['TableCellRight']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("<b>$ 8.156.500</b>", styles['TableCellRightBold'])],
        [Paragraph("<b>Costo de Ventas (Mercancía)</b>", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 41.640.000", styles['TableCellRight']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 3.288.000", styles['TableCellRight'])],
        [Paragraph("<b>Utilidad Bruta en Ventas</b>", styles['TableCellBold']), Paragraph("$ 0", styles['TableCellRightBold']), Paragraph("<b>$ 19.660.000</b>", styles['TableCellRightBold']), Paragraph("$ 0", styles['TableCellRightBold']), Paragraph("<b>$ 4.868.500</b>", styles['TableCellRightBold'])],
        [Paragraph("• Margen Bruto Comercial (%)", styles['TableCell']), Paragraph("0,00 %", styles['TableCellRight']), Paragraph("32,07 %", styles['TableCellRight']), Paragraph("N/A", styles['TableCellRight']), Paragraph("<b>59,69 %</b>", styles['TableCellRightBold'])],
        [Paragraph("<b>Gastos Operacionales (Administración y Ventas)</b>", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 3.213.918", styles['TableCellRight']), Paragraph("$ 17.154.577", styles['TableCellRight']), Paragraph("$ 12.755.658", styles['TableCellRight'])],
        [Paragraph("• Gastos de Personal (Nómina)", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 2.450.000", styles['TableCellRight']), Paragraph("$ 10.450.000", styles['TableCellRight']), Paragraph("$ 9.250.000", styles['TableCellRight'])],
        [Paragraph("• Arriendos, Servicios y Tributos", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 763.918", styles['TableCellRight']), Paragraph("$ 6.704.577", styles['TableCellRight']), Paragraph("$ 3.505.658", styles['TableCellRight'])],
        [Paragraph("<b>RESULTADO NETO DEL EJERCICIO</b>", styles['TableCellBold']), Paragraph("<b>$ 0</b>", styles['TableCellRightBold']), Paragraph("<font color='#059669'><b>+$ 16.446.082</b></font>", styles['TableCellRightBold']), Paragraph("<font color='#DC2626'><b>-$ 17.154.577</b></font>", styles['TableCellRightBold']), Paragraph("<font color='#DC2626'><b>-$ 7.887.158</b></font>", styles['TableCellRightBold'])],
    ]
    t_er = Table(er_data, colWidths=[204, 75, 75, 75, 75])
    t_er.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A2540")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#EEF2FF")),
        ('BACKGROUND', (0,8), (-1,8), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t_er)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: EXPLICACIÓN DETALLADA DEL ESF Y ER (CRÓNICA Y REGLA 12 MESES)
    # =========================================================================
    story.append(Paragraph("4.3. EXPLICACIÓN DETALLADA DEL BALANCE GENERAL Y ESTADO DE RESULTADOS", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=6, spaceBefore=0))
    
    story.append(Paragraph(
        "A continuación se presenta el análisis económico mes a mes que explica cómo interactúan los ingresos, costos y deudas:",
        styles['BodyCustom']
    ))
    
    expl_data = [
        [
            Paragraph("<b>Período</b>", styles['TableCellBold']),
            Paragraph("<b>Hecho Económico Principal</b>", styles['TableCellBold']),
            Paragraph("<b>Impacto en el Balance y Estado de Resultados</b>", styles['TableCellBold']),
            Paragraph("<b>Interpretación Gerencial</b>", styles['TableCellBold'])
        ],
        [
            Paragraph("<b>ENERO 2026</b><br/><font color='#64748B'>Constitución</font>", styles['TableCellBold']),
            Paragraph("Aporte de capital de socios fundadores por <b>$240.000.000</b>.", styles['TableCell']),
            Paragraph("Activo = $240M ($36M efectivo + $204M inmuebles/locales). Pasivo = $0. Ventas = $0.", styles['TableCell']),
            Paragraph("Nacimiento con cero deudas, solvencia plena y patrimonio 100% propio.", styles['TableCell'])
        ],
        [
            Paragraph("<b>FEBRERO 2026</b><br/><font color='#64748B'>Apertura Comercial</font>", styles['TableCellBold']),
            Paragraph("Ventas masivas de electrodomésticos por <b>$61.300.000</b>.", styles['TableCell']),
            Paragraph("Margen bruto de 32,07%. Se generó utilidad neta récord de <b>+$16.446.082</b>. La cartera creció a $49,6M y caja a $88,5M.", styles['TableCell']),
            Paragraph("Validación comercial del modelo: alta demanda y rápido retorno sobre la inversión.", styles['TableCell'])
        ],
        [
            Paragraph("<b>MARZO 2026</b><br/><font color='#64748B'>Aprovisionamiento</font>", styles['TableCellBold']),
            Paragraph("Recepción de gran lote de mercancía ($58M en kardex) y preparación operativa.", styles['TableCell']),
            Paragraph("Sin ventas registradas en el mes. Se pagaron nóminas, arriendos e impuestos por $17.154.577, generando pérdida de -$17,15M.", styles['TableCell']),
            Paragraph("Pérdida operativa planeada: se mantuvieron los costos fijos mientras se llenaba la bodega.", styles['TableCell'])
        ],
        [
            Paragraph("<b>ABRIL 2026</b><br/><font color='#64748B'>Reactivación y Pago Deuda</font>", styles['TableCellBold']),
            Paragraph("Ventas de <b>$8.156.500</b> con margen récord de <b>59,69%</b> y amortización masiva de deudas.", styles['TableCell']),
            Paragraph("El pasivo se redujo en más de $30 millones (de $120,8M a $90,6M). La pérdida del mes bajó a -$7,88M (reducción del 54%).", styles['TableCell']),
            Paragraph("<b>Saneamiento agresivo:</b> La empresa priorizó pagar proveedores y reducir pasivos, blindando la liquidez.", styles['TableCell'])
        ],
    ]
    t_expl = Table(expl_data, colWidths=[80, 134, 150, 140])
    t_expl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A2540")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#ECFDF5")),
    ]))
    story.append(t_expl)
    
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>LA REGLA NIIF DE LOS 12 MESES EN EL PASIVO:</b>", styles['SubSectionHeader']))
    story.append(Paragraph(
        "Bajo NIIF para PYMES, el <b>Pasivo Corriente</b> agrupa únicamente obligaciones a pagar en <b>menos de 12 meses</b>. "
        "Las deudas pactadas a más de 12 meses son <b>Pasivo No Corriente</b>. En ELECTROVIVIENDA, la deuda a corto plazo "
        "en abril es de solo <b>$53.927.428 (16,28% del activo)</b> y está cubierta 2,25 veces con los activos corrientes.",
        styles['BodyCustom']
    ))
    
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 6: ESTADOS 3 Y 4: ECP (PATRIMONIO) Y EFE (FLUJO DE EFECTIVO)
    # =========================================================================
    story.append(Paragraph("4.4. ESTADO DE CAMBIOS EN EL PATRIMONIO (ECP CONSOLIDADO)", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=5, spaceBefore=0))
    
    ecp_data = [
        [Paragraph("<b>Concepto Patrimonial (COP)</b>", styles['TableCellBold']), Paragraph("<b>Capital Social</b>", styles['TableCellRightBold']), Paragraph("<b>Resultados Acumulados</b>", styles['TableCellRightBold']), Paragraph("<b>Resultado del Ejercicio</b>", styles['TableCellRightBold']), Paragraph("<b>TOTAL PATRIMONIO</b>", styles['TableCellRightBold'])],
        [Paragraph("<b>Saldo al 1 de Enero de 2026</b>", styles['TableCellBold']), Paragraph("$ 240.000.000", styles['TableCellRight']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("<b>$ 240.000.000</b>", styles['TableCellRightBold'])],
        [Paragraph("Movimiento Neto Febrero (Utilidad del mes)", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("+$ 16.446.082", styles['TableCellRight']), Paragraph("+$ 16.446.082", styles['TableCellRight'])],
        [Paragraph("<b>Saldo al 28 de Febrero de 2026</b>", styles['TableCellBold']), Paragraph("$ 240.000.000", styles['TableCellRight']), Paragraph("+$ 10.481.390", styles['TableCellRight']), Paragraph("+$ 16.446.082", styles['TableCellRight']), Paragraph("<b>$ 266.927.472</b>", styles['TableCellRightBold'])],
        [Paragraph("Movimiento Neto Marzo (Pérdida del mes)", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("+$ 26.201.590", styles['TableCellRight']), Paragraph("-$ 17.154.577", styles['TableCellRight']), Paragraph("-$ 17.154.577", styles['TableCellRight'])],
        [Paragraph("<b>Saldo al 31 de Marzo de 2026</b>", styles['TableCellBold']), Paragraph("$ 240.000.000", styles['TableCellRight']), Paragraph("+$ 26.201.590", styles['TableCellRight']), Paragraph("-$ 17.154.577", styles['TableCellRight']), Paragraph("<b>$ 249.047.013</b>", styles['TableCellRightBold'])],
        [Paragraph("Movimiento Neto Abril (Pérdida reducida)", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("+$ 8.447.598", styles['TableCellRight']), Paragraph("-$ 7.887.158", styles['TableCellRight']), Paragraph("-$ 7.887.158", styles['TableCellRight'])],
        [Paragraph("<b>SALDO FINAL AL 30 DE ABRIL DE 2026</b>", styles['TableCellBold']), Paragraph("<b>$ 240.000.000</b>", styles['TableCellRightBold']), Paragraph("<b>+$ 8.447.598</b>", styles['TableCellRightBold']), Paragraph("<b>-$ 7.887.158</b>", styles['TableCellRightBold']), Paragraph("<b>$ 240.560.440</b>", styles['TableCellRightBold'])],
    ]
    t_ecp = Table(ecp_data, colWidths=[164, 85, 85, 85, 85])
    t_ecp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A2540")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor("#FEF3C7")),
    ]))
    story.append(t_ecp)

    story.append(Spacer(1, 6))
    story.append(Paragraph("4.5. ESTADO DE FLUJOS DE EFECTIVO (EFE CONSOLIDADO - MÉTODO DIRECTO/INDIRECTO)", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=5, spaceBefore=0))
    
    efe_data = [
        [Paragraph("<b>Actividades de Flujo de Fondos (COP)</b>", styles['TableCellBold']), Paragraph("<b>Enero</b>", styles['TableCellRightBold']), Paragraph("<b>Febrero</b>", styles['TableCellRightBold']), Paragraph("<b>Marzo</b>", styles['TableCellRightBold']), Paragraph("<b>Abril</b>", styles['TableCellRightBold'])],
        [Paragraph("<b>Flujos Netos de Actividades de Operación</b>", styles['TableCellBold']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("+$ 12.942.532", styles['TableCellRight']), Paragraph("-$ 36.200.000", styles['TableCellRight']), Paragraph("-$ 9.800.000", styles['TableCellRight'])],
        [Paragraph("• Recaudos por ventas y cobranza de clientes", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("+$ 28.140.000", styles['TableCellRight']), Paragraph("+$ 2.600.000", styles['TableCellRight']), Paragraph("+$ 31.756.500", styles['TableCellRight'])],
        [Paragraph("• Pagos a proveedores de mercancías", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("-$ 12.000.000", styles['TableCellRight']), Paragraph("-$ 21.645.423", styles['TableCellRight']), Paragraph("-$ 28.800.842", styles['TableCellRight'])],
        [Paragraph("• Pagos de nómina y gastos operativos", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("-$ 3.197.468", styles['TableCellRight']), Paragraph("-$ 17.154.577", styles['TableCellRight']), Paragraph("-$ 12.755.658", styles['TableCellRight'])],
        [Paragraph("<b>Flujos Netos de Actividades de Inversión</b>", styles['TableCellBold']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("-$ 0", styles['TableCellRight']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 0", styles['TableCellRight'])],
        [Paragraph("<b>Flujos Netos de Actividades de Financiación</b>", styles['TableCellBold']), Paragraph("+$ 36.000.000", styles['TableCellRight']), Paragraph("+$ 39.600.000", styles['TableCellRight']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 0", styles['TableCellRight'])],
        [Paragraph("<b>VARIACIÓN NETA DE EFECTIVO DEL MES</b>", styles['TableCellBold']), Paragraph("<b>+$ 36.000.000</b>", styles['TableCellRightBold']), Paragraph("<b>+$ 52.542.532</b>", styles['TableCellRightBold']), Paragraph("<b>-$ 36.200.000</b>", styles['TableCellRightBold']), Paragraph("<b>-$ 9.800.000</b>", styles['TableCellRightBold'])],
        [Paragraph("Saldo Inicial de Efectivo", styles['TableCell']), Paragraph("$ 0", styles['TableCellRight']), Paragraph("$ 36.000.000", styles['TableCellRight']), Paragraph("$ 88.542.532", styles['TableCellRight']), Paragraph("$ 52.342.532", styles['TableCellRight'])],
        [Paragraph("<b>SALDO FINAL DE EFECTIVO Y EQUIVALENTES</b>", styles['TableCellBold']), Paragraph("<b>$ 36.000.000</b>", styles['TableCellRightBold']), Paragraph("<b>$ 88.542.532</b>", styles['TableCellRightBold']), Paragraph("<b>$ 52.342.532</b>", styles['TableCellRightBold']), Paragraph("<b>$ 42.542.532</b>", styles['TableCellRightBold'])],
    ]
    t_efe = Table(efe_data, colWidths=[204, 75, 75, 75, 75])
    t_efe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A2540")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor("#EEF2FF")),
        ('BACKGROUND', (0,9), (-1,9), colors.HexColor("#ECFDF5")),
    ]))
    story.append(t_efe)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 7: ESTADO 5: NOTAS Y REVELACIONES A LOS ESTADOS FINANCIEROS (NIIF)
    # =========================================================================
    story.append(Paragraph("4.6. ESTADO DE NOTAS Y REVELACIONES A LOS ESTADOS FINANCIEROS (NIIF PARA PYMES)", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=6, spaceBefore=0))
    
    story.append(Paragraph(
        "Bajo la Sección 8 de NIIF para PYMES, las notas proporcionan descripciones narrativas o desagregaciones de partidas:",
        styles['BodyCustom']
    ))
    
    notas_data = [
        [Paragraph("<b>Número &amp; Título de la Nota</b>", styles['TableCellBold']), Paragraph("<b>Políticas Contables y Revelación Específica en ELECTROVIVIENDA S.A.S</b>", styles['TableCellBold'])],
        [
            Paragraph("<b>NOTA 1: Entidad Reportante y Objeto</b>", styles['TableCellBold']),
            Paragraph("ELECTROVIVIENDA S.A.S, sociedad por acciones simplificada con NIT 901.765.438-3, domiciliada en Bucaramanga. Dedicada a la comercialización de electrodomésticos y gasodomésticos con régimen responsable de IVA.", styles['TableCell'])
        ],
        [
            Paragraph("<b>NOTA 2: Base de Preparación NIIF</b>", styles['TableCellBold']),
            Paragraph("Estados financieros preparados bajo NIIF para PYMES (Decreto 2420/2015, Grupo 2). Se aplica la hipótesis fundamental de Negocio en Marcha y la base contable de acumulación o devengo en pesos colombianos (COP).", styles['TableCell'])
        ],
        [
            Paragraph("<b>NOTA 3: Efectivo y Equivalentes</b>", styles['TableCellBold']),
            Paragraph("Saldo al 30 de abril: <b>$42.542.532</b> en cuentas corrientes bancarias y caja menor. Recursos de disponibilidad inmediata sin embargos, pignorado o restricciones para su uso.", styles['TableCell'])
        ],
        [
            Paragraph("<b>NOTA 4: Deudores Comerciales (Clientes)</b>", styles['TableCellBold']),
            Paragraph("Saldo al 30 de abril: <b>$23.600.000</b> por ventas a cuotas. La cartera se redujo un 50% frente a marzo ($47M) gracias a la gestión de cobro. No se evidencian indicios de deterioro o cartera morosa material.", styles['TableCell'])
        ],
        [
            Paragraph("<b>NOTA 5: Inventarios en Bodega</b>", styles['TableCellBold']),
            Paragraph("Saldo al 30 de abril: <b>$43.200.000</b> valuados al costo de adquisición mediante sistema permanente en kardex. Comprende televisores, lavadoras y neveras en exhibición, sin deterioro físico ni obsolescencia.", styles['TableCell'])
        ],
        [
            Paragraph("<b>NOTA 6: Propiedad, Planta y Equipo</b>", styles['TableCellBold']),
            Paragraph("Saldo neto al 30 de abril: <b>$209.890.151</b>. Incluye inmueble propio, vitrinas y vehículos de transporte, medidos al costo histórico menos depreciación acumulada por método de línea recta.", styles['TableCell'])
        ],
        [
            Paragraph("<b>NOTA 7: Pasivos Financieros y Proveedores</b>", styles['TableCellBold']),
            Paragraph("Pasivo Corriente (< 12 meses): <b>$53.927.428</b> (proveedores y nómina). Pasivo No Corriente (> 12 meses): <b>$36.744.815</b> (crédito bancario pactado a largo plazo). Total deuda: $90.672.243.", styles['TableCell'])
        ],
        [
            Paragraph("<b>NOTA 8: Capital Social y Patrimonio</b>", styles['TableCellBold']),
            Paragraph("Capital suscrito y pagado: <b>$240.000.000</b>. Patrimonio total: <b>$240.560.440</b> (100,23% del capital). Se constata formalmente la NO ocurrencia de causal de disolución del Art. 457 del Código de Comercio.", styles['TableCell'])
        ],
        [
            Paragraph("<b>NOTA 9: Hechos Posteriores al Cierre</b>", styles['TableCellBold']),
            Paragraph("Entre el 30 de abril y la fecha de este informe, no se presentaron hechos materiales que alteren las cifras. Se ratifica la política de rotación de inventarios existentes en mayo sin adquirir deudas.", styles['TableCell'])
        ],
    ]
    t_not = Table(notas_data, colWidths=[140, 364])
    t_not.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A2540")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_not)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 8: NEGOCIO EN MARCHA Y SUPERVIVENCIA (RUNWAY)
    # =========================================================================
    story.append(Paragraph("5. DICTAMEN DE NEGOCIO EN MARCHA Y RUNWAY DE SUPERVIVENCIA", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=6, spaceBefore=0))
    
    story.append(Paragraph(
        "<b>EVALUACIÓN DEL ARTÍCULO 457 DEL CÓDIGO DE COMERCIO:</b><br/>"
        "La ley colombiana establece que una sociedad entra en causal de disolución si las pérdidas acumuladas reducen el patrimonio "
        "neto por debajo del <b>50% del capital suscrito</b>. En ELECTROVIVIENDA S.A.S el capital social es de <b>$240.000.000</b>. "
        "El límite de alarma del 50% ocurriría únicamente si el patrimonio cayera por debajo de <b>$120.000.000</b>.<br/>"
        "Al cierre de abril de 2026, el patrimonio de la compañía se ubica en <b>$ 240.560.440 (100,23%)</b>. Incluso tras absorber "
        "todas las deudas y los gastos de arranque, el patrimonio supera el capital inicial. Por tanto, <b>la empresa es con certeza "
        "absoluta un NEGOCIO EN MARCHA</b>.", styles['BodyCustom']
    ))
    
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>SIMULACIÓN DE RESISTENCIA Y SUPERVIVENCIA FINANCIERA (RUNWAY SIN VENTAS):</b>", styles['SubSectionHeader']))
    story.append(Paragraph(
        "Bajo una prueba de estrés extrema: si la empresa no vendiera un solo peso y mantuviera sus gastos fijos de $10,2 millones mensuales, "
        "¿cuántos meses resiste sin quebrar ni entrar en cesación de pagos?", styles['BodyCustom']
    ))
    
    runway_data = [
        [Paragraph("<b>Escenario de Resistencia</b>", styles['TableCellBold']), Paragraph("<b>Recursos Disponibles</b>", styles['TableCellBold']), Paragraph("<b>Meses de Vida (Runway)</b>", styles['TableCellBold']), Paragraph("<b>Explicación Técnica</b>", styles['TableCellBold'])],
        [
            Paragraph("<b>Escenario 1: Solo con Dinero en Bancos</b>", styles['TableCellBold']),
            Paragraph("$ 42.542.532 (Caja/Bancos)", styles['TableCell']),
            Paragraph("<b>4,17 Meses</b><br/>(125 días)", styles['TableCellBold']),
            Paragraph("Cubrimiento de nóminas, arriendos y servicios con el efectivo inmediato en cuenta corriente, sin pedir créditos.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Escenario 2: Cobrando la Cartera de Clientes</b>", styles['TableCellBold']),
            Paragraph("$ 66.142.532 (Caja + Clientes)", styles['TableCell']),
            Paragraph("<b>6,49 Meses</b><br/>(195 días)", styles['TableCellBold']),
            Paragraph("Cobrando los $23,6M que deben los clientes en cuotas comerciales, la empresa sobrevive más de medio año a costo cero de ventas.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Escenario 3: Liquidando Mercancía al Costo</b>", styles['TableCellBold']),
            Paragraph("$ 94.000.000 (Efectivo + Stock)", styles['TableCell']),
            Paragraph("<b>9,22 Meses</b><br/>(276 días)", styles['TableCellBold']),
            Paragraph("Rematando los electrodomésticos en bodega sin ganar utilidad (al costo puro), la empresa opera sin problemas hasta 2027.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Escenario 4: Límite Legal del 50% del Capital</b>", styles['TableCellBold']),
            Paragraph("$ 120.560.440 (Colchón Patrimonial)", styles['TableCell']),
            Paragraph("<b>11,82 Meses</b><br/>(Casi 1 año)", styles['TableCellBold']),
            Paragraph("La empresa tendría que perder $10,2M todos los meses durante un año completo para llegar al límite de causal de disolución.", styles['TableCell'])
        ],
    ]
    t_run = Table(runway_data, colWidths=[120, 100, 84, 200])
    t_run.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A2540")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#FEF3C7")),
    ]))
    story.append(t_run)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 9: MATRIZ COMPLETA DE INDICADORES FINANCIEROS (FÓRMULAS Y PASO A PASO)
    # =========================================================================
    story.append(Paragraph("6. MATRIZ COMPLETA: INDICADORES FINANCIEROS Y SU SIGNIFICADO EN PALABRAS SIMPLES", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=6, spaceBefore=0))
    
    story.append(Paragraph(
        "A continuación se detalla la matriz técnica con su <b>fórmula matemática oficial</b>, la <b>explicación paso a paso</b> "
        "de cómo se obtienen las cifras sustituyendo los saldos de abril, los valores de los 4 meses y el diagnóstico didáctico:",
        styles['BodyCustom']
    ))
    
    ind_data = [
        [
            Paragraph("<b>Indicador &amp; Grupo</b>", styles['TableCellBold']),
            Paragraph("<b>Fórmula Matemática</b>", styles['TableCellBold']),
            Paragraph("<b>Paso a Paso &amp; Cálculo Real (Abril 2026)</b>", styles['TableCellBold']),
            Paragraph("<b>Feb</b>", styles['TableCellRightBold']),
            Paragraph("<b>Mar</b>", styles['TableCellRightBold']),
            Paragraph("<b>Abril</b>", styles['TableCellRightBold']),
            Paragraph("<b>Diagnóstico</b>", styles['TableCellBold'])
        ],
        # 1. Razón Corriente
        [
            Paragraph("<b>1. Razón Corriente</b><br/><font color='#64748B'>Liquidez Inmediata</font>", styles['TableCellBold']),
            Paragraph("<font face='Courier'>Activo Corriente<br/>───────────────<br/>Pasivo Corriente</font>", styles['TableCell']),
            Paragraph("Se divide el activo corriente entre el pasivo a pagar en menos de 1 año:<br/><b>$121.342.532 ÷ $53.927.428 = 2,25 veces</b>.<br/><i>Por cada $1 que debemos ya, tenemos $2,25 para responder.</i>", styles['TableCell']),
            Paragraph("2,15x", styles['TableCellRight']),
            Paragraph("1,92x", styles['TableCellRight']),
            Paragraph("<b>2,25x</b>", styles['TableCellRightBold']),
            Paragraph("🟢 Óptimo", styles['TableCellBold'])
        ],
        # 2. Prueba Ácida
        [
            Paragraph("<b>2. Prueba Ácida</b><br/><font color='#64748B'>Liquidez Severa</font>", styles['TableCellBold']),
            Paragraph("<font face='Courier'>Act. Corr. - Inv.<br/>───────────────<br/>Pasivo Corriente</font>", styles['TableCell']),
            Paragraph("Se resta el inventario ($43,2M) dejando el disponible y clientes ($78.142.532), y se divide entre la deuda corriente:<br/><b>$78.142.532 ÷ $53.927.428 = 1,45 veces</b>.<br/><i>Sin vender mercancía, se paga toda la deuda y sobra 45%.</i>", styles['TableCell']),
            Paragraph("1,38x", styles['TableCellRight']),
            Paragraph("1,14x", styles['TableCellRight']),
            Paragraph("<b>1,45x</b>", styles['TableCellRightBold']),
            Paragraph("🟢 Sobrado", styles['TableCellBold'])
        ],
        # 3. KTN
        [
            Paragraph("<b>3. Capital de Trabajo (KTN)</b><br/><font color='#64748B'>Fondo Operativo</font>", styles['TableCellBold']),
            Paragraph("<font face='Courier'>Activo Corriente<br/>─ Pasivo Corriente</font>", styles['TableCell']),
            Paragraph("Se restan las deudas de corto plazo de los activos de corto plazo:<br/><b>$121.342.532 - $53.927.428 = $67.415.104</b>.<br/><i>Plata libre y limpia para seguir trabajando sin apuros.</i>", styles['TableCell']),
            Paragraph("$92,8M", styles['TableCellRight']),
            Paragraph("$75,5M", styles['TableCellRight']),
            Paragraph("<b>$67,4M</b>", styles['TableCellRightBold']),
            Paragraph("🟢 Solvente", styles['TableCellBold'])
        ],
        # 4. Endeudamiento CP
        [
            Paragraph("<b>4. Endeudamiento Corto Plazo</b><br/><font color='#64748B'>Deuda &lt; 12 meses</font>", styles['TableCellBold']),
            Paragraph("<font face='Courier'>Pasivo Corriente<br/>───────────────<br/>Activo Total</font>", styles['TableCell']),
            Paragraph("Se divide la deuda corriente entre el activo total:<br/><b>$53.927.428 ÷ $331.232.683 = 16,28%</b>.<br/><i>Solo el 16,28% de los bienes está comprometido a corto plazo.</i>", styles['TableCell']),
            Paragraph("20,80%", styles['TableCellRight']),
            Paragraph("22,13%", styles['TableCellRight']),
            Paragraph("<b>16,28%</b>", styles['TableCellRightBold']),
            Paragraph("🟢 Muy Cómodo", styles['TableCellBold'])
        ],
        # 5. Endeudamiento LP
        [
            Paragraph("<b>5. Endeudamiento Largo Plazo</b><br/><font color='#64748B'>Deuda &gt; 12 meses</font>", styles['TableCellBold']),
            Paragraph("<font face='Courier'>Pasivo No Corriente<br/>───────────────<br/>Activo Total</font>", styles['TableCell']),
            Paragraph("Se divide la deuda no corriente entre el activo total:<br/><b>$36.744.815 ÷ $331.232.683 = 11,09%</b>.<br/><i>Créditos diferidos que no presionan la caja inmediata.</i>", styles['TableCell']),
            Paragraph("10,23%", styles['TableCellRight']),
            Paragraph("10,54%", styles['TableCellRight']),
            Paragraph("<b>11,09%</b>", styles['TableCellRightBold']),
            Paragraph("🟢 Estable", styles['TableCellBold'])
        ],
        # 6. Endeudamiento Total
        [
            Paragraph("<b>6. Nivel de Deuda Total</b><br/><font color='#64748B'>Acreedores vs Activo</font>", styles['TableCellBold']),
            Paragraph("<font face='Courier'>Pasivo Total<br/>───────────────<br/>Activo Total</font>", styles['TableCell']),
            Paragraph("Se divide el pasivo total entre el activo total:<br/><b>$90.672.243 ÷ $331.232.683 = 27,37%</b>.<br/><i>De cada $100 que la empresa tiene, solo debe $27,37.</i>", styles['TableCell']),
            Paragraph("31,04%", styles['TableCellRight']),
            Paragraph("32,68%", styles['TableCellRight']),
            Paragraph("<b>27,37%</b>", styles['TableCellRightBold']),
            Paragraph("🟢 Saneado", styles['TableCellBold'])
        ],
        # 7. Apalancamiento
        [
            Paragraph("<b>7. Apalancamiento (Leverage)</b><br/><font color='#64748B'>Deuda vs Patrimonio</font>", styles['TableCellBold']),
            Paragraph("<font face='Courier'>Pasivo Total<br/>───────────────<br/>Patrimonio Neto</font>", styles['TableCell']),
            Paragraph("Se divide la deuda total entre el patrimonio:<br/><b>$90.672.243 ÷ $240.560.440 = 0,38 veces</b>.<br/><i>Por cada $1 de los socios, los acreedores ponen 38 centavos.</i>", styles['TableCell']),
            Paragraph("0,45x", styles['TableCellRight']),
            Paragraph("0,49x", styles['TableCellRight']),
            Paragraph("<b>0,38x</b>", styles['TableCellRightBold']),
            Paragraph("🟢 Seguro", styles['TableCellBold'])
        ],
        # 8. Concentración CP
        [
            Paragraph("<b>8. Concentración Deuda CP</b><br/><font color='#64748B'>Perfil Vencimiento</font>", styles['TableCellBold']),
            Paragraph("<font face='Courier'>Pasivo Corriente<br/>───────────────<br/>Pasivo Total</font>", styles['TableCell']),
            Paragraph("Se divide el pasivo corriente entre el pasivo total:<br/><b>$53.927.428 ÷ $90.672.243 = 59,48%</b>.<br/><i>El 40,52% de la deuda está protegida a largo plazo.</i>", styles['TableCell']),
            Paragraph("67,03%", styles['TableCellRight']),
            Paragraph("68,32%", styles['TableCellRight']),
            Paragraph("<b>59,48%</b>", styles['TableCellRightBold']),
            Paragraph("🟢 Mejoró 8.8%", styles['TableCellBold'])
        ],
        # 9. Margen Bruto
        [
            Paragraph("<b>9. Margen Bruto Comercial</b><br/><font color='#64748B'>Ganancia en Ventas</font>", styles['TableCellBold']),
            Paragraph("<font face='Courier'>Utilidad Bruta<br/>───────────────<br/>Ventas Netas</font>", styles['TableCell']),
            Paragraph("Se divide la ganancia bruta ($4,86M) entre ventas ($8,15M):<br/><b>$4.868.500 ÷ $8.156.500 = 59,69%</b>.<br/><i>De cada $100 vendidos, quedan $59,69 limpios antes de fijos.</i>", styles['TableCell']),
            Paragraph("32,07%", styles['TableCellRight']),
            Paragraph("N/A", styles['TableCellRight']),
            Paragraph("<b>59,69%</b>", styles['TableCellRightBold']),
            Paragraph("🟢 Altísimo", styles['TableCellBold'])
        ],
        # 10. Resultado Neto
        [
            Paragraph("<b>10. Resultado Neto del Mes</b><br/><font color='#64748B'>Utilidad / Pérdida</font>", styles['TableCellBold']),
            Paragraph("<font face='Courier'>Utilidad Bruta<br/>─ Gastos Operativos</font>", styles['TableCell']),
            Paragraph("Utilidad bruta ($4,86M) menos nómina y arriendos ($12,75M):<br/><b>$4.868.500 - $12.755.658 = -$7.887.158</b>.<br/><i>La pérdida bajó un 54% frente a marzo; rumbo al equilibrio.</i>", styles['TableCell']),
            Paragraph("+$16,4M", styles['TableCellRight']),
            Paragraph("-$17,1M", styles['TableCellRight']),
            Paragraph("<b>-$7,89M</b>", styles['TableCellRightBold']),
            Paragraph("🟡 Sanando", styles['TableCellBold'])
        ],
        # 11. ROE
        [
            Paragraph("<b>11. Rendimiento Capital (ROE)</b><br/><font color='#64748B'>Retorno Socios</font>", styles['TableCellBold']),
            Paragraph("<font face='Courier'>Resultado Neto<br/>───────────────<br/>Patrimonio Neto</font>", styles['TableCell']),
            Paragraph("Se divide el resultado neto entre el patrimonio:<br/><b>-$7.887.158 ÷ $240.560.440 = -3,28%</b>.<br/><i>La pérdida solo rozó el 3,28% del capital de los socios.</i>", styles['TableCell']),
            Paragraph("+6,19%", styles['TableCellRight']),
            Paragraph("-6,90%", styles['TableCellRight']),
            Paragraph("<b>-3,28%</b>", styles['TableCellRightBold']),
            Paragraph("🟢 Redujo 52%", styles['TableCellBold'])
        ],
        # 12. ROA
        [
            Paragraph("<b>12. Rendimiento Activo (ROA)</b><br/><font color='#64748B'>Eficiencia Activos</font>", styles['TableCellBold']),
            Paragraph("<font face='Courier'>Resultado Neto<br/>───────────────<br/>Activo Total</font>", styles['TableCell']),
            Paragraph("Se divide el resultado neto entre los activos totales:<br/><b>-$7.887.158 ÷ $331.232.683 = -2,38%</b>.<br/><i>Los activos están intactos; con ventas en mayo el ROA será positivo.</i>", styles['TableCell']),
            Paragraph("+4,25%", styles['TableCellRight']),
            Paragraph("-4,64%", styles['TableCellRight']),
            Paragraph("<b>-2,38%</b>", styles['TableCellRightBold']),
            Paragraph("🟢 Resiliente", styles['TableCellBold'])
        ],
    ]
    t_ind = Table(ind_data, colWidths=[80, 80, 184, 38, 38, 42, 42])
    t_ind.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A2540")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_ind)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 10: CONCLUSIONES, PUNTO DE EQUILIBRIO Y FIRMAS OFICIALES
    # =========================================================================
    story.append(Paragraph("7. CONCLUSIONES ESTRATÉGICAS Y PLAN DE ACCIÓN PARA MAYO", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=6, spaceBefore=0))
    
    concl_p = [
        [Paragraph("<b>1. ¿La empresa está en quiebra o en peligro?</b><br/><b>Rotundamente NO.</b> ELECTROVIVIENDA S.A.S es una empresa sumamente sólida. Las pérdidas de marzo y abril fueron consecuencia de mantener la estructura fija de salarios mientras se recibían y catalogaban los inventarios de electrodomésticos. El patrimonio de $240 millones de los socios blinda íntegramente a la compañía.", styles['TableCell'])],
        [Paragraph("<b>2. Punto de Equilibrio Matemático:</b><br/>Para cubrir la totalidad de sus gastos de operación sin generar pérdidas, ELECTROVIVIENDA requiere facturar <b>$22.000.000 mensuales</b>. Con ese volumen de ventas, el margen comercial del 59% genera <b>$13.000.000 de utilidad bruta</b>, cubriendo con holgura los salarios y servicios del local.", styles['TableCell'])],
        [Paragraph("<b>3. Estrategia y Recomendación para Mayo de 2026:</b><br/>Como la empresa ya dispone de un surtido completamente pago en bodega ($43,2M en kardex), la orden de gerencia para mayo debe ser: <b>Cero endeudamiento nuevo y máxima rotación comercial</b>. Cada venta nueva en mayo representará dinero líquido que entrará directamente a caja.", styles['TableCell'])],
    ]
    t_concl = Table(concl_p, colWidths=[504])
    t_concl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_concl)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("8. CERTIFICACIÓN PERICIAL Y FIRMAS DE AUTORIDADES", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=10, spaceBefore=0))
    
    story.append(Paragraph(
        "En constancia de lo actuado, se expide el presente informe financiero y peritaje contable en Bucaramanga, "
        "Santander, a los 10 días del mes de noviembre de 2026, con validez jurídica y probatoria bajo la ley colombiana:",
        styles['BodyCustom']
    ))
    
    story.append(Spacer(1, 25))
    
    firmas_data = [
        [
            Paragraph("____________________________________<br/><b>Gina Villamizar</b><br/>Contadora Titular — T.P. 248960-T<br/>Especialista en Normas NIIF<br/>Estudiante SENA CSET Bucaramanga", styles['TableCell']),
            Paragraph("____________________________________<br/><b>Kevin Guerrero</b><br/>Representante Legal Principal<br/>C.C. 1.098.765.432<br/>ELECTROVIVIENDA S.A.S", styles['TableCell']),
            Paragraph("____________________________________<br/><b>Marcela Gonzales</b><br/>Revisora Fiscal Colegiada<br/>T.P. 194820-T<br/>Dictamen Sin Salvedades", styles['TableCell']),
        ]
    ]
    t_firm = Table(firmas_data, colWidths=[168, 168, 168])
    t_firm.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_firm)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF built successfully: {filename}")

if __name__ == '__main__':
    out_pdf = "/Users/ginavillamizar/Downloads/CONTABILIDAD/INFORME_FINANCIERO_ELECTROVIVIENDA_2026.pdf"
    build_pdf(out_pdf)

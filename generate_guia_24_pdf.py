import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
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
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#00324D"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 755, "SERVICIO NACIONAL DE APRENDIZAJE SENA — GUÍA DE APRENDIZAJE Nº 24 RESUELTA")
            self.setFont("Helvetica", 7)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawRightString(572, 755, "Flujo de Efectivo y Estado de Cambios en el Patrimonio")
            self.setStrokeColor(colors.HexColor("#39A900")) # SENA green
            self.setLineWidth(1)
            self.line(40, 748, 572, 748)

        # Footer
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(40, 42, 572, 42)
        
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#39A900"))
        self.drawString(40, 30, "SENA • Tecnología en Gestión Contable y de Información Financiera")
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#666666"))
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(572, 30, page_text)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor("#00324D"),
        alignment=1, # Center
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#39A900"),
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#FFFFFF"),
        spaceAfter=0
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#00324D"),
        spaceBefore=7,
        spaceAfter=4
    )

    q_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0B192C"),
        spaceBefore=6,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#222222"),
        spaceAfter=4
    )

    ans_box_style = ParagraphStyle(
        'AnsBoxText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1A365D")
    )

    ans_bold_style = ParagraphStyle(
        'AnsBoldText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0B2545")
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#222222"),
        leftIndent=12,
        spaceAfter=2
    )

    story = []

    def make_section_banner(title_text):
        p = Paragraph(f"<b>{title_text}</b>", h1_style)
        t = Table([[p]], colWidths=[532])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#00324D")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('LINELEFT', (0,0), (0,0), 4, colors.HexColor("#39A900")),
        ]))
        return t

    def make_answer_box(content_flowables, label="RESPUESTA / DESARROLLO:"):
        cell_elements = []
        if label:
            lbl_p = Paragraph(f"<b><font color='#39A900'>✔ {label}</font></b>", ans_bold_style)
            cell_elements.append(lbl_p)
            cell_elements.append(Spacer(1, 3))
        if isinstance(content_flowables, list):
            cell_elements.extend(content_flowables)
        else:
            cell_elements.append(content_flowables)
        
        t = Table([[cell_elements]], colWidths=[532])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E1")),
            ('LINELEFT', (0,0), (0,0), 3.5, colors.HexColor("#0284C7")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    # HEADER DEL DOCUMENTO
    header_data = [
        [
            Paragraph("<b>SERVICIO NACIONAL DE APRENDIZAJE SENA</b><br/>DIRECCIÓN DE FORMACIÓN PROFESIONAL INTEGRAL<br/>FORMATO GUÍA DE APRENDIZAJE", ParagraphStyle('HdrP', fontName='Helvetica-Bold', fontSize=8.5, leading=11, alignment=1, textColor=colors.HexColor("#00324D"))),
            Paragraph("<b>GFPI-F-019 V03</b><br/><font color='#39A900'><b>GUÍA RESUELTA</b></font>", ParagraphStyle('HdrCode', fontName='Helvetica-Bold', fontSize=8, leading=10, alignment=1, textColor=colors.HexColor("#555555")))
        ]
    ]
    hdr_table = Table(header_data, colWidths=[420, 112])
    hdr_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#00324D")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(hdr_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("GUÍA Nº 24: FLUJO DE EFECTIVO Y ESTADO DE CAMBIOS EN EL PATRIMONIO", title_style))
    story.append(Paragraph("PROGRAMA: TECNOLOGÍA EN GESTIÓN CONTABLE Y DE INFORMACIÓN FINANCIERA (CÓDIGO 123101 V1)", subtitle_style))

    # 1. IDENTIFICACIÓN DE LA GUÍA
    story.append(make_section_banner("1. IDENTIFICACIÓN DE LA GUÍA DE APRENDIZAJE"))
    story.append(Spacer(1, 4))
    
    ident_data = [
        [Paragraph("<b>Denominación del Programa:</b>", body_style), Paragraph("Tecnología en Gestión Contable y de Información Financiera", body_style)],
        [Paragraph("<b>Código del Programa:</b>", body_style), Paragraph("123101 versión 1", body_style)],
        [Paragraph("<b>Nombre del Proyecto:</b>", body_style), Paragraph("Aplicación de la normativa contable, tributaria, laboral, comercial y financiera, a través de una empresa didáctica y/o del sector productivo", body_style)],
        [Paragraph("<b>Fase del Proyecto:</b>", body_style), Paragraph("Ejecución: Presentar informes contables, tributarios y proyecciones de acuerdo con políticas y normativa", body_style)],
        [Paragraph("<b>Actividad de Proyecto:</b>", body_style), Paragraph("AP 5: Elaborar informes financieros aplicando herramientas informáticas según políticas y normativa", body_style)],
        [Paragraph("<b>Actividad de Aprendizaje:</b>", body_style), Paragraph("AA_24: Preparar estado de flujo de efectivo y cambios en el patrimonio según normativa y políticas contables", body_style)],
        [Paragraph("<b>Competencia:</b>", body_style), Paragraph("210303023 Elaborar informes financieros de acuerdo con metodología y normativa", body_style)],
        [Paragraph("<b>Resultados de Aprendizaje:</b>", body_style), Paragraph("• 210303023 01 Establecer la estructura de los informes financieros de acuerdo con normativa.<br/>• 210303023 02 Elaborar los informes financieros, según políticas contables y normativa.", body_style)],
        [Paragraph("<b>Duración de la Guía:</b>", body_style), Paragraph("144 horas (3 Créditos)", body_style)]
    ]
    ident_table = Table(ident_data, colWidths=[150, 382])
    ident_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F1F5F9")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(ident_table)
    story.append(Spacer(1, 10))

    # 2. PRESENTACIÓN
    story.append(make_section_banner("2. PRESENTACIÓN Y MARCO CONCEPTUAL"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "El <b>Estado de Flujos de Efectivo (NIC 7 / Sección 7 NIIF PYMES)</b> y el <b>Estado de Cambios en el Patrimonio (NIC 1 / Sección 6 NIIF PYMES)</b> son informes financieros dinámicos y pilares insustituibles en la toma de decisiones económicas. Mientras que el balance general y el estado de resultados operan bajo la base del devengo, el flujo de efectivo revela la liquidez real y la capacidad de la entidad para generar caja a través de sus actividades operativas, de inversión y de financiación. Paralelamente, el estado de cambios en el patrimonio expone las variaciones patrimoniales originadas por aportes, reservas, dividendos y el rendimiento integral acumulado. <i>'Si queréis ser ricos no aprendáis solamente a saber cómo se gana, sino también cómo se invierte' (Benjamin Franklin).</i>",
        body_style
    ))
    story.append(Spacer(1, 8))

    # 3.1 REFLEXIÓN INICIAL
    story.append(make_section_banner("3.1 ACTIVIDADES DE REFLEXIÓN INICIAL (FLUJOS DEL HOGAR)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Instrucción:</b> Tomando como referencia la situación financiera de su hogar, analice las entradas y salidas de dinero y realice las siguientes clasificaciones en un informe escrito:",
        body_style
    ))
    story.append(Spacer(1, 3))

    # Clasificación salidas
    story.append(Paragraph("<b>1. Clasificación del dinero empleado (salidas) en el hogar:</b>", q_style))
    salidas_ans = [
        Paragraph("<b>Desglose mensual de erogaciones del hogar (Total salidas: $3.900.000 COP):</b>", ans_box_style),
        Paragraph("• <b>1. Compra de bienes para el hogar (Inversión patrimonial):</b> $300.000 (Adquisición y reposición de pequeños electrodomésticos, vajilla y mejoras del hogar).", bullet_style),
        Paragraph("• <b>2. Gastos corrientes del hogar (Operación):</b> $2.950.000 (Alimentación y mercado $1.500.000; Servicios públicos de agua, luz, gas e internet $450.000; Arriendo de vivienda $750.000; Transporte y movilidad $250.000).", bullet_style),
        Paragraph("• <b>3. Pago de deudas (Financiación):</b> $650.000 (Abono a capital e intereses de crédito bancario de consumo $400.000; Pago de tarjeta de crédito comercial $250.000).", bullet_style)
    ]
    story.append(make_answer_box(salidas_ans))
    story.append(Spacer(1, 6))

    # Clasificación entradas
    story.append(Paragraph("<b>2. Clasificación del dinero recibido (entradas) en el hogar:</b>", q_style))
    entradas_ans = [
        Paragraph("<b>Desglose mensual de fuentes de financiamiento (Total entradas: $4.400.000 COP):</b>", ans_box_style),
        Paragraph("• <b>1. Del salario o trabajo de los líderes del hogar (Actividad operativa):</b> $3.800.000 (Sueldos netos devengados por los miembros laboralmente activos).", bullet_style),
        Paragraph("• <b>2. Del usufructo de bienes adquiridos (Inversión y rendimiento):</b> $600.000 (Ingresos por arrendamiento de una habitación o local comercial y venta de productos menores).", bullet_style),
        Paragraph("• <b>3. De préstamos o deudas adquiridas (Financiación externa):</b> $0 ordinario en el mes (Se activa exclusivamente ante imprevistos de capital o adquisición de activos fijos).", bullet_style)
    ]
    story.append(make_answer_box(entradas_ans))
    story.append(Spacer(1, 6))

    # Conclusiones
    story.append(Paragraph("<b>3. Conclusiones del análisis de flujo del hogar:</b>", q_style))
    conc_ans = [
        Paragraph("• <b>¿Cuál es la principal fuente de ingresos de su hogar?</b><br/>La principal fuente de ingresos proviene de la <b>actividad laboral directa (salarios de los líderes del hogar)</b>, representando el <b>86,36%</b> de los fondos totales recibidos ($3.800.000 de $4.400.000). Esto refleja que la economía familiar depende primordialmente de su fuerza de trabajo (operación).", ans_box_style),
        Spacer(1, 3),
        Paragraph("• <b>¿En qué se gasta más dinero en su hogar?</b><br/>El mayor porcentaje de desembolsos corresponde a los <b>gastos operacionales de supervivencia básica</b>, encabezados por la <b>alimentación (mercado familiar con $1.500.000 / 38,46%)</b> y los costos de <b>vivienda (arriendo y servicios públicos con $1.200.000 / 30,77%)</b>. Juntos absorben el <b>69,23%</b> del gasto total mensual del hogar.", ans_box_style)
    ]
    story.append(make_answer_box(conc_ans))
    story.append(Spacer(1, 10))

    # 3.2 CONTEXTUALIZACIÓN
    story.append(make_section_banner("3.2 CONTEXTUALIZACIÓN: CASO DE INVERSIÓN Y MATRIZ DE FLUJO DE CAJA"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Planteamiento del Caso:</b> La familia planea adquirir un televisor plasma de 60¨ ($2.200.000) y un juego de sala y comedor nuevo ($3.800.000), totalizando una inversión en bienes de <b>$6.000.000 COP</b>.",
        body_style
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>Preguntas de Análisis Estratégico Familiar:</b>", q_style))
    caso_p_ans = [
        Paragraph("• <b>¿De dónde obtendrían el dinero para realizar la inversión y qué cambios realizaría para obtener más ingresos?</b><br/>Se estructurará un modelo mixto: (1) <b>Ahorros acumulados familiares</b> por $2.000.000 (equivalentes a 4 meses del superávit mensual); (2) <b>Venta del televisor y sala actuales usados</b> por $800.000; y (3) <b>Crédito de financiación bancaria a 24 meses</b> por el saldo de $3.200.000 a una cuota mensual estimada de $175.000. Para robustecer los ingresos, se incrementarán horas extras y actividades comerciales independientes de fin de semana.", ans_box_style),
        Spacer(1, 3),
        Paragraph("• <b>¿Qué cambios realizará para disminuir los gastos y asegurar el pago de la deuda?</b><br/>Se aplicará un plan de austeridad focalizado: (1) Racionalización de planes de telefonía móvil y plataformas de streaming ($70.000/mes); (2) Optimización de consumo de energía eléctrica y agua ($50.000/mes); y (3) Disminución de salidas a restaurantes y ocio exterior ($100.000/mes). Con este ahorro de $220.000 mensuales se cubre con holgura la cuota del nuevo crédito sin asfixiar la economía del hogar.", ans_box_style)
    ]
    story.append(make_answer_box(caso_p_ans))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Cuadro Clasificado en 3 Actividades de Flujo (Operación, Inversión y Financiación):</b>", q_style))
    
    matriz_data = [
        [
            Paragraph("<b>Detalle del Movimiento Contable</b>", ans_bold_style),
            Paragraph("<b>Actividad Principal (Operación)</b>", ans_bold_style), "",
            Paragraph("<b>Inversión en Bienes y Muebles</b>", ans_bold_style), "",
            Paragraph("<b>Financiación (Deudas > 1 Año)</b>", ans_bold_style), ""
        ],
        [
            "",
            Paragraph("<b>Entradas</b>", body_style), Paragraph("<b>Salidas</b>", body_style),
            Paragraph("<b>Entradas</b>", body_style), Paragraph("<b>Salidas</b>", body_style),
            Paragraph("<b>Entradas</b>", body_style), Paragraph("<b>Salidas</b>", body_style)
        ],
        [
            Paragraph("Salarios o ingresos laborales del hogar", body_style),
            Paragraph("$3.800.000", body_style), Paragraph("-", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style)
        ],
        [
            Paragraph("Arriendos o usufructo de bienes recibidos", body_style),
            Paragraph("$600.000", body_style), Paragraph("-", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style)
        ],
        [
            Paragraph("Gastos del hogar (comida, arriendo, servicios, transporte)", body_style),
            Paragraph("-", body_style), Paragraph("$2.950.000", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style)
        ],
        [
            Paragraph("Pago de deudas menores a un año (tarjetas y pasivos corrientes)", body_style),
            Paragraph("-", body_style), Paragraph("$250.000", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style)
        ],
        [
            Paragraph("Venta de televisor y muebles usados antiguos", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style),
            Paragraph("$800.000", body_style), Paragraph("-", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style)
        ],
        [
            Paragraph("Compra del televisor plasma 60'' y juego de sala/comedor", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style),
            Paragraph("-", body_style), Paragraph("$6.000.000", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style)
        ],
        [
            Paragraph("Dinero recibido por nuevo préstamo bancario (> 1 año)", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style),
            Paragraph("$3.200.000", body_style), Paragraph("-", body_style)
        ],
        [
            Paragraph("Pago cuotas de amortización créditos a largo plazo", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style),
            Paragraph("-", body_style), Paragraph("$400.000", body_style)
        ],
        [
            Paragraph("Uso de ahorros acumulados previos para completar compra", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style),
            Paragraph("$2.000.000", body_style), Paragraph("-", body_style),
            Paragraph("-", body_style), Paragraph("-", body_style)
        ],
        [
            Paragraph("<b>TOTALES POR ACTIVIDAD</b>", ans_bold_style),
            Paragraph("<b>$4.400.000</b>", ans_bold_style), Paragraph("<b>$3.200.000</b>", ans_bold_style),
            Paragraph("<b>$2.800.000</b>", ans_bold_style), Paragraph("<b>$6.000.000</b>", ans_bold_style),
            Paragraph("<b>$3.200.000</b>", ans_bold_style), Paragraph("<b>$400.000</b>", ans_bold_style)
        ],
        [
            Paragraph("<b>FLUJO NETO POR ACTIVIDAD</b>", ans_bold_style),
            Paragraph("<b>+$1.200.000</b>", ans_bold_style), "",
            Paragraph("<b>-$3.200.000</b>", ans_bold_style), "",
            Paragraph("<b>+$2.800.000</b>", ans_bold_style), ""
        ],
        [
            Paragraph("<b>VARIACIÓN NETA TOTAL DEL EFECTIVO (A + B + C):</b>", ans_bold_style),
            Paragraph("<b>+$800.000 COP</b> (Incremento neto de caja al cierre del período)", ans_bold_style), "", "", "", "", ""
        ]
    ]

    matriz_table = Table(matriz_data, colWidths=[160, 62, 62, 62, 62, 62, 62])
    matriz_table.setStyle(TableStyle([
        ('SPAN', (1,0), (2,0)),
        ('SPAN', (3,0), (4,0)),
        ('SPAN', (5,0), (6,0)),
        ('SPAN', (1,12), (2,12)),
        ('SPAN', (3,12), (4,12)),
        ('SPAN', (5,12), (6,12)),
        ('SPAN', (1,13), (6,13)),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,1), colors.HexColor("#00324D")),
        ('TEXTCOLOR', (0,0), (-1,1), colors.HexColor("#FFFFFF")),
        ('BACKGROUND', (0,11), (-1,11), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (0,12), (-1,12), colors.HexColor("#FEF08A")),
        ('BACKGROUND', (0,13), (-1,13), colors.HexColor("#DCFCE7")),
        ('ALIGN', (1,2), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(matriz_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>¿Los bienes, deudas y patrimonio de su hogar cambió respecto a los datos iniciales? Explique:</b>", q_style))
    impacto_ans = [
        Paragraph("<b>Sí, hubo una variación patrimonial sustancial y positiva:</b>", ans_bold_style),
        Paragraph("1. <b>Activos (Bienes):</b> Se incrementaron en <b>+$5.200.000</b> netos (Entraron muebles nuevos por $6.000.000, salió el ahorro por $2.000.000, salieron muebles usados por $800.000 y aumentó el efectivo neto en +$800.000). El nuevo activo total asciende a <b>$29.000.000 COP</b>.", bullet_style),
        Paragraph("2. <b>Pasivos (Deudas):</b> Se incrementaron en <b>+$2.800.000</b> netos (Nuevo préstamo recibido por $3.200.000 menos amortización pagada de $400.000). El pasivo total pasó a <b>$9.150.000 COP</b>.", bullet_style),
        Paragraph("3. <b>Patrimonio Neto:</b> Pasó de $17.450.000 a <b>$19.850.000 COP</b>, experimentando un <b>aumento neto de +$2.400.000 COP</b> gracias al superávit operativo generado en el período que capitalizó a la familia con activos de mayor valor.", bullet_style)
    ]
    story.append(make_answer_box(impacto_ans))
    story.append(Spacer(1, 10))

    # 3.3.1 APROPIACIÓN NIC 7
    story.append(make_section_banner("3.3.1 MARCO TÉCNICO NORMATIVO: ESTADO DE FLUJOS DE EFECTIVO (NIC 7)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Estructura Técnica, Componentes y Métodos del Estado de Flujos de Efectivo (NIC 7 / NIIF PYMES Sección 7):</b>", body_style))
    story.append(Spacer(1, 3))

    nic7_data = [
        [Paragraph("<b>Componente Normativo</b>", ans_bold_style), Paragraph("<b>Fundamentación Técnica y Requerimientos de la NIC 7</b>", ans_bold_style)],
        [
            Paragraph("<b>1. Definición del Estado de Flujos de Efectivo</b>", body_style),
            Paragraph("Estado financiero básico que informa acerca de los flujos de entradas y salidas de efectivo y equivalentes al efectivo habidos durante un período, clasificándolos en actividades de operación, de inversión y de financiación.", body_style)
        ],
        [
            Paragraph("<b>2. Importancia y Utilidad</b>", body_style),
            Paragraph("Permite evaluar la capacidad de la empresa para generar efectivo genuino; determinar sus necesidades de liquidez; predecir la solvencia futura; evaluar la viabilidad de pagar deudas y dividendos; y aislar los efectos contables del devengo que no representan caja inmediata.", body_style)
        ],
        [
            Paragraph("<b>3. Objetivo de la NIC 7</b>", body_style),
            Paragraph("Exigir a las entidades que suministren información histórica sobre los cambios en el efectivo y sus equivalentes, mediante un estado que clasifique los flujos de fondos según su origen económico.", body_style)
        ],
        [
            Paragraph("<b>4. Elementos Clave</b>", body_style),
            Paragraph("• <b>Efectivo:</b> Comprende la caja general, cajas menores y los depósitos bancarios a la vista.<br/>• <b>Equivalentes al Efectivo:</b> Inversiones a corto plazo de gran liquidez, fácilmente convertibles en importes determinados de efectivo, con vencimiento original <b>no superior a 3 meses</b> y sujetas a un riesgo insignificante de cambios en su valor.", body_style)
        ],
        [
            Paragraph("<b>5. Estructura: Las 3 Actividades</b>", body_style),
            Paragraph("• <b>Actividades de Operación (NIC 7.14):</b> Constituyen la principal fuente de ingresos ordinarios de la entidad (cobros a clientes por venta de bienes/servicios, pagos a proveedores por mercancías, pagos de nómina y pagos de impuestos).<br/>• <b>Actividades de Inversión (NIC 7.16):</b> Representan la adquisición y desapropiación de activos a largo plazo (compra o venta de propiedades, planta y equipo, activos intangibles e instrumentos financieros a largo plazo).<br/>• <b>Actividades de Financiación (NIC 7.17):</b> Producen cambios en el tamaño y composición de los capitales propios y de los préstamos tomados (emisión de acciones, obtención o reembolso de préstamos bancarios y pago de dividendos).", body_style)
        ],
        [
            Paragraph("<b>6. Fuentes y Usos</b>", body_style),
            Paragraph("• <b>Fuentes (Orígenes / Entradas):</b> Disminución de activos (ej. cobro de cartera, venta de inventario o maquinaria), aumento de pasivos (préstamos bancarios) y aumentos de capital social.<br/>• <b>Usos (Aplicaciones / Salidas):</b> Aumento de activos (compra de equipo o inventarios), disminución de pasivos (pago de proveedores o créditos) y pérdidas operacionales.", body_style)
        ],
        [
            Paragraph("<b>7. Métodos de Presentación</b>", body_style),
            Paragraph("• <b>Método Directo (NIC 7.18a):</b> Presenta por separado las principales categorías de cobros y pagos brutos en efectivo (ej. efectivo cobrado a clientes, efectivo pagado a proveedores, efectivo pagado a empleados). Es el método recomendado por el IASB.<br/>• <b>Método Indirecto (NIC 7.18b):</b> Comienza con la Ganancia o Pérdida neta del ejercicio y se ajusta por los efectos de transacciones no monetarias (depreciaciones, provisiones, deterioro), cambios en el capital de trabajo de balance (variaciones de cartera, inventarios, proveedores) y partidas asociadas a inversión o financiación.", body_style)
        ]
    ]

    nic7_table = Table(nic7_data, colWidths=[150, 382])
    nic7_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#00324D")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#FFFFFF")),
        ('BACKGROUND', (0,1), (0,-1), colors.HexColor("#F8FAFC")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(nic7_table)
    story.append(Spacer(1, 10))

    # 3.3.2 ESTADO DE CAMBIOS EN EL PATRIMONIO
    story.append(make_section_banner("3.3.2 ESTADO DE CAMBIOS EN EL PATRIMONIO (NIC 1.96–101)"))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>1. ¿En qué consiste el Estado de Cambios en el Patrimonio?</b>", q_style))
    ecp_def_ans = [
        Paragraph("Es un estado financiero básico y dinámico que refleja de forma detallada y comparativa las variaciones, aumentos y disminuciones ocurridas en cada uno de los rubros que integran el patrimonio de una entidad durante un ejercicio contable. Permite a los inversionistas y entes de control comprender la distribución de las utilidades, el fortalecimiento de reservas, los aportes o reembolsos de capital, y los efectos patrimoniales reconocidos directamente en el Otro Resultado Integral (ORI).", ans_box_style)
    ]
    story.append(make_answer_box(ecp_def_ans))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2. Elementos que Componen el Patrimonio:</b>", q_style))
    ecp_elem_ans = [
        Paragraph("• <b>Capital Social / Emitido:</b> Aportes en dinero o en especie realizados por los socios o accionistas (Capital suscrito y pagado).", bullet_style),
        Paragraph("• <b>Prima en Colocación de Acciones / Cuotas:</b> Valor pagado por los accionistas por encima del valor nominal de las acciones.", bullet_style),
        Paragraph("• <b>Reservas Patrimoniales:</b> Fondos retenidos por mandato legal (Reserva Legal 10% según Art. 452 C.Co.), estatutarias u ocasionales.", bullet_style),
        Paragraph("• <b>Otro Resultado Integral (ORI) Acumulado:</b> Ganancias o pérdidas no realizadas (revaluaciones de PPyE, coberturas de flujos de efectivo, diferencias de cambio).", bullet_style),
        Paragraph("• <b>Resultados Acumulados de Ejercicios Anteriores:</b> Utilidades o pérdidas no distribuidas de períodos contables previos.", bullet_style),
        Paragraph("• <b>Resultado del Ejercicio Actual:</b> Ganancia o pérdida neta generada en el período reportado según el Estado de Resultados.", bullet_style)
    ]
    story.append(make_answer_box(ecp_elem_ans))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>3. Estructura y Aspectos Contables a Presentar y Revelar (NIC 1.106):</b>", q_style))
    ecp_struct_ans = [
        Paragraph("<b>Estructura Matricial Obligatoria:</b>", ans_bold_style),
        Paragraph("Se presenta en una matriz columnar donde cada columna representa un componente patrimonial (Capital, Reservas, Resultados, ORI, Total). En las filas se detallan cronológicamente: (1) Saldo al inicio del período; (2) Ajustes retroactivos por cambios de políticas o correcciones de errores (NIC 8); (3) Resultado integral total del período; (4) Transacciones con los propietarios en su calidad de tales (emisiones de capital, readquisición de acciones y dividendos decretados); y (5) Saldo al cierre del período.", ans_box_style),
        Spacer(1, 3),
        Paragraph("<b>Información a Revelar en Notas:</b> Desglose de dividendos reconocidos como distribución a los propietarios (y el importe por acción); restricciones legales o contractuales sobre reservas; y conciliación detallada de cada partida.", ans_box_style)
    ]
    story.append(make_answer_box(ecp_struct_ans))
    story.append(Spacer(1, 10))

    # 3.4 TRANSFERENCIA DEL CONOCIMIENTO (CASO PRÁCTICO ELECTROVIVIENDA)
    story.append(make_section_banner("3.4 TRANSFERENCIA DEL CONOCIMIENTO: APLICACIÓN PRÁCTICA REAL"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Aplicación al Proyecto Formativo:</b> Estados financieros emitidos para la empresa <b>ELECTROVIVIENDA S.A.S. (NIT: 901.765.438-3)</b> bajo <b>NIIF para las PYMES (Grupo 2)</b> en el período de <b>ABRIL 2026</b>:",
        body_style
    ))
    story.append(Spacer(1, 3))

    # ESTADO FLUJO DE EFECTIVO OFICIAL
    story.append(Paragraph("<b>A. ESTADO DE FLUJOS DE EFECTIVO — MÉTODO INDIRECTO NIIF (ABRIL 2026)</b>", h2_style))
    fe_data = [
        [Paragraph("<b>CÓDIGO</b>", ans_bold_style), Paragraph("<b>ACTIVIDAD / CONCEPTO NIIF</b>", ans_bold_style), Paragraph("<b>EFECTO EN CAJA (COP)</b>", ans_bold_style)],
        [Paragraph("<b>ACTIVIDADES</b>", ans_bold_style), Paragraph("<b>ACTIVIDADES DE INVERSIÓN</b>", ans_bold_style), Paragraph("", ans_bold_style)],
        [Paragraph("2320", body_style), Paragraph("Adquisiciones de activos a contratistas de obra", body_style), Paragraph("-$568.800", body_style)],
        [Paragraph("<b>SUBTOTAL</b>", ans_bold_style), Paragraph("<b>SUBTOTAL FLUJO NETO DE INVERSIÓN</b>", ans_bold_style), Paragraph("<b>-$568.800</b>", ans_bold_style)],
        [Paragraph("<b>ACTIVIDADES</b>", ans_bold_style), Paragraph("<b>ACTIVIDADES DE OPERACIÓN</b>", ans_bold_style), Paragraph("", ans_bold_style)],
        [Paragraph("1355", body_style), Paragraph("Anticipo de impuestos y retenciones", body_style), Paragraph("-$431.080", body_style)],
        [Paragraph("1435", body_style), Paragraph("Variación de inventarios comerciales", body_style), Paragraph("-$4.662.000", body_style)],
        [Paragraph("2465", body_style), Paragraph("Retención en la fuente por pagar", body_style), Paragraph("$442.490", body_style)],
        [Paragraph("2468", body_style), Paragraph("Impuesto de ICA retenido a terceros", body_style), Paragraph("$95.400", body_style)],
        [Paragraph("2570/2580", body_style), Paragraph("Pasivos laborales y de seguridad social", body_style), Paragraph("-$1.300.734", body_style)],
        [Paragraph("2610", body_style), Paragraph("Provisión para obligaciones laborales", body_style), Paragraph("$1.605.003", body_style)],
        [Paragraph("<b>SUBTOTAL</b>", ans_bold_style), Paragraph("<b>SUBTOTAL FLUJO NETO OPERACIONAL</b>", ans_bold_style), Paragraph("<b>-$4.250.921</b>", ans_bold_style)],
        [Paragraph("<b>ACTIVIDADES</b>", ans_bold_style), Paragraph("<b>ACTIVIDADES DE FINANCIACIÓN</b>", ans_bold_style), Paragraph("", ans_bold_style)],
        [Paragraph("2105", body_style), Paragraph("Amortización pasivos financieros (Bancos nacionales)", body_style), Paragraph("-$30.222.643", body_style)],
        [Paragraph("<b>SUBTOTAL</b>", ans_bold_style), Paragraph("<b>SUBTOTAL FLUJO NETO DE FINANCIACIÓN</b>", ans_bold_style), Paragraph("<b>-$30.222.643</b>", ans_bold_style)],
        [Paragraph("<b>PARTIDAS</b>", ans_bold_style), Paragraph("<b>PARTIDAS QUE NO AFECTAN EL EFECTIVO (CONCILIACIÓN)</b>", ans_bold_style), Paragraph("", ans_bold_style)],
        [Paragraph("3610/3710", body_style), Paragraph("Pérdidas acumuladas y del ejercicio", body_style), Paragraph("-$34.309.153", body_style)],
        [Paragraph("1592", body_style), Paragraph("Depreciación acumulada del período", body_style), Paragraph("$1.279.533", body_style)],
        [Paragraph("<b>SUBTOTAL</b>", ans_bold_style), Paragraph("<b>SUBTOTAL PARTIDAS NO MONETARIAS</b>", ans_bold_style), Paragraph("<b>-$33.029.620</b>", ans_bold_style)],
        [Paragraph("<b>TOTAL</b>", ans_bold_style), Paragraph("<b>DISMINUCIÓN NETA DEL EFECTIVO EN EL PERÍODO</b>", ans_bold_style), Paragraph("<b>-$68.071.984</b>", ans_bold_style)],
        [Paragraph("<b>SALDO INI</b>", ans_bold_style), Paragraph("<b>EFECTIVO Y EQUIVALENTES AL INICIO (MARZO 2026)</b>", ans_bold_style), Paragraph("<b>$93.502.800</b>", ans_bold_style)],
        [Paragraph("<b>SALDO FIN</b>", ans_bold_style), Paragraph("<b>EFECTIVO Y EQUIVALENTES AL FINAL (ABRIL 2026)</b>", ans_bold_style), Paragraph("<b>$25.430.816</b>", ans_bold_style)]
    ]
    fe_table = Table(fe_data, colWidths=[80, 312, 140])
    fe_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0B192C")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#FFFFFF")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,11), (-1,11), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (0,12), (-1,12), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,14), (-1,14), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (0,15), (-1,15), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,18), (-1,18), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (0,19), (-1,19), colors.HexColor("#FECACA")),
        ('BACKGROUND', (0,20), (-1,20), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (0,21), (-1,21), colors.HexColor("#FEF08A")),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(fe_table)
    story.append(Spacer(1, 8))

    # ESTADO DE CAMBIOS EN EL PATRIMONIO
    story.append(Paragraph("<b>B. ESTADO DE CAMBIOS EN EL PATRIMONIO (ABRIL 2026)</b>", h2_style))
    ecp_data = [
        [Paragraph("<b>RUBRO PATRIMONIAL</b>", ans_bold_style), Paragraph("<b>SALDO MARZO</b>", ans_bold_style), Paragraph("<b>AUMENTOS</b>", ans_bold_style), Paragraph("<b>DISMINUCIONES</b>", ans_bold_style), Paragraph("<b>SALDO ABRIL</b>", ans_bold_style)],
        [Paragraph("3105 Capital Suscrito y Pagado", body_style), Paragraph("$248.600.000", body_style), Paragraph("$0", body_style), Paragraph("$0", body_style), Paragraph("$248.600.000", body_style)],
        [Paragraph("3305 Reservas Obligatorias (10%)", body_style), Paragraph("$1.827.343", body_style), Paragraph("$0", body_style), Paragraph("$0", body_style), Paragraph("$1.827.343", body_style)],
        [Paragraph("3610 Pérdida del Ejercicio", body_style), Paragraph("-$17.154.577", body_style), Paragraph("$9.267.419", body_style), Paragraph("$0", body_style), Paragraph("-$7.887.158", body_style)],
        [Paragraph("3705 Utilidades Acumuladas", body_style), Paragraph("$16.446.082", body_style), Paragraph("$0", body_style), Paragraph("$0", body_style), Paragraph("$16.446.082", body_style)],
        [Paragraph("3710 Pérdidas Acumuladas", body_style), Paragraph("-$1.271.250", body_style), Paragraph("$0", body_style), Paragraph("-$17.154.577", body_style), Paragraph("-$18.425.827", body_style)],
        [Paragraph("<b>TOTAL PATRIMONIO NETO</b>", ans_bold_style), Paragraph("<b>$248.447.598</b>", ans_bold_style), Paragraph("<b>$9.267.419</b>", ans_bold_style), Paragraph("<b>-$17.154.577</b>", ans_bold_style), Paragraph("<b>$240.560.440</b>", ans_bold_style)]
    ]
    ecp_table = Table(ecp_data, colWidths=[152, 95, 95, 95, 95])
    ecp_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0B192C")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#FFFFFF")),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#FEF08A")),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(ecp_table)
    story.append(Spacer(1, 8))

    # FIRMAS
    story.append(Paragraph("<b>C. FIRMAS OFICIALES DE CERTIFICACIÓN Y DICTAMEN:</b>", h2_style))
    sign_data = [
        [
            Paragraph("______________________________<br/><b>GINA VILLAMIZAR</b><br/>Contadora Pública Titular<br/>T.P. 248910-T • Especialista NIIF", ParagraphStyle('SignP', fontName='Helvetica', fontSize=7.5, leading=10, alignment=1)),
            Paragraph("______________________________<br/><b>KEVIN GUERRERO</b><br/>Representante Legal<br/>Gerencia General • ELECTROVIVIENDA S.A.S", ParagraphStyle('SignP', fontName='Helvetica', fontSize=7.5, leading=10, alignment=1)),
            Paragraph("______________________________<br/><b>MARCELA GONZALES</b><br/>Revisora Fiscal Independiente<br/>T.P. 182740-T • Dictamen Sin Salvedades", ParagraphStyle('SignP', fontName='Helvetica', fontSize=7.5, leading=10, alignment=1)),
        ]
    ]
    sign_table = Table(sign_data, colWidths=[177, 177, 178])
    sign_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(sign_table)
    story.append(Spacer(1, 10))

    # 4. GLOSARIO
    story.append(make_section_banner("4. GLOSARIO Y REFERENCIAS TÉCNICAS"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("• <b>Efectivo:</b> Comprende la moneda de curso legal en caja general y los depósitos bancarios a la vista a favor del ente económico.", bullet_style))
    story.append(Paragraph("• <b>Equivalente de Efectivo:</b> Depósitos e inversiones financieras de gran liquidez con vencimiento no superior a 3 meses convertibles en importes conocidos de caja.", bullet_style))
    story.append(Paragraph("• <b>Flujos de Efectivo:</b> Entradas y salidas de efectivo y equivalentes de efectivo clasificados en operación, inversión y financiación.", bullet_style))
    story.append(Paragraph("• <b>Patrimonio:</b> Parte residual de los activos de la entidad una vez deducidos todos sus pasivos.", bullet_style))
    story.append(Paragraph("• <b>NIC 7 / NIIF PYMES Sección 7:</b> Norma internacional reguladora del estado de flujos de efectivo.", bullet_style))
    story.append(Paragraph("• <b>NIC 1 / NIIF PYMES Sección 6:</b> Marco técnico regulador del estado de cambios en el patrimonio.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Guia 24 successfully generated at: {filename}")

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "guia_24_resuelta.pdf"
    build_pdf(out_path)

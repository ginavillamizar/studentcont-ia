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
            self.drawString(40, 755, "SERVICIO NACIONAL DE APRENDIZAJE SENA — GUÍA DE APRENDIZAJE Nº 23 RESUELTA")
            self.setFont("Helvetica", 7)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawRightString(572, 755, "Estados Financieros NIIF, Notas y Revelaciones")
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
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#00324D"),
        alignment=1, # Center
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#39A900"),
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#FFFFFF"),
        spaceAfter=0
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#00324D"),
        spaceBefore=8,
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

    story.append(Paragraph("GUÍA Nº 23: ESTADO DE SITUACIÓN FINANCIERA, ESTADO DE RESULTADOS INTEGRAL, NOTAS Y REVELACIONES", title_style))
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
        [Paragraph("<b>Actividad de Aprendizaje:</b>", body_style), Paragraph("AA_23: Preparar estado de situación financiera y estado de resultados integral utilizando software especializado según normativa y políticas contables", body_style)],
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
    story.append(make_section_banner("2. PRESENTACIÓN Y MARCO INTRODUCTORIO"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Los estados financieros son informes contables estructurados y fundamentales para conocer la verdadera situación financiera y el desempeño operativo de una organización bajo las Normas Internacionales de Información Financiera (NIIF / DUR 2420 de 2015). Ofrecen un panorama verídico de los bienes y derechos controlados (Activos), las obligaciones contraídas (Pasivos), la participación de los accionistas (Patrimonio) y el resultado integral de las operaciones del período. La información de alta calidad es el instrumento más potente para la toma de decisiones económicas acertadas.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # 3.1 REFLEXIÓN INICIAL
    story.append(make_section_banner("3.1 ACTIVIDADES DE REFLEXIÓN INICIAL (ECONOMÍA DEL HOGAR)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Instrucción:</b> Escoja al miembro(s) de su hogar a cargo del control financiero y elabore un informe financiero del hogar respondiendo a las siguientes preguntas:",
        body_style
    ))
    story.append(Spacer(1, 3))

    # P1
    story.append(Paragraph("<b>1. ¿Cuánto es el valor de sus bienes y cuentas por cobrar? (Activos)</b>", q_style))
    p1_ans = [
        Paragraph("<b>Total Activos del Hogar: $23.800.000 COP</b>, discriminados detalladamente así:", ans_box_style),
        Paragraph("• <b>Efectivo y Disponible:</b> $2.800.000 (Cuentas de ahorro en Bancolombia y efectivo disponible para contingencias).", bullet_style),
        Paragraph("• <b>Bienes Muebles y Enseres:</b> $12.000.000 (Nevera, lavadora, televisor, computadores, comedor y juegos de alcoba valorados al costo estimado de reposición).", bullet_style),
        Paragraph("• <b>Vehículo / Transporte:</b> $8.500.000 (Motocicleta familiar para transporte al trabajo y estudio).", bullet_style),
        Paragraph("• <b>Cuentas por Cobrar:</b> $500.000 (Préstamo temporal otorgado a un familiar con recuperación en 30 días).", bullet_style)
    ]
    story.append(make_answer_box(p1_ans))
    story.append(Spacer(1, 6))

    # P2
    story.append(Paragraph("<b>2. ¿Cuánto es el valor de sus deudas? (Pasivos)</b>", q_style))
    p2_ans = [
        Paragraph("<b>Total Pasivos del Hogar: $6.350.000 COP</b>, desglosados en:", ans_box_style),
        Paragraph("• <b>Crédito Bancario de Consumo / Libre Inversión:</b> $4.200.000 (Saldo capital pendiente en cuotas mensuales).", bullet_style),
        Paragraph("• <b>Tarjetas de Crédito Comerciales:</b> $1.300.000 (Compras diferidas de electrodomésticos y mercado).", bullet_style),
        Paragraph("• <b>Pasivos Corrientes de Servicios y Vivienda:</b> $850.000 (Recibos de energía, agua, gas, internet y canon de arriendo por pagar a fin de mes).", bullet_style)
    ]
    story.append(make_answer_box(p2_ans))
    story.append(Spacer(1, 6))

    # P3
    story.append(Paragraph("<b>3. ¿Cuánto es el valor de su patrimonio? (Ecuación Patrimonial: Activo – Pasivo)</b>", q_style))
    p3_ans = [
        Paragraph("<b>Patrimonio Neto del Hogar: $17.450.000 COP</b>", ans_box_style),
        Paragraph("<b>Fórmula de cálculo contable:</b> Patrimonio = Activos ($23.800.000) – Pasivos ($6.350.000) = <b>$17.450.000</b>.<br/><i>Interpretación:</i> Representa la riqueza neta y real de la que la familia es propietaria absoluta libre de gravámenes o deudas externas.", ans_box_style)
    ]
    story.append(make_answer_box(p3_ans))
    story.append(Spacer(1, 6))

    # P4
    story.append(Paragraph("<b>4. ¿Cuánto reciben de ingresos mensuales?</b>", q_style))
    p4_ans = [
        Paragraph("<b>Total Ingresos Mensuales: $4.400.000 COP</b>", ans_box_style),
        Paragraph("• Salarios laborales netos de los miembros que aportan al hogar: $3.800.000.<br/>• Ingresos complementarios independientes (servicios y ventas menores): $600.000.", bullet_style)
    ]
    story.append(make_answer_box(p4_ans))
    story.append(Spacer(1, 6))

    # P5
    story.append(Paragraph("<b>5. ¿Cuánto gastan mensualmente?</b>", q_style))
    p5_ans = [
        Paragraph("<b>Total Gastos Mensuales: $3.900.000 COP</b>", ans_box_style),
        Paragraph("• <b>Alimentación, mercado y canasta familiar:</b> $1.500.000.<br/>• <b>Vivienda (arriendo, servicios públicos y administración):</b> $1.200.000.<br/>• <b>Transporte y movilidad:</b> $450.000.<br/>• <b>Educación, salud y bienestar:</b> $400.000.<br/>• <b>Gastos financieros (intereses bancarios):</b> $350.000.", bullet_style)
    ]
    story.append(make_answer_box(p5_ans))
    story.append(Spacer(1, 6))

    # P6
    story.append(Paragraph("<b>6. ¿Cuánto es el valor que les queda de los ingresos (Superávit / Excedente)?</b>", q_style))
    p6_ans = [
        Paragraph("<b>Excedente Neto Mensual (Ahorro): $500.000 COP</b>", ans_box_style),
        Paragraph("<b>Cálculo:</b> Ingresos ($4.400.000) – Gastos ($3.900.000) = <b>$500.000 COP</b> mensual.<br/>Representa una tasa de ahorro del <b>11,36%</b> de los ingresos brutos, destinada a fondo de imprevistos e inversión.", ans_box_style)
    ]
    story.append(make_answer_box(p6_ans))
    story.append(Spacer(1, 6))

    # P7
    story.append(Paragraph("<b>7. Opinión acerca de cómo se encuentra la situación financiera de su hogar:</b>", q_style))
    p7_ans = [
        Paragraph("El hogar goza de una situación financiera <b>estable, solvente y con liquidez positiva</b>. El nivel de endeudamiento es moderado y controlado (26,68% del activo total), lo que garantiza que los pasivos están respaldados 3,74 veces por los activos. Asimismo, el flujo de caja operativo es superavitario en $500.000 mensuales, lo que permite amortizar créditos anticipadamente y consolidar el patrimonio familiar sin recurrir a sobreendeudamiento.", ans_box_style)
    ]
    story.append(make_answer_box(p7_ans))
    story.append(Spacer(1, 10))

    # 3.2 CONTEXTUALIZACIÓN
    story.append(make_section_banner("3.2 ACTIVIDADES DE CONTEXTUALIZACIÓN (CONCEPTOS BÁSICOS)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Actividad 3.2.1:</b> Análisis del video 'Concepto y Uso de los Estados Financieros':", body_style))
    story.append(Spacer(1, 3))

    # Q 3.2.1
    story.append(Paragraph("<b>a) ¿A quiénes les interesa la información financiera y para qué les sirve?</b>", q_style))
    q_a_ans = [
        Paragraph("La información financiera interesa a usuarios internos y externos según el Marco Conceptual NIIF:", ans_box_style),
        Paragraph("1. <b>Inversionistas y Socios (Actuales y Potenciales):</b> Evalúan la rentabilidad, el riesgo de su inversión, la seguridad de su patrimonio y la capacidad de reparto de dividendos.", bullet_style),
        Paragraph("2. <b>Entidades Financieras y Prestamistas:</b> Determinan la capacidad de pago, liquidez y solvencia del ente para otorgar créditos y fijar tasas de interés.", bullet_style),
        Paragraph("3. <b>Proveedores y Acreedores Comerciales:</b> Deciden si otorgar plazos comerciales, límites de crédito y evaluar el riesgo de incobrabilidad.", bullet_style),
        Paragraph("4. <b>Gerencia y Administradores:</b> Monitorean la eficiencia operativa, controlan presupuestos y formulan estrategias de crecimiento y reducción de costos.", bullet_style),
        Paragraph("5. <b>Empleados y Sindicatos:</b> Analizan la estabilidad laboral, sostenibilidad empresarial y capacidad de negociación de beneficios.", bullet_style),
        Paragraph("6. <b>Gobierno y Entes de Fiscalización (DIAN, Supersociedades):</b> Verifican la correcta liquidación tributaria (Renta, IVA, Retenciones) y el cumplimiento de la ley comercial.", bullet_style)
    ]
    story.append(make_answer_box(q_a_ans))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>b) ¿Por qué son importantes los estados financieros para la empresa?</b>", q_style))
    q_b_ans = [
        Paragraph("Son el principal instrumento de comunicación de la realidad económica empresarial. Permiten: (1) Medir objetivamente el rendimiento económico; (2) Demostrar la rendición de cuentas de la gerencia sobre los recursos administrados; (3) Facilitar el acceso a fuentes de financiamiento bancario e inversión de capital; (4) Proyectar flujos de caja y presupuestos; y (5) Cumplir con los requerimientos legales y tributarios vigentes en Colombia.", ans_box_style)
    ]
    story.append(make_answer_box(q_b_ans))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>c) En sus palabras: ¿En qué consiste el Estado de Resultados?</b>", q_style))
    q_c_ans = [
        Paragraph("Es un informe financiero dinámico y acumulativo que resume el desempeño operativo de una empresa durante un período contable específico (ej. un mes o un año). Enfrenta todos los <b>ingresos devengados</b> frente a los <b>costos y gastos causados</b>, con el propósito de determinar si la operación generó una <b>Utilidad Neta</b> (ganancia) o una <b>Pérdida del Ejercicio</b>.", ans_box_style)
    ]
    story.append(make_answer_box(q_c_ans))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>d) En sus palabras: ¿En qué consiste el Estado de Situación Financiera?</b>", q_style))
    q_d_ans = [
        Paragraph("Es una 'fotografía' estática que muestra la situación patrimonial de la empresa a una fecha de corte determinada. Revela con precisión qué recursos económicos controla la empresa (<b>Activos</b>), qué obligaciones tiene contraídas con terceros (<b>Pasivos</b>) y cuál es el valor neto que verdaderamente les pertenece a los socios o dueños (<b>Patrimonio</b>), cumpliendo con la ecuación fundamental: <i>Activo = Pasivo + Patrimonio</i>.", ans_box_style)
    ]
    story.append(make_answer_box(q_d_ans))
    story.append(Spacer(1, 10))

    # 3.3.1 APROPIACIÓN
    story.append(make_section_banner("3.3.1 MARCO TÉCNICO NORMATIVO (NIC 1, MARCO CONCEPTUAL Y LEY 1314 DE 2009)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Rejilla Conceptual y Fundamentación Normativa Internacional:</b>", body_style))
    story.append(Spacer(1, 3))

    grid_data = [
        [Paragraph("<b>Concepto Normativo</b>", ans_bold_style), Paragraph("<b>Definición y Fundamento Técnico (NIC 1 / Marco Conceptual / DUR 2420)</b>", ans_bold_style)],
        [
            Paragraph("<b>1. Finalidad de los Estados Financieros (NIC 1.9)</b>", body_style),
            Paragraph("Suministrar información estructurada sobre la situación financiera, el rendimiento financiero y los flujos de efectivo de una entidad, que sea de utilidad a una amplia gama de usuarios al tomar decisiones económicas. Asimismo, demuestran los resultados de la gestión de la administración sobre los recursos que se le han encomendado.", body_style)
        ],
        [
            Paragraph("<b>2. Comprensibilidad</b>", body_style),
            Paragraph("La información debe ser clara, organizada y concisa, permitiendo que usuarios con un conocimiento razonable de las actividades económicas y contables puedan comprender su significado e impacto.", body_style)
        ],
        [
            Paragraph("<b>• Relevancia</b>", body_style),
            Paragraph("Cualidad por la cual la información ejerce influencia en las decisiones económicas de los usuarios, ayudándoles a evaluar sucesos pasados, presentes o futuros (valor predictivo) o bien a confirmar o corregir evaluaciones pasadas (valor confirmatorio).", body_style)
        ],
        [
            Paragraph("<b>• Materialidad o Importancia Relativa</b>", body_style),
            Paragraph("Una partida es material si su omisión, inexactitud o encubrimiento puede influir en las decisiones que los usuarios toman sobre la base de los estados financieros. Depende de la magnitud y de la naturaleza de la transacción evaluada en su contexto específico.", body_style)
        ],
        [
            Paragraph("<b>• Fiabilidad / Representación Fiel</b>", body_style),
            Paragraph("Para ser útil, la información debe representar fielmente las transacciones y demás sucesos, estando completa, neutral y libre de error material.", body_style)
        ],
        [
            Paragraph("<b>• Esencia sobre Forma</b>", body_style),
            Paragraph("Las transacciones y sucesos deben contabilizarse y presentarse de acuerdo con su esencia y realidad económica, y no meramente según su forma estrictamente legal.", body_style)
        ],
        [
            Paragraph("<b>• Prudencia</b>", body_style),
            Paragraph("Es la inclusión de cierto grado de precaución al realizar los juicios necesarios para hacer las estimaciones requeridas en condiciones de incertidumbre, de tal manera que los activos o ingresos no se sobrevaloren y los pasivos o gastos no se subvaloren.", body_style)
        ],
        [
            Paragraph("<b>• Integridad</b>", body_style),
            Paragraph("Para ser fiable, la información contenida en los estados financieros debe ser completa dentro de los límites de la importancia relativa y el costo.", body_style)
        ],
        [
            Paragraph("<b>• Comparabilidad</b>", body_style),
            Paragraph("Permite a los usuarios identificar y comprender las similitudes y diferencias entre partidas de la misma entidad a lo largo del tiempo, y entre diferentes entidades en el mismo período.", body_style)
        ],
        [
            Paragraph("<b>• Oportunidad</b>", body_style),
            Paragraph("Implica proporcionar información a los responsables de la toma de decisiones a tiempo para que sea capaz de influir en sus decisiones antes de que pierda su capacidad de impacto.", body_style)
        ],
        [
            Paragraph("<b>• Costo - Beneficio</b>", body_style),
            Paragraph("Restricción general donde los beneficios obtenidos de la información deben superar los costos en que se incurre para suministrarla.", body_style)
        ],
        [
            Paragraph("<b>3. Declaración de Cumplimiento (NIC 1.16)</b>", body_style),
            Paragraph("Una entidad cuyos estados financieros cumplan las NIIF efectuará, en las notas, una declaración explícita y sin reservas de dicho cumplimiento. No se declarará que se cumplen las NIIF a menos que se hayan cumplido todos los requerimientos normativos aplicables.", body_style)
        ],
        [
            Paragraph("<b>4. Hipótesis de Negocio en Marcha (NIC 1.25)</b>", body_style),
            Paragraph("<b>Concepto:</b> Los estados financieros se preparan bajo el supuesto de que la entidad continuará en funcionamiento en el futuro previsible (mínimo 12 meses siguientes al corte).<br/><b>Indicios de Incumplimiento:</b> Posición de patrimonio neto negativo o capital de trabajo negativo; préstamos a plazo fijo cercanos al vencimiento sin posibilidad de renovación; pérdidas de explotación continuadas; imposibilidad de pagar a acreedores; huelgas laborales prolongadas; o pérdidas de licencias comerciales indispensables.", body_style)
        ],
        [
            Paragraph("<b>5. Base de Acumulación o Devengo (NIC 1.27)</b>", body_style),
            Paragraph("La entidad elaborará sus estados financieros (excepto en lo relacionado con los flujos de efectivo) utilizando la base contable de acumulación o devengo. Las partidas se reconocen como activos, pasivos, patrimonio, ingresos o gastos cuando satisfacen las definiciones y criterios de reconocimiento, sin depender de la fecha en que se perciba o desembolse el efectivo.", body_style)
        ]
    ]

    grid_table = Table(grid_data, colWidths=[160, 372])
    grid_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#00324D")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#FFFFFF")),
        ('BACKGROUND', (0,1), (0,-1), colors.HexColor("#F8FAFC")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(grid_table)
    story.append(Spacer(1, 10))

    # 3.3.2 CLASIFICACIÓN DE LOS ESTADOS FINANCIEROS
    story.append(make_section_banner("3.3.2 CLASIFICACIÓN DE LOS ESTADOS FINANCIEROS EN COLOMBIA"))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>1. Definición de Estados Financieros de Propósito General:</b>", q_style))
    ef_pg_ans = [
        Paragraph("Son aquellos que se preparan al cierre de un período contable para ser conocidos por un número indeterminado de usuarios (inversionistas, bancos, proveedores, empleados y público en general), con el fin de satisfacer su interés común de evaluar la situación patrimonial, el desempeño operativo y la capacidad de la entidad para generar flujos favorables de fondos, sin que ninguno de estos usuarios pueda exigir informes diseñados a su medida individual.", ans_box_style)
    ]
    story.append(make_answer_box(ef_pg_ans))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2. Los 5 Elementos de los Estados Financieros bajo Estándares Internacionales:</b>", q_style))
    elem_data = [
        [Paragraph("<b>Elemento</b>", ans_bold_style), Paragraph("<b>Definición Técnica Internacional (Marco Conceptual NIIF)</b>", ans_bold_style)],
        [Paragraph("<b>ACTIVO</b>", body_style), Paragraph("Recurso económico presente controlado por la entidad como resultado de sucesos pasados. Un recurso económico es un derecho que tiene el potencial de producir beneficios económicos futuros para la organización.", body_style)],
        [Paragraph("<b>PASIVO</b>", body_style), Paragraph("Obligación presente de la entidad de transferir un recurso económico como resultado de sucesos pasados. La entidad no tiene la capacidad práctica de evitar liquidar dicha obligación.", body_style)],
        [Paragraph("<b>PATRIMONIO</b>", body_style), Paragraph("Parte residual de los activos de la entidad, una vez deducidos todos sus pasivos (<i>Patrimonio = Activos – Pasivos</i>). Representa el valor neto perteneciente a los dueños o accionistas.", body_style)],
        [Paragraph("<b>INGRESOS</b>", body_style), Paragraph("Incrementos en los beneficios económicos producidos a lo largo del período contable, en forma de entradas o aumentos en el valor de los activos, o disminuciones de pasivos, que dan como resultado aumentos en el patrimonio, distintos de los aportes de capital de los socios.", body_style)],
        [Paragraph("<b>GASTOS (Y COSTOS)</b>", body_style), Paragraph("Disminuciones en los beneficios económicos a lo largo del período contable, en forma de salidas o disminuciones en el valor de los activos, o incurrimiento en pasivos, que dan como resultado disminuciones en el patrimonio, distintas de las distribuciones de utilidades a los socios.", body_style)]
    ]
    elem_table = Table(elem_data, colWidths=[110, 422])
    elem_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,1), (0,-1), colors.HexColor("#F8FAFC")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(elem_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>3. Juegos Completos de Estados Financieros según los Grupos en Colombia (DUR 2420 de 2015):</b>", q_style))
    grupos_data = [
        [Paragraph("<b>Grupo Contable</b>", ans_bold_style), Paragraph("<b>Marco Técnico Aplicable</b>", ans_bold_style), Paragraph("<b>Juego Completo de Estados Financieros Obligatorios</b>", ans_bold_style)],
        [
            Paragraph("<b>GRUPO 1</b><br/>Grandes Empresas y Emisores", body_style),
            Paragraph("NIIF Plenas<br/>(Decreto 2784 / DUR 2420)", body_style),
            Paragraph("1. Estado de Situación Financiera.<br/>2. Estado de Resultado y Otro Resultado Integral (ORI).<br/>3. Estado de Cambios en el Patrimonio.<br/>4. Estado de Flujos de Efectivo.<br/>5. Notas y Políticas Contables.", body_style)
        ],
        [
            Paragraph("<b>GRUPO 2</b><br/>PYMES (Mediana y Pequeña)", body_style),
            Paragraph("NIIF para las PYMES<br/>(Decreto 3022 / DUR 2420)", body_style),
            Paragraph("1. Estado de Situación Financiera.<br/>2. Estado de Resultado Integral (o Estado de Resultados + ORI).<br/>3. Estado de Cambios en el Patrimonio.<br/>4. Estado de Flujos de Efectivo.<br/>5. Notas y Revelaciones a los Estados Financieros.", body_style)
        ],
        [
            Paragraph("<b>GRUPO 3</b><br/>Microempresas", body_style),
            Paragraph("Régimen Simplificado<br/>(Decreto 2706 / DUR 2420)", body_style),
            Paragraph("1. Estado de Situación Financiera simplificado.<br/>2. Estado de Resultados.<br/>3. Notas a los estados financieros.", body_style)
        ],
        [
            Paragraph("<b>ENTIDADES EN LIQUIDACIÓN</b>", body_style),
            Paragraph("Marco Especial de Liquidación<br/>(Decreto 2101 / DUR 2420)", body_style),
            Paragraph("1. Estado de Situación Financiera de Liquidación.<br/>2. Estado de Resultado Integral de Liquidación.<br/>3. Notas explicativas sobre base de valor neto de liquidación.", body_style)
        ]
    ]
    grupos_table = Table(grupos_data, colWidths=[120, 140, 272])
    grupos_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,1), (0,-1), colors.HexColor("#F8FAFC")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(grupos_table)
    story.append(Spacer(1, 10))

    # 3.3.3 ESTRUCTURA Y PRESENTACIÓN
    story.append(make_section_banner("3.3.3 ESTRUCTURA Y PRESENTACIÓN DEL ESF Y DEL ESTADO DE RESULTADOS (NIC 1)"))
    story.append(Spacer(1, 4))

    # ESF
    story.append(Paragraph("<b>A. Estado de Situación Financiera (NIC 1.60 – 1.78):</b>", h2_style))
    esf_pres_ans = [
        Paragraph("<b>1. Criterios de Clasificación:</b>", ans_bold_style),
        Paragraph("• <b>Entre Corrientes y No Corrientes (Criterio principal):</b> Un activo o pasivo se clasifica como <i>corriente</i> si se espera realizar, vender, consumir o liquidar dentro del ciclo normal de operación de la entidad (máximo 12 meses contados desde la fecha de corte). En caso contrario, se clasificará como <i>no corriente</i>.<br/>• <b>Por Orden de Liquidez:</b> Se aplica cuando proporciona información más fiable y relevante (propio de instituciones financieras).<br/>• <b>Regla NIIF clave:</b> Los activos y pasivos por <b>impuestos diferidos nunca</b> se clasificarán como de corto plazo (siempre son no corrientes).", ans_box_style),
        Spacer(1, 3),
        Paragraph("<b>2. Partidas Mínimas a Presentar en el ESF (NIC 1.54):</b>", ans_bold_style),
        Paragraph("Efectivo y equivalentes al efectivo; Deudores comerciales y otras cuentas por cobrar; Inventarios; Activos financieros; Propiedades, planta y equipo; Propiedades de inversión; Activos intangibles; Acreedores comerciales y otras cuentas por pagar; Provisiones; Pasivos financieros; Pasivos y activos por impuestos corrientes; Impuestos diferidos; Participaciones no controladoras; y Capital emitido y reservas atribuibles a los propietarios.", ans_box_style)
    ]
    story.append(make_answer_box(esf_pres_ans, "ESTRUCTURA DEL ESF"))
    story.append(Spacer(1, 6))

    # ERI
    story.append(Paragraph("<b>B. Estado de Resultado Integral (NIC 1.81 – 1.105):</b>", h2_style))
    eri_pres_ans = [
        Paragraph("<b>1. Opciones de Presentación (NIC 1.81):</b>", ans_bold_style),
        Paragraph("• <b>En un solo estado:</b> Presenta en un único documento continuo tanto el resultado operativo del período como las partidas del Otro Resultado Integral (ORI).<br/>• <b>En dos estados separados:</b> Primer informe que muestra el Estado de Resultados separado (con la ganancia o pérdida neta), seguido inmediatamente por un segundo informe con el Estado del Resultado Integral (que inicia con el resultado del período y añade las partidas de ORI).", ans_box_style),
        Spacer(1, 3),
        Paragraph("<b>2. Clasificación de Gastos (NIC 1.99):</b>", ans_bold_style),
        Paragraph("• <b>Por Naturaleza (NIC 1.102):</b> Se agrupan según su esencia económica sin redistribuirlos dentro de las áreas de la entidad (ej. variación de inventarios, compras de materias primas, sueldos y salarios, depreciación y amortización).<br/>• <b>Por Función o Costo de Ventas (NIC 1.103):</b> Se clasifican según su destino operativo (Costo de ventas, Gastos de administración, Gastos de distribución y ventas). Requiere revelar en notas la naturaleza de los gastos.<br/>• <b>Prohibición expresa (NIC 1.87):</b> <i>No se permite presentar ninguna partida de ingresos o gastos como 'Partida Extraordinaria'</i> ni en los estados financieros ni en las notas.", ans_box_style)
    ]
    story.append(make_answer_box(eri_pres_ans, "ESTRUCTURA DEL ERI"))
    story.append(Spacer(1, 10))

    # 3.3.4 NOTAS Y REVELACIONES
    story.append(make_section_banner("3.3.4 ESTRUCTURA DE LAS NOTAS Y REVELACIONES (NIC 1.112–138 Y NIC 8)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Los 5 Elementos Fundamentales de las Notas a los Estados Financieros:</b>", body_style))
    story.append(Spacer(1, 3))

    notas_elements_data = [
        [Paragraph("<b>Elemento</b>", ans_bold_style), Paragraph("<b>Contenido Obligatorio y Referencia Técnica NIIF</b>", ans_bold_style)],
        [
            Paragraph("<b>1. Identificación y Domicilio</b>", body_style),
            Paragraph("Nombre de la entidad reportante (razón social), NIT, domicilio principal, forma legal, país de constitución, dirección de la sede y descripción de la naturaleza de sus operaciones principales y actividades de negocio.", body_style)
        ],
        [
            Paragraph("<b>2. Declaración de Cumplimiento</b>", body_style),
            Paragraph("Declaración explícita y sin reservas de que los estados financieros han sido preparados de acuerdo con las Normas Internacionales de Información Financiera (DUR 2420 de 2015).", body_style)
        ],
        [
            Paragraph("<b>3. Resumen de Políticas Contables</b>", body_style),
            Paragraph("Bases de medición empleadas (costo histórico, costo amortizado, valor razonable); juicios de la gerencia al aplicar políticas; y supuestos clave sobre la incertidumbre en las estimaciones futuras que tengan riesgo significativo de ajustes en el ejercicio próximo.", body_style)
        ],
        [
            Paragraph("<b>4. Desglose Numérico de Partidas (Información de Apoyo)</b>", body_style),
            Paragraph("Información de respaldo y desagregación analítica para las partidas presentadas en el ESF, ERI, Cambios en el Patrimonio y Flujos de Efectivo, presentadas en el mismo orden sistemático de las cuentas de balance y de resultados.", body_style)
        ],
        [
            Paragraph("<b>5. Otras Revelaciones Relevantes</b>", body_style),
            Paragraph("Pasivos contingentes y compromisos contractuales no reconocidos en el balance; información de partes relacionadas; objetivos y políticas de gestión de riesgo financiero y de capital; y hechos posteriores al cierre.", body_style)
        ]
    ]
    notas_table = Table(notas_elements_data, colWidths=[150, 382])
    notas_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#00324D")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#FFFFFF")),
        ('BACKGROUND', (0,1), (0,-1), colors.HexColor("#F8FAFC")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(notas_table)
    story.append(Spacer(1, 10))

    # 3.4 TRANSFERENCIA DEL CONOCIMIENTO (PROYECTO FORMATIVO)
    story.append(make_section_banner("3.4 ACTIVIDADES DE TRANSFERENCIA DEL CONOCIMIENTO (CASO PRÁCTICO EMPRESA)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Aplicación al Proyecto Formativo:</b> A continuación se presentan los estados financieros oficiales preparados con la herramienta didáctica contable para la empresa formativa <b>ELECTROVIVIENDA S.A.S. (NIT: 901.765.438-3)</b>, clasificada en el <b>Grupo 2 (NIIF para las PYMES)</b>:",
        body_style
    ))
    story.append(Spacer(1, 3))

    # ESF RESUMEN
    story.append(Paragraph("<b>A. ESTADO DE SITUACIÓN FINANCIERA CLASIFICADO — ABRIL 2026</b>", h2_style))
    esf_data = [
        [Paragraph("<b>CÓDIGO</b>", ans_bold_style), Paragraph("<b>CUENTA / CONCEPTO NIIF</b>", ans_bold_style), Paragraph("<b>SALDO NETO OFICIAL (COP)</b>", ans_bold_style)],
        [Paragraph("11", body_style), Paragraph("Efectivo y Equivalentes al Efectivo (Caja y Bancos)", body_style), Paragraph("$93.502.800", body_style)],
        [Paragraph("13", body_style), Paragraph("Cuentas Comerciales por Cobrar y Anticipos", body_style), Paragraph("$5.568.100", body_style)],
        [Paragraph("14", body_style), Paragraph("Inventarios de Mercancías (Promedio Ponderado)", body_style), Paragraph("$4.662.000", body_style)],
        [Paragraph("<b>TOTAL</b>", ans_bold_style), Paragraph("<b>TOTAL ACTIVOS CORRIENTES</b>", ans_bold_style), Paragraph("<b>$103.732.900</b>", ans_bold_style)],
        [Paragraph("15", body_style), Paragraph("Propiedad, Planta y Equipo (Terrenos, Vehículos, Muebles)", body_style), Paragraph("$227.499.783", body_style)],
        [Paragraph("<b>TOTAL</b>", ans_bold_style), Paragraph("<b>TOTAL ACTIVO (CORRIENTE + NO CORRIENTE)</b>", ans_bold_style), Paragraph("<b>$331.232.683</b>", ans_bold_style)],
        [Paragraph("21-26", body_style), Paragraph("Pasivos Corrientes (Proveedores, Impuestos, Laborales)", body_style), Paragraph("$90.672.243", body_style)],
        [Paragraph("3105", body_style), Paragraph("Capital Social (Capital Suscrito y Pagado - 5 Socios)", body_style), Paragraph("$248.600.000", body_style)],
        [Paragraph("3305", body_style), Paragraph("Reservas Obligatorias (Reserva Legal 10%)", body_style), Paragraph("$1.827.343", body_style)],
        [Paragraph("36/37", body_style), Paragraph("Resultados Acumulados y del Ejercicio", body_style), Paragraph("-$9.866.903", body_style)],
        [Paragraph("<b>TOTAL</b>", ans_bold_style), Paragraph("<b>TOTAL PATRIMONIO</b>", ans_bold_style), Paragraph("<b>$240.560.440</b>", ans_bold_style)],
        [Paragraph("<b>SUMAS</b>", ans_bold_style), Paragraph("<b>TOTAL PASIVO Y PATRIMONIO (SUMAS IGUALES)</b>", ans_bold_style), Paragraph("<b>$331.232.683</b>", ans_bold_style)]
    ]
    esf_table = Table(esf_data, colWidths=[70, 312, 150])
    esf_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0B192C")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#FFFFFF")),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#FEF08A")),
        ('BACKGROUND', (0,11), (-1,11), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (0,12), (-1,12), colors.HexColor("#FEF08A")),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(esf_table)
    story.append(Spacer(1, 8))

    # ERI RESUMEN
    story.append(Paragraph("<b>B. ESTADO DE RESULTADOS INTEGRAL — ABRIL 2026</b>", h2_style))
    eri_data = [
        [Paragraph("<b>RUBRO CONTABLE</b>", ans_bold_style), Paragraph("<b>CONCEPTO OPERACIONAL</b>", ans_bold_style), Paragraph("<b>VALOR COP</b>", ans_bold_style)],
        [Paragraph("Ingresos Ordinarios (4135)", body_style), Paragraph("Comercio al por mayor y al detal de electrodomésticos", body_style), Paragraph("$8.524.000", body_style)],
        [Paragraph("Menos: Devoluciones (4175)", body_style), Paragraph("Devoluciones y descuentos concedidos en venta", body_style), Paragraph("-$1.560.000", body_style)],
        [Paragraph("<b>Ingresos Operacionales Netos</b>", ans_bold_style), Paragraph("Base de comercialización", ans_bold_style), Paragraph("<b>$6.964.000</b>", ans_bold_style)],
        [Paragraph("Menos: Costo de Ventas (6135)", body_style), Paragraph("Costo promedio ponderado de la mercancía vendida", body_style), Paragraph("-$4.018.000", body_style)],
        [Paragraph("<b>Utilidad Bruta en Ventas</b>", ans_bold_style), Paragraph("Margen comercial bruto", ans_bold_style), Paragraph("<b>$2.946.000</b>", ans_bold_style)],
        [Paragraph("Gastos Operacionales (51/52)", body_style), Paragraph("Beneficios a empleados, nómina y depreciaciones", body_style), Paragraph("-$10.386.009", body_style)],
        [Paragraph("Gastos Financieros (5305)", body_style), Paragraph("Intereses bancarios y comisiones", body_style), Paragraph("-$1.289.650", body_style)],
        [Paragraph("Otros Ingresos Financieros (4210)", body_style), Paragraph("Rendimientos bancarios", body_style), Paragraph("$1.192.500", body_style)],
        [Paragraph("<b>RESULTADO DEL EJERCICIO</b>", ans_bold_style), Paragraph("<b>PÉRDIDA NETA DEL PERÍODO (ABRIL 2026)</b>", ans_bold_style), Paragraph("<b>-$7.887.158</b>", ans_bold_style)]
    ]
    eri_table = Table(eri_data, colWidths=[160, 242, 130])
    eri_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0B192C")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#FFFFFF")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (0,9), (-1,9), colors.HexColor("#FECACA")),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(eri_table)
    story.append(Spacer(1, 8))

    # FIRMAS OFICIALES REGLAMENTARIAS
    story.append(Paragraph("<b>C. FIRMAS OFICIALES DE LEGALIZACIÓN DE LOS ESTADOS FINANCIEROS:</b>", h2_style))
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

    # 4. GLOSARIO Y REFERENTES
    story.append(make_section_banner("4. GLOSARIO DE TÉRMINOS Y REFERENCIAS BIBLIOGRÁFICAS"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("• <b>Estados Financieros:</b> Juego completo estructurado que comprende: Estado de Situación Financiera al final del período; Estado del Resultado Integral del período; Estado de Cambios en el Patrimonio; Estado de Flujos de Efectivo; y Notas contentivas de políticas contables y revelaciones explicativas.", bullet_style))
    story.append(Paragraph("• <b>Estados de Propósito General:</b> Informes que satisfacen las necesidades comunes de usuarios indeterminados que no están en condiciones de exigir informes a la medida.", bullet_style))
    story.append(Paragraph("• <b>Carvalho, J. (2010):</b> Estados Financieros. Normas para su preparación y presentación. Bogotá: Ecoe Ediciones.", bullet_style))
    story.append(Paragraph("• <b>Estupiñán, R., Sierra, A (2012):</b> Estados financieros básicos bajo NIC/NIIF. Bogotá: Ecoe Ediciones.", bullet_style))
    story.append(Paragraph("• <b>Ley 1314 de 2009 y Decreto Único Reglamentario 2420 de 2015:</b> Marco técnico contable obligatorio en Colombia.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {filename}")

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "guia_23_resuelta.pdf"
    build_pdf(out_path)

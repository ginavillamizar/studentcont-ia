# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
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
        self.setFont("Helvetica-Bold", 7)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header
        self.drawString(30, 762, "SENA CSET BUCARAMANGA | GUIA No. 32 PRESUPUESTO | INFOGRAFIA VISUAL 3.3.1 | GINA VILLAMIZAR")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(30, 757, 582, 757)
            
        # Footer
        page_text = f"Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(582, 18, page_text)
        self.drawString(30, 18, "INFOGRAFIA TEORICA VISUAL: DIAGNOSTICO, PRINCIPIOS, CLASIFICACION Y CICLO PRESUPUESTAL")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(30, 26, 582, 26)
        self.restoreState()

def generate_infografia():
    pdf_path = "/Users/ginavillamizar/Downloads/CONTABILIDAD/GUIA_32_INFOGRAFIA_PRESUPUESTAL_GINA_VILLAMIZAR.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=30,
        rightMargin=30,
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()
    
    primary = colors.HexColor("#0B192C")
    gold = colors.HexColor("#D4AF37")
    emerald = colors.HexColor("#047857")
    slate_dark = colors.HexColor("#1E293B")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=13,
        textColor=primary,
        alignment=TA_CENTER
    )
    
    sub_title_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=emerald,
        alignment=TA_CENTER
    )

    sec_title = ParagraphStyle(
        'SecTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=primary
    )

    card_header = ParagraphStyle(
        'CardHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9,
        textColor=colors.white
    )

    card_body = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.4,
        leading=8.2,
        textColor=slate_dark,
        alignment=TA_JUSTIFY
    )

    flow_box = ParagraphStyle(
        'FlowBox',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.5,
        leading=8.2,
        textColor=primary,
        alignment=TA_CENTER
    )

    icons_dir = "/Users/ginavillamizar/Downloads/CONTABILIDAD/assets/icons"

    story = []

    # ENCABEZADO
    story.append(Paragraph("SERVICIO NACIONAL DE APRENDIZAJE - SENA", title_style))
    story.append(Paragraph("CENTRO DE SERVICIOS EMPRESARIALES Y TURISTICOS • GESTION CONTABLE Y FINANCIERA", sub_title_style))
    story.append(Paragraph("INFOGRAFIA VISUAL: CONCEPTOS GENERALES, PRINCIPIOS Y CICLO PRESUPUESTAL (ACTIVIDAD 3.3.1)", ParagraphStyle('SubSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.2, leading=9, textColor=gold, alignment=TA_CENTER)))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=1.2, color=gold, spaceAfter=2, spaceBefore=0))

    # FICHA TECNICA RÁPIDA
    ficha = [
        [
            Paragraph("<b>Guia:</b> No. 32 Presupuesto", card_body),
            Paragraph("<b>Actividad:</b> 3.3.1 Infografia", card_body),
            Paragraph("<b>Aprendiz:</b> Gina Villamizar", ParagraphStyle('F1', parent=card_body, fontName='Helvetica-Bold', textColor=primary)),
            Paragraph("<b>Instructor:</b> George Olago", card_body)
        ]
    ]
    t_f = Table(ficha, colWidths=[135, 135, 142, 140])
    t_f.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_f)
    story.append(Spacer(1, 2))

    # =========================================================================
    # FILA 1: MODULO 1 (DIAGNOSTICO) & MODULO 2 (VENTAJAS Y DESVENTAJAS)
    # =========================================================================
    img_diag = RLImage(os.path.join(icons_dir, "icon_diagnostico.png"), width=24, height=24)
    img_vent = RLImage(os.path.join(icons_dir, "icon_ventajas.png"), width=24, height=24)

    text_m1 = (
        "<b>DIAGNOSTICO ESTRATEGICO Y DEMANDA:</b><br/>"
        "• <b>Factores Internos (Controlables):</b> Capacidad instalada, liquidez de caja, calificacion del personal, eficiencia de costos e insumos.<br/>"
        "• <b>Factores Externos (No Controlables):</b> Inflacion, tasa de interes Banco de la Republica, reformas DIAN, TRM y competencia.<br/>"
        "• <b>Datos Historicos & Elasticidad:</b> Analisis de 3-5 anos para detectar estacionalidad. Si la demanda es <i>elastica</i>, al subir el precio caen las ventas; si es <i>inelastica</i>, el cliente sigue comprando."
    )
    
    text_m2 = (
        "<b>VENTAJAS VS. LIMITACIONES DEL PRESUPUESTO:</b><br/>"
        "• <b>Ventajas:</b> Fija metas numericas, optimiza capital de trabajo, previene crisis de iliquidez, estandariza costos y mide variaciones de gestion.<br/>"
        "• <b>Limitaciones:</b> Se basa en estimaciones (riesgo e incertidumbre), requiere disciplina y cultura de registro contable; no sustituye a la administracion, es una herramienta de apoyo directivo.<br/>"
        "• <b>Principio Rector:</b> Debe ser <i>flexible</i> para absorber fluctuaciones economicas."
    )

    col1 = [
        [img_diag, Paragraph("<b>1. DIAGNOSTICO PREVIO Y DEMANDA</b>", card_header)],
        [Paragraph(text_m1, card_body), ""]
    ]
    t_col1 = Table(col1, colWidths=[28, 238])
    t_col1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('SPAN', (0,1), (1,1)),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))

    col2 = [
        [img_vent, Paragraph("<b>2. VENTAJAS Y LIMITACIONES</b>", card_header)],
        [Paragraph(text_m2, card_body), ""]
    ]
    t_col2 = Table(col2, colWidths=[28, 238])
    t_col2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), emerald),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('SPAN', (0,1), (1,1)),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))

    t_row1 = Table([[t_col1, t_col2]], colWidths=[273, 273])
    t_row1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
    story.append(t_row1)
    story.append(Spacer(1, 2))

    # =========================================================================
    # FILA 2: CICLO PRESUPUESTAL VISUAL (DIAGRAMA DE FLUJO EN 5 PASOS)
    # =========================================================================
    img_ciclo = RLImage(os.path.join(icons_dir, "icon_ciclo.png"), width=20, height=20)
    ciclo_hdr = Table([[img_ciclo, Paragraph("<b>3. EL CICLO PRESUPUESTAL (FLUJO METODOLOGICO EN 5 ETAPAS OBLIGATORIAS)</b>", card_header)]], colWidths=[24, 524])
    ciclo_hdr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1E3A8A")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(ciclo_hdr)

    # 5 Cajitas del Flujo Horizontal
    paso1 = "<b>ETAPA 1<br/>PREINICIACION</b><br/>Diagnostico, metas, politicas gerenciales y comite presupuestal."
    paso2 = "<b>ETAPA 2<br/>ELABORACION</b><br/>Calculo de cedulas: ventas, compras, MOD, CIF y flujo de caja."
    paso3 = "<b>ETAPA 3<br/>EJECUCION</b><br/>Puesta en marcha operativa y desembolsos diarios en cada area."
    paso4 = "<b>ETAPA 4<br/>CONTROL</b><br/>Monitoreo mes a mes: calculo de variaciones (Real vs Presupuesto)."
    paso5 = "<b>ETAPA 5<br/>EVALUACION</b><br/>Informe final, cierre de periodo y lecciones para el siguiente ciclo."

    ciclo_boxes = [
        [
            Paragraph(paso1, flow_box),
            Paragraph("─►", ParagraphStyle('A1', parent=flow_box, fontSize=9, textColor=gold)),
            Paragraph(paso2, flow_box),
            Paragraph("─►", ParagraphStyle('A2', parent=flow_box, fontSize=9, textColor=gold)),
            Paragraph(paso3, flow_box),
            Paragraph("─►", ParagraphStyle('A3', parent=flow_box, fontSize=9, textColor=gold)),
            Paragraph(paso4, flow_box),
            Paragraph("─►", ParagraphStyle('A4', parent=flow_box, fontSize=9, textColor=gold)),
            Paragraph(paso5, flow_box),
        ]
    ]
    t_flow = Table(ciclo_boxes, colWidths=[96, 16, 96, 16, 96, 16, 96, 16, 96])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor("#FEF3C7")),
        ('BACKGROUND', (4,0), (4,0), colors.HexColor("#ECFDF5")),
        ('BACKGROUND', (6,0), (6,0), colors.HexColor("#FEF2F2")),
        ('BACKGROUND', (8,0), (8,0), colors.HexColor("#F5F3FF")),
        ('BOX', (0,0), (0,0), 0.5, colors.HexColor("#93C5FD")),
        ('BOX', (2,0), (2,0), 0.5, colors.HexColor("#FCD34D")),
        ('BOX', (4,0), (4,0), 0.5, colors.HexColor("#6EE7B7")),
        ('BOX', (6,0), (6,0), 0.5, colors.HexColor("#FCA5A5")),
        ('BOX', (8,0), (8,0), 0.5, colors.HexColor("#C4B5FD")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_flow)
    story.append(Spacer(1, 2))

    # =========================================================================
    # FILA 3: CLASIFICACION DOCTRINAL (8 CRITERIOS)
    # =========================================================================
    img_clas = RLImage(os.path.join(icons_dir, "icon_clasificacion.png"), width=20, height=20)
    clas_hdr = Table([[img_clas, Paragraph("<b>4. CLASIFICACION UNIVERSAL DE LOS PRESUPUESTOS (SEGUN AUTORES Y NIIF)</b>", card_header)]], colWidths=[24, 524])
    clas_hdr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#B45309")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(clas_hdr)

    c1 = "<b>1. Flexibilidad:</b><br/>• <i>Rigidos/Fijos:</i> Sin cambios.<br/>• <i>Flexibles:</i> Se adaptan al volumen."
    c2 = "<b>2. Periodo:</b><br/>• <i>Corto Plazo:</i> <= 1 ano.<br/>• <i>Mediano/Largo:</i> 2 a 5 anos."
    c3 = "<b>3. Campo/Area:</b><br/>• <i>Operacion:</i> Ventas, Costos.<br/>• <i>Financiero:</i> Caja, Balance."
    c4 = "<b>4. Sector:</b><br/>• <i>Publico:</i> Fin social estatal.<br/>• <i>Privado:</i> Lucro y rentabilidad."
    c5 = "<b>5. Contenido:</b><br/>• <i>Principales:</i> Resumen.<br/>• <i>Auxiliares:</i> Detalle cuentas."
    c6 = "<b>6. Valuacion:</b><br/>• <i>Estimados:</i> Historicos.<br/>• <i>Estandar:</i> Tecnico cientifico."
    c7 = "<b>7. Responsabilidad:</b><br/>• Centros de Costos.<br/>• Centros de Utilidades."
    c8 = "<b>8. Finalidad:</b><br/>• Rutinarios / Expansion.<br/>• De Promocion / Fusion."

    clas_table_data = [
        [Paragraph(c1, card_body), Paragraph(c2, card_body), Paragraph(c3, card_body), Paragraph(c4, card_body)],
        [Paragraph(c5, card_body), Paragraph(c6, card_body), Paragraph(c7, card_body), Paragraph(c8, card_body)]
    ]
    t_clas = Table(clas_table_data, colWidths=[137, 137, 137, 137])
    t_clas.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFBEB")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#FCD34D")),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#FDE68A")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_clas)
    story.append(Spacer(1, 2))

    # =========================================================================
    # FILA 4: MODULO 5 (CONTROL Y VARIACIONES) & MODULO 6 (PROYECCION EEFF)
    # =========================================================================
    img_ctrl = RLImage(os.path.join(icons_dir, "icon_control.png"), width=24, height=24)
    img_est = RLImage(os.path.join(icons_dir, "icon_estados.png"), width=24, height=24)

    text_m5 = (
        "<b>CONTROL PRESUPUESTAL Y VARIACIONES:</b><br/>"
        "• <b>Formula:</b> <i>Variacion = Real Ejecutado - Presupuestado</i>.<br/>"
        "• <b>Favorable (F):</b> Mayor ingreso real o menor costo que la meta.<br/>"
        "• <b>Desfavorable (D):</b> Caida en ventas o sobrecosto en insumos.<br/>"
        "• <b>Acciones Correctivas:</b> Ajuste inmediato de ordenes de compra, reduccion de mermas, turnos de trabajo y austeridad en gastos administrativos."
    )

    text_m6 = (
        "<b>INTEGRACION EN ESTADOS FINANCIEROS (NIIF):</b><br/>"
        "• <b>1. Estado de Resultados (ERI):</b> Proyecta Ventas Netas - Costo de Ventas = Utilidad Bruta - Gastos Fijos - Impuestos = <i>Resultado Neto</i>.<br/>"
        "• <b>2. Presupuesto de Caja (Flujo de Efectivo):</b> Control de liquidez real: Cobranza a clientes menos salidas efectivas. Previene cesacion de pagos.<br/>"
        "• <b>3. Balance General (ESF):</b> Verifica equilibrio: <i>Activo = Pasivo + Patrimonio</i>."
    )

    col5 = [
        [img_ctrl, Paragraph("<b>5. CONTROL, VARIACIONES Y ACCION</b>", card_header)],
        [Paragraph(text_m5, card_body), ""]
    ]
    t_col5 = Table(col5, colWidths=[28, 238])
    t_col5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#991B1B")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FEF2F2")),
        ('SPAN', (0,1), (1,1)),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#FCA5A5")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))

    col6 = [
        [img_est, Paragraph("<b>6. CIERRE: ESTADOS FINANCIEROS Y CAJA</b>", card_header)],
        [Paragraph(text_m6, card_body), ""]
    ]
    t_col6 = Table(col6, colWidths=[28, 238])
    t_col6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('SPAN', (0,1), (1,1)),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))

    t_row4 = Table([[t_col5, t_col6]], colWidths=[273, 273])
    t_row4.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
    story.append(t_row4)
    story.append(Spacer(1, 4))

    # FIRMAS
    sign = [
        [
            Paragraph("___________________________________<br/><b>Gina Villamizar</b><br/>Aprendiz SENA CSET • Gestora Contable", ParagraphStyle('S1', parent=card_body, alignment=TA_CENTER)),
            Paragraph("___________________________________<br/><b>George Olago</b><br/>Instructor Titular de Proyecto • SENA CSET", ParagraphStyle('S2', parent=card_body, alignment=TA_CENTER))
        ]
    ]
    t_sign = Table(sign, colWidths=[274, 274])
    t_sign.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Infografia PDF generated successfully:", pdf_path)

if __name__ == '__main__':
    generate_infografia()

# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
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
        self.drawString(32, 762, "SENA CSET BUCARAMANGA | GUIA No. 32 PRESUPUESTO MAESTRO | APRENDIZ: GINA VILLAMIZAR")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(32, 757, 580, 757)
            
        # Footer
        page_text = f"Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(580, 20, page_text)
        self.drawString(32, 20, "TECNOLOGIA EN GESTION CONTABLE Y FINANCIERA • PROYECTO DE VIDA Y PRESUPUESTO A 5 ANOS")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(32, 28, 580, 28)
        self.restoreState()

def generate_pdf():
    pdf_path = "/Users/ginavillamizar/Downloads/CONTABILIDAD/GUIA_32_REFLEXION_INICIAL_GINA_VILLAMIZAR.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=32,
        rightMargin=32,
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

    sec_header = ParagraphStyle(
        'SecHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=primary,
        spaceBefore=2,
        spaceAfter=1
    )

    body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.2,
        textColor=slate_dark,
        alignment=TA_JUSTIFY
    )

    vision_box = ParagraphStyle(
        'VisionBox',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.2,
        leading=9.6,
        textColor=primary,
        alignment=TA_JUSTIFY
    )

    cell_hdr = ParagraphStyle(
        'CellHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.5,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    cell_hdr_left = ParagraphStyle(
        'CellHdrLeft',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.5,
        textColor=colors.white,
        alignment=TA_LEFT
    )

    cell_txt = ParagraphStyle(
        'CellTxt',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.6,
        leading=8,
        textColor=slate_dark
    )

    cell_txt_bold = ParagraphStyle(
        'CellTxtBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.6,
        leading=8,
        textColor=primary
    )

    cell_num = ParagraphStyle(
        'CellNum',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.6,
        leading=8,
        alignment=TA_RIGHT,
        textColor=slate_dark
    )

    cell_num_bold = ParagraphStyle(
        'CellNumBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.6,
        leading=8,
        alignment=TA_RIGHT,
        textColor=primary
    )

    story = []

    # Header Institucional
    story.append(Paragraph("SERVICIO NACIONAL DE APRENDIZAJE - SENA", title_style))
    story.append(Paragraph("CENTRO DE SERVICIOS EMPRESARIALES Y TURISTICOS (CSET) • REGIONAL SANTANDER", sub_title_style))
    story.append(Paragraph("TECNOLOGIA EN GESTION CONTABLE Y DE INFORMACION FINANCIERA (CODIGO 123101)", ParagraphStyle('SubSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.2, leading=9, textColor=colors.HexColor("#64748B"), alignment=TA_CENTER)))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=1.2, color=gold, spaceAfter=2, spaceBefore=0))

    # Ficha Tecnica
    info_data = [
        [
            Paragraph("<b>Guia:</b> No. 32 Presupuesto Maestro", cell_txt),
            Paragraph("<b>Fase del Proyecto:</b> Evaluacion (AP 7)", cell_txt),
            Paragraph("<b>Aprendiz:</b> Gina Villamizar", cell_txt_bold)
        ],
        [
            Paragraph("<b>Competencia:</b> 210303023 - Informes Financieros", cell_txt),
            Paragraph("<b>Actividad:</b> AA_32 Presupuesto Maestro", cell_txt),
            Paragraph("<b>Fecha:</b> Noviembre 2026", cell_txt)
        ]
    ]
    t_info = Table(info_data, colWidths=[180, 180, 188])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 2))

    # Titulo Seccion
    story.append(Paragraph("3.1. ACTIVIDAD DE REFLEXION INICIAL: PROYECTO DE VIDA Y PRESUPUESTO A 5 ANOS", sec_header))
    story.append(HRFlowable(width="100%", thickness=0.5, color=primary, spaceAfter=2, spaceBefore=0))

    # 1. Vision
    vision_text = (
        "<b>1. Vision Personal y Profesional (2026 - 2030):</b> \"En el ano 2030 sere Contadora Publica con tarjeta profesional "
        "egresada de universidad publica en jornada nocturna, Tecnologa en Gestion Contable del SENA y Cosmetologa y Esteticista Integral. "
        "Liderare mi propia cabina y centro de estetica integral gestionado con rigor contable, consolidandome paralelamente como conferencista "
        "y asesora financiera para el gremio de la estetica, formando a profesionales de la belleza en costeo cientifico de servicios, "
        "fijacion de precios rentables y administracion del dinero.\""
    )
    t_vis = Table([[Paragraph(vision_text, vision_box)]], colWidths=[548])
    t_vis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 0.6, gold),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_vis)
    story.append(Spacer(1, 2))

    # 2. Objetivos y Metas
    obj_meta_text = (
        "<b>2. Objetivos y Metas Estrategicas:</b><br/>"
        "<b>• General:</b> Integrar estetica y contabilidad para liderar una cabina rentable, graduarme como Contadora Publica y crear una linea de conferencias en costos.<br/>"
        "<b>• Metas Clave:</b> <b>a)</b> Graduarme como Esteticista Integral (Dic 2026). <b>b)</b> Abrir cabina en casa (Feb 2027) con camilla y aparatologia valorada en $5M (donacion/regalo). "
        "<b>c)</b> Iniciar practicas tecnólogo (27 Jul 2027) y grado SENA (Ene 2028). <b>d)</b> 4 semestres nocturnos Contaduria publica ($1,5M semestre) y Tarjeta Profesional (2030). "
        "<b>e)</b> Meta cabina 2027: 3 limpiezas faciales semanales ($100.000 c/u, insumos $15.000). <b>f)</b> Reinversion 100% de utilidad CrewStore ($500.000/mes) en ropa."
    )
    story.append(Paragraph(obj_meta_text, body))
    story.append(Spacer(1, 2))

    # 3. Tabla Presupuesto
    story.append(Paragraph("<b>3. Presupuesto Financiero Personal y Profesional Proyectado (2026 - 2030):</b>", sec_header))
    
    fin_data = [
        [
            Paragraph("<b>Concepto Presupuestal (COP)</b>", cell_hdr_left),
            Paragraph("<b>2026 (Real)</b>", cell_hdr),
            Paragraph("<b>2027 (Proy)</b>", cell_hdr),
            Paragraph("<b>2028 (Proy)</b>", cell_hdr),
            Paragraph("<b>2029 (Proy)</b>", cell_hdr),
            Paragraph("<b>2030 (Proy)</b>", cell_hdr)
        ],
        [Paragraph("<b>INGRESOS</b>", cell_txt_bold), Paragraph("", cell_txt), Paragraph("", cell_txt), Paragraph("", cell_txt), Paragraph("", cell_txt), Paragraph("", cell_txt)],
        [Paragraph("Contrato Aprendizaje (Sep-Dic / Practicas)", cell_txt), Paragraph("$ 5.200.000", cell_num), Paragraph("$ 15.600.000", cell_num), Paragraph("$ 1.300.000", cell_num), Paragraph("$ 0", cell_num), Paragraph("$ 0", cell_num)],
        [Paragraph("Utilidad Emprendimiento Ropa (CrewStore)", cell_txt), Paragraph("$ 2.000.000", cell_num), Paragraph("$ 6.000.000", cell_num), Paragraph("$ 6.000.000", cell_num), Paragraph("$ 6.000.000", cell_num), Paragraph("$ 6.000.000", cell_num)],
        [Paragraph("Cabina Estetica (Limpiezas $100.000)", cell_txt), Paragraph("$ 0", cell_num), Paragraph("$ 14.400.000", cell_num), Paragraph("$ 24.000.000", cell_num), Paragraph("$ 36.000.000", cell_num), Paragraph("$ 48.000.000", cell_num)],
        [Paragraph("Asesorias Contables Negocios Belleza", cell_txt), Paragraph("$ 0", cell_num), Paragraph("$ 0", cell_num), Paragraph("$ 2.400.000", cell_num), Paragraph("$ 7.200.000", cell_num), Paragraph("$ 18.000.000", cell_num)],
        [Paragraph("Conferencias Costos y Finanzas", cell_txt), Paragraph("$ 0", cell_num), Paragraph("$ 0", cell_num), Paragraph("$ 1.000.000", cell_num), Paragraph("$ 4.000.000", cell_num), Paragraph("$ 10.000.000", cell_num)],
        [Paragraph("<b>TOTAL INGRESOS (A)</b>", cell_txt_bold), Paragraph("<b>$ 7.200.000</b>", cell_num_bold), Paragraph("<b>$ 36.000.000</b>", cell_num_bold), Paragraph("<b>$ 34.700.000</b>", cell_num_bold), Paragraph("<b>$ 53.200.000</b>", cell_num_bold), Paragraph("<b>$ 82.000.000</b>", cell_num_bold)],
        
        [Paragraph("<b>EGRESOS</b>", cell_txt_bold), Paragraph("", cell_txt), Paragraph("", cell_txt), Paragraph("", cell_txt), Paragraph("", cell_txt), Paragraph("", cell_txt)],
        [Paragraph("Transporte, Alimentacion y Personales", cell_txt), Paragraph("$ 3.200.000", cell_num), Paragraph("$ 9.600.000", cell_num), Paragraph("$ 10.800.000", cell_num), Paragraph("$ 12.000.000", cell_num), Paragraph("$ 14.400.000", cell_num)],
        [Paragraph("Aporte Estudios Estetica (Sep-Dic 2026)", cell_txt), Paragraph("$ 2.000.000", cell_num), Paragraph("$ 0", cell_num), Paragraph("$ 0", cell_num), Paragraph("$ 0", cell_num), Paragraph("$ 0", cell_num)],
        [Paragraph("Reinversion Mercancia Ropa (CrewStore)", cell_txt), Paragraph("$ 2.000.000", cell_num), Paragraph("$ 6.000.000", cell_num), Paragraph("$ 6.000.000", cell_num), Paragraph("$ 6.000.000", cell_num), Paragraph("$ 6.000.000", cell_num)],
        [Paragraph("Insumos Cabina ($15.000 por servicio)", cell_txt), Paragraph("$ 0", cell_num), Paragraph("$ 2.160.000", cell_num), Paragraph("$ 3.600.000", cell_num), Paragraph("$ 5.400.000", cell_num), Paragraph("$ 7.200.000", cell_num)],
        [Paragraph("Servicios Hogar asignados a Cabina", cell_txt), Paragraph("$ 0", cell_num), Paragraph("$ 1.100.000", cell_num), Paragraph("$ 1.200.000", cell_num), Paragraph("$ 1.400.000", cell_num), Paragraph("$ 1.600.000", cell_num)],
        [Paragraph("Capacitacion Oratoria y Comunicacion", cell_txt), Paragraph("$ 0", cell_num), Paragraph("$ 1.000.000", cell_num), Paragraph("$ 0", cell_num), Paragraph("$ 500.000", cell_num), Paragraph("$ 500.000", cell_num)],
        [Paragraph("Matricula Univ. Publica / Tarjeta Prof.", cell_txt), Paragraph("$ 0", cell_num), Paragraph("$ 0", cell_num), Paragraph("$ 3.000.000", cell_num), Paragraph("$ 3.000.000", cell_num), Paragraph("$ 1.800.000", cell_num)],
        [Paragraph("Imprevistos y Marketing Digital", cell_txt), Paragraph("$ 0", cell_num), Paragraph("$ 800.000", cell_num), Paragraph("$ 1.200.000", cell_num), Paragraph("$ 1.500.000", cell_num), Paragraph("$ 2.000.000", cell_num)],
        [Paragraph("<b>TOTAL EGRESOS (B)</b>", cell_txt_bold), Paragraph("<b>$ 7.200.000</b>", cell_num_bold), Paragraph("<b>$ 20.660.000</b>", cell_num_bold), Paragraph("<b>$ 26.800.000</b>", cell_num_bold), Paragraph("<b>$ 30.800.000</b>", cell_num_bold), Paragraph("<b>$ 33.500.000</b>", cell_num_bold)],
        
        [Paragraph("<b>SUPERAVIT NETO ANUAL (A - B)</b>", cell_txt_bold), Paragraph("<b>$ 0</b>", cell_num_bold), Paragraph("<b>+$ 15.340.000</b>", cell_num_bold), Paragraph("<b>+$ 7.900.000</b>", cell_num_bold), Paragraph("<b>+$ 22.400.000</b>", cell_num_bold), Paragraph("<b>+$ 48.500.000</b>", cell_num_bold)],
        [Paragraph("<b>FONDO DE AHORRO ACUMULADO</b>", cell_txt_bold), Paragraph("<b>$ 0</b>", cell_num_bold), Paragraph("<b>$ 15.340.000</b>", cell_num_bold), Paragraph("<b>$ 23.240.000</b>", cell_num_bold), Paragraph("<b>$ 45.640.000</b>", cell_num_bold), Paragraph("<b>$ 94.140.000</b>", cell_num_bold)],
    ]
    t_fin = Table(fin_data, colWidths=[188, 72, 72, 72, 72, 72])
    t_fin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 2.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 2.5),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor("#EEF2FF")),
        ('BACKGROUND', (0,16), (-1,16), colors.HexColor("#FEE2E2")),
        ('BACKGROUND', (0,17), (-1,17), colors.HexColor("#DCFCE7")),
        ('BACKGROUND', (0,18), (-1,18), colors.HexColor("#FEF3C7")),
    ]))
    story.append(t_fin)
    story.append(Spacer(1, 2))

    # 4. Notas y Viabilidad
    notes_text = (
        "<b>4. Notas Contables y Conclusion de Viabilidad:</b><br/>"
        "• <b>Inversion Estetica 2026:</b> Se valoraron $15M financiados en su mayoria por apoyo familiar y completados con $2M del contrato ($500k/mes sep-dic).<br/>"
        "• <b>Activos Fijos:</b> Camilla y aparatologia ($5M) recibidas por donacion entran al balance como activo no corriente para depreciacion tecnica.<br/>"
        "• <b>Margen Unitario:</b> Con venta de $100.000 e insumos de $15.000, el margen es del <b>85% ($85.000)</b>, cubriendo servicios y generando utilidad limpia.<br/>"
        "• <b>Viabilidad:</b> Plenamente viable. 2026 cierra en equilibrio exacto ($0 ahorro) y desde 2027 la cabina financia la universidad y acumula <b>$94.140.000 a 2030</b>."
    )
    story.append(Paragraph(notes_text, body))
    story.append(Spacer(1, 4))

    # Firmas
    sign_data = [
        [
            Paragraph("___________________________________<br/><b>Gina Villamizar</b><br/>Aprendiz SENA CSET • Gestora Contable", ParagraphStyle('S1', parent=cell_txt, alignment=TA_CENTER)),
            Paragraph("___________________________________<br/><b>George Olago</b><br/>Instructor Titular de Proyecto • SENA CSET", ParagraphStyle('S2', parent=cell_txt, alignment=TA_CENTER))
        ]
    ]
    t_sign = Table(sign_data, colWidths=[274, 274])
    t_sign.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF generated successfully:", pdf_path)

if __name__ == '__main__':
    generate_pdf()

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
        self.drawString(28, 764, "SENA CSET BUCARAMANGA | GUIA No. 32 | CEDULAS DE COSTOS MP, MO Y CIF (PAG. 8-9) | GINA VILLAMIZAR")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(28, 759, 584, 759)
            
        # Footer
        page_text = f"Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(584, 16, page_text)
        self.drawString(28, 16, "TECNOLOGIA EN GESTION CONTABLE Y FINANCIERA • PRESUPUESTOS OPERATIVOS DE COSTOS DE PRODUCCION")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(28, 23, 584, 23)
        self.restoreState()

def generate_costos_pdf():
    pdf_path = "/Users/ginavillamizar/Downloads/CONTABILIDAD/GUIA_32_CEDULAS_COSTOS_MP_MO_CIF_GINA_VILLAMIZAR.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=28,
        rightMargin=28,
        topMargin=28,
        bottomMargin=28
    )

    styles = getSampleStyleSheet()
    
    primary = colors.HexColor("#0B192C")
    gold = colors.HexColor("#D4AF37")
    emerald = colors.HexColor("#047857")
    slate_dark = colors.HexColor("#1E293B")
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=primary, alignment=TA_CENTER)
    sub_title_style = ParagraphStyle('DocSubTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.6, leading=9.5, textColor=emerald, alignment=TA_CENTER)

    sec_hdr = ParagraphStyle('SecHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7, leading=8.5, textColor=primary, spaceBefore=2, spaceAfter=1)
    cell_hdr = ParagraphStyle('CellHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.2, leading=7.5, textColor=colors.white, alignment=TA_CENTER)
    cell_txt = ParagraphStyle('CellTxt', parent=styles['Normal'], fontName='Helvetica', fontSize=5.5, leading=7, textColor=slate_dark)
    cell_txt_bold = ParagraphStyle('CellTxtBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=5.5, leading=7, textColor=primary)
    cell_num = ParagraphStyle('CellNum', parent=styles['Normal'], fontName='Helvetica', fontSize=5.5, leading=7, alignment=TA_RIGHT, textColor=slate_dark)
    cell_num_bold = ParagraphStyle('CellNumBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=5.5, leading=7, alignment=TA_RIGHT, textColor=primary)

    body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=5.8, leading=7.5, textColor=slate_dark, alignment=TA_JUSTIFY)

    story = []

    # ENCABEZADO INSTITUCIONAL
    story.append(Paragraph("SERVICIO NACIONAL DE APRENDIZAJE - SENA • REGIONAL SANTANDER", title_style))
    story.append(Paragraph("CENTRO DE SERVICIOS EMPRESARIALES Y TURISTICOS (CSET) • GESTION CONTABLE (123101)", sub_title_style))
    story.append(Paragraph("ACTIVIDADES 3.3.5, 3.3.6 Y 3.3.7: CEDULAS DE MATERIA PRIMA, MANO DE OBRA Y COSTOS INDIRECTOS (CIF)", ParagraphStyle('SubSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=gold, alignment=TA_CENTER)))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=2, spaceBefore=0))

    # FICHA TECNICA COMPACTA
    ficha = [
        [
            Paragraph("<b>Guia:</b> No. 32 Presupuesto", cell_txt),
            Paragraph("<b>Actividades:</b> 3.3.5, 3.3.6, 3.3.7", cell_txt),
            Paragraph("<b>Aprendiz:</b> Gina Villamizar", cell_txt_bold),
            Paragraph("<b>Instructor:</b> George Olago", cell_txt)
        ]
    ]
    t_f = Table(ficha, colWidths=[139, 139, 139, 139])
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
    # 3.3.5 CEDULA MATERIA PRIMA DIRECTA (TELA BLUE JEAN)
    # =========================================================================
    story.append(Paragraph("<b>1. PRESUPUESTO DE MATERIA PRIMA 1 (TELA BLUE JEAN) - ACTIVIDAD 3.3.5:</b>", sec_hdr))
    
    mp_data = [
        [
            Paragraph("<b>FORMATO CEDULA MATERIA PRIMA 1 (Tela Blue Jean)</b>", cell_hdr),
            Paragraph("<b>Ano 2020</b>", cell_hdr),
            Paragraph("<b>Ano 2021</b>", cell_hdr),
            Paragraph("<b>Ano 2022</b>", cell_hdr),
            Paragraph("<b>Ano 2023</b>", cell_hdr),
            Paragraph("<b>Ano 2024</b>", cell_hdr)
        ],
        [
            Paragraph("<b>Unidades a producir (Cedula Produccion)</b>", cell_txt_bold),
            Paragraph("51.800", cell_num),
            Paragraph("63.960*", cell_num),
            Paragraph("<b>72.432</b>", cell_num_bold),
            Paragraph("<b>86.918</b>", cell_num_bold),
            Paragraph("<b>104.302</b>", cell_num_bold)
        ],
        [
            Paragraph("<b>Cantidad Materia prima Tela Blue Jean (Metros / unidad)</b>", cell_txt),
            Paragraph("1,50 m", cell_num),
            Paragraph("1,50 m", cell_num),
            Paragraph("1,50 m", cell_num),
            Paragraph("1,50 m", cell_num),
            Paragraph("1,50 m", cell_num)
        ],
        [
            Paragraph("<b>Total cantidad materia prima requerida (Metros)</b>", cell_txt_bold),
            Paragraph("77.700 m", cell_num),
            Paragraph("95.940 m", cell_num),
            Paragraph("<b>108.648 m</b>", cell_num_bold),
            Paragraph("<b>130.377 m</b>", cell_num_bold),
            Paragraph("<b>156.453 m</b>", cell_num_bold)
        ],
        [
            Paragraph("<b>Valor Costo por unidad medida ($ por metro)</b>", cell_txt),
            Paragraph("$ 7.500", cell_num),
            Paragraph("$ 7.500", cell_num),
            Paragraph("<b>$ 7.950</b> (+6%)", cell_num_bold),
            Paragraph("<b>$ 8.427</b> (+6%)", cell_num_bold),
            Paragraph("<b>$ 8.933</b> (+6%)", cell_num_bold)
        ],
        [
            Paragraph("<b>TOTAL COSTO MATERIA PRIMA 1 (TELA)</b>", cell_txt_bold),
            Paragraph("<b>$ 582.750.000</b>", cell_num_bold),
            Paragraph("<b>$ 719.550.000</b>", cell_num_bold),
            Paragraph("<b>$ 863.751.600</b>", cell_num_bold),
            Paragraph("<b>$ 1.098.687.000</b>", cell_num_bold),
            Paragraph("<b>$ 1.397.600.000</b>", cell_num_bold)
        ]
    ]
    t_mp = Table(mp_data, colWidths=[186, 74, 74, 74, 74, 74])
    t_mp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.35, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#FEF3C7")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_mp)
    story.append(Spacer(1, 2))

    # =========================================================================
    # 3.3.6 CEDULA MANO DE OBRA DIRECTA (OPERARIO 1)
    # =========================================================================
    story.append(Paragraph("<b>2. PRESUPUESTO DE MANO DE OBRA (OPERARIO 1) - ACTIVIDAD 3.3.6:</b>", sec_hdr))
    
    mo_data = [
        [
            Paragraph("<b>FORMATO CEDULA DE MANO DE OBRA Operario 1</b>", cell_hdr),
            Paragraph("<b>Ano 2020</b>", cell_hdr),
            Paragraph("<b>Ano 2021</b>", cell_hdr),
            Paragraph("<b>Ano 2022</b>", cell_hdr),
            Paragraph("<b>Ano 2023</b>", cell_hdr),
            Paragraph("<b>Ano 2024</b>", cell_hdr)
        ],
        [
            Paragraph("<b>Unidades a producir (Cedula Produccion)</b>", cell_txt_bold),
            Paragraph("51.800", cell_num),
            Paragraph("63.960*", cell_num),
            Paragraph("<b>72.432</b>", cell_num_bold),
            Paragraph("<b>86.918</b>", cell_num_bold),
            Paragraph("<b>104.302</b>", cell_num_bold)
        ],
        [
            Paragraph("<b>Cantidad minutos mano de obra por unidad</b>", cell_txt),
            Paragraph("2,00 Min", cell_num),
            Paragraph("1,50 Min", cell_num),
            Paragraph("1,50 Min", cell_num),
            Paragraph("1,50 Min", cell_num),
            Paragraph("1,50 Min", cell_num)
        ],
        [
            Paragraph("<b>TOTAL MINUTOS MANO OBRA REQUERIDOS</b>", cell_txt_bold),
            Paragraph("103.600 Min", cell_num),
            Paragraph("95.940 Min", cell_num),
            Paragraph("<b>108.648 Min</b>", cell_num_bold),
            Paragraph("<b>130.377 Min</b>", cell_num_bold),
            Paragraph("<b>156.453 Min</b>", cell_num_bold)
        ],
        [
            Paragraph("<b>Valor minuto de mano de obra ($)</b>", cell_txt),
            Paragraph("$ 111,15", cell_num),
            Paragraph("$ 111,15", cell_num),
            Paragraph("<b>$ 117,82</b> (+6%)", cell_num_bold),
            Paragraph("<b>$ 124,89</b> (+6%)", cell_num_bold),
            Paragraph("<b>$ 132,38</b> (+6%)", cell_num_bold)
        ],
        [
            Paragraph("<b>COSTO TOTAL MANO DE OBRA OPERARIO 1</b>", cell_txt_bold),
            Paragraph("<b>$ 11.514.701</b>", cell_num_bold),
            Paragraph("<b>$ 10.663.324</b>", cell_num_bold),
            Paragraph("<b>$ 12.800.907</b>", cell_num_bold),
            Paragraph("<b>$ 16.282.783</b>", cell_num_bold),
            Paragraph("<b>$ 20.711.248</b>", cell_num_bold)
        ]
    ]
    t_mo = Table(mo_data, colWidths=[186, 74, 74, 74, 74, 74])
    t_mo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), emerald),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.35, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#FEF3C7")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_mo)
    story.append(Spacer(1, 2))

    # =========================================================================
    # CONCEPTOS PREVIOS CIF Y METODOS DE SEPARACION (PUNTO ALTO / PUNTO BAJO)
    # =========================================================================
    cif_teoria = (
        "<b>3. CONCEPTOS DE COSTOS INDIRECTOS DE FABRICACION (CIF) Y SEPARACION DE COSTOS MIXTOS (ACTIVIDAD 3.3.7):</b><br/>"
        "• <b>a. Tasa Predeterminada de CIF:</b> Cociente entre los CIF presupuestados del periodo y la base de actividad proyectada: "
        "<i>Tasa = CIF Presupuestados / Nivel de Actividad Estandar</i> (Horas Maquina, Horas MOD o Unidades).<br/>"
        "• <b>b. Clasificacion de CIF:</b> <b>Fijos</b> (independientes del volumen: arriendo planta, seguros), <b>Variables</b> (crecen con la produccion: hilos, energia de corte) y <b>Mixtos</b> (parte fija y variable: servicios publicos y mantenimiento).<br/>"
        "• <b>c. Metodo Punto Alto y Punto Bajo:</b> Separa la porcion fija y variable de un costo mixto tomando el nivel mas alto y mas bajo de actividad:<br/>"
        "&nbsp;&nbsp;<i>Costo Variable Unitario (b) = (Costo Punto Alto - Costo Punto Bajo) / (Actividad Punto Alto - Actividad Punto Bajo)</i><br/>"
        "&nbsp;&nbsp;<i>Costo Fijo Total (a) = Costo Total Punto Alto - [b &times; Actividad Punto Alto]</i>.<br/>"
        "• <b>d. Metodo de Dispersion / Regresion:</b> Ajusta estadisticamente una nube de puntos mediante minimos cuadrados para hallar el costo fijo y variable con mayor precision matematica."
    )
    story.append(Paragraph(cif_teoria, body))
    story.append(Spacer(1, 2))

    # =========================================================================
    # 3.3.7 CEDULA COSTOS INDIRECTOS DE FABRICACION FIJOS
    # =========================================================================
    story.append(Paragraph("<b>4. CEDULA DE COSTOS INDIRECTOS DE FABRICACION FIJOS (PAGINA 9 DE LA GUIA):</b>", sec_hdr))
    
    cif_fijos_data = [
        [
            Paragraph("<b>Item</b>", cell_hdr),
            Paragraph("<b>Descripcion del Costo Fijo</b>", cell_hdr),
            Paragraph("<b>Valor Mes ($)</b>", cell_hdr),
            Paragraph("<b>Base de Asignacion CIF</b>", cell_hdr),
            Paragraph("<b>Tasa CIF Unitaria</b>", cell_hdr),
            Paragraph("<b>Ano 2020</b>", cell_hdr),
            Paragraph("<b>Ano 2021</b>", cell_hdr),
            Paragraph("<b>Ano 2022</b>", cell_hdr),
            Paragraph("<b>Ano 2023</b>", cell_hdr),
            Paragraph("<b>Ano 2024</b>", cell_hdr)
        ],
        [
            Paragraph("1", cell_txt),
            Paragraph("Servicios publicos Luz y Fuerza", cell_txt),
            Paragraph("$ 1.057.600", cell_num),
            Paragraph("Horas Maquina", cell_txt),
            Paragraph("$ 245,00", cell_num),
            Paragraph("$ 12.691.200", cell_num),
            Paragraph("$ 12.691.200", cell_num),
            Paragraph("$ 13.452.672", cell_num),
            Paragraph("$ 14.259.832", cell_num),
            Paragraph("$ 15.115.422", cell_num)
        ],
        [
            Paragraph("2", cell_txt),
            Paragraph("Arriendo de Fabrica / Taller", cell_txt),
            Paragraph("$ 6.610.000", cell_num),
            Paragraph("Unidades a producir", cell_txt),
            Paragraph("$ 1.531,16", cell_num),
            Paragraph("$ 79.320.000", cell_num),
            Paragraph("$ 79.320.000", cell_num),
            Paragraph("$ 84.079.200", cell_num),
            Paragraph("$ 89.123.952", cell_num),
            Paragraph("$ 94.471.389", cell_num)
        ],
        [
            Paragraph("3", cell_txt),
            Paragraph("Mantenimiento Preventivo Maquinaria", cell_txt),
            Paragraph("$ 661.000", cell_num),
            Paragraph("Horas Maquina", cell_txt),
            Paragraph("$ 153,12", cell_num),
            Paragraph("$ 7.932.000", cell_num),
            Paragraph("$ 7.932.000", cell_num),
            Paragraph("$ 8.407.920", cell_num),
            Paragraph("$ 8.912.395", cell_num),
            Paragraph("$ 9.447.139", cell_num)
        ],
        [
            Paragraph("4", cell_txt),
            Paragraph("Servicios generales y Aseo Fabril", cell_txt),
            Paragraph("$ 1.057.600", cell_num),
            Paragraph("Unidades a producir", cell_txt),
            Paragraph("$ 245,00", cell_num),
            Paragraph("$ 12.691.200", cell_num),
            Paragraph("$ 12.691.200", cell_num),
            Paragraph("$ 13.452.672", cell_num),
            Paragraph("$ 14.259.832", cell_num),
            Paragraph("$ 15.115.422", cell_num)
        ],
        [
            Paragraph("<b>TOTAL</b>", cell_txt_bold),
            Paragraph("<b>COSTOS INDIRECTOS FIJOS</b>", cell_txt_bold),
            Paragraph("<b>$ 9.386.200</b>", cell_num_bold),
            Paragraph("<b>Tasa Global Unitaria:</b>", cell_txt_bold),
            Paragraph("<b>$ 2.174,28</b>", cell_num_bold),
            Paragraph("<b>$ 112.634.400</b>", cell_num_bold),
            Paragraph("<b>$ 112.634.400</b>", cell_num_bold),
            Paragraph("<b>$ 119.392.464</b>", cell_num_bold),
            Paragraph("<b>$ 126.556.011</b>", cell_num_bold),
            Paragraph("<b>$ 134.149.372</b>", cell_num_bold)
        ]
    ]

    t_cif = Table(cif_fijos_data, colWidths=[18, 126, 52, 64, 48, 50, 50, 50, 50, 48])
    t_cif.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.35, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#FEF3C7")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_cif)
    story.append(Spacer(1, 3))

    # FIRMAS
    sign = [
        [
            Paragraph("___________________________________<br/><b>Gina Villamizar</b><br/>Aprendiz SENA CSET • Gestora Contable", ParagraphStyle('S1', parent=cell_txt, alignment=TA_CENTER)),
            Paragraph("___________________________________<br/><b>George Olago</b><br/>Instructor Titular de Proyecto • SENA CSET", ParagraphStyle('S2', parent=cell_txt, alignment=TA_CENTER))
        ]
    ]
    t_sign = Table(sign, colWidths=[278, 278])
    t_sign.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Costos MP MO CIF PDF generated successfully:", pdf_path)

if __name__ == '__main__':
    generate_costos_pdf()

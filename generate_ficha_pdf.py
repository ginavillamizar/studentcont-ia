# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
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
        self.drawString(26, 764, "SENA CSET BUCARAMANGA | GUIA No. 32 | FICHA TECNICA COSTOS UNITARIOS ESTANDAR | GINA VILLAMIZAR")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(26, 759, 586, 759)
            
        # Footer
        page_text = f"Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(586, 16, page_text)
        self.drawString(26, 16, "TECNOLOGIA EN GESTION CONTABLE Y FINANCIERA • DETERMINACION ESTANDAR MPD + MOD + CIF")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(26, 23, 586, 23)
        self.restoreState()

def generate_ficha_pdf():
    pdf_path = "/Users/ginavillamizar/Downloads/CONTABILIDAD/GUIA_32_FICHA_COSTOS_UNITARIOS_GINA_VILLAMIZAR.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=26,
        rightMargin=26,
        topMargin=26,
        bottomMargin=26
    )

    styles = getSampleStyleSheet()
    
    primary = colors.HexColor("#0B192C")
    gold = colors.HexColor("#D4AF37")
    emerald = colors.HexColor("#047857")
    slate_dark = colors.HexColor("#1E293B")
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=primary, alignment=TA_CENTER)
    sub_title_style = ParagraphStyle('DocSubTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.6, leading=9.5, textColor=emerald, alignment=TA_CENTER)

    sec_hdr = ParagraphStyle('SecHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=colors.white)
    cell_hdr = ParagraphStyle('CellHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.2, leading=7.8, textColor=primary, alignment=TA_CENTER)
    cell_txt = ParagraphStyle('CellTxt', parent=styles['Normal'], fontName='Helvetica', fontSize=5.8, leading=7.2, textColor=slate_dark)
    cell_txt_bold = ParagraphStyle('CellTxtBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=5.8, leading=7.2, textColor=primary)
    cell_num = ParagraphStyle('CellNum', parent=styles['Normal'], fontName='Helvetica', fontSize=5.8, leading=7.2, alignment=TA_RIGHT, textColor=slate_dark)
    cell_num_bold = ParagraphStyle('CellNumBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=5.8, leading=7.2, alignment=TA_RIGHT, textColor=primary)

    story = []

    # ENCABEZADO INSTITUCIONAL
    story.append(Paragraph("SERVICIO NACIONAL DE APRENDIZAJE - SENA • REGIONAL SANTANDER", title_style))
    story.append(Paragraph("CENTRO DE SERVICIOS EMPRESARIALES Y TURISTICOS (CSET) • GESTION CONTABLE (123101)", sub_title_style))
    story.append(Paragraph("ACTIVIDAD 3.3.3: FICHA DE COSTOS UNITARIOS ESTANDAR (CONFECCION BLUE JEAN CLASICO)", ParagraphStyle('SubSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=gold, alignment=TA_CENTER)))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=2, spaceBefore=0))

    # ENCABEZADO DEL PRODUCTO (Tal cual formato)
    prod_data = [
        [
            Paragraph("<b>NOMBRE PRODUCTO:</b> Pantalon Blue Jean Clasico", cell_txt_bold),
            Paragraph("<b>Referencia:</b> BJ-FEM-01", cell_txt_bold),
            Paragraph("<b>Unidad de Costeo:</b> 1 Pantalon Terminado", cell_txt_bold)
        ]
    ]
    t_prod = Table(prod_data, colWidths=[200, 160, 200])
    t_prod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_prod)
    story.append(Spacer(1, 2))

    # TABLA GENERAL DE COSTOS
    # 560 pt disponibles de ancho
    # Columnas: 6 columnas proporcionales
    cw = [120, 75, 95, 95, 85, 90]

    grid_data = []

    # =========================================================================
    # SECCION 1: MATERIA PRIMA DIRECTA (MPD)
    # =========================================================================
    grid_data.append([Paragraph("<b>ELEMENTO COSTO: MATERIA PRIMA DIRECTA (MPD)</b>", sec_hdr), "", "", "", "", ""])
    grid_data.append([
        Paragraph("<b>MATERIAL</b>", cell_hdr),
        Paragraph("<b>TIPO COSTO</b>", cell_hdr),
        Paragraph("<b>VALOR UNIDAD MEDIDA<br/>(m, carrete, und, lb)</b>", cell_hdr),
        Paragraph("<b>CANTIDAD REQUERIDA<br/>POR UNIDAD PRODUCIDA</b>", cell_hdr),
        Paragraph("<b>VALOR COSTO POR<br/>UNIDAD DE MEDIDA</b>", cell_hdr),
        Paragraph("<b>TOTAL COSTO POR<br/>UNIDAD PRODUCIDA</b>", cell_hdr)
    ])
    grid_data.append([Paragraph("Tela Denim Blue Jean Indigo", cell_txt), Paragraph("Variable Directo", cell_txt), Paragraph("Metro (m)", cell_txt), Paragraph("1,50 Metros", cell_num), Paragraph("$ 7.500", cell_num), Paragraph("$ 11.250", cell_num_bold)])
    grid_data.append([Paragraph("Cremallera Metalica Reforzada", cell_txt), Paragraph("Variable Directo", cell_txt), Paragraph("Unidad (und)", cell_txt), Paragraph("1,00 Unidad", cell_num), Paragraph("$ 850", cell_num), Paragraph("$ 850", cell_num_bold)])
    grid_data.append([Paragraph("Boton Metalico Contramarcado", cell_txt), Paragraph("Variable Directo", cell_txt), Paragraph("Unidad (und)", cell_txt), Paragraph("1,00 Unidad", cell_num), Paragraph("$ 350", cell_num), Paragraph("$ 350", cell_num_bold)])
    grid_data.append([Paragraph("Remaches Metalicos Bolsillos", cell_txt), Paragraph("Variable Directo", cell_txt), Paragraph("Juego x 6 und", cell_txt), Paragraph("1,00 Juego (6)", cell_num), Paragraph("$ 450", cell_num), Paragraph("$ 450", cell_num_bold)])
    grid_data.append([Paragraph("Hilo de Confeccion Pesada (Poliester)", cell_txt), Paragraph("Variable Directo", cell_txt), Paragraph("Carrete x 1000m", cell_txt), Paragraph("0,08 Carrete (80m)", cell_num), Paragraph("$ 4.000", cell_num), Paragraph("$ 320", cell_num_bold)])
    grid_data.append([Paragraph("<b>TOTAL COSTO UNITARIO MATERIA PRIMA (MP)</b>", cell_txt_bold), "", "", "", "", Paragraph("<b>$ 13.220</b>", cell_num_bold)])

    # =========================================================================
    # SECCION 2: MANO DE OBRA DIRECTA (MOD)
    # =========================================================================
    grid_data.append([Paragraph("<b>ELEMENTO COSTO: MANO DE OBRA DIRECTA (MOD)</b>", sec_hdr), "", "", "", "", ""])
    grid_data.append([
        Paragraph("<b>CARGO POR PROCESO<br/>PRODUCCION</b>", cell_hdr),
        Paragraph("<b>AREA / DPTO<br/>(CENTRO COSTO)</b>", cell_hdr),
        Paragraph("<b>VALOR UNITARIO HORA<br/>MANO DE OBRA (176h)</b>", cell_hdr),
        Paragraph("<b>VALOR UNITARIO OSEA<br/>POR MINUTO MO (192)</b>", cell_hdr),
        Paragraph("<b>TIEMPO REQUERIDO<br/>POR UNIDAD (MINUTOS)</b>", cell_hdr),
        Paragraph("<b>TOTAL COSTO DE<br/>MANO DE OBRA</b>", cell_hdr)
    ])
    grid_data.append([Paragraph("Operario Corte y Trazo", cell_txt), Paragraph("Planta - Area Corte", cell_txt), Paragraph("$ 11.737 / Hora", cell_num), Paragraph("$ 195,62 / Min", cell_num), Paragraph("10,00 Minutos", cell_num), Paragraph("$ 1.956", cell_num_bold)])
    grid_data.append([Paragraph("Operario Ensamble / Costura (Guia)", cell_txt), Paragraph("Planta - Confeccion", cell_txt), Paragraph("$ 6.669 / Hora", cell_num), Paragraph("$ 111,15 / Min", cell_num), Paragraph("25,00 Minutos", cell_num), Paragraph("$ 2.779", cell_num_bold)])
    grid_data.append([Paragraph("Operario Ojal, Boton y Remache", cell_txt), Paragraph("Planta - Terminacion", cell_txt), Paragraph("$ 6.669 / Hora", cell_num), Paragraph("$ 111,15 / Min", cell_num), Paragraph("5,00 Minutos", cell_num), Paragraph("$ 556", cell_num_bold)])
    grid_data.append([Paragraph("Operario Planchado y Empaque", cell_txt), Paragraph("Planta - Acabados", cell_txt), Paragraph("$ 6.669 / Hora", cell_num), Paragraph("$ 111,15 / Min", cell_num), Paragraph("5,00 Minutos", cell_num), Paragraph("$ 556", cell_num_bold)])
    grid_data.append([Paragraph("<b>TOTALES / TOTAL COSTO UNITARIO MANO DE OBRA (MO)</b>", cell_txt_bold), "", "", "", Paragraph("<b>45,00 Minutos</b>", cell_num_bold), Paragraph("<b>$ 5.847</b>", cell_num_bold)])

    # =========================================================================
    # SECCION 3: COSTOS INDIRECTOS DE FABRICACION (CIF) VARIABLES
    # =========================================================================
    grid_data.append([Paragraph("<b>ELEMENTO COSTO: COSTOS INDIRECTOS DE FABRICACION (CIF)</b>", sec_hdr), "", "", "", "", ""])
    grid_data.append([
        Paragraph("<b>COSTOS CIF VARIABLES</b>", cell_hdr),
        Paragraph("<b>AREA / DPTO<br/>(CENTRO COSTO)</b>", cell_hdr),
        Paragraph("<b>UNIDAD MEDIDA<br/>(Kg, gr, lt, ml, m, horas)</b>", cell_hdr),
        Paragraph("<b>VALOR POR UNIDAD<br/>DE MEDIDA</b>", cell_hdr),
        Paragraph("<b>CANTIDAD REQUERIDA<br/>POR UNIDAD PRODUCIDA</b>", cell_hdr),
        Paragraph("<b>TOTAL COSTO POR<br/>UNIDAD PRODUCIDA</b>", cell_hdr)
    ])
    grid_data.append([Paragraph("Proceso Lavanderia / Desgaste Indigo", cell_txt), Paragraph("Planta Externa", cell_txt), Paragraph("Servicio por Prenda", cell_txt), Paragraph("$ 2.800", cell_num), Paragraph("1,00 Prenda", cell_num), Paragraph("$ 2.800", cell_num_bold)])
    grid_data.append([Paragraph("Etiquetas, Marquilla y Codigo Barras", cell_txt), Paragraph("Empaque y Acabados", cell_txt), Paragraph("Juego Etiquetas", cell_txt), Paragraph("$ 450", cell_num), Paragraph("1,00 Juego", cell_num), Paragraph("$ 450", cell_num_bold)])
    grid_data.append([Paragraph("Bolsa Plastica Protectora Despacho", cell_txt), Paragraph("Empaque y Acabados", cell_txt), Paragraph("Unidad (und)", cell_txt), Paragraph("$ 180", cell_num), Paragraph("1,00 Bolsa", cell_num), Paragraph("$ 180", cell_num_bold)])
    grid_data.append([Paragraph("<b>TOTAL COSTO UNITARIO CIF (VARIABLE)</b>", cell_txt_bold), "", "", "", "", Paragraph("<b>$ 3.430</b>", cell_num_bold)])

    # =========================================================================
    # SECCION 4: CIF FIJOS Y TASA PREDETERMINADA
    # =========================================================================
    grid_data.append([
        Paragraph("<b>COSTOS CIF FIJOS</b>", cell_hdr),
        Paragraph("<b>AREA / DPTO<br/>(CENTRO COSTO)</b>", cell_hdr),
        Paragraph("<b>UNIDAD MEDIDA</b>", cell_hdr),
        Paragraph("<b>VALOR TOTAL<br/>CONSUMO MES</b>", cell_hdr),
        Paragraph("<b>CAPACIDAD INSTALADA<br/>EN UNIDADES POR MES</b>", cell_hdr),
        Paragraph("<b>TASA PREDETERMINADA<br/>UNITARIA CIF FIJOS</b>", cell_hdr)
    ])
    grid_data.append([Paragraph("Servicios Publicos Luz y Fuerza Motriz", cell_txt), Paragraph("Planta de Confeccion", cell_txt), Paragraph("Horas Maquina / Mes", cell_txt), Paragraph("$ 1.057.600", cell_num), Paragraph("4.317 Unidades / Mes", cell_num), Paragraph("$ 245,00", cell_num_bold)])
    grid_data.append([Paragraph("Arriendo de Fabrica / Bodega Taller", cell_txt), Paragraph("Instalaciones Fabriles", cell_txt), Paragraph("Canon Mensual", cell_txt), Paragraph("$ 6.610.000", cell_num), Paragraph("4.317 Unidades / Mes", cell_num), Paragraph("$ 1.531,16", cell_num_bold)])
    grid_data.append([Paragraph("Mantenimiento Preventivo Maquinaria", cell_txt), Paragraph("Dpto Mantenimiento", cell_txt), Paragraph("Horas Maquina / Mes", cell_txt), Paragraph("$ 661.000", cell_num), Paragraph("4.317 Unidades / Mes", cell_num), Paragraph("$ 153,12", cell_num_bold)])
    grid_data.append([Paragraph("Servicios Generales y Aseo Fabril", cell_txt), Paragraph("Planta de Produccion", cell_txt), Paragraph("Servicios Mensuales", cell_txt), Paragraph("$ 1.057.600", cell_num), Paragraph("4.317 Unidades / Mes", cell_num), Paragraph("$ 245,00", cell_num_bold)])
    grid_data.append([
        Paragraph("<b>TOTAL COSTOS INDIRECTOS FIJOS DEL MES</b>", cell_txt_bold),
        "",
        "",
        Paragraph("<b>$ 9.386.200</b>", cell_num_bold),
        Paragraph("<b>Costo Unitario CIF Fijos</b>", cell_txt_bold),
        Paragraph("<b>$ 2.174,28</b>", cell_num_bold)
    ])

    # =========================================================================
    # SECCION 5: LIQUIDACION TOTAL DE COSTOS Y PRECIO DE VENTA
    # =========================================================================
    grid_data.append([Paragraph("<b>TOTAL COSTO UNITARIO VARIABLE (MPD $13.220 + MOD $5.847 + CIF Var $3.430)</b>", cell_txt_bold), "", "", "", "", Paragraph("<b>$ 22.497</b>", cell_num_bold)])
    grid_data.append([Paragraph("<b>TOTAL COSTO UNITARIO FIJO (Tasa Predeterminada CIF Fijo)</b>", cell_txt_bold), "", "", "", "", Paragraph("<b>$ 2.174</b>", cell_num_bold)])
    grid_data.append([Paragraph("<b>TOTAL COSTO UNITARIO PRIMO (MPD $13.220 + MOD $5.847)</b>", cell_txt_bold), "", "", "", "", Paragraph("<b>$ 19.067</b>", cell_num_bold)])
    grid_data.append([Paragraph("<b>TOTAL COSTO UNITARIO CONVERSION (MOD $5.847 + CIF Total $5.604)</b>", cell_txt_bold), "", "", "", "", Paragraph("<b>$ 11.451</b>", cell_num_bold)])
    grid_data.append([Paragraph("<b>TOTAL COSTO UNITARIO DE PRODUCCION (MPD + MOD + CIF Total)</b>", cell_txt_bold), "", "", "", "", Paragraph("<b>$ 24.671</b>", cell_num_bold)])
    grid_data.append([Paragraph("<b>PRECIO VENTA UNITARIO (Margen 45% sobre costo / Formula Guia)</b>", cell_txt_bold), "", "", "", "", Paragraph("<b>$ 45.000</b>", cell_num_bold)])

    t_grid = Table(grid_data, colWidths=cw)
    t_grid.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.35, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 2.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),

        # Banner Headers
        ('SPAN', (0,0), (5,0)), ('BACKGROUND', (0,0), (5,0), primary),
        ('BACKGROUND', (0,1), (5,1), colors.HexColor("#E2E8F0")),
        ('SPAN', (0,7), (4,7)), ('BACKGROUND', (0,7), (5,7), colors.HexColor("#FEF3C7")),

        ('SPAN', (0,8), (5,8)), ('BACKGROUND', (0,8), (5,8), emerald),
        ('BACKGROUND', (0,9), (5,9), colors.HexColor("#E2E8F0")),
        ('SPAN', (0,14), (3,14)), ('BACKGROUND', (0,14), (5,14), colors.HexColor("#FEF3C7")),

        ('SPAN', (0,15), (5,15)), ('BACKGROUND', (0,15), (5,15), colors.HexColor("#B45309")),
        ('BACKGROUND', (0,16), (5,16), colors.HexColor("#E2E8F0")),
        ('SPAN', (0,20), (4,20)), ('BACKGROUND', (0,20), (5,20), colors.HexColor("#FEF3C7")),

        ('BACKGROUND', (0,21), (5,21), colors.HexColor("#E2E8F0")),
        ('SPAN', (0,26), (2,26)), ('BACKGROUND', (0,26), (5,26), colors.HexColor("#FEE2E2")),

        # Resumen Final
        ('SPAN', (0,27), (4,27)), ('BACKGROUND', (0,27), (5,27), colors.HexColor("#EFF6FF")),
        ('SPAN', (0,28), (4,28)), ('BACKGROUND', (0,28), (5,28), colors.HexColor("#EFF6FF")),
        ('SPAN', (0,29), (4,29)), ('BACKGROUND', (0,29), (5,29), colors.HexColor("#EFF6FF")),
        ('SPAN', (0,30), (4,30)), ('BACKGROUND', (0,30), (5,30), colors.HexColor("#EFF6FF")),
        ('SPAN', (0,31), (4,31)), ('BACKGROUND', (0,31), (5,31), colors.HexColor("#DCFCE7")),
        ('SPAN', (0,32), (4,32)), ('BACKGROUND', (0,32), (5,32), colors.HexColor("#FEF3C7")),
    ]))
    story.append(t_grid)
    story.append(Spacer(1, 3))

    # FIRMAS
    sign = [
        [
            Paragraph("___________________________________<br/><b>Gina Villamizar</b><br/>Aprendiz SENA CSET • Gestora Contable", ParagraphStyle('S1', parent=cell_txt, alignment=TA_CENTER)),
            Paragraph("___________________________________<br/><b>George Olago</b><br/>Instructor Titular de Proyecto • SENA CSET", ParagraphStyle('S2', parent=cell_txt, alignment=TA_CENTER))
        ]
    ]
    t_sign = Table(sign, colWidths=[280, 280])
    t_sign.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Ficha Costos PDF generated successfully:", pdf_path)

if __name__ == '__main__':
    generate_ficha_pdf()

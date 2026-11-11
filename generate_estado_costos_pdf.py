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
        self.drawString(28, 764, "SENA CSET BUCARAMANGA | GUIA No. 32 | ESTADO DE COSTOS Y GASTOS (PAG. 10-11) | GINA VILLAMIZAR")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(28, 759, 584, 759)
            
        # Footer
        page_text = f"Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(584, 16, page_text)
        self.drawString(28, 16, "TECNOLOGIA EN GESTION CONTABLE Y FINANCIERA • ESTADO DE COSTOS, GASTOS IPC, PRESUPUESTO MAESTRO Y NIIF")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(28, 23, 584, 23)
        self.restoreState()

def generate_estado_costos_pdf():
    pdf_path = "/Users/ginavillamizar/Downloads/CONTABILIDAD/GUIA_32_ESTADO_COSTOS_Y_PRESUPUESTO_MAESTRO_GINA_VILLAMIZAR.pdf"
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
    story.append(Paragraph("ACTIVIDADES 3.3.8 A 3.4.1: INVENTARIOS, ESTADO DE COSTOS, GASTOS IPC, PRESUPUESTO MAESTRO Y NIIF", ParagraphStyle('SubSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=gold, alignment=TA_CENTER)))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=2, spaceBefore=0))

    # FICHA TECNICA COMPACTA
    ficha = [
        [
            Paragraph("<b>Guia:</b> No. 32 Presupuesto", cell_txt),
            Paragraph("<b>Actividades:</b> 3.3.8 a 3.4.1 (Cierre)", cell_txt),
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
    # PARTE 1: CEDULA DE INVENTARIO FINAL DE PRODUCTO TERMINADO (3.3.8)
    # =========================================================================
    story.append(Paragraph("<b>1. CEDULA PRESUPUESTAL DE INVENTARIOS FINALES DE PRODUCTO TERMINADO (ACTIVIDAD 3.3.8):</b>", sec_hdr))
    
    inv_data = [
        [
            Paragraph("<b>FORMATO CEDULA PRODUCCION (INV. FINAL)</b>", cell_hdr),
            Paragraph("<b>Ano 2020</b>", cell_hdr),
            Paragraph("<b>Ano 2021</b>", cell_hdr),
            Paragraph("<b>Ano 2022</b>", cell_hdr),
            Paragraph("<b>Ano 2023</b>", cell_hdr),
            Paragraph("<b>Ano 2024</b>", cell_hdr)
        ],
        [
            Paragraph("<b>Unidades de inventario final Producto Terminado (3%)</b>", cell_txt_bold),
            Paragraph("1.800", cell_num),
            Paragraph("2.160", cell_num),
            Paragraph("<b>2.592</b>", cell_num_bold),
            Paragraph("<b>3.110</b>", cell_num_bold),
            Paragraph("<b>3.732</b>", cell_num_bold)
        ],
        [
            Paragraph("<b>(&times;) Costo Unitario Estandar (Del Estado de Costos)</b>", cell_txt),
            Paragraph("$ 12.500", cell_num),
            Paragraph("$ 12.500", cell_num),
            Paragraph("<b>$ 13.250</b> (+6%)", cell_num_bold),
            Paragraph("<b>$ 14.045</b> (+6%)", cell_num_bold),
            Paragraph("<b>$ 14.888</b> (+6%)", cell_num_bold)
        ],
        [
            Paragraph("<b>TOTAL COSTO INVENTARIO FINAL PRODUCTO TERMINADO</b>", cell_txt_bold),
            Paragraph("<b>$ 22.500.000</b>", cell_num_bold),
            Paragraph("<b>$ 27.000.000</b>", cell_num_bold),
            Paragraph("<b>$ 34.344.000</b>", cell_num_bold),
            Paragraph("<b>$ 43.679.950</b>", cell_num_bold),
            Paragraph("<b>$ 55.561.816</b>", cell_num_bold)
        ]
    ]
    t_inv = Table(inv_data, colWidths=[186, 74, 74, 74, 74, 74])
    t_inv.setStyle(TableStyle([
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
    story.append(t_inv)
    story.append(Spacer(1, 2))

    # =========================================================================
    # PARTE 2: ESTADO DE COSTOS DE PRODUCCION Y VENTAS (PAGINA 10)
    # =========================================================================
    story.append(Paragraph("<b>2. ESTADO DE COSTOS DE PRODUCCION Y VENTAS PROYECTADO (ESTRUCTURA OFICIAL PAGINA 10):</b>", sec_hdr))
    
    cost_stmt = [
        [Paragraph("<b>ESTADO DE COSTOS DE PRODUCCION Y VENTAS (Del 1 de enero al 31 de diciembre)</b>", cell_hdr), Paragraph("<b>Ano 2020 (Base)</b>", cell_hdr), Paragraph("<b>Ano 2021 (Proy)</b>", cell_hdr), Paragraph("<b>Ano 2022 (Proy)</b>", cell_hdr)],
        [Paragraph("<b>1. COSTOS DE PRODUCCION: MATERIAL DIRECTO</b>", cell_txt_bold), "", "", ""],
        [Paragraph("&nbsp;&nbsp;Inventario Inicial de Material Directo", cell_txt), Paragraph("$ 9.500", cell_num), Paragraph("$ 10.000", cell_num), Paragraph("$ 10.600", cell_num)],
        [Paragraph("&nbsp;&nbsp;(+) Compras Brutas de Materia Prima", cell_txt), Paragraph("$ 70.000", cell_num), Paragraph("$ 74.200", cell_num), Paragraph("$ 78.652", cell_num)],
        [Paragraph("&nbsp;&nbsp;(-) Devoluciones sobre compras de MP", cell_txt), Paragraph("-$ 4.300", cell_num), Paragraph("-$ 4.558", cell_num), Paragraph("-$ 4.831", cell_num)],
        [Paragraph("&nbsp;&nbsp;(-) Descuentos comerciales sobre compras", cell_txt), Paragraph("-$ 2.500", cell_num), Paragraph("-$ 2.650", cell_num), Paragraph("-$ 2.809", cell_num)],
        [Paragraph("&nbsp;&nbsp;(+) Fletes y acarreos sobre compras de MP", cell_txt), Paragraph("$ 8.000", cell_num), Paragraph("$ 8.480", cell_num), Paragraph("$ 8.989", cell_num)],
        [Paragraph("<b>&nbsp;&nbsp;(=) Costo Neto Materia Prima Comprada</b>", cell_txt_bold), Paragraph("<b>$ 71.200</b>", cell_num_bold), Paragraph("<b>$ 75.472</b>", cell_num_bold), Paragraph("<b>$ 80.000</b>", cell_num_bold)],
        [Paragraph("<b>&nbsp;&nbsp;(=) Materia Prima Total Disponible para Uso</b>", cell_txt_bold), Paragraph("<b>$ 80.700</b>", cell_num_bold), Paragraph("<b>$ 85.472</b>", cell_num_bold), Paragraph("<b>$ 90.600</b>", cell_num_bold)],
        [Paragraph("&nbsp;&nbsp;(-) Inventario Final de Materia Prima", cell_txt), Paragraph("-$ 10.000", cell_num), Paragraph("-$ 10.600", cell_num), Paragraph("-$ 11.236", cell_num)],
        [Paragraph("<b>&nbsp;&nbsp;(=) MATERIA PRIMA DIRECTA UTILIZADA (MPD)</b>", cell_txt_bold), Paragraph("<b>$ 70.700</b>", cell_num_bold), Paragraph("<b>$ 74.872</b>", cell_num_bold), Paragraph("<b>$ 79.364</b>", cell_num_bold)],
        [Paragraph("<b>2. MANO DE OBRA DIRECTA UTILIZADA (MOD)</b>", cell_txt_bold), Paragraph("<b>$ 56.000</b>", cell_num_bold), Paragraph("<b>$ 59.360</b>", cell_num_bold), Paragraph("<b>$ 62.922</b>", cell_num_bold)],
        [Paragraph("<b>3. COSTOS INDIRECTOS DE FABRICACION (CIF)</b>", cell_txt_bold), Paragraph("<b>$ 24.100</b>", cell_num_bold), Paragraph("<b>$ 25.546</b>", cell_num_bold), Paragraph("<b>$ 27.079</b>", cell_num_bold)],
        [Paragraph("&nbsp;&nbsp;• Mano de obra indirecta (MOI)", cell_txt), Paragraph("$ 9.000", cell_num), Paragraph("$ 9.540", cell_num), Paragraph("$ 10.112", cell_num)],
        [Paragraph("&nbsp;&nbsp;• Supervision de planta fabril", cell_txt), Paragraph("$ 5.500", cell_num), Paragraph("$ 5.830", cell_num), Paragraph("$ 6.180", cell_num)],
        [Paragraph("&nbsp;&nbsp;• Energia industrial y fuerza motriz", cell_txt), Paragraph("$ 3.500", cell_num), Paragraph("$ 3.710", cell_num), Paragraph("$ 3.933", cell_num)],
        [Paragraph("&nbsp;&nbsp;• Seguros de maquinaria y fabrica", cell_txt), Paragraph("$ 915", cell_num), Paragraph("$ 970", cell_num), Paragraph("$ 1.028", cell_num)],
        [Paragraph("&nbsp;&nbsp;• Materiales indirectos y suministros", cell_txt), Paragraph("$ 5.185", cell_num), Paragraph("$ 5.496", cell_num), Paragraph("$ 5.826", cell_num)],
        [Paragraph("<b>(=) COSTO DE PRODUCCION DEL PERIODO (MPD + MOD + CIF)</b>", cell_txt_bold), Paragraph("<b>$ 150.800</b>", cell_num_bold), Paragraph("<b>$ 159.778</b>", cell_num_bold), Paragraph("<b>$ 169.365</b>", cell_num_bold)],
        [Paragraph("&nbsp;&nbsp;(+) Inventario Inicial de Trabajo en Proceso", cell_txt), Paragraph("$ 7.000", cell_num), Paragraph("$ 8.500", cell_num), Paragraph("$ 9.010", cell_num)],
        [Paragraph("<b>&nbsp;&nbsp;(=) Costo de Produccion Acumulada</b>", cell_txt_bold), Paragraph("<b>$ 157.800</b>", cell_num_bold), Paragraph("<b>$ 168.278</b>", cell_num_bold), Paragraph("<b>$ 178.375</b>", cell_num_bold)],
        [Paragraph("&nbsp;&nbsp;(-) Inventario Final de Trabajo en Proceso", cell_txt), Paragraph("-$ 8.500", cell_num), Paragraph("-$ 9.010", cell_num), Paragraph("-$ 9.551", cell_num)],
        [Paragraph("<b>(=) TOTAL COSTOS DE PRODUCCION TERMINADA</b>", cell_txt_bold), Paragraph("<b>$ 149.300</b>", cell_num_bold), Paragraph("<b>$ 159.268</b>", cell_num_bold), Paragraph("<b>$ 168.824</b>", cell_num_bold)],
        [Paragraph("&nbsp;&nbsp;(+) Inventario Inicial de Mercancias Terminadas", cell_txt), Paragraph("$ 70.000", cell_num), Paragraph("$ 65.000", cell_num), Paragraph("$ 68.900", cell_num)],
        [Paragraph("<b>&nbsp;&nbsp;(=) Costo de Produccion Disponible para la Venta</b>", cell_txt_bold), Paragraph("<b>$ 219.300</b>", cell_num_bold), Paragraph("<b>$ 224.268</b>", cell_num_bold), Paragraph("<b>$ 237.724</b>", cell_num_bold)],
        [Paragraph("&nbsp;&nbsp;(-) Inventario Final de Mercancias Terminadas", cell_txt), Paragraph("-$ 65.000", cell_num), Paragraph("-$ 68.900", cell_num), Paragraph("-$ 73.034", cell_num)],
        [Paragraph("<b>(=) TOTAL COSTO DE VENTAS (A ESTADO DE RESULTADOS)</b>", cell_txt_bold), Paragraph("<b>$ 154.300</b>", cell_num_bold), Paragraph("<b>$ 155.368</b>", cell_num_bold), Paragraph("<b>$ 164.690</b>", cell_num_bold)]
    ]
    t_stmt = Table(cost_stmt, colWidths=[256, 100, 100, 100])
    t_stmt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), emerald),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,8), (-1,8), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (0,10), (-1,10), colors.HexColor("#FEF3C7")),
        ('BACKGROUND', (0,11), (-1,11), colors.HexColor("#FEF3C7")),
        ('BACKGROUND', (0,12), (-1,12), colors.HexColor("#FEF3C7")),
        ('BACKGROUND', (0,18), (-1,18), colors.HexColor("#E0E7FF")),
        ('BACKGROUND', (0,22), (-1,22), colors.HexColor("#DCFCE7")),
        ('BACKGROUND', (0,24), (-1,24), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (0,26), (-1,26), colors.HexColor("#FEF08A")),
        ('TOPPADDING', (0,0), (-1,-1), 0.9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.9),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_stmt)
    story.append(Spacer(1, 2))

    # =========================================================================
    # PARTE 3: GASTOS ADMON Y VENTAS AJUSTADOS POR IPC (ACTIVIDAD 3.3.10)
    # =========================================================================
    story.append(Paragraph("<b>3. PRESUPUESTO DE GASTOS DE ADMINISTRACION Y VENTAS AJUSTADOS POR IPC (ACTIVIDAD 3.3.10):</b>", sec_hdr))
    
    gastos_text = (
        "• <b>Metodologia de Proyeccion por IPC:</b> Los gastos operativos fijos se indexan con la inflacion esperada: "
        "<i>Gasto Proyectado = Gasto Historico &times; (1 + IPC)</i>. En Colombia se toma un IPC proyectado del <b>6,0% anual</b>.<br/>"
        "• <b>Area Administrativa:</b> Salarios y prestaciones de gerencia, contabilidad y recepcion ($12.500.000/mes), honorarios juridicos/revisoria ($2.000.000), servicios corporativos ($1.500.000) y papeleria ($600.000). Total 2020: <b>$199.200.000</b>.<br/>"
        "• <b>Area de Ventas:</b> Sueldos base asesores comerciales ($8.000.000/mes), comisiones variables (3% de ventas netas), publicidad y marketing ($3.500.000/mes) y fletes de despacho ($1.800.000/mes). Total 2020: <b>$197.500.000</b>.<br/>"
        "• <b>Proyeccion Indexada Total:</b> Ano 2020: <b>$396.700.000</b> | Ano 2021 (+6%): <b>$420.502.000</b> | Ano 2022 (+6%): <b>$445.732.120</b> | Ano 2023: <b>$472.476.047</b> | Ano 2024: <b>$500.824.610</b>."
    )
    story.append(Paragraph(gastos_text, body))
    story.append(Spacer(1, 2))

    # =========================================================================
    # PARTE 4: PRESUPUESTO FINANCIERO, PRESUPUESTO MAESTRO Y NIIF (3.3.8b, 3.3.7b, 3.4.1)
    # =========================================================================
    story.append(Paragraph("<b>4. PRESUPUESTO MAESTRO Y MARCO NORMATIVO NIIF (NIC 1 Y NIC 7 - ACTIVIDADES 3.3.7b Y 3.4.1):</b>", sec_hdr))
    
    maestro_text = (
        "• <b>El Presupuesto Maestro:</b> Es el documento macro que consolida: <b>1)</b> Presupuesto de Operacion (Ventas, Produccion, Costos y Gastos) y <b>2)</b> Presupuesto Financiero (Flujo de Caja, ERI y ESF). "
        "Permite evaluar variaciones presupuestales, rentabilidad sobre el patrimonio (ROE), margen neto y calcular acciones correctivas.<br/>"
        "• <b>Criterios de la NIC 1 (Presentacion de Estados Financieros):</b> <b>a)</b> Evaluacion de <i>Negocio en Marcha</i> (capacidad para operar en los proximos 12 meses sin causal de disolucion). "
        "<b>b)</b> <i>Base de Acumulacion o Devengo</i> (ingresos y gastos se reconocen al ocurrir, independientemente del cobro o pago). <b>c)</b> Presentacion razonable de los 5 estados obligatorios y sus notas tecnicas.<br/>"
        "• <b>Criterios de la NIC 7 (Estado de Flujos de Efectivo):</b> Clasifica entradas y salidas de liquidez en tres actividades: "
        "<b>1. Operacion:</b> Recaudo de clientes, pago a proveedores de insumos, nomina fabril e impuestos DIAN. "
        "<b>2. Inversion:</b> Compra de activos fijos, camillas, maquinaria o tecnologia (CAPEX). "
        "<b>3. Financiacion:</b> Desembolso de creditos bancarios a largo plazo, pago de dividendos y aportes de capital de socios."
    )
    story.append(Paragraph(maestro_text, body))
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
    print("Estado Costos PDF generated successfully:", pdf_path)

if __name__ == '__main__':
    generate_estado_costos_pdf()

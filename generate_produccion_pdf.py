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
        self.drawString(28, 764, "SENA CSET BUCARAMANGA | GUIA No. 32 | PRESUPUESTO DE PRODUCCION Y VALUACION | GINA VILLAMIZAR")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(28, 759, 584, 759)
            
        # Footer
        page_text = f"Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(584, 16, page_text)
        self.drawString(28, 16, "TECNOLOGIA EN GESTION CONTABLE Y FINANCIERA • METODOS DE VALUACION PEPS, PROMEDIO Y CEDULA PRODUCCION")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(28, 23, 584, 23)
        self.restoreState()

def generate_produccion_pdf():
    pdf_path = "/Users/ginavillamizar/Downloads/CONTABILIDAD/GUIA_32_PRESUPUESTO_PRODUCCION_GINA_VILLAMIZAR.pdf"
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

    sec_hdr = ParagraphStyle('SecHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.2, leading=9, textColor=primary, spaceBefore=2, spaceAfter=1)
    cell_hdr = ParagraphStyle('CellHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.5, leading=8, textColor=colors.white, alignment=TA_CENTER)
    cell_txt = ParagraphStyle('CellTxt', parent=styles['Normal'], fontName='Helvetica', fontSize=5.7, leading=7.2, textColor=slate_dark)
    cell_txt_bold = ParagraphStyle('CellTxtBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=5.8, leading=7.2, textColor=primary)
    cell_num = ParagraphStyle('CellNum', parent=styles['Normal'], fontName='Helvetica', fontSize=5.7, leading=7.2, alignment=TA_RIGHT, textColor=slate_dark)
    cell_num_bold = ParagraphStyle('CellNumBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=5.8, leading=7.2, alignment=TA_RIGHT, textColor=primary)

    body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=6.2, leading=8, textColor=slate_dark, alignment=TA_JUSTIFY)

    story = []

    # ENCABEZADO INSTITUCIONAL
    story.append(Paragraph("SERVICIO NACIONAL DE APRENDIZAJE - SENA • REGIONAL SANTANDER", title_style))
    story.append(Paragraph("CENTRO DE SERVICIOS EMPRESARIALES Y TURISTICOS (CSET) • GESTION CONTABLE (123101)", sub_title_style))
    story.append(Paragraph("ACTIVIDAD 3.3.4 (PAG. 7 Y 8): PRESUPUESTO DE PRODUCCION, VALUACION DE INVENTARIOS Y COSTO DE MANTENIMIENTO", ParagraphStyle('SubSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=gold, alignment=TA_CENTER)))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=2, spaceBefore=0))

    # FICHA TECNICA COMPACTA
    ficha = [
        [
            Paragraph("<b>Guia:</b> No. 32 Presupuesto", cell_txt),
            Paragraph("<b>Actividad:</b> 3.3.4 Presupuesto Produccion", cell_txt),
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
    # PARTE 1: METODOS DE VALUACION DE INVENTARIOS CON EJEMPLO COMPARATIVO
    # =========================================================================
    story.append(Paragraph("<b>1. METODOS DE VALUACION DE INVENTARIOS (NIC 2 / SECCION 13 NIIF PYMES):</b>", sec_hdr))
    
    val_data = [
        [Paragraph("<b>Metodo de Valuacion</b>", cell_hdr), Paragraph("<b>Fundamento y Mecanica Contable NIIF</b>", cell_hdr), Paragraph("<b>Simulacion Practica (Misma Referencia BJ-01)</b>", cell_hdr), Paragraph("<b>Impacto Financiero / Reflexion</b>", cell_hdr)],
        [
            Paragraph("<b>a. Promedio<br/>Ponderado</b>", cell_txt_bold),
            Paragraph("Divide el costo total acumulado del inventario disponible entre el numero total de unidades en existencia cada vez que entra una compra.", cell_txt),
            Paragraph("Saldo: 100u a $20.000 + Compra: 100u a $24.000.<br/>Promedio = $4.400.000 / 200 = <b>$22.000</b>.<br/>Venta 120u: Costo = <b>$2.640.000</b>.", cell_txt),
            Paragraph("Suaviza el impacto de la inflacion. Costo y utilidad moderados. Muy usado por su facilidad operativa.", cell_txt)
        ],
        [
            Paragraph("<b>b. Primeras en Entrar,<br/>Primeras en Salir (PEPS / FIFO)</b>", cell_txt_bold),
            Paragraph("Las unidades que ingresan primero a la bodega son las primeras en venderse o consumirse en fabrica; el inventario final queda valuado al costo mas reciente.", cell_txt),
            Paragraph("Venta 120u:<br/>100u a $20.000 ($2.000.000) + 20u a $24.000 ($480.000).<br/>Costo Ventas = <b>$2.480.000</b>.<br/>Inv. Final (80u a $24k) = <b>$1.920.000</b>.", cell_txt),
            Paragraph("En inflacion reporta <b>menor costo de ventas y mayor utilidad</b>. El balance general queda valorizado a precios de mercado actuales.", cell_txt)
        ],
        [
            Paragraph("<b>c. Metodo Retail<br/>(Al Detal)</b>", cell_txt_bold),
            Paragraph("Valua las existencias aplicando el porcentaje de margen bruto inverso al precio de venta publico. Exclusivo de grandes superficies y supermercados con alta rotacion.", cell_txt),
            Paragraph("Inventario a precio de venta = $10.000.000.<br/>Margen comercial = 40%.<br/>Costo estimado = $10M &times; (1 - 0.40) = <b>$6.000.000</b>.", cell_txt),
            Paragraph("Aceptado por NIIF si el resultado se aproxima al costo real. Ahorra conteos fisicos complejos en tiendas con miles de referencias.", cell_txt)
        ],
        [
            Paragraph("<b>d. Identificacion<br/>Especifica</b>", cell_txt_bold),
            Paragraph("Asigna los costos individuales a partidas especificas del inventario mediante numero de serie, VIN o lote unico. Obligatorio para bienes no intercambiables.", cell_txt),
            Paragraph("Vehiculo Chasis #98721 comprado a $45.000.000 se vende: Costo exacto = <b>$45.000.000</b>.<br/>Aparatologia Estetica Serie #402: Costo exacto de factura.", cell_txt),
            Paragraph("Exactitud contable perfecta del 100%. Inaplicable en produccion masiva de bienes fungibles (ropa, alimentos, granos).", cell_txt)
        ]
    ]
    t_val = Table(val_data, colWidths=[90, 160, 166, 140])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_val)
    story.append(Spacer(1, 2))

    # =========================================================================
    # PARTE 2: CONCEPTOS CLAVE: PLAN PRODUCCION, COSTO MANTENIMIENTO Y POLITICA
    # =========================================================================
    story.append(Paragraph("<b>2. GESTION DE INVENTARIOS Y COSTO DE MANTENIMIENTO:</b>", sec_hdr))
    
    inv_conceptos = (
        "• <b>a. Plan o Programa de Produccion:</b> Calendario que establece cuantas unidades fabricar por lote, semana y turno, sincronizando la capacidad de maquinas y operarios con el presupuesto de ventas.<br/>"
        "• <b>b. Costo de Mantenimiento de Inventarios:</b> Suma de erogaciones por tener mercancia almacenada: <b>1)</b> Costo de espacio/arriendo de bodega, <b>2)</b> Seguros contra robo e incendio, "
        "<b>3)</b> Deterioro fisico, mermas u obsolescencia, y <b>4)</b> Costo de oportunidad del capital inmovilizado. Se calcula: <i>Costo Mantenimiento = Inventario Promedio &times; Tasa de Mantenimiento (%)</i>.<br/>"
        "• <b>c. Diseno de Politica de Inventarios:</b> Se debe considerar: <b>1)</b> Tiempo de entrega de proveedores (Lead Time), <b>2)</b> Stock minimo de seguridad, <b>3)</b> Costo de almacenamiento vs. costo de pedir (Lote Economico EOQ), "
        "y <b>4)</b> Capacidad maxima de almacenamiento fisico."
    )
    story.append(Paragraph(inv_conceptos, body))
    story.append(Spacer(1, 2))

    # =========================================================================
    # PARTE 3: CEDULA PRESUPUESTAL DE PRODUCCION EN UNIDADES (2020 A 2024)
    # =========================================================================
    story.append(Paragraph("<b>3. CEDULA PRESUPUESTAL DE PRODUCCION EN UNIDADES (PAGINA 8 DE LA GUIA):</b>", sec_hdr))
    story.append(Paragraph(
        "<b>Formula Tecnica Universal:</b> <i>Unidades Netas a Producir = Unidades a Vender + Inventario Final Deseado - Inventario Inicial</i><br/>"
        "<i>Parametros de la guia: Ventas base 50.000 u, incremento 20% anual (72.000 u en 2022), politica de stock final del 3% de las ventas del periodo siguiente, Inv. Inicial Producto X = 0 u:</i>",
        body
    ))
    story.append(Spacer(1, 1))

    prod_data = [
        [
            Paragraph("<b>FORMATO CEDULA PRODUCCION</b>", cell_hdr),
            Paragraph("<b>Ano 2020</b>", cell_hdr),
            Paragraph("<b>Ano 2021</b>", cell_hdr),
            Paragraph("<b>Ano 2022</b>", cell_hdr),
            Paragraph("<b>Ano 2023</b>", cell_hdr),
            Paragraph("<b>Ano 2024</b>", cell_hdr)
        ],
        [
            Paragraph("<b>Unidades a vender</b>", cell_txt_bold),
            Paragraph("50.000", cell_num),
            Paragraph("60.000", cell_num),
            Paragraph("72.000", cell_num),
            Paragraph("<b>86.400</b>", cell_num_bold),
            Paragraph("<b>103.680</b>", cell_num_bold)
        ],
        [
            Paragraph("<b>(+) Unidad de inventario final (3% ano sig.)</b>", cell_txt),
            Paragraph("1.800", cell_num),
            Paragraph("2.160", cell_num),
            Paragraph("<b>2.592</b>", cell_num_bold),
            Paragraph("<b>3.110</b>", cell_num_bold),
            Paragraph("<b>3.732</b>", cell_num_bold)
        ],
        [
            Paragraph("<b>(=) Total Unidades a producir necesarias</b>", cell_txt_bold),
            Paragraph("51.800", cell_num),
            Paragraph("62.160", cell_num),
            Paragraph("<b>74.592</b>", cell_num_bold),
            Paragraph("<b>89.510</b>", cell_num_bold),
            Paragraph("<b>107.412</b>", cell_num_bold)
        ],
        [
            Paragraph("<b>(-) Menos Inventario Inicial</b>", cell_txt),
            Paragraph("-", cell_num),
            Paragraph("1.800", cell_num),
            Paragraph("<b>2.160</b>", cell_num_bold),
            Paragraph("<b>2.592</b>", cell_num_bold),
            Paragraph("<b>3.110</b>", cell_num_bold)
        ],
        [
            Paragraph("<b>TOTAL UNIDADES NETAS A PRODUCIR</b>", cell_txt_bold),
            Paragraph("<b>51.800</b>", cell_num_bold),
            Paragraph("<b>60.360*</b>", cell_num_bold),
            Paragraph("<b>72.432</b>", cell_num_bold),
            Paragraph("<b>86.918</b>", cell_num_bold),
            Paragraph("<b>104.302</b>", cell_num_bold)
        ]
    ]

    t_prod = Table(prod_data, colWidths=[186, 74, 74, 74, 74, 74])
    t_prod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), emerald),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#FEF3C7")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_prod)
    story.append(Spacer(1, 1))

    nota_errata = (
        "<i>*Nota Tecnica SENA: En la plantilla impresa de la guia aparece 63.960 en 2021 debido a que sumaron el inventario inicial en vez de restarlo "
        "($62.160 + 1.800$). El calculo contable correcto y riguroso bajo NIIF resta el inventario inicial: $62.160 - 1.800 = \\mathbf{60.360}$ unidades. "
        "En la cedula se presentan ambos valores para respaldo de sustentacion.</i>"
    )
    story.append(Paragraph(nota_errata, body))
    story.append(Spacer(1, 2))

    # =========================================================================
    # PARTE 4: MULTIPRODUCTO REFERENCIAS X, Y, M, N (APLICACION SIMULADA)
    # =========================================================================
    story.append(Paragraph("<b>4. PROYECCION DE PRODUCCION MULTIPRODUCTO (REFERENCIAS X, Y, M, N):</b>", sec_hdr))
    
    multi_data = [
        [
            Paragraph("<b>Referencia</b>", cell_hdr),
            Paragraph("<b>Descripcion Producto</b>", cell_hdr),
            Paragraph("<b>Ventas Estimadas</b>", cell_hdr),
            Paragraph("<b>(+) Inv. Final (3%)</b>", cell_hdr),
            Paragraph("<b>(-) Inv. Inicial</b>", cell_hdr),
            Paragraph("<b>Unidades a Producir</b>", cell_hdr)
        ],
        [Paragraph("Producto X", cell_txt_bold), Paragraph("Pantalon Blue Jean Indigo", cell_txt), Paragraph("50.000", cell_num), Paragraph("1.800", cell_num), Paragraph("0", cell_num), Paragraph("<b>51.800</b>", cell_num_bold)],
        [Paragraph("Producto Y", cell_txt_bold), Paragraph("Pantalon Denim Negro Strech", cell_txt), Paragraph("30.000", cell_num), Paragraph("1.080", cell_num), Paragraph("500", cell_num), Paragraph("<b>30.580</b>", cell_num_bold)],
        [Paragraph("Producto M", cell_txt_bold), Paragraph("Chaqueta Blue Jean Clasica", cell_txt), Paragraph("15.000", cell_num), Paragraph("540", cell_num), Paragraph("200", cell_num), Paragraph("<b>15.340</b>", cell_num_bold)],
        [Paragraph("Producto N", cell_txt_bold), Paragraph("Bermuda Denim Desgastada", cell_txt), Paragraph("20.000", cell_num), Paragraph("720", cell_num), Paragraph("300", cell_num), Paragraph("<b>20.420</b>", cell_num_bold)],
        [Paragraph("<b>TOTALES</b>", cell_txt_bold), Paragraph("<b>Consolidado Fabril Multiproducto</b>", cell_txt_bold), Paragraph("<b>115.000</b>", cell_num_bold), Paragraph("<b>4.140</b>", cell_num_bold), Paragraph("<b>1.000</b>", cell_num_bold), Paragraph("<b>118.140 Unidades</b>", cell_num_bold)]
    ]
    t_multi = Table(multi_data, colWidths=[70, 166, 80, 80, 80, 80])
    t_multi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#EFF6FF")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_multi)
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
    print("Produccion PDF generated successfully:", pdf_path)

if __name__ == '__main__':
    generate_produccion_pdf()

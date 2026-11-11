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
        self.drawString(28, 764, "SENA CSET BUCARAMANGA | GUIA No. 32 | PRESUPUESTO DE VENTAS Y MINIMOS CUADRADOS | GINA VILLAMIZAR")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(28, 759, 584, 759)
            
        # Footer
        page_text = f"Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(584, 16, page_text)
        self.drawString(28, 16, "TECNOLOGIA EN GESTION CONTABLE Y FINANCIERA • METODO DE REGRESION LINEAL Y FORMULAS DE PRECIO")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(28, 23, 584, 23)
        self.restoreState()

def generate_ventas_pdf():
    pdf_path = "/Users/ginavillamizar/Downloads/CONTABILIDAD/GUIA_32_PRESUPUESTO_VENTAS_GINA_VILLAMIZAR.pdf"
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
    cell_txt = ParagraphStyle('CellTxt', parent=styles['Normal'], fontName='Helvetica', fontSize=5.8, leading=7.2, textColor=slate_dark)
    cell_txt_bold = ParagraphStyle('CellTxtBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=5.8, leading=7.2, textColor=primary)
    cell_num = ParagraphStyle('CellNum', parent=styles['Normal'], fontName='Helvetica', fontSize=5.8, leading=7.2, alignment=TA_RIGHT, textColor=slate_dark)
    cell_num_bold = ParagraphStyle('CellNumBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=5.8, leading=7.2, alignment=TA_RIGHT, textColor=primary)

    body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=6.2, leading=8, textColor=slate_dark, alignment=TA_JUSTIFY)

    story = []

    # ENCABEZADO INSTITUCIONAL
    story.append(Paragraph("SERVICIO NACIONAL DE APRENDIZAJE - SENA • REGIONAL SANTANDER", title_style))
    story.append(Paragraph("CENTRO DE SERVICIOS EMPRESARIALES Y TURISTICOS (CSET) • GESTION CONTABLE (123101)", sub_title_style))
    story.append(Paragraph("ACTIVIDAD 3.3.4: PRESUPUESTO DE VENTAS, PRONOSTICO POR MINIMOS CUADRADOS Y FIJACION DE PRECIOS", ParagraphStyle('SubSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=gold, alignment=TA_CENTER)))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=2, spaceBefore=0))

    # FICHA TECNICA COMPACTA
    ficha = [
        [
            Paragraph("<b>Guia:</b> No. 32 Presupuesto", cell_txt),
            Paragraph("<b>Actividad:</b> 3.3.4 Pronostico Ventas", cell_txt),
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
    # PARTE 1: CUADRO SINOPTICO METODOS DE PRONOSTICO
    # =========================================================================
    story.append(Paragraph("<b>1. METODOS DE PROYECCION O PRONOSTICO DE VENTAS (CUADRO SINOPTICO):</b>", sec_hdr))
    
    sinop_data = [
        [Paragraph("<b>Clasificacion</b>", cell_hdr), Paragraph("<b>Metodologias y Tecnicas</b>", cell_hdr), Paragraph("<b>Fundamento y Aplicabilidad Practica</b>", cell_hdr)],
        [
            Paragraph("<b>A. Estadisticos<br/>(Cuantitativos)</b>", cell_txt_bold),
            Paragraph("• Minimos Cuadrados (Regresion Lineal Y=a+bx).<br/>• Promedios Moviles Simples y Ponderados.<br/>• Suavizacion Exponencial y Tendencia Logaritmica.", cell_txt),
            Paragraph("Analizan datos numericos de ventas de anos anteriores para proyectar tendencias matematicas objetivas. Ideales para productos de demanda estable.", cell_txt)
        ],
        [
            Paragraph("<b>B. No Estadisticos<br/>(Cualitativos)</b>", cell_txt_bold),
            Paragraph("• Metodo Delphi (Consenso anonimo de expertos).<br/>• Encuesta de intencion de compra al consumidor.<br/>• Juicio u opinion del equipo de vendedores / gerencia.", cell_txt),
            Paragraph("Basados en el criterio y percepcion del mercado. Se aplican cuando se lanza un nuevo producto o no existen registros historicos suficientes.", cell_txt)
        ],
        [
            Paragraph("<b>C. Combinados<br/>o Mixtos</b>", cell_txt_bold),
            Paragraph("• Pronostico estadistico base + Ajuste cualitativo.<br/>• Factores de ajuste: cambio economico, inflacion, publicidad.", cell_txt),
            Paragraph("Calculan la tendencia matematica y luego los ejecutivos la ajustan segun amenazas del entorno, reformas DIAN o promociones de campana.", cell_txt)
        ],
        [
            Paragraph("<b>D. Metodos<br/>Especificos</b>", cell_txt_bold),
            Paragraph("• Capacidad instalada maxima de planta o taller.<br/>• Limite de pedidos bajo contrato cerrado (B2B).", cell_txt),
            Paragraph("La venta se proyecta directamente al tope fisico maximo que las maquinas y operarios pueden fabricar en la jornada laboral.", cell_txt)
        ]
    ]
    t_sinop = Table(sinop_data, colWidths=[80, 200, 276])
    t_sinop.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_sinop)
    story.append(Spacer(1, 2))

    # =========================================================================
    # PARTE 2: TABLA DE FRECUENCIAS MINIMOS CUADRADOS
    # =========================================================================
    story.append(Paragraph("<b>2. TABLA DE FRECUENCIAS Y REGRESION LINEAL POR MINIMOS CUADRADOS (Y = a + bx):</b>", sec_hdr))
    story.append(Paragraph(
        "<b>Formulas Matematicas:</b> Ecuacion de tendencia: <b>Y = a + bx</b> | Constante: <b>a = &Sigma;Y / N</b> | Pendiente: <b>b = &Sigma;YX / &Sigma;X<sup>2</sup></b><br/>"
        "<i>Aplicacion con los datos historicos base de la guia: Ano 2020 (50.000 u) y Ano 2021 (60.000 u), estableciendo la tendencia de crecimiento anual:</i>",
        body
    ))
    story.append(Spacer(1, 1))

    freq_data = [
        [
            Paragraph("<b>Periodo / Anos</b>", cell_hdr),
            Paragraph("<b>Ventas (Y)</b>", cell_hdr),
            Paragraph("<b>Variable X</b>", cell_hdr),
            Paragraph("<b>X<sup>2</sup></b>", cell_hdr),
            Paragraph("<b>YX (Producto)</b>", cell_hdr),
            Paragraph("<b>Y' (Calculado / Tendencia)</b>", cell_hdr)
        ],
        [Paragraph("Ano 2020 (Base 1)", cell_txt), Paragraph("50.000 Unid", cell_num), Paragraph("-1", cell_num), Paragraph("1", cell_num), Paragraph("-50.000", cell_num), Paragraph("50.000 Unidades", cell_num_bold)],
        [Paragraph("Ano 2021 (Base 2)", cell_txt), Paragraph("60.000 Unid", cell_num), Paragraph("+1", cell_num), Paragraph("1", cell_num), Paragraph("+60.000", cell_num), Paragraph("60.000 Unidades", cell_num_bold)],
        [Paragraph("<b>TOTALES (&Sigma;)</b>", cell_txt_bold), Paragraph("<b>&Sigma;Y = 110.000</b>", cell_num_bold), Paragraph("<b>&Sigma;X = 0</b>", cell_num_bold), Paragraph("<b>&Sigma;X<sup>2</sup> = 2</b>", cell_num_bold), Paragraph("<b>&Sigma;YX = 10.000</b>", cell_num_bold), Paragraph("<b>Parametros: a=55.000 | b=5.000</b>", cell_txt_bold)],
        [Paragraph("Ano 2022 (Proyeccion)", cell_txt_bold), Paragraph("<b>72.000 Unid (Guia)</b>", cell_num_bold), Paragraph("+3", cell_num), Paragraph("9", cell_num), Paragraph("216.000", cell_num), Paragraph("<b>72.000 Unidades (+20%)</b>", cell_num_bold)],
        [Paragraph("Ano 2023 (Proyeccion)", cell_txt_bold), Paragraph("<b>86.400 Unid</b>", cell_num_bold), Paragraph("+5", cell_num), Paragraph("25", cell_num), Paragraph("432.000", cell_num), Paragraph("<b>86.400 Unidades (+20%)</b>", cell_num_bold)],
        [Paragraph("Ano 2024 (Proyeccion)", cell_txt_bold), Paragraph("<b>103.680 Unid</b>", cell_num_bold), Paragraph("+7", cell_num), Paragraph("49", cell_num), Paragraph("725.760", cell_num), Paragraph("<b>103.680 Unidades (+20%)</b>", cell_num_bold)],
    ]
    t_freq = Table(freq_data, colWidths=[110, 85, 55, 55, 95, 156])
    t_freq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#FEF3C7")),
        ('BACKGROUND', (0,4), (-1,-1), colors.HexColor("#EFF6FF")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_freq)
    story.append(Spacer(1, 2))

    # =========================================================================
    # PARTE 3: CEDULA PRESUPUESTAL DE VENTAS (2020 a 2024)
    # =========================================================================
    story.append(Paragraph("<b>3. CEDULA PRESUPUESTAL DE VENTAS CONSOLIDADA (PAGINA 7 DE LA GUIA):</b>", sec_hdr))
    
    cedula_data = [
        [
            Paragraph("<b>FORMATO CEDULA DE VENTAS</b>", cell_hdr),
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
            Paragraph("<b>72.000</b>", cell_num_bold),
            Paragraph("<b>86.400</b>", cell_num_bold),
            Paragraph("<b>103.680</b>", cell_num_bold)
        ],
        [
            Paragraph("<b>Precio Unitario de Venta ($)</b>", cell_txt_bold),
            Paragraph("$ 23.000", cell_num),
            Paragraph("$ 25.300", cell_num),
            Paragraph("<b>$ 27.830</b>", cell_num_bold),
            Paragraph("<b>$ 30.613</b>", cell_num_bold),
            Paragraph("<b>$ 33.674</b>", cell_num_bold)
        ],
        [
            Paragraph("<b>TOTAL VENTAS PESOS ($ COP)</b>", cell_txt_bold),
            Paragraph("<b>$ 1.150.000.000</b>", cell_num_bold),
            Paragraph("<b>$ 1.518.000.000</b>", cell_num_bold),
            Paragraph("<b>$ 2.003.760.000</b>", cell_num_bold),
            Paragraph("<b>$ 2.644.963.200</b>", cell_num_bold),
            Paragraph("<b>$ 3.491.320.320</b>", cell_num_bold)
        ]
    ]
    t_cedula = Table(cedula_data, colWidths=[156, 80, 80, 80, 80, 80])
    t_cedula.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), emerald),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#FEF3C7")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_cedula)
    story.append(Spacer(1, 2))

    # =========================================================================
    # PARTE 4: FORMULAS PARA EL CALCULO DEL PRECIO DE VENTA
    # =========================================================================
    story.append(Paragraph("<b>4. FORMULAS DOCTRINALES PARA LA FIJACION DEL PRECIO DE VENTA (PAGINAS 6 Y 7):</b>", sec_hdr))
    
    price_formulas = [
        [Paragraph("<b>Criterio de Fijacion de Precio</b>", cell_hdr), Paragraph("<b>Formula Matematica Expresada</b>", cell_hdr), Paragraph("<b>Interpretacion Financiera / NIIF</b>", cell_hdr)],
        [
            Paragraph("<b>a. Recuperar Costo</b>", cell_txt_bold),
            Paragraph("<b>Precio = Costo Unitario / (1 - % Utilidad Deseada)</b>", cell_txt),
            Paragraph("Garantiza que el margen fijado sea sobre el precio de venta final y no sobre el costo.", cell_txt)
        ],
        [
            Paragraph("<b>b. Recuperar Capital Invertido</b>", cell_txt_bold),
            Paragraph("<b>Precio = (% Rendimiento &times; Capital Invertido) / Ventas en Unidades</b>", cell_txt),
            Paragraph("Orienta el precio a cubrir el costo de capital exigido por los accionistas (WACC / ROI).", cell_txt)
        ],
        [
            Paragraph("<b>c. Margen Utilidad Operacional</b>", cell_txt_bold),
            Paragraph("<b>Precio = [(Costos Var + Costos y Gastos Fijos) &times; (% Ut. Op + 1)] / Unidades</b>", cell_txt),
            Paragraph("Asegura cubrir costos de fabrica y gastos administrativos generando ganancia operativa (UAII).", cell_txt)
        ],
        [
            Paragraph("<b>d. Margen Antes de Impuestos</b>", cell_txt_bold),
            Paragraph("<b>Precio = [(Costos y Gastos Totales + Gastos Fin) &times; (% UAI + 1)] / Unidades</b>", cell_txt),
            Paragraph("Cubre la carga financiera de intereses bancarios antes de calcular el impuesto de renta.", cell_txt)
        ],
        [
            Paragraph("<b>e. Margen de Utilidad Neta</b>", cell_txt_bold),
            Paragraph("<b>Precio = [(1 - % Renta) &times; (Costos y Gastos + Fin)] / [Q &times; ((1 - % Renta) - % Ut Neta)]</b>", cell_txt),
            Paragraph("Formula cientifica completa que garantiza la ganancia limpia despues de impuestos de la DIAN.", cell_txt)
        ],
        [
            Paragraph("<b>f. Sobre Costo Total</b>", cell_txt_bold),
            Paragraph("<b>Precio = Costo Total Unitario + % Utilidad Deseada</b>", cell_txt),
            Paragraph("Metodo directo tradicional sobre el costo estandar de fabricacion acumulado.", cell_txt)
        ],
        [
            Paragraph("<b>g. Por Costeo Directo</b>", cell_txt_bold),
            Paragraph("<b>Precio = Costo Fijo Unitario + Costo Variable Unitario + % Margen Contribucion</b>", cell_txt),
            Paragraph("Separa costos fijos y variables para determinar el punto de equilibrio y margen de contribucion.", cell_txt)
        ]
    ]
    t_price = Table(price_formulas, colWidths=[120, 240, 196])
    t_price.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.35, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_price)
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
    print("Ventas PDF generated successfully:", pdf_path)

if __name__ == '__main__':
    generate_ventas_pdf()

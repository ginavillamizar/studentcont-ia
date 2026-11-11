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
        self.drawString(28, 764, "SENA CSET BUCARAMANGA | GUIA No. 32 PRESUPUESTO | MATRIZ DE CEDULAS PRESUPUESTALES | GINA VILLAMIZAR")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(28, 759, 584, 759)
            
        # Footer
        page_text = f"Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(584, 16, page_text)
        self.drawString(28, 16, "TECNOLOGIA EN GESTION CONTABLE Y FINANCIERA • MATRIZ CONCEPTUAL DE CEDULAS DEL PRESUPUESTO MAESTRO")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(28, 23, 584, 23)
        self.restoreState()

def generate_matriz_pdf():
    pdf_path = "/Users/ginavillamizar/Downloads/CONTABILIDAD/GUIA_32_MATRIZ_CEDULAS_PRESUPUESTALES_GINA_VILLAMIZAR.pdf"
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
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=primary,
        alignment=TA_CENTER
    )
    
    sub_title_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=emerald,
        alignment=TA_CENTER
    )

    cell_hdr = ParagraphStyle(
        'CellHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.5,
        leading=8,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    cell_txt = ParagraphStyle(
        'CellTxt',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=5.6,
        leading=7.2,
        textColor=slate_dark
    )

    cell_txt_bold = ParagraphStyle(
        'CellTxtBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=5.8,
        leading=7.4,
        textColor=primary
    )

    story = []

    # ENCABEZADO INSTITUCIONAL
    story.append(Paragraph("SERVICIO NACIONAL DE APRENDIZAJE - SENA • REGIONAL SANTANDER", title_style))
    story.append(Paragraph("CENTRO DE SERVICIOS EMPRESARIALES Y TURISTICOS (CSET) • TECNOLOGIA EN GESTION CONTABLE (123101)", sub_title_style))
    story.append(Paragraph("MATRIZ DE CONCEPTOS: TIPOS DE PRESUPUESTOS Y CEDULAS DEL PRESUPUESTO MAESTRO (GUIA No. 32)", ParagraphStyle('SubSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=gold, alignment=TA_CENTER)))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=2, spaceBefore=0))

    # FICHA TECNICA COMPACTA
    ficha = [
        [
            Paragraph("<b>Guia:</b> No. 32 Presupuesto", cell_txt),
            Paragraph("<b>Actividad:</b> Matriz Cedulas Presupuestales", cell_txt),
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

    # MATRIZ COMPLETA DE 11 CÉDULAS
    matriz_data = [
        [
            Paragraph("<b>Definicion / Tipo Presupuesto</b>", cell_hdr),
            Paragraph("<b>Definicion o Descripcion</b>", cell_hdr),
            Paragraph("<b>Caracteristicas / Requisitos</b>", cell_hdr),
            Paragraph("<b>Informacion Requerida Previamente para su Elaboracion</b>", cell_hdr),
            Paragraph("<b>Para que Sirve (Utilidad)</b>", cell_hdr)
        ],
        # 1. Ventas
        [
            Paragraph("<b>1. Presupuesto de Ventas</b>", cell_txt_bold),
            Paragraph("Punto de partida del presupuesto maestro. Proyecta cantidades fisicas a vender y los ingresos operacionales que se obtendran en cada periodo.", cell_txt),
            Paragraph("• Cuantifica unidades y precios unitarios.<br/>• Considera estacionalidad y canales.<br/>• Base de todo el plan operativo.", cell_txt),
            Paragraph("• Historico de ventas (3-5 anos).<br/>• Estudio de mercado y competencia.<br/>• Capacidad comercial y precios de venta.", cell_txt),
            Paragraph("Determina el nivel de ingresos que financiara toda la empresa y define que cantidad se debe fabricar o comprar.", cell_txt)
        ],
        # 2. Compras
        [
            Paragraph("<b>2. Presupuesto de Compras (Materia Prima / Mercancia)</b>", cell_txt_bold),
            Paragraph("Proyeccion de unidades e importes de insumos o mercancias a adquirir para sostener la produccion o ventas sin sufrir desabastecimiento.", cell_txt),
            Paragraph("• Expresado en medidas fisicas y dinero.<br/>• Respeta politicas de stock de seguridad.<br/>• Considera descuentos y fletes de entrega.", cell_txt),
            Paragraph("• Cedula de produccion / ventas.<br/>• Consumo unitario estandar por producto.<br/>• Inventario inicial y stock final deseado.<br/>• Lista de precios y plazos de proveedores.", cell_txt),
            Paragraph("Garantiza el abastecimiento oportuno sin generar sobrecostos de almacenamiento y programa los pagos a proveedores.", cell_txt)
        ],
        # 3. Mano de Obra
        [
            Paragraph("<b>3. Presupuesto de Mano de Obra Directa (MOD)</b>", cell_txt_bold),
            Paragraph("Calculo del costo del personal involucrado directamente en la elaboracion del bien o servicio prestado.", cell_txt),
            Paragraph("• Incluye salario, subsidio transporte, prestaciones (cesantias, prima, vacaciones) y aportes parafiscales y seguridad social (52.5%).", cell_txt),
            Paragraph("• Unidades a producir por periodo.<br/>• Tiempo estandar de fabricacion (horas/minutos unitarios).<br/>• Valor hora/minuto laboral con recargos.", cell_txt),
            Paragraph("Permite programar la contratacion, turnos laborales y controlar el costo de mano de obra por unidad fabricada.", cell_txt)
        ],
        # 4. CIF
        [
            Paragraph("<b>4. Presupuesto de Costos Indirectos Fabricacion (CIF)</b>", cell_txt_bold),
            Paragraph("Estimacion de recursos fabriles complementarios distintos a MPD y MOD (energia industrial, arriendo fabrica, mantenimiento, supervisores).", cell_txt),
            Paragraph("• Se clasifican en fijos y variables.<br/>• Requiere una base de asignacion tecnica (horas maquina, horas MOD, unidades).", cell_txt),
            Paragraph("• Capacidad instalada de la planta.<br/>• Contratos de arrendamiento y seguros.<br/>• Tarifas de servicios y depreciacion.", cell_txt),
            Paragraph("Permite calcular la <b>tasa predeterminada de CIF</b> para cargar con precision los costos indirectos a cada producto.", cell_txt)
        ],
        # 5. Producción
        [
            Paragraph("<b>5. Presupuesto de Produccion (Unidades)</b>", cell_txt_bold),
            Paragraph("Estimacion del volumen fisico de productos terminados a fabricar para cubrir la demanda y mantener el stock de inventario deseado.", cell_txt),
            Paragraph("• <b>Expresado unicamente en unidades fisicas</b>.<br/>• Formula: <i>Ventas + Inv. Final - Inv. Inicial</i>.<br/>• Respeta capacidad instalada maxima.", cell_txt),
            Paragraph("• Presupuesto de ventas en unidades.<br/>• Inventario inicial real disponible.<br/>• Politica de stock final de seguridad.", cell_txt),
            Paragraph("Evita roturas de stock (perdida de clientes) y sobreproduccion (costos innecesarios de bodegaje o vencimiento).", cell_txt)
        ],
        # 6. Costos Producción
        [
            Paragraph("<b>6. Presupuesto de Costos de Produccion</b>", cell_txt_bold),
            Paragraph("Consolidacion economica valorizada de los tres elementos del costo fabril: Materia Prima + Mano de Obra Directa + Costos Indirectos.", cell_txt),
            Paragraph("• Muestra el costo total del periodo y el costo unitario de fabricacion estandar.<br/>• Une las cedulas operativas de costo.", cell_txt),
            Paragraph("• Cedula de consumo de Materia Prima.<br/>• Cedula de Mano de Obra Directa.<br/>• Cedula de CIF totales aprobada.", cell_txt),
            Paragraph("Insumo indispensable para determinar el costo de ventas y proyectar el margen de utilidad bruta en el Estado de Resultados.", cell_txt)
        ],
        # 7. Gastos Administración
        [
            Paragraph("<b>7. Presupuesto Gastos Administrativos</b>", cell_txt_bold),
            Paragraph("Proyeccion de erogaciones para la gestion gerencial, contable, legal y directiva de la compania (oficina principal).", cell_txt),
            Paragraph("• Fijos en su mayoria.<br/>• Se ajustan anualmente con el IPC y salario minimo.<br/>• Independientes del volumen de ventas.", cell_txt),
            Paragraph("• Nomina y honorarios administrativos.<br/>• Arriendos corporativos y seguros.<br/>• Licencias software, papeleria y servicios.", cell_txt),
            Paragraph("Establece topes maximos de gasto a las areas de soporte y evita el despilfarro burocratico de recursos.", cell_txt)
        ],
        # 8. Gastos Ventas
        [
            Paragraph("<b>8. Presupuesto Gastos de Ventas</b>", cell_txt_bold),
            Paragraph("Estimacion de recursos para promocionar, comercializar, distribuir y colocar los productos en manos del cliente final.", cell_txt),
            Paragraph("• Componentes variables (comisiones comerciales, fletes) y fijos (sueldos comerciales base, publicidad institucional).", cell_txt),
            Paragraph("• Presupuesto de ventas proyectado.<br/>• Tabla de comisiones y bonificaciones.<br/>• Plan de marketing, pauta y transporte.", cell_txt),
            Paragraph("Cuantifica el esfuerzo financiero necesario para alcanzar la meta de ventas trazada en el plan estrategico.", cell_txt)
        ],
        # 9. Inversión
        [
            Paragraph("<b>9. Presupuesto de Inversion (CAPEX)</b>", cell_txt_bold),
            Paragraph("Planificacion de compra de activos fijos no corrientes (terrenos, edificaciones, maquinaria, tecnologia, flota vehicular).", cell_txt),
            Paragraph("• Horizonte de mediano y largo plazo.<br/>• Requiere evaluacion financiera (VPN, TIR, periodo de recuperacion del capital).", cell_txt),
            Paragraph("• Planes de expansion y crecimiento.<br/>• Desgaste y obsolescencia de equipos.<br/>• Opciones de credito bancario o leasing.", cell_txt),
            Paragraph("Garantiza la modernizacion tecnologica y la expansion de la capacidad instalada para crecer en el mercado.", cell_txt)
        ],
        # 10. Caja
        [
            Paragraph("<b>10. Presupuesto de Caja (Flujo de Tesoreria)</b>", cell_txt_bold),
            Paragraph("Cronograma proyectado que detalla las entradas reales de dinero en efectivo y salidas efectivas de liquidez periodo a periodo.", cell_txt),
            Paragraph("• Rige bajo principio de <b>caja</b> (efectivo cobrado/pagado), no por causacion.<br/>• Controla saldo minimo de seguridad.", cell_txt),
            Paragraph("• Politica de cobro (% contado vs credito).<br/>• Plazos de pago a proveedores y nomina.<br/>• Fechas tributarias DIAN (IVA, Renta).", cell_txt),
            Paragraph("Previene la quiebra por falta de efectivo inmediato; programa con anticipacion prestamos o inversiones de excedentes.", cell_txt)
        ],
        # 11. Financieros
        [
            Paragraph("<b>11. Presupuestos Financieros (Estados Proyectados)</b>", cell_txt_bold),
            Paragraph("Consolidacion final del presupuesto maestro: emision proyectada del Estado de Resultados, Situacion Financiera y Flujo de Efectivo NIIF.", cell_txt),
            Paragraph("• Cumple estructura estricta NIIF (NIC 1 y NIC 7).<br/>• Cierra cuantitativamente el plan maestro.<br/>• Permite calcular ROE, ROA y endeudamiento.", cell_txt),
            Paragraph("• Todas las cedulas operativas y de gastos.<br/>• Cedula de inversion y flujo de caja.<br/>• Tasas de impuestos y reservas legales.", cell_txt),
            Paragraph("Muestra la situacion patrimonial y rentabilidad futura a socios y bancos para validar la viabilidad del negocio.", cell_txt)
        ]
    ]

    t_matriz = Table(matriz_data, colWidths=[90, 116, 116, 116, 118])
    t_matriz.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 1.6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
        ('LEFTPADDING', (0,0), (-1,-1), 2.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,1), (0,-1), colors.HexColor("#EFF6FF")),
    ]))
    story.append(t_matriz)
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
    print("Matriz PDF generated successfully:", pdf_path)

if __name__ == '__main__':
    generate_matriz_pdf()

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
        self.drawString(28, 764, "SENA CSET BUCARAMANGA | GUIA No. 32 | PRESUPUESTO FINANCIERO Y FRISO MAESTRO | GINA VILLAMIZAR")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(28, 759, 584, 759)
            
        # Footer
        page_text = f"Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(584, 16, page_text)
        self.drawString(28, 16, "TECNOLOGIA EN GESTION CONTABLE Y FINANCIERA • CUADRO SINOPTICO 3.3.8 Y COMPONENTES DEL FRISO 3.3.7")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(28, 23, 584, 23)
        self.restoreState()

def generate_presupuesto_financiero_pdf():
    pdf_path = "/Users/ginavillamizar/Downloads/CONTABILIDAD/GUIA_32_PRESUPUESTO_FINANCIERO_Y_FRISO_GINA_VILLAMIZAR.pdf"
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
    cell_txt = ParagraphStyle('CellTxt', parent=styles['Normal'], fontName='Helvetica', fontSize=5.6, leading=7.2, textColor=slate_dark)
    cell_txt_bold = ParagraphStyle('CellTxtBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=5.6, leading=7.2, textColor=primary)

    body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=5.8, leading=7.5, textColor=slate_dark, alignment=TA_JUSTIFY)

    story = []

    # ENCABEZADO INSTITUCIONAL
    story.append(Paragraph("SERVICIO NACIONAL DE APRENDIZAJE - SENA • REGIONAL SANTANDER", title_style))
    story.append(Paragraph("CENTRO DE SERVICIOS EMPRESARIALES Y TURISTICOS (CSET) • GESTION CONTABLE (123101)", sub_title_style))
    story.append(Paragraph("ACTIVIDADES 3.3.8 Y 3.3.7: EL PRESUPUESTO FINANCIERO (CUADRO SINOPTICO) Y FRISO DEL PRESUPUESTO MAESTRO", ParagraphStyle('SubSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=gold, alignment=TA_CENTER)))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=2, spaceBefore=0))

    # FICHA TECNICA COMPACTA
    ficha = [
        [
            Paragraph("<b>Guia:</b> No. 32 Presupuesto", cell_txt),
            Paragraph("<b>Actividades:</b> 3.3.8 y 3.3.7 (Pag. 10-11)", cell_txt),
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
    # PARTE 1: TEORIA Y METODOLOGIA DEL PRESUPUESTO FINANCIERO (3.3.8)
    # =========================================================================
    story.append(Paragraph("<b>1. METODOLOGIA, ESTRUCTURA Y UTILIDAD DEL PRESUPUESTO FINANCIERO (ACTIVIDAD 3.3.8):</b>", sec_hdr))
    metodologia_text = (
        "• <b>Metodologia de Aplicacion:</b> Exige culminar primero todo el <i>Presupuesto Operativo</i> (Ventas, Produccion, Compras MP, Nomina MOD, CIF y Gastos). "
        "A partir de estos se proyecta cronologicamente el flujo monetario real en el <i>Presupuesto de Caja</i> (Tesorería), luego se liquida el <i>Estado de Resultados Integral (ERI)</i> "
        "para determinar la ganancia neta y la carga fiscal (Impuesto de Renta 35% y Reserva Legal 10%), y finalmente se ensambla el <i>Estado de Situacion Financiera (ESF)</i> "
        "para verificar la ecuacion contable: <i>Activo = Pasivo + Patrimonio</i>.<br/>"
        "• <b>Utilidad Estrategica:</b> Evalua anticipadamente la <b>rentabilidad</b> (ROE, ROA, margen neto) y la <b>solvencia</b> (liquidez, KTN, cobertura de deuda); sirve de sustento tecnico "
        "ante entidades financieras para tramitar creditos y alerta a la Gerencia sobre riesgos de iliquidez o disolucion antes de que ocurran en la realidad."
    )
    story.append(Paragraph(metodologia_text, body))
    story.append(Spacer(1, 2))

    # =========================================================================
    # PARTE 2: CUADRO SINOPTICO DEL PRESUPUESTO FINANCIERO
    # =========================================================================
    story.append(Paragraph("<b>2. CUADRO SINOPTICO DEL PRESUPUESTO FINANCIERO PROYECTADO (ESTRUCTURA NIIF):</b>", sec_hdr))
    
    sinop_box = [
        [
            Paragraph("<b>COMPONENTE / ESTADO FINANCIERO</b>", cell_hdr),
            Paragraph("<b>ESTRUCTURA TECNICA FORMULADA (NIIF)</b>", cell_hdr),
            Paragraph("<b>UTILIDAD Y TOMA DE DECISIONES</b>", cell_hdr)
        ],
        [
            Paragraph("<b>A. Estado de Resultados Integral (ERI) Proyectado</b>", cell_txt_bold),
            Paragraph("<b>Ventas Netas</b> (-) Costo de Ventas (=) <b>Utilidad Bruta</b><br/>"
                      "(-) Gastos Operacionales de Administracion y Ventas<br/>"
                      "(=) <b>Utilidad Operativa (UAII)</b> (-) Gastos Financieros (Intereses)<br/>"
                      "(=) <b>Utilidad Antes de Impuestos (UAI)</b> (-) Provision Renta (35%)<br/>"
                      "(=) <b>RESULTADO NETO DEL EJERCICIO</b> (-) Reserva Legal (10%)", cell_txt),
            Paragraph("• Mide la eficiencia economica y rentabilidad proyectada.<br/>"
                      "• Determina el valor a pagar por impuestos a la DIAN.<br/>"
                      "• Define la capacidad de generar utilidades o absorber perdidas.", cell_txt)
        ],
        [
            Paragraph("<b>B. Estado de Flujos de Efectivo Proyectado (NIC 7 / Caja)</b>", cell_txt_bold),
            Paragraph("<b>Saldo Inicial en Caja y Bancos</b><br/>"
                      "(+) Cobranza de Cartera a Clientes y Ventas de Contado<br/>"
                      "(-) Pagos Operativos: Proveedores MP, Nomina MOD, CIF, Dian<br/>"
                      "(=) <b>Flujo Neto de Actividades de Operacion</b><br/>"
                      "(-) Desembolsos de Inversion (CAPEX Maquinaria y Equipos)<br/>"
                      "(+) Creditos Bancarios / Aportes (-) Pago de Dividendos<br/>"
                      "(=) <b>SALDO FINAL DE EFECTIVO DISPONIBLE</b>", cell_txt),
            Paragraph("• Rige bajo estricto <b>principio de caja</b> (dinero disponible).<br/>"
                      "• Previene la quiebra por iliquidez o cesacion de pagos.<br/>"
                      "• Determina excedentes para invertir o necesidad de sobregiro.<br/>"
                      "• Alimenta directamente la cuenta 1105/1110 en el Balance.", cell_txt)
        ],
        [
            Paragraph("<b>C. Estado de Situacion Financiera (ESF / Balance Proyectado)</b>", cell_txt_bold),
            Paragraph("• <b>ACTIVO:</b> Efectivo Final + Cartera Clientes + Inventarios Finales (PT y MP) + Propiedades, Planta y Equipos Netos.<br/>"
                      "• <b>PASIVO:</b> Proveedores + Obligaciones Bancarias + Impuestos por Pagar (Renta e IVA) + Pasivos Laborales.<br/>"
                      "• <b>PATRIMONIO:</b> Capital Social + Reservas + Utilidades Acumuladas.<br/>"
                      "<b>Ecuacion Contable: ACTIVO = PASIVO + PATRIMONIO</b>", cell_txt),
            Paragraph("• Es la 'fotografia' de la solidez patrimonial futura.<br/>"
                      "• Evalua la cobertura de deudas a corto y largo plazo.<br/>"
                      "• Valida la hipotesis de <i>Negocio en Marcha</i> (NIC 1).<br/>"
                      "• Exigido por bancos e inversionistas para evaluacion de riesgo.", cell_txt)
        ]
    ]
    t_sinop = Table(sinop_box, colWidths=[130, 266, 160])
    t_sinop.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.35, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_sinop)
    story.append(Spacer(1, 2))

    # =========================================================================
    # PARTE 3: EL FRISO DEL PRESUPUESTO MAESTRO (5 CARAS - ACTIVIDAD 3.3.7)
    # =========================================================================
    story.append(Paragraph("<b>3. ESTRUCTURA Y CONTENIDO DEL FRISO DEL PRESUPUESTO MAESTRO (ACTIVIDAD 3.3.7):</b>", sec_hdr))
    story.append(Paragraph("<i>Diseno didactico en 5 caras plegables que sintetiza la consolidacion, medicion de indicadores, control de variaciones y plan de accion:</i>", body))
    story.append(Spacer(1, 1))

    c1 = "<b>CARA 1: DEFINICION Y PROPOSITO</b><br/>" \
         "• <b>Definicion:</b> Documento integral que consolida los planes operativos y financieros de todas las areas de la empresa en un horizonte anual.<br/>" \
         "• <b>Proposito:</b> Servir de brujula directiva, coordinar compras y produccion, asignar recursos de forma austera y anticipar el logro de metas."

    c2 = "<b>CARA 2: COMPONENTES DEL INFORME</b><br/>" \
         "• <b>Presupuesto Operativo:</b> Ventas, Produccion en unidades, Compras MP, MOD, CIF, Gastos de Administracion y Ventas.<br/>" \
         "• <b>Presupuesto Financiero:</b> Inversiones (CAPEX), Presupuesto de Tesoreria (Caja) y Estados Financieros Proyectados (ERI, ESF, Flujo Efectivo)."

    c3 = "<b>CARA 3: INDICADORES CLAVE</b><br/>" \
         "• <b>Razon Corriente:</b> Act. Corr / Pas. Corr &ge; 1,5x.<br/>" \
         "• <b>Prueba Acida:</b> (Act. Corr - Inv) / Pas. Corr &ge; 1,0x.<br/>" \
         "• <b>Endeudamiento:</b> Pasivo / Activo &le; 50%.<br/>" \
         "• <b>Margen Neto:</b> Ut. Neta / Ventas &times; 100.<br/>" \
         "• <b>ROE (Retorno Socios):</b> Ut. Neta / Patrimonio."

    c4 = "<b>CARA 4: CONTROL Y VARIACIONES</b><br/>" \
         "• <b>Formula:</b> <i>Variacion = Real - Presupuesto</i>.<br/>" \
         "• <b>Favorable (F):</b> Mas ventas de lo planeado o menores costos/gastos operacionales.<br/>" \
         "• <b>Desfavorable (D):</b> Caida en facturacion o sobrecostos en materia prima y mano de obra.<br/>" \
         "• Monitoreo mensual de desviaciones."

    c5 = "<b>CARA 5: PLAN DE ACCION</b><br/>" \
         "• <b>Ventas bajas:</b> Ajuste por costeo directo, intensificar promociones y nuevos canales.<br/>" \
         "• <b>Sobrecosto MP:</b> Negociar compras por volumen, buscar sustitutos y frenar mermas.<br/>" \
         "• <b>Deficit de caja:</b> Descuentos por pronto pago a clientes y renegociar plazos de proveedores."

    friso_table = [
        [
            Paragraph(c1, cell_txt),
            Paragraph(c2, cell_txt),
            Paragraph(c3, cell_txt),
            Paragraph(c4, cell_txt),
            Paragraph(c5, cell_txt)
        ]
    ]
    t_friso = Table(friso_table, colWidths=[111, 111, 111, 111, 112])
    t_friso.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#FEF3C7")),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor("#ECFDF5")),
        ('BACKGROUND', (3,0), (3,0), colors.HexColor("#FEF2F2")),
        ('BACKGROUND', (4,0), (4,0), colors.HexColor("#F5F3FF")),
        ('BOX', (0,0), (0,0), 0.5, colors.HexColor("#93C5FD")),
        ('BOX', (1,0), (1,0), 0.5, colors.HexColor("#FCD34D")),
        ('BOX', (2,0), (2,0), 0.5, colors.HexColor("#6EE7B7")),
        ('BOX', (3,0), (3,0), 0.5, colors.HexColor("#FCA5A5")),
        ('BOX', (4,0), (4,0), 0.5, colors.HexColor("#C4B5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 2.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_friso)
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
    print("Presupuesto Financiero y Friso PDF generated successfully:", pdf_path)

if __name__ == '__main__':
    generate_presupuesto_financiero_pdf()

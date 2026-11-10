import os
import re

base_dir = "/Users/ginavillamizar/Downloads/CONTABILIDAD"
index_path = os.path.join(base_dir, "index.html")
styles_path = os.path.join(base_dir, "styles.css")
app_path = os.path.join(base_dir, "app.js")

# 1. Update index.html
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Add Chart.js CDN before styles.css if not present
if "chart.umd.min.js" not in html:
    html = html.replace(
        '<link rel="stylesheet" href="styles.css',
        '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>\n  <link rel="stylesheet" href="styles.css'
    )

# Add the button in #efSubTabs if not present
if 'data-eftab="ANALISIS"' not in html:
    html = html.replace(
        '<button class="filter-chip" data-eftab="FLUJO" onclick="selectEfTab(\'FLUJO\')">💵 Flujo de Efectivo</button>',
        '<button class="filter-chip" data-eftab="FLUJO" onclick="selectEfTab(\'FLUJO\')">💵 Flujo de Efectivo</button>\n              <button class="filter-chip" data-eftab="ANALISIS" onclick="selectEfTab(\'ANALISIS\')">📊 Análisis Financiero & Gráficas</button>'
    )

# Bump version to force cache refresh
html = re.sub(r'href="styles\.css\?v=[^"]+"', 'href="styles.css?v=20261110_18"', html)
html = re.sub(r'src="app\.js\?v=[^"]+"', 'src="app.js?v=20261110_18"', html)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated index.html with Chart.js and tab button.")

# 2. Update styles.css
with open(styles_path, "r", encoding="utf-8") as f:
    css = f.read()

analysis_css = """
/* ===============================================================
   ESTILOS PARA ANÁLISIS FINANCIERO Y GRÁFICAS INTERACTIVAS
   =============================================================== */
.analysis-grid-2col {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.chart-card-box {
  background: var(--bg-surface);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-sm);
  padding: 18px;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
}

.chart-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  padding-bottom: 8px;
  border-bottom: 1.5px solid var(--border-light);
}

.chart-card-title {
  font-size: 0.88rem;
  font-weight: 800;
  color: var(--brand-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

[data-theme="dark"] .chart-card-title {
  color: var(--brand-gold);
}

.chart-canvas-container {
  position: relative;
  width: 100%;
  height: 280px;
}

.ratio-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 8px;
  border-radius: 99px;
  font-size: 0.73rem;
  font-weight: 800;
}

.ratio-badge-pill.status-good {
  background: rgba(16, 185, 129, 0.15);
  color: #059669;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.ratio-badge-pill.status-warn {
  background: rgba(245, 158, 11, 0.15);
  color: #D97706;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.indicator-traffic-light {
  display: inline-block;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  margin-right: 4px;
}

.indicator-traffic-light.green { background: #10B981; box-shadow: 0 0 6px #10B981; }
.indicator-traffic-light.yellow { background: #F59E0B; box-shadow: 0 0 6px #F59E0B; }
.indicator-traffic-light.blue { background: #3B82F6; box-shadow: 0 0 6px #3B82F6; }
"""

if "ESTILOS PARA ANÁLISIS FINANCIERO Y GRÁFICAS INTERACTIVAS" not in css:
    css += "\n" + analysis_css
    with open(styles_path, "w", encoding="utf-8") as f:
        f.write(css)
    print("Updated styles.css with chart box styling.")

# 3. Update app.js
with open(app_path, "r", encoding="utf-8") as f:
    js = f.read()

analysis_js = r'''
// ============================================================================
// 7.B. MÓDULO DE ANÁLISIS FINANCIERO Y GRÁFICAS INTERACTIVAS NIIF
// ============================================================================
let ACTIVE_CHARTS_INSTANCES = [];

function renderFinancialAnalysisDashboardHtml(period) {
  const emp = DB?.empresa || {};
  const isAbril = period === "ABRIL";

  return `
    <div class="niif-statement-paper">
      <!-- Encabezado Corporativo Oficial -->
      <div class="niif-header-box">
        <div class="niif-company-title">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
        <div class="niif-company-sub">NIT: ${emp.nit || "901.765.438-3"} • ${emp.regimen || "RRI — Agente Autorretenedor de Renta"}</div>
        <div class="niif-statement-badge">
          <div class="niif-statement-name">📊 INFORME EJECUTIVO DE ANÁLISIS FINANCIERO & GRÁFICAS INTERACTIVAS</div>
          <span class="niif-period-tag">Período Comparativo: MARZO 2026 vs ABRIL 2026</span>
          <span style="font-size:0.7rem; color:#94A3B8; display:block; margin-top:3px;">
            Diagnóstico Financiero Integral NIIF para las PYMES • Indicadores de Liquidez, Endeudamiento y Rentabilidad
          </span>
        </div>
      </div>

      <!-- Tarjetas KPI de Alto Impacto -->
      <div class="niif-kpi-summary-strip" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:14px; margin-bottom:24px;">
        <div class="niif-kpi-pill" style="border-left:4px solid #10B981;">
          <span class="kpi-title">Razón Corriente (Liquidez)</span>
          <span class="kpi-amount" style="color:#059669;">2,25 x</span>
          <span style="font-size:0.72rem; color:var(--text-muted); margin-top:3px;">Marzo: 1,92x (Mejora: +17.2%) • Óptimo</span>
        </div>
        <div class="niif-kpi-pill" style="border-left:4px solid #3B82F6;">
          <span class="kpi-title">Endeudamiento Total</span>
          <span class="kpi-amount" style="color:#2563EB;">27,37 %</span>
          <span style="font-size:0.72rem; color:var(--text-muted); margin-top:3px;">Marzo: 32,68% (Desendeudamiento: -5.31%)</span>
        </div>
        <div class="niif-kpi-pill" style="border-left:4px solid #D4AF37;">
          <span class="kpi-title">Margen Bruto Comercial</span>
          <span class="kpi-amount" style="color:var(--brand-gold);">59,69 %</span>
          <span style="font-size:0.72rem; color:var(--text-muted); margin-top:3px;">Utilidad Bruta $4.868.500 / Ventas $8.156.500</span>
        </div>
        <div class="niif-kpi-pill" style="border-left:4px solid #8B5CF6;">
          <span class="kpi-title">Capital de Trabajo Neto</span>
          <span class="kpi-amount" style="color:#7C3AED;">$ 67.415.103</span>
          <span style="font-size:0.72rem; color:var(--text-muted); margin-top:3px;">Fondo de maniobra operativo disponible</span>
        </div>
      </div>

      <!-- SECCIÓN 1: PANEL DE GRÁFICAS INTERACTIVAS -->
      <div style="background:var(--brand-primary); color:#FFFFFF; padding:8px 14px; border-radius:4px 4px 0 0; font-weight:800; font-size:0.84rem; letter-spacing:0.4px; margin-bottom:14px;">
        📈 PANEL VISUAL DE ESTRUCTURA Y EVOLUCIÓN FINANCIERA
      </div>

      <div class="analysis-grid-2col">
        <!-- Gráfica 1: Estructura Financiera Comparativa -->
        <div class="chart-card-box">
          <div class="chart-card-header">
            <span class="chart-card-title">🏛️ Estructura del Balance (Marzo vs Abril)</span>
            <span class="ratio-badge-pill status-good"><span class="indicator-traffic-light green"></span>Solvente</span>
          </div>
          <div class="chart-canvas-container">
            <canvas id="chartEstructuraFinanciera"></canvas>
          </div>
          <div style="font-size:0.72rem; color:var(--text-secondary); margin-top:8px; line-height:1.4;">
            El Activo Total se desapalancó un 10.25% ($369.1M a $331.2M), reduciendo pasivos bancarios sin comprometer la base de capital.
          </div>
        </div>

        <!-- Gráfica 2: Composición Fuentes de Financiación -->
        <div class="chart-card-box">
          <div class="chart-card-header">
            <span class="chart-card-title">🥧 Fuentes de Financiación (Pasivo vs Patrimonio)</span>
            <span class="ratio-badge-pill status-good"><span class="indicator-traffic-light green"></span>72.6% Patrimonio</span>
          </div>
          <div class="chart-canvas-container">
            <canvas id="chartComposicionFinanciacion"></canvas>
          </div>
          <div style="font-size:0.72rem; color:var(--text-secondary); margin-top:8px; line-height:1.4;">
            Alta autonomía financiera: el 72.63% de los activos pertenece a los socios y solo el 27.37% está comprometido con terceros.
          </div>
        </div>

        <!-- Gráfica 3: Cascada Estado de Resultados -->
        <div class="chart-card-box">
          <div class="chart-card-header">
            <span class="chart-card-title">📉 Cascada del Estado de Resultados (Abril 2026)</span>
            <span class="ratio-badge-pill status-warn"><span class="indicator-traffic-light yellow"></span>Absorción Fija</span>
          </div>
          <div class="chart-canvas-container">
            <canvas id="chartCascadaResultados"></canvas>
          </div>
          <div style="font-size:0.72rem; color:var(--text-secondary); margin-top:8px; line-height:1.4;">
            Margen bruto robusto ($4.87M, 59.7%). La pérdida ($7.89M) obedece a gastos de nómina y adecuación propios del arranque.
          </div>
        </div>

        <!-- Gráfica 4: Flujo de Efectivo por Actividades -->
        <div class="chart-card-box">
          <div class="chart-card-header">
            <span class="chart-card-title">💵 Flujo de Fondos por Tipo de Actividad</span>
            <span class="ratio-badge-pill status-good"><span class="indicator-traffic-light blue"></span>Caja: $25.4M</span>
          </div>
          <div class="chart-canvas-container">
            <canvas id="chartFlujoEfectivo"></canvas>
          </div>
          <div style="font-size:0.72rem; color:var(--text-secondary); margin-top:8px; line-height:1.4;">
            El flujo reflejó el pago neto de obligaciones bancarias ($30.2M) e inventarios, cerrando con $25.430.816 en disponible.
          </div>
        </div>
      </div>

      <!-- SECCIÓN 2: MATRIZ DE INDICADORES FINANCIEROS NIIF -->
      <div style="background:var(--brand-primary); color:#FFFFFF; padding:8px 14px; border-radius:4px 4px 0 0; font-weight:800; font-size:0.84rem; letter-spacing:0.4px; margin-top:10px;">
        📋 MATRIZ DE RAZONES E INDICADORES FINANCIEROS (NIIF PARA LAS PYMES)
      </div>
      <div class="table-wrap" style="margin-bottom:24px;">
        <table class="niif-table">
          <thead>
            <tr>
              <th style="width:160px;">Grupo de Indicador</th>
              <th>Nombre de la Razón</th>
              <th style="width:160px;">Fórmula NIIF</th>
              <th class="num-col" style="width:110px;">Marzo 2026</th>
              <th class="num-col" style="width:110px;">Abril 2026</th>
              <th class="num-col" style="width:90px;">Variación</th>
              <th style="width:140px; text-align:center;">Diagnóstico</th>
            </tr>
          </thead>
          <tbody>
            <tr class="niif-row-clase">
              <td colspan="7">1. INDICADORES DE LIQUIDEZ Y CAPITAL DE TRABAJO</td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Liquidez</strong></td>
              <td><strong>Razón Corriente</strong></td>
              <td>Activo Cte / Pasivo Cte</td>
              <td class="num-col">1,92 veces</td>
              <td class="num-col" style="color:#059669; font-weight:800;">2,25 veces</td>
              <td class="num-col">+ 0,33 x</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Excelente</span></td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Liquidez</strong></td>
              <td><strong>Prueba Ácida</strong></td>
              <td>(Activo Cte - Inv) / Pasivo Cte</td>
              <td class="num-col">1,56 veces</td>
              <td class="num-col" style="color:#059669; font-weight:800;">1,62 veces</td>
              <td class="num-col">+ 0,06 x</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Alta Liquidez</span></td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Liquidez</strong></td>
              <td><strong>Capital de Trabajo Neto</strong></td>
              <td>Activo Cte - Pasivo Cte</td>
              <td class="num-col">$ 75.489.713</td>
              <td class="num-col" style="font-weight:800;">$ 67.415.103</td>
              <td class="num-col text-danger">- 10,70 %</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Colchón Sólido</span></td>
            </tr>

            <tr class="niif-row-clase">
              <td colspan="7">2. INDICADORES DE ENDEUDAMIENTO Y SOLVENCIA</td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Endeudamiento</strong></td>
              <td><strong>Nivel de Endeudamiento</strong></td>
              <td>Pasivo Total / Activo Total</td>
              <td class="num-col">32,68 %</td>
              <td class="num-col" style="color:#059669; font-weight:800;">27,37 %</td>
              <td class="num-col" style="color:#059669;">- 5,31 %</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Bajo Riesgo</span></td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Endeudamiento</strong></td>
              <td><strong>Autonomía Financiera</strong></td>
              <td>Patrimonio / Activo Total</td>
              <td class="num-col">67,32 %</td>
              <td class="num-col" style="color:#059669; font-weight:800;">72,63 %</td>
              <td class="num-col" style="color:#059669;">+ 5,31 %</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Muy Favorable</span></td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Endeudamiento</strong></td>
              <td><strong>Apalancamiento (Leverage)</strong></td>
              <td>Pasivo Total / Patrimonio</td>
              <td class="num-col">0,49 veces</td>
              <td class="num-col" style="font-weight:800;">0,38 veces</td>
              <td class="num-col">- 0,11 x</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Desapalancada</span></td>
            </tr>

            <tr class="niif-row-clase">
              <td colspan="7">3. INDICADORES DE RENTABILIDAD Y RENDIMIENTO</td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Rentabilidad</strong></td>
              <td><strong>Margen Bruto</strong></td>
              <td>Utilidad Bruta / Ventas</td>
              <td class="num-col">0,00 %</td>
              <td class="num-col" style="color:var(--brand-gold); font-weight:900;">59,69 %</td>
              <td class="num-col" style="color:#059669;">+ 59,69 %</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Excelente</span></td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Rentabilidad</strong></td>
              <td><strong>Margen Neto</strong></td>
              <td>Resultado Neto / Ventas</td>
              <td class="num-col">N/A</td>
              <td class="num-col text-danger" style="font-weight:800;">- 96,70 %</td>
              <td class="num-col">N/A</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-warn">🟡 Etapa Puesta en Marcha</span></td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Rentabilidad</strong></td>
              <td><strong>Rendimiento del Patrimonio (ROE)</strong></td>
              <td>Resultado / Patrimonio</td>
              <td class="num-col text-danger">- 6,90 %</td>
              <td class="num-col text-danger" style="font-weight:800;">- 3,28 %</td>
              <td class="num-col" style="color:#059669;">+ 3,62 %</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Redujo Pérdida 52%</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- SECCIÓN 3: DIAGNÓSTICO FINANCIERO Y CONCLUSIONES PARA GERENCIA -->
      <div style="background:var(--bg-subtle); border-left:4px solid var(--brand-gold); border-radius:6px; padding:18px 20px; margin-bottom:24px; line-height:1.6; font-size:0.83rem; color:var(--text-main);">
        <div style="font-size:0.95rem; font-weight:900; color:var(--brand-primary); margin-bottom:10px; display:flex; align-items:center; gap:8px;">
          <span>🎯 CONCLUSIONES Y RECOMENDACIONES ESTRATÉGICAS (GERENCIA Y CONTROL FISCAL):</span>
        </div>
        <ul style="margin:0; padding-left:18px;">
          <li><strong>1. Calidad y Fortaleza de la Liquidez:</strong> La entidad pasó de \$ 1,92 a \$ 2,25 de activo corriente por cada peso de pasivo corriente. Aún deduciendo la totalidad de inventarios de mercancías, la prueba ácida es de 1,62x, lo que certifica cero riesgo de cesación de pagos en el corto plazo.</li>
          <li><strong>2. Estructura de Capital y Desendeudamiento:</strong> Durante el mes de abril se destinaron \$ 30.222.643 a amortizar obligaciones bancarias, reduciendo el nivel de endeudamiento del 32,68% al 27,37%. El 72,63% de la empresa está financiada con patrimonio propio.</li>
          <li><strong>3. Potencial del Modelo de Negocio (Margen Unitario 59.7%):</strong> Por cada \$ 100 vendidos en estufas y calentadores, la empresa retiene \$ 59,69 tras deducir el costo comercial de adquisición, lo que demuestra alta competitividad de precios.</li>
          <li><strong>4. Plan de Acción y Punto de Equilibrio:</strong> Para revertir la pérdida neta mensual (-\$ 7.887.158), generada por los costos de estructura fija (nómina de \$ 10.4M y amortizaciones), se requiere un volumen mínimo de ventas mensuales de <strong>\$ 21.400.000</strong>. Se recomienda dinamizar el canal comercial mayorista aprovechando el inventario actual de \$ 33.8M.</li>
        </ul>
      </div>

      ${renderOfficialSignaturesBlock()}
    </div>
  `;
}

function initFinancialAnalysisCharts(period) {
  // Destruir instancias previas para evitar memory leaks o solapamientos
  ACTIVE_CHARTS_INSTANCES.forEach(ch => {
    try { ch.destroy(); } catch (e) {}
  });
  ACTIVE_CHARTS_INSTANCES = [];

  if (typeof Chart === "undefined") {
    console.warn("Chart.js no está disponible aún.");
    return;
  }

  // Paleta de colores oficial
  const gold = "#D4AF37";
  const navy = "#0B192C";
  const green = "#10B981";
  const red = "#EF4444";
  const blue = "#3B82F6";
  const slate = "#64748B";

  // 1. Gráfica de Estructura Financiera Comparativa (Marzo vs Abril)
  const ctx1 = document.getElementById("chartEstructuraFinanciera")?.getContext("2d");
  if (ctx1) {
    const ch1 = new Chart(ctx1, {
      type: "bar",
      data: {
        labels: ["Activo Total", "Pasivo Total", "Patrimonio Neto"],
        datasets: [
          {
            label: "Marzo 2026",
            data: [369.07, 120.62, 248.45],
            backgroundColor: "rgba(100, 116, 139, 0.75)",
            borderColor: "#64748B",
            borderWidth: 1.5,
            borderRadius: 4
          },
          {
            label: "Abril 2026",
            data: [331.23, 90.67, 240.56],
            backgroundColor: "rgba(212, 175, 55, 0.85)",
            borderColor: "#D4AF37",
            borderWidth: 1.5,
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top", labels: { boxWidth: 12, font: { size: 11, weight: "bold" } } },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.dataset.label}: $ ${ctx.parsed.y.toFixed(2)} Millones COP`
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { callback: (v) => `$${v}M` }
          }
        }
      }
    });
    ACTIVE_CHARTS_INSTANCES.push(ch1);
  }

  // 2. Gráfica de Fuentes de Financiación (Abril 2026)
  const ctx2 = document.getElementById("chartComposicionFinanciacion")?.getContext("2d");
  if (ctx2) {
    const ch2 = new Chart(ctx2, {
      type: "doughnut",
      data: {
        labels: ["Pasivo Corriente (16.3%)", "Pasivo No Corriente (11.1%)", "Patrimonio Neto Socios (72.6%)"],
        datasets: [{
          data: [53.93, 36.74, 240.56],
          backgroundColor: ["#EF4444", "#F59E0B", "#10B981"],
          borderWidth: 2,
          borderColor: "#FFFFFF"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "60%",
        plugins: {
          legend: { position: "bottom", labels: { boxWidth: 10, font: { size: 10 } } },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.label}: $ ${ctx.parsed.toFixed(2)}M COP`
            }
          }
        }
      }
    });
    ACTIVE_CHARTS_INSTANCES.push(ch2);
  }

  // 3. Cascada del Estado de Resultados (Abril 2026)
  const ctx3 = document.getElementById("chartCascadaResultados")?.getContext("2d");
  if (ctx3) {
    const ch3 = new Chart(ctx3, {
      type: "bar",
      data: {
        labels: ["Ingresos Ventas", "Costo Ventas", "Utilidad Bruta", "Gastos Operación", "Resultado Neto"],
        datasets: [{
          label: "Valor COP (Millones)",
          data: [8.16, -3.29, 4.87, -12.76, -7.89],
          backgroundColor: [
            "rgba(16, 185, 129, 0.8)",
            "rgba(239, 68, 68, 0.8)",
            "rgba(212, 175, 55, 0.85)",
            "rgba(239, 68, 68, 0.8)",
            "rgba(220, 38, 38, 0.9)"
          ],
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => ` $ ${ctx.parsed.y.toFixed(2)} Millones COP`
            }
          }
        },
        scales: {
          y: {
            ticks: { callback: (v) => `$${v}M` }
          }
        }
      }
    });
    ACTIVE_CHARTS_INSTANCES.push(ch3);
  }

  // 4. Flujo de Efectivo por Actividades
  const ctx4 = document.getElementById("chartFlujoEfectivo")?.getContext("2d");
  if (ctx4) {
    const ch4 = new Chart(ctx4, {
      type: "bar",
      data: {
        labels: ["Inversión", "Operación", "Financiación", "Partidas no Caja", "Variación Neta"],
        datasets: [{
          label: "Efecto en Efectivo ($ Millones)",
          data: [-0.57, -4.25, -30.22, -33.03, -68.07],
          backgroundColor: [
            "rgba(59, 130, 246, 0.8)",
            "rgba(245, 158, 11, 0.8)",
            "rgba(239, 68, 68, 0.8)",
            "rgba(100, 116, 139, 0.8)",
            "rgba(185, 28, 28, 0.9)"
          ],
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => ` $ ${ctx.parsed.y.toFixed(2)} Millones COP`
            }
          }
        },
        scales: {
          y: {
            ticks: { callback: (v) => `$${v}M` }
          }
        }
      }
    });
    ACTIVE_CHARTS_INSTANCES.push(ch4);
  }
}
'''

# Insert analysis_js before renderEstadosFinancieros
ef_pos = js.find("function renderEstadosFinancieros()")
if ef_pos != -1 and "renderFinancialAnalysisDashboardHtml" not in js:
    js = js[:ef_pos] + analysis_js + "\n\n" + js[ef_pos:]

# Hook tab in renderEstadosFinancieros
target_hook = '  if (ACTIVE_EF_TAB === "FLUJO") {'
new_hook = '''  if (ACTIVE_EF_TAB === "ANALISIS") {
    container.innerHTML = renderFinancialAnalysisDashboardHtml(ACTIVE_PERIOD);
    setTimeout(() => initFinancialAnalysisCharts(ACTIVE_PERIOD), 50);
    return;
  }

  if (ACTIVE_EF_TAB === "FLUJO") {'''

if 'ACTIVE_EF_TAB === "ANALISIS"' not in js:
    js = js.replace(target_hook, new_hook)

# Update docName in exportSmartContextualPDF
old_doc_name = 'ECP: "Estado_Cambios_Patrimonio_ECP",'
new_doc_name = 'ECP: "Estado_Cambios_Patrimonio_ECP",\n      ANALISIS: "Analisis_Financiero_y_Graficas",'
if 'ANALISIS: "Analisis_Financiero_y_Graficas"' not in js:
    js = js.replace(old_doc_name, new_doc_name)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(js)
print("Updated app.js with renderFinancialAnalysisDashboardHtml and Chart.js initialization!")

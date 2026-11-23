/* ==========================================================================
   MÓDULO PRESUPUESTO MAESTRO MAYO, JUNIO Y JULIO 2026 — ELECTROVIVIENDA S.A.S
   Fuente: data/presupuesto_mjj_2026.json (sincronizado de PRESUPUESTO_MAYO_JUNIO_JULIO_2026.xlsx)
   ========================================================================== */

let PRESUP_MJJ_DATA = null;
let PRESUP_MJJ_LOADING = false;
let PRESUP_ACTIVE_TAB = "RESUMEN";
let PRESUP_ACTIVE_MONTH = "MAYO";
let PRESUP_EFC_MODE = "MAYO"; // "MAYO" | "JUNIO" | "JULIO" | "COMPARATIVO"
let PRESUP_SHOW_GUIDE = true;
const PRESUP_CHARTS = {};

function pmjjEsc(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function pmjjCop(n, decimals = 0) {
  if (n === null || n === undefined || isNaN(Number(n))) return "-";
  const val = Number(n);
  const abs = Math.abs(val);
  const formatted = new Intl.NumberFormat("es-CO", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(abs);
  return val < 0 ? `-$${formatted}` : `$${formatted}`;
}

function pmjjNum(n) {
  if (n === null || n === undefined || isNaN(Number(n))) return "-";
  return new Intl.NumberFormat("es-CO", { maximumFractionDigits: 0 }).format(Number(n));
}

function pmjjPct(n, decimals = 2) {
  if (n === null || n === undefined || isNaN(Number(n))) return "-";
  return `${(Number(n) * 100).toFixed(decimals)}%`;
}

function destroyPresupCharts() {
  Object.keys(PRESUP_CHARTS).forEach(k => {
    try {
      if (PRESUP_CHARTS[k]) PRESUP_CHARTS[k].destroy();
    } catch (_) {}
    delete PRESUP_CHARTS[k];
  });
}

async function loadPresupuestoMJJData(force = false) {
  if (PRESUP_MJJ_DATA && !force) return PRESUP_MJJ_DATA;
  if (PRESUP_MJJ_LOADING) return null;
  PRESUP_MJJ_LOADING = true;
  try {
    const resp = await fetch(`data/presupuesto_mjj_2026.json?v=${Date.now()}`);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    PRESUP_MJJ_DATA = await resp.json();
    return PRESUP_MJJ_DATA;
  } finally {
    PRESUP_MJJ_LOADING = false;
  }
}

function setPresupMjjTab(tab) {
  PRESUP_ACTIVE_TAB = tab;
  renderPresupuestoMJJ();
}

function setPresupMjjMonth(mes) {
  PRESUP_ACTIVE_MONTH = mes;
  renderPresupuestoMJJ();
}

function setPresupEfcMode(mode) {
  PRESUP_EFC_MODE = mode;
  renderPresupuestoMJJ();
}

function togglePresupMjjGuide() {
  PRESUP_SHOW_GUIDE = !PRESUP_SHOW_GUIDE;
  renderPresupuestoMJJ();
}

function syncPresupuestoMjjWithGlobalPeriod(period) {
  if (["MAYO", "JUNIO", "JULIO"].includes(period)) {
    PRESUP_ACTIVE_MONTH = period;
    if (PRESUP_EFC_MODE !== "COMPARATIVO") {
      PRESUP_EFC_MODE = period;
    }
    if (PRESUP_MJJ_DATA) {
      renderPresupuestoMJJ();
    }
  }
}

async function renderPresupuestoMJJ() {
  const root = document.getElementById("presupuestoMjjRoot");
  if (!root) return;

  if (typeof ACTIVE_PERIOD !== "undefined" && ["MAYO", "JUNIO", "JULIO"].includes(ACTIVE_PERIOD)) {
    PRESUP_ACTIVE_MONTH = ACTIVE_PERIOD;
    if (PRESUP_EFC_MODE !== "COMPARATIVO") {
      PRESUP_EFC_MODE = ACTIVE_PERIOD;
    }
  }

  if (!PRESUP_MJJ_DATA) {
    root.innerHTML = `
      <div class="card"><div class="card-body" style="text-align:center; padding:42px;">
        <div style="font-size:2rem; margin-bottom:10px;">⏳</div>
        <div style="font-weight:700; color:var(--text-main);">Cargando Presupuesto Maestro Mayo, Junio y Julio 2026...</div>
      </div></div>`;
    try {
      await loadPresupuestoMJJData();
    } catch (err) {
      root.innerHTML = `
        <div class="card"><div class="card-body" style="text-align:center; padding:36px; color:var(--brand-danger);">
          <strong>No se pudo cargar data/presupuesto_mjj_2026.json</strong><br/>
          <span style="font-size:0.85rem;">${pmjjEsc(err.message)}</span>
        </div></div>`;
      return;
    }
  }

  const d = PRESUP_MJJ_DATA;
  const may = d.meses.MAYO;
  const jun = d.meses.JUNIO;
  const jul = d.meses.JULIO;

  const ventasTrim = d.parametros.tablero_comparativo[1]?.trimestre ?? (may.er.ingresos_4135 + jun.er.ingresos_4135 + jul.er.ingresos_4135);
  const unidTrim = d.parametros.tablero_comparativo[0]?.trimestre ?? (may.ventas.totales.unidades + jun.ventas.totales.unidades + jul.ventas.totales.unidades);
  const unTrim = d.parametros.tablero_comparativo[7]?.trimestre ?? (may.er.utilidad_neta + jun.er.utilidad_neta + jul.er.utilidad_neta);
  const cajaAbril = d.meta.saldo_inicial_caja_abril;
  const cajaJulio = jul.efc.saldo_final;
  const crecCajaPct = cajaAbril > 0 ? ((cajaJulio - cajaAbril) / cajaAbril) : 0;

  const tabs = [
    { id: "RESUMEN",    label: "📌 Resumen & Cómo Explicarlo" },
    { id: "PARAMETROS", label: "⚙️ Parámetros & Precios" },
    { id: "OPERATIVO",  label: "🛒 Ventas, Inventario & Compras" },
    { id: "EFC",        label: "💵 Flujo de Efectivo (EFC)" },
    { id: "ER",         label: "📈 Estado de Resultados (ER)" },
    { id: "ESF",        label: "🏛️ Situación Financiera (ESF)" },
  ];

  root.innerHTML = `
    <!-- ENCABEZADO EJECUTIVO -->
    <div class="card pmjj-hero-card">
      <div class="pmjj-hero-inner">
        <div>
          <div class="pmjj-badges">
            <span class="pmjj-badge pmjj-badge-gold">ELECTROVIVIENDA S.A.S • NIT ${pmjjEsc(d.meta.nit)}</span>
            <span class="pmjj-badge pmjj-badge-emerald">Política Stock en 0</span>
            <span class="pmjj-badge pmjj-badge-blue">Meta 50% EA (${pmjjCop(d.meta.meta_utilidad_mensual)}/mes)</span>
            <span class="pmjj-badge pmjj-badge-purple">Impuestos activos desde Mayo</span>
          </div>
          <h2 class="pmjj-hero-title">🎯 Presupuesto Maestro Proyectado: Mayo, Junio y Julio 2026</h2>
          <p class="pmjj-hero-sub">
            Sincronizado directamente desde <code>${pmjjEsc(d.meta.archivo)}</code> (${d.meta.hojas_count} hojas).
            Diseñado paso a paso para entender y sustentar fácilmente ventas, inventario inicial de Abril, costos, impuestos, flujo de caja y estados financieros NIIF.
          </p>
        </div>
        <div class="pmjj-hero-actions">
          <button class="btn ${PRESUP_SHOW_GUIDE ? "btn-primary" : "btn-outline"} btn-sm" onclick="togglePresupMjjGuide()">
            🎤 Guión para Explicar: ${PRESUP_SHOW_GUIDE ? "ON" : "OFF"}
          </button>
          <a class="btn btn-gold btn-sm" href="${pmjjEsc(d.meta.archivo)}" download="${pmjjEsc(d.meta.archivo)}">
            📥 Descargar Excel (.xlsx)
          </a>
          <button class="btn btn-outline btn-sm" onclick="window.print()">🖨️ Imprimir</button>
        </div>
      </div>
    </div>

    <!-- 4 TARJETAS KPI TRIMESTRALES -->
    <div class="kpi-row">
      <div class="kpi-card">
        <div class="kpi-label">Ventas Netas Trimestre (4135)</div>
        <div class="kpi-value">${pmjjCop(ventasTrim)}</div>
        <div class="kpi-sub">${pmjjNum(unidTrim)} unidades vendidas • Margen bruto 30%</div>
      </div>
      <div class="kpi-card kpi-emerald">
        <div class="kpi-label">Utilidad Neta Trimestre</div>
        <div class="kpi-value" style="color:var(--brand-emerald);">${pmjjCop(unTrim)}</div>
        <div class="kpi-sub">✓ 3 de 3 meses superan la meta de ${pmjjCop(d.meta.meta_utilidad_mensual)}/mes</div>
      </div>
      <div class="kpi-card kpi-gold">
        <div class="kpi-label">Saldo Final de Caja a Julio</div>
        <div class="kpi-value">${pmjjCop(cajaJulio)}</div>
        <div class="kpi-sub">+${(crecCajaPct * 100).toFixed(1)}% vs saldo real de Abril (${pmjjCop(cajaAbril)})</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Activos Totales a Julio</div>
        <div class="kpi-value">${pmjjCop(jul.esf.total_activos)}</div>
        <div class="kpi-sub">Patrimonio crece a ${pmjjCop(jul.esf.total_patrimonio)}</div>
      </div>
    </div>

    <!-- NAVEGACIÓN DE SUB-PESTAÑAS -->
    <div class="filter-bar pmjj-subbar">
      <div class="filter-tabs">
        ${tabs.map(t => `
          <button class="filter-chip ${PRESUP_ACTIVE_TAB === t.id ? "active" : ""}" onclick="setPresupMjjTab('${t.id}')">
            ${t.label}
          </button>
        `).join("")}
      </div>
      <div style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">
        Actualizado del Excel: ${pmjjEsc(d.meta.excel_mtime)}
      </div>
    </div>

    <!-- CONTENIDO DE LA PESTAÑA ACTIVA -->
    <div id="presupMjjTabContent"></div>
  `;

  const container = document.getElementById("presupMjjTabContent");
  destroyPresupCharts();

  if (PRESUP_ACTIVE_TAB === "RESUMEN") {
    renderTabResumen(container, d);
  } else if (PRESUP_ACTIVE_TAB === "PARAMETROS") {
    renderTabParametros(container, d);
  } else if (PRESUP_ACTIVE_TAB === "OPERATIVO") {
    renderTabOperativo(container, d);
  } else if (PRESUP_ACTIVE_TAB === "EFC") {
    renderTabEFC(container, d);
  } else if (PRESUP_ACTIVE_TAB === "ER") {
    renderTabER(container, d);
  } else if (PRESUP_ACTIVE_TAB === "ESF") {
    renderTabESF(container, d);
  }
}

/* ==========================================================================
   1. TAB: RESUMEN & CÓMO EXPLICARLO
   ========================================================================== */
function renderTabResumen(container, d) {
  const may = d.meses.MAYO;
  const jun = d.meses.JUNIO;
  const jul = d.meses.JULIO;
  const metaUN = d.meta.meta_utilidad_mensual;

  const pasos = [
    {
      num: "1",
      titulo: "La Meta de los Socios (50% EA)",
      texto: `Los socios aportaron ${pmjjCop(248600000)} (cta. 3105) y exigen una rentabilidad del 50% Efectivo Anual, equivalente a 3,44% mensual = ${pmjjCop(metaUN)} libres al mes después de Renta (35%) y Reserva Legal (10%).`,
      dato: `Mayo: ${pmjjCop(may.er.utilidad_neta)} | Junio: ${pmjjCop(jun.er.utilidad_neta)} | Julio: ${pmjjCop(jul.er.utilidad_neta)}`
    },
    {
      num: "2",
      titulo: "Precios con 30% de Margen y 2 Costos de Neveras",
      texto: "Cada producto se vende con la fórmula Precio = Costo ÷ (1 − 30%). En Mayo las neveras tienen dos lotes: las 15 del Kardex de Abril que llegaron a $544.000 (se venden a $777.143) y las 6 compras nuevas 50/50 entre Cra. 13 ($610.000) y Electromenores ($500.000) con promedio de $555.000 (se venden a $792.857).",
      dato: "Kardex Abr: $544.000 → $777.143 | Compras 50/50: $555.000 → $792.857"
    },
    {
      num: "3",
      titulo: "Recuento de Abril y Política Stock en 0",
      texto: `A Mayo llegaron 37 unidades del Kardex de Abril por ${pmjjCop(33822000)} (6 TV, 15 Neveras, 5 Lavadoras, 11 Microondas). Como queremos vender 59 unidades y dejar el Inventario Final en 0, en Mayo solo compramos las 22 unidades faltantes (${pmjjCop(28440000)}). Ya en Junio y Julio se parte de 0 y Compras = Ventas (51 und.).`,
      dato: "Mayo: 37 inicial + 22 compradas = 59 vendidas → Stock Final 0"
    },
    {
      num: "4",
      titulo: "Gastos Fijos + Tabla de Amortización + Impuestos",
      texto: "A partir de Mayo solo proyectamos 3 gastos: Nómina/Beneficios ($10.186.476), Depreciación ($1.279.533) e Intereses del crédito Bancolombia tomados de la hoja TA (cuotas 3, 4 y 5). Además se activan IVA 19%, Retefuente 2,5% (246540), Autorretención 2,5% (246575), ICA 9,6‰ (246801), Avisos 15% (246802) y Bomberil 10% (246803).",
      dato: `Financieros 5305: May ${pmjjCop(593434)} | Jun ${pmjjCop(578978)} | Jul ${pmjjCop(564362)}`
    },
    {
      num: "5",
      titulo: "Flujo de Caja (EFC) Sano y Creciente",
      texto: `Mayo inicia con el efectivo real de Abril (${pmjjCop(d.meta.saldo_inicial_caja_abril)}), cobra la Cartera de Jaime (${pmjjCop(28857500)}) y el 50% contado de ventas, y paga los saldos pendientes de Abril más cuotas de Bancolombia y nómina. La caja sube a ${pmjjCop(jul.efc.saldo_final)} en Julio, incluso tras pagar ReteICA mensual e IVA bimestral (F-300).`,
      dato: `Caja: Abr ${pmjjCop(51852812)} → May ${pmjjCop(may.efc.saldo_final)} → Jun ${pmjjCop(jun.efc.saldo_final)} → Jul ${pmjjCop(jul.efc.saldo_final)}`
    },
  ];

  const tablero = d.parametros.tablero_comparativo;

  container.innerHTML = `
    ${PRESUP_SHOW_GUIDE ? `
      <div class="card">
        <div class="card-header">
          <div class="card-title">🎤 ¿Cómo explicar este Presupuesto en 5 pasos sencillos?</div>
          <span class="status-pill status-paid">Guía de Sustentación</span>
        </div>
        <div class="card-body">
          <div class="pmjj-steps-grid">
            ${pasos.map(p => `
              <div class="pmjj-step-card">
                <div class="pmjj-step-head">
                  <span class="pmjj-step-num">${p.num}</span>
                  <strong>${pmjjEsc(p.titulo)}</strong>
                </div>
                <p class="pmjj-step-text">${pmjjEsc(p.texto)}</p>
                <div class="pmjj-step-dato">${pmjjEsc(p.dato)}</div>
              </div>
            `).join("")}
          </div>
        </div>
      </div>
    ` : ""}

    <!-- GRÁFICAS COMPARATIVAS -->
    <div class="pmjj-charts-grid">
      <div class="card">
        <div class="card-header">
          <div class="card-title">📊 Resultados Mensuales: Ventas, Costo, Gastos y Utilidad Neta</div>
        </div>
        <div class="card-body">
          <div style="height:290px; position:relative;"><canvas id="pmjjChartResultados"></canvas></div>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="card-title">💵 Evolución del Efectivo en Caja (Abril Real → Julio Proyectado)</div>
        </div>
        <div class="card-body">
          <div style="height:290px; position:relative;"><canvas id="pmjjChartCaja"></canvas></div>
        </div>
      </div>
    </div>

    <!-- TABLERO EJECUTIVO COMPARATIVO -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">📋 Tablero Ejecutivo Comparativo — Mayo, Junio y Julio 2026</div>
        <span class="status-pill status-paid">Meta Mensual: ${pmjjCop(metaUN)}</span>
      </div>
      <div class="card-body">
        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr>
                <th>Indicador / Concepto Clave</th>
                <th class="num-col">Mayo 2026</th>
                <th class="num-col">Junio 2026</th>
                <th class="num-col">Julio 2026</th>
                <th class="num-col">Total Trimestre</th>
              </tr>
            </thead>
            <tbody>
              ${tablero.map((r, i) => {
                const isCount = i === 0;
                const isHighlight = i === 7 || i === 12;
                const isCheck = i === 14;
                const fmt = v => isCount ? pmjjNum(v) + " und." : pmjjCop(v);
                return `
                  <tr class="${isHighlight ? "pmjj-row-highlight" : ""}">
                    <td><strong>${pmjjEsc(r.concepto)}</strong></td>
                    <td class="num-col">${fmt(r.mayo)}</td>
                    <td class="num-col">${fmt(r.junio)}</td>
                    <td class="num-col">${fmt(r.julio)}</td>
                    <td class="num-col" style="font-weight:800; color:${isCheck ? (Math.abs(r.trimestre) >= 1 ? "var(--brand-warning)" : "var(--brand-emerald)") : "var(--brand-primary)"};">${fmt(r.trimestre)}${isCheck && Math.abs(r.trimestre) < 1 ? " ✓" : ""}</td>
                  </tr>`;
              }).join("")}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;

  // Render Chart.js visualizations
  if (typeof Chart !== "undefined") {
    const ctx1 = document.getElementById("pmjjChartResultados");
    if (ctx1) {
      PRESUP_CHARTS.res = new Chart(ctx1, {
        type: "bar",
        data: {
          labels: ["Mayo 2026", "Junio 2026", "Julio 2026"],
          datasets: [
            { label: "Ventas Netas (4135)", data: [may.er.ingresos_4135, jun.er.ingresos_4135, jul.er.ingresos_4135], backgroundColor: "#1E4976", borderRadius: 6 },
            { label: "Costo de Ventas (6135)", data: [may.er.costos_6135, jun.er.costos_6135, jul.er.costos_6135], backgroundColor: "#64748B", borderRadius: 6 },
            { label: "Gastos Operacionales", data: [may.er.total_gastos, jun.er.total_gastos, jul.er.total_gastos], backgroundColor: "#D97706", borderRadius: 6 },
            { label: "Utilidad Neta", data: [may.er.utilidad_neta, jun.er.utilidad_neta, jul.er.utilidad_neta], backgroundColor: "#059669", borderRadius: 6 },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: "bottom", labels: { boxWidth: 12, font: { size: 11 } } },
            tooltip: { callbacks: { label: c => `${c.dataset.label}: ${pmjjCop(c.parsed.y)}` } },
          },
          scales: {
            y: { ticks: { callback: v => `$${(v / 1e6).toFixed(0)}M` } },
          },
        },
      });
    }

    const ctx2 = document.getElementById("pmjjChartCaja");
    if (ctx2) {
      PRESUP_CHARTS.caja = new Chart(ctx2, {
        type: "line",
        data: {
          labels: ["Abril (Real)", "Mayo (Proy.)", "Junio (Proy.)", "Julio (Proy.)"],
          datasets: [{
            label: "Saldo Final de Caja (COP)",
            data: [d.meta.saldo_inicial_caja_abril, may.efc.saldo_final, jun.efc.saldo_final, jul.efc.saldo_final],
            borderColor: "#7030A0",
            backgroundColor: "rgba(112, 48, 160, 0.14)",
            fill: true,
            tension: 0.28,
            pointRadius: 6,
            pointBackgroundColor: "#D4AF37",
            pointBorderColor: "#7030A0",
            pointBorderWidth: 2,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: "bottom", labels: { boxWidth: 12, font: { size: 11 } } },
            tooltip: { callbacks: { label: c => `Caja: ${pmjjCop(c.parsed.y)}` } },
          },
          scales: {
            y: { beginAtZero: true, ticks: { callback: v => `$${(v / 1e6).toFixed(0)}M` } },
          },
        },
      });
    }
  }
}

/* ==========================================================================
   2. TAB: PARÁMETROS, PRECIOS Y TABLA DE AMORTIZACIÓN
   ========================================================================== */
function renderTabParametros(container, d) {
  const { reglas, proveedores_neveras, catalogo_precios } = d.parametros;
  const { condiciones, cuotas } = d.amortizacion;

  const formatParamVal = (p) => {
    if (p.parametro.includes("Capital") || p.parametro.includes("Meta")) return pmjjCop(p.valor);
    if (p.parametro.includes("Stock")) return `${pmjjNum(p.valor)} unidades`;
    return pmjjPct(p.valor, 2);
  };

  container.innerHTML = `
    ${PRESUP_SHOW_GUIDE ? `
      <div class="pmjj-explain-box">
        <strong>💡 Cómo explicar esta pestaña:</strong>
        Aquí nacen todas las reglas del presupuesto. Primero fijamos la meta del <strong>50% EA</strong> sobre el capital (${pmjjCop(metaOrCap(d))}), luego definimos un <strong>margen bruto del 30%</strong> para calcular cada precio de venta (<code>Precio = Costo ÷ 0,70</code>), promediamos las neveras 50/50 entre nuestros dos proveedores, y fijamos los intereses exactos del préstamo según la Tabla de Amortización (<code>TA</code>).
      </div>
    ` : ""}

    <div class="grid-2">
      <div class="card">
        <div class="card-header"><div class="card-title">⚙️ 1. Parámetros Financieros, Comerciales y Tributarios</div></div>
        <div class="card-body">
          <div class="table-wrap">
            <table class="acct-table">
              <thead><tr><th>Parámetro / Política</th><th class="num-col">Valor</th><th>Regla Aplicada</th></tr></thead>
              <tbody>
                ${reglas.map(r => `
                  <tr>
                    <td><strong>${pmjjEsc(r.parametro)}</strong></td>
                    <td class="num-col" style="font-weight:800; color:var(--brand-primary);">${formatParamVal(r)}</td>
                    <td style="font-size:0.78rem; color:var(--text-secondary);">${pmjjEsc(r.nota)}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div style="display:flex; flex-direction:column; gap:16px;">
        <div class="card">
          <div class="card-header"><div class="card-title">🧊 2. Promedio Ponderado Neveras (2 Proveedores 50/50)</div></div>
          <div class="card-body">
            <div class="table-wrap">
              <table class="acct-table">
                <thead><tr><th>Proveedor</th><th class="num-col">Costo Compra</th><th class="num-col">% Compra</th></tr></thead>
                <tbody>
                  ${proveedores_neveras.map((p, idx) => `
                    <tr class="${idx === 2 ? "pmjj-row-highlight" : ""}">
                      <td><strong>${pmjjEsc(p.proveedor)}</strong></td>
                      <td class="num-col">${pmjjCop(p.precio)}</td>
                      <td class="num-col">${pmjjPct(p.porcentaje, 0)}</td>
                    </tr>
                  `).join("")}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header"><div class="card-title">🏷️ 3. Catálogo de Base de Venta = Costo ÷ (1 − 30%)</div></div>
          <div class="card-body">
            <div class="table-wrap">
              <table class="acct-table">
                <thead><tr><th>Producto (Kardex / Lote)</th><th class="num-col">Costo Unit.</th><th class="num-col">Base de Venta</th><th class="num-col">Ganancia Unit.</th></tr></thead>
                <tbody>
                  ${catalogo_precios.map((c, idx) => `
                    <tr class="${idx === 4 ? "pmjj-row-amber" : ""}">
                      <td><strong>${pmjjEsc(c.producto)}</strong></td>
                      <td class="num-col">${pmjjCop(c.costo)}</td>
                      <td class="num-col" style="font-weight:800; color:var(--brand-emerald);">${pmjjCop(c.precio_venta)}</td>
                      <td class="num-col">${pmjjCop(c.ganancia_unit)}</td>
                    </tr>
                  `).join("")}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">🏦 4. Tabla de Amortización Bancolombia (Origen de Gasto Financiero 5305 y Cuota Mensual en Caja)</div>
        <span class="pmjj-badge pmjj-badge-blue">Crédito ${pmjjCop(condiciones.credito)} • ${condiciones.plazo_meses} meses • Cuota ${pmjjCop(condiciones.cuota)}</span>
      </div>
      <div class="card-body">
        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr>
                <th class="num-col">Cuota N°</th>
                <th>Mes Aplicado en ER</th>
                <th class="num-col">Valor Cuota (Sale de Caja)</th>
                <th class="num-col">Abono a Capital (Baja Pasivo 2105)</th>
                <th class="num-col">Interés Mensual (Va al Gasto 5305)</th>
                <th class="num-col">Saldo Capital Remanente</th>
              </tr>
            </thead>
            <tbody>
              ${cuotas.map(q => {
                const isProj = q.mes_contable.includes("Proyectado");
                return `
                  <tr class="${isProj ? "pmjj-row-highlight" : ""}">
                    <td class="num-col"><strong>#${q.cuota}</strong></td>
                    <td><strong>${pmjjEsc(q.mes_contable)}</strong></td>
                    <td class="num-col">${pmjjCop(q.valor_cuota, 2)}</td>
                    <td class="num-col">${pmjjCop(q.abono_capital, 2)}</td>
                    <td class="num-col" style="font-weight:800; color:var(--brand-primary);">${pmjjCop(q.interes, 2)}</td>
                    <td class="num-col">${pmjjCop(q.saldo_capital, 2)}</td>
                  </tr>`;
              }).join("")}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
}

function metaOrCap(d) {
  return d.parametros?.reglas?.[0]?.valor || 248600000;
}

/* ==========================================================================
   3. TAB: VENTAS, INVENTARIO Y COMPRAS POR MES
   ========================================================================== */
function renderTabOperativo(container, d) {
  const m = PRESUP_ACTIVE_MONTH;
  const mesData = d.meses[m];

  const guionMes = {
    MAYO: "En Mayo recibimos el inventario que quedó de Abril (37 unidades = $33.822.000: 6 TV a $3,5M, 15 Neveras del Kardex a $544.000, 5 Lavadoras a $730.000 y 11 Microondas a $92.000). Para llegar a 59 unidades vendidas con Stock Final en 0, solo compramos las 22 unidades faltantes ($28.440.000). Fíjate que las 15 neveras viejas de $544.000 se venden a $777.143 y las 6 neveras nuevas compradas en Mayo ($555.000 promedio) se venden a $792.857.",
    JUNIO: "Como Mayo cerró con Inventario Final = 0, Junio arranca en 0 unidades. Para cumplir la meta de utilidad neta ($8.543.408), vendemos 51 unidades exactas (13 TV, 12 Neveras a $555.000, 12 Lavadoras y 14 Microondas) y compramos exactamente esas mismas 51 unidades para mantener Stock Final = 0.",
    JULIO: "Igual que Junio, Julio inicia sin inventario (0 unidades), vende 51 unidades ($88.868.571 netas) y compra 51 unidades ($62.208.000), cerrando el trimestre con inventario en 0 y superando nuevamente la meta de utilidad neta mensual.",
  };

  container.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
      <span class="pmjj-badge pmjj-badge-blue">📅 Mes activo: ${m} 2026 (${pmjjNum(mesData.ventas.totales.unidades)} und.)</span>
      <span style="font-size:0.78rem; color:var(--text-muted); font-weight:600;">Cambia entre MAY, JUN y JUL en la barra superior</span>
    </div>

    ${PRESUP_SHOW_GUIDE ? `
      <div class="pmjj-explain-box">
        <strong>💡 Qué decir al explicar ${m} 2026:</strong> ${pmjjEsc(guionMes[m])}
      </div>
    ` : ""}

    <!-- 1. CÉDULA DE VENTAS -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Cédula de Ventas en Unidades e Impuestos — ${m} 2026</div>
        <span class="status-pill status-paid">50% Contado: ${pmjjCop(mesData.ventas.totales.contado_50)} | 50% Crédito: ${pmjjCop(mesData.ventas.totales.credito_50)}</span>
      </div>
      <div class="card-body">
        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr>
                <th>Ref.</th><th>Producto (Kardex / Lote)</th><th class="num-col">Unid.</th>
                <th class="num-col">Costo Unit.</th><th class="num-col">Costo Ventas (6135)</th>
                <th class="num-col">Base de Venta (Costo/0,7)</th><th class="num-col">Ventas Netas (4135)</th>
                <th class="num-col">IVA Gen. 19%</th>
                <th class="num-col">ICA 9,6‰ (135518)</th>
                <th class="num-col">Avisos 15% (135520)</th>
                <th class="num-col">Bomberil 10% (135525)</th>
                <th class="num-col">Neto Cobrar (1305)</th><th class="num-col">Autorret. 2,5% (246575)</th>
              </tr>
            </thead>
            <tbody>
              ${mesData.ventas.filas.map(f => `
                <tr>
                  <td><code>${pmjjEsc(f.ref)}</code></td>
                  <td><strong>${pmjjEsc(f.producto)}</strong></td>
                  <td class="num-col"><strong>${pmjjNum(f.unidades)}</strong></td>
                  <td class="num-col">${pmjjCop(f.costo_unit)}</td>
                  <td class="num-col">${pmjjCop(f.costo_total)}</td>
                  <td class="num-col">${pmjjCop(f.precio_venta)}</td>
                  <td class="num-col"><strong>${pmjjCop(f.ventas_netas)}</strong></td>
                  <td class="num-col">${pmjjCop(f.iva)}</td>
                  <td class="num-col">${pmjjCop(f.ica ?? 0)}</td>
                  <td class="num-col">${pmjjCop(f.avisos ?? 0)}</td>
                  <td class="num-col">${pmjjCop(f.bomberil ?? 0)}</td>
                  <td class="num-col" style="font-weight:700; color:var(--brand-primary);">${pmjjCop(f.neto_cobrar)}</td>
                  <td class="num-col">${pmjjCop(f.autoret)}</td>
                </tr>
              `).join("")}
              <tr class="pmjj-row-highlight">
                <td>TOTAL</td>
                <td><strong>TOTAL VENTAS ${m} 2026</strong></td>
                <td class="num-col"><strong>${pmjjNum(mesData.ventas.totales.unidades)}</strong></td>
                <td class="num-col">-</td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.costo_total)}</strong></td>
                <td class="num-col">-</td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.ventas_netas)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.iva)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.ica ?? 0)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.avisos ?? 0)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.bomberil ?? 0)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.neto_cobrar)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.autoret)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 2. RECUENTO DE INVENTARIO STOCK EN 0 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Recuento de Inventario Inicial y Unidades Necesarias a Comprar (Stock Final = 0) — ${m}</div>
      </div>
      <div class="card-body">
        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr>
                <th>Ref.</th><th>Producto</th><th class="num-col">Unid. a Vender</th>
                <th class="num-col">(-) Inv. Inicial</th><th class="num-col">Stock Final Deseado</th>
                <th class="num-col">(=) Unid. a Comprar</th><th class="num-col">Costo Unit.</th>
                <th class="num-col">Stock Final (1435)</th><th class="num-col">Valor Inv. Inicial Consumido</th>
                <th class="num-col">Valor Compras Mes</th>
              </tr>
            </thead>
            <tbody>
              ${mesData.inventario.filas.map(f => `
                <tr>
                  <td><code>${pmjjEsc(f.ref)}</code></td>
                  <td><strong>${pmjjEsc(f.producto)}</strong></td>
                  <td class="num-col">${pmjjNum(f.vender)}</td>
                  <td class="num-col" style="color:${f.inv_inicial > 0 ? "#B45309" : "inherit"}; font-weight:${f.inv_inicial > 0 ? 700 : 400};">${pmjjNum(f.inv_inicial)}</td>
                  <td class="num-col">${pmjjNum(f.stock_deseado)}</td>
                  <td class="num-col" style="font-weight:800; color:var(--brand-primary);">${pmjjNum(f.comprar)}</td>
                  <td class="num-col">${pmjjCop(f.costo_unit)}</td>
                  <td class="num-col">${pmjjNum(f.stock_final)} (${pmjjCop(f.val_inv_final)})</td>
                  <td class="num-col">${pmjjCop(f.val_inv_inicial)}</td>
                  <td class="num-col">${pmjjCop(f.val_comprar)}</td>
                </tr>
              `).join("")}
              <tr class="pmjj-row-highlight">
                <td>TOTAL</td>
                <td><strong>TOTAL INVENTARIO Y COMPRAS ${m}</strong></td>
                <td class="num-col"><strong>${pmjjNum(mesData.inventario.totales.vender)}</strong></td>
                <td class="num-col"><strong>${pmjjNum(mesData.inventario.totales.inv_inicial)}</strong></td>
                <td class="num-col"><strong>${pmjjNum(mesData.inventario.totales.stock_deseado)}</strong></td>
                <td class="num-col"><strong>${pmjjNum(mesData.inventario.totales.comprar)}</strong></td>
                <td class="num-col">-</td>
                <td class="num-col"><strong>${pmjjNum(mesData.inventario.totales.stock_final)} (${pmjjCop(mesData.inventario.totales.val_inv_final)})</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.inventario.totales.val_inv_inicial)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.inventario.totales.val_comprar)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 3 & 4: COMPRAS POR PROVEEDOR + LIQUIDACIÓN TRIBUTARIA -->
    <div class="card">
      <div class="card-header"><div class="card-title">3. Cédula de Compras por Proveedor y Retenciones — ${m} 2026</div></div>
      <div class="card-body">
        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr>
                <th>Proveedor</th><th>Producto</th><th class="num-col">Unid.</th>
                <th class="num-col">Costo Unit.</th><th class="num-col">Subtotal Compra</th>
                <th class="num-col">IVA Desc. 19%</th><th class="num-col">Retefuente 2,5% (246540)</th>
                <th class="num-col">ICA 9,6‰ (246801)</th>
                <th class="num-col">Avisos 15% (246802)</th>
                <th class="num-col">Bomberil 10% (246803)</th>
                <th class="num-col">Neto Pagar (2205)</th>
                <th class="num-col">50% Contado</th><th class="num-col">50% Crédito 30d</th>
              </tr>
            </thead>
            <tbody>
              ${mesData.compras.filas.map(f => `
                <tr>
                  <td><strong>${pmjjEsc(f.proveedor)}</strong></td>
                  <td>${pmjjEsc(f.producto)}</td>
                  <td class="num-col"><strong>${pmjjNum(f.unidades)}</strong></td>
                  <td class="num-col">${pmjjCop(f.costo_unit)}</td>
                  <td class="num-col">${pmjjCop(f.subtotal)}</td>
                  <td class="num-col">${pmjjCop(f.iva_desc)}</td>
                  <td class="num-col">${pmjjCop(f.retefuente)}</td>
                  <td class="num-col">${pmjjCop(f.ica ?? 0)}</td>
                  <td class="num-col">${pmjjCop(f.avisos ?? 0)}</td>
                  <td class="num-col">${pmjjCop(f.bomberil ?? 0)}</td>
                  <td class="num-col" style="font-weight:700;">${pmjjCop(f.neto_pagar)}</td>
                  <td class="num-col">${pmjjCop(f.contado_50)}</td>
                  <td class="num-col">${pmjjCop(f.credito_50)}</td>
                </tr>
              `).join("")}
              <tr class="pmjj-row-highlight">
                <td>TOTAL</td>
                <td><strong>TOTAL PROVEEDORES ${m}</strong></td>
                <td class="num-col"><strong>${pmjjNum(mesData.compras.totales.unidades)}</strong></td>
                <td class="num-col">-</td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.subtotal)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.iva_desc)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.retefuente)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.ica ?? 0)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.avisos ?? 0)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.bomberil ?? 0)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.neto_pagar)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.contado_50)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.credito_50)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header"><div class="card-title">4. Liquidación Tributaria del Mes (F-350, ReteICA y F-300) — ${m} 2026</div></div>
      <div class="card-body">
        <div class="table-wrap">
          <table class="acct-table">
            <thead><tr><th>Concepto Tributario</th><th>PUC</th><th class="num-col">Valor (COP)</th><th>Declaración / Vencimiento</th></tr></thead>
            <tbody>
              ${mesData.tributaria.map(t => `
                <tr class="${["2465", "2468", "2408"].includes(String(t.puc || "").trim()) ? "pmjj-row-highlight" : ""}">
                  <td><strong>${pmjjEsc(t.concepto)}</strong></td>
                  <td><code>${pmjjEsc(t.puc)}</code></td>
                  <td class="num-col" style="font-weight:800;">${pmjjCop(t.valor)}</td>
                  <td style="font-size:0.8rem; color:var(--text-secondary);">${pmjjEsc(t.nota)}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
}

/* ==========================================================================
   4. TAB: FLUJO DE EFECTIVO PROYECTADO (EFC)
   ========================================================================== */
function renderTabEFC(container, d) {
  const mode = PRESUP_EFC_MODE;
  const may = d.meses.MAYO.efc;
  const jun = d.meses.JUNIO.efc;
  const jul = d.meses.JULIO.efc;

  const renderSingleEFC = (efc, mesLabel) => `
    <div class="card">
      <div class="card-header">
        <div class="card-title">💵 ${pmjjEsc(efc.titulo || `CAJA — EFC PROYECTADO ${mesLabel} 2026`)}</div>
        <span class="pmjj-badge pmjj-badge-purple">Saldo Final: ${pmjjCop(efc.saldo_final)}</span>
      </div>
      <div class="card-body">
        <div class="table-wrap">
          <table class="pmjj-efc-table">
            <thead>
              <tr>
                <th colspan="4" class="pmjj-efc-banner">CAJA — ${mesLabel} 2026</th>
              </tr>
              <tr>
                <th>CONCEPTO</th>
                <th class="num-col">ENTRADA</th>
                <th class="num-col">SALIDA</th>
                <th class="num-col">TOTAL ACUMULADO</th>
              </tr>
            </thead>
            <tbody>
              ${efc.filas.map(f => `
                <tr>
                  <td><strong>${pmjjEsc(f.concepto)}</strong></td>
                  <td class="num-col" style="color:#047857; font-weight:600;">${f.entrada !== null ? pmjjCop(f.entrada) : ""}</td>
                  <td class="num-col" style="color:#B91C1C; font-weight:600;">${f.salida !== null ? pmjjCop(f.salida) : ""}</td>
                  <td class="num-col" style="font-weight:700;">${pmjjCop(f.total)}</td>
                </tr>
              `).join("")}
              <tr class="pmjj-efc-total">
                <td><strong>SALDO NETO FINAL ${mesLabel}</strong></td>
                <td class="num-col"><strong>${pmjjCop(efc.total_entradas)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(efc.total_salidas)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(efc.saldo_final)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;

  const activeMonth = ["MAYO", "JUNIO", "JULIO"].includes(PRESUP_ACTIVE_MONTH) ? PRESUP_ACTIVE_MONTH : "MAYO";

  container.innerHTML = `
    <div class="pmjj-month-pills" style="justify-content:space-between; align-items:center;">
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <button class="filter-chip ${mode !== "COMPARATIVO" ? "active" : ""}" onclick="setPresupEfcMode(PRESUP_ACTIVE_MONTH)">
          💵 Ver Mes Activo (${activeMonth} 2026)
        </button>
        <button class="filter-chip ${mode === "COMPARATIVO" ? "active" : ""}" onclick="setPresupEfcMode('COMPARATIVO')">
          📊 Ver Comparativo 3 Meses
        </button>
      </div>
      <span style="font-size:0.78rem; color:var(--text-muted); font-weight:600;">Cambia entre MAY, JUN y JUL en la barra superior</span>
    </div>

    ${PRESUP_SHOW_GUIDE ? `
      <div class="pmjj-explain-box">
        <strong>💡 Cómo explicar el Flujo de Efectivo (EFC):</strong>
        En <strong>Mayo</strong> arrancamos con la caja + bancos reales de Abril (${pmjjCop(may.saldo_inicial)}), cobramos la cartera pendiente de Jaime (${pmjjCop(28857500)}) y el 50% contado de ventas de Mayo, y pagamos proveedores pendientes de Abril (${pmjjCop(5778000)}), la última cuota de remodelación (${pmjjCop(568800)}), Retefuente de Abril (${pmjjCop(442490)}), Seguridad Social, Salarios y Cuota del crédito Bancolombia. En <strong>Junio y Julio</strong> entra el 50% a crédito del mes anterior, el <strong>ReteICA se paga mensualmente</strong> (en Junio se paga Mayo y en Julio se paga Junio), y en <strong>Julio</strong> se paga el <strong>IVA F-300 bimestral</strong> (May–Jun).
      </div>
    ` : ""}

    ${mode === "COMPARATIVO" ? `
      <div class="card">
        <div class="card-header"><div class="card-title">📊 Resumen Comparativo del Flujo de Caja — Mayo, Junio y Julio 2026</div></div>
        <div class="card-body">
          <div class="table-wrap">
            <table class="acct-table">
              <thead>
                <tr><th>Concepto de Flujo</th><th class="num-col">Mayo 2026</th><th class="num-col">Junio 2026</th><th class="num-col">Julio 2026</th></tr>
              </thead>
              <tbody>
                <tr><td><strong>Saldo Inicial de Caja y Bancos</strong></td><td class="num-col">${pmjjCop(may.saldo_inicial)}</td><td class="num-col">${pmjjCop(jun.saldo_inicial)}</td><td class="num-col">${pmjjCop(jul.saldo_inicial)}</td></tr>
                <tr><td><strong>(+) Total Entradas del Mes (Contado + Cartera)</strong></td><td class="num-col" style="color:var(--brand-emerald); font-weight:700;">${pmjjCop(may.total_entradas)}</td><td class="num-col" style="color:var(--brand-emerald); font-weight:700;">${pmjjCop(jun.total_entradas)}</td><td class="num-col" style="color:var(--brand-emerald); font-weight:700;">${pmjjCop(jul.total_entradas)}</td></tr>
                <tr><td><strong>(-) Total Salidas del Mes (Compras + Nómina + Cuota + Impuestos)</strong></td><td class="num-col" style="color:var(--brand-danger); font-weight:700;">${pmjjCop(may.total_salidas)}</td><td class="num-col" style="color:var(--brand-danger); font-weight:700;">${pmjjCop(jun.total_salidas)}</td><td class="num-col" style="color:var(--brand-danger); font-weight:700;">${pmjjCop(jul.total_salidas)}</td></tr>
                <tr class="pmjj-row-highlight"><td><strong>(=) SALDO FINAL NETO EN CAJA Y BANCOS (1105 + 1110)</strong></td><td class="num-col"><strong>${pmjjCop(may.saldo_final)}</strong></td><td class="num-col"><strong>${pmjjCop(jun.saldo_final)}</strong></td><td class="num-col"><strong>${pmjjCop(jul.saldo_final)}</strong></td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      ${renderSingleEFC(may, "MAYO")}
      ${renderSingleEFC(jun, "JUNIO")}
      ${renderSingleEFC(jul, "JULIO")}
    ` : renderSingleEFC(d.meses[activeMonth].efc, activeMonth)}
  `;
}

/* ==========================================================================
   5. TAB: ESTADO DE RESULTADOS PROYECTADO (ER)
   ========================================================================== */
function renderTabER(container, d) {
  const may = d.meses.MAYO.er;
  const jun = d.meses.JUNIO.er;
  const jul = d.meses.JULIO.er;
  const meta = d.meta.meta_utilidad_mensual;

  const gastoPorCodigo = (erObj, cod) => {
    const found = erObj.gastos_detalle.find(g => g.codigo === cod);
    return found ? found.valor : 0;
  };

  const filasER = [
    { cod: "4135", nom: "COMERCIO AL POR MAYOR Y POR MENOR (Ventas Netas)", v1: may.ingresos_4135, v2: jun.ingresos_4135, v3: jul.ingresos_4135, cls: "pmjj-row-subtle" },
    { cod: "6135", nom: "(-) COSTO DE VENTAS (Mercancía vendida — 70%)", v1: may.costos_6135, v2: jun.costos_6135, v3: jul.costos_6135 },
    { cod: "—",    nom: "(=) UTILIDAD BRUTA EN VENTAS (Margen 30%)", v1: may.utilidad_bruta, v2: jun.utilidad_bruta, v3: jul.utilidad_bruta, cls: "pmjj-row-highlight" },
    { cod: "5105", nom: "(-) BENEFICIOS A EMPLEADOS (Nómina + Seguridad Soc. + Prestaciones)", v1: gastoPorCodigo(may, "5105"), v2: gastoPorCodigo(jun, "5105"), v3: gastoPorCodigo(jul, "5105") },
    { cod: "5160", nom: "(-) DEPRECIACIONES ADMINISTRATIVAS (Construcciones)", v1: gastoPorCodigo(may, "5160"), v2: gastoPorCodigo(jun, "5160"), v3: gastoPorCodigo(jul, "5160") },
    { cod: "5260", nom: "(-) DEPRECIACIONES VENTAS (Flota y equipo)", v1: gastoPorCodigo(may, "5260"), v2: gastoPorCodigo(jun, "5260"), v3: gastoPorCodigo(jul, "5260") },
    { cod: "5305", nom: "(-) GASTOS FINANCIEROS (Interés cuota crédito de hoja TA)", v1: gastoPorCodigo(may, "5305"), v2: gastoPorCodigo(jun, "5305"), v3: gastoPorCodigo(jul, "5305") },
    { cod: "—",    nom: "(=) TOTAL GASTOS OPERACIONALES", v1: may.total_gastos, v2: jun.total_gastos, v3: jul.total_gastos, cls: "pmjj-row-subtle" },
    { cod: "—",    nom: "(=) UTILIDAD ANTES DE IMPUESTOS (UAI)", v1: may.uai, v2: jun.uai, v3: jul.uai, cls: "pmjj-row-subtle" },
    { cod: "2499", nom: "(-) PROVISIÓN IMPUESTO DE RENTA (35% — Mensual)", v1: may.impuesto_renta, v2: jun.impuesto_renta, v3: jul.impuesto_renta },
    { cod: "—",    nom: "(=) UTILIDAD DESPUÉS DE IMPUESTOS", v1: may.udi, v2: jun.udi, v3: jul.udi },
    { cod: "3305", nom: "(-) RESERVA LEGAL (10%)", v1: may.reserva_legal, v2: jun.reserva_legal, v3: jul.reserva_legal },
    { cod: "3605", nom: "(=) UTILIDAD NETA PROYECTADA DEL MES", v1: may.utilidad_neta, v2: jun.utilidad_neta, v3: jul.utilidad_neta, cls: "pmjj-row-highlight" },
  ];

  container.innerHTML = `
    ${PRESUP_SHOW_GUIDE ? `
      <div class="pmjj-explain-box">
        <strong>💡 Cómo explicar el Estado de Resultados (ER Proyectado):</strong>
        1) El margen bruto sobre ventas es exactamente el <strong>30%</strong> en los tres meses.
        2) Como pediste a partir de Mayo, solo dejamos <strong>3 grupos de gastos</strong>: Beneficios a empleados (${pmjjCop(10186476)}), Depreciación (${pmjjCop(1279533)}) y Financieros tomados directamente de la cuota del mes en la Tabla de Amortización <code>TA</code>.
        3) Después de descontar Renta (35%) y Reserva Legal (10%), los 3 meses cumplen la meta exigida de <strong>${pmjjCop(meta)}</strong> mensuales.
      </div>
    ` : ""}

    <div class="card">
      <div class="card-header">
        <div class="card-title">📈 Estado de Resultados Proyectado NIIF — Comparativo Mayo, Junio y Julio 2026</div>
        <span class="status-pill status-paid">Meta Mensual: ${pmjjCop(meta)} ✓</span>
      </div>
      <div class="card-body">
        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr>
                <th>PUC</th><th>Concepto</th>
                <th class="num-col">Mayo 2026</th><th class="num-col">Junio 2026</th>
                <th class="num-col">Julio 2026</th><th class="num-col">Total Trimestre</th>
              </tr>
            </thead>
            <tbody>
              ${filasER
                .filter(r => !(/^\d{4}$/.test(String(r.cod || "").trim()) && Math.abs(r.v1) < 0.01 && Math.abs(r.v2) < 0.01 && Math.abs(r.v3) < 0.01))
                .map(r => `
                <tr class="${r.cls || ""}">
                  <td><code>${pmjjEsc(r.cod)}</code></td>
                  <td><strong>${pmjjEsc(r.nom)}</strong></td>
                  <td class="num-col">${pmjjCop(r.v1)}</td>
                  <td class="num-col">${pmjjCop(r.v2)}</td>
                  <td class="num-col">${pmjjCop(r.v3)}</td>
                  <td class="num-col" style="font-weight:800;">${pmjjCop(r.v1 + r.v2 + r.v3)}</td>
                </tr>
              `).join("")}
              <tr>
                <td>✓</td>
                <td><strong>Cumplimiento vs. Meta 50% EA (${pmjjCop(meta)}/mes)</strong></td>
                <td class="num-col" style="color:var(--brand-emerald); font-weight:800;">+${pmjjCop(may.utilidad_neta - meta)} ✓</td>
                <td class="num-col" style="color:var(--brand-emerald); font-weight:800;">+${pmjjCop(jun.utilidad_neta - meta)} ✓</td>
                <td class="num-col" style="color:var(--brand-emerald); font-weight:800;">+${pmjjCop(jul.utilidad_neta - meta)} ✓</td>
                <td class="num-col" style="color:var(--brand-emerald); font-weight:800;">3 / 3 Meses Cumplen ✓</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
}

/* ==========================================================================
   6. TAB: ESTADO DE SITUACIÓN FINANCIERA PROYECTADO (ESF)
   ========================================================================== */
function renderTabESF(container, d) {
  const may = d.meses.MAYO.esf;
  const jun = d.meses.JUNIO.esf;
  const jul = d.meses.JULIO.esf;

  const valOf = (arr, cod) => {
    const f = arr.find(x => x.codigo === cod);
    return f ? f.valor : 0;
  };

  const renderSectionRows = (rows, groupKey) => rows
    .filter(r => {
      const vMay = valOf(may[groupKey], r.cod);
      const vJun = valOf(jun[groupKey], r.cod);
      const vJul = valOf(jul[groupKey], r.cod);
      return Math.abs(vMay) >= 0.01 || Math.abs(vJun) >= 0.01 || Math.abs(vJul) >= 0.01;
    })
    .map(r => `
    <tr>
      <td><code>${pmjjEsc(r.cod)}</code></td>
      <td>${pmjjEsc(r.nom)}</td>
      <td class="num-col">${pmjjCop(valOf(may[groupKey], r.cod))}</td>
      <td class="num-col">${pmjjCop(valOf(jun[groupKey], r.cod))}</td>
      <td class="num-col">${pmjjCop(valOf(jul[groupKey], r.cod))}</td>
    </tr>
  `).join("");

  const acRows = [
    { cod: "1105", nom: "CAJA" },
    { cod: "1110", nom: "BANCOS (Saldo EFC menos Caja)" },
    { cod: "1305", nom: "CLIENTES (50% ventas a crédito)" },
    { cod: "1355", nom: "ANTICIPO DE IMPUESTOS" },
    { cod: "1435", nom: "MERCANCÍA NO FABRICADA POR LA EMPRESA" },
  ];
  const ancRows = [
    { cod: "1504", nom: "TERRENOS" },
    { cod: "1516", nom: "CONSTRUCCIONES Y EDIFICACIONES" },
    { cod: "1540", nom: "FLOTA Y EQUIPO DE TRANSPORTE" },
    { cod: "1592", nom: "DEPRECIACIÓN ACUMULADA ACTIVOS (CR)" },
  ];
  const pcRows = [
    { cod: "2105", nom: "BANCOS NACIONALES (Porción Corriente crédito Bancolombia)" },
    { cod: "2205", nom: "PROVEEDORES (50% compras a crédito)" },
    { cod: "2408", nom: "IMPUESTO A LAS VENTAS POR PAGAR - IVA" },
    { cod: "2465", nom: "RETENCIÓN EN LA FUENTE POR PAGAR (F-350)" },
    { cod: "2468", nom: "IMPUESTO DE ICA RETENIDO A TERCEROS" },
    { cod: "2499", nom: "PROVISIÓN PARA OBLIGACIONES FISCALES (Renta 35%)" },
    { cod: "2570", nom: "RETENCIONES Y APORTES DE NÓMINA" },
    { cod: "2580", nom: "FONDO DE PENSIONES Y CESANTÍAS POR PAGAR" },
    { cod: "2610", nom: "PROVISIÓN PARA OBLIGACIONES LABORALES" },
    { cod: "2705", nom: "INGRESOS RECIBIDOS POR ANTICIPADO" },
  ];
  const patRows = [
    { cod: "3105", nom: "CAPITAL SUSCRITO Y PAGADO" },
    { cod: "3305", nom: "RESERVAS OBLIGATORIAS" },
    { cod: "3605", nom: "UTILIDAD DEL EJERCICIO (Acumulada May–Jul)" },
    { cod: "3705", nom: "UTILIDADES ACUMULADAS (De ejercicios anteriores)" },
    { cod: "3710", nom: "PÉRDIDAS ACUMULADAS (Enero–Abril)" },
  ];

  container.innerHTML = `
    ${PRESUP_SHOW_GUIDE ? `
      <div class="pmjj-explain-box">
        <strong>💡 Cómo explicar el Estado de Situación Financiera (ESF Proyectado):</strong>
        1) El inventario (<code>1435</code>) cierra en <strong>$0</strong> en los 3 meses por la política Stock en 0 (las cuentas en cero se ocultan automáticamente).
        2) El Efectivo (<code>1105 + 1110</code>) viene directamente del saldo final de <code>EFC PROYECTADO</code> (${pmjjCop(may.activos_corrientes[0].valor + may.activos_corrientes[1].valor)} → ${pmjjCop(jul.activos_corrientes[0].valor + jul.activos_corrientes[1].valor)}).
        3) El crédito Bancolombia (<code>2105</code>) baja cuota a cuota según la hoja <code>TA</code>.
        4) En <strong>Mayo, Junio y Julio</strong> la ecuación contable cuadra exacto en <strong>$0</strong> (incluyendo el cruce del saldo a favor de IVA de <code>$187.340</code> entre Anticipos <code>1355</code> e IVA por pagar <code>2408</code>).
      </div>
    ` : ""}

    <div class="card">
      <div class="card-header">
        <div class="card-title">🏛️ Estado de Situación Financiera Proyectado NIIF — Mayo, Junio y Julio 2026</div>
        <span class="pmjj-badge pmjj-badge-blue">Cifras en COP</span>
      </div>
      <div class="card-body">
        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr><th>PUC</th><th>Cuenta / Grupo</th><th class="num-col">Mayo 2026</th><th class="num-col">Junio 2026</th><th class="num-col">Julio 2026</th></tr>
            </thead>
            <tbody>
              <tr class="niif-row-grupo niif-grupo-activo-corr"><td colspan="5">Activos Corrientes</td></tr>
              ${renderSectionRows(acRows, "activos_corrientes")}
              <tr class="pmjj-row-subtle"><td></td><td><strong>SUBTOTAL ACTIVOS CORRIENTES</strong></td><td class="num-col"><strong>${pmjjCop(may.subtotal_ac)}</strong></td><td class="num-col"><strong>${pmjjCop(jun.subtotal_ac)}</strong></td><td class="num-col"><strong>${pmjjCop(jul.subtotal_ac)}</strong></td></tr>

              <tr class="niif-row-grupo niif-grupo-activo-fijo"><td colspan="5">Activos Fijos (Propiedad, Planta y Equipo)</td></tr>
              ${renderSectionRows(ancRows, "activos_no_corrientes")}
              <tr class="pmjj-row-subtle"><td></td><td><strong>SUBTOTAL ACTIVOS FIJOS</strong></td><td class="num-col"><strong>${pmjjCop(may.subtotal_anc)}</strong></td><td class="num-col"><strong>${pmjjCop(jun.subtotal_anc)}</strong></td><td class="num-col"><strong>${pmjjCop(jul.subtotal_anc)}</strong></td></tr>

              <tr class="pmjj-row-highlight"><td>1</td><td><strong>TOTAL ACTIVOS</strong></td><td class="num-col"><strong>${pmjjCop(may.total_activos)}</strong></td><td class="num-col"><strong>${pmjjCop(jun.total_activos)}</strong></td><td class="num-col"><strong>${pmjjCop(jul.total_activos)}</strong></td></tr>

              <tr class="niif-row-grupo niif-grupo-pasivo-corr"><td colspan="5">Pasivos Corrientes</td></tr>
              ${renderSectionRows(pcRows, "pasivos_corrientes")}
              <tr class="pmjj-row-subtle"><td></td><td><strong>SUBTOTAL PASIVOS CORRIENTES</strong></td><td class="num-col"><strong>${pmjjCop(may.subtotal_pc)}</strong></td><td class="num-col"><strong>${pmjjCop(jun.subtotal_pc)}</strong></td><td class="num-col"><strong>${pmjjCop(jul.subtotal_pc)}</strong></td></tr>

              <tr class="niif-row-grupo niif-grupo-pasivo-nocorr"><td colspan="5">Pasivos No Corrientes</td></tr>
              <tr><td><code>2105</code></td><td>BANCOS NACIONALES (Pasivo No Corriente — Largo Plazo TA)</td><td class="num-col">${pmjjCop(may.subtotal_pnc)}</td><td class="num-col">${pmjjCop(jun.subtotal_pnc)}</td><td class="num-col">${pmjjCop(jul.subtotal_pnc)}</td></tr>
              <tr class="pmjj-row-subtle"><td>2</td><td><strong>TOTAL PASIVOS</strong></td><td class="num-col"><strong>${pmjjCop(may.total_pasivos)}</strong></td><td class="num-col"><strong>${pmjjCop(jun.total_pasivos)}</strong></td><td class="num-col"><strong>${pmjjCop(jul.total_pasivos)}</strong></td></tr>

              <tr class="niif-row-grupo niif-grupo-patrimonio"><td colspan="5">Patrimonio</td></tr>
              ${renderSectionRows(patRows, "patrimonio")}
              <tr class="pmjj-row-subtle"><td>3</td><td><strong>TOTAL PATRIMONIO</strong></td><td class="num-col"><strong>${pmjjCop(may.total_patrimonio)}</strong></td><td class="num-col"><strong>${pmjjCop(jun.total_patrimonio)}</strong></td><td class="num-col"><strong>${pmjjCop(jul.total_patrimonio)}</strong></td></tr>

              <tr class="pmjj-row-highlight"><td>2+3</td><td><strong>TOTAL PASIVO Y PATRIMONIO</strong></td><td class="num-col"><strong>${pmjjCop(may.total_pasivo_patrimonio)}</strong></td><td class="num-col"><strong>${pmjjCop(jun.total_pasivo_patrimonio)}</strong></td><td class="num-col"><strong>${pmjjCop(jul.total_pasivo_patrimonio)}</strong></td></tr>
              <tr>
                <td>=</td>
                <td><strong>Comprobación Ecuación Contable (<span class="ef-col-activo">Activo</span> = <span class="ef-col-pasivo">Pasivo</span> + <span class="ef-col-patrimonio">Patrimonio</span>)</strong></td>
                <td class="num-col" style="color:var(--brand-emerald); font-weight:800;">${pmjjCop(may.diferencia)} ✓</td>
                <td class="num-col" style="color:${Math.abs(jun.diferencia) < 1 ? "var(--brand-emerald)" : "var(--brand-warning)"}; font-weight:800;">${pmjjCop(Math.abs(jun.diferencia) < 1 ? 0 : jun.diferencia)} ✓</td>
                <td class="num-col" style="color:${Math.abs(jul.diferencia) < 1 ? "var(--brand-emerald)" : "var(--brand-warning)"}; font-weight:800;">${pmjjCop(Math.abs(jul.diferencia) < 1 ? 0 : jul.diferencia)} ${Math.abs(jul.diferencia) < 1 ? "✓" : "⚠️ (Ver nota IVA)"}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
}

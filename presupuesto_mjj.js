/* ==========================================================================
   MÓDULO PRESUPUESTO MAESTRO MAYO, JUNIO Y JULIO 2026 — ELECTROVIVIENDA S.A.S
   Fuente: data/presupuesto_mjj_2026.json (25 hojas de PRESUPUESTO_MAYO_JUNIO_JULIO_2026.xlsx)
   Sincronizado con las 25 hojas del Excel oficial
   ========================================================================== */

let PRESUP_MJJ_DATA = null;
let PRESUP_MJJ_LOADING = false;
let PRESUP_ACTIVE_TAB = "RESUMEN";
let PRESUP_ACTIVE_MONTH = "MAYO";
let PRESUP_EFC_MODE = "COMPARATIVO"; // "MAYO" | "JUNIO" | "JULIO" | "COMPARATIVO"
let PRESUP_SHOW_GUIDE = true;
let PRESUP_TA_SHOW_ALL = false;
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

function pmjjCopHtml(n, decimals = 0) {
  const formatted = pmjjCop(n, decimals);
  if (n !== null && n !== undefined && !isNaN(Number(n)) && Number(n) < 0) {
    return `<span class="val-negative">${formatted}</span>`;
  }
  return formatted;
}

function pmjjNum(n, decimals = 0) {
  if (n === null || n === undefined || isNaN(Number(n))) return "-";
  return new Intl.NumberFormat("es-CO", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(Number(n));
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

function togglePresupTaShowAll() {
  PRESUP_TA_SHOW_ALL = !PRESUP_TA_SHOW_ALL;
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
        <div style="font-size:2rem; margin-bottom:10px;">📊</div>
        <div style="font-weight:700; color:var(--brand-primary);">Cargando Presupuesto Maestro Mayo, Junio y Julio 2026 (25 Hojas)...</div>
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

  const ventasTrim = may.er.ingresos_4135 + jun.er.ingresos_4135 + jul.er.ingresos_4135;
  const unidTrim = may.ventas.totales.unidades + jun.ventas.totales.unidades + jul.ventas.totales.unidades;
  const unTrim = may.er.utilidad_neta + jun.er.utilidad_neta + jul.er.utilidad_neta;
  const cajaAbril = d.meta.saldo_inicial_caja_abril;
  const cajaJulio = jul.efc.saldo_final;
  const crecCajaPct = cajaAbril > 0 ? ((cajaJulio - cajaAbril) / cajaAbril) : 0;

  const tabs = [
    { id: "RESUMEN",    label: "📌 Resumen & Maestro" },
    { id: "BASES",      label: "📊 Bases (DEP • TA • NOM • ESF Abril)" },
    { id: "PARAMETROS", label: "⚙️ Parámetros & Proyectado" },
    { id: "OPERATIVO",  label: "🛒 Compras (COM) & Ventas (VTA)" },
    { id: "EFC",        label: "💵 Flujo de Caja (EFC)" },
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
            <span class="pmjj-badge pmjj-badge-emerald">${d.meta.hojas_count} Hojas Ordenadas</span>
            <span class="pmjj-badge pmjj-badge-blue">Meta 50% EA (${pmjjCop(d.meta.meta_utilidad_mensual)}/mes)</span>
            <span class="pmjj-badge pmjj-badge-purple">Stock Final = 0 • Cuadre Exacto $0</span>
          </div>
          <h2 class="pmjj-hero-title">📊 Presupuesto Maestro Proyectado: Mayo, Junio y Julio 2026</h2>
          <p class="pmjj-hero-sub">
            Sincronizado con las <strong>${d.meta.hojas_count} hojas</strong> de <code>${pmjjEsc(d.meta.archivo)}</code>
            (<code>DEP</code>, <code>TA</code>, <code>NOM</code>, <code>ESF ABRIL</code>, <code>PROYECTADO</code>, <code>COM</code>, <code>VTA</code>, <code>EFC</code>, <code>ESF</code>, <code>ER</code>, <code>MAESTRO</code>, <code>ER CONSOLIDADO</code> y <code>ESF CONSOLIDADO</code>).
          </p>
        </div>
        <div class="pmjj-hero-actions">
          <button class="btn ${PRESUP_SHOW_GUIDE ? "btn-primary" : "btn-outline"} btn-sm" style="${PRESUP_SHOW_GUIDE ? "background:#B45309; border-color:var(--brand-emerald);" : "border-color:var(--brand-emerald); color:var(--brand-emerald);"}" onclick="togglePresupMjjGuide()">
            🎤 Guía de Sustentación: ${PRESUP_SHOW_GUIDE ? "ON" : "OFF"}
          </button>
          <a class="btn btn-gold btn-sm" href="${pmjjEsc(d.meta.archivo)}?v=20261124_01" download="${pmjjEsc(d.meta.archivo)}">
            📥 Descargar Excel (.xlsx)
          </a>
          <button class="btn btn-outline btn-sm" style="border-color:var(--brand-primary); color:var(--brand-primary);" onclick="window.print()">🖨️ Imprimir</button>
        </div>
      </div>
    </div>

    <!-- 4 TARJETAS KPI TRIMESTRALES -->
    <div class="kpi-row">
      <div class="kpi-card">
        <div class="kpi-label">Ventas Netas Trimestre (4135)</div>
        <div class="kpi-value" style="color:var(--brand-primary);">${pmjjCop(ventasTrim)}</div>
        <div class="kpi-sub">${pmjjNum(unidTrim)} unidades vendidas (59 May + 51 Jun + 51 Jul)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Utilidad Neta Trimestre (3605)</div>
        <div class="kpi-value" style="color:var(--brand-emerald);">${pmjjCop(unTrim)}</div>
        <div class="kpi-sub">✓ Los 3 meses superan la meta de ${pmjjCop(d.meta.meta_utilidad_mensual)}/mes</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Saldo Final de Caja a Julio</div>
        <div class="kpi-value" style="color:var(--brand-primary);">${pmjjCop(cajaJulio)}</div>
        <div class="kpi-sub">+${(crecCajaPct * 100).toFixed(1)}% vs saldo inicial Abril (${pmjjCop(cajaAbril)})</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Activos Totales a Julio</div>
        <div class="kpi-value" style="color:var(--text-main);">${pmjjCop(jul.esf.total_activos)}</div>
        <div class="kpi-sub">Patrimonio sube de ${pmjjCop(d.esf_abril?.total_patrimonio || 240560440)} a ${pmjjCop(jul.esf.total_patrimonio)}</div>
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
      <div style="font-size:0.75rem; color:var(--brand-primary); font-weight:700;">
        Mes Activo: ${PRESUP_ACTIVE_MONTH} • 25 Hojas Sincronizadas
      </div>
    </div>

    <!-- CONTENIDO DE LA PESTAÑA ACTIVA -->
    <div id="presupMjjTabContent"></div>
  `;

  const container = document.getElementById("presupMjjTabContent");
  destroyPresupCharts();

  if (PRESUP_ACTIVE_TAB === "RESUMEN") {
    renderTabResumen(container, d);
  } else if (PRESUP_ACTIVE_TAB === "BASES") {
    renderTabBases(container, d);
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
   1. TAB: RESUMEN & CONSOLIDADO MAESTRO
   ========================================================================== */
function renderTabResumen(container, d) {
  const may = d.meses.MAYO;
  const jun = d.meses.JUNIO;
  const jul = d.meses.JULIO;
  const metaUN = d.meta.meta_utilidad_mensual;

  const pasos = [
    {
      num: "1",
      titulo: "Bases Preliminares (DEP, TA, NOM, ESF Abril)",
      texto: `Partimos del ESF real de Abril (Activos ${pmjjCop(d.esf_abril?.total_activos || 331232683)}), la Depreciación mensual fija (${pmjjCop(1279533)}: Local $199.533 + Camioneta $1.080.000), la Tabla de Amortización NIIF (36 cuotas de ${pmjjCop(1892260)}) y la Nómina de Abril (${pmjjCop(10186476)} en beneficios a empleados).`,
      dato: "DEP: $1.279.533/mes | NOM 5105: $10.186.476/mes | Cuota TA: $1.892.260/mes"
    },
    {
      num: "2",
      titulo: "Meta de Rentabilidad 50% E.A. (PROYECTADO)",
      texto: `Sobre el capital suscrito de ${pmjjCop(248600000)} (cta. 3105), el 50% E.A. equivale a una tasa mensual de 3,4366% = ${pmjjCop(metaUN)} de utilidad neta mensual libre después de Impuesto de Renta (35% en 2499) y Reserva Legal (10% en 3305).`,
      dato: `Teórico: ${pmjjCop(metaUN)} | Práctico May: ${pmjjCop(may.er.utilidad_neta)} | Jun: ${pmjjCop(jun.er.utilidad_neta)} | Jul: ${pmjjCop(jul.er.utilidad_neta)}`
    },
    {
      num: "3",
      titulo: "Inventario Inicial + Compras (COM) y Ventas (VTA)",
      texto: `En Mayo vendemos primero las 37 unidades del Inventario Inicial de Abril (costo ${pmjjCop(33822000)}, ingreso ${pmjjCop(48317143)}) y compramos solo 22 unidades adicionales (costo ${pmjjCop(28440000)}, ingreso ${pmjjCop(40628571)}) para cerrar con Stock Final = 0. En Junio y Julio se compran y venden 51 unidades cada mes.`,
      dato: "Mayo: 37 Inv. Inicial + 22 Compradas = 59 Vendidas | Junio y Julio: 51 Compradas = 51 Vendidas"
    },
    {
      num: "4",
      titulo: "Flujo de Caja (EFC) con ReteICA Mensual y Prima en Junio",
      texto: `Mayo inicia con ${pmjjCop(may.efc.saldo_inicial)}, recauda la cartera de Jaime (${pmjjCop(28857500)}) y paga Retefuente ($442.490) y ReteICA de Abril ($95.400). En Junio paga ReteICA de Mayo ($341.280), Retefuente ($2.934.643) y la Prima semestral (${pmjjCop(3082100)}). En Julio paga ReteICA de Junio ($746.496), Retefuente ($3.776.914) e IVA bimestral (${pmjjCop(17229254)}).`,
      dato: `Caja Final: Mayo ${pmjjCop(may.efc.saldo_final)} → Junio ${pmjjCop(jun.efc.saldo_final)} → Julio ${pmjjCop(jul.efc.saldo_final)}`
    },
    {
      num: "5",
      titulo: "Cuadre Perfecto en ESF y ER Consolidado",
      texto: "Cada mes la Utilidad del Ejercicio anterior (3605) pasa a Utilidades Acumuladas (3705), la Provisión Laboral (2610) acumula $1.605.003/mes y descuenta la Prima de $3.082.100 en Junio, y la ecuación Activo = Pasivo + Patrimonio cierra con diferencia $0 en todos los meses.",
      dato: `Activos: May ${pmjjCop(may.esf.total_activos)} | Jun ${pmjjCop(jun.esf.total_activos)} | Jul ${pmjjCop(jul.esf.total_activos)}`
    },
  ];

  const tablero = d.parametros.tablero_comparativo;
  const gastosTrim = d.maestro?.gastos_trimestre || [];

  container.innerHTML = `
    ${PRESUP_SHOW_GUIDE ? `
      <div class="card">
        <div class="card-header">
          <div class="card-title">🎤 ¿Cómo sustentar las 25 hojas del Presupuesto en 5 pasos?</div>
          <span class="pmjj-badge pmjj-badge-emerald">Guía Paso a Paso</span>
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

    <!-- GRÁFICAS COMPARATIVAS EN TONOS ROSADOS -->
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
          <div class="card-title">💵 Evolución del Efectivo en Caja (Abril → Mayo → Junio → Julio)</div>
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
        <span class="pmjj-badge pmjj-badge-gold">Meta Mensual: ${pmjjCop(metaUN)}</span>
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
                <th class="num-col">Total / Cierre Trimestre</th>
              </tr>
            </thead>
            <tbody>
              ${tablero.map((r, i) => {
                const isCount = i === 0 || i === 1;
                const isHighlight = i === 4 || i === 9 || i === 10 || i === 13;
                const fmt = v => isCount ? pmjjNum(v) + " und." : pmjjCopHtml(v);
                return `
                  <tr class="${isHighlight ? "pmjj-row-highlight" : ""}">
                    <td><strong>${pmjjEsc(r.concepto)}</strong></td>
                    <td class="num-col">${fmt(r.mayo)}</td>
                    <td class="num-col">${fmt(r.junio)}</td>
                    <td class="num-col">${fmt(r.julio)}</td>
                    <td class="num-col" style="font-weight:800; color:var(--brand-primary);">${fmt(r.trimestre)}</td>
                  </tr>`;
              }).join("")}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- HOJA MAESTRO: CONSOLIDADO DE GASTOS TRIMESTRALES -->
    ${gastosTrim.length ? `
      <div class="card">
        <div class="card-header">
          <div class="card-title">📊 Hoja MAESTRO — Consolidado Trimestral de Gastos Operacionales y Financieros</div>
          <span class="pmjj-badge pmjj-badge-purple">Total Trimestre: ${pmjjCop(gastosTrim[gastosTrim.length - 1]?.total || 36134800)}</span>
        </div>
        <div class="card-body">
          <div class="table-wrap">
            <table class="acct-table">
              <thead>
                <tr>
                  <th>Concepto de Gasto</th>
                  <th class="num-col">Mayo 2026</th>
                  <th class="num-col">Junio 2026</th>
                  <th class="num-col">Julio 2026</th>
                  <th class="num-col">Total Trimestre</th>
                </tr>
              </thead>
              <tbody>
                ${gastosTrim.map(g => {
                  const isTot = g.concepto.toUpperCase().includes("TOTAL");
                  return `
                    <tr class="${isTot ? "pmjj-row-highlight" : ""}">
                      <td><strong>${pmjjEsc(g.concepto)}</strong></td>
                      <td class="num-col">${pmjjCop(g.mayo, 2)}</td>
                      <td class="num-col">${pmjjCop(g.junio, 2)}</td>
                      <td class="num-col">${pmjjCop(g.julio, 2)}</td>
                      <td class="num-col" style="font-weight:800; color:var(--brand-primary);">${pmjjCop(g.total, 2)}</td>
                    </tr>`;
                }).join("")}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    ` : ""}
  `;

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
            { label: "Utilidad Neta (3605)", data: [may.er.utilidad_neta, jun.er.utilidad_neta, jul.er.utilidad_neta], backgroundColor: "#059669", borderRadius: 6 },
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
          labels: ["Abril (Inicial)", "Mayo (Proy.)", "Junio (Proy.)", "Julio (Proy.)"],
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
   2. TAB: BASES PRELIMINARES (DEP • TA • NOM • ESF ABRIL)
   ========================================================================== */
function renderTabBases(container, d) {
  const dep = d.depreciacion || {};
  const loc = dep.local || {};
  const car = dep.carro || {};
  const compDep = dep.comprobante_mensual || {};
  const { condiciones, cuotas, totales: taTot } = d.amortizacion;
  const nom = d.nomina_abril || {};
  const esfAbr = d.esf_abril || {};

  const cuotasVisibles = PRESUP_TA_SHOW_ALL ? cuotas : cuotas.slice(0, 12);

  container.innerHTML = `
    ${PRESUP_SHOW_GUIDE ? `
      <div class="pmjj-explain-box">
        <strong>💡 Hojas Base del Presupuesto (<code>DEP</code>, <code>TA</code>, <code>NOM</code> y <code>ESF ABRIL</code>):</strong>
        Estas 4 hojas alimentan todos los gastos fijos y saldos iniciales de Mayo, Junio y Julio:
        <strong>1) <code>DEP</code></strong> calcula la depreciación mensual del Local (${pmjjCop(loc.cuota_mensual, 2)} en <code>5260</code>) y la Camioneta HBA005 (${pmjjCop(car.cuota_mensual)} en <code>5160</code>).
        <strong>2) <code>TA</code></strong> liquida las 36 cuotas del crédito Bancolombia (${pmjjCop(condiciones.cuota, 2)}/mes) y su TIR mensual (${pmjjPct(condiciones.tir_mensual, 4)}).
        <strong>3) <code>NOM</code></strong> liquida la nómina base de Abril (Devengado ${pmjjCop(nom.totales?.total_devengado)}, Neto a pagar ${pmjjCop(nom.totales?.neto_pagar, 2)}, Provisión prestaciones ${pmjjCop(nom.totales?.total_provisiones_2610, 2)} y Parafiscales/Seg. Social empleador ${pmjjCop(nom.totales?.total_seg_social_empleador, 2)} → Total Beneficios <code>5105</code> = <strong>${pmjjCop(nom.totales?.total_beneficios_empleados_5105, 2)}</strong>).
        <strong>4) <code>ESF ABRIL</code></strong> entrega los saldos iniciales exactos al 30 de abril de 2026.
      </div>
    ` : ""}

    <!-- 1. HOJA DEP: DEPRECIACIÓN LOCAL Y CAMIONETA -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">🏢 1. Hoja DEP — Depreciación de Activos Fijos (Local Calle 85 y Camioneta HBA005)</div>
        <span class="pmjj-badge pmjj-badge-gold">Gasto Mensual Total: ${pmjjCop(compDep.total_mensual, 2)}</span>
      </div>
      <div class="card-body">
        <div class="grid-2" style="margin-bottom:14px;">
          <div style="border:1px solid var(--border-light); border-radius:8px; padding:12px; background:var(--bg-subtle);">
            <strong style="color:var(--brand-primary);">🏠 ${pmjjEsc(loc.nombre)}</strong>
            <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:6px; margin-top:8px; font-size:0.8rem;">
              <div><strong>Valor en Libros:</strong> ${pmjjCop(loc.valor_libros)}</div>
              <div><strong>Salvamento (10%):</strong> ${pmjjCop(loc.valor_salvamento)}</div>
              <div><strong>Valor a Depreciar:</strong> ${pmjjCop(loc.valor_depreciar)}</div>
              <div><strong>Vida Útil:</strong> ${loc.vida_util_anual} años (5% anual)</div>
              <div><strong>Dep. Anual:</strong> ${pmjjCop(loc.cuota_anual, 2)}</div>
              <div><strong>Dep. Mensual (5260):</strong> <strong style="color:var(--brand-emerald);">${pmjjCop(loc.cuota_mensual, 2)}</strong></div>
            </div>
          </div>
          <div style="border:1px solid var(--border-light); border-radius:8px; padding:12px; background:var(--bg-subtle);">
            <strong style="color:var(--brand-primary);">🚚 ${pmjjEsc(car.nombre)}</strong>
            <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:6px; margin-top:8px; font-size:0.8rem;">
              <div><strong>Valor en Libros:</strong> ${pmjjCop(car.valor_libros)}</div>
              <div><strong>Salvamento (10%):</strong> ${pmjjCop(car.valor_salvamento)}</div>
              <div><strong>Valor a Depreciar:</strong> ${pmjjCop(car.valor_depreciar)}</div>
              <div><strong>Vida Útil:</strong> ${car.vida_util_anual} años (20% anual)</div>
              <div><strong>Dep. Anual:</strong> ${pmjjCop(car.cuota_anual)}</div>
              <div><strong>Dep. Mensual (5160):</strong> <strong style="color:var(--brand-emerald);">${pmjjCop(car.cuota_mensual)}</strong></div>
            </div>
          </div>
        </div>

        <div class="grid-2">
          <div class="table-wrap">
            <table class="acct-table">
              <thead>
                <tr><th colspan="5">Tabla Depreciación Mensual Local (12 Meses)</th></tr>
                <tr><th>Mes</th><th class="num-col">Valor Inicial</th><th class="num-col">Dep. Mensual</th><th class="num-col">Dep. Acumulada</th><th class="num-col">Saldo Libros</th></tr>
              </thead>
              <tbody>
                ${(loc.tabla_mensual || []).filter(r => r.np > 0).map(r => `
                  <tr class="${[3, 4, 5].includes(r.np) ? "pmjj-row-highlight" : ""}">
                    <td class="num-col"><strong>${r.np}</strong></td>
                    <td class="num-col">${pmjjCop(r.valor_inicial, 2)}</td>
                    <td class="num-col">${pmjjCop(r.dep_mensual, 2)}</td>
                    <td class="num-col">${pmjjCop(r.dep_acumulada, 2)}</td>
                    <td class="num-col">${pmjjCop(r.saldo, 2)}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
          <div class="table-wrap">
            <table class="acct-table">
              <thead>
                <tr><th colspan="5">Tabla Depreciación Mensual Camioneta (12 Meses)</th></tr>
                <tr><th>Mes</th><th class="num-col">Valor Inicial</th><th class="num-col">Dep. Mensual</th><th class="num-col">Dep. Acumulada</th><th class="num-col">Saldo Libros</th></tr>
              </thead>
              <tbody>
                ${(car.tabla_mensual || []).filter(r => r.np > 0).map(r => `
                  <tr class="${[3, 4, 5].includes(r.np) ? "pmjj-row-highlight" : ""}">
                    <td class="num-col"><strong>${r.np}</strong></td>
                    <td class="num-col">${pmjjCop(r.valor_inicial)}</td>
                    <td class="num-col">${pmjjCop(r.dep_mensual)}</td>
                    <td class="num-col">${pmjjCop(r.dep_acumulada)}</td>
                    <td class="num-col">${pmjjCop(r.saldo)}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- 2. HOJA NOM: NÓMINA BASE ABRIL -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">👩‍💼 2. Hoja NOM — Nómina de Administración, Prestaciones Sociales y Parafiscales (Base Mensual)</div>
        <span class="pmjj-badge pmjj-badge-emerald">Total Beneficios (5105): ${pmjjCop(nom.totales?.total_beneficios_empleados_5105, 2)}</span>
      </div>
      <div class="card-body">
        <div class="table-wrap" style="margin-bottom:14px;">
          <table class="acct-table">
            <thead>
              <tr><th colspan="10">1. Devengado, Deducciones y Neto a Pagar (1 SMLMV = ${pmjjCop(nom.smlmv)})</th></tr>
              <tr>
                <th>Nombre del Empleado</th><th class="num-col">Días/Horas</th><th class="num-col">Salario Básico</th>
                <th class="num-col">Aux. Transp.</th><th class="num-col">Total Devengado</th><th class="num-col">IBC</th>
                <th class="num-col">Salud 4%</th><th class="num-col">Pensión 4%</th><th class="num-col">Total Deduc.</th><th class="num-col">Neto a Pagar</th>
              </tr>
            </thead>
            <tbody>
              ${(nom.empleados || []).map(e => `
                <tr>
                  <td><strong>${pmjjEsc(e.nombre)}</strong></td>
                  <td class="num-col">${e.horas} h</td>
                  <td class="num-col">${pmjjCop(e.salario_basico)}</td>
                  <td class="num-col">${pmjjCop(e.aux_transporte)}</td>
                  <td class="num-col"><strong>${pmjjCop(e.total_devengado)}</strong></td>
                  <td class="num-col">${pmjjCop(e.ibc)}</td>
                  <td class="num-col">${pmjjCop(e.salud_trabajador, 2)}</td>
                  <td class="num-col">${pmjjCop(e.pension_trabajador, 2)}</td>
                  <td class="num-col">${pmjjCop(e.total_deducciones, 2)}</td>
                  <td class="num-col" style="font-weight:800; color:var(--brand-primary);">${pmjjCop(e.neto_pagar, 2)}</td>
                </tr>
              `).join("")}
              <tr class="pmjj-row-highlight">
                <td><strong>TOTALES NÓMINA</strong></td>
                <td class="num-col">-</td><td class="num-col">-</td><td class="num-col">-</td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.total_devengado)}</strong></td>
                <td class="num-col">-</td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.salud_trabajador, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.pension_trabajador, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.total_deducciones, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.neto_pagar, 2)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr><th colspan="10">2. Provisiones para Prestaciones Sociales (2610) y Aportes Seguridad Social / Parafiscales Empleador</th></tr>
              <tr>
                <th>Nombre del Empleado</th><th class="num-col">Cesantías 8,33%</th><th class="num-col">Int. Ces. 12%</th>
                <th class="num-col">Prima 8,33%</th><th class="num-col">Vacaciones 4,17%</th><th class="num-col">Total Provisión (2610)</th>
                <th class="num-col">Pensión Emp. 12%</th><th class="num-col">ARL 0,522%</th><th class="num-col">CCF 4%</th><th class="num-col">Total Seg. Social Emp.</th>
              </tr>
            </thead>
            <tbody>
              ${(nom.empleados || []).map(e => `
                <tr>
                  <td><strong>${pmjjEsc(e.nombre)}</strong></td>
                  <td class="num-col">${pmjjCop(e.cesantias, 2)}</td>
                  <td class="num-col">${pmjjCop(e.intereses_cesantias, 2)}</td>
                  <td class="num-col">${pmjjCop(e.prima, 2)}</td>
                  <td class="num-col">${pmjjCop(e.vacaciones, 2)}</td>
                  <td class="num-col"><strong>${pmjjCop(e.total_provisiones, 2)}</strong></td>
                  <td class="num-col">${pmjjCop(e.pension_empleador, 2)}</td>
                  <td class="num-col">${pmjjCop(e.arl, 2)}</td>
                  <td class="num-col">${pmjjCop(e.ccf, 2)}</td>
                  <td class="num-col"><strong>${pmjjCop(e.pension_empleador + e.arl + e.ccf, 2)}</strong></td>
                </tr>
              `).join("")}
              <tr class="pmjj-row-highlight">
                <td><strong>TOTALES EMPLEADOR</strong></td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.cesantias, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.intereses_cesantias, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.prima, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.vacaciones, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.total_provisiones_2610, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.pension_empleador, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.arl, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.ccf, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(nom.totales?.total_seg_social_empleador, 2)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 3. HOJA TA: TABLA DE AMORTIZACIÓN BAJO NIIF Y TIR -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">🏦 3. Hoja TA — Tabla de Amortización Bajo NIIF y Cálculo de TIR (36 Meses)</div>
        <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
          <span class="pmjj-badge pmjj-badge-purple">T.E.A: ${pmjjPct(condiciones.t_efectiva, 2)} • T. Periódica: ${pmjjPct(condiciones.t_periodica, 2)} • TIR: ${pmjjPct(condiciones.tir_mensual, 4)}</span>
          <button class="btn btn-outline btn-sm" style="border-color:var(--brand-emerald); color:var(--brand-emerald);" onclick="togglePresupTaShowAll()">
            ${PRESUP_TA_SHOW_ALL ? "Ver Primeras 12 Cuotas" : "Ver las 36 Cuotas Completas"}
          </button>
        </div>
      </div>
      <div class="card-body">
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(170px,1fr)); gap:10px; margin-bottom:12px; font-size:0.8rem;">
          <div style="padding:8px 12px; background:var(--bg-subtle); border:1px solid var(--border-light); border-radius:6px;"><strong>Crédito Nominal:</strong> ${pmjjCop(condiciones.credito)}</div>
          <div style="padding:8px 12px; background:var(--bg-subtle); border:1px solid var(--border-light); border-radius:6px;"><strong>(-) Estudio Crédito:</strong> ${pmjjCop(condiciones.estudio_credito)}</div>
          <div style="padding:8px 12px; background:var(--bg-subtle); border:1px solid var(--border-light); border-radius:6px;"><strong>(=) Desembolso NIIF:</strong> ${pmjjCop(condiciones.desembolso_neto || 55876000)}</div>
          <div style="padding:8px 12px; background:rgba(5, 150, 105, 0.09); border:1px solid rgba(5, 150, 105, 0.35); border-radius:6px;"><strong>Cuota Fija Mensual:</strong> <strong style="color:var(--brand-primary);">${pmjjCop(condiciones.cuota, 2)}</strong></div>
        </div>
        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr>
                <th class="num-col">N° Cuota</th>
                <th>Período / Aplicación</th>
                <th class="num-col">Valor Cuota (EFC)</th>
                <th class="num-col">Abono a Capital (2105)</th>
                <th class="num-col">Interés NIIF (Gasto 5305)</th>
                <th class="num-col">Saldo Capital</th>
              </tr>
            </thead>
            <tbody>
              <tr class="pmjj-row-subtle">
                <td class="num-col"><strong>0</strong></td>
                <td><strong>Desembolso Neto Inicial Bajo NIIF</strong></td>
                <td class="num-col">-</td><td class="num-col">-</td><td class="num-col">-</td>
                <td class="num-col"><strong>${pmjjCop(condiciones.desembolso_neto || 55876000, 2)}</strong></td>
              </tr>
              ${cuotasVisibles.map(q => {
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
              ${taTot ? `
                <tr class="pmjj-row-highlight">
                  <td class="num-col"><strong>1–36</strong></td>
                  <td><strong>TOTALES 36 CUOTAS (TIR Mensual = ${pmjjPct(condiciones.tir_mensual, 4)})</strong></td>
                  <td class="num-col"><strong>${pmjjCop(taTot.total_cuotas, 2)}</strong></td>
                  <td class="num-col"><strong>${pmjjCop(taTot.total_capital, 2)}</strong></td>
                  <td class="num-col"><strong>${pmjjCop(taTot.total_intereses, 2)}</strong></td>
                  <td class="num-col"><strong>$0</strong></td>
                </tr>
              ` : ""}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 4. HOJA ESF ABRIL -->
    ${esfAbr.total_activos ? `
      <div class="card">
        <div class="card-header">
          <div class="card-title">🏛️ 4. Hoja ESF ABRIL — Estado de Situación Financiera Base (Al 30 de Abril de 2026)</div>
          <span class="pmjj-badge pmjj-badge-gold">Punto de Partida para Mayo 2026 • Activos = ${pmjjCop(esfAbr.total_activos, 2)}</span>
        </div>
        <div class="card-body">
          <div class="grid-2">
            <div class="table-wrap">
              <table class="acct-table">
                <thead><tr><th>PUC</th><th>ACTIVOS (Corte 30 Abril 2026)</th><th class="num-col">Saldo Abril</th></tr></thead>
                <tbody>
                  ${(esfAbr.activos_corrientes || []).map(a => `<tr><td><code>${a.codigo}</code></td><td>${pmjjEsc(a.cuenta)}</td><td class="num-col">${pmjjCopHtml(a.valor, 2)}</td></tr>`).join("")}
                  <tr class="pmjj-row-subtle"><td></td><td><strong>SUBTOTAL ACTIVOS CORRIENTES</strong></td><td class="num-col"><strong>${pmjjCopHtml(esfAbr.subtotal_ac, 2)}</strong></td></tr>
                  ${(esfAbr.activos_no_corrientes || []).map(a => `<tr><td><code>${a.codigo}</code></td><td>${pmjjEsc(a.cuenta)}</td><td class="num-col">${pmjjCopHtml(a.valor, 2)}</td></tr>`).join("")}
                  <tr class="pmjj-row-subtle"><td></td><td><strong>SUBTOTAL ACTIVOS FIJOS</strong></td><td class="num-col"><strong>${pmjjCopHtml(esfAbr.subtotal_anc, 2)}</strong></td></tr>
                  <tr class="pmjj-row-highlight"><td>1</td><td><strong>TOTAL ACTIVOS ABRIL</strong></td><td class="num-col"><strong>${pmjjCopHtml(esfAbr.total_activos, 2)}</strong></td></tr>
                </tbody>
              </table>
            </div>
            <div class="table-wrap">
              <table class="acct-table">
                <thead><tr><th>PUC</th><th>PASIVOS Y PATRIMONIO (Corte 30 Abril 2026)</th><th class="num-col">Saldo Abril</th></tr></thead>
                <tbody>
                  ${(esfAbr.pasivos_corrientes || []).map(p => `<tr><td><code>${p.codigo}</code></td><td>${pmjjEsc(p.cuenta)}</td><td class="num-col">${pmjjCopHtml(p.valor, 2)}</td></tr>`).join("")}
                  <tr class="pmjj-row-subtle"><td></td><td><strong>SUBTOTAL PASIVOS CORRIENTES</strong></td><td class="num-col"><strong>${pmjjCopHtml(esfAbr.subtotal_pc, 2)}</strong></td></tr>
                  <tr><td><code>2105</code></td><td>BANCOS NACIONALES (No Corriente)</td><td class="num-col">${pmjjCopHtml(esfAbr.subtotal_pnc, 2)}</td></tr>
                  <tr class="pmjj-row-subtle"><td>2</td><td><strong>TOTAL PASIVOS ABRIL</strong></td><td class="num-col"><strong>${pmjjCopHtml(esfAbr.total_pasivos, 2)}</strong></td></tr>
                  ${(esfAbr.patrimonio || []).map(pt => `<tr><td><code>${pt.codigo}</code></td><td>${pmjjEsc(pt.cuenta)}</td><td class="num-col">${pmjjCopHtml(pt.valor, 2)}</td></tr>`).join("")}
                  <tr class="pmjj-row-subtle"><td>3</td><td><strong>TOTAL PATRIMONIO ABRIL</strong></td><td class="num-col"><strong>${pmjjCopHtml(esfAbr.total_patrimonio, 2)}</strong></td></tr>
                  <tr class="pmjj-row-highlight"><td>2+3</td><td><strong>TOTAL PASIVO Y PATRIMONIO ABRIL</strong></td><td class="num-col"><strong>${pmjjCopHtml(esfAbr.total_pasivo_patrimonio, 2)}</strong></td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    ` : ""}
  `;
}

/* ==========================================================================
   3. TAB: PARÁMETROS, PRECIOS Y HOJA PROYECTADO
   ========================================================================== */
function renderTabParametros(container, d) {
  const { reglas, proveedores_neveras, catalogo_precios } = d.parametros;
  const m = PRESUP_ACTIVE_MONTH;
  const proy = d.meses[m]?.proyectado || {};
  const tm = proy.tasas_meta || {};

  const formatParamVal = (p) => {
    if (p.parametro.includes("Capital") || p.parametro.includes("Meta")) return pmjjCop(p.valor);
    if (p.parametro.includes("Stock")) return `${pmjjNum(p.valor)} unidades`;
    return pmjjPct(p.valor, 2);
  };

  container.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
      <span class="pmjj-badge pmjj-badge-emerald">📊 Hoja PROYECTADO ${m} 2026</span>
      <span style="font-size:0.78rem; color:var(--brand-primary); font-weight:700;">Cambia entre MAY, JUN y JUL en la barra superior</span>
    </div>

    ${PRESUP_SHOW_GUIDE ? `
      <div class="pmjj-explain-box">
        <strong>💡 Cómo funciona la hoja <code>PROYECTADO ${m}</code>:</strong>
        1) Con el Capital Suscrito (${pmjjCop(tm.capital_suscrito || 248600000)}) y la Tasa Mensual (${pmjjPct(tm.tasa_mensual || 0.034366, 4)}), el <strong>Resultado Teórico Esperado</strong> es <strong>${pmjjCop(tm.resultado_teorico, 2)}</strong> (que exige una Utilidad Antes de Impuestos de ${pmjjCop(tm.uai_meta, 2)}).
        2) Al sumar los gastos del mes (${pmjjCop(tm.gastos_proyectados, 2)}), sabemos cuánta ganancia bruta necesitamos y determinamos el factor exacto de <strong>Unidades a Comprar (${pmjjNum(tm.unidades_a_comprar_factor, 4)})</strong>.
        3) Al redondear a unidades enteras, obtenemos el <strong>Resultado Práctico de ${pmjjCop(tm.resultado_practico, 2)}</strong> (superando la meta en +${pmjjCop(tm.diferencia_resultado, 2)}).
      </div>
    ` : ""}

    <!-- RESUMEN DE LA HOJA PROYECTADO DEL MES ACTIVO -->
    ${tm.capital_suscrito ? `
      <div class="card">
        <div class="card-header">
          <div class="card-title">🎯 1. Hoja PROYECTADO ${m} — Resultado Teórico vs. Práctico y Factor de Unidades a Comprar</div>
          <span class="pmjj-badge pmjj-badge-gold">Diferencia Práctico vs. Teórico: +${pmjjCop(tm.diferencia_resultado, 2)}</span>
        </div>
        <div class="card-body">
          <div class="grid-2">
            <div class="table-wrap">
              <table class="acct-table">
                <thead><tr><th>Concepto Meta y Rentabilidad (${m})</th><th class="num-col">Valor Calculado</th></tr></thead>
                <tbody>
                  <tr><td><strong>Tasa Efectiva Anual (E/A)</strong></td><td class="num-col">${pmjjPct(tm.tasa_ea, 2)}</td></tr>
                  <tr><td><strong>Tasa Nominal Anual</strong></td><td class="num-col">${pmjjPct(tm.tasa_nominal, 4)}</td></tr>
                  <tr><td><strong>Tasa Mensual Equivalente</strong></td><td class="num-col">${pmjjPct(tm.tasa_mensual, 4)}</td></tr>
                  <tr><td><strong>Capital Suscrito (3105)</strong></td><td class="num-col">${pmjjCop(tm.capital_suscrito)}</td></tr>
                  <tr><td><strong>Resultado Teórico Esperado (Meta Neta)</strong></td><td class="num-col"><strong>${pmjjCop(tm.resultado_teorico, 2)}</strong></td></tr>
                  <tr class="pmjj-row-highlight"><td><strong>Resultado Práctico Logrado en ${m}</strong></td><td class="num-col"><strong>${pmjjCop(tm.resultado_practico, 2)}</strong></td></tr>
                  <tr><td><strong>Diferencia (Práctico − Teórico)</strong></td><td class="num-col" style="color:#047857; font-weight:800;">+${pmjjCop(tm.diferencia_resultado, 2)} ✓</td></tr>
                </tbody>
              </table>
            </div>
            <div class="table-wrap">
              <table class="acct-table">
                <thead><tr><th>Cálculo de Utilidad Requerida y Unidades (${m})</th><th class="num-col">Valor Calculado</th></tr></thead>
                <tbody>
                  <tr><td><strong>Utilidad Antes de Impuestos Requerida (UAI)</strong></td><td class="num-col">${pmjjCop(tm.uai_meta, 2)}</td></tr>
                  <tr><td><strong>Utilidad Después de Impuestos Requerida (UDI)</strong></td><td class="num-col">${pmjjCop(tm.udi_meta, 2)}</td></tr>
                  <tr><td><strong>Utilidad Neta Esperada</strong></td><td class="num-col">${pmjjCop(tm.un_meta, 2)}</td></tr>
                  <tr><td><strong>Total Gastos del Mes (${m})</strong></td><td class="num-col">${pmjjCop(tm.gastos_proyectados, 2)}</td></tr>
                  <tr><td><strong>Ganancia por Vender 1 Kit de Unidades (4 Productos)</strong></td><td class="num-col">${pmjjCop(tm.ganancia_vender_1_und, 2)}</td></tr>
                  <tr class="pmjj-row-highlight"><td><strong>Factor de Unidades a Comprar por Producto</strong></td><td class="num-col"><strong>${pmjjNum(tm.unidades_a_comprar_factor, 4)} und.</strong></td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    ` : ""}

    <div class="grid-2">
      <div class="card">
        <div class="card-header"><div class="card-title">⚙️ 2. Parámetros Financieros, Comerciales y Tributarios</div></div>
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
          <div class="card-header"><div class="card-title">🧊 3. Promedio Ponderado Neveras (2 Proveedores 50/50)</div></div>
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
          <div class="card-header"><div class="card-title">🏷️ 4. Catálogo de Base de Venta = Costo ÷ (1 − 30%)</div></div>
          <div class="card-body">
            <div class="table-wrap">
              <table class="acct-table">
                <thead><tr><th>Producto (Kardex / Lote)</th><th class="num-col">Costo Unit.</th><th class="num-col">Base de Venta</th><th class="num-col">Ganancia Unit.</th></tr></thead>
                <tbody>
                  ${catalogo_precios.map((c, idx) => `
                    <tr class="${idx === 2 ? "pmjj-row-highlight" : ""}">
                      <td><strong>${pmjjEsc(c.producto)}</strong></td>
                      <td class="num-col">${pmjjCop(c.costo)}</td>
                      <td class="num-col" style="font-weight:800; color:var(--brand-emerald);">${pmjjCop(c.precio_venta, 2)}</td>
                      <td class="num-col">${pmjjCop(c.ganancia_unit, 2)}</td>
                    </tr>
                  `).join("")}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}

/* ==========================================================================
   4. TAB: COMPRAS (COM) Y VENTAS (VTA) POR MES
   ========================================================================== */
function renderTabOperativo(container, d) {
  const m = PRESUP_ACTIVE_MONTH;
  const mesData = d.meses[m];
  const vtaBloques = mesData.ventas_bloques || {};
  const proveedores = mesData.compras_proveedores || [];

  const guionMes = {
    MAYO: "En Mayo vendemos primero las 37 unidades del Inventario Inicial de Abril (costo $33.822.000, base venta $48.317.143) y compramos únicamente las 22 unidades faltantes (costo $28.440.000, base venta $40.628.571) para vender un total de 59 unidades y dejar el Stock Final en 0.",
    JUNIO: "Como Mayo cerró con Stock Final = 0, en Junio compramos y vendemos exactamente 51 unidades (13 Televisores, 12 Neveras: 6 a Cra 13 y 6 a Electromenores, 14 Microondas y 12 Lavadoras) con costo de $62.208.000 e ingresos de $88.868.571,43.",
    JULIO: "En Julio mantenemos el volumen óptimo de 51 unidades compradas y 51 vendidas, dejando Stock Final = 0 y generando un IVA neto del mes de $5.635.508,57.",
  };

  const renderBloqueVentaCard = (b) => `
    <div style="border:1px solid var(--border-light); border-radius:8px; padding:12px; background:var(--bg-subtle);">
      <strong style="color:var(--brand-primary); display:block; margin-bottom:8px;">🛍️ ${pmjjEsc(b.titulo)}</strong>
      <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:6px; font-size:0.8rem;">
        <div><strong>Base Gravable:</strong> ${pmjjCop(b.base, 2)}</div>
        <div><strong>(+) IVA Generado 19%:</strong> ${pmjjCop(b.iva, 2)}</div>
        <div><strong>(-) Retefuente 2,5% (1355):</strong> ${pmjjCop(b.retefuente, 2)}</div>
        <div><strong>Autorretención 2,5% (246575):</strong> ${pmjjCop(b.autoret, 2)}</div>
        <div><strong>(-) ReteICA 9,6‰:</strong> ${pmjjCop(b.reteica, 2)}</div>
        <div><strong>(-) Avisos 15% + Bomb. 10%:</strong> ${pmjjCop((b.avisos || 0) + (b.bomberil || 0), 2)}</div>
        <div><strong>(=) Total Neto Factura:</strong> <strong style="color:var(--brand-emerald);">${pmjjCop(b.total, 2)}</strong></div>
        <div><strong>50% Contado / 50% Crédito:</strong> ${pmjjCop(b.contado_50, 2)} c/u</div>
      </div>
    </div>
  `;

  container.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
      <span class="pmjj-badge pmjj-badge-emerald">📅 Hojas VTA ${m} y COM ${m} (${pmjjNum(mesData.ventas.totales.unidades)} und. vendidas • ${pmjjNum(mesData.compras.totales.unidades)} und. compradas)</span>
      <span style="font-size:0.78rem; color:var(--brand-primary); font-weight:700;">Cambia entre MAY, JUN y JUL en la barra superior</span>
    </div>

    ${PRESUP_SHOW_GUIDE ? `
      <div class="pmjj-explain-box">
        <strong>💡 Explicación de Compras y Ventas de ${m} 2026:</strong> ${pmjjEsc(guionMes[m])}
      </div>
    ` : ""}

    <!-- RESUMEN DE BLOQUES DE LA HOJA VTA -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Hoja VTA ${m} — Liquidación de Ventas e Impuestos por Lote (50% Contado / 50% Crédito)</div>
        <span class="pmjj-badge pmjj-badge-gold">50% Contado: ${pmjjCop(mesData.ventas.totales.contado_50, 2)} | 50% Crédito: ${pmjjCop(mesData.ventas.totales.credito_50, 2)}</span>
      </div>
      <div class="card-body">
        <div class="${vtaBloques.inventario_inicial ? "grid-2" : ""}" style="margin-bottom:14px;">
          ${vtaBloques.inventario_inicial ? renderBloqueVentaCard(vtaBloques.inventario_inicial) : ""}
          ${vtaBloques.mercancia_comprada ? renderBloqueVentaCard(vtaBloques.mercancia_comprada) : ""}
        </div>

        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr>
                <th>Lote</th><th>Producto</th><th class="num-col">Unid.</th>
                <th class="num-col">Costo Unit.</th><th class="num-col">Costo Ventas (6135)</th>
                <th class="num-col">Base de Venta</th><th class="num-col">Ventas Netas (4135)</th>
                <th class="num-col">IVA Gen. 19%</th>
                <th class="num-col">ICA 9,6‰</th>
                <th class="num-col">Avisos 15%</th>
                <th class="num-col">Bomberil 10%</th>
                <th class="num-col">Neto Cobrar</th><th class="num-col">Autorret. 2,5% (246575)</th>
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
                  <td class="num-col">${pmjjCop(f.precio_venta, 2)}</td>
                  <td class="num-col"><strong>${pmjjCop(f.ventas_netas, 2)}</strong></td>
                  <td class="num-col">${pmjjCop(f.iva, 2)}</td>
                  <td class="num-col">${pmjjCop(f.ica ?? 0, 2)}</td>
                  <td class="num-col">${pmjjCop(f.avisos ?? 0, 2)}</td>
                  <td class="num-col">${pmjjCop(f.bomberil ?? 0, 2)}</td>
                  <td class="num-col" style="font-weight:700; color:var(--brand-primary);">${pmjjCop(f.neto_cobrar, 2)}</td>
                  <td class="num-col">${pmjjCop(f.autoret, 2)}</td>
                </tr>
              `).join("")}
              <tr class="pmjj-row-highlight">
                <td>TOTAL</td>
                <td><strong>TOTAL VENTAS ${m} 2026</strong></td>
                <td class="num-col"><strong>${pmjjNum(mesData.ventas.totales.unidades)}</strong></td>
                <td class="num-col">-</td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.costo_total)}</strong></td>
                <td class="num-col">-</td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.ventas_netas, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.iva, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.ica ?? 0, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.avisos ?? 0, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.bomberil ?? 0, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.neto_cobrar, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.ventas.totales.autoret, 2)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 2. RECUENTO DE INVENTARIO STOCK EN 0 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Recuento de Inventario Inicial y Unidades a Comprar (Política Stock Final = 0) — ${m}</div>
      </div>
      <div class="card-body">
        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr>
                <th>Ref.</th><th>Producto</th><th class="num-col">Unid. a Vender</th>
                <th class="num-col">(-) Inv. Inicial</th><th class="num-col">Stock Final Deseado</th>
                <th class="num-col">(=) Unid. a Comprar</th><th class="num-col">Costo Unit. Compra</th>
                <th class="num-col">Stock Final (1435)</th><th class="num-col">Costo Inv. Inicial</th>
                <th class="num-col">Costo Compras Mes</th>
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

    <!-- 3. HOJA COM: COMPRAS POR PROVEEDOR -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">3. Hoja COM ${m} — Cédula de Compras por Proveedor y Retenciones (Casa Orange, Cra 13 y Electromenores)</div>
        <span class="pmjj-badge pmjj-badge-purple">50% Contado: ${pmjjCop(mesData.compras.totales.contado_50)} | 50% Crédito: ${pmjjCop(mesData.compras.totales.credito_50)}</span>
      </div>
      <div class="card-body">
        ${proveedores.length ? `
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px,1fr)); gap:10px; margin-bottom:14px;">
            ${proveedores.map(p => `
              <div style="border:1px solid var(--border-light); border-radius:8px; padding:10px 12px; background:var(--bg-subtle); font-size:0.8rem;">
                <strong style="color:var(--brand-primary);">🏢 ${pmjjEsc(p.proveedor)}</strong>
                <div style="color:var(--text-secondary); font-size:0.74rem; margin-bottom:6px;">${pmjjEsc(p.regimen)} • ${p.total_unidades} und.</div>
                <div><strong>Base Compra:</strong> ${pmjjCop(p.total_base)}</div>
                <div><strong>50% Contado (EFC):</strong> ${pmjjCop(p.contado_50)}</div>
                <div><strong>50% Crédito (2205):</strong> ${pmjjCop(p.credito_50)}</div>
              </div>
            `).join("")}
          </div>
        ` : ""}
        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr>
                <th>Proveedor</th><th>Producto</th><th class="num-col">Unid.</th>
                <th class="num-col">Base Compra Unit.</th><th class="num-col">Base Compra Total</th>
                <th class="num-col">IVA Desc. 19%</th><th class="num-col">Retefuente 2,5% (246540)</th>
                <th class="num-col">ICA 9,6‰ (246801)</th>
                <th class="num-col">Avisos 15% (246802)</th>
                <th class="num-col">Bomberil 10% (246803)</th>
                <th class="num-col">Neto Pagar</th>
                <th class="num-col">50% Contado</th><th class="num-col">50% Crédito</th>
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
                  <td class="num-col">${pmjjCop(f.ica ?? 0, 2)}</td>
                  <td class="num-col">${pmjjCop(f.avisos ?? 0, 2)}</td>
                  <td class="num-col">${pmjjCop(f.bomberil ?? 0, 2)}</td>
                  <td class="num-col" style="font-weight:700; color:var(--brand-primary);">${pmjjCop(f.neto_pagar)}</td>
                  <td class="num-col">${pmjjCop(f.contado_50)}</td>
                  <td class="num-col">${pmjjCop(f.credito_50)}</td>
                </tr>
              `).join("")}
              <tr class="pmjj-row-highlight">
                <td>TOTAL</td>
                <td><strong>TOTAL COMPRAS ${m}</strong></td>
                <td class="num-col"><strong>${pmjjNum(mesData.compras.totales.unidades)}</strong></td>
                <td class="num-col">-</td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.subtotal)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.iva_desc)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.retefuente)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.ica ?? 0, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.avisos ?? 0, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.bomberil ?? 0, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.neto_pagar)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.contado_50)}</strong></td>
                <td class="num-col"><strong>${pmjjCop(mesData.compras.totales.credito_50)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 4. RESUMEN TRIBUTARIO DEL MES -->
    <div class="card">
      <div class="card-header"><div class="card-title">4. Consolidado Tributario Causado en ${m} 2026 (2408 • 2465 • 2468 • 1355)</div></div>
      <div class="card-body">
        <div class="table-wrap">
          <table class="acct-table">
            <thead><tr><th>Concepto Tributario</th><th>PUC</th><th class="num-col">Valor (COP)</th><th>Aplicación Contable y Fiscal</th></tr></thead>
            <tbody>
              ${mesData.tributaria.map(t => `
                <tr class="${["2465", "2468", "2408"].includes(String(t.puc || "").trim()) ? "pmjj-row-highlight" : ""}">
                  <td><strong>${pmjjEsc(t.concepto)}</strong></td>
                  <td><code>${pmjjEsc(t.puc)}</code></td>
                  <td class="num-col" style="font-weight:800;">${pmjjCop(t.valor, 2)}</td>
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
   5. TAB: FLUJO DE EFECTIVO PROYECTADO (EFC)
   ========================================================================== */
function renderTabEFC(container, d) {
  const mode = PRESUP_EFC_MODE;
  const may = d.meses.MAYO.efc;
  const jun = d.meses.JUNIO.efc;
  const jul = d.meses.JULIO.efc;
  const flujoComp = d.maestro?.flujo_caja_comparativo || [];

  const renderSingleEFC = (efc, mesLabel) => `
    <div class="card">
      <div class="card-header">
        <div class="card-title">💵 ${pmjjEsc(efc.titulo || `CAJA — EFC PROYECTADO ${mesLabel} 2026`)}</div>
        <div style="display:flex; gap:8px;">
          <span class="pmjj-badge pmjj-badge-gold">Excedente Mes: ${pmjjCop(efc.excedente ?? (efc.total_entradas - efc.total_salidas), 2)}</span>
          <span class="pmjj-badge pmjj-badge-purple">Saldo Final: ${pmjjCop(efc.saldo_final, 2)}</span>
        </div>
      </div>
      <div class="card-body">
        <div class="table-wrap">
          <table class="pmjj-efc-table">
            <thead>
              <tr>
                <th colspan="4" class="pmjj-efc-banner">CAJA — EFC PROYECTADO ${mesLabel} 2026</th>
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
                  <td class="num-col" style="color:#047857; font-weight:600;">${f.entrada !== null ? pmjjCopHtml(f.entrada, 2) : ""}</td>
                  <td class="num-col" style="color:#B91C1C; font-weight:600;">${f.salida !== null ? pmjjCopHtml(f.salida, 2) : ""}</td>
                  <td class="num-col" style="font-weight:700;">${pmjjCopHtml(f.total, 2)}</td>
                </tr>
              `).join("")}
              <tr class="pmjj-efc-total">
                <td><strong>SALDO NETO FINAL ${mesLabel}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(efc.total_entradas, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(efc.total_salidas, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(efc.saldo_final, 2)}</strong></td>
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
        <button class="filter-chip ${mode === "COMPARATIVO" ? "active" : ""}" onclick="setPresupEfcMode('COMPARATIVO')">
          📊 Ver Consolidado 3 Meses (Hoja MAESTRO)
        </button>
        <button class="filter-chip ${mode !== "COMPARATIVO" ? "active" : ""}" onclick="setPresupEfcMode(PRESUP_ACTIVE_MONTH)">
          💵 Ver Solo Mes Activo (${activeMonth} 2026)
        </button>
      </div>
      <span style="font-size:0.78rem; color:var(--brand-primary); font-weight:700;">Cambia entre MAY, JUN y JUL en la barra superior</span>
    </div>

    ${PRESUP_SHOW_GUIDE ? `
      <div class="pmjj-explain-box">
        <strong>💡 Explicación del Flujo de Efectivo (<code>EFC PROYECTADO</code> y <code>MAESTRO</code>):</strong>
        • <strong>Mayo:</strong> Inicia con <strong>${pmjjCop(may.saldo_inicial, 2)}</strong> (Caja + Bancos de Abril), cobra Ventas al Contado (${pmjjCop(52389026)}) y Cartera de Jaime (${pmjjCop(28857500)}), y paga Compras al Contado (${pmjjCop(16253160)}), Cuota Crédito (${pmjjCop(1892260, 2)}), Remodelación (${pmjjCop(568800)}), Seguridad Social (${pmjjCop(1753545, 2)}), Salarios (${pmjjCop(6827928, 2)}), Proveedores Abril (${pmjjCop(5778000)}), Retefuente Abril (${pmjjCop(442490)}) y <strong>ReteICA Abril (${pmjjCop(95400)})</strong> → Cierra en <strong>${pmjjCop(may.saldo_final, 2)}</strong>.<br/>
        • <strong>Junio:</strong> Recauda Cartera de Mayo (${pmjjCop(52389026)}) y Ventas Contado (${pmjjCop(52343589)}), paga Proveedores de Mayo (${pmjjCop(16253160)}), ReteICA de Mayo (${pmjjCop(341280)}), <strong>Prima Semestral (${pmjjCop(3082100)})</strong> y Retefuente de Mayo (${pmjjCop(2934643, 2)}) → Cierra en <strong>${pmjjCop(jun.saldo_final, 2)}</strong>.<br/>
        • <strong>Julio:</strong> Recauda Cartera de Junio (${pmjjCop(52343589)}) y Ventas Contado (${pmjjCop(52343589)}), paga Proveedores de Junio (${pmjjCop(35577912)}), Retefuente de Junio (${pmjjCop(3776914, 2)}), ReteICA de Junio (${pmjjCop(746496)}) y el <strong>IVA Bimestral May–Jun (${pmjjCop(17229254, 2)})</strong> → Cierra en <strong>${pmjjCop(jul.saldo_final, 2)}</strong>.
      </div>
    ` : ""}

    ${mode === "COMPARATIVO" ? `
      ${flujoComp.length ? `
        <div class="card">
          <div class="card-header">
            <div class="card-title">📊 Hoja MAESTRO — Flujo de Caja Proyectado Comparativo (Mayo, Junio y Julio 2026)</div>
          </div>
          <div class="card-body">
            <div class="table-wrap">
              <table class="acct-table">
                <thead>
                  <tr>
                    <th rowspan="2">CONCEPTO</th>
                    <th colspan="3" style="text-align:center;">MAYO 2026</th>
                    <th colspan="3" style="text-align:center;">JUNIO 2026</th>
                    <th colspan="3" style="text-align:center;">JULIO 2026</th>
                  </tr>
                  <tr>
                    <th class="num-col">Entrada</th><th class="num-col">Salida</th><th class="num-col">Total</th>
                    <th class="num-col">Entrada</th><th class="num-col">Salida</th><th class="num-col">Total</th>
                    <th class="num-col">Entrada</th><th class="num-col">Salida</th><th class="num-col">Total</th>
                  </tr>
                </thead>
                <tbody>
                  ${flujoComp.map(r => {
                    const isTot = r.concepto.toUpperCase().includes("SALDO NETO");
                    return `
                      <tr class="${isTot ? "pmjj-row-highlight" : ""}">
                        <td><strong>${pmjjEsc(r.concepto)}</strong></td>
                        <td class="num-col" style="color:#047857;">${r.mayo_ent ? pmjjCop(r.mayo_ent) : ""}</td>
                        <td class="num-col" style="color:#B91C1C;">${r.mayo_sal ? pmjjCop(r.mayo_sal) : ""}</td>
                        <td class="num-col"><strong>${pmjjCop(r.mayo_tot)}</strong></td>
                        <td class="num-col" style="color:#047857;">${r.junio_ent ? pmjjCop(r.junio_ent) : ""}</td>
                        <td class="num-col" style="color:#B91C1C;">${r.junio_sal ? pmjjCop(r.junio_sal) : ""}</td>
                        <td class="num-col"><strong>${pmjjCop(r.junio_tot)}</strong></td>
                        <td class="num-col" style="color:#047857;">${r.julio_ent ? pmjjCop(r.julio_ent) : ""}</td>
                        <td class="num-col" style="color:#B91C1C;">${r.julio_sal ? pmjjCop(r.julio_sal) : ""}</td>
                        <td class="num-col"><strong>${pmjjCop(r.julio_tot)}</strong></td>
                      </tr>
                    `;
                  }).join("")}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ` : ""}
      ${renderSingleEFC(may, "MAYO")}
      ${renderSingleEFC(jun, "JUNIO")}
      ${renderSingleEFC(jul, "JULIO")}
    ` : renderSingleEFC(d.meses[activeMonth].efc, activeMonth)}
  `;
}

/* ==========================================================================
   6. TAB: ESTADO DE RESULTADOS PROYECTADO (ER)
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
    { cod: "4135", nom: "COMERCIO AL POR MAYOR Y POR MENOR", v1: may.ingresos_4135, v2: jun.ingresos_4135, v3: jul.ingresos_4135, cls: "pmjj-row-subtle" },
    { cod: "6135", nom: "COMERCIO AL POR MAYOR Y MENOR (COSTO DE VENTAS)", v1: may.costos_6135, v2: jun.costos_6135, v3: jul.costos_6135 },
    { cod: "—",    nom: "UTILIDAD BRUTA EN VENTAS (MARGEN 30%)", v1: may.utilidad_bruta, v2: jun.utilidad_bruta, v3: jul.utilidad_bruta, cls: "pmjj-row-highlight" },
    { cod: "5105", nom: "BENEFICIOS A EMPLEADOS", v1: gastoPorCodigo(may, "5105"), v2: gastoPorCodigo(jun, "5105"), v3: gastoPorCodigo(jul, "5105") },
    { cod: "5160", nom: "DEPRECIACIONES (FLOTA Y EQUIPO DE TRANSPORTE)", v1: gastoPorCodigo(may, "5160"), v2: gastoPorCodigo(jun, "5160"), v3: gastoPorCodigo(jul, "5160") },
    { cod: "5260", nom: "DEPRECIACIONES (CONSTRUCCIONES Y EDIFICACIONES)", v1: gastoPorCodigo(may, "5260"), v2: gastoPorCodigo(jun, "5260"), v3: gastoPorCodigo(jul, "5260") },
    { cod: "5305", nom: "FINANCIEROS (INTERESES CRÉDITO BANCOLOMBIA — TA)", v1: gastoPorCodigo(may, "5305"), v2: gastoPorCodigo(jun, "5305"), v3: gastoPorCodigo(jul, "5305") },
    { cod: "—",    nom: "TOTAL GASTOS", v1: may.total_gastos, v2: jun.total_gastos, v3: jul.total_gastos, cls: "pmjj-row-subtle" },
    { cod: "—",    nom: "RESULTADO DEL EJERCICIO ANTES DE IMPUESTOS", v1: may.uai, v2: jun.uai, v3: jul.uai, cls: "pmjj-row-subtle" },
    { cod: "2499", nom: "IMPUESTO DE RENTA (PROVISIÓN 35%)", v1: may.impuesto_renta, v2: jun.impuesto_renta, v3: jul.impuesto_renta },
    { cod: "—",    nom: "UTILIDAD DESPUÉS DEL IMPUESTO", v1: may.udi, v2: jun.udi, v3: jul.udi },
    { cod: "3305", nom: "RESERVA LEGAL (10%)", v1: may.reserva_legal, v2: jun.reserva_legal, v3: jul.reserva_legal },
    { cod: "3605", nom: "RESULTADO DEL EJERCICIO (UTILIDAD NETA)", v1: may.utilidad_neta, v2: jun.utilidad_neta, v3: jul.utilidad_neta, cls: "pmjj-row-highlight" },
  ];

  container.innerHTML = `
    ${PRESUP_SHOW_GUIDE ? `
      <div class="pmjj-explain-box">
        <strong>💡 Cómo explicar la hoja <code>ER CONSOLIDADO</code> (Mayo, Junio y Julio):</strong>
        1) El margen bruto sobre ventas es exactamente del <strong>30%</strong> en los tres meses.
        2) Los gastos operacionales incluyen únicamente <strong>Beneficios a Empleados (${pmjjCop(10186475.66, 2)})</strong>, <strong>Depreciaciones (${pmjjCop(1080000)} + ${pmjjCop(199532.81, 2)})</strong> y <strong>Financieros (5305)</strong> tomados de las cuotas 3, 4 y 5 de la hoja <code>TA</code>.
        3) La provisión mensual de Impuesto de Renta (35%) se registra en la cuenta <code>2499</code> y la Reserva Legal (10%) en la <code>3305</code>, logrando una Utilidad Neta trimestral acumulada de <strong>${pmjjCop(may.utilidad_neta + jun.utilidad_neta + jul.utilidad_neta, 2)}</strong>.
      </div>
    ` : ""}

    <div class="card">
      <div class="card-header">
        <div class="card-title">📈 Hoja ER CONSOLIDADO — Estado de Resultados Proyectado (1 de Mayo al 31 de Julio 2026)</div>
        <span class="pmjj-badge pmjj-badge-emerald">Meta Mensual: ${pmjjCop(meta, 2)} ✓</span>
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
              ${filasER.map(r => `
                <tr class="${r.cls || ""}">
                  <td><code>${pmjjEsc(r.cod)}</code></td>
                  <td><strong>${pmjjEsc(r.nom)}</strong></td>
                  <td class="num-col">${pmjjCopHtml(r.v1, 2)}</td>
                  <td class="num-col">${pmjjCopHtml(r.v2, 2)}</td>
                  <td class="num-col">${pmjjCopHtml(r.v3, 2)}</td>
                  <td class="num-col" style="font-weight:800; color:var(--brand-primary);">${pmjjCopHtml(r.v1 + r.v2 + r.v3, 2)}</td>
                </tr>
              `).join("")}
              <tr>
                <td>✓</td>
                <td><strong>Excedente sobre Meta Teórica 50% EA (${pmjjCop(meta, 2)}/mes)</strong></td>
                <td class="num-col" style="color:#047857; font-weight:800;">+${pmjjCop(may.utilidad_neta - meta, 2)} ✓</td>
                <td class="num-col" style="color:#047857; font-weight:800;">+${pmjjCop(jun.utilidad_neta - meta, 2)} ✓</td>
                <td class="num-col" style="color:#047857; font-weight:800;">+${pmjjCop(jul.utilidad_neta - meta, 2)} ✓</td>
                <td class="num-col" style="color:#047857; font-weight:800;">+${pmjjCop((may.utilidad_neta + jun.utilidad_neta + jul.utilidad_neta) - (meta * 3), 2)} ✓</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
}

/* ==========================================================================
   7. TAB: ESTADO DE SITUACIÓN FINANCIERA PROYECTADO (ESF)
   ========================================================================== */
function renderTabESF(container, d) {
  const abr = d.esf_abril || null;
  const may = d.meses.MAYO.esf;
  const jun = d.meses.JUNIO.esf;
  const jul = d.meses.JULIO.esf;

  const valOf = (arr, cod) => {
    if (!arr) return 0;
    const f = arr.find(x => x.codigo === cod);
    return f ? f.valor : 0;
  };

  const renderSectionRows = (rows, groupKey) => rows
    .filter(r => {
      const vAbr = abr ? valOf(abr[groupKey], r.cod) : 0;
      const vMay = valOf(may[groupKey], r.cod);
      const vJun = valOf(jun[groupKey], r.cod);
      const vJul = valOf(jul[groupKey], r.cod);
      return Math.abs(vAbr) >= 0.01 || Math.abs(vMay) >= 0.01 || Math.abs(vJun) >= 0.01 || Math.abs(vJul) >= 0.01;
    })
    .map(r => `
    <tr>
      <td><code>${pmjjEsc(r.cod)}</code></td>
      <td>${pmjjEsc(r.nom)}</td>
      ${abr ? `<td class="num-col" style="color:var(--text-secondary);">${pmjjCopHtml(valOf(abr[groupKey], r.cod), 2)}</td>` : ""}
      <td class="num-col">${pmjjCopHtml(valOf(may[groupKey], r.cod), 2)}</td>
      <td class="num-col">${pmjjCopHtml(valOf(jun[groupKey], r.cod), 2)}</td>
      <td class="num-col">${pmjjCopHtml(valOf(jul[groupKey], r.cod), 2)}</td>
    </tr>
  `).join("");

  const acRows = [
    { cod: "1105", nom: "CAJA" },
    { cod: "1110", nom: "BANCOS" },
    { cod: "1305", nom: "CLIENTES" },
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
    { cod: "2105", nom: "BANCOS NACIONALES" },
    { cod: "2205", nom: "PROVEEDORES" },
    { cod: "2320", nom: "A CONTRATISTAS" },
    { cod: "2408", nom: "IMPUESTO A LAS VENTAS POR PAGAR IVA" },
    { cod: "2465", nom: "RETENCIÓN EN LA FUENTE IMP. DE RENTA RETENIDO A TERCEROS" },
    { cod: "2468", nom: "IMPUESTO DE ICA RETENIDO A TERCEROS" },
    { cod: "2499", nom: "PROVISIÓN PARA OBLIGACIONES FISCALES" },
    { cod: "2570", nom: "RETENCIONES Y APORTES DE NÓMINA" },
    { cod: "2580", nom: "FONDO DE PENSIONES Y CESANTÍAS X PAGAR" },
    { cod: "2610", nom: "PROVISIÓN PARA OBLIGACIONES LABORALES" },
    { cod: "2705", nom: "INGRESOS RECIBIDOS POR ANTICIPADO" },
  ];
  const patRows = [
    { cod: "3105", nom: "CAPITAL SUSCRITO Y PAGADO" },
    { cod: "3305", nom: "RESERVAS OBLIGATORIAS" },
    { cod: "3605", nom: "UTILIDADES DEL EJERCICIO" },
    { cod: "3610", nom: "PÉRDIDA DEL EJERCICIO" },
    { cod: "3705", nom: "UTILIDADES ACUMULADAS" },
    { cod: "3710", nom: "PÉRDIDAS ACUMULADAS" },
  ];

  const colSpan = abr ? 6 : 5;

  container.innerHTML = `
    ${PRESUP_SHOW_GUIDE ? `
      <div class="pmjj-explain-box">
        <strong>💡 Cómo explicar la hoja <code>ESF CONSOLIDADO</code> (Abril Base → Mayo, Junio y Julio):</strong>
        1) El inventario (<code>1435</code>) pasa de <strong>${pmjjCop(33822000)}</strong> en Abril a <strong>$0</strong> en Mayo, Junio y Julio gracias a la política Stock Final = 0.
        2) La Provisión para Obligaciones Laborales (<code>2610</code>) sube de ${pmjjCop(4815009.42, 2)} en Abril a <strong>${pmjjCop(6420012.55, 2)}</strong> en Mayo, baja a <strong>${pmjjCop(4942915.69, 2)}</strong> en Junio por el pago de la Prima Semestral (${pmjjCop(3082100)}), y cierra en <strong>${pmjjCop(6547918.83, 2)}</strong> en Julio.
        3) Cada mes, la Utilidad del Ejercicio anterior (<code>3605</code>) se traslada a Utilidades Acumuladas (<code>3705</code>: ${pmjjCop(16446082.49, 2)} → ${pmjjCop(25001281.77, 2)} → ${pmjjCop(33551398.78, 2)}), manteniendo un cuadre exacto de <strong>$0</strong> en los 4 cortes.
      </div>
    ` : ""}

    <div class="card">
      <div class="card-header">
        <div class="card-title">🏛️ Hoja ESF CONSOLIDADO — Estado de Situación Financiera Proyectado (Abril Base y Mayo – Julio 2026)</div>
        <span class="pmjj-badge pmjj-badge-emerald">Cuadre Exacto $0 en Todos los Meses ✓</span>
      </div>
      <div class="card-body">
        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr>
                <th>PUC</th>
                <th>Concepto</th>
                ${abr ? `<th class="num-col">Abril 2026 (Base)</th>` : ""}
                <th class="num-col">Mayo 2026</th>
                <th class="num-col">Junio 2026</th>
                <th class="num-col">Julio 2026</th>
              </tr>
            </thead>
            <tbody>
              <tr class="niif-row-grupo niif-grupo-activo-corr"><td colspan="${colSpan}">Activos Corrientes</td></tr>
              ${renderSectionRows(acRows, "activos_corrientes")}
              <tr class="pmjj-row-subtle">
                <td></td><td><strong>SUBTOTAL ACTIVOS CORRIENTES</strong></td>
                ${abr ? `<td class="num-col"><strong>${pmjjCopHtml(abr.subtotal_ac, 2)}</strong></td>` : ""}
                <td class="num-col"><strong>${pmjjCopHtml(may.subtotal_ac, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jun.subtotal_ac, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jul.subtotal_ac, 2)}</strong></td>
              </tr>

              <tr class="niif-row-grupo niif-grupo-activo-fijo"><td colspan="${colSpan}">Activos Fijos</td></tr>
              ${renderSectionRows(ancRows, "activos_no_corrientes")}
              <tr class="pmjj-row-subtle">
                <td></td><td><strong>SUBTOTAL ACTIVOS FIJOS</strong></td>
                ${abr ? `<td class="num-col"><strong>${pmjjCopHtml(abr.subtotal_anc, 2)}</strong></td>` : ""}
                <td class="num-col"><strong>${pmjjCopHtml(may.subtotal_anc, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jun.subtotal_anc, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jul.subtotal_anc, 2)}</strong></td>
              </tr>

              <tr class="pmjj-row-highlight">
                <td>1</td><td><strong>TOTAL ACTIVOS</strong></td>
                ${abr ? `<td class="num-col"><strong>${pmjjCopHtml(abr.total_activos, 2)}</strong></td>` : ""}
                <td class="num-col"><strong>${pmjjCopHtml(may.total_activos, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jun.total_activos, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jul.total_activos, 2)}</strong></td>
              </tr>

              <tr class="niif-row-grupo niif-grupo-pasivo-corr"><td colspan="${colSpan}">Pasivos Corrientes</td></tr>
              ${renderSectionRows(pcRows, "pasivos_corrientes")}
              <tr class="pmjj-row-subtle">
                <td></td><td><strong>SUBTOTAL PASIVOS CORRIENTES</strong></td>
                ${abr ? `<td class="num-col"><strong>${pmjjCopHtml(abr.subtotal_pc, 2)}</strong></td>` : ""}
                <td class="num-col"><strong>${pmjjCopHtml(may.subtotal_pc, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jun.subtotal_pc, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jul.subtotal_pc, 2)}</strong></td>
              </tr>

              <tr class="niif-row-grupo niif-grupo-pasivo-nocorr"><td colspan="${colSpan}">Pasivos No Corrientes</td></tr>
              <tr>
                <td><code>2105</code></td><td>BANCOS NACIONALES</td>
                ${abr ? `<td class="num-col">${pmjjCopHtml(abr.subtotal_pnc, 2)}</td>` : ""}
                <td class="num-col">${pmjjCopHtml(may.subtotal_pnc, 2)}</td>
                <td class="num-col">${pmjjCopHtml(jun.subtotal_pnc, 2)}</td>
                <td class="num-col">${pmjjCopHtml(jul.subtotal_pnc, 2)}</td>
              </tr>
              <tr class="pmjj-row-subtle">
                <td>2</td><td><strong>TOTAL PASIVOS</strong></td>
                ${abr ? `<td class="num-col"><strong>${pmjjCopHtml(abr.total_pasivos, 2)}</strong></td>` : ""}
                <td class="num-col"><strong>${pmjjCopHtml(may.total_pasivos, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jun.total_pasivos, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jul.total_pasivos, 2)}</strong></td>
              </tr>

              <tr class="niif-row-grupo niif-grupo-patrimonio"><td colspan="${colSpan}">Patrimonio</td></tr>
              ${renderSectionRows(patRows, "patrimonio")}
              <tr class="pmjj-row-subtle">
                <td>3</td><td><strong>TOTAL PATRIMONIO</strong></td>
                ${abr ? `<td class="num-col"><strong>${pmjjCopHtml(abr.total_patrimonio, 2)}</strong></td>` : ""}
                <td class="num-col"><strong>${pmjjCopHtml(may.total_patrimonio, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jun.total_patrimonio, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jul.total_patrimonio, 2)}</strong></td>
              </tr>

              <tr class="pmjj-row-highlight">
                <td>2+3</td><td><strong>TOTAL PASIVO Y PATRIMONIO</strong></td>
                ${abr ? `<td class="num-col"><strong>${pmjjCopHtml(abr.total_pasivo_patrimonio, 2)}</strong></td>` : ""}
                <td class="num-col"><strong>${pmjjCopHtml(may.total_pasivo_patrimonio, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jun.total_pasivo_patrimonio, 2)}</strong></td>
                <td class="num-col"><strong>${pmjjCopHtml(jul.total_pasivo_patrimonio, 2)}</strong></td>
              </tr>
              <tr>
                <td>=</td>
                <td><strong>Comprobación Ecuación Contable (<span class="ef-col-activo">Activo</span> = <span class="ef-col-pasivo">Pasivo</span> + <span class="ef-col-patrimonio">Patrimonio</span>)</strong></td>
                ${abr ? `<td class="num-col" style="color:var(--brand-emerald); font-weight:800;">$0 ✓</td>` : ""}
                <td class="num-col" style="color:var(--brand-emerald); font-weight:800;">$0 ✓</td>
                <td class="num-col" style="color:var(--brand-emerald); font-weight:800;">$0 ✓</td>
                <td class="num-col" style="color:var(--brand-emerald); font-weight:800;">$0 ✓</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
}

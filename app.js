/**
 * STUDENTCONT.IA — Motor Frontend NIIF, Facturación por Régimen, Kardex, Libros Auxiliares en Vivo y Multi-Empresa
 * Desarrollado a la medida para ELECTROVIVIENDA S.A.S (NIT 901.765.438-3) y Estudiantes Independientes
 */

let DB = null;
let ACTIVE_PERIOD = "ABRIL";
let ACTIVE_SECTION = "dashboard";
let ACTIVE_VOUCHER_CAT = "ALL";
let ACTIVE_VOUCHER_SCOPE = "MONTH"; // 'MONTH' | 'ALL'
let ACTIVE_VOUCHER_SHEET = null;
let VOUCHER_VIEW_MODE = "voucher";
let ACTIVE_INVOICE_CAT = "ALL";
let ACTIVE_INVOICE_ID = null;
let ACTIVE_AUX_MODE = "VIVO_SUBCUENTAS";
let ACTIVE_KARDEX_ID = "TV01";
const ALL_12_MONTHS = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"];
let ACTIVE_EF_TAB = "DINAMICO";
let ACTIVE_EF_SHEET = "";
let ACTIVE_TAX_TAB = "F350";
let ACTIVE_STUDENT_PROFILE = {
  id: "gina_villamizar",
  nombre: "Gina Villamizar",
  correo: "gina.villamizar@studentcont.ia",
  programa: "Contadora Titular • NIIF Grupo 2",
  rol: "Titular / Administradora",
  workspace_id: "electrovivienda"
};

// ============================================================================
// MATRIZ DE REGÍMENES TRIBUTARIOS COLOMBIA 2026 (COMPRADOR VS VENDEDOR)
// ============================================================================
const REGIMENES_VENTA_COMPRADOR = [
  {
    id: "GC_AUTO",
    label: "Gran Contribuyente y Autorretenedor DIAN (Ej: Industrias Super S.A.S)",
    aplica_iva: true,
    tarifa_iva: 0.19,
    aplica_retefuente: false,
    tarifa_retefuente: 0.025,
    nota_retefuente: "NO (Nosotros somos Autorretenedores en Renta)",
    aplica_autorretencion: true,
    tarifa_autorretencion: 0.025,
    nota_autorretencion: "SÍ (2.5% Compras/Ventas Generales - 135575 vs 246575)",
    aplica_reteiva: true,
    tarifa_reteiva: 0.15,
    nota_reteiva: "SÍ (15% del IVA - El Gran Contribuyente nos retiene IVA en 135517)",
    aplica_reteica: true,
    tarifa_reteica: 0.0096,
    nota_reteica: "SÍ (9.6‰ ReteICA + 15% Avisos + 10% Sobretasa Bomberil)"
  },
  {
    id: "RRI_DECLARANTE",
    label: "Régimen Responsable de IVA (RRI) — Declarante Renta (Ej: Electrohogar S.A.S)",
    aplica_iva: true,
    tarifa_iva: 0.19,
    aplica_retefuente: false,
    tarifa_retefuente: 0.025,
    nota_retefuente: "NO (Somos Autorretenedores en Renta)",
    aplica_autorretencion: true,
    tarifa_autorretencion: 0.025,
    nota_autorretencion: "SÍ (2.5% Autorretención en Renta - 135575 vs 246575)",
    aplica_reteiva: false,
    tarifa_reteiva: 0.15,
    nota_reteiva: "NO (Entre dos RRI ordinarios no hay ReteIVA)",
    aplica_reteica: true,
    tarifa_reteica: 0.0096,
    nota_reteica: "SÍ (9.6‰ ReteICA + 15% Avisos + 10% Bomberil)"
  },
  {
    id: "NO_RRI_NO_DEC",
    label: "No Responsable de IVA — Persona Natural No Declarante (Ej: Jhon Estiven Rueda / Juan Camilo)",
    aplica_iva: true,
    tarifa_iva: 0.19,
    aplica_retefuente: false,
    tarifa_retefuente: 0.035,
    nota_retefuente: "NO (El comprador PN No Responsable no es agente de retención)",
    aplica_autorretencion: true,
    tarifa_autorretencion: 0.035,
    nota_autorretencion: "SÍ (3.5% Autorretención por venta a No Declarante - Hojas 22, 54, 57)",
    aplica_reteiva: false,
    tarifa_reteiva: 0.15,
    nota_reteiva: "NO",
    aplica_reteica: false,
    tarifa_reteica: 0.0096,
    nota_reteica: "NO (No es agente retenedor de ICA)"
  },
  {
    id: "RST_SIMPLE",
    label: "Régimen Simple de Tributación (RST)",
    aplica_iva: true,
    tarifa_iva: 0.19,
    aplica_retefuente: false,
    tarifa_retefuente: 0.025,
    nota_retefuente: "NO (El RST no practica retención en la fuente por renta)",
    aplica_autorretencion: true,
    tarifa_autorretencion: 0.025,
    nota_autorretencion: "SÍ (2.5% Autorretención en Renta)",
    aplica_reteiva: false,
    tarifa_reteiva: 0.15,
    nota_reteiva: "NO",
    aplica_reteica: false,
    tarifa_reteica: 0.0096,
    nota_reteica: "NO"
  }
];

const REGIMENES_COMPRA_VENDEDOR = [
  {
    id: "GC_AUTO_PROV",
    label: "Gran Contribuyente y Autorretenedor (Ej: Distribuidora Samsung S.A / LG S.A.S / AIWA S.A.S)",
    aplica_iva: true,
    tarifa_iva: 0.19,
    aplica_retefuente: false,
    tarifa_retefuente: 0.025,
    nota_retefuente: "NO (El proveedor es Autorretenedor en Renta - Hojas 12, 13, 14, 15)",
    aplica_autorretencion: false,
    tarifa_autorretencion: 0,
    nota_autorretencion: "NO (Ellos se autorretienen en su propia factura)",
    aplica_reteiva: false,
    tarifa_reteiva: 0.15,
    nota_reteiva: "NO (No se retiene IVA a Gran Contribuyente)",
    aplica_reteica: false,
    tarifa_reteica: 0.0096,
    nota_reteica: "NO (Gran Contribuyente / Autorretenedor ICA)"
  },
  {
    id: "RRI_PROV_DEC",
    label: "Régimen Responsable de IVA (RRI) — Declarante Renta (Proveedor Ordinario)",
    aplica_iva: true,
    tarifa_iva: 0.19,
    aplica_retefuente: true,
    tarifa_retefuente: 0.025,
    nota_retefuente: "SÍ (2.5% Retefuente Compras Declarante - 246540)",
    aplica_autorretencion: false,
    tarifa_autorretencion: 0,
    nota_autorretencion: "NO",
    aplica_reteiva: false,
    tarifa_reteiva: 0.15,
    nota_reteiva: "NO (Entre dos RRI ordinarios no aplica ReteIVA)",
    aplica_reteica: true,
    tarifa_reteica: 0.0096,
    nota_reteica: "SÍ (9.6‰ ReteICA 246801 + 15% Avisos 246802 + 10% Bomberil 246803)"
  },
  {
    id: "NO_RRI_DEC_COMPRA",
    label: "No Responsable de IVA — Persona Natural Declarante (Ej: Papelería Hojas 7 y 51)",
    aplica_iva: false,
    tarifa_iva: 0,
    aplica_retefuente: true,
    tarifa_retefuente: 0.025,
    nota_retefuente: "SÍ (2.5% Compras a Declarante - 246540)",
    aplica_autorretencion: false,
    tarifa_autorretencion: 0,
    nota_autorretencion: "NO",
    aplica_reteiva: false,
    tarifa_reteiva: 0,
    nota_reteiva: "NO (No cobra IVA)",
    aplica_reteica: true,
    tarifa_reteica: 0.0096,
    nota_reteica: "SÍ (9.6‰ ReteICA + 15% Avisos + 10% Bomberil)"
  },
  {
    id: "NO_RRI_NO_DEC_COMPRA",
    label: "No Responsable de IVA — Persona Natural No Declarante (Compras 3.5% - Hoja 5)",
    aplica_iva: false,
    tarifa_iva: 0,
    aplica_retefuente: true,
    tarifa_retefuente: 0.035,
    nota_retefuente: "SÍ (3.5% Compras a No Declarante - 246540)",
    aplica_autorretencion: false,
    tarifa_autorretencion: 0,
    nota_autorretencion: "NO",
    aplica_reteiva: false,
    tarifa_reteiva: 0,
    nota_reteiva: "NO",
    aplica_reteica: true,
    tarifa_reteica: 0.0096,
    nota_reteica: "SÍ (9.6‰ ReteICA + 15% Avisos + 10% Bomberil)"
  },
  {
    id: "SERVICIOS_4",
    label: "Prestador de Servicios Declarante (Mantenimiento / Transporte 4% - Hoja 9)",
    aplica_iva: false,
    tarifa_iva: 0,
    aplica_retefuente: true,
    tarifa_retefuente: 0.04,
    nota_retefuente: "SÍ (4.0% Servicios Generales - 246525)",
    aplica_autorretencion: false,
    tarifa_autorretencion: 0,
    nota_autorretencion: "NO",
    aplica_reteiva: false,
    tarifa_reteiva: 0,
    nota_reteiva: "NO",
    aplica_reteica: true,
    tarifa_reteica: 0.0096,
    nota_reteica: "SÍ (9.6‰ ReteICA + 15% Avisos + 10% Bomberil)"
  }
];

function fmtCOP(val) {
  const num = Number(val) || 0;
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(Math.round(num));
}

function fmtNum(val, dec = 0) {
  const num = Number(val) || 0;
  return new Intl.NumberFormat("es-CO", {
    minimumFractionDigits: dec,
    maximumFractionDigits: dec
  }).format(num);
}

function showToast(msg) {
  const container = document.getElementById("toastContainer");
  if (!container) return;
  const el = document.createElement("div");
  el.className = "toast";
  el.innerHTML = `<span>✅</span> <span>${msg}</span>`;
  container.appendChild(el);
  setTimeout(() => el.remove(), 4500);
}

// ============================================================================
// INICIALIZACIÓN
// ============================================================================
window.addEventListener("DOMContentLoaded", async () => {
  loadSavedStudentProfileFromStorage();
  await loadDatabase();
  initLogoPreview();
  // Sincronización automática en segundo plano para actualizar cambios en vivo sin recargar
  setInterval(async () => {
    try {
      const res = await fetch(`/api/version?t=${Date.now()}`);
      if (!res.ok) return;
      const vData = await res.json();
      if (vData.ok && vData.actualizado && DB?.meta?.actualizado && vData.actualizado !== DB.meta.actualizado) {
        await loadDatabase();
      }
    } catch (e) {}
  }, 8000);
});

function loadSavedStudentProfileFromStorage() {
  const ginaProf = {
    id: "gina_villamizar",
    usuario: "gina",
    nombre: "Gina Villamizar",
    correo: "gina.villamizar@studentcont.ia",
    programa: "Contadora Titular • Especialista NIIF",
    rol: "Titular / Administradora",
    workspace_id: "electrovivienda"
  };
  const saved = localStorage.getItem("studentcont_active_profile");
  if (saved) {
    try {
      ACTIVE_STUDENT_PROFILE = JSON.parse(saved);
    } catch (e) {
      ACTIVE_STUDENT_PROFILE = ginaProf;
    }
  } else {
    ACTIVE_STUDENT_PROFILE = ginaProf;
    try { localStorage.setItem("studentcont_active_profile", JSON.stringify(ginaProf)); } catch (e) {}
  }
  // Permitir navegación inmediata sin bloqueos
  document.getElementById("welcomeAuthOverlay")?.classList.add("hidden");
  updateStudentProfileUI();
}

async function loginAsGinaDirect() {
  const ginaProf = {
    id: "gina_villamizar",
    usuario: "gina",
    nombre: "Gina Villamizar",
    correo: "gina.villamizar@studentcont.ia",
    programa: "Contadora Titular • Especialista NIIF",
    rol: "Titular / Administradora",
    workspace_id: "electrovivienda"
  };
  ACTIVE_STUDENT_PROFILE = ginaProf;
  localStorage.setItem("studentcont_active_profile", JSON.stringify(ginaProf));
  await loadDatabase("electrovivienda");
  updateStudentProfileUI();
  refreshAllViews();
  closeWelcomeLoginOverlay();
  showToast("🔐 Bienvenida Gina Villamizar — ELECTROVIVIENDA S.A.S activa");
}
window.loginAsGinaDirect = loginAsGinaDirect;

function logoutToWelcomeScreen() {
  localStorage.removeItem("studentcont_active_profile");
  openWelcomeLoginOverlay();
  showToast("🔒 Sesión finalizada. Ingresa tus credenciales.");
}
window.logoutToWelcomeScreen = logoutToWelcomeScreen;

function updateStudentProfileUI() {
  const sName = document.getElementById("sidebarAuthorName");
  const tName = document.getElementById("topbarStudentName");
  const sRole = document.getElementById("sidebarProfileRole");
  if (sName) sName.textContent = ACTIVE_STUDENT_PROFILE.nombre || "Gina Villamizar";
  if (tName) tName.textContent = ACTIVE_STUDENT_PROFILE.nombre || "Gina Villamizar";
  if (sRole) sRole.textContent = ACTIVE_STUDENT_PROFILE.programa || "Contadora Titular • NIIF Grupo 2";
}

async function loadDatabase(wsId = null) {
  try {
    const url = wsId ? `/api/db?ws=${encodeURIComponent(wsId)}` : `/api/db?t=${Date.now()}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("API local no disponible");
    DB = await res.json();
  } catch (e) {
    const res = await fetch("data/electrovivienda_db.json");
    DB = await res.json();
    // Si estamos en modo nube estático (Vercel/GitHub Pages), cargar también transacciones guardadas en localStorage del estudiante
    applyLocalCloudOverlay();
  }
  refreshAllViews();
}

function applyLocalCloudOverlay() {
  try {
    const key = `studentcont_cloud_db_${ACTIVE_STUDENT_PROFILE.id}`;
    const savedCloud = localStorage.getItem(key);
    if (savedCloud) {
      const parsed = JSON.parse(savedCloud);
      if (parsed && parsed.empresa && parsed.meses) {
        DB = parsed;
      }
    }
  } catch (err) {}
}

function saveLocalCloudOverlay() {
  try {
    const key = `studentcont_cloud_db_${ACTIVE_STUDENT_PROFILE.id}`;
    localStorage.setItem(key, JSON.stringify(DB));
  } catch (err) {}
}

function refreshAllViews() {
  if (!DB) return;
  updateSidebarCompanyCard();
  updateBadgesAndAlerts();
  populateQuickComprobanteSelectors();
  renderWelcomeExistingProfiles();
  renderSectionDidacticBanner(ACTIVE_SECTION);
  renderDashboard();
  renderInvoicesSection();
  renderVouchersList();
  populateProductSelect();
  onChangeTipoOperacion();
  renderAuxiliaresSection();
  renderKardexSection();
  renderNominaSection();
  renderEstadosFinancieros();
  renderTaxSection();
  renderAiTutorSection();
  renderReformasSection();
}

function updateSidebarCompanyCard() {
  const emp = DB.empresa || {};
  const wsInfo = DB.workspaces_info || { active_id: "electrovivienda", workspaces: [] };
  const activeWs = (wsInfo.workspaces || []).find(w => w.id === wsInfo.active_id);

  document.getElementById("sidebarWsTypeBadge").textContent = activeWs ? activeWs.tipo : "EMPRESA ACTIVA";
  document.getElementById("sidebarCompanyName").textContent = emp.razon_social || "ELECTROVIVIENDA S.A.S";
  document.getElementById("sidebarCompanyNit").textContent = `NIT: ${emp.nit || ""} • Dígito ${emp.ultimo_digito_nit || "8"}`;
  document.getElementById("sidebarCompanyRegimen").textContent = (emp.regimen || "").slice(0, 56);
  if (emp.elaborado_por && ACTIVE_STUDENT_PROFILE.id === "gina_villamizar") {
    document.getElementById("sidebarAuthorName").textContent = emp.elaborado_por;
  }

  const txtMiRegimen = document.getElementById("txtMiRegimenFijo");
  if (txtMiRegimen) {
    txtMiRegimen.value = `${emp.razon_social} — ${emp.regimen}`;
  }
  const badgeMiReg = document.getElementById("badgeMiRegimenHeader");
  if (badgeMiReg) {
    badgeMiReg.textContent = `Mi Régimen: ${(emp.regimen || "").slice(0, 54)}`;
  }
}

function openAnalisisFinancieroSection() {
  switchSection('estados');
  selectEfTab('ANALISIS');
  const chip = document.querySelector("#efSubTabs [data-eftab='ANALISIS']");
  if (chip) chip.scrollIntoView({ behavior: 'smooth', inline: 'center' });
}
window.openAnalisisFinancieroSection = openAnalisisFinancieroSection;

function switchSection(targetId) {
  if (targetId === 'analisis') {
    openAnalisisFinancieroSection();
    return;
  }
  ACTIVE_SECTION = targetId;

  // Cerrar sidebar en celular si está abierto
  toggleMobileSidebar(false);

  document.querySelectorAll(".nav-item").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.target === targetId);
  });
  document.querySelectorAll(".section-view").forEach(sec => {
    sec.classList.toggle("active", sec.id === `sec-${targetId}`);
  });

  const empName = DB?.empresa?.razon_social || "ELECTROVIVIENDA S.A.S";
  const titles = {
    dashboard: [`Inicio & Resumen Ejecutivo — ${empName}`, "Control contable automatizado en tiempo real sincronizado con la carpeta CONTABILIDAD"],
    facturas: ["Facturas Realizadas & Vista Previa Oficial", "Facturas de venta emitidas, facturas de compra de proveedores y notas crédito/débito con su contabilización"],
    comprobantes: [`Comprobantes Contables (Comprobante Diario N° 1 al 47 y Hojas 1 a 60)`, "Consulta inmediata respetando la numeración exacta del Libro Diario y cada hoja de Excel"],
    facturacion: ["Emitir Factura / Registro Contable por Régimen", "Selecciona el régimen del comprador o vendedor y genera automáticamente liquidación, PUC, Kardex y Auxiliares"],
    auxiliares: [`Libros Auxiliares en Vivo — ${ACTIVE_PERIOD} 2026`, "Subcuentas (6 dígitos), Auxiliares por Tercero (8 dígitos) y Libro Auxiliar de Bancos actualizados en vivo"],
    kardex: ["Kardex de Productos — Promedio Ponderado", "Control permanente de existencias, entradas, salidas, devoluciones y costo promedio en vivo"],
    nomina: ["Nómina & Liquidación Laboral NIIF", "Gran planilla de sueldos, horas extras, auxilio de transporte, deducciones, aportes de seguridad social y provisiones"],
    estados: [`Estados Financieros NIIF & Libros Oficiales — ${ACTIVE_PERIOD} 2026`, "Situación Financiera (ESF), Resultados (ER), Consolidados, Flujo de Efectivo, Hoja de Trabajo y Mayor"],
    tributaria: ["Declaraciones Tributarias & Calendario Fiscal 2026", "Formularios Oficiales DIAN 350, 300, ReteICA Bucaramanga y alertas de vencimientos"],
    ia: ["Tutor de Inteligencia Artificial Contable (Entrenable)", "Pregunta cualquier tema de PUC, NIIF, impuestos o ejercicios y enseña nuevos conceptos a la IA"],
    reformas: ["Actualidad, Reformas y Leyes Contables en Colombia 2025-2026", "Reforma Tributaria, Reforma Pensional, Reducción Jornada Laboral, Facturación Electrónica DIAN y NIIF PYMES"]
  };
  if (titles[targetId]) {
    document.getElementById("topbarSectionTitle").textContent = titles[targetId][0];
    document.getElementById("topbarSectionSubtitle").textContent = titles[targetId][1];
  }
  renderSectionDidacticBanner(targetId);

  if (targetId === "nomina") {
    renderNominaSection();
  } else if (targetId === "tributaria") {
    renderTaxSection();
  }
}

function navGlobalPeriod(delta) {
  const months = (typeof ALL_12_MONTHS !== "undefined" && ALL_12_MONTHS.length)
    ? ALL_12_MONTHS
    : ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"];
  let idx = months.indexOf(ACTIVE_PERIOD);
  if (idx === -1) idx = 3;
  let nextIdx = (idx + delta + months.length) % months.length;
  setGlobalPeriod(months[nextIdx]);
}

function setGlobalPeriod(period) {
  ACTIVE_PERIOD = period;
  document.querySelectorAll(".period-pill").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.period === period);
  });
  const lblTop = document.getElementById("topbarPeriodDisplay");
  if (lblTop) lblTop.textContent = `${period} 2026`;
  const lbl1 = document.getElementById("btnActiveMonthLabel");
  if (lbl1) lbl1.textContent = period;
  const lbl2 = document.getElementById("efMonthLabel");
  if (lbl2) lbl2.textContent = period;
  const lbl3 = document.getElementById("compActiveMonthBadge");
  if (lbl3) lbl3.textContent = period;
  const lbl4 = document.getElementById("compMonthTitle");
  if (lbl4) lbl4.textContent = ACTIVE_VOUCHER_SCOPE === "ALL" ? "TODOS (1 AL 47)" : period;
  const lbl5 = document.getElementById("compScopeMonthLbl");
  if (lbl5) lbl5.textContent = period;
  const txMes = document.getElementById("txMes");
  if (txMes) txMes.value = period;

  // Sincronizar también el filtro de mes en la sección de Facturas Realizadas
  const invMonthSel = document.getElementById("invoiceMonthFilter");
  if (invMonthSel) invMonthSel.value = period;
  document.querySelectorAll("#invoiceMonthPills .filter-chip").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.invmonth === period);
  });

  ACTIVE_VOUCHER_SHEET = null;
  ACTIVE_INVOICE_ID = null;
  updateBadgesAndAlerts();
  renderDashboard();
  renderInvoicesSection();
  renderVouchersList();
  renderAuxiliaresSection();
  renderEstadosFinancieros();
  renderTaxSection();
  showToast(`Mes activo seleccionado: ${period} 2026`);
}

function downloadActiveMonthExcel() {
  const mesObj = DB?.meses?.[ACTIVE_PERIOD];
  const file = mesObj?.archivo || `${ACTIVE_PERIOD}.xlsx`;
  fetch(`/api/download/${encodeURIComponent(file)}`, { method: "HEAD" })
    .then(res => {
      if (res.ok) {
        window.location.href = `/api/download/${encodeURIComponent(file)}`;
      } else if (["ENERO.xlsx", "FEBRERO.xlsx", "MARZO.xlsx", "ABRIL.xlsx"].includes(file)) {
        const a = document.createElement("a");
        a.href = file;
        a.download = file;
        a.click();
      } else {
        exportMonthWorkbookClientSide(ACTIVE_PERIOD);
      }
    })
    .catch(() => {
      if (["ENERO.xlsx", "FEBRERO.xlsx", "MARZO.xlsx", "ABRIL.xlsx"].includes(file)) {
        const a = document.createElement("a");
        a.href = file;
        a.download = file;
        a.click();
      } else {
        exportMonthWorkbookClientSide(ACTIVE_PERIOD);
      }
    });
}

function exportMonthWorkbookClientSide(mes) {
  if (typeof XLSX === "undefined" || !DB) return;
  const wb = XLSX.utils.book_new();
  const mesData = DB.meses[mes] || { transacciones: [] };
  const rows = [
    [DB.empresa.razon_social, `NIT ${DB.empresa.nit}`, `MES: ${mes}`],
    ["COMPROBANTE DIARIO", "HOJA", "FECHA", "TIPO", "TERCERO", "CÓDIGO PUC", "CUENTA CONTABLE", "PARCIAL", "DEBE", "HABER"]
  ];
  (mesData.transacciones || []).forEach(tx => {
    (tx.asientos || []).forEach(a => {
      rows.push([
        tx.comprobante_diario || `Comprobante Hoja ${tx.hoja}`,
        tx.hoja,
        tx.fecha,
        tx.tipo,
        tx.tercero || "",
        a.codigo,
        a.cuenta,
        a.parcial || 0,
        a.debe || 0,
        a.haber || 0
      ]);
    });
  });
  const ws = XLSX.utils.aoa_to_sheet(rows);
  XLSX.utils.book_append_sheet(wb, ws, `LIBRO_${mes}`);
  XLSX.writeFile(wb, `${DB.empresa.razon_social.replace(/\s+/g, "_")}_${mes}.xlsx`);
  showToast(`Archivo Excel ${mes}.xlsx generado y descargado`);
}

function updateBadgesAndAlerts() {
  const cal = DB.calendario_tributario || [];
  const pendientes = cal.filter(c => !c.estado.includes("PAGADO") && !c.estado.includes("PRESENTADO"));
  const badgeCount = document.getElementById("notifBadgeCount");
  if (badgeCount) badgeCount.textContent = pendientes.length;
  const navAlertas = document.getElementById("navBadgeAlertas");
  if (navAlertas) navAlertas.textContent = pendientes.length;

  const txsMes = DB?.meses?.[ACTIVE_PERIOD]?.transacciones || [];
  const navComp = document.getElementById("navBadgeComprobantes");
  if (navComp) navComp.textContent = txsMes.length;

  const facturas = DB.facturas || [];
  const navFac = document.getElementById("navBadgeFacturas");
  if (navFac) navFac.textContent = facturas.length;

  const kardex = DB.kardex || [];
  const navKar = document.getElementById("navBadgeKardex");
  if (navKar) navKar.textContent = kardex.length;
}

// ============================================================================
// 1. SECCIÓN: DASHBOARD & FICHA EMPRESARIAL
// ============================================================================
const ALL_MONTHS = [
  "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
  "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
];
let UNLOCKED_NITS_IN_SESSION = new Set();

function renderDashboard() {
  const emp = DB.empresa;
  let totalTxs = 0;
  let ventasAcumuladas = 0;
  let capitalSocial = 0;
  let numDiarios = new Set();

  ALL_MONTHS.forEach(m => {
    if (!DB.meses[m]) {
      DB.meses[m] = { archivo: `${m}.xlsx`, hojas: ["PUC"], total_transacciones: 0, transacciones: [], hojas_especiales: {} };
    }
    const txs = DB.meses[m]?.transacciones || [];
    totalTxs += txs.length;
    txs.forEach(t => {
      if (t.num_comprobante_diario) numDiarios.add(t.num_comprobante_diario);
      (t.asientos || []).forEach(a => {
        if (String(a.codigo).startsWith("4135") && a.haber > 0) ventasAcumuladas += a.haber;
        if (String(a.codigo) === "3105" && a.haber > 0) capitalSocial += a.haber;
      });
    });
  });

  if (capitalSocial === 0 && (emp.socios || []).length) {
    capitalSocial = (emp.socios || []).reduce((acc, s) => acc + (Number(s.aporte) || 0), 0);
  }

  let invTotal = 0;
  (DB.kardex || []).forEach(p => {
    let cant = 0, val = 0;
    (p.movimientos || []).forEach(mv => {
      cant += (Number(mv.ent_cant) || 0) - (Number(mv.sal_cant) || 0);
      val += (Number(mv.ent_valor) || 0) - (Number(mv.sal_valor) || 0);
    });
    if (cant > 0 && val > 0) invTotal += val;
  });

  document.getElementById("dashboardKpiGrid").innerHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Aporte Social / Capital (3105)</div>
      <div class="kpi-value">${fmtCOP(capitalSocial)}</div>
      <div class="kpi-sub">${capitalSocial > 0 ? "Comprobante Diario N° 1 (Hoja 1)" : "Taller en $0 (Listo para iniciar)"}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Ingresos por Ventas (4135)</div>
      <div class="kpi-value">${fmtCOP(ventasAcumuladas)}</div>
      <div class="kpi-sub">${(DB.facturas || []).filter(f => f.categoria === "VENTA").length} Facturas de Venta Emitidas</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Inventario Kardex Actual (1435)</div>
      <div class="kpi-value">${fmtCOP(invTotal)}</div>
      <div class="kpi-sub">${(DB.kardex || []).length} Referencias Promedio Ponderado</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Comprobantes Diarios y Hojas</div>
      <div class="kpi-value">${numDiarios.size || totalTxs} Diarios / ${totalTxs} Hojas</div>
      <div class="kpi-sub">12 Meses Activos (Enero a Diciembre)</div>
    </div>
  `;

  document.getElementById("companyProfileBody").innerHTML = `
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:0.82rem;">
      <div><strong>Razón Social:</strong><br/>${emp.razon_social}</div>
      <div><strong>NIT y Dígito DIAN:</strong><br/><span class="code-col">${emp.nit}</span> (Dígito <strong>${emp.ultimo_digito_nit}</strong>)</div>
      <div><strong>Régimen Tributario:</strong><br/>${emp.regimen}</div>
      <div><strong>Marco Normativo:</strong><br/>${emp.grupo_niif}</div>
      <div><strong>Sistema de Inventarios:</strong><br/>${emp.sistema_inventario}</div>
      <div><strong>Domicilio Fiscal:</strong><br/>${emp.direccion} — ${emp.ciudad}</div>
    </div>
    <div style="margin-top:14px; border-top:1px solid var(--border-light); padding-top:10px;">
      <div style="font-size:0.75rem; font-weight:800; color:var(--brand-primary); margin-bottom:6px;">SOCIOS / TITULARES REGISTRADOS:</div>
      <div class="table-wrap">
        <table class="acct-table">
          <thead>
            <tr><th>Socio Accionista</th><th>Documento / NIT</th><th class="num-col">Aporte Social</th></tr>
          </thead>
          <tbody>
            ${(emp.socios && emp.socios.length) ? emp.socios.map(s => `
              <tr>
                <td><strong>${s.nombre}</strong></td>
                <td class="code-col">${s.documento}</td>
                <td class="num-col">${fmtCOP(s.aporte)}</td>
              </tr>
            `).join("") : `<tr><td colspan="3" style="color:var(--text-muted);">Taller en $0 (Sin aportes iniciales registrados aún)</td></tr>`}
          </tbody>
        </table>
      </div>
    </div>
  `;

  const files = ALL_MONTHS.map(m => ({
    label: `Libro Contable ${m} 2026`,
    file: DB.meses[m]?.archivo || `${m}.xlsx`,
    txs: DB.meses[m]?.total_transacciones || (DB.meses[m]?.transacciones || []).length || 0,
    sheets: (DB.meses[m]?.hojas || ["PUC"]).length,
    period: m
  }));

  document.getElementById("excelFilesTableBody").innerHTML = files.map(f => `
    <tr>
      <td><strong>${f.label}</strong></td>
      <td class="code-col">${f.file}</td>
      <td>${f.txs} reg.</td>
      <td>${f.sheets} hojas</td>
      <td>
        <div style="display:flex; gap:5px;">
          <button class="btn btn-outline btn-sm" onclick="setGlobalPeriod('${f.period}'); switchSection('comprobantes');">Ver (${f.txs})</button>
          <button class="btn btn-gold btn-sm" onclick="setGlobalPeriod('${f.period}'); downloadActiveMonthExcel();">📥 .xlsx</button>
        </div>
      </td>
    </tr>
  `).join("");

  const compRows = ALL_MONTHS.map(m => {
    const mData = DB.meses[m] || { transacciones: [], hojas_especiales: {} };
    let sumD = 0, sumH = 0;
    (mData.transacciones || []).forEach(t => {
      sumD += Number(t.total_debe) || 0;
      sumH += Number(t.total_haber) || 0;
    });
    const txsLen = (mData.transacciones || []).length;
    const espNames = Object.keys(mData.hojas_especiales || {}).join(", ") || (txsLen > 0 ? "Movimientos en Vivo" : "En $0 (Disponible para registrar)");
    return `
      <tr>
        <td><strong>${m} 2026</strong></td>
        <td><strong>${txsLen}</strong> hojas operativas</td>
        <td style="font-size:0.75rem; color:var(--text-secondary); max-width:340px;">${espNames}</td>
        <td class="num-col">${fmtCOP(sumD)}</td>
        <td class="num-col">${fmtCOP(sumH)}</td>
        <td><span class="status-pill ${txsLen > 0 ? "status-paid" : "status-pending"}">${txsLen > 0 ? "CUADRADO ✓" : "EN $0"}</span></td>
        <td>
          <button class="btn btn-primary btn-sm" onclick="setGlobalPeriod('${m}'); switchSection('comprobantes');">Abrir ${m}</button>
        </td>
      </tr>
    `;
  }).join("");
  document.getElementById("monthlyComparisonBody").innerHTML = compRows;
}

// ============================================================================
// 2. SECCIÓN: FACTURAS REALIZADAS Y VISTA PREVIA COMERCIAL + ASIENTO CONTABLE
// ============================================================================
function setInvoiceMonthFilter(monthVal) {
  const sel = document.getElementById("invoiceMonthFilter");
  if (sel) sel.value = monthVal;
  document.querySelectorAll("#invoiceMonthPills .filter-chip").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.invmonth === monthVal);
  });
  if (monthVal !== "ALL") {
    ACTIVE_PERIOD = monthVal;
    document.querySelectorAll(".period-pill").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.period === monthVal);
    });
    const lbl1 = document.getElementById("btnActiveMonthLabel");
    if (lbl1) lbl1.textContent = monthVal;
  }
  ACTIVE_INVOICE_ID = null;
  renderInvoicesSection();
}

function setInvoiceCategoryFilter(cat) {
  ACTIVE_INVOICE_CAT = cat;
  document.querySelectorAll("#invoiceCategoryTabs .filter-chip").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.invcat === cat);
  });
  ACTIVE_INVOICE_ID = null;
  renderInvoicesSection();
}

function normalizeInvoiceRecord(f) {
  const isVenta = f.categoria === "VENTA" || String(f.id || "").startsWith("NC-V");
  const tercero = f.tercero || (isVenta ? f.tercero_nombre : f.emisor_nombre) || "Tercero Comercial";
  const nitTercero = f.nit_tercero || (isVenta ? f.tercero_nit : f.emisor_nit) || "";
  const regVendedor = f.regimen_vendedor || f.emisor_regimen || "RRI • Autorretenedor Renta";
  const regComprador = f.regimen_comprador || f.tercero_regimen || "RRI • Agente de Retención";
  const tipoOp = f.tipo_operacion || (f.categoria === "VENTA" ? "FACTURA DE VENTA" : (f.categoria === "COMPRA" ? "FACTURA DE COMPRA / SOPORTE" : "NOTA CRÉDITO / DÉBITO / AJUSTE"));
  const txMatch = (DB?.meses?.[f.mes]?.transacciones || []).find(t => String(t.hoja) === String(f.hoja));
  const asientos = (f.asientos && f.asientos.length) ? f.asientos : (txMatch?.asientos || []);
  const totalDebe = f.total_debe || txMatch?.total_debe || f.total_neto || f.subtotal || 0;
  const totalHaber = f.total_haber || txMatch?.total_haber || f.total_neto || f.subtotal || 0;
  const compDiario = f.comprobante_diario || txMatch?.comprobante_diario || `Hoja ${f.hoja}`;
  const enunciado = f.enunciado || txMatch?.enunciado || f.observaciones || tipoOp;
  const items = (f.items || []).map((it, idx) => ({
    referencia: it.referencia || it.ref || `ITEM-0${idx + 1}`,
    descripcion: it.descripcion || "Artículo / Servicio",
    cantidad: it.cantidad || 1,
    valor_unitario: it.valor_unitario ?? it.vlr_unitario ?? 0,
    subtotal: it.subtotal || 0
  }));

  return Object.assign({}, f, {
    tercero,
    nit_tercero: nitTercero,
    regimen_vendedor: regVendedor,
    regimen_comprador: regComprador,
    tipo_operacion: tipoOp,
    enunciado,
    comprobante_diario: compDiario,
    asientos,
    total_debe: totalDebe,
    total_haber: totalHaber,
    items
  });
}

function renderInvoicesSection() {
  const rawInvoices = DB.facturas || [];
  const allInvoices = rawInvoices.map(normalizeInvoiceRecord);
  const monthFilter = document.getElementById("invoiceMonthFilter")?.value || "ALL";

  const hdrLbl = document.getElementById("invoiceActiveMonthHeaderLbl");
  if (hdrLbl) {
    hdrLbl.textContent = monthFilter === "ALL" ? "TODOS LOS MESES (ENERO - ABRIL)" : `${monthFilter} 2026`;
  }
  document.querySelectorAll("#invoiceMonthPills .filter-chip").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.invmonth === monthFilter);
  });

  const monthScoped = allInvoices.filter(f => monthFilter === "ALL" || f.mes === monthFilter);
  const ventas = monthScoped.filter(f => f.categoria === "VENTA");
  const compras = monthScoped.filter(f => f.categoria === "COMPRA");
  const devs = monthScoped.filter(f => f.categoria === "DEVOLUCION");
  const sumVentas = ventas.reduce((acc, f) => acc + (Number(f.subtotal) || 0), 0);
  const sumCompras = compras.reduce((acc, f) => acc + (Number(f.subtotal) || 0), 0);

  document.getElementById("invoicesKpiRow").innerHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Facturas en ${monthFilter === "ALL" ? "Enero - Abril" : monthFilter}</div>
      <div class="kpi-value">${monthScoped.length} Documentos</div>
      <div class="kpi-sub">Con vista previa comercial y asiento contable</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Facturas de Venta (${ventas.length})</div>
      <div class="kpi-value">${fmtCOP(sumVentas)}</div>
      <div class="kpi-sub">Ventas emitidas del período</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Facturas de Compra / Soportes (${compras.length})</div>
      <div class="kpi-value">${fmtCOP(sumCompras)}</div>
      <div class="kpi-sub">Compras, servicios y liquidaciones</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Notas Crédito / Débito (${devs.length})</div>
      <div class="kpi-value">${devs.length} Notas</div>
      <div class="kpi-sub">Devoluciones y notas de ajuste</div>
    </div>
  `;

  const filtered = monthScoped.filter(f => {
    const matchCat = ACTIVE_INVOICE_CAT === "ALL" || f.categoria === ACTIVE_INVOICE_CAT;
    if (!matchCat) return false;
    if (!ACTIVE_INVOICE_SEARCH) return true;
    const txt = `${f.numero} ${f.tercero} ${f.nit_tercero || ""} ${f.enunciado || ""} ${f.mes}`.toLowerCase();
    return txt.includes(ACTIVE_INVOICE_SEARCH);
  });

  const countEl = document.getElementById("invoiceListCountLabel");
  if (countEl) countEl.textContent = `${filtered.length} documentos`;
  const listEl = document.getElementById("invoicesListContainer");

  if (!filtered.length) {
    listEl.innerHTML = `<div style="padding:24px; text-align:center; color:var(--text-muted); background:var(--bg-surface); border-radius:10px;">No se encontraron facturas con este criterio de búsqueda o categoría en ${monthFilter}.</div>`;
    document.getElementById("invoicePreviewContainer").innerHTML = `<div class="card"><div class="card-body">Selecciona otra categoría o borra el texto del buscador arriba para visualizar las facturas.</div></div>`;
    return;
  }

  if (!ACTIVE_INVOICE_ID || !filtered.some(f => f.id === ACTIVE_INVOICE_ID)) {
    ACTIVE_INVOICE_ID = filtered[0].id;
  }

  listEl.innerHTML = filtered.map(f => {
    const isAct = f.id === ACTIVE_INVOICE_ID;
    const badgeColor = f.categoria === "VENTA" ? "status-paid" : (f.categoria === "COMPRA" ? "status-alert" : "status-pending");
    return `
      <div class="list-item-row ${isAct ? "active" : ""}" onclick="selectInvoicePreview('${f.id}')" style="padding:12px 14px; margin-bottom:8px; border-radius:10px; border:1.5px solid ${isAct ? 'var(--brand-gold)' : 'var(--border-light)'}; background:${isAct ? 'rgba(212,175,55,0.08)' : 'var(--bg-surface)'}; box-shadow:${isAct ? '0 3px 10px rgba(0,0,0,0.06)' : 'none'}; cursor:pointer; transition:all 0.15s ease;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
          <span style="font-family:'JetBrains Mono',monospace; font-weight:800; color:var(--brand-primary); font-size:0.86rem;">${f.numero}</span>
          <span class="status-pill ${badgeColor}" style="font-size:0.67rem; font-weight:800; padding:2px 8px;">${f.categoria}</span>
        </div>
        <div style="font-weight:700; font-size:0.82rem; color:var(--text-primary); margin-bottom:5px; line-height:1.25;">${f.tercero}</div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.74rem; color:var(--text-muted);">
          <span>📅 ${f.fecha} • <strong>${f.mes}</strong></span>
          <strong style="color:var(--brand-gold); font-size:0.85rem;">${fmtCOP(f.subtotal)}</strong>
        </div>
      </div>
    `;
  }).join("");

  const activeInv = filtered.find(f => f.id === ACTIVE_INVOICE_ID) || filtered[0];
  renderCommercialInvoicePreview(activeInv);
}

let ACTIVE_INVOICE_SEARCH = "";
function filterInvoicesBySearch(val) {
  ACTIVE_INVOICE_SEARCH = String(val || "").trim().toLowerCase();
  renderInvoicesSection();
}

function selectInvoicePreview(invId) {
  ACTIVE_INVOICE_ID = invId;
  renderInvoicesSection();
}

function renderCommercialInvoicePreview(inv) {
  const container = document.getElementById("invoicePreviewContainer");
  if (!inv) return;

  const isVenta = inv.categoria === "VENTA" || inv.tipo_operacion === "DEVOLUCIÓN EN VENTA";
  const emisorNombre = isVenta ? DB.empresa.razon_social : inv.tercero;
  const emisorNit = isVenta ? DB.empresa.nit : inv.nit_tercero;
  const emisorRegimen = isVenta ? inv.regimen_vendedor : inv.regimen_vendedor;
  const receptorNombre = isVenta ? inv.tercero : DB.empresa.razon_social;
  const receptorNit = isVenta ? inv.nit_tercero : DB.empresa.nit;
  const receptorRegimen = isVenta ? inv.regimen_comprador : inv.regimen_comprador;

  const itemsHtml = (inv.items && inv.items.length)
    ? inv.items.map((it, i) => `
        <tr>
          <td class="code-col">${it.referencia || `ITEM-0${i + 1}`}</td>
          <td><strong>${it.descripcion}</strong></td>
          <td class="num-col">${fmtNum(it.cantidad)}</td>
          <td class="num-col">${fmtCOP(it.valor_unitario)}</td>
          <td class="num-col"><strong>${fmtCOP(it.subtotal)}</strong></td>
        </tr>
      `).join("")
    : `
      <tr>
        <td class="code-col">MERC-01</td>
        <td><strong>${inv.enunciado || inv.tipo_operacion}</strong></td>
        <td class="num-col">1</td>
        <td class="num-col">${fmtCOP(inv.subtotal)}</td>
        <td class="num-col"><strong>${fmtCOP(inv.subtotal)}</strong></td>
      </tr>
    `;

  const asientosHtml = (inv.asientos || []).map(a => {
    const isSub = String(a.codigo).length >= 6 && a.debe === 0 && a.haber === 0;
    return `
      <tr>
        <td class="code-col">${a.codigo}</td>
        <td style="${isSub ? "padding-left:20px; color:var(--text-secondary); font-style:italic;" : "font-weight:700;"}">${a.cuenta}</td>
        <td class="num-col">${a.parcial ? fmtCOP(a.parcial) : ""}</td>
        <td class="num-col">${a.debe ? fmtCOP(a.debe) : ""}</td>
        <td class="num-col">${a.haber ? fmtCOP(a.haber) : ""}</td>
      </tr>
    `;
  }).join("");

  container.innerHTML = `
    <div style="display:flex; flex-direction:column; gap:16px;">
      <!-- VISTA PREVIA COMERCIAL DE LA FACTURA -->
      <div class="invoice-paper">
        <div class="invoice-top">
          <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
            ${isVenta ? `<div style="background:#ffffff; padding:6px 10px; border-radius:8px; border:1px solid #e2e8f0; display:flex; align-items:center; justify-content:center; box-shadow:0 2px 5px rgba(0,0,0,0.06);"><img src="${DB.empresa.logo || 'assets/logo-electrovivienda.png'}" alt="${DB.empresa.razon_social}" style="height:44px; width:auto; max-width:180px; object-fit:contain;" /></div>` : ''}
            <div class="invoice-brand">
              <h2>${emisorNombre}</h2>
              <p><strong>NIT:</strong> ${emisorNit} • <strong>Régimen:</strong> ${emisorRegimen}</p>
              <p>${isVenta ? DB.empresa.direccion : 'Operación Comercial'} — ${isVenta ? DB.empresa.ciudad : ''}</p>
              ${isVenta ? `<p>Tel: ${DB.empresa.telefono} • ${DB.empresa.correo}</p>` : ''}
            </div>
          </div>
          <div class="invoice-badge-box">
            <div class="doc-type">${inv.tipo_operacion}</div>
            <div class="doc-num">${inv.numero}</div>
            <div style="font-size:0.75rem; color:var(--text-secondary); margin-top:4px;">
              Fecha: <strong>${inv.fecha}</strong> • Mes: <strong>${inv.mes} (Hoja ${inv.hoja})</strong>
            </div>
          </div>
        </div>

        <div class="invoice-parties">
          <div class="party-box">
            <div class="party-label">🧑‍💼 VENDEDOR / EMISOR Y SU RÉGIMEN</div>
            <div class="party-name">${emisorNombre}</div>
            <div class="party-meta">
              <strong>NIT:</strong> ${emisorNit}<br/>
              <strong>Régimen Vendedor:</strong> ${inv.regimen_vendedor}
            </div>
          </div>
          <div class="party-box">
            <div class="party-label">🏢 COMPRADOR / ADQUIRIENTE Y SU RÉGIMEN</div>
            <div class="party-name">${receptorNombre}</div>
            <div class="party-meta">
              <strong>NIT / CC:</strong> ${receptorNit}<br/>
              <strong>Régimen Comprador:</strong> ${inv.regimen_comprador}<br/>
              <strong>Forma de Pago:</strong> ${inv.forma_pago || "Crédito / Giro Bancario"}
            </div>
          </div>
        </div>

        <div style="padding:18px 24px;">
          <div style="font-size:0.76rem; font-weight:800; color:var(--brand-primary); margin-bottom:8px;">
            DETALLE DE PRODUCTOS FACTURADOS (SINCRONIZADO CON KARDEX PROMEDIO PONDERADO):
          </div>
          <div class="table-wrap">
            <table class="acct-table">
              <thead>
                <tr>
                  <th>Referencia</th>
                  <th>Descripción del Producto / Electrodoméstico</th>
                  <th class="num-col">Cant.</th>
                  <th class="num-col">Vlr. Unitario</th>
                  <th class="num-col">Valor Total</th>
                </tr>
              </thead>
              <tbody>${itemsHtml}</tbody>
            </table>
          </div>
        </div>

        <div class="invoice-totals-row">
          <div>
            <div style="font-size:0.78rem; font-weight:700; color:var(--brand-primary); margin-bottom:4px;">Observaciones y Soporte Contable:</div>
            <p style="font-size:0.78rem; color:var(--text-secondary); margin-bottom:8px;">${inv.enunciado}</p>
            <div style="font-size:0.75rem; background:var(--brand-gold-soft); padding:8px 12px; border-radius:6px; border:1px solid var(--brand-gold);">
              <strong>Valor en Letras:</strong> ${inv.suma_letras || "Valor según liquidación oficial."}
            </div>
            <div style="margin-top:10px; display:flex; gap:8px; flex-wrap:wrap;">
              <button class="btn btn-outline btn-sm" onclick="setGlobalPeriod('${inv.mes}'); ACTIVE_VOUCHER_SHEET='${inv.mes}|${inv.hoja}'; switchSection('comprobantes');">
                📑 Ir al Comprobante Hoja ${inv.hoja} (${inv.mes})
              </button>
              <button class="btn btn-primary btn-sm" onclick="exportProfessionalInvoicePDF(false)">
                📄 Descargar PDF Factura Real (DIAN)
              </button>
              <button class="btn btn-gold btn-sm" onclick="exportProfessionalInvoicePDF(true)">
                📘 Descargar PDF Factura + Asiento Contable
              </button>
            </div>
          </div>

          <div class="totals-card">
            <div class="totals-line"><span>Subtotal Base Gravable:</span><strong>${fmtCOP(inv.subtotal)}</strong></div>
            <div class="totals-line"><span>(+) IVA Generado / Descontable (19%):</span><strong>${fmtCOP(inv.iva)}</strong></div>
            ${inv.retefuente ? `<div class="totals-line"><span>(-) Retención en la Fuente:</span><strong style="color:var(--brand-danger);">-${fmtCOP(inv.retefuente)}</strong></div>` : ""}
            ${inv.reteiva ? `<div class="totals-line"><span>(-) Retención de IVA (15%):</span><strong style="color:var(--brand-danger);">-${fmtCOP(inv.reteiva)}</strong></div>` : ""}
            ${inv.reteica ? `<div class="totals-line"><span>(-) ReteICA + Avisos + Bomberil:</span><strong style="color:var(--brand-danger);">-${fmtCOP(inv.reteica)}</strong></div>` : ""}
            ${inv.autorretencion ? `<div class="totals-line"><span>(±) Autorretención en Renta (135575 / 246575):</span><strong style="color:var(--brand-primary);">${fmtCOP(inv.autorretencion)}</strong></div>` : ""}
            <div class="totals-line grand">
              <span>NETO FACTURA / CAUSACIÓN:</span>
              <span>${fmtCOP(inv.total_neto)}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- REGISTRO CONTABLE ADJUNTO DE LA FACTURA -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">📘 Contabilización Oficial de esta Factura (Hoja ${inv.hoja} de ${inv.mes})</div>
          <span class="status-pill status-paid">SUMAS IGUALES: ${fmtCOP(inv.total_debe)}</span>
        </div>
        <div class="card-body">
          <div class="table-wrap">
            <table class="acct-table">
              <thead>
                <tr>
                  <th>Código PUC</th>
                  <th>Cuenta Contable y Auxiliar</th>
                  <th class="num-col">Parcial</th>
                  <th class="num-col">Debe</th>
                  <th class="num-col">Haber</th>
                </tr>
              </thead>
              <tbody>
                ${asientosHtml}
                <tr class="row-total">
                  <td colspan="2">SUMAS IGUALES DE LA FACTURA</td>
                  <td></td>
                  <td class="num-col">${fmtCOP(inv.total_debe)}</td>
                  <td class="num-col">${fmtCOP(inv.total_haber)}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  `;
}

// ============================================================================
// 3. SECCIÓN: COMPROBANTES DEL MES Y NUMERACIÓN OFICIAL (COMPROBANTE DIARIO 1 AL 47)
// ============================================================================
function getAllTransactionsAcrossMonths() {
  const list = [];
  ALL_MONTHS.forEach(m => {
    const txs = DB?.meses?.[m]?.transacciones || [];
    txs.forEach(t => {
      list.push(Object.assign({}, t, { mes: m }));
    });
  });
  return list;
}

function populateQuickComprobanteSelectors() {
  const selDiario = document.getElementById("quickSelectCompDiario");
  const selHoja = document.getElementById("quickSelectHojaExacta");
  if (!selDiario || !selHoja || !DB) return;

  const allTxs = getAllTransactionsAcrossMonths();

  // Agrupar por Comprobante Diario N° 1 al 47
  const byDiario = new Map();
  allTxs.forEach(t => {
    const numD = t.num_comprobante_diario || 0;
    const labelD = t.comprobante_diario || `Hoja ${t.hoja} (${t.mes})`;
    const key = numD > 0 ? `D-${numD}` : `H-${t.mes}-${t.hoja}`;
    if (!byDiario.has(key)) {
      byDiario.set(key, {
        key,
        num: numD || 999,
        label: numD > 0 ? `Comprobante Diario N° ${numD} — ${t.mes} (Hoja ${t.hoja}: ${(t.concepto_comprobante_diario || t.tipo || "").slice(0, 38)})` : `${labelD} — ${t.mes}`,
        mes: t.mes,
        hoja: t.hoja
      });
    } else {
      const existing = byDiario.get(key);
      if (!existing.label.includes(`, ${t.hoja}`)) {
        existing.label = existing.label.replace(")", `, ${t.hoja})`);
      }
    }
  });

  const sortedDiarios = Array.from(byDiario.values()).sort((a, b) => a.num - b.num);
  selDiario.innerHTML = `<option value="">-- Seleccionar Comprobante Diario (N° 1 al N° 47) --</option>` +
    sortedDiarios.map(d => `<option value="${d.mes}|${d.hoja}">${d.label}</option>`).join("");

  selHoja.innerHTML = `<option value="">-- Seleccionar por Hoja Exacta (${allTxs.length} Hojas) --</option>` +
    allTxs.map(t => `<option value="${t.mes}|${t.hoja}">Hoja ${t.hoja} (${t.mes}) — ${t.comprobante_diario || t.tipo} • ${(t.tercero || t.enunciado || "").slice(0, 34)}</option>`).join("");
}

function jumpToComprobanteDiario(val) {
  if (!val) return;
  const [mes, hoja] = val.split("|");
  ACTIVE_PERIOD = mes;
  document.querySelectorAll(".period-pill").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.period === mes);
  });
  ACTIVE_VOUCHER_CAT = "ALL";
  ACTIVE_VOUCHER_SHEET = `${mes}|${hoja}`;
  renderVouchersList();
  showToast(`Mostrando ${hoja} de ${mes}`);
}

function jumpToHojaExacta(val) {
  if (!val) return;
  jumpToComprobanteDiario(val);
}

function setVoucherScope(scope) {
  ACTIVE_VOUCHER_SCOPE = scope;
  const bMonth = document.getElementById("btnScopeMesActual");
  const bAll = document.getElementById("btnScopeTodos");
  if (bMonth) bMonth.className = scope === "MONTH" ? "btn btn-primary btn-sm" : "btn btn-outline btn-sm";
  if (bAll) bAll.className = scope === "ALL" ? "btn btn-primary btn-sm" : "btn btn-outline btn-sm";
  const lblTitle = document.getElementById("compMonthTitle");
  if (lblTitle) lblTitle.textContent = scope === "ALL" ? "TODOS (DIARIO 1 AL 47)" : ACTIVE_PERIOD;
  ACTIVE_VOUCHER_SHEET = null;
  renderVouchersList();
}

function classifyVoucherCategory(tx) {
  const t = (tx.tipo || "").toUpperCase();
  const h = String(tx.hoja || "").toUpperCase();
  const en = (tx.enunciado || "").toUpperCase();
  if (t.includes("EGRESO")) return "EGRESO";
  if (t.includes("INGRESO")) return "INGRESO";
  if (t.includes("FACTURA") || t.includes("NOTA") || en.includes("VENDE MERCANC") || en.includes("COMPRA MERCANC") || en.includes("DEVOLUCI")) return "FACTURA";
  if (h.startsWith("AD") || en.includes("NÓMINA") || en.includes("NOMINA") || en.includes("SEGURIDAD SOCIAL")) return "NOMINA";
  return "CONTABLE";
}

function setVoucherCategoryFilter(cat) {
  ACTIVE_VOUCHER_CAT = cat;
  document.querySelectorAll("#voucherCategoryTabs .filter-chip").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.vcat === cat);
  });
  if (cat === "DIARIO") {
    setVoucherScope("ALL");
    return;
  }
  ACTIVE_VOUCHER_SHEET = null;
  renderVouchersList();
}

function setVoucherViewMode(mode) {
  VOUCHER_VIEW_MODE = mode;
  renderVoucherDetail();
}

function renderVouchersList() {
  const sourceTxs = ACTIVE_VOUCHER_SCOPE === "ALL"
    ? getAllTransactionsAcrossMonths()
    : (DB?.meses?.[ACTIVE_PERIOD]?.transacciones || []).map(t => Object.assign({}, t, { mes: ACTIVE_PERIOD }));

  const q = (document.getElementById("searchVoucherInput")?.value || "").toLowerCase().trim();

  const filtered = sourceTxs.filter(tx => {
    const cat = classifyVoucherCategory(tx);
    const matchCat = (ACTIVE_VOUCHER_CAT === "ALL" || ACTIVE_VOUCHER_CAT === "DIARIO") || cat === ACTIVE_VOUCHER_CAT;
    const compDiarioStr = (tx.comprobante_diario || "").toLowerCase();
    const numDiarioStr = tx.num_comprobante_diario ? `comprobante diario ${tx.num_comprobante_diario}` : "";
    const matchQ = !q ||
      String(tx.hoja).toLowerCase().includes(q) ||
      compDiarioStr.includes(q) ||
      numDiarioStr.includes(q) ||
      (tx.tipo || "").toLowerCase().includes(q) ||
      (tx.enunciado || "").toLowerCase().includes(q) ||
      (tx.tercero || "").toLowerCase().includes(q) ||
      (tx.cheque || "").toLowerCase().includes(q);
    return matchCat && matchQ;
  });

  document.getElementById("voucherFilteredCount").textContent = `${filtered.length} comprobantes`;
  const container = document.getElementById("vouchersListContainer");

  if (!filtered.length) {
    container.innerHTML = `<div style="padding:20px; text-align:center; color:var(--text-muted);">No hay comprobantes en esta categoría o búsqueda.</div>`;
    document.getElementById("voucherDetailPanel").innerHTML = `<div class="card"><div class="card-body">Selecciona otra categoría o limpia el buscador.</div></div>`;
    return;
  }

  if (!ACTIVE_VOUCHER_SHEET || !filtered.some(t => `${t.mes}|${t.hoja}` === ACTIVE_VOUCHER_SHEET || String(t.hoja) === String(ACTIVE_VOUCHER_SHEET))) {
    ACTIVE_VOUCHER_SHEET = `${filtered[0].mes}|${filtered[0].hoja}`;
  }

  container.innerHTML = filtered.map(tx => {
    const itemKey = `${tx.mes}|${tx.hoja}`;
    const isAct = (ACTIVE_VOUCHER_SHEET === itemKey || String(tx.hoja) === String(ACTIVE_VOUCHER_SHEET));
    const numDiarioBadge = tx.num_comprobante_diario
      ? `<span style="background:var(--brand-gold-soft); color:var(--brand-primary); border:1px solid var(--brand-gold); font-size:0.66rem; font-weight:800; padding:1px 6px; border-radius:4px;">Comp. Diario N° ${tx.num_comprobante_diario}</span>`
      : "";
    return `
      <div class="list-item-row ${isAct ? "active" : ""}" onclick="selectVoucherSheet('${tx.mes}', '${tx.hoja}')" style="padding:12px 14px; margin-bottom:8px; border-radius:10px; border:1.5px solid ${isAct ? 'var(--brand-gold)' : 'var(--border-light)'}; background:${isAct ? 'rgba(212,175,55,0.08)' : 'var(--bg-surface)'}; box-shadow:${isAct ? '0 3px 10px rgba(0,0,0,0.06)' : 'none'}; cursor:pointer; transition:all 0.15s ease;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
          <span style="font-family:'JetBrains Mono',monospace; font-weight:800; color:var(--brand-primary); font-size:0.83rem;">Hoja ${tx.hoja} (${tx.mes})</span>
          ${numDiarioBadge}
        </div>
        <div style="font-weight:700; font-size:0.81rem; color:var(--text-primary); margin-bottom:5px; line-height:1.3;">${(tx.enunciado || tx.concepto_soporte || tx.tipo).slice(0, 80)}</div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.73rem; color:var(--text-muted);">
          <span>👤 ${(tx.tercero || tx.tipo || "Contabilidad").slice(0, 24)}</span>
          <strong style="color:var(--brand-gold); font-size:0.84rem;">${fmtCOP(tx.total_debe)}</strong>
        </div>
      </div>
    `;
  }).join("");

  renderVoucherDetail();
}

function selectVoucherSheet(mes, hoja) {
  ACTIVE_VOUCHER_SHEET = `${mes}|${hoja}`;
  renderVouchersList();
}

function renderVoucherDetail() {
  const panel = document.getElementById("voucherDetailPanel");
  if (!panel || !DB) return;

  let mes = ACTIVE_PERIOD;
  let hoja = ACTIVE_VOUCHER_SHEET;
  if (String(ACTIVE_VOUCHER_SHEET || "").includes("|")) {
    const parts = String(ACTIVE_VOUCHER_SHEET).split("|");
    mes = parts[0];
    hoja = parts[1];
  }

  const txs = DB?.meses?.[mes]?.transacciones || [];
  const tx = txs.find(t => String(t.hoja) === String(hoja)) || txs[0];
  if (!tx) {
    panel.innerHTML = `<div class="card"><div class="card-body">No se encontró el comprobante seleccionado.</div></div>`;
    return;
  }

  if (VOUCHER_VIEW_MODE === "grid") {
    panel.innerHTML = `
      <div class="card">
        <div class="card-header">
          <div class="card-title">📊 Hoja Excel Original: Hoja "${tx.hoja}" (${mes}.xlsx) — ${tx.comprobante_diario || tx.tipo}</div>
          <button class="btn btn-outline btn-sm" onclick="setVoucherViewMode('voucher')">Volver a Vista Comprobante</button>
        </div>
        <div class="card-body">${renderExcelGridHtml(tx.rows || [])}</div>
      </div>
    `;
    return;
  }

  const asientosHtml = (tx.asientos || []).map(a => {
    const isSub = String(a.codigo).length >= 6 && a.debe === 0 && a.haber === 0;
    return `
      <tr>
        <td class="code-col">${a.codigo}</td>
        <td style="${isSub ? "padding-left:20px; color:var(--text-secondary); font-style:italic;" : "font-weight:700;"}">${a.cuenta}</td>
        <td class="num-col">${a.parcial ? fmtCOP(a.parcial) : ""}</td>
        <td class="num-col">${a.debe ? fmtCOP(a.debe) : ""}</td>
        <td class="num-col">${a.haber ? fmtCOP(a.haber) : ""}</td>
      </tr>
    `;
  }).join("");

  const compDiarioTitle = tx.comprobante_diario || `Comprobante Operativo Hoja ${tx.hoja}`;

  panel.innerHTML = `
    <div class="invoice-paper">
      <div class="invoice-top">
        <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
          <div style="background:#ffffff; padding:6px 10px; border-radius:8px; border:1px solid #e2e8f0; display:flex; align-items:center; justify-content:center; box-shadow:0 2px 5px rgba(0,0,0,0.06);">
            <img src="${DB.empresa.logo || 'assets/logo-electrovivienda.png'}" alt="${DB.empresa.razon_social}" style="height:44px; width:auto; max-width:180px; object-fit:contain;" />
          </div>
          <div class="invoice-brand">
            <h2>${DB.empresa.razon_social}</h2>
            <p><strong>NIT:</strong> ${DB.empresa.nit} • ${DB.empresa.regimen}</p>
            <p>${DB.empresa.direccion} — ${DB.empresa.ciudad}</p>
          </div>
        </div>
        <div class="invoice-badge-box">
          <div class="doc-type">${compDiarioTitle}</div>
          <div class="doc-num">Hoja N° ${tx.hoja} (${mes})</div>
          <div style="font-size:0.75rem; color:var(--text-secondary); margin-top:4px;">
            Documento: <strong>${tx.tipo}</strong> • Fecha: <strong>${tx.fecha}</strong>
          </div>
        </div>
      </div>

      <div class="invoice-parties">
        <div class="party-box">
          <div class="party-label">📌 ENUNCIADO DE LA OPERACIÓN (HOJA ${tx.hoja} DE ${mes})</div>
          <div style="font-size:0.84rem; font-weight:700; color:var(--text-primary); line-height:1.45;">
            ${tx.enunciado || tx.concepto_soporte || "Registro contable del período"}
          </div>
          ${tx.concepto_comprobante_diario ? `<div style="margin-top:6px; font-size:0.75rem; color:var(--brand-primary); font-weight:700;">📘 Libro Diario: ${tx.comprobante_diario} — ${tx.concepto_comprobante_diario}</div>` : ""}
        </div>
        <div class="party-box">
          <div class="party-label">🧾 DATOS DEL DOCUMENTO SOPORTE Y TERCERO</div>
          <div class="party-meta">
            <strong>Tercero / Beneficiario:</strong> ${tx.tercero || DB.empresa.razon_social}<br/>
            <strong>NIT / CC:</strong> <span class="code-col">${tx.nit_tercero || DB.empresa.nit}</span><br/>
            <strong>Cheque / Pago / Referencia:</strong> ${tx.cheque || "Contado / Causación"}<br/>
            <strong>La Suma de (Letras):</strong> ${tx.suma_letras || fmtCOP(tx.total_debe)}
          </div>
        </div>
      </div>

      <div style="padding:18px 24px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
          <span style="font-size:0.78rem; font-weight:800; color:var(--brand-primary);">
            CONTABILIZACIÓN OFICIAL — ${compDiarioTitle.toUpperCase()} (HOJA ${tx.hoja})
          </span>
          <div style="display:flex; align-items:center; gap:8px;">
            <span class="status-pill status-paid">SUMAS IGUALES: ${fmtCOP(tx.total_debe)}</span>
            <button class="btn btn-primary btn-sm" onclick="exportProfessionalVoucherPDF()">
              📄 Descargar PDF Comprobante / Asiento
            </button>
          </div>
        </div>

        <div class="table-wrap">
          <table class="acct-table">
            <thead>
              <tr>
                <th>Código PUC</th>
                <th>Cuenta Contable / Subcuenta / Auxiliar</th>
                <th class="num-col">Parcial</th>
                <th class="num-col">Debe (Débitos)</th>
                <th class="num-col">Haber (Créditos)</th>
              </tr>
            </thead>
            <tbody>
              ${asientosHtml}
              <tr class="row-total">
                <td colspan="2">SUMAS IGUALES DEL COMPROBANTE</td>
                <td></td>
                <td class="num-col">${fmtCOP(tx.total_debe)}</td>
                <td class="num-col">${fmtCOP(tx.total_haber)}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:16px; padding-top:12px; border-top:1px dashed var(--border-strong); font-size:0.75rem; text-align:center;">
          <div><strong>Elaborado por:</strong><br/>${tx.elaborado_por || DB.empresa.elaborado_por || "Gina Villamizar"}</div>
          <div><strong>Revisado por:</strong><br/>Auditoría Interna NIIF</div>
          <div><strong>Aprobado por:</strong><br/>Kevin Guerrero (Representante Legal)</div>
          <div><strong>Firma y Sello:</strong><br/>Contabilidad verificada ✓</div>
        </div>
      </div>
    </div>
  `;
}

// ============================================================================
// 4. SECCIÓN: GENERADOR DE FACTURAS CON MATRIZ DE REGÍMENES COMPRADOR VS VENDEDOR
// ============================================================================
function populateProductSelect() {
  const sel = document.getElementById("txProductoId");
  if (!sel || !DB) return;
  const kardexList = DB.kardex || [];
  const optionsHtml = kardexList.map(p => {
    let cant = 0, val = 0, prom = 0;
    (p.movimientos || []).forEach(m => {
      cant += (Number(m.ent_cant) || 0) - (Number(m.sal_cant) || 0);
      val += (Number(m.ent_valor) || 0) - (Number(m.sal_valor) || 0);
      prom = Number(m.promedio) || prom;
    });
    if (cant > 0 && val > 0) prom = Math.round(val / cant);
    return `<option value="${p.id}" data-promedio="${prom}" data-cant="${cant}" data-val="${val}" data-precio="${p.precio_venta_sugerido || Math.round(prom * 1.35)}">${p.referencia} — ${p.articulo} (Saldo: ${cant} und | Prom: ${fmtCOP(prom)})</option>`;
  }).join("");

  sel.innerHTML = optionsHtml + `<option value="__NEW__" data-promedio="0" data-cant="0" data-val="0" data-precio="0">➕ Crear Nuevo Artículo en Kardex Automáticamente...</option>`;
  onSelectProductoKardex();
}

function onSelectProductoKardex() {
  const sel = document.getElementById("txProductoId");
  if (!sel || !sel.selectedOptions.length) return;
  const opt = sel.selectedOptions[0];
  const isNew = sel.value === "__NEW__";
  const newFields = document.getElementById("newKardexProductFields");
  if (newFields) {
    newFields.style.display = isNew ? "grid" : "none";
  }

  const prom = Number(opt.dataset.promedio) || 0;
  const precio = Number(opt.dataset.precio) || prom;
  const tipo = document.getElementById("txTipoOperacion")?.value || "VENTA";

  if (isNew) {
    const nextIdx = ((DB?.kardex || []).length || 0) + 1;
    const refInput = document.getElementById("txNuevoProdRef");
    if (refInput && (!refInput.value || refInput.value.startsWith("PROD-"))) {
      refInput.value = `PROD-00${nextIdx}`;
    }
    const vUnitActual = Number(document.getElementById("txValorUnitario")?.value) || 2500000;
    document.getElementById("txCostoPromedioKardex").value = (tipo === "COMPRA" || tipo === "DEV_COMPRA") ? vUnitActual : Math.round(vUnitActual * 0.72);
  } else {
    document.getElementById("txCostoPromedioKardex").value = Math.round(prom);
    if (tipo === "VENTA" || tipo === "DEV_VENTA") {
      document.getElementById("txValorUnitario").value = Math.round(precio || prom * 1.35 || 1500000);
    } else {
      document.getElementById("txValorUnitario").value = Math.round(prom || 1000000);
    }
  }
  recalcLiveTransaction();
}

function resolveOrCreateAuxiliaryAccount(subcuenta6, entityName, entityNit, prefixLabel) {
  const cleanSub = String(subcuenta6 || "130505").slice(0, 6);
  const nameNorm = String(entityName || "Tercero").trim();
  const nitNorm = String(entityNit || "").trim();
  const searchKey = nameNorm.toLowerCase();
  const nitDigits = nitNorm.replace(/[^0-9]/g, "");

  const pucList = DB?.puc || [];
  // 1. Buscar si ya existe un auxiliar de 8 dígitos para esta subcuenta y este tercero/producto en el PUC
  const existingInPuc = pucList.filter(c => {
    const code = String(c.codigo || "").trim();
    return code.startsWith(cleanSub) && code.length >= 8;
  });

  for (const item of existingInPuc) {
    const nLower = String(item.nombre || "").toLowerCase();
    if ((searchKey && nLower.includes(searchKey)) || (nitDigits && nitDigits.length >= 5 && nLower.includes(nitDigits))) {
      return {
        codigo: String(item.codigo).trim(),
        nombre: item.nombre,
        esNuevo: false
      };
    }
  }

  // 2. Buscar también en los asientos de las transacciones de todos los meses
  const usedCodes = new Set(existingInPuc.map(x => String(x.codigo).trim()));
  for (const m of ALL_12_MONTHS) {
    const txs = DB?.meses?.[m]?.transacciones || [];
    for (const tx of txs) {
      for (const a of (tx.asientos || [])) {
        const ac = String(a.codigo || "").trim();
        if (ac.startsWith(cleanSub) && ac.length >= 8) {
          usedCodes.add(ac);
          const ctaLow = String(a.cuenta || "").toLowerCase();
          const txTerLow = String(tx.tercero || "").toLowerCase();
          if (searchKey && (ctaLow.includes(searchKey) || txTerLow === searchKey)) {
            return {
              codigo: ac,
              nombre: a.cuenta || `${prefixLabel} ${nameNorm}`,
              esNuevo: false
            };
          }
        }
      }
    }
  }

  // 3. Si no existe, generar automáticamente el siguiente consecutivo de 8 dígitos (ej: 13050501, 13050502...)
  let seq = 1;
  while (seq < 99) {
    const candidate = `${cleanSub}${String(seq).padStart(2, "0")}`;
    if (!usedCodes.has(candidate)) {
      const fullLabel = nitNorm
        ? `${prefixLabel} ${nameNorm} (NIT ${nitNorm})`
        : `${prefixLabel} ${nameNorm}`;
      return {
        codigo: candidate,
        nombre: fullLabel,
        esNuevo: true
      };
    }
    seq++;
  }
  return {
    codigo: `${cleanSub}99`,
    nombre: `${prefixLabel} ${nameNorm}`,
    esNuevo: true
  };
}

function onChangeTipoOperacion() {
  const tipo = document.getElementById("txTipoOperacion")?.value || "VENTA";
  const selReg = document.getElementById("txRegimenTercero");
  const lblMiRol = document.getElementById("lblMiRolRegimen");
  const lblContraRol = document.getElementById("lblContraparteRolRegimen");
  const kardexBlock = document.getElementById("kardexInputBlock");

  if (!selReg) return;

  const isVentaSide = (tipo === "VENTA" || tipo === "DEV_VENTA" || tipo === "INGRESO");
  if (isVentaSide) {
    if (lblMiRol) lblMiRol.textContent = "VENDEDOR (NUESTRA EMPRESA)";
    if (lblContraRol) lblContraRol.textContent = "SELECCIONA EL RÉGIMEN DEL COMPRADOR (CLIENTE)";
    selReg.innerHTML = REGIMENES_VENTA_COMPRADOR.map(r => `<option value="${r.id}">${r.label}</option>`).join("");
  } else {
    if (lblMiRol) lblMiRol.textContent = "COMPRADOR (NUESTRA EMPRESA)";
    if (lblContraRol) lblContraRol.textContent = "SELECCIONA EL RÉGIMEN DEL VENDEDOR (PROVEEDOR)";
    selReg.innerHTML = REGIMENES_COMPRA_VENDEDOR.map(r => `<option value="${r.id}">${r.label}</option>`).join("");
  }

  if (kardexBlock) {
    kardexBlock.style.display = (tipo === "EGRESO" || tipo === "INGRESO") ? "none" : "block";
  }

  applyRegimenMatrix();
}

function getActiveRegimenRule() {
  const tipo = document.getElementById("txTipoOperacion")?.value || "VENTA";
  const regId = document.getElementById("txRegimenTercero")?.value;
  const isVentaSide = (tipo === "VENTA" || tipo === "DEV_VENTA" || tipo === "INGRESO");
  const list = isVentaSide ? REGIMENES_VENTA_COMPRADOR : REGIMENES_COMPRA_VENDEDOR;
  return list.find(r => r.id === regId) || list[0];
}

function applyRegimenMatrix() {
  const rule = getActiveRegimenRule();
  if (!rule) return;

  document.getElementById("chkIva").checked = !!rule.aplica_iva;
  document.getElementById("chkRetefuente").checked = !!rule.aplica_retefuente;
  document.getElementById("chkAutorretencion").checked = !!rule.aplica_autorretencion;
  document.getElementById("chkReteIva").checked = !!rule.aplica_reteiva;
  document.getElementById("chkReteIca").checked = !!rule.aplica_reteica;

  document.getElementById("lblTarifaRete").textContent = `${(rule.tarifa_retefuente * 100).toFixed(1)}%`;
  document.getElementById("lblTarifaAuto").textContent = `${(rule.tarifa_autorretencion * 100).toFixed(1)}%`;

  renderAntesDeLiquidacionTable(rule);
  recalcLiveTransaction();
}

function renderAntesDeLiquidacionTable(rule) {
  const box = document.getElementById("antesDeLiquidacionBox");
  if (!box || !rule) return;
  const tipo = document.getElementById("txTipoOperacion")?.value || "VENTA";
  const isVentaSide = (tipo === "VENTA" || tipo === "DEV_VENTA" || tipo === "INGRESO");
  const miRegimen = `${DB?.empresa?.razon_social || "ELECTROVIVIENDA S.A.S"} (RRI • Agente Retenedor y Autorretenedor Renta)`;
  const compradorTxt = isVentaSide ? rule.label : miRegimen;
  const vendedorTxt = isVentaSide ? miRegimen : rule.label;

  box.innerHTML = `
    <div class="table-wrap">
      <table class="acct-table" style="background:#fff;">
        <thead>
          <tr>
            <th>COMPRADOR</th>
            <th>VENDEDOR</th>
            <th>IVA (19%)</th>
            <th>RETEFUENTE RENTA</th>
            <th>AUTORRETENCIÓN RENTA</th>
            <th>RETEIVA (15%)</th>
            <th>RETEICA + AVISOS + BOMBERIL</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>${compradorTxt}</strong></td>
            <td><strong>${vendedorTxt}</strong></td>
            <td><span class="status-pill ${rule.aplica_iva ? "status-paid" : "status-pending"}">${rule.aplica_iva ? "SÍ (19%)" : "NO (0%)"}</span></td>
            <td><span class="status-pill ${rule.aplica_retefuente ? "status-paid" : "status-pending"}">${rule.nota_retefuente}</span></td>
            <td><span class="status-pill ${rule.aplica_autorretencion ? "status-paid" : "status-pending"}">${rule.nota_autorretencion}</span></td>
            <td><span class="status-pill ${rule.aplica_reteiva ? "status-paid" : "status-pending"}">${rule.nota_reteiva}</span></td>
            <td><span class="status-pill ${rule.aplica_reteica ? "status-paid" : "status-pending"}">${rule.nota_reteica}</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  `;
}

function recalcLiveTransaction() {
  const rule = getActiveRegimenRule();
  const tipo = document.getElementById("txTipoOperacion")?.value || "VENTA";
  const cant = Number(document.getElementById("txCantidad")?.value) || 1;
  const vUnit = Number(document.getElementById("txValorUnitario")?.value) || 0;
  const cProm = Number(document.getElementById("txCostoPromedioKardex")?.value) || 0;
  const formaPago = document.getElementById("txFormaPago")?.value || "CREDITO";
  const tercero = document.getElementById("txTercero")?.value?.trim() || "Tercero Comercial";
  const nitTercero = document.getElementById("txNitTercero")?.value?.trim() || "900.000.000-1";
  const mes = document.getElementById("txMes")?.value || ACTIVE_PERIOD || "ABRIL";
  const hoja = document.getElementById("txHoja")?.value?.trim() || "61";
  const numFactura = document.getElementById("txNumFactura")?.value?.trim() || `Doc N° ${hoja}`;

  const base = (tipo === "EGRESO" || tipo === "INGRESO") ? vUnit : Math.round(cant * vUnit);
  const costoTotal = Math.round(cant * cProm);

  const chkIva = document.getElementById("chkIva")?.checked;
  const chkRete = document.getElementById("chkRetefuente")?.checked;
  const chkAuto = document.getElementById("chkAutorretencion")?.checked;
  const chkAutoEsp = document.getElementById("chkAutoEspecial")?.checked;
  const chkReteIva = document.getElementById("chkReteIva")?.checked;
  const chkReteIca = document.getElementById("chkReteIca")?.checked;

  const iva = chkIva ? Math.round(base * 0.19) : 0;
  const tarifaRete = rule ? rule.tarifa_retefuente : 0.025;
  const tarifaAuto = rule ? rule.tarifa_autorretencion : 0.025;

  const retefuente = chkRete ? Math.round(base * tarifaRete) : 0;
  const autorretencion = chkAuto ? Math.round(base * tarifaAuto) : 0;
  const autoEspecial = chkAutoEsp ? Math.round(base * 0.0055) : 0;
  const reteiva = chkReteIva ? Math.round(iva * 0.15) : 0;
  const reteica = chkReteIca ? Math.round(base * 0.0096) : 0;
  const avisos = chkReteIca ? Math.round(reteica * 0.15) : 0;
  const bomberil = chkReteIca ? Math.round(reteica * 0.10) : 0;
  const totalIcaPaquete = reteica + avisos + bomberil;

  const isVentaSide = (tipo === "VENTA" || tipo === "DEV_VENTA");
  const neto = base + iva - retefuente - reteiva - totalIcaPaquete;

  document.getElementById("liveBaseBadge").textContent = `Subtotal: ${fmtCOP(base)} | Neto: ${fmtCOP(neto)}`;

  const prodSelect = document.getElementById("txProductoId");
  const isNewProd = !prodSelect || prodSelect.value === "__NEW__" || !(DB?.kardex || []).length;
  const nuevoProdRef = (document.getElementById("txNuevoProdRef")?.value || "PROD-005").trim();
  const nuevoProdNombre = (document.getElementById("txNuevoProdNombre")?.value || "Mercancía General").trim();

  let prodRef = nuevoProdRef;
  let prodName = nuevoProdNombre;
  let existCant = 0, existVal = 0, existProm = cProm;

  if (!isNewProd && prodSelect) {
    const prodObj = (DB?.kardex || []).find(p => p.id === prodSelect.value);
    if (prodObj) {
      prodRef = prodObj.referencia || prodObj.id;
      prodName = prodObj.articulo;
      (prodObj.movimientos || []).forEach(mv => {
        existCant += (Number(mv.ent_cant) || 0) - (Number(mv.sal_cant) || 0);
        existVal += (Number(mv.ent_valor) || 0) - (Number(mv.sal_valor) || 0);
        existProm = Number(mv.promedio) || existProm;
      });
      if (existCant > 0 && existVal > 0) existProm = Math.round(existVal / existCant);
    }
  }

  // Resolver o autogenerar Cuentas Auxiliares de 8 dígitos para que nada quede suelto
  const auxCliente = resolveOrCreateAuxiliaryAccount("130505", tercero, nitTercero, "Cliente");
  const auxProveedor = resolveOrCreateAuxiliaryAccount("220505", tercero, nitTercero, "Proveedor");
  const auxKardexProd = resolveOrCreateAuxiliaryAccount("143536", `${prodRef} ${prodName}`, "", "Kardex");

  const nuevosAuxiliaresPuc = [];
  if ((isVentaSide || tipo === "INGRESO") && formaPago === "CREDITO" && auxCliente.esNuevo) {
    nuevosAuxiliaresPuc.push(auxCliente);
  }
  if ((!isVentaSide || tipo === "EGRESO") && (formaPago === "CREDITO" || tipo === "EGRESO") && auxProveedor.esNuevo) {
    nuevosAuxiliaresPuc.push(auxProveedor);
  }
  if (tipo !== "EGRESO" && tipo !== "INGRESO" && auxKardexProd.esNuevo) {
    nuevosAuxiliaresPuc.push(auxKardexProd);
  }

  document.getElementById("liveLiquidacionPreview").innerHTML = `
    <div style="font-size:0.8rem; display:flex; flex-direction:column; gap:6px;">
      <div style="display:flex; justify-content:space-between;"><span>Producto Kardex (${prodRef}):</span><strong>${prodName} (${cant} und)</strong></div>
      <div style="display:flex; justify-content:space-between;"><span>Auxiliar Tercero Encadenado:</span><strong class="code-col">${isVentaSide ? auxCliente.codigo : auxProveedor.codigo} — ${tercero}</strong></div>
      <div style="display:flex; justify-content:space-between;"><span>Subtotal Base Gravable:</span><strong>${fmtCOP(base)}</strong></div>
      <div style="display:flex; justify-content:space-between;"><span>(+) IVA (19%):</span><strong>${fmtCOP(iva)}</strong></div>
      <div style="display:flex; justify-content:space-between;"><span>(-) Retención en la Fuente (${(tarifaRete * 100).toFixed(1)}%):</span><strong style="color:var(--brand-danger);">-${fmtCOP(retefuente)}</strong></div>
      <div style="display:flex; justify-content:space-between;"><span>(-) ReteIVA (15% del IVA):</span><strong style="color:var(--brand-danger);">-${fmtCOP(reteiva)}</strong></div>
      <div style="display:flex; justify-content:space-between;"><span>(-) ReteICA (9.6‰) + Avisos (15%) + Bomberil (10%):</span><strong style="color:var(--brand-danger);">-${fmtCOP(totalIcaPaquete)}</strong></div>
      <div style="display:flex; justify-content:space-between;"><span>(±) Autorretención Renta (${(tarifaAuto * 100).toFixed(1)}%):</span><strong style="color:var(--brand-primary);">${fmtCOP(autorretencion + autoEspecial)}</strong></div>
      <div style="display:flex; justify-content:space-between; border-top:2px solid var(--brand-primary); padding-top:6px; font-size:0.92rem;">
        <strong>VALOR NETO FACTURA / CAUSACIÓN:</strong>
        <strong style="color:var(--brand-primary);">${fmtCOP(neto)}</strong>
      </div>
    </div>
  `;

  // Construir Asientos PUC exactos con Auxiliares de 8 dígitos encadenados
  const asientos = [];
  const cuentaPagoVenta = formaPago === "BANCO" ? ["1110", "BANCOS", "11100501", "Bancolombia Cta Cte 123456789-111"]
    : (formaPago === "CAJA" ? ["1105", "CAJA", "11050501", "Caja general principal"] : ["1305", "CLIENTES", auxCliente.codigo, auxCliente.nombre]);

  const cuentaPagoCompra = formaPago === "BANCO" ? ["1110", "BANCOS", "11100501", "Bancolombia Cta Cte 123456789-111"]
    : (formaPago === "CAJA" ? ["1105", "CAJA", "11050501", "Caja general principal"] : ["2205", "PROVEEDORES NACIONALES", auxProveedor.codigo, auxProveedor.nombre]);

  if (tipo === "VENTA") {
    asientos.push({ codigo: cuentaPagoVenta[0], cuenta: cuentaPagoVenta[1], parcial: 0, debe: neto, haber: 0 });
    asientos.push({ codigo: cuentaPagoVenta[2], cuenta: cuentaPagoVenta[3], parcial: neto, debe: 0, haber: 0 });
    if (reteiva > 0 || totalIcaPaquete > 0 || autorretencion > 0 || autoEspecial > 0) {
      const sum1355 = reteiva + totalIcaPaquete + autorretencion + autoEspecial;
      asientos.push({ codigo: "1355", cuenta: "ANTICIPO DE IMPUESTOS Y CONTRIBUCIONES", parcial: 0, debe: sum1355, haber: 0 });
      if (reteiva > 0) asientos.push({ codigo: "135517", cuenta: `Impuesto a las ventas retenido ReteIVA — ${tercero}`, parcial: reteiva, debe: 0, haber: 0 });
      if (reteica > 0) asientos.push({ codigo: "135518", cuenta: `Impuesto de industria y comercio retenido (9.6‰) — ${tercero}`, parcial: reteica, debe: 0, haber: 0 });
      if (avisos > 0) asientos.push({ codigo: "135520", cuenta: "Avisos y tableros retenido (15%)", parcial: avisos, debe: 0, haber: 0 });
      if (bomberil > 0) asientos.push({ codigo: "135525", cuenta: "Sobretasa Bomberil retenida (10%)", parcial: bomberil, debe: 0, haber: 0 });
      if (autorretencion > 0) asientos.push({ codigo: "135575", cuenta: `Autorretención en Renta (${(tarifaAuto * 100).toFixed(1)}%) — ${numFactura}`, parcial: autorretencion, debe: 0, haber: 0 });
      if (autoEspecial > 0) asientos.push({ codigo: "135595", cuenta: "Autorretención Especial (0.55%)", parcial: autoEspecial, debe: 0, haber: 0 });
    }
    asientos.push({ codigo: "4135", cuenta: "COMERCIO AL POR MAYOR Y AL POR MENOR", parcial: 0, debe: 0, haber: base });
    asientos.push({ codigo: "413536", cuenta: `Venta de ${prodName} (${prodRef}) — ${numFactura}`, parcial: base, debe: 0, haber: 0 });
    if (iva > 0) {
      asientos.push({ codigo: "2408", cuenta: "IMPUESTO SOBRE LAS VENTAS POR PAGAR", parcial: 0, debe: 0, haber: iva });
      asientos.push({ codigo: "240805", cuenta: `IVA generado en ventas (19%) — ${numFactura}`, parcial: iva, debe: 0, haber: 0 });
    }
    if (autorretencion > 0 || autoEspecial > 0) {
      asientos.push({ codigo: "2465", cuenta: "RETENCIÓN EN LA FUENTE POR PAGAR", parcial: 0, debe: 0, haber: autorretencion + autoEspecial });
      if (autorretencion > 0) asientos.push({ codigo: "246575", cuenta: `Autorretenciones en Renta — ${numFactura}`, parcial: autorretencion, debe: 0, haber: 0 });
      if (autoEspecial > 0) asientos.push({ codigo: "246590", cuenta: "Autorretención Especial Decreto 2201", parcial: autoEspecial, debe: 0, haber: 0 });
    }
    if (costoTotal > 0) {
      asientos.push({ codigo: "6135", cuenta: "COSTO DE VENTAS - COMERCIO AL POR MAYOR Y MENOR", parcial: 0, debe: costoTotal, haber: 0 });
      asientos.push({ codigo: "613536", cuenta: `Costo venta Kardex ${prodName} (${prodRef})`, parcial: costoTotal, debe: 0, haber: 0 });
      asientos.push({ codigo: "1435", cuenta: "MERCANCÍAS NO FABRICADAS POR LA EMPRESA", parcial: 0, debe: 0, haber: costoTotal });
      asientos.push({ codigo: auxKardexProd.codigo, cuenta: `Salida Kardex ${prodRef} — ${prodName} (${numFactura})`, parcial: costoTotal, debe: 0, haber: 0 });
    }
  } else if (tipo === "COMPRA") {
    asientos.push({ codigo: "1435", cuenta: "MERCANCÍAS NO FABRICADAS POR LA EMPRESA", parcial: 0, debe: base, haber: 0 });
    asientos.push({ codigo: auxKardexProd.codigo, cuenta: `Entrada Kardex ${prodRef} — ${prodName} (${numFactura})`, parcial: base, debe: 0, haber: 0 });
    if (iva > 0) {
      asientos.push({ codigo: "2408", cuenta: "IMPUESTO SOBRE LAS VENTAS POR PAGAR", parcial: 0, debe: iva, haber: 0 });
      asientos.push({ codigo: "240810", cuenta: `IVA descontable por compras (19%) — ${numFactura}`, parcial: iva, debe: 0, haber: 0 });
    }
    if (retefuente > 0) {
      asientos.push({ codigo: "2465", cuenta: "RETENCIÓN EN LA FUENTE", parcial: 0, debe: 0, haber: retefuente });
      asientos.push({ codigo: "246540", cuenta: `Retefuente Compras (${(tarifaRete * 100).toFixed(1)}%) — ${tercero}`, parcial: retefuente, debe: 0, haber: 0 });
    }
    if (totalIcaPaquete > 0) {
      asientos.push({ codigo: "2468", cuenta: "IMPUESTO DE INDUSTRIA Y COMERCIO RETENIDO", parcial: 0, debe: 0, haber: totalIcaPaquete });
      asientos.push({ codigo: "246801", cuenta: `ReteICA Bucaramanga (9.6‰) — ${tercero}`, parcial: reteica, debe: 0, haber: 0 });
      asientos.push({ codigo: "246802", cuenta: "Avisos y Tableros (15%)", parcial: avisos, debe: 0, haber: 0 });
      asientos.push({ codigo: "246803", cuenta: "Sobretasa Bomberil (10%)", parcial: bomberil, debe: 0, haber: 0 });
    }
    asientos.push({ codigo: cuentaPagoCompra[0], cuenta: cuentaPagoCompra[1], parcial: 0, debe: 0, haber: neto });
    asientos.push({ codigo: cuentaPagoCompra[2], cuenta: cuentaPagoCompra[3], parcial: neto, debe: 0, haber: 0 });
  } else if (tipo === "DEV_VENTA") {
    asientos.push({ codigo: "4175", cuenta: "DEVOLUCIONES EN VENTAS (DB)", parcial: 0, debe: base, haber: 0 });
    asientos.push({ codigo: "417505", cuenta: `Devolución venta ${prodName} (${prodRef})`, parcial: base, debe: 0, haber: 0 });
    if (iva > 0) {
      asientos.push({ codigo: "2408", cuenta: "IMPUESTO SOBRE LAS VENTAS POR PAGAR", parcial: 0, debe: iva, haber: 0 });
      asientos.push({ codigo: "240820", cuenta: "IVA por devoluciones en ventas", parcial: iva, debe: 0, haber: 0 });
    }
    if (autorretencion > 0) {
      asientos.push({ codigo: "2465", cuenta: "RETENCIÓN EN LA FUENTE", parcial: 0, debe: autorretencion, haber: 0 });
      asientos.push({ codigo: "246575", cuenta: "Reversión Autorretención Renta", parcial: autorretencion, debe: 0, haber: 0 });
      asientos.push({ codigo: "1355", cuenta: "ANTICIPO DE IMPUESTOS", parcial: 0, debe: 0, haber: autorretencion });
      asientos.push({ codigo: "135575", cuenta: "Reversión Anticipo Autorretención", parcial: autorretencion, debe: 0, haber: 0 });
    }
    asientos.push({ codigo: cuentaPagoVenta[0], cuenta: cuentaPagoVenta[1], parcial: 0, debe: 0, haber: neto });
    asientos.push({ codigo: cuentaPagoVenta[2], cuenta: cuentaPagoVenta[3], parcial: neto, debe: 0, haber: 0 });
    if (costoTotal > 0) {
      asientos.push({ codigo: "1435", cuenta: "MERCANCÍAS NO FABRICADAS POR LA EMPRESA", parcial: 0, debe: costoTotal, haber: 0 });
      asientos.push({ codigo: auxKardexProd.codigo, cuenta: `Reingreso Kardex ${prodRef} — ${prodName}`, parcial: costoTotal, debe: 0, haber: 0 });
      asientos.push({ codigo: "6135", cuenta: "COSTO DE VENTAS", parcial: 0, debe: 0, haber: costoTotal });
      asientos.push({ codigo: "613536", cuenta: "Reversión costo de venta", parcial: costoTotal, debe: 0, haber: 0 });
    }
  } else if (tipo === "DEV_COMPRA") {
    asientos.push({ codigo: cuentaPagoCompra[0], cuenta: cuentaPagoCompra[1], parcial: 0, debe: neto, haber: 0 });
    asientos.push({ codigo: cuentaPagoCompra[2], cuenta: cuentaPagoCompra[3], parcial: neto, debe: 0, haber: 0 });
    asientos.push({ codigo: "1435", cuenta: "MERCANCÍAS NO FABRICADAS POR LA EMPRESA", parcial: 0, debe: 0, haber: base });
    asientos.push({ codigo: auxKardexProd.codigo, cuenta: `Devolución Kardex ${prodRef} — ${prodName}`, parcial: base, debe: 0, haber: 0 });
    if (iva > 0) {
      asientos.push({ codigo: "2408", cuenta: "IMPUESTO SOBRE LAS VENTAS POR PAGAR", parcial: 0, debe: 0, haber: iva });
      asientos.push({ codigo: "240825", cuenta: "IVA en devoluciones en compras", parcial: iva, debe: 0, haber: 0 });
    }
  } else if (tipo === "EGRESO") {
    asientos.push({ codigo: "2205", cuenta: "PROVEEDORES NACIONALES / CUENTAS POR PAGAR", parcial: 0, debe: base, haber: 0 });
    asientos.push({ codigo: auxProveedor.codigo, cuenta: `Abono o pago a ${auxProveedor.nombre}`, parcial: base, debe: 0, haber: 0 });
    asientos.push({ codigo: "1110", cuenta: "BANCOS", parcial: 0, debe: 0, haber: base });
    asientos.push({ codigo: "11100501", cuenta: "Bancolombia Cta Cte 123456789-111", parcial: base, debe: 0, haber: 0 });
  } else {
    asientos.push({ codigo: "1110", cuenta: "BANCOS", parcial: 0, debe: base, haber: 0 });
    asientos.push({ codigo: "11100501", cuenta: "Bancolombia Cta Cte 123456789-111", parcial: base, debe: 0, haber: 0 });
    asientos.push({ codigo: "1305", cuenta: "CLIENTES NACIONALES", parcial: 0, debe: 0, haber: base });
    asientos.push({ codigo: auxCliente.codigo, cuenta: `Recaudo de ${auxCliente.nombre}`, parcial: base, debe: 0, haber: 0 });
  }

  let sumDebe = 0, sumHaber = 0;
  asientos.forEach(a => { sumDebe += a.debe; sumHaber += a.haber; });

  document.getElementById("liveJournalBody").innerHTML = asientos.map(a => {
    const isSub = String(a.codigo).length >= 6 && a.debe === 0 && a.haber === 0;
    return `
      <tr>
        <td class="code-col">${a.codigo}</td>
        <td style="${isSub ? "padding-left:18px; color:var(--text-secondary); font-style:italic;" : "font-weight:700;"}">${a.cuenta}</td>
        <td class="num-col">${a.parcial ? fmtCOP(a.parcial) : ""}</td>
        <td class="num-col">${a.debe ? fmtCOP(a.debe) : ""}</td>
        <td class="num-col">${a.haber ? fmtCOP(a.haber) : ""}</td>
      </tr>
    `;
  }).join("") + `
    <tr class="row-total">
      <td colspan="2">SUMAS IGUALES</td>
      <td></td>
      <td class="num-col">${fmtCOP(sumDebe)}</td>
      <td class="num-col">${fmtCOP(sumHaber)}</td>
    </tr>
  `;

  // Calcular previsualización del movimiento de Kardex encadenado
  const isEntradaKardex = (tipo === "COMPRA" || tipo === "DEV_VENTA");
  const vlrMovKardex = (tipo === "COMPRA" || tipo === "DEV_COMPRA") ? base : costoTotal;
  const newKardexCant = isEntradaKardex ? (existCant + cant) : (existCant - cant);
  const newKardexVal = isEntradaKardex ? (existVal + vlrMovKardex) : (existVal - vlrMovKardex);
  const newKardexProm = newKardexCant > 0 ? Math.round(newKardexVal / newKardexCant) : cProm;

  const traceBox = document.getElementById("liveTraceabilityChainBox");
  if (traceBox) {
    const activeThirdAux = (isVentaSide || tipo === "INGRESO") ? auxCliente : auxProveedor;
    traceBox.innerHTML = `
      <div style="background:var(--bg-card); border:1.5px solid var(--brand-primary); border-left:5px solid var(--brand-emerald); border-radius:var(--radius-md); padding:14px 16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
          <span style="font-size:0.82rem; font-weight:800; color:var(--brand-primary);">
            🔗 CADENA DE TRAZABILIDAD AUTOMÁTICA (NADA SUELTO — TODO ENCADENADO DE ORIGEN A DESTINO)
          </span>
          <span class="status-pill status-paid">Sincronización Automática Activa ✓</span>
        </div>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:10px; font-size:0.77rem;">
          <div style="background:var(--bg-subtle); padding:10px; border-radius:6px; border:1px solid var(--border-light);">
            <strong style="color:var(--brand-primary);">1️⃣ Documento & Hoja Origen:</strong><br/>
            <span><strong>${numFactura}</strong></span><br/>
            <span style="color:var(--text-secondary);">Mes: <strong>${mes}</strong> • Hoja N° <strong>${hoja}</strong></span>
          </div>
          <div style="background:var(--bg-subtle); padding:10px; border-radius:6px; border:1px solid var(--border-light);">
            <strong style="color:var(--brand-primary);">2️⃣ Auxiliar Tercero (8 Dígitos):</strong><br/>
            <span class="code-col" style="font-weight:800;">${activeThirdAux.codigo}</span>
            <span class="status-pill ${activeThirdAux.esNuevo ? "status-pending" : "status-paid"}" style="font-size:0.66rem; padding:1px 6px;">
              ${activeThirdAux.esNuevo ? "✨ Se crea automático en PUC" : "✓ Ya existe en PUC"}
            </span><br/>
            <span style="color:var(--text-secondary);">${activeThirdAux.nombre}</span>
          </div>
          ${(tipo !== "EGRESO" && tipo !== "INGRESO") ? `
          <div style="background:var(--bg-subtle); padding:10px; border-radius:6px; border:1px solid var(--border-light);">
            <strong style="color:var(--brand-primary);">3️⃣ Tarjeta Kardex (${prodRef}):</strong><br/>
            <span>Auxiliar: <strong class="code-col">${auxKardexProd.codigo}</strong> ${isNewProd ? `<span class="status-pill status-pending" style="font-size:0.65rem;">✨ Nueva Tarjeta Kardex</span>` : ""}</span><br/>
            <span style="color:var(--text-secondary);">
              Saldo Ant: <strong>${existCant} und</strong> ➔ ${isEntradaKardex ? `Entrada +${cant}` : `Salida -${cant}`} ➔ <strong>Nuevo: ${newKardexCant} und (${fmtCOP(newKardexVal)})</strong> • Prom: <strong>${fmtCOP(newKardexProm)}</strong>
            </span>
          </div>` : ""}
          <div style="background:var(--bg-subtle); padding:10px; border-radius:6px; border:1px solid var(--border-light);">
            <strong style="color:var(--brand-primary);">4️⃣ Libros Auxiliares & NIIF:</strong><br/>
            <span style="color:var(--text-secondary);">
              Actualiza en vivo <strong>${asientos.filter(a => String(a.codigo).length >= 6).length} cuentas auxiliares</strong>, Libro Diario, Balance de Prueba y Estado de Resultados de <strong>${mes}</strong>.
            </span>
          </div>
        </div>
      </div>
    `;
  }

  window.__LIVE_TX_STATE = {
    rule, tipo, cant, vUnit, cProm, base, iva, retefuente, autorretencion: autorretencion + autoEspecial,
    autoEspecial, reteiva, reteica: totalIcaPaquete, neto, sumDebe, sumHaber, asientos,
    isNewProd, prodRef, prodName, auxCliente, auxProveedor, auxKardexProd, nuevosAuxiliaresPuc,
    existCant, existVal, newKardexCant, newKardexVal, newKardexProm
  };

  LIVE_TX_CACHE = {
    mes,
    hoja,
    fecha: document.getElementById("txFecha")?.value || "2026-04-15",
    tipo: tipo === "VENTA" ? "FACTURA ELECTRÓNICA DE VENTA" : (tipo === "COMPRA" ? "FACTURA DE COMPRA / SOPORTE" : tipo),
    op_code: tipo,
    num_doc: numFactura,
    tercero,
    nit_tercero: nitTercero,
    regimen_vendedor: isVentaSide ? `${DB?.empresa?.razon_social || "ELECTROVIVIENDA S.A.S"} — RRI` : (rule?.label || "RRI"),
    regimen_comprador: isVentaSide ? (rule?.label || "RRI") : `${DB?.empresa?.razon_social || "ELECTROVIVIENDA S.A.S"} — RRI`,
    forma_pago: formaPago,
    cheque: document.getElementById("txCheque")?.value || formaPago,
    enunciado: document.getElementById("txEnunciado")?.value || "",
    suma_letras: `${fmtCOP(neto)} PESOS M/CTE.`,
    subtotal: base,
    iva,
    retefuente,
    reteiva,
    reteica_total: totalIcaPaquete,
    autorretencion,
    auto_especial: autoEspecial,
    neto_pagar: neto,
    total_debe: sumDebe,
    total_haber: sumHaber,
    asientos,
    producto_id: prodRef,
    cantidad: cant,
    valor_unitario: vUnit
  };

  if (typeof renderDidacticLiveExerciseExplanation === "function") {
    renderDidacticLiveExerciseExplanation();
  }
}

async function saveAndSyncTransaction() {
  recalcLiveTransaction();
  const st = window.__LIVE_TX_STATE;
  if (!st) return;

  const mes = document.getElementById("txMes").value;
  const hoja = document.getElementById("txHoja").value.trim() || "61";
  const numFactura = document.getElementById("txNumFactura").value.trim() || `Doc N° ${hoja}`;
  const fecha = document.getElementById("txFecha").value;
  const tercero = document.getElementById("txTercero").value.trim();
  const nitTercero = document.getElementById("txNitTercero").value.trim();
  const cheque = document.getElementById("txCheque").value.trim();
  const enunciado = document.getElementById("txEnunciado").value.trim();
  const prodSelectVal = document.getElementById("txProductoId")?.value;

  const isVentaSide = (st.tipo === "VENTA" || st.tipo === "DEV_VENTA");
  const miReg = `${DB.empresa.razon_social} — RRI Aut. Renta`;

  // Calcular el siguiente número consecutivo de Comprobante Diario para mantener numeración oficial encadenada
  let maxCompNum = 0;
  for (const m of ALL_12_MONTHS) {
    for (const t of (DB?.meses?.[m]?.transacciones || [])) {
      const n = Number(t.num_comprobante_diario) || 0;
      if (n > maxCompNum) maxCompNum = n;
    }
  }
  const nextCompDiarioNum = maxCompNum + 1;
  const compDiarioLabel = `Comprobante Diario N° ${nextCompDiarioNum}`;

  const txObj = {
    hoja,
    mes,
    fecha,
    tipo: numFactura,
    comprobante_diario: compDiarioLabel,
    num_comprobante_diario: nextCompDiarioNum,
    enunciado,
    tercero,
    nit_tercero: nitTercero,
    cheque,
    concepto_soporte: `${enunciado} [Origen: ${numFactura} • Hoja ${hoja} • ${mes}]`,
    suma_letras: `${fmtCOP(st.neto)} PESOS M/CTE.`,
    elaborado_por: ACTIVE_STUDENT_PROFILE.nombre || DB.empresa.elaborado_por || "Gina Villamizar",
    auxiliar_tercero: (isVentaSide || st.tipo === "INGRESO") ? st.auxCliente?.codigo : st.auxProveedor?.codigo,
    auxiliar_kardex: st.auxKardexProd?.codigo || "",
    producto_kardex_ref: st.prodRef || "",
    total_debe: st.sumDebe,
    total_haber: st.sumHaber,
    liquidacion: {
      base: st.base,
      iva: st.iva,
      retefuente: st.retefuente,
      autorretencion: st.autorretencion,
      reteiva: st.reteiva,
      reteica: st.reteica,
      neto: st.neto,
      regimen_comprador: isVentaSide ? st.rule.label : miReg,
      regimen_vendedor: isVentaSide ? miReg : st.rule.label
    },
    asientos: st.asientos,
    rows: []
  };

  let kardexMov = null;
  let nuevoProductoKardex = null;
  let targetProdId = st.isNewProd ? st.prodRef : prodSelectVal;

  if (st.tipo !== "EGRESO" && st.tipo !== "INGRESO" && targetProdId) {
    if (st.isNewProd) {
      nuevoProductoKardex = {
        id: st.prodRef,
        referencia: st.prodRef,
        articulo: st.prodName,
        cuenta_puc: st.auxKardexProd?.codigo || "14353601",
        auxiliar_puc: st.auxKardexProd?.codigo || "14353601",
        proveedor: isVentaSide ? (DB.empresa.razon_social || "Proveedor General") : tercero,
        metodo: "PROMEDIO PONDERADO",
        unidad: "UND",
        precio_venta_sugerido: Math.round(st.vUnit * 1.35),
        movimientos: []
      };
    }

    const isEntrada = (st.tipo === "COMPRA" || st.tipo === "DEV_VENTA");
    const vlrMov = (st.tipo === "COMPRA" || st.tipo === "DEV_COMPRA") ? st.base : Math.round(st.cant * st.cProm);

    kardexMov = {
      producto_id: targetProdId,
      registro: {
        fecha,
        mes,
        hoja,
        comprobante_diario: compDiarioLabel,
        auxiliar_puc: st.auxKardexProd?.codigo || "143536",
        tipo: st.tipo,
        descripcion: `${numFactura} — ${tercero} (${compDiarioLabel} • Hoja ${hoja})`,
        doc: numFactura,
        vlr_unitario: (st.tipo === "COMPRA" || st.tipo === "DEV_COMPRA") ? st.vUnit : st.cProm,
        ent_cant: isEntrada ? st.cant : 0,
        ent_valor: isEntrada ? vlrMov : 0,
        sal_cant: isEntrada ? 0 : st.cant,
        sal_valor: isEntrada ? 0 : vlrMov,
        saldo_cant: st.newKardexCant,
        saldo_valor: st.newKardexVal,
        promedio: st.newKardexProm
      }
    };
  }

  let facturaDetalle = null;
  if (st.tipo === "VENTA" || st.tipo === "COMPRA" || st.tipo === "DEV_VENTA" || st.tipo === "DEV_COMPRA") {
    const cat = st.tipo === "VENTA" ? "VENTA" : (st.tipo === "COMPRA" ? "COMPRA" : "DEVOLUCION");
    facturaDetalle = {
      id: `FAC-${Date.now()}`,
      numero: numFactura,
      comprobante_diario: compDiarioLabel,
      num_comprobante_diario: nextCompDiarioNum,
      categoria: cat,
      tipo_operacion: st.tipo === "VENTA" ? "FACTURA DE VENTA" : (st.tipo === "COMPRA" ? "FACTURA DE COMPRA" : "NOTA CONTABLE / DEVOLUCIÓN"),
      mes,
      hoja,
      fecha,
      tercero,
      nit_tercero: nitTercero,
      auxiliar_tercero: isVentaSide ? st.auxCliente?.codigo : st.auxProveedor?.codigo,
      auxiliar_kardex: st.auxKardexProd?.codigo || "",
      regimen_comprador: isVentaSide ? st.rule.label : miReg,
      regimen_vendedor: isVentaSide ? miReg : st.rule.label,
      forma_pago: cheque,
      enunciado,
      items: [{
        referencia: st.prodRef,
        descripcion: st.prodName,
        cantidad: st.cant,
        valor_unitario: st.vUnit,
        subtotal: st.base
      }],
      subtotal: st.base,
      iva: st.iva,
      retefuente: st.retefuente,
      autorretencion: st.autorretencion,
      reteiva: st.reteiva,
      reteica: st.reteica,
      total_neto: st.neto,
      suma_letras: `${fmtCOP(st.neto)} PESOS M/CTE.`,
      asientos: st.asientos,
      total_debe: st.sumDebe,
      total_haber: st.sumHaber
    };
  }

  try {
    const res = await fetch("/api/transaccion", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mes,
        transaccion: txObj,
        kardex_movimiento: kardexMov,
        nuevo_producto_kardex: nuevoProductoKardex,
        nuevos_auxiliares_puc: st.nuevosAuxiliaresPuc || [],
        factura_detalle: facturaDetalle
      })
    });
    const data = await res.json();
    if (data.ok && data.db) {
      DB = data.db;
      saveLocalCloudOverlay();
      ACTIVE_PERIOD = mes;
      populateProductSelect();
      refreshAllViews();
      // Avanzar automáticamente el número de hoja sugerido para la siguiente operación
      const nextHojaNum = (parseInt(hoja, 10) || 60) + 1;
      const hojaEl = document.getElementById("txHoja");
      if (hojaEl) hojaEl.value = String(nextHojaNum);
      showToast(`✅ Encadenado completo: ${numFactura} ➔ ${compDiarioLabel} ➔ Kardex (${st.prodRef}) ➔ Auxiliares PUC`);
      if (facturaDetalle) {
        ACTIVE_INVOICE_ID = facturaDetalle.id;
        switchSection("facturas");
      } else {
        ACTIVE_VOUCHER_SHEET = `${mes}|${hoja}`;
        switchSection("comprobantes");
      }
      return;
    }
  } catch (e) {
    // Fallback local
    if (st.nuevosAuxiliaresPuc && st.nuevosAuxiliaresPuc.length) {
      st.nuevosAuxiliaresPuc.forEach(aux => {
        if (!DB.puc.some(c => String(c.codigo) === String(aux.codigo))) {
          DB.puc.push({ codigo: aux.codigo, nombre: aux.nombre, nivel: "Auxiliar (8 dígitos - Automático)" });
        }
      });
    }
    if (nuevoProductoKardex) {
      DB.kardex.push(nuevoProductoKardex);
    }
    if (kardexMov) {
      const pTarget = (DB.kardex || []).find(p => p.id === kardexMov.producto_id || p.referencia === kardexMov.producto_id);
      if (pTarget) pTarget.movimientos.push(kardexMov.registro);
    }
    DB.meses[mes].transacciones.push(txObj);
    if (facturaDetalle) DB.facturas.unshift(facturaDetalle);
    saveLocalCloudOverlay();
    populateProductSelect();
    refreshAllViews();
    showToast("Guardado y encadenado en vivo (Factura + Kardex + Auxiliares + Estados Financieros)");
  }
}

// ============================================================================
// 5. SECCIÓN: LIBROS AUXILIARES EN VIVO (SUBCUENTAS 6 DÍGITOS, TERCEROS 8 DÍGITOS Y BANCOS)
// ============================================================================
function setAuxMode(mode) {
  ACTIVE_AUX_MODE = mode;
  document.querySelectorAll("#auxModeTabs .filter-chip").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.auxmode === mode);
  });
  renderAuxiliaresSection();
}

function buildLiveAuxiliaresFromTransactions(mes) {
  const txs = DB?.meses?.[mes]?.transacciones || [];
  const subcuentasMap = new Map();
  const tercerosMap = new Map();
  const bancoMovs = [];

  txs.forEach(tx => {
    const asientos = tx.asientos || [];
    for (let i = 0; i < asientos.length; i++) {
      const a = asientos[i];
      const code = String(a.codigo || "").trim();
      if (!code) continue;

      // Si es cuenta de 4 dígitos con Debe/Haber y debajo vienen subcuentas con parcial
      if (code.length === 4 && (a.debe > 0 || a.haber > 0)) {
        const isDebitSide = a.debe > 0;
        let hasChildren = false;
        let j = i + 1;
        while (j < asientos.length && String(asientos[j].codigo || "").startsWith(code) && String(asientos[j].codigo || "").length >= 6) {
          hasChildren = true;
          const child = asientos[j];
          const cCode = String(child.codigo).trim();
          const val = Number(child.parcial) || (isDebitSide ? child.debe : child.haber) || 0;
          const entrada = isDebitSide ? val : 0;
          const salida = isDebitSide ? 0 : val;

          const subCode6 = cCode.slice(0, 6);
          if (!subcuentasMap.has(subCode6)) {
            subcuentasMap.set(subCode6, { codigo: subCode6, nombre: child.cuenta || a.cuenta, movs: [] });
          }
          subcuentasMap.get(subCode6).movs.push({
            hoja: tx.hoja,
            fecha: tx.fecha,
            descripcion: `${tx.tipo} — ${tx.tercero || tx.enunciado || ""}`.slice(0, 68),
            entrada,
            salida
          });

          if (cCode.length >= 8 || tx.tercero) {
            const auxKey = cCode.length >= 8 ? cCode : `${subCode6}01`;
            const auxName = cCode.length >= 8 ? child.cuenta : `${child.cuenta} — ${tx.tercero}`;
            if (!tercerosMap.has(auxKey)) {
              tercerosMap.set(auxKey, { codigo: auxKey, nombre: auxName, movs: [] });
            }
            tercerosMap.get(auxKey).movs.push({
              hoja: tx.hoja,
              fecha: tx.fecha,
              descripcion: `${tx.tipo} (${tx.tercero || "Tercero"})`.slice(0, 65),
              entrada,
              salida
            });
          }

          if (cCode.startsWith("1110")) {
            bancoMovs.push({
              hoja: tx.hoja,
              fecha: tx.fecha,
              cheque: tx.cheque || tx.tipo,
              beneficiario: tx.tercero || child.cuenta,
              concepto: tx.enunciado || tx.concepto_soporte || child.cuenta,
              entrada,
              salida
            });
          }
          j++;
        }

        if (!hasChildren) {
          const sub6 = `${code}05`;
          if (!subcuentasMap.has(sub6)) {
            subcuentasMap.set(sub6, { codigo: sub6, nombre: a.cuenta, movs: [] });
          }
          subcuentasMap.get(sub6).movs.push({
            hoja: tx.hoja,
            fecha: tx.fecha,
            descripcion: `${tx.tipo} — ${tx.tercero || ""}`,
            entrada: a.debe || 0,
            salida: a.haber || 0
          });
        }
      }
    }
  });

  return {
    subcuentas: Array.from(subcuentasMap.values()).sort((a, b) => a.codigo.localeCompare(b.codigo)),
    terceros: Array.from(tercerosMap.values()).sort((a, b) => a.codigo.localeCompare(b.codigo)),
    bancoMovs
  };
}

function renderAuxiliaresSection() {
  const container = document.getElementById("auxiliaresContentContainer");
  if (!container || !DB) return;

  const live = buildLiveAuxiliaresFromTransactions(ACTIVE_PERIOD);
  const q = (document.getElementById("searchAuxInput")?.value || "").toLowerCase().trim();

  let saldoBanco = 0;
  live.bancoMovs.forEach(m => { saldoBanco += (m.entrada - m.salida); });

  document.getElementById("auxiliaresKpiRow").innerHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Subcuentas Activas (6 Dígitos)</div>
      <div class="kpi-value">${live.subcuentas.length} Subcuentas</div>
      <div class="kpi-sub">Actualizadas en vivo en ${ACTIVE_PERIOD}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Auxiliares por Tercero (8 Dígitos)</div>
      <div class="kpi-value">${live.terceros.length} Auxiliares</div>
      <div class="kpi-sub">Clientes, Proveedores, Socios y Bancos</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Movimientos Bancarios (11100501)</div>
      <div class="kpi-value">${live.bancoMovs.length} Giros/Consig.</div>
      <div class="kpi-sub">Bancolombia Cta Cte 123456789-111</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Flujo Neto Bancos del Mes</div>
      <div class="kpi-value">${fmtCOP(saldoBanco)}</div>
      <div class="kpi-sub">Sincronizado con L.BANCO AUXILIAR</div>
    </div>
  `;

  if (ACTIVE_AUX_MODE === "EXCEL_AUX" || ACTIVE_AUX_MODE === "EXCEL_BANCO") {
    const esp = DB?.meses?.[ACTIVE_PERIOD]?.hojas_especiales || {};
    const targetKey = ACTIVE_AUX_MODE === "EXCEL_AUX"
      ? Object.keys(esp).find(k => k.includes("AUXILIAR") && !k.includes("BANCO"))
      : Object.keys(esp).find(k => k.includes("BANCO"));
    const rows = targetKey ? sheetRows(esp[targetKey]) : [];
    container.innerHTML = `
      <div class="card">
        <div class="card-header">
          <div class="card-title">📊 Hoja Oficial de Excel: ${targetKey || "LIBROS AUXILIARES"} (${ACTIVE_PERIOD}.xlsx)</div>
          <span class="status-pill status-paid">Formato Original del Libro Excel</span>
        </div>
        <div class="card-body">
          ${rows.length ? renderExcelGridHtml(rows) : `<p>Usa la pestaña "Libros Auxiliares en Vivo" para ver todas las subcuentas de ${ACTIVE_PERIOD}.</p>`}
        </div>
      </div>
    `;
    return;
  }

  if (ACTIVE_AUX_MODE === "VIVO_BANCO") {
    let running = 0;
    const rowsHtml = live.bancoMovs
      .filter(m => !q || m.beneficiario.toLowerCase().includes(q) || m.concepto.toLowerCase().includes(q) || String(m.cheque).toLowerCase().includes(q))
      .map((m, idx) => {
        constnaturaleza = String(m.codigo || "1110").startsWith("2") ? -1 : 1;
        running += (m.entrada - m.salida);
        return `
          <tr>
            <td class="code-col">
              <button class="btn btn-outline btn-sm" style="padding:2px 6px; font-size:0.7rem;" onclick="ACTIVE_VOUCHER_SHEET='${ACTIVE_PERIOD}|${m.hoja}'; switchSection('comprobantes');" title="Ir al Comprobante Origen Hoja ${m.hoja}">
                🔗 ${idx + 1} (Hoja ${m.hoja})
              </button>
            </td>
            <td>${m.fecha}</td>
            <td class="code-col">${m.cheque}</td>
            <td><strong>${m.beneficiario}</strong></td>
            <td>${m.concepto}</td>
            <td class="num-col" style="color:var(--brand-emerald);">${m.entrada ? fmtCOP(m.entrada) : "$0"}</td>
            <td class="num-col" style="color:var(--brand-danger);">${m.salida ? fmtCOP(m.salida) : "$0"}</td>
            <td class="num-col"><strong>${fmtCOP(running)}</strong></td>
          </tr>
        `;
      }).join("");

    container.innerHTML = `
      <div class="card">
        <div class="card-header">
          <div class="card-title">🏦 Libro Auxiliar de Bancos en Vivo — Cuenta 11100501 Bancolombia Cta Cte N° 123456789-111 (${ACTIVE_PERIOD})</div>
          <span class="status-pill status-paid">Actualización Automática en Tiempo Real</span>
        </div>
        <div class="card-body">
          <div class="table-wrap">
            <table class="acct-table">
              <thead>
                <tr>
                  <th>N° / Hoja</th>
                  <th>Fecha</th>
                  <th>Cheque / Doc</th>
                  <th>Tercero / Beneficiario</th>
                  <th>Descripción / Concepto</th>
                  <th class="num-col">Entrada (Debe)</th>
                  <th class="num-col">Salida (Haber)</th>
                  <th class="num-col">Saldo Acumulado</th>
                </tr>
              </thead>
              <tbody>${rowsHtml || `<tr><td colspan="8">Sin movimientos bancarios en este filtro.</td></tr>`}</tbody>
            </table>
          </div>
        </div>
      </div>
    `;
    return;
  }

  // Modo VIVO_SUBCUENTAS: Dos columnas paralelas como en el Excel (Izquierda: SUBCUENTA 6 dígitos, Derecha: AUXILIAR 8 dígitos)
  const renderLedgerCards = (items, badgeTitle) => items
    .filter(item => !q || item.codigo.toLowerCase().includes(q) || item.nombre.toLowerCase().includes(q) || item.movs.some(m => m.descripcion.toLowerCase().includes(q)))
    .map(item => {
      let saldo = 0;
      const firstDigit = item.codigo.charAt(0);
      const isCreditNature = (firstDigit === "2" || firstDigit === "3" || firstDigit === "4");
      let sumE = 0, sumS = 0;
      const movRows = item.movs.map((m, idx) => {
        sumE += m.entrada;
        sumS += m.salida;
        saldo += isCreditNature ? (m.salida - m.entrada) : (m.entrada - m.salida);
        return `
          <tr>
            <td class="code-col">
              <button class="btn btn-outline btn-sm" style="padding:2px 6px; font-size:0.68rem;" onclick="ACTIVE_VOUCHER_SHEET='${ACTIVE_PERIOD}|${m.hoja}'; switchSection('comprobantes');" title="Ver Comprobante Origen Hoja ${m.hoja}">
                🔗 ${idx + 1} (H.${m.hoja})
              </button>
            </td>
            <td>${m.fecha}</td>
            <td>${m.descripcion}</td>
            <td class="num-col">${m.entrada ? fmtCOP(m.entrada) : "$0"}</td>
            <td class="num-col">${m.salida ? fmtCOP(m.salida) : "$0"}</td>
            <td class="num-col"><strong>${fmtCOP(Math.abs(saldo))}</strong></td>
          </tr>
        `;
      }).join("");

      return `
        <div class="card" style="margin-bottom:14px;">
          <div class="card-header" style="background:var(--bg-subtle); padding:10px 14px;">
            <div class="card-title" style="font-size:0.84rem;">
              <span class="status-pill status-paid" style="margin-right:6px;">${badgeTitle}: ${item.codigo}</span>
              <span>${item.nombre}</span>
            </div>
            <span style="font-family:var(--font-mono); font-size:0.78rem; font-weight:800; color:var(--brand-primary);">
              Saldo Final: ${fmtCOP(Math.abs(saldo))}
            </span>
          </div>
          <div class="card-body" style="padding:10px 14px;">
            <div class="table-wrap">
              <table class="acct-table">
                <thead>
                  <tr>
                    <th>N°</th>
                    <th>Fecha</th>
                    <th>Descripción</th>
                    <th class="num-col">Entrada (Debe)</th>
                    <th class="num-col">Salida (Haber)</th>
                    <th class="num-col">Saldo</th>
                  </tr>
                </thead>
                <tbody>
                  ${movRows}
                  <tr class="row-total">
                    <td colspan="3">TOTALES ${item.codigo}</td>
                    <td class="num-col">${fmtCOP(sumE)}</td>
                    <td class="num-col">${fmtCOP(sumS)}</td>
                    <td class="num-col">${fmtCOP(Math.abs(saldo))}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      `;
    }).join("");

  container.innerHTML = `
    <div class="grid-2">
      <div>
        <div style="font-size:0.8rem; font-weight:800; color:var(--brand-primary); margin-bottom:10px; padding:6px 10px; background:var(--brand-gold-soft); border-radius:6px;">
          📘 COLUMNA IZQUIERDA DEL EXCEL: LIBROS AUXILIARES POR SUBCUENTA (6 DÍGITOS)
        </div>
        ${renderLedgerCards(live.subcuentas, "SUBCUENTA")}
      </div>
      <div>
        <div style="font-size:0.8rem; font-weight:800; color:var(--brand-primary); margin-bottom:10px; padding:6px 10px; background:var(--brand-gold-soft); border-radius:6px;">
          📙 COLUMNA DERECHA DEL EXCEL: AUXILIARES ESPECÍFICOS POR TERCERO (8 DÍGITOS)
        </div>
        ${renderLedgerCards(live.terceros, "AUXILIAR")}
      </div>
    </div>
  `;
}

// ============================================================================
// 6. SECCIÓN: KARDEX PROMEDIO PONDERADO
// ============================================================================
function renderKardexSection() {
  const kardex = DB.kardex || [];
  if (!kardex.length) {
    document.getElementById("kardexSummaryCards").innerHTML = "";
    document.getElementById("kardexProductTabs").innerHTML = "";
    document.getElementById("kardexDetailBody").innerHTML = `
      <div style="text-align:center; padding:32px;">
        <h3 style="color:var(--brand-primary); margin-bottom:8px;">📦 Kardex en $0 (Sin Productos Registrados Aún)</h3>
        <p style="font-size:0.84rem; color:var(--text-secondary); margin-bottom:14px;">
          Al emitir tu primera <strong>Factura de Compra o Venta</strong> en <em>Emitir Factura / Registro</em>, el sistema creará y encadenará automáticamente la Tarjeta Kardex Promedio Ponderado y su auxiliar PUC de 8 dígitos.
        </p>
        <div style="display:flex; justify-content:center; gap:10px;">
          <button class="btn btn-gold btn-sm" onclick="switchSection('facturacion')">⚡ Ir a Emitir Factura (Auto-Kardex)</button>
          <button class="btn btn-primary btn-sm" onclick="openNewProductKardexModal()">+ Crear Producto Manualmente</button>
        </div>
      </div>
    `;
    return;
  }
  if (!kardex.some(p => p.id === ACTIVE_KARDEX_ID)) {
    ACTIVE_KARDEX_ID = kardex[0].id;
  }

  document.getElementById("kardexSummaryCards").innerHTML = kardex.map(p => {
    let cant = 0, val = 0, prom = 0;
    (p.movimientos || []).forEach(m => {
      cant += (Number(m.ent_cant) || 0) - (Number(m.sal_cant) || 0);
      val += (Number(m.ent_valor) || 0) - (Number(m.sal_valor) || 0);
      prom = Number(m.promedio) || prom;
    });
    if (cant > 0 && val > 0) prom = Math.round(val / cant);
    return `
      <div class="kpi-card" style="cursor:pointer; ${p.id === ACTIVE_KARDEX_ID ? "border:2px solid var(--brand-gold);" : ""}" onclick="ACTIVE_KARDEX_ID='${p.id}'; renderKardexSection();">
        <div class="kpi-label">Ref: ${p.referencia} • PUC ${p.cuenta_puc || p.auxiliar_puc || "143536"}</div>
        <div class="kpi-value">${cant} UND — ${fmtCOP(val)}</div>
        <div class="kpi-sub">${p.articulo} • Prom: ${fmtCOP(prom)}</div>
      </div>
    `;
  }).join("");

  document.getElementById("kardexProductTabs").innerHTML = kardex.map(p => `
    <button class="filter-chip ${p.id === ACTIVE_KARDEX_ID ? "active" : ""}" onclick="ACTIVE_KARDEX_ID='${p.id}'; renderKardexSection();">
      📦 ${p.referencia} — ${p.articulo}
    </button>
  `).join("");

  const prod = kardex.find(p => p.id === ACTIVE_KARDEX_ID) || kardex[0];
  let salCant = 0, salVal = 0;
  const rowsHtml = (prod.movimientos || []).map((m, idx) => {
    salCant += (Number(m.ent_cant) || 0) - (Number(m.sal_cant) || 0);
    salVal += (Number(m.ent_valor) || 0) - (Number(m.sal_valor) || 0);
    const prom = salCant > 0 ? (salVal / salCant) : (Number(m.promedio) || 0);
    const originBtn = m.hoja
      ? `<button class="btn btn-outline btn-sm" style="padding:2px 6px; font-size:0.68rem;" onclick="setGlobalPeriod('${m.mes || ACTIVE_PERIOD}'); ACTIVE_VOUCHER_SHEET='${m.mes || ACTIVE_PERIOD}|${m.hoja}'; switchSection('comprobantes');" title="Ir al Comprobante / Factura Origen">${m.doc || `Hoja ${m.hoja}`} 🔗</button>`
      : `<span class="code-col">${m.doc || "-"}</span>`;
    return `
      <tr>
        <td class="code-col">${idx + 1}</td>
        <td>${m.fecha}</td>
        <td><span class="status-pill status-paid">${m.mes || "2026"}</span></td>
        <td><strong>${m.descripcion}</strong></td>
        <td>${originBtn}</td>
        <td class="num-col">${fmtCOP(m.vlr_unitario)}</td>
        <td class="num-col" style="background:rgba(16,185,129,0.06);">${m.ent_cant || ""}</td>
        <td class="num-col" style="background:rgba(16,185,129,0.06);">${m.ent_valor ? fmtCOP(m.ent_valor) : ""}</td>
        <td class="num-col" style="background:rgba(220,38,38,0.06);">${m.sal_cant || ""}</td>
        <td class="num-col" style="background:rgba(220,38,38,0.06);">${m.sal_valor ? fmtCOP(m.sal_valor) : ""}</td>
        <td class="num-col" style="background:rgba(212,175,55,0.12); font-weight:800;">${salCant}</td>
        <td class="num-col" style="background:rgba(212,175,55,0.12); font-weight:800;">${fmtCOP(salVal)}</td>
        <td class="num-col"><strong>${fmtCOP(prom)}</strong></td>
      </tr>
    `;
  }).join("");

  document.getElementById("kardexDetailBody").innerHTML = `
    <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:12px; padding:10px 14px; background:var(--bg-subtle); border-radius:6px; font-size:0.8rem;">
      <div><strong>Artículo:</strong> ${prod.articulo}</div>
      <div><strong>Referencia:</strong> <span class="code-col">${prod.referencia}</span></div>
      <div><strong>Auxiliar PUC Encadenado:</strong> <span class="code-col">${prod.cuenta_puc || prod.auxiliar_puc || "14353601"}</span></div>
      <div><strong>Proveedor Principal:</strong> ${prod.proveedor}</div>
      <div><strong>Método:</strong> ${prod.metodo}</div>
    </div>
    <div class="table-wrap">
      <table class="acct-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Fecha</th>
            <th>Mes</th>
            <th>Detalle / Concepto y Origen</th>
            <th>Factura / Doc Origen</th>
            <th class="num-col">Costo Unit.</th>
            <th class="num-col">Ent. Cant</th>
            <th class="num-col">Ent. Valor</th>
            <th class="num-col">Sal. Cant</th>
            <th class="num-col">Sal. Valor</th>
            <th class="num-col">Saldo Cant</th>
            <th class="num-col">Saldo Valor</th>
            <th class="num-col">Promedio Ponderado</th>
          </tr>
        </thead>
        <tbody>${rowsHtml}</tbody>
      </table>
    </div>
  `;
}

async function openNewProductKardexModal() {
  const ref = prompt("Referencia del nuevo producto (Ej: NV02):", "REF-05");
  if (!ref) return;
  const art = prompt("Nombre del Electrodoméstico / Producto:", "Aire Acondicionado Inverter 18.000 BTU");
  if (!art) return;
  const prov = prompt("Proveedor Principal:", "Distribuidora Nacional S.A.S") || "Proveedor General";
  const costoIni = Number(prompt("Costo Unitario Inicial ($):", "1800000") || 0);
  const cantIni = Number(prompt("Cantidad Inicial (Unidades):", "5") || 0);

  const nuevo = {
    id: ref.trim(),
    referencia: ref.trim(),
    articulo: art.trim(),
    cuenta_puc: "14350505",
    proveedor: prov.trim(),
    metodo: "Promedio Ponderado",
    unidad: "UND",
    minimo: 2,
    maximo: 30,
    precio_venta_sugerido: Math.round(costoIni * 1.4),
    movimientos: [
      {
        fecha: new Date().toISOString().slice(0, 10),
        mes: ACTIVE_PERIOD,
        tipo: "INV_INICIAL",
        descripcion: "Registro Inicial de Producto en Kardex",
        doc: "INI",
        vlr_unitario: costoIni,
        ent_cant: cantIni,
        ent_valor: Math.round(costoIni * cantIni),
        sal_cant: 0,
        sal_valor: 0,
        promedio: costoIni
      }
    ]
  };

  try {
    const res = await fetch("/api/kardex/producto", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ producto: nuevo })
    });
    const data = await res.json();
    if (data.ok && data.db) DB = data.db;
  } catch (e) {
    DB.kardex.push(nuevo);
    saveLocalCloudOverlay();
  }
  ACTIVE_KARDEX_ID = nuevo.id;
  refreshAllViews();
  showToast(`Producto ${nuevo.articulo} agregado al Kardex`);
}

// ============================================================================
// 7. SECCIÓN: ESTADOS FINANCIEROS NIIF Y LIBROS OFICIALES
// ============================================================================
function selectEfTab(tab) {
  ACTIVE_EF_TAB = tab;
  document.querySelectorAll("#efSubTabs .filter-chip").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.eftab === tab);
  });
  renderEstadosFinancieros();
}

function getRowCells(r) {
  if (Array.isArray(r)) return r;
  if (r && Array.isArray(r.cells)) return r.cells;
  if (r && typeof r === "object") return Object.values(r);
  return [];
}

function sheetRows(sheet) {
  if (!sheet) return [];
  const raw = Array.isArray(sheet) ? sheet : (Array.isArray(sheet.rows) ? sheet.rows : []);
  return raw.map(getRowCells);
}

function parseNIIFStatementRows(rowsIn) {
  const rows = (rowsIn || []).map(getRowCells);
  const parsed = [];

  rows.forEach((r, idx) => {
    const nonNull = r.filter(c => c !== null && String(c).trim() !== "");
    if (!nonNull.length) return;
    const fullText = nonNull.join(" ").toUpperCase();
    const nums = nonNull.filter(c => typeof c === "number");
    const lastNum = nums.length ? nums[nums.length - 1] : null;

    if (idx < 5 && (fullText.includes("ESTADO") || fullText.includes("ELECTROVIVIENDA") || fullText.includes("NIT") || fullText.includes("PERIODO") || fullText.includes("RRI"))) {
      return; // Cabecera institucional
    }

    if (fullText.includes("CÓDIGO") && fullText.includes("CONCEPTO")) {
      return; // Fila de nombres de columnas
    }

    if (fullText.includes("TOTAL ") || fullText.includes("RESULTADO ") || fullText.includes("UTILIDAD ") || fullText.includes("PERDIDA ")) {
      const cleanConcept = nonNull.find(x => typeof x === "string" && x.trim() !== "-") || "TOTAL";
      parsed.push({ type: "TOTAL", concept: cleanConcept, val: lastNum });
      return;
    }
    if (fullText.includes("SUBTOTAL")) {
      const cleanConcept = nonNull.find(x => typeof x === "string" && x.trim() !== "-") || "SUBTOTAL";
      parsed.push({ type: "SUBTOTAL", concept: cleanConcept, val: lastNum });
      return;
    }

    // Identificar Clases (1 ACTIVOS, 2 PASIVOS, 3 PATRIMONIO, INGRESOS, COSTOS, GASTOS)
    const cleanWords = nonNull.filter(x => typeof x === "string" && x.trim() !== "-").map(x => x.trim());
    if (/^\s*[1-9]\s*$/.test(String(nonNull[0])) && nonNull.length >= 2 && ["ACTIVOS","PASIVOS","PATRIMONIO","INGRESOS","GASTOS","COSTOS"].some(w => String(nonNull[1]).toUpperCase().includes(w))) {
      parsed.push({ type: "CLASE", code: nonNull[0], concept: nonNull[1] });
      return;
    }
    if (["INGRESOS", "COSTOS", "GASTOS"].some(w => cleanWords[0] === w || fullText.endsWith(" " + w))) {
      parsed.push({ type: "CLASE", code: "", concept: cleanWords[0] || fullText });
      return;
    }

    // Identificar Cuentas (4 dígitos)
    const codeCand = nonNull.find(c => /^\d{4}$/.test(String(c).trim()));
    if (codeCand) {
      const codeStr = String(codeCand).trim();
      const textCand = nonNull.find(c => typeof c === "string" && c.trim() !== "-" && c.trim() !== codeStr);
      parsed.push({ type: "CUENTA", code: codeStr, concept: textCand || "", val: lastNum, note: "" });
      return;
    }

    // Grupos / Subsecciones
    const grupoTitle = cleanWords.join(" ");
    if (grupoTitle) {
      parsed.push({ type: "GRUPO", concept: grupoTitle });
    }
  });

  return parsed;
}

function renderOfficialSignaturesBlock() {
  const emp = DB?.empresa || {};
  return `
    <div class="niif-signatures-grid">
      <div class="niif-sign-box">
        <div class="niif-sign-line"></div>
        <div class="niif-sign-role">Contadora Pública Titular</div>
        <div class="niif-sign-name" style="font-weight:800; font-size:0.86rem; color:var(--text-main); margin-top:2px;">Gina Villamizar</div>
        <div style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">T.P. 248910-T • Especialista NIIF</div>
      </div>
      <div class="niif-sign-box">
        <div class="niif-sign-line"></div>
        <div class="niif-sign-role">Representante Legal</div>
        <div class="niif-sign-name" style="font-weight:800; font-size:0.86rem; color:var(--text-main); margin-top:2px;">Kevin Guerrero</div>
        <div style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">Gerencia General • ${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
      </div>
      <div class="niif-sign-box">
        <div class="niif-sign-line"></div>
        <div class="niif-sign-role">Revisora Fiscal</div>
        <div class="niif-sign-name" style="font-weight:800; font-size:0.86rem; color:var(--text-main); margin-top:2px;">Marcela Gonzales</div>
        <div style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">Revisoría Fiscal Independiente • T.P. 182740-T</div>
      </div>
    </div>
  `;
}


function renderCorporateHeaderBoxHtml(title, periodTag, subTag) {
  const emp = DB?.empresa || {};
  return `
    <div class="niif-header-box">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px; margin-bottom:10px; border-bottom:1.5px solid rgba(212,175,55,0.35); padding-bottom:10px;">
        <div style="background:#FFFFFF; padding:6px 14px; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,0.1); border:1px solid #E2E8F0; display:inline-flex; align-items:center;">
          <img src="assets/logo-electrovivienda.png" alt="ELECTROVIVIENDA S.A.S" style="height:44px; width:auto; max-width:220px; object-fit:contain;" />
        </div>
        <div style="text-align:right;">
          <div class="niif-company-title" style="font-size:1.15rem; font-weight:900;">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
          <div class="niif-company-sub">NIT: ${emp.nit || "901.765.438-3"} • ${emp.regimen || "RRI — Agente Autorretenedor de Renta"}</div>
          <div style="font-size:0.72rem; color:var(--text-muted); margin-top:2px;">${emp.direccion || "Cra 21 N° 46-11"} • ${emp.ciudad || "Bucaramanga, Santander"}</div>
        </div>
      </div>
      <div class="niif-statement-badge">
        <div class="niif-statement-name">${title}</div>
        <span class="niif-period-tag">${periodTag}</span>
        ${subTag ? `<span style="font-size:0.7rem; color:#94A3B8; display:block; margin-top:3px;">${subTag}</span>` : ""}
      </div>
    </div>
  `;
}

function renderExecutiveNIIFStatementHtml(rowsIn, statementType, month, statementTitle) {
  const emp = DB?.empresa || {};
  const parsed = parseNIIFStatementRows(rowsIn);
  if (!parsed.length) {
    return `<div class="card"><div class="card-body">No hay datos estructurados para este informe en ${month}.</div></div>`;
  }

  // Extraer totales clave para las tarjetas superiores
  let totActivos = 0, totPasivos = 0, totPatrimonio = 0, totPasivoPat = 0;
  let totIngresos = 0, totCostos = 0, totGastos = 0, resultadoNeto = 0;

  parsed.forEach(p => {
    const uc = String(p.concept || "").toUpperCase();
    if (uc.includes("TOTAL ACTIVOS")) totActivos = p.val || 0;
    else if (uc.includes("TOTAL PASIVOS")) totPasivos = p.val || 0;
    else if (uc.includes("TOTAL PATRIMONIO")) totPatrimonio = p.val || 0;
    else if (uc.includes("TOTAL PASIVO Y PATRIMONIO") || uc.includes("TOTAL PASIVO + PATRIMONIO")) totPasivoPat = p.val || 0;
    else if (uc.includes("TOTAL INGRESOS")) totIngresos = p.val || 0;
    else if (uc.includes("TOTAL COSTOS")) totCostos = p.val || 0;
    else if (uc.includes("TOTAL GASTOS")) totGastos = p.val || 0;
    else if (uc.includes("RESULTADO DEL EJERCICIO") || uc.includes("UTILIDAD") || uc.includes("PERDIDA")) resultadoNeto = p.val || 0;
  });

  const isEsf = statementType === "ESF" || String(statementTitle).toUpperCase().includes("SITUACIÓN") || String(statementTitle).toUpperCase().includes("SITUACION");
  const isEr = statementType === "ER" || String(statementTitle).toUpperCase().includes("RESULTADO");

  // KPI strip
  let kpiHtml = "";
  if (isEsf) {
    const isCuadrado = Math.abs(totActivos - (totPasivos + totPatrimonio)) < 1;
    kpiHtml = `
      <div class="niif-kpi-summary-strip">
        <div class="niif-kpi-pill">
          <span class="kpi-title">🏛️ Total Activos</span>
          <span class="kpi-amount" style="color:var(--brand-primary);">${fmtCOP(totActivos)}</span>
        </div>
        <div class="niif-kpi-pill">
          <span class="kpi-title">💳 Total Pasivos</span>
          <span class="kpi-amount" style="color:#DC2626;">${fmtCOP(totPasivos)}</span>
        </div>
        <div class="niif-kpi-pill">
          <span class="kpi-title">💎 Total Patrimonio</span>
          <span class="kpi-amount" style="color:var(--brand-emerald);">${fmtCOP(totPatrimonio)}</span>
        </div>
        <div class="niif-kpi-pill">
          <span class="kpi-title">⚖️ Ecuación Patrimonial</span>
          <span class="kpi-amount" style="font-size:0.95rem; font-weight:800; color:${isCuadrado ? 'var(--brand-emerald)' : '#DC2626'};">
            ${isCuadrado ? '✓ Activo = Pasivo + Patrimonio' : '⚠️ Descuadre'}
          </span>
          <span style="font-size:0.7rem; color:var(--text-muted);">${fmtCOP(totPasivoPat || (totPasivos + totPatrimonio))}</span>
        </div>
      </div>
    `;
  } else if (isEr) {
    const utilidadBruta = totIngresos - totCostos;
    kpiHtml = `
      <div class="niif-kpi-summary-strip">
        <div class="niif-kpi-pill">
          <span class="kpi-title">💰 Total Ingresos</span>
          <span class="kpi-amount" style="color:var(--brand-emerald);">${fmtCOP(totIngresos)}</span>
        </div>
        <div class="niif-kpi-pill">
          <span class="kpi-title">📦 Total Costos</span>
          <span class="kpi-amount" style="color:#D97706;">${fmtCOP(totCostos)}</span>
        </div>
        <div class="niif-kpi-pill">
          <span class="kpi-title">📊 Utilidad Bruta en Ventas</span>
          <span class="kpi-amount" style="color:var(--brand-primary);">${fmtCOP(utilidadBruta)}</span>
        </div>
        <div class="niif-kpi-pill">
          <span class="kpi-title">💼 Total Gastos Operacionales</span>
          <span class="kpi-amount" style="color:#DC2626;">${fmtCOP(totGastos)}</span>
        </div>
        <div class="niif-kpi-pill">
          <span class="kpi-title">📈 Resultado del Ejercicio</span>
          <span class="kpi-amount" style="color:${resultadoNeto >= 0 ? 'var(--brand-emerald)' : '#DC2626'};">${fmtCOP(resultadoNeto)}</span>
        </div>
      </div>
    `;
  }

  // Generar filas de la tabla
  const tableRows = parsed.map(item => {
    if (item.type === "CLASE") {
      return `
        <tr class="niif-row-clase">
          <td colspan="2">
            <span class="niif-code-pill" style="background:var(--brand-primary); color:#fff; font-weight:800;">${item.code ? `CLASE ${item.code}` : "NIIF"}</span>
            <strong style="margin-left:8px; letter-spacing:0.4px;">${item.concept}</strong>
          </td>
          <td style="text-align:center;"></td>
          <td class="num-col"></td>
        </tr>
      `;
    }
    if (item.type === "GRUPO") {
      return `
        <tr class="niif-row-grupo">
          <td colspan="3"><strong>${item.concept}</strong></td>
          <td class="num-col"></td>
        </tr>
      `;
    }
    if (item.type === "CUENTA") {
      const isNeg = (item.val || 0) < 0;
      return `
        <tr class="niif-row-cuenta">
          <td class="code-col"><span class="niif-code-pill">${item.code}</span></td>
          <td>${item.concept}</td>
          <td style="text-align:center; color:var(--text-muted); font-size:0.75rem;">${item.note || ""}</td>
          <td class="num-col" style="${isNeg ? 'color:#DC2626; font-weight:700;' : ''}">${item.val !== null ? fmtCOP(item.val) : "-"}</td>
        </tr>
      `;
    }
    if (item.type === "SUBTOTAL") {
      return `
        <tr class="niif-row-subtotal">
          <td colspan="3"><strong>${item.concept}</strong></td>
          <td class="num-col"><strong>${fmtCOP(item.val || 0)}</strong></td>
        </tr>
      `;
    }
    if (item.type === "TOTAL") {
      return `
        <tr class="niif-row-total">
          <td colspan="3"><strong>${item.concept}</strong></td>
          <td class="num-col"><strong>${fmtCOP(item.val || 0)}</strong></td>
        </tr>
      `;
    }
    return "";
  }).join("");

  return `
    <div class="niif-statement-paper">
${renderCorporateHeaderBoxHtml(statementTitle || "ESTADO FINANCIERO OFICIAL NIIF", `Al corte del período: ${month} 2026`, "Cifras en Pesos Colombianos (COP) • NIIF para las PYMES (Grupo 2)")}

      ${kpiHtml}

      <div class="table-wrap">
        <table class="niif-table">
          <thead>
            <tr>
              <th style="width:110px;">Código</th>
              <th>Concepto / Cuenta NIIF</th>
              <th style="width:90px; text-align:center;">Notas</th>
              <th style="width:190px;" class="num-col">Saldo Oficial (COP)</th>
            </tr>
          </thead>
          <tbody>
            ${tableRows}
          </tbody>
        </table>
      </div>

      ${renderOfficialSignaturesBlock()}
    </div>
  `;
}

function renderConsolidatedComparativeStatementHtml(rowsIn, statementType, month, statementTitle) {
  const emp = DB?.empresa || {};
  const rows = (rowsIn || []).map(getRowCells);
  if (!rows.length) {
    return `<div class="card"><div class="card-body">Sin datos en consolidado para ${month}.</div></div>`;
  }

  // Find column header row
  let headerRowIdx = 4;
  for (let i = 0; i < Math.min(8, rows.length); i++) {
    const nonNull = rows[i].filter(c => c !== null).map(c => String(c).trim().toUpperCase());
    if (nonNull.includes("CONCEPTO") || nonNull.includes("SALDO") || nonNull.includes("VARIACION $") || nonNull.includes("VARIACIÓN $") || (nonNull.includes("CÓDIGO") && nonNull.length >= 3)) {
      headerRowIdx = i;
      break;
    }
  }

  let firstCol = 99;
  for (let r = headerRowIdx; r < rows.length; r++) {
    for (let c = 0; c < rows[r].length; c++) {
      if (rows[r][c] !== null && String(rows[r][c]).trim() !== "") {
        if (c < firstCol) firstCol = c;
      }
    }
  }
  if (firstCol === 99) firstCol = 0;

  const rawHeaders = rows[headerRowIdx].slice(firstCol);

  const theadHtml = `
    <thead>
      <tr>
        ${rawHeaders.map((h, hIdx) => {
          const txt = h !== null && h !== undefined ? String(h).trim() : "";
          const isNumHeader = hIdx >= 2;
          return `<th style="${isNumHeader ? 'text-align:right;' : ''}">${txt}</th>`;
        }).join("")}
      </tr>
    </thead>
  `;

  const dataRows = rows.slice(headerRowIdx + 1);
  let tbodyHtml = "";

  dataRows.forEach(r => {
    const nonNull = r.filter(c => c !== null && String(c).trim() !== "");
    if (!nonNull.length) return;
    const fullText = nonNull.join(" ").toUpperCase();
    if (fullText === "0") return;

    const isTotalRow = fullText.includes("TOTAL ACTIVOS") || fullText.includes("TOTAL PASIVOS") || fullText.includes("TOTAL PATRIMONIO") || fullText.includes("TOTAL PASIVO Y PATRIMONIO") || fullText.includes("TOTAL INGRESOS") || fullText.includes("TOTAL COSTOS") || fullText.includes("TOTAL GASTOS") || fullText.includes("RESULTADO DEL EJERCICIO");
    const isSubtotalRow = fullText.includes("SUBTOTAL");
    const isClassRow = ["ACTIVOS", "PASIVOS", "PATRIMONIO", "INGRESOS", "COSTOS", "GASTOS"].some(w => (fullText === w || fullText.includes(` ${w}`)) && !isTotalRow && !isSubtotalRow && nonNull.length <= 3);
    const isGroupRow = !isTotalRow && !isSubtotalRow && !isClassRow && nonNull.length <= 2 && !/^\d{4}$/.test(String(nonNull[0]).trim());

    if (isClassRow) {
      const className = nonNull.find(x => typeof x === "string" && x.trim() !== "-") || fullText;
      const classCode = nonNull.find(x => /^[1-9]$/.test(String(x).trim())) || "";
      tbodyHtml += `
        <tr class="niif-row-clase">
          <td colspan="${rawHeaders.length}">
            <span class="niif-code-pill" style="background:var(--brand-primary); color:#fff; font-weight:800;">${classCode ? `CLASE ${classCode}` : "NIIF"}</span>
            <strong style="margin-left:8px; letter-spacing:0.4px;">${className}</strong>
          </td>
        </tr>
      `;
      return;
    }

    if (isGroupRow) {
      tbodyHtml += `
        <tr class="niif-row-grupo">
          <td colspan="${rawHeaders.length}"><strong>${nonNull.join(" ")}</strong></td>
        </tr>
      `;
      return;
    }

    let trCls = "niif-row-cuenta";
    if (isTotalRow) trCls = "niif-row-total";
    else if (isSubtotalRow) trCls = "niif-row-subtotal";

    const tdCells = [];
    for (let c = firstCol; c < firstCol + rawHeaders.length; c++) {
      const v = r[c];
      const hTitle = String(rawHeaders[c - firstCol] || "").toUpperCase();
      let disp = "";
      let cls = "";

      if (typeof v === "number") {
        if (hTitle.includes("%") || (Math.abs(v) <= 1 && v !== 0 && !hTitle.includes("ENERO") && !hTitle.includes("FEBRERO") && !hTitle.includes("MARZO") && !hTitle.includes("ABRIL"))) {
          disp = (v * 100).toFixed(1) + "%";
          cls = "num-col" + (v < 0 ? " text-danger" : "");
        } else {
          disp = fmtCOP(v);
          cls = "num-col" + (v < 0 ? " text-danger" : "");
        }
      } else if (v !== null && v !== undefined && String(v).trim() !== "") {
        disp = String(v).trim();
        if (/^\d{4}$/.test(disp)) {
          disp = `<span class="niif-code-pill">${disp}</span>`;
          cls = "code-col";
        }
      }

      tdCells.push(`<td class="${cls}">${disp}</td>`);
    }

    tbodyHtml += `<tr class="${trCls}">${tdCells.join("")}</tr>`;
  });

  return `
    <div class="niif-statement-paper">
${renderCorporateHeaderBoxHtml(statementTitle || "ESTADO FINANCIERO CONSOLIDADO NIIF", `Corte Consolidado Comparativo — ${month} 2026`, "Cifras en Pesos Colombianos (COP) • NIIF para las PYMES (Grupo 2) • Variaciones y Sumas Corridas")}

      <div class="table-wrap">
        <table class="niif-table niif-table-consolidado">
          ${theadHtml}
          <tbody>
            ${tbodyHtml}
          </tbody>
        </table>
      </div>

      ${renderOfficialSignaturesBlock()}
    </div>
  `;
}

function renderClassifiedTrialBalance(txs, period) {
  const saldos4 = new Map();
  (txs || []).forEach(t => {
    (t.asientos || []).forEach(a => {
      const c = String(a.codigo || "").trim();
      if (c.length === 4 && (a.debe > 0 || a.haber > 0)) {
        if (!saldos4.has(c)) {
          saldos4.set(c, { codigo: c, cuenta: a.cuenta, debe: 0, haber: 0 });
        }
        const item = saldos4.get(c);
        item.debe += Number(a.debe) || 0;
        item.haber += Number(a.haber) || 0;
      }
    });
  });

  const list = Array.from(saldos4.values()).sort((a, b) => a.codigo.localeCompare(b.codigo));
  
  const classNames = {
    "1": "CLASE 1: ACTIVOS (Naturaleza Débito)",
    "2": "CLASE 2: PASIVOS (Naturaleza Crédito)",
    "3": "CLASE 3: PATRIMONIO (Naturaleza Crédito)",
    "4": "CLASE 4: INGRESOS (Naturaleza Crédito)",
    "5": "CLASE 5: GASTOS OPERACIONALES (Naturaleza Débito)",
    "6": "CLASE 6: COSTOS DE VENTA (Naturaleza Débito)"
  };

  const groups = {};
  list.forEach(item => {
    const cl = item.codigo.charAt(0);
    if (!groups[cl]) groups[cl] = [];
    groups[cl].push(item);
  });

  let grandDebe = 0;
  let grandHaber = 0;

  const sectionsHtml = Object.keys(classNames).map(cl => {
    const items = groups[cl] || [];
    if (!items.length) return "";
    let clDebe = 0;
    let clHaber = 0;

    const rowsHtml = items.map(s => {
      clDebe += s.debe;
      clHaber += s.haber;
      grandDebe += s.debe;
      grandHaber += s.haber;
      const isDeudora = (cl === "1" || cl === "5" || cl === "6");
      const saldoNeto = isDeudora ? (s.debe - s.haber) : (s.haber - s.debe);
      return `
        <tr>
          <td class="code-col"><span class="niif-code-pill">${s.codigo}</span></td>
          <td><strong>${s.cuenta}</strong></td>
          <td class="num-col">${fmtCOP(s.debe)}</td>
          <td class="num-col">${fmtCOP(s.haber)}</td>
          <td class="num-col" style="font-weight:700;">${fmtCOP(saldoNeto)}</td>
        </tr>
      `;
    }).join("");

    const clSaldo = (cl === "1" || cl === "5" || cl === "6") ? (clDebe - clHaber) : (clHaber - clDebe);

    return `
      <div style="margin-bottom:20px;">
        <div style="background:var(--brand-primary); color:#FFFFFF; padding:8px 14px; font-weight:800; font-size:0.84rem; border-radius:6px 6px 0 0; display:flex; justify-content:space-between; align-items:center;">
          <span>${classNames[cl]}</span>
          <span style="font-size:0.75rem; color:var(--brand-gold);">Saldo Neto: ${fmtCOP(clSaldo)}</span>
        </div>
        <div class="table-wrap" style="border-radius:0 0 6px 6px; border-top:none;">
          <table class="acct-table">
            <thead>
              <tr>
                <th style="width:110px;">Código</th>
                <th>Denominación PUC (4 Dígitos)</th>
                <th class="num-col" style="width:160px;">Total Débitos</th>
                <th class="num-col" style="width:160px;">Total Créditos</th>
                <th class="num-col" style="width:170px;">Saldo Neto</th>
              </tr>
            </thead>
            <tbody>
              ${rowsHtml}
              <tr style="background:var(--bg-subtle); font-weight:800; border-top:2px solid var(--border-strong);">
                <td colspan="2">SUBTOTAL ${classNames[cl]}</td>
                <td class="num-col">${fmtCOP(clDebe)}</td>
                <td class="num-col">${fmtCOP(clHaber)}</td>
                <td class="num-col">${fmtCOP(clSaldo)}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `;
  }).join("");

  const isCuadrado = Math.abs(grandDebe - grandHaber) < 0.01;

  return `
    <div class="niif-statement-paper">
      <div class="niif-header-box">
        <div class="niif-company-title">ELECTROVIVIENDA S.A.S</div>
        <div class="niif-company-sub">NIT: 901.765.438-3 • RRI — Agente Autorretenedor de Renta</div>
        <div class="niif-statement-badge">
          <div class="niif-statement-name">BALANCE DE COMPROBACIÓN CLASIFICADO</div>
          <span class="niif-period-tag">Período: ${period} 2026</span>
          <span style="font-size:0.7rem; color:#94A3B8; display:block; margin-top:3px;">6 Clases del PUC • Principio Universal de Partida Doble</span>
        </div>
      </div>

      <div style="margin-bottom:16px;">
        ${sectionsHtml}
      </div>

      <div style="background:var(--brand-gold-soft); border:2px solid var(--brand-gold); border-radius:8px; padding:16px 20px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-top:14px;">
        <div>
          <div style="font-weight:900; font-size:1.05rem; color:var(--brand-primary);">TOTAL SUMAS IGUALES DEL MES:</div>
          <div style="font-size:0.75rem; color:var(--text-secondary);">Verificación del principio contable universal de partida doble</div>
        </div>
        <div style="display:flex; gap:20px; font-family:'JetBrains Mono', monospace; font-size:1.15rem; font-weight:900;">
          <div><span style="font-size:0.72rem; color:var(--text-muted); display:block; font-family:sans-serif;">TOTAL DÉBITOS:</span> ${fmtCOP(grandDebe)}</div>
          <div><span style="font-size:0.72rem; color:var(--text-muted); display:block; font-family:sans-serif;">TOTAL CRÉDITOS:</span> ${fmtCOP(grandHaber)}</div>
        </div>
      </div>

      ${renderOfficialSignaturesBlock()}
    </div>
  `;
}

function renderNotasNIIFStatementHtml(month) {
  const emp = DB?.empresa || {};
  const esp = DB?.meses?.[month]?.hojas_especiales || {};
  const notasKey = Object.keys(esp).find(k => k.toUpperCase().includes("NOTA"));

  let noteBlocks = [];

  if (notasKey && esp[notasKey]) {
    const rawRows = sheetRows(esp[notasKey]).map(getRowCells);
    const lines = [];
    rawRows.forEach(r => {
      const parts = r.filter(c => c !== null && c !== undefined && String(c).trim() !== "").map(c => String(c).trim());
      if (parts.length) {
        lines.push(parts.join(" — "));
      }
    });

    const contentLines = lines.slice(4);
    let curBlock = null;

    contentLines.forEach(line => {
      const upper = line.toUpperCase();
      if (/^NOTA\s+\d+/i.test(line)) {
        if (curBlock) noteBlocks.push(curBlock);
        curBlock = { nota: line, title: "", paragraphs: [] };
      } else if (curBlock) {
        if (!curBlock.title && upper === line && line.length < 90 && !line.includes("$")) {
          curBlock.title = line;
        } else {
          curBlock.paragraphs.push(line);
        }
      } else if (upper.includes("ACTIVOS") || upper.includes("PASIVOS") || upper.includes("PATRIMONIO")) {
        noteBlocks.push({ isSectionHeader: true, title: line });
      }
    });
    if (curBlock) noteBlocks.push(curBlock);
  }

  if (!noteBlocks.length) {
    noteBlocks = [
      {
        nota: "NOTA 1",
        title: "IDENTIFICACIÓN Y NATURALEZA DE LA ENTIDAD",
        paragraphs: [
          `${emp.razon_social || "ELECTROVIVIENDA S.A.S"}, identificada con NIT ${emp.nit || "901.765.438-3"}, domiciliada en ${emp.direccion || "Cra. 21 # 46-11, Bucaramanga, Santander"}. Es una persona jurídica constituida bajo las leyes de Colombia, perteneciente al Régimen Responsable de IVA (RRI), Agente de Retención en la Fuente y Autorretenedor en Renta, dedicada al comercio al por mayor y al detal de gasodomésticos y electrodomésticos.`
        ]
      },
      {
        nota: "NOTA 2",
        title: "BASES DE PREPARACIÓN Y MARCO TÉCNICO NORMATIVO (NIIF PARA LAS PYMES - GRUPO 2)",
        paragraphs: [
          "Los estados financieros han sido preparados bajo el marco técnico de las Normas Internacionales de Información Financiera para Pequeñas y Medianas Entidades (NIIF para las PYMES), incorporadas a la legislación colombiana mediante el Decreto Único Reglamentario 2420 de 2015 y sus decretos modificatorios.",
          "Principio de Acumulación o Devengo (Sección 2 NIIF PYMES): Las transacciones y demás hechos económicos se reconocen contablemente en el período en que ocurren y no cuando se produce el movimiento de fondos.",
          "Hipótesis de Negocio en Marcha (Sección 3 NIIF PYMES): Los estados financieros se preparan bajo el supuesto de continuidad operativa por un período no inferior a un año a partir de la fecha de corte."
        ]
      },
      {
        nota: "NOTA 3",
        title: "POLÍTICAS DE EFECTIVO Y EQUIVALENTES AL EFECTIVO (GRUPO 11)",
        paragraphs: [
          "Comprende el disponible en Caja General (110505), Cajas Menores (110510) y Cuentas Bancarias Comerciales en moneda legal colombiana. Se miden a su valor nominal y representan alta liquidez para atender obligaciones inmediatas."
        ]
      },
      {
        nota: "NOTA 4",
        title: "POLÍTICA DE INVENTARIOS Y MÉTODO DE VALUACIÓN (GRUPO 14)",
        paragraphs: [
          "Los inventarios de mercancías (1435) son administrados permanentemente y valuados mediante la fórmula del Costo Promedio Ponderado, controlados a través de tarjetas Kardex analíticas por referencia comercial."
        ]
      },
      {
        nota: "NOTA 5",
        title: "CAPITAL SOCIAL, RESERVAS Y PATRIMONIO (GRUPOS 31 A 37)",
        paragraphs: [
          "El Capital Suscrito y Pagado (3105) asciende a $280.000.000, respaldado en aportes de capital según Comprobante de Apertura N° 1.",
          "La Reserva Legal (3305) se apropia según el artículo 452 del Código de Comercio (10% de las utilidades líquidas del ejercicio)."
        ]
      }
    ];
  }

  const blocksHtml = noteBlocks.map(b => {
    if (b.isSectionHeader) {
      return `
        <div style="background:var(--brand-primary); color:#FFFFFF; padding:8px 14px; border-radius:4px; font-weight:900; font-size:0.86rem; letter-spacing:0.5px; margin:16px 0 8px 0;">
          📌 ${b.title}
        </div>
      `;
    }
    const parasHtml = (b.paragraphs || []).map(p => {
      const isSub = p.startsWith("·") || p.startsWith("•") || p.startsWith("Grupo ") || (p.includes(":") && p.indexOf(":") < 45 && !p.startsWith("http"));
      if (isSub && p.length < 90) {
        return `<div class="niif-nota-subtitle">${p}</div>`;
      }
      return `<p class="niif-nota-text">${p}</p>`;
    }).join("");

    return `
      <div class="niif-nota-card">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px; flex-wrap:wrap;">
          <span class="niif-nota-badge">${b.nota}</span>
          ${b.title ? `<div class="niif-nota-title" style="margin:0;">${b.title}</div>` : ""}
        </div>
        <div style="padding-left:4px;">
          ${parasHtml}
        </div>
      </div>
    `;
  }).join("");

  return `
    <div class="niif-statement-paper">
      <div class="niif-header-box">
        <div class="niif-company-title">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
        <div class="niif-company-sub">NIT: ${emp.nit || "901.765.438-3"} • ${emp.regimen || "RRI — Agente Autorretenedor de Renta"}</div>
        <div class="niif-statement-badge">
          <div class="niif-statement-name">NOTAS Y REVELACIONES A LOS ESTADOS FINANCIEROS</div>
          <span class="niif-period-tag">Período Contable: ${month} 2026</span>
          <span style="font-size:0.7rem; color:#94A3B8; display:block; margin-top:3px;">
            Decreto Único Reglamentario 2420 de 2015 • NIIF para las PYMES (Grupo 2)
          </span>
        </div>
      </div>

      <div class="niif-notas-container">
        ${blocksHtml}
      </div>

      ${renderOfficialSignaturesBlock()}
    </div>
  `;
}


function renderECPStatementHtml(rowsIn, month) {
  const emp = DB?.empresa || {};
  const rows = (rowsIn || []).map(getRowCells);
  if (!rows.length) {
    return `<div class="card"><div class="card-body">Sin datos de Estado de Cambios en el Patrimonio para ${month}.</div></div>`;
  }

  let periodText = `Período Comparativo: 1 de Marzo al 30 de ${month} de 2026`;
  if (rows[2] && rows[2].length > 1 && rows[2][1]) {
    periodText = String(rows[2][1]).trim();
  }

  const prevMonthName = month === "ABRIL" ? "MARZO" : (month === "MARZO" ? "FEBRERO" : "ANTERIOR");
  let hSaldoIni = `SALDO ${prevMonthName}`;
  let hSaldoFin = `SALDO ${month}`;

  let colHeaderRow = rows.find(r => {
    const txt = (r || []).filter(c => c != null).join(" ").toUpperCase();
    return txt.includes("CUENTA") && (txt.includes("SALDO") || txt.includes("AUMENTO"));
  });

  if (colHeaderRow) {
    const nonNull = colHeaderRow.filter(c => c != null).map(String);
    const sIni = nonNull.find(x => x.toUpperCase().includes("SALDO") && !x.toUpperCase().includes(month));
    const sFin = nonNull.find(x => x.toUpperCase().includes("SALDO") && x.toUpperCase().includes(month));
    if (sIni) hSaldoIni = sIni;
    if (sFin) hSaldoFin = sFin;
  }

  const items = [];
  let totalRow = null;

  rows.forEach((r, idx) => {
    if (idx < 3) return;
    const nonNull = r.filter(c => c !== null && String(c).trim() !== "");
    if (!nonNull.length) return;
    const fullText = nonNull.join(" ").toUpperCase();
    if (fullText.includes("CUENTA") && fullText.includes("AUMENTO")) return;

    if (fullText.includes("TOTAL PATRIMONIO") || fullText.includes("TOTAL PATRIMONIAL")) {
      totalRow = {
        label: "TOTAL PATRIMONIO NETO",
        saldoIni: typeof r[3] === "number" ? r[3] : (parseFloat(r[3]) || 0),
        aumento: typeof r[4] === "number" ? r[4] : (parseFloat(r[4]) || 0),
        disminucion: typeof r[5] === "number" ? r[5] : (parseFloat(r[5]) || 0),
        saldoFin: typeof r[6] === "number" ? r[6] : (parseFloat(r[6]) || 0)
      };
      return;
    }

    const code = r[1] != null && !isNaN(r[1]) ? String(r[1]).trim() : (r[1] != null ? String(r[1]).trim() : "");
    const concept = r[2] != null ? String(r[2]).trim() : "";
    const sIni = typeof r[3] === "number" ? r[3] : (parseFloat(r[3]) || 0);
    const aum = typeof r[4] === "number" ? r[4] : (parseFloat(r[4]) || 0);
    const dis = typeof r[5] === "number" ? r[5] : (parseFloat(r[5]) || 0);
    const sFin = typeof r[6] === "number" ? r[6] : (parseFloat(r[6]) || 0);

    if (code || concept) {
      items.push({ code, concept, saldoIni: sIni, aumento: aum, disminucion: dis, saldoFin: sFin });
    }
  });

  if (!totalRow && items.length) {
    totalRow = {
      label: "TOTAL PATRIMONIO NETO",
      saldoIni: items.reduce((acc, x) => acc + x.saldoIni, 0),
      aumento: items.reduce((acc, x) => acc + x.aumento, 0),
      disminucion: items.reduce((acc, x) => acc + x.disminucion, 0),
      saldoFin: items.reduce((acc, x) => acc + x.saldoFin, 0)
    };
  }

  const varNeta = totalRow ? (totalRow.saldoFin - totalRow.saldoIni) : 0;
  const pctVar = (totalRow && totalRow.saldoIni !== 0) ? ((varNeta / totalRow.saldoIni) * 100).toFixed(2) : "0.00";

  const kpiHtml = `
    <div class="niif-kpi-summary-strip" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:12px; margin-bottom:20px;">
      <div class="niif-kpi-pill">
        <span class="kpi-title">Saldo Inicial Patrimonio (${prevMonthName})</span>
        <span class="kpi-amount">${fmtCOP(totalRow ? totalRow.saldoIni : 0)}</span>
        <span style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">Corte anterior</span>
      </div>
      <div class="niif-kpi-pill">
        <span class="kpi-title">Aumentos del Período (+)</span>
        <span class="kpi-amount" style="color:#059669;">+ ${fmtCOP(totalRow ? totalRow.aumento : 0)}</span>
        <span style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">Traslados a pérdidas acumuladas</span>
      </div>
      <div class="niif-kpi-pill">
        <span class="kpi-title">Disminuciones del Período (-)</span>
        <span class="kpi-amount" style="color:#DC2626;">- ${fmtCOP(totalRow ? totalRow.disminucion : 0)}</span>
        <span style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">Pérdida del ejercicio aplicada</span>
      </div>
      <div class="niif-kpi-pill" style="border-color:var(--brand-gold);">
        <span class="kpi-title" style="color:var(--brand-gold);">Saldo Final Patrimonio (${month})</span>
        <span class="kpi-amount" style="color:var(--brand-gold);">${fmtCOP(totalRow ? totalRow.saldoFin : 0)}</span>
        <span style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">Variación: ${varNeta < 0 ? '-' : '+'}${fmtCOP(Math.abs(varNeta))} (${pctVar}%)</span>
      </div>
    </div>
  `;

  const tbodyRows = items.map(it => {
    return `
      <tr class="niif-row-cuenta">
        <td class="code-col" style="width:90px;"><span class="niif-code-pill">${it.code}</span></td>
        <td><strong>${it.concept}</strong></td>
        <td class="num-col" style="width:170px;">${fmtCOP(it.saldoIni)}</td>
        <td class="num-col" style="width:160px; ${it.aumento > 0 ? 'color:#059669; font-weight:700;' : 'color:var(--text-muted);'}">${it.aumento !== 0 ? fmtCOP(it.aumento) : "-"}</td>
        <td class="num-col" style="width:160px; ${it.disminucion > 0 ? 'color:#DC2626; font-weight:700;' : 'color:var(--text-muted);'}">${it.disminucion !== 0 ? fmtCOP(it.disminucion) : "-"}</td>
        <td class="num-col" style="width:180px; font-weight:800; color:var(--text-main);">${fmtCOP(it.saldoFin)}</td>
      </tr>
    `;
  }).join("");

  const totalHtml = totalRow ? `
    <tr class="niif-row-total" style="font-size:0.92rem; background:rgba(212,175,55,0.14); border-top:2px solid var(--brand-gold);">
      <td colspan="2"><strong>${totalRow.label}</strong></td>
      <td class="num-col"><strong>${fmtCOP(totalRow.saldoIni)}</strong></td>
      <td class="num-col" style="color:#059669;"><strong>${fmtCOP(totalRow.aumento)}</strong></td>
      <td class="num-col" style="color:#DC2626;"><strong>${fmtCOP(totalRow.disminucion)}</strong></td>
      <td class="num-col" style="color:var(--brand-gold); font-weight:900;"><strong>${fmtCOP(totalRow.saldoFin)}</strong></td>
    </tr>
  ` : "";

  return `
    <div class="niif-statement-paper">
${renderCorporateHeaderBoxHtml("ESTADO DE CAMBIOS EN EL PATRIMONIO (ECP)", periodText, "NIIF para las PYMES (Sección 6) • Cifras en Pesos Colombianos (COP) • Sumas Corridas")}

      ${kpiHtml}

      <div class="table-wrap">
        <table class="niif-table">
          <thead>
            <tr>
              <th style="width:90px;">Código</th>
              <th>Cuenta / Rubro Patrimonial</th>
              <th style="width:170px;" class="num-col">${hSaldoIni} (COP)</th>
              <th style="width:160px;" class="num-col">Aumentos (+)</th>
              <th style="width:160px;" class="num-col">Disminuciones (-)</th>
              <th style="width:180px;" class="num-col">${hSaldoFin} (COP)</th>
            </tr>
          </thead>
          <tbody>
            ${tbodyRows}
            ${totalHtml}
          </tbody>
        </table>
      </div>

      <div style="margin-top:16px; margin-bottom:24px; padding:12px 16px; background:var(--bg-subtle); border-left:4px solid var(--brand-gold); border-radius:4px; font-size:0.78rem; color:var(--text-secondary); line-height:1.5;">
        <strong>📝 REVELACIONES SOBRE LAS VARIACIONES DEL PATRIMONIO (${month} 2026):</strong><br/>
        • <strong>Capital Suscrito y Pagado (3105):</strong> Saldo constante de $248.600.000 respaldado por aportes de socios.<br/>
        • <strong>Reservas Obligatorias (3305):</strong> Saldo de $1.827.342,50 correspondiente a reserva legal del 10%.<br/>
        • <strong>Resultado del Ejercicio (3610):</strong> Saldo de $7.887.158,12 por pérdida neta del ejercicio de Abril 2026.<br/>
        • <strong>Pérdidas Acumuladas (3710):</strong> Traslado de la pérdida de Marzo ($17.154.576,67) alcanzando saldo acumulado de -$18.425.826,67.<br/>
        • <strong>Patrimonio Neto Total:</strong> Cierra en <strong>$240.560.440,20</strong> cuadrando exactamente con el Balance de Situación Financiera.
      </div>

      ${renderOfficialSignaturesBlock()}
    </div>
  `;
}

function renderFlujoEfectivoStatementHtml(rowsIn, month) {
  const emp = DB?.empresa || {};
  const rows = (rowsIn || []).map(getRowCells);
  if (!rows.length) {
    return `<div class="card"><div class="card-body">Sin datos de Flujo de Efectivo para ${month}.</div></div>`;
  }

  // 1. Extraer datos del Estado Oficial (columnas 6 a 8 del Excel)
  const oficialRows = [];
  rows.slice(3).forEach(r => {
    const c6 = r[6] != null ? r[6] : null;
    const c7 = r[7] != null ? r[7] : null;
    const c8 = r[8] != null ? r[8] : null;
    if (c6 === null && c7 === null && c8 === null) return;
    const txt = [c6, c7, c8].filter(x => x !== null).join(" ").trim().toUpperCase();
    if (txt.includes("CÓDIGO") && txt.includes("DETALLE")) return;
    oficialRows.push({ c6, c7, c8, txt });
  });

  let kpiEfectivoIni = 93502800;
  let kpiEfectivoFin = 25430816.44;
  let kpiVarNeta = -68071983.56;
  let kpiFlujoOp = -4250920.39;

  rows.forEach(r => {
    const c6 = r[6] != null ? String(r[6]).toUpperCase() : "";
    const c8 = typeof r[8] === "number" ? r[8] : (typeof r[7] === "number" ? r[7] : null);
    if (c6.includes("EFECTIVO A ") && c8 != null) kpiEfectivoIni = c8;
    if (c6.includes("EFECTIVO FINAL") && c8 != null) kpiEfectivoFin = c8;
    if (c6.includes("TOTAL AUMENTO") && c8 != null) kpiVarNeta = c8;
  });

  let oficialTbody = "";
  oficialRows.forEach(item => {
    const { c6, c7, c8, txt } = item;
    const isSection = ["INVERSIÓN", "OPERACIONAL", "FINANCIACIÓN", "PARTIDAS QUE NO AFECTAN"].some(w => txt.includes(w));
    const isTotal = txt.includes("TOTAL AUMENTO") || txt.includes("EFECTIVO FINAL") || txt.includes("EFECTIVO A ");
    const isSubtotal = txt.includes("SUBTOTAL");

    if (isSection) {
      oficialTbody += `
        <tr class="niif-row-clase">
          <td colspan="3">
            <span class="niif-code-pill" style="background:var(--brand-primary); color:#fff; font-weight:800;">ACTIVIDADES</span>
            <strong style="margin-left:8px; letter-spacing:0.4px;">${txt}</strong>
          </td>
        </tr>
      `;
    } else if (isTotal) {
      const label = c6 || c7 || "TOTAL FLUJO DE EFECTIVO";
      const val = c8 != null ? c8 : c7;
      oficialTbody += `
        <tr class="niif-row-total">
          <td colspan="2"><strong>${label}</strong></td>
          <td class="num-col"><strong>${typeof val === "number" ? fmtCOP(val) : val}</strong></td>
        </tr>
      `;
    } else if (isSubtotal) {
      const val = c8 != null ? c8 : c7;
      oficialTbody += `
        <tr class="niif-row-subtotal">
          <td colspan="2"><strong>SUBTOTAL FLUJO NETO</strong></td>
          <td class="num-col"><strong>${typeof val === "number" ? fmtCOP(val) : val}</strong></td>
        </tr>
      `;
    } else {
      const codeStr = c6 != null ? String(c6).trim() : "";
      const isNum = typeof c8 === "number";
      const isNeg = isNum && c8 < 0;
      oficialTbody += `
        <tr class="niif-row-cuenta">
          <td class="code-col" style="width:90px;">${codeStr ? `<span class="niif-code-pill">${codeStr}</span>` : ""}</td>
          <td>${c7 || ""}</td>
          <td class="num-col ${isNeg ? 'text-danger' : ''}" style="width:160px; ${isNeg ? 'font-weight:700;' : ''}">${isNum ? fmtCOP(c8) : (c8 || "-")}</td>
        </tr>
      `;
    }
  });

  // 2. Extraer datos de la Hoja de Trabajo de Variaciones de Balance (columnas 1 a 4 del Excel)
  const varRows = [];
  rows.slice(3).forEach(r => {
    const c1 = r[1] != null ? r[1] : null;
    const c2 = r[2] != null ? r[2] : null;
    const c3 = r[3] != null ? r[3] : null;
    const c4 = r[4] != null ? r[4] : null;
    if (c1 === null && c2 === null && c3 === null && c4 === null) return;
    const txt = [c1, c2, c3, c4].filter(x => x !== null).join(" ").trim().toUpperCase();
    if (txt.includes("CÓDIGO") && txt.includes("CONCEPTO")) return;
    varRows.push({ c1, c2, c3, c4, txt });
  });

  let varTbody = "";
  varRows.forEach(item => {
    const { c1, c2, c3, c4, txt } = item;
    const isClass = ["ACTIVOS", "ACTIVO", "PASIVOS", "PATRIMONIO"].some(w => txt === w || txt.startsWith(w + " ") || txt.endsWith(" " + w));
    const isTotal = txt.includes("TOTAL AUMENTO") || txt.includes("EFECTIVO FINAL") || txt.includes("EFECTIVO A ");
    const isSubtotal = txt.includes("SUBTOTAL");

    if (isClass) {
      varTbody += `
        <tr class="niif-row-clase">
          <td colspan="4">
            <span class="niif-code-pill" style="background:var(--brand-primary); color:#fff; font-weight:800;">GRUPO BALANCE</span>
            <strong style="margin-left:8px; letter-spacing:0.4px;">${txt}</strong>
          </td>
        </tr>
      `;
    } else if (isTotal) {
      const label = c1 || c2 || "TOTAL EFECTIVO";
      const val = c4 != null ? c4 : c3;
      varTbody += `
        <tr class="niif-row-total">
          <td colspan="3"><strong>${label}</strong></td>
          <td class="num-col"><strong>${typeof val === "number" ? fmtCOP(val) : val}</strong></td>
        </tr>
      `;
    } else if (isSubtotal) {
      varTbody += `
        <tr class="niif-row-subtotal">
          <td colspan="2"><strong>SUBTOTAL</strong></td>
          <td class="num-col"><strong>${typeof c3 === "number" ? fmtCOP(c3) : ""}</strong></td>
          <td class="num-col"><strong>${typeof c4 === "number" ? fmtCOP(c4) : ""}</strong></td>
        </tr>
      `;
    } else {
      const codeStr = c1 != null ? String(c1).trim() : "";
      const isNeg = typeof c4 === "number" && c4 < 0;
      varTbody += `
        <tr class="niif-row-cuenta">
          <td class="code-col" style="width:85px;">${codeStr ? `<span class="niif-code-pill">${codeStr}</span>` : ""}</td>
          <td>${c2 || ""}</td>
          <td class="num-col" style="width:140px;">${typeof c3 === "number" ? fmtCOP(c3) : (c3 || "-")}</td>
          <td class="num-col ${isNeg ? 'text-danger' : ''}" style="width:140px; ${isNeg ? 'font-weight:700;' : ''}">${typeof c4 === "number" ? fmtCOP(c4) : (c4 || "-")}</td>
        </tr>
      `;
    }
  });

  const kpiFlujoHtml = `
    <div class="niif-kpi-summary-strip" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:12px; margin-bottom:20px;">
      <div class="niif-kpi-pill">
        <span class="kpi-title">Saldo Inicial Efectivo (Marzo)</span>
        <span class="kpi-amount">${fmtCOP(kpiEfectivoIni)}</span>
        <span style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">Caja + Bancos inicio de mes</span>
      </div>
      <div class="niif-kpi-pill">
        <span class="kpi-title">Flujo Actividades de Operación</span>
        <span class="kpi-amount" style="color:#DC2626;">${fmtCOP(kpiFlujoOp)}</span>
        <span style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">Proveedores, inventarios e impuestos</span>
      </div>
      <div class="niif-kpi-pill">
        <span class="kpi-title">Variación Neta del Efectivo</span>
        <span class="kpi-amount" style="color:#DC2626;">${fmtCOP(kpiVarNeta)}</span>
        <span style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">Disminución neta del período</span>
      </div>
      <div class="niif-kpi-pill" style="border-color:var(--brand-gold);">
        <span class="kpi-title" style="color:var(--brand-gold);">Efectivo Final (Abril 2026)</span>
        <span class="kpi-amount" style="color:var(--brand-gold);">${fmtCOP(kpiEfectivoFin)}</span>
        <span style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">Disponible al cierre del balance</span>
      </div>
    </div>
  `;

  return `
    <div class="niif-statement-paper">
${renderCorporateHeaderBoxHtml("ESTADO DE FLUJOS DE EFECTIVO — MÉTODO INDIRECTO", `Período Contable: ${month} 2026`, "NIIF para las PYMES (Sección 7) • Cifras en Pesos Colombianos (COP) • Sumas Corridas")}

      ${kpiFlujoHtml}

      <!-- PARTE 1: ESTADO OFICIAL NIIF -->
      <div style="margin-bottom:28px;">
        <div style="background:var(--brand-primary); color:#FFFFFF; padding:8px 14px; border-radius:4px 4px 0 0; font-weight:800; font-size:0.83rem; letter-spacing:0.4px;">
          📊 ESTADO OFICIAL DE FLUJO DE EFECTIVO (MÉTODO INDIRECTO NIIF)
        </div>
        <div class="table-wrap">
          <table class="niif-table niif-table-flujo">
            <thead>
              <tr>
                <th style="width:90px;">Código</th>
                <th>Concepto / Actividad NIIF</th>
                <th style="width:160px; text-align:right;">Efecto en Caja (COP)</th>
              </tr>
            </thead>
            <tbody>
              ${oficialTbody}
            </tbody>
          </table>
        </div>
      </div>

      <!-- PARTE 2: HOJA DE TRABAJO Y VARIACIONES DE BALANCE -->
      <div style="margin-bottom:20px;">
        <div style="background:#1e293b; color:#FFFFFF; padding:8px 14px; border-radius:4px 4px 0 0; font-weight:800; font-size:0.83rem; letter-spacing:0.4px;">
          📋 HOJA DE TRABAJO: VARIACIONES Y EFECTOS EN EL BALANCE GENERAL
        </div>
        <div class="table-wrap">
          <table class="niif-table niif-table-flujo">
            <thead>
              <tr>
                <th style="width:85px;">Código</th>
                <th>Cuenta / Rubro de Balance</th>
                <th style="width:140px; text-align:right;">Variación Período ($)</th>
                <th style="width:140px; text-align:right;">Efecto ($)</th>
              </tr>
            </thead>
            <tbody>
              ${varTbody}
            </tbody>
          </table>
        </div>
      </div>

      ${renderOfficialSignaturesBlock()}
    </div>
  `;
}

function renderExcelGridHtml(rowsIn, sheetTitle) {
  const rawRows = (Array.isArray(rowsIn) ? rowsIn : []).map(getRowCells);
  if (!rawRows.length) return `<p style="color:var(--text-muted);">Sin filas en esta hoja.</p>`;

  let lastNonEmptyRow = rawRows.length - 1;
  while (lastNonEmptyRow >= 0 && rawRows[lastNonEmptyRow].every(c => c === null || c === undefined || String(c).trim() === "")) {
    lastNonEmptyRow--;
  }
  const allRows = rawRows.slice(0, lastNonEmptyRow + 1);
  if (!allRows.length) return `<p style="color:var(--text-muted);">Hoja vacía.</p>`;

  // Extract metadata / title in the first 4 rows
  let docTitle = sheetTitle || "INFORME CONTABLE OFICIAL";
  let docPeriod = `Período: ${ACTIVE_PERIOD} 2026`;
  let startDataRow = 0;

  for (let i = 0; i < Math.min(5, allRows.length); i++) {
    const rTexts = allRows[i].filter(c => c !== null && String(c).trim() !== "").map(c => String(c).trim());
    const rowStr = rTexts.join(" ").toUpperCase();
    if (rowStr.includes("ESTADO") || rowStr.includes("BORRADOR") || rowStr.includes("HOJA DE TRABAJO") || rowStr.includes("LIBRO") || rowStr.includes("PATRIMONIO") || rowStr.includes("FLUJO")) {
      const cand = rTexts.find(t => t.toUpperCase().includes("ESTADO") || t.toUpperCase().includes("BORRADOR") || t.toUpperCase().includes("HOJA") || t.toUpperCase().includes("LIBRO"));
      if (cand) docTitle = cand.replace(/^BORRADOR\s+(DE\s+)?/i, "").trim().toUpperCase();
      startDataRow = i + 1;
    } else if (rowStr.includes("PERIODO") || rowStr.includes("FEBRERO") || rowStr.includes("MARZO") || rowStr.includes("ABRIL") || rowStr.includes("ENERO")) {
      const pCand = rTexts.find(t => t.toUpperCase().includes("PERIODO") || t.toUpperCase().includes("1 DE") || t.toUpperCase().includes("DEL "));
      if (pCand) docPeriod = pCand;
      startDataRow = Math.max(startDataRow, i + 1);
    } else if (rowStr.includes("ELECTROVIVIENDA") || rowStr.includes("NIT")) {
      startDataRow = Math.max(startDataRow, i + 1);
    }
  }

  let headerRowIdx = startDataRow;
  for (let i = startDataRow; i < Math.min(startDataRow + 3, allRows.length); i++) {
    const txt = allRows[i].filter(c => c !== null).join(" ").toUpperCase();
    if (txt.includes("CONCEPTO") || txt.includes("CUENTA") || txt.includes("CÓDIGO") || txt.includes("CODIGO") || txt.includes("SALDO") || txt.includes("DETALLE")) {
      headerRowIdx = i;
      break;
    }
  }

  let firstNonEmptyCol = 99;
  for (let r = headerRowIdx; r < allRows.length; r++) {
    for (let c = 0; c < allRows[r].length; c++) {
      const v = allRows[r][c];
      if (v !== null && v !== undefined && String(v).trim() !== "") {
        if (c < firstNonEmptyCol) firstNonEmptyCol = c;
      }
    }
  }
  if (firstNonEmptyCol === 99) firstNonEmptyCol = 0;

  const dataRows = allRows.slice(headerRowIdx);
  const maxCols = Math.min(18, Math.max(...dataRows.map(r => r.length), 1));

  let theadHtml = "";
  let tbodyHtml = "";

  dataRows.forEach((r, idx) => {
    const cells = [];
    for (let c = firstNonEmptyCol; c < maxCols; c++) {
      const v = r[c];
      let disp = "";
      let cls = "";
      if (typeof v === "number") {
        disp = Math.abs(v) > 999 ? fmtCOP(v) : fmtNum(v, 2);
        cls = "num-col";
      } else if (v !== null && v !== undefined && String(v).trim() !== "") {
        disp = String(v);
        if (/^\d{4}$/.test(disp.trim())) {
          disp = `<span class="niif-code-pill">${disp.trim()}</span>`;
          cls = "code-col";
        }
      }
      cells.push({ val: disp, cls });
    }

    const rowText = r.map(x => x == null ? "" : String(x)).join(" ").toUpperCase();
    const isTotalRow = rowText.includes("TOTAL") || rowText.includes("SUMAS IGUALES") || rowText.includes("RESULTADO");
    const isSubtotalRow = rowText.includes("SUBTOTAL");
    const isClassRow = ["ACTIVOS", "PASIVOS", "PATRIMONIO", "INGRESOS", "COSTOS", "GASTOS"].some(w => rowText.includes(w) && !isTotalRow && !isSubtotalRow && r.filter(c => c !== null).length <= 3);

    if (idx === 0) {
      theadHtml = `
        <thead>
          <tr>
            ${cells.map(c => `<th>${c.val || ""}</th>`).join("")}
          </tr>
        </thead>
      `;
    } else {
      let trCls = "niif-row-cuenta";
      if (isTotalRow) {
        trCls = "niif-row-total";
      } else if (isSubtotalRow) {
        trCls = "niif-row-subtotal";
      } else if (isClassRow) {
        trCls = "niif-row-clase";
      }
      tbodyHtml += `
        <tr class="${trCls}">
          ${cells.map(c => `<td class="${c.cls}">${c.val}</td>`).join("")}
        </tr>
      `;
    }
  });

  const emp = DB?.empresa || {};

  return `
    <div class="niif-statement-paper">
      <div class="niif-header-box">
        <div class="niif-company-title">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
        <div class="niif-company-sub">NIT: ${emp.nit || "901.765.438-3"} • ${emp.regimen || "RRI — Agente Autorretenedor de Renta"}</div>
        <div class="niif-statement-badge">
          <div class="niif-statement-name">${docTitle}</div>
          <span class="niif-period-tag">${docPeriod}</span>
          <span style="font-size:0.7rem; color:#94A3B8; display:block; margin-top:3px;">Cifras en Pesos Colombianos (COP) • NIIF para las PYMES</span>
        </div>
      </div>

      <div class="table-wrap">
        <table class="niif-table niif-table-consolidado">
          ${theadHtml}
          <tbody>
            ${tbodyHtml}
          </tbody>
        </table>
      </div>

      ${renderOfficialSignaturesBlock()}
    </div>
  `;
}

let ACTIVE_DYNAMIC_EF_SUBVIEW = "ESF";

function setDynamicEfSubView(view) {
  ACTIVE_DYNAMIC_EF_SUBVIEW = view;
  renderEstadosFinancieros();
}


// ============================================================================
// 7.B. MÓDULO DE ANÁLISIS FINANCIERO Y GRÁFICAS INTERACTIVAS NIIF
// ============================================================================
let ACTIVE_CHARTS_INSTANCES = [];

function renderFinancialAnalysisDashboardHtml(period) {
  const emp = DB?.empresa || {};

  return `
    <div class="niif-statement-paper">
${renderCorporateHeaderBoxHtml("📊 INFORME INTEGRAL DE ANÁLISIS FINANCIERO DE LOS 4 PERÍODOS CONSOLIDADOS", "Evaluación Detallada: ENERO, FEBRERO, MARZO Y ABRIL 2026", "Diagnóstico Didáctico NIIF para las PYMES • Explicación Paso a Paso para No Contadores")}

      <!-- INTRODUCCIÓN PEDAGÓGICA PARA PERSONAS QUE NO SABEN CONTABILIDAD -->
      <div style="background:#F0FDF4; border:1.5px solid #10B981; border-left:6px solid #059669; border-radius:10px; padding:18px 20px; margin-bottom:24px; line-height:1.6; font-size:0.84rem; color:#1E293B;">
        <div style="font-size:1.02rem; font-weight:900; color:#065F46; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
          <span>💡 ¿CÓMO ENTENDER ESTE INFORME SI NO SABES DE CONTABILIDAD? (EXPLICACIÓN CON MANZANAS)</span>
        </div>
        <p style="margin:0 0 10px 0;">
          Para entender la salud financiera de <strong>ELECTROVIVIENDA S.A.S</strong> sin enredarte con términos técnicos, imagínala como la economía de una casa o un bolsillo familiar:
        </p>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:12px; margin-top:8px;">
          <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:8px; padding:12px;">
            <strong style="color:#0B192C; display:block; margin-bottom:4px; font-size:0.86rem;">1. EL ACTIVO (Lo que la empresa TIENE):</strong>
            <span>Es todo el dinero en bancos ($46M), la mercancía lista para vender en bodega (neveras Mabe, lavadoras y televisores LG por $33M), más el local, camionetas de reparto y computadores ($210M). En total, hoy la empresa tiene cosas valoradas en <strong>$331,2 millones</strong>.</span>
          </div>
          <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:8px; padding:12px;">
            <strong style="color:#DC2626; display:block; margin-bottom:4px; font-size:0.86rem;">2. EL PASIVO (Lo que la empresa DEBE):</strong>
            <span>Son los compromisos con terceros: el préstamo bancario con Bancolombia ($36M a largo plazo) y las cuentas de proveedores por pagar el próximo mes ($53M). En total debe <strong>$90,6 millones</strong>.</span>
          </div>
          <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:8px; padding:12px;">
            <strong style="color:#D4AF37; display:block; margin-bottom:4px; font-size:0.86rem;">3. EL PATRIMONIO (Lo que es de los DUEÑOS):</strong>
            <span>Es la resta limpia entre lo que tenemos y lo que debemos. Si hoy vendiéramos todo y pagáramos todas las deudas, a los socios fundadores (Gina Villamizar y asociados) les quedarían limpios en el bolsillo <strong>$240,5 millones</strong>.</span>
          </div>
        </div>
      </div>

      <!-- Tarjetas KPI de Alto Impacto (4 Períodos) -->
      <div class="niif-kpi-summary-strip" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:14px; margin-bottom:24px;">
        <div class="niif-kpi-pill" style="border-left:4px solid #10B981; background:#FFFFFF;">
          <span class="kpi-title">Razón Corriente (Liquidez)</span>
          <span class="kpi-amount" style="color:#059669;">2,25 x</span>
          <span style="font-size:0.74rem; color:#475569; margin-top:3px; line-height:1.35;">Por cada $1 que debemos a corto plazo, tenemos <strong>$2,25 en caja</strong> para pagar inmediatamente. ¡Excelente respaldo!</span>
        </div>
        <div class="niif-kpi-pill" style="border-left:4px solid #3B82F6; background:#FFFFFF;">
          <span class="kpi-title">Endeudamiento Total</span>
          <span class="kpi-amount" style="color:#2563EB;">27,37 %</span>
          <span style="font-size:0.74rem; color:#475569; margin-top:3px; line-height:1.35;">Solo el 27,3% de la empresa es deuda. El <strong>72,6% restante es 100% de los socios</strong>. Muy bajo riesgo.</span>
        </div>
        <div class="niif-kpi-pill" style="border-left:4px solid #D4AF37; background:#FFFFFF;">
          <span class="kpi-title">Margen Bruto Comercial</span>
          <span class="kpi-amount" style="color:var(--brand-gold);">59,69 %</span>
          <span style="font-size:0.74rem; color:#475569; margin-top:3px; line-height:1.35;">Por cada $100 que vendemos en Abril, ganamos <strong>$59,69 limpios</strong> antes de pagar sueldos y local.</span>
        </div>
        <div class="niif-kpi-pill" style="border-left:4px solid #8B5CF6; background:#FFFFFF;">
          <span class="kpi-title">Capital de Trabajo Neto</span>
          <span class="kpi-amount" style="color:#7C3AED;">$ 67.415.103</span>
          <span style="font-size:0.74rem; color:#475569; margin-top:3px; line-height:1.35;">Dinero disponible libre de deudas para seguir comprando electrodomésticos y operando sin asfixia.</span>
        </div>
      </div>

      <!-- SECCIÓN 1: PANEL DE GRÁFICAS Y EXPLICACIÓN DETALLADA PARA NO CONTADORES -->
      <div style="background:var(--brand-primary); color:#FFFFFF; padding:10px 16px; border-radius:6px 6px 0 0; font-weight:800; font-size:0.88rem; letter-spacing:0.4px; margin-bottom:16px;">
        📈 PANEL VISUAL: EXPLICACIÓN DETALLADA DE CADA GRÁFICA DEL SISTEMA
      </div>

      <div class="analysis-grid-2col" style="gap:20px;">
        <!-- Gráfica 1: Estructura Financiera 4 Periodos -->
        <div class="chart-card-box" style="padding:16px;">
          <div class="chart-card-header">
            <span class="chart-card-title">🏛️ Gráfica 1: Evolución de Activo, Pasivo y Patrimonio (4 Períodos)</span>
            <span class="ratio-badge-pill status-good"><span class="indicator-traffic-light green"></span>Solvente</span>
          </div>
          <div class="chart-canvas-container" style="height:270px;">
            <canvas id="chartEstructuraFinanciera"></canvas>
          </div>
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:12px; margin-top:12px; font-size:0.76rem; color:#334155; line-height:1.5;">
            <strong style="color:var(--brand-primary); font-size:0.8rem; display:block; margin-bottom:4px;">🔍 ¿Qué significa esta gráfica en la vida real?</strong>
            <p style="margin:0 0 6px 0;">• <strong>Barra Azul Oscura (Activo / Todo lo que tenemos):</strong> En enero arrancó en $247M (los aportes iniciales). En febrero creció a $385M porque nos endeudamos con el banco y los proveedores para llenar el almacén de televisores y neveras. En abril baja a $331M porque usamos plata para pagar esas deudas.</p>
            <p style="margin:0 0 6px 0;">• <strong>Barra Roja (Pasivo / Lo que debemos):</strong> En enero no debíamos nada ($0). En febrero y marzo subió a $120M por el préstamo de Bancolombia y compras a crédito. <strong>Fíjate en Abril:</strong> la barra roja se encoge a $90M porque pagamos casi $30 millones en deudas.</p>
            <p style="margin:0;">• <strong>Barra Dorada (Patrimonio / Plata de los socios):</strong> Se ha mantenido súper fuerte y estable alrededor de los $240 - $265 millones en los 4 meses. Esto garantiza que la empresa no depende de bancos para sobrevivir.</p>
          </div>
        </div>

        <!-- Gráfica 2: Composición Fuentes de Financiación -->
        <div class="chart-card-box" style="padding:16px;">
          <div class="chart-card-header">
            <span class="chart-card-title">⚖️ Gráfica 2: Fuentes de Financiación (¿De quién es la plata al cierre de Abril?)</span>
            <span class="ratio-badge-pill status-good"><span class="indicator-traffic-light green"></span>Bajo Riesgo</span>
          </div>
          <div class="chart-canvas-container" style="height:270px;">
            <canvas id="chartComposicionFinanciacion"></canvas>
          </div>
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:12px; margin-top:12px; font-size:0.76rem; color:#334155; line-height:1.5;">
            <strong style="color:var(--brand-primary); font-size:0.8rem; display:block; margin-bottom:4px;">🔍 ¿Qué significa esta gráfica en la vida real?</strong>
            <p style="margin:0 0 6px 0;">Esta dona responde a una pregunta clave: <em>Si vendiéramos todos los bienes de la empresa hoy, ¿quién se quedaría con el dinero?</em></p>
            <p style="margin:0 0 6px 0;">• <strong>Porción Verde (72,6% - Patrimonio Neto):</strong> Es la porción gigante. Casi tres cuartas partes del negocio le pertenecen a los socios. Nadie nos puede quitar la empresa porque no estamos hipotecados ni ahogados.</p>
            <p style="margin:0 0 6px 0;">• <strong>Porción Naranja (11,1% - Préstamo Bancolombia a Largo Plazo):</strong> Son $36,7M de deuda que se van pagando cómodamente mes a mes a varios años sin estrés de liquidez.</p>
            <p style="margin:0;">• <strong>Porción Roja (16,3% - Deudas de Corto Plazo):</strong> Son $53,9M de facturas corrientes a proveedores y la nómina próxima, totalmente respaldadas por el dinero en bancos y el inventario.</p>
          </div>
        </div>

        <!-- Gráfica 3: Desempeño Operacional y Resultados -->
        <div class="chart-card-box" style="padding:16px;">
          <div class="chart-card-header">
            <span class="chart-card-title">📊 Gráfica 3: Ventas Netas, Costos de Compra y Ganancias/Pérdidas (4 Meses)</span>
            <span class="ratio-badge-pill status-warn"><span class="indicator-traffic-light yellow"></span>Comercial</span>
          </div>
          <div class="chart-canvas-container" style="height:270px;">
            <canvas id="chartCascadaResultados"></canvas>
          </div>
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:12px; margin-top:12px; font-size:0.76rem; color:#334155; line-height:1.5;">
            <strong style="color:var(--brand-primary); font-size:0.8rem; display:block; margin-bottom:4px;">🔍 ¿Qué significa esta gráfica en la vida real?</strong>
            <p style="margin:0 0 6px 0;">• <strong>Barra Verde (Ventas):</strong> En Febrero rompimos el mercado vendiendo <strong>$185,9 millones</strong>. En Marzo no se facturó porque fue mes de inventario y papeles. En Abril reactivamos con <strong>$8,15 millones</strong>.</p>
            <p style="margin:0 0 6px 0;">• <strong>Barra Naranja (Costo de Mercancía):</strong> Lo que nos costó comprarle esos productos a los mayoristas ($126,3M en febrero y solo $3,28M en abril).</p>
            <p style="margin:0;">• <strong>Barra Azul / Roja (Ganancia o Pérdida):</strong> En Febrero ganamos <strong>+$16,4 millones limpios</strong> (barra azul). En Marzo y Abril hay números rojos (-$17,1M y -$7,8M) porque pagamos la nómina fija ($10,4M) vendiéramos o no. <strong>Fíjate en lo bueno:</strong> la pérdida de Abril es la mitad de la de Marzo; estamos a un paso de volver a ganar dinero en Mayo.</p>
          </div>
        </div>

        <!-- Gráfica 4: Evolución de Indicadores de Liquidez y Deuda -->
        <div class="chart-card-box" style="padding:16px;">
          <div class="chart-card-header">
            <span class="chart-card-title">💧 Gráfica 4: Curva de Liquidez (Disponibilidad de Plata) vs Deuda (%)</span>
            <span class="ratio-badge-pill status-good"><span class="indicator-traffic-light green"></span>2,25x</span>
          </div>
          <div class="chart-canvas-container" style="height:270px;">
            <canvas id="chartFlujoEfectivo"></canvas>
          </div>
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:12px; margin-top:12px; font-size:0.76rem; color:#334155; line-height:1.5;">
            <strong style="color:var(--brand-primary); font-size:0.8rem; display:block; margin-bottom:4px;">🔍 ¿Qué significa esta gráfica en la vida real?</strong>
            <p style="margin:0 0 6px 0;">• <strong>Línea Verde (Razón Corriente - Plata en Mano):</strong> Mide cuántos pesos tiene la empresa por cada peso de deuda inmediata. Arrancó en 2,15x en febrero, bajó a 1,92x en marzo porque pagamos impuestos a la DIAN, y <strong>en abril se disparó a 2,25 veces</strong>. Es el mejor momento de liquidez de todo el año: tenemos más del doble del dinero necesario para responder.</p>
            <p style="margin:0;">• <strong>Línea Azul (Endeudamiento Total):</strong> Cayó en picada de 32,68% a <strong>27,37%</strong> en Abril. Menos deuda significa menos intereses y mayor tranquilidad para la gerencia.</p>
          </div>
        </div>
      </div>

      <!-- SECCIÓN 2: MATRIZ INTEGRAL DE INDICADORES FINANCIEROS (LOS 4 PERIODOS) -->
      <div style="background:var(--brand-primary); color:#FFFFFF; padding:10px 16px; border-radius:6px 6px 0 0; font-weight:800; font-size:0.88rem; letter-spacing:0.4px; margin-top:28px; margin-bottom:0;">
        📑 TABLA COMPLETA: INDICADORES FINANCIEROS Y SU SIGNIFICADO EN PALABRAS SIMPLES
      </div>

      <div class="niif-table-responsive-box" style="margin-bottom:24px;">
        <table class="niif-official-table">
          <thead>
            <tr>
              <th style="width:14%;">Grupo / Categoría</th>
              <th style="width:16%;">Indicador Financiero</th>
              <th style="width:20%;">¿Qué mide en la vida real?</th>
              <th class="num-col" style="width:10%;">Enero</th>
              <th class="num-col" style="width:10%;">Febrero</th>
              <th class="num-col" style="width:10%;">Marzo</th>
              <th class="num-col" style="width:10%;">Abril</th>
              <th style="width:10%; text-align:center;">Diagnóstico</th>
            </tr>
          </thead>
          <tbody>
            <tr class="niif-row-clase">
              <td colspan="8">1. INDICADORES DE LIQUIDEZ (¿HAY PLATA SUFICIENTE EN EL BOLSILLO PARA PAGAR LAS CUENTAS?)</td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Liquidez</strong></td>
              <td><strong>Razón Corriente</strong></td>
              <td>Pesos de respaldo por cada $1 que debemos ya</td>
              <td class="num-col">Sin deudas</td>
              <td class="num-col">2,15 veces</td>
              <td class="num-col">1,92 veces</td>
              <td class="num-col" style="color:#059669; font-weight:900;">2,25 veces</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Excelente</span></td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Liquidez</strong></td>
              <td><strong>Prueba Ácida</strong></td>
              <td>Si no vendemos nada, cuánto respaldo líquido nos queda</td>
              <td class="num-col">N/A</td>
              <td class="num-col">1,38 veces</td>
              <td class="num-col">1,14 veces</td>
              <td class="num-col" style="font-weight:800;">1,45 veces</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Sobrado</span></td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Liquidez</strong></td>
              <td><strong>Capital de Trabajo Neto</strong></td>
              <td>Plata libre para trabajar tras restar deudas de corto plazo</td>
              <td class="num-col">$ 36.000.000</td>
              <td class="num-col">$ 92.815.595</td>
              <td class="num-col">$ 75.489.713</td>
              <td class="num-col" style="font-weight:800;">$ 67.415.103</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Muy Solvente</span></td>
            </tr>

            <tr class="niif-row-clase">
              <td colspan="8">2. INDICADORES DE DEUDA (¿QUÉ TANTO LE DEBEMOS A TERCEROS?)</td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Endeudamiento</strong></td>
              <td><strong>Nivel de Deuda Total</strong></td>
              <td>Porcentaje de la empresa que está comprometido en deudas</td>
              <td class="num-col">0,00 %</td>
              <td class="num-col">31,17 %</td>
              <td class="num-col">32,68 %</td>
              <td class="num-col" style="color:#2563EB; font-weight:900;">27,37 %</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Saneado</span></td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Endeudamiento</strong></td>
              <td><strong>Apalancamiento (Leverage)</strong></td>
              <td>Proporción entre la plata prestada y la plata de los socios</td>
              <td class="num-col">0,00 x</td>
              <td class="num-col">0,45 x</td>
              <td class="num-col">0,49 x</td>
              <td class="num-col" style="font-weight:800;">0,38 x</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Muy Seguro</span></td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Endeudamiento</strong></td>
              <td><strong>Concentración de Deuda Inmediata</strong></td>
              <td>De lo que debemos, cuánto vence en menos de 1 año</td>
              <td class="num-col">0,00 %</td>
              <td class="num-col">67,03 %</td>
              <td class="num-col">68,32 %</td>
              <td class="num-col" style="font-weight:800;">59,48 %</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Mejoró 8.8%</span></td>
            </tr>

            <tr class="niif-row-clase">
              <td colspan="8">3. INDICADORES DE RENTABILIDAD Y VENTAS (¿ESTAMOS GANANDO DINERO?)</td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Rentabilidad</strong></td>
              <td><strong>Margen Bruto de Ganancia</strong></td>
              <td>De cada $100 vendidos, cuánto nos queda antes de gastos fijos</td>
              <td class="num-col">N/A</td>
              <td class="num-col">32,07 %</td>
              <td class="num-col">N/A</td>
              <td class="num-col" style="color:var(--brand-gold); font-weight:900;">59,69 %</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Margen Altísimo</span></td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Rentabilidad</strong></td>
              <td><strong>Resultado Neto del Mes</strong></td>
              <td>Ganancia (+) o Pérdida (-) final que entra al bolsillo</td>
              <td class="num-col">$ 0</td>
              <td class="num-col" style="color:#059669; font-weight:800;">+$ 16.446.082</td>
              <td class="num-col text-danger">-$ 17.154.577</td>
              <td class="num-col text-danger" style="font-weight:800;">-$ 7.887.158</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-warn">🟡 Recuperándose</span></td>
            </tr>
            <tr class="niif-row-cuenta">
              <td><strong>Rentabilidad</strong></td>
              <td><strong>Rendimiento del Patrimonio (ROE)</strong></td>
              <td>Qué porcentaje de ganancia genera el capital de los socios</td>
              <td class="num-col">0,00 %</td>
              <td class="num-col" style="color:#059669;">+ 6,19 %</td>
              <td class="num-col text-danger">- 6,90 %</td>
              <td class="num-col text-danger" style="font-weight:800;">- 3,28 %</td>
              <td style="text-align:center;"><span class="ratio-badge-pill status-good">🟢 Redujo Pérdida 52%</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- SECCIÓN 3: DIAGNÓSTICO FINANCIERO Y CONCLUSIONES ESTRATÉGICAS EN PALABRAS SENCILLAS -->
      <div style="background:#F8FAFC; border:1px solid #CBD5E1; border-left:5px solid var(--brand-gold); border-radius:8px; padding:20px 22px; margin-bottom:24px; line-height:1.7; font-size:0.85rem; color:#1E293B;">
        <div style="font-size:1.02rem; font-weight:900; color:var(--brand-primary); margin-bottom:12px; display:flex; align-items:center; gap:8px;">
          <span>🎯 CONCLUSIONES Y DICTAMEN FINAL EN PALABRAS CLARAS (PARA LA GERENCIA Y SOCIOS):</span>
        </div>
        
        <div style="margin-bottom:12px;">
          <strong style="color:var(--brand-primary); font-size:0.9rem;">1. ¿La empresa está en peligro o en quiebra?</strong><br>
          <span><strong>De ninguna manera.</strong> ELECTROVIVIENDA S.A.S es una empresa con una salud financiera y solvencia envidiables. Las pérdidas de marzo y abril son pérdidas normales de cualquier negocio que está arrancando (se tuvieron que pagar nóminas, arriendos e impuestos mientras se organizaban los pedidos). Los $240 millones de patrimonio propio protegen a la empresa como un escudo de acero.</span>
        </div>

        <div style="margin-bottom:12px;">
          <strong style="color:#059669; font-size:0.9rem;">2. El Gran Triunfo de Abril: Desendeudarse sin ahogarse</strong><br>
          <span>La mejor decisión de la gerencia en abril fue pagar deudas. Se amortizaron <strong>casi $30 millones de pasivos</strong>. Como resultado, hoy la empresa solo debe el 27,3% de lo que tiene, y por cada peso de deuda a corto plazo tiene <strong>$2,25 en caja y bienes líquidos</strong>. Pocas empresas nuevas en Colombia alcanzan una liquidez tan alta en sus primeros 4 meses.</span>
        </div>

        <div style="margin-bottom:12px;">
          <strong style="color:var(--brand-gold); font-size:0.9rem;">3. El Producto es un Éxito Comercial (Margen del 59,7%)</strong><br>
          <span>El electrodoméstico que vende ELECTROVIVIENDA no se está vendiendo a pérdida ni rematado. Por cada $100 pesos que entran por venta en abril, quedan casi $60 de ganancia comercial. Esto demuestra que los clientes en Santander aceptan los precios y que el modelo de negocio es altamente rentable.</span>
        </div>

        <div>
          <strong style="color:#2563EB; font-size:0.9rem;">4. La Receta para Ganar Mucho Dinero en Mayo 2026:</strong><br>
          <span>La empresa necesita vender exactamente <strong>$22.000.000 al mes</strong> para que las ganancias brutas cubran el 100% de los sueldos y gastos fijos (Punto de Equilibrio). Como ya se tienen las neveras y televisores guardados en bodega en el kardex, la meta de mayo es sencilla: <strong>salir a vender ese inventario que ya está pagado</strong>. Toda venta que se haga entrará prácticamente como ganancia neta.</span>
        </div>
      </div>

      ${renderOfficialSignaturesBlock()}
    </div>
  `;
}
function initFinancialAnalysisCharts(period) {
  ACTIVE_CHARTS_INSTANCES.forEach(ch => {
    try { ch.destroy(); } catch (e) {}
  });
  ACTIVE_CHARTS_INSTANCES = [];

  if (typeof Chart === "undefined") {
    console.warn("Chart.js no está disponible aún.");
    return;
  }

  // 1. Gráfica de Estructura Financiera de los 4 Períodos (Enero, Febrero, Marzo, Abril)
  const ctx1 = document.getElementById("chartEstructuraFinanciera")?.getContext("2d");
  if (ctx1) {
    const ch1 = new Chart(ctx1, {
      type: "bar",
      data: {
        labels: ["Enero 2026", "Febrero 2026", "Marzo 2026", "Abril 2026"],
        datasets: [
          {
            label: "Activo Total ($M)",
            data: [247.33, 385.91, 369.07, 331.23],
            backgroundColor: "rgba(11, 25, 44, 0.85)",
            borderColor: "#0B192C",
            borderWidth: 1.5,
            borderRadius: 4
          },
          {
            label: "Pasivo Total ($M)",
            data: [0.00, 120.30, 120.62, 90.67],
            backgroundColor: "rgba(239, 68, 68, 0.85)",
            borderColor: "#EF4444",
            borderWidth: 1.5,
            borderRadius: 4
          },
          {
            label: "Patrimonio ($M)",
            data: [247.33, 265.60, 248.45, 240.56],
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
          legend: { position: "top", labels: { boxWidth: 12, font: { size: 10, weight: "bold" } } },
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

  // 2. Gráfica de Fuentes de Financiación (Cierre Abril 2026)
  const ctx2 = document.getElementById("chartComposicionFinanciacion")?.getContext("2d");
  if (ctx2) {
    const ch2 = new Chart(ctx2, {
      type: "doughnut",
      data: {
        labels: ["Pasivo Corriente (16,3%)", "Pasivo No Corriente (11,1%)", "Patrimonio Neto (72,6%)"],
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
        cutout: "55%",
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

  // 3. Ventas Netas, Costos y Utilidades (Enero a Abril)
  const ctx3 = document.getElementById("chartCascadaResultados")?.getContext("2d");
  if (ctx3) {
    const ch3 = new Chart(ctx3, {
      type: "bar",
      data: {
        labels: ["Enero 2026", "Febrero 2026", "Marzo 2026", "Abril 2026"],
        datasets: [
          {
            label: "Ventas Netas ($M)",
            data: [0.00, 185.95, 0.00, 8.16],
            backgroundColor: "rgba(16, 185, 129, 0.85)",
            borderColor: "#10B981",
            borderWidth: 1.2
          },
          {
            label: "Costo de Ventas ($M)",
            data: [0.00, 126.31, 0.00, 3.29],
            backgroundColor: "rgba(245, 158, 11, 0.85)",
            borderColor: "#F59E0B",
            borderWidth: 1.2
          },
          {
            label: "Resultado Neto ($M)",
            data: [0.00, 16.45, -17.15, -7.89],
            backgroundColor: (ctx) => {
              const val = ctx.raw;
              return val >= 0 ? "rgba(59, 130, 246, 0.85)" : "rgba(239, 68, 68, 0.85)";
            },
            borderWidth: 1.2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top", labels: { boxWidth: 10, font: { size: 10 } } },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.dataset.label}: $ ${ctx.parsed.y.toFixed(2)}M COP`
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

  // 4. Curva de Liquidez (Razón Corriente) vs Endeudamiento
  const ctx4 = document.getElementById("chartFlujoEfectivo")?.getContext("2d");
  if (ctx4) {
    const ch4 = new Chart(ctx4, {
      type: "line",
      data: {
        labels: ["Enero 2026", "Febrero 2026", "Marzo 2026", "Abril 2026"],
        datasets: [
          {
            label: "Razón Corriente (x)",
            data: [null, 2.15, 1.92, 2.25],
            borderColor: "#10B981",
            backgroundColor: "rgba(16, 185, 129, 0.15)",
            fill: false,
            tension: 0.3,
            yAxisID: "y"
          },
          {
            label: "Endeudamiento Total (%)",
            data: [0.0, 31.17, 32.68, 27.37],
            borderColor: "#3B82F6",
            backgroundColor: "rgba(59, 130, 246, 0.15)",
            fill: false,
            tension: 0.3,
            yAxisID: "y1"
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top", labels: { boxWidth: 12, font: { size: 10 } } }
        },
        scales: {
          y: {
            type: "linear",
            display: true,
            position: "left",
            title: { display: true, text: "Razón Corriente (veces)", font: { size: 10 } }
          },
          y1: {
            type: "linear",
            display: true,
            position: "right",
            grid: { drawOnChartArea: false },
            title: { display: true, text: "Endeudamiento (%)", font: { size: 10 } }
          }
        }
      }
    });
    ACTIVE_CHARTS_INSTANCES.push(ch4);
  }
}



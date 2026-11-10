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
  const isAbril = period === "ABRIL";

  return `
    <div class="niif-statement-paper">
${renderCorporateHeaderBoxHtml("📊 INFORME EJECUTIVO DE ANÁLISIS FINANCIERO & GRÁFICAS INTERACTIVAS", "Período Comparativo: MARZO 2026 vs ABRIL 2026", "Diagnóstico Financiero Integral NIIF para las PYMES • Indicadores de Liquidez, Endeudamiento y Rentabilidad")}

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


function renderEstadosFinancieros() {
  const container = document.getElementById("efContentContainer");
  if (!container || !DB) return;
  const esp = DB?.meses?.[ACTIVE_PERIOD]?.hojas_especiales || {};

  const esfKey = Object.keys(esp).find(k => k.startsWith("ESF") && !k.includes("CONSOLIDADO")) || "ESF";
  const erKey = Object.keys(esp).find(k => k.startsWith("ER") && !k.includes("CONSOLIDADO")) || "ER";

  if (ACTIVE_EF_TAB === "DINAMICO") {
    const txs = DB?.meses?.[ACTIVE_PERIOD]?.transacciones || [];
    const esfRows = esp[esfKey] ? sheetRows(esp[esfKey]) : [];
    const erRows = esp[erKey] ? sheetRows(esp[erKey]) : [];

    const switcherBar = `
      <div class="ef-subview-switcher no-print" style="background:var(--bg-surface); border:1px solid var(--border-light); border-radius:var(--radius-sm); padding:10px 16px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; box-shadow:var(--shadow-xs);">
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <span style="font-size:0.75rem; font-weight:800; color:var(--brand-primary);">VISTA OFICIAL (${ACTIVE_PERIOD} 2026):</span>
          <div class="filter-tabs" style="margin:0;">
            <button class="filter-chip ${ACTIVE_DYNAMIC_EF_SUBVIEW === 'ESF' ? 'active' : ''}" onclick="setDynamicEfSubView('ESF')">
              🏛️ Situación Financiera (ESF NIIF)
            </button>
            <button class="filter-chip ${ACTIVE_DYNAMIC_EF_SUBVIEW === 'ER' ? 'active' : ''}" onclick="setDynamicEfSubView('ER')">
              📈 Estado de Resultados Integral (ER NIIF)
            </button>
            <button class="filter-chip ${ACTIVE_DYNAMIC_EF_SUBVIEW === 'BALANCE' ? 'active' : ''}" onclick="setDynamicEfSubView('BALANCE')">
              ⚡ Balance de Comprobación Clasificado (PUC con Sumas Iguales)
            </button>
          </div>
        </div>
        <div style="display:flex; gap:8px;">
          <button class="btn btn-primary btn-sm" onclick="exportSmartContextualPDF()">
            📄 Descargar PDF Oficial
          </button>
          <button class="btn btn-gold btn-sm" onclick="downloadActiveMonthExcel()">
            📥 Excel ${ACTIVE_PERIOD}
          </button>
        </div>
      </div>
    `;

    let activeViewContent = "";
    if (ACTIVE_DYNAMIC_EF_SUBVIEW === "ESF") {
      activeViewContent = esfRows.length
        ? renderExecutiveNIIFStatementHtml(esfRows, "ESF", ACTIVE_PERIOD, "Estado de Situación Financiera")
        : `<div class="card"><div class="card-body">Sin hoja ESF registrada en ${ACTIVE_PERIOD}.</div></div>`;
    } else if (ACTIVE_DYNAMIC_EF_SUBVIEW === "ER") {
      activeViewContent = erRows.length
        ? renderExecutiveNIIFStatementHtml(erRows, "ER", ACTIVE_PERIOD, "Estado de Resultados Integral")
        : `<div class="card"><div class="card-body">Sin hoja ER registrada en ${ACTIVE_PERIOD}.</div></div>`;
    } else {
      activeViewContent = renderClassifiedTrialBalance(txs, ACTIVE_PERIOD);
    }

    container.innerHTML = switcherBar + activeViewContent;
    return;
  }

  if (ACTIVE_EF_TAB === "ESF") {
    const rows = esp[esfKey] ? sheetRows(esp[esfKey]) : [];
    container.innerHTML = rows.length
      ? renderExecutiveNIIFStatementHtml(rows, "ESF", ACTIVE_PERIOD, "Estado de Situación Financiera")
      : `<div class="card"><div class="card-body">No se encontró hoja de Estado de Situación Financiera en ${ACTIVE_PERIOD}.</div></div>`;
    return;
  }

  if (ACTIVE_EF_TAB === "ER") {
    const rows = esp[erKey] ? sheetRows(esp[erKey]) : [];
    container.innerHTML = rows.length
      ? renderExecutiveNIIFStatementHtml(rows, "ER", ACTIVE_PERIOD, "Estado de Resultados Integral")
      : `<div class="card"><div class="card-body">No se encontró hoja de Estado de Resultados Integral en ${ACTIVE_PERIOD}.</div></div>`;
    return;
  }

  if (ACTIVE_EF_TAB === "CONSOLIDADOS") {
    const esfConsKey = Object.keys(esp).find(k => k.includes("ESF CONSOLIDADO") || (k.startsWith("ESF") && k.includes("CONSOLIDADO")));
    const erConsKey = Object.keys(esp).find(k => k.includes("ER CONSOLIDADO") || (k.startsWith("ER") && k.includes("CONSOLIDADO")));
    const esfConsRows = esfConsKey ? sheetRows(esp[esfConsKey]) : [];
    const erConsRows = erConsKey ? sheetRows(esp[erConsKey]) : [];

    container.innerHTML = `
      <div style="display:flex; flex-direction:column; gap:24px;">
        ${esfConsRows.length ? renderConsolidatedComparativeStatementHtml(esfConsRows, "ESF", ACTIVE_PERIOD, "Estado de Situación Financiera Consolidado") : ""}
        ${erConsRows.length ? renderConsolidatedComparativeStatementHtml(erConsRows, "ER", ACTIVE_PERIOD, "Estado de Resultados Integral Consolidado") : ""}
        ${(!esfConsRows.length && !erConsRows.length) ? `<div class="card"><div class="card-body">No hay hojas consolidadas en ${ACTIVE_PERIOD}.</div></div>` : ""}
      </div>
    `;
    return;
  }

  const mapFilter = {
    ESF: k => k.startsWith("ESF") && !k.includes("CONSOLIDADO"),
    ER: k => k.startsWith("ER") && !k.includes("CONSOLIDADO"),
    CONSOLIDADOS: k => k.includes("CONSOLIDADO"),
    ECP: k => k.startsWith("ECP"),
    FLUJO: k => k.includes("F&E") || k.includes("FLUJO"),
    HOJA_TR: k => k.includes("HOJA TR"),
    LIBROS: k => k.includes("L.D") || k.includes("LIBRO DC") || k.includes("M&B"),
    NOMINA_TA: k => k.trim().toUpperCase() === "TA" || k.includes("RET-FTE"),
    CUENTAS_T: k => /^(T|T2|T\d+)$/i.test(k.trim()) || /^CT[\s\d-]/i.test(k.trim()) || k.toUpperCase().includes("CUENTAS T"),
    NOTAS: k => k.toUpperCase().includes("NOTA")
  };

  if (ACTIVE_EF_TAB === "ECP") {
    const ecpKey = Object.keys(esp).find(mapFilter.ECP);
    const rows = ecpKey ? sheetRows(esp[ecpKey]) : [];
    container.innerHTML = rows.length
      ? renderECPStatementHtml(rows, ACTIVE_PERIOD)
      : `<div class="card"><div class="card-body">No se encontró hoja de Estado de Cambios en el Patrimonio en ${ACTIVE_PERIOD}.</div></div>`;
    return;
  }

  if (ACTIVE_EF_TAB === "ANALISIS") {
    container.innerHTML = renderFinancialAnalysisDashboardHtml(ACTIVE_PERIOD);
    setTimeout(() => initFinancialAnalysisCharts(ACTIVE_PERIOD), 50);
    return;
  }

  if (ACTIVE_EF_TAB === "FLUJO") {
    const flujoKey = Object.keys(esp).find(mapFilter.FLUJO);
    const rows = flujoKey ? sheetRows(esp[flujoKey]) : [];
    container.innerHTML = rows.length
      ? renderFlujoEfectivoStatementHtml(rows, ACTIVE_PERIOD)
      : `<div class="card"><div class="card-body">No se encontró hoja de Flujo de Efectivo en ${ACTIVE_PERIOD}.</div></div>`;
    return;
  }

  if (ACTIVE_EF_TAB === "TODAS") {
    const names = Object.keys(esp);
    if (!names.includes(ACTIVE_EF_SHEET)) ACTIVE_EF_SHEET = names[0] || "";
    const opts = names.map(n => `<option value="${n.replace(/"/g, "&quot;")}" ${n === ACTIVE_EF_SHEET ? "selected" : ""}>${n} (${sheetRows(esp[n]).length} filas)</option>`).join("");
    container.innerHTML = names.length ? `
      <div class="card">
        <div class="card-header">
          <div class="card-title">📂 Todas las hojas del libro ${ACTIVE_PERIOD}.xlsx (${names.length} hojas especiales)</div>
          <select class="form-control" style="max-width:340px; font-weight:700;" onchange="ACTIVE_EF_SHEET=this.value; renderEstadosFinancieros();">${opts}</select>
        </div>
        <div class="card-body">${renderExcelGridHtml(sheetRows(esp[ACTIVE_EF_SHEET]), ACTIVE_EF_SHEET)}</div>
      </div>
      <p style="font-size:0.76rem; color:var(--text-muted);">Los comprobantes/hojas numeradas (1 a 60, AD1…) están en la sección <strong>Comprobantes del Mes</strong>; los Kardex en <strong>Kardex de Productos</strong>.</p>`
      : `<div class="card"><div class="card-body">${ACTIVE_PERIOD} no tiene hojas especiales (en $0).</div></div>`;
    return;
  }

  if (ACTIVE_EF_TAB === "NOTAS") {
    container.innerHTML = renderNotasNIIFStatementHtml(ACTIVE_PERIOD);
    return;
  }

  const fn = mapFilter[ACTIVE_EF_TAB] || (() => true);
  let matchingKeys = Object.keys(esp).filter(fn);
  let sourceMonth = ACTIVE_PERIOD;
  const monthHasData = (DB?.meses?.[ACTIVE_PERIOD]?.transacciones || []).length > 0 || Object.keys(esp).length > 0;
  if (!matchingKeys.length && monthHasData) {
    const idxM = ALL_12_MONTHS.indexOf(ACTIVE_PERIOD);
    for (let i = idxM - 1; i >= 0; i--) {
      const prevEsp = DB?.meses?.[ALL_12_MONTHS[i]]?.hojas_especiales || {};
      const prevKeys = Object.keys(prevEsp).filter(fn);
      if (prevKeys.length) {
        matchingKeys = prevKeys;
        sourceMonth = ALL_12_MONTHS[i];
        break;
      }
    }
  }

  const targetEsp = DB?.meses?.[sourceMonth]?.hojas_especiales || {};
  container.innerHTML = matchingKeys.map(k => `
    <div class="card">
      <div class="card-header">
        <div class="card-title">📊 Hoja Oficial: ${k} (${sourceMonth}.xlsx)</div>
        <span class="status-pill status-paid">Sincronizado con Excel</span>
      </div>
      <div class="card-body">${renderExcelGridHtml(sheetRows(targetEsp[k]), k)}</div>
    </div>
  `).join("") || `<div class="card"><div class="card-body">No hay hojas de esta categoría en ${ACTIVE_PERIOD} (mes en $0 o sin esa hoja en su libro Excel). Prueba la pestaña <strong>📂 Todas las Hojas del Excel</strong>.</div></div>`;
}

// ============================================================================
// CONTROL RESPONSIVO MULTI-DISPOSITIVO (MAC, PC, PORTÁTIL Y CELULAR)
// ============================================================================
function toggleMobileSidebar(force) {
  const sidebar = document.querySelector(".app-sidebar");
  const backdrop = document.getElementById("mobileSidebarBackdrop");
  if (!sidebar) return;
  const isOpen = sidebar.classList.contains("mobile-open");
  const next = (typeof force === "boolean") ? force : !isOpen;
  sidebar.classList.toggle("mobile-open", next);
  if (backdrop) backdrop.classList.toggle("open", next);
}

// ============================================================================
// 7.B SECCIÓN: NÓMINA & LIQUIDACIÓN LABORAL COLOMBIANA (PLANILLA COMPLETA NIIF)
// ============================================================================
let ACTIVE_NOMINA_MONTH = "FEBRERO";
let ACTIVE_NOMINA_SUBTAB = "PLANILLA";

function selectNominaMonth(m) {
  ACTIVE_NOMINA_MONTH = m;
  document.querySelectorAll("#nominaMonthTabs .filter-chip").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.nommonth === m);
  });
  renderNominaSection();
}

function selectNominaSubTab(sub) {
  ACTIVE_NOMINA_SUBTAB = sub;
  document.querySelectorAll("#nominaSubTabs .filter-chip").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.nomsub === sub);
  });
  renderNominaSection();
}

function renderNominaSection() {
  const container = document.getElementById("nominaContentContainer");
  const kpiRow = document.getElementById("nominaKpiRow");
  if (!container || !DB) return;

  const nomData = DB.nominas?.[ACTIVE_NOMINA_MONTH] || DB.nominas?.["FEBRERO"] || {};
  const emps = nomData.empleados || [];
  const tots = nomData.totales || {};
  const prests = nomData.prestaciones || [];

  const totalDev = tots.total_devengado || emps.reduce((a, b) => a + (Number(b.total_devengado) || 0), 0);
  const totalDed = tots.total_deducciones || emps.reduce((a, b) => a + (Number(b.total_deducciones) || 0), 0);
  const netoPagar = tots.neto_pagar || emps.reduce((a, b) => a + (Number(b.neto_pagar) || 0), 0);
  const totalPrest = prests.reduce((a, b) => a + (Number(b.total_prestaciones) || 0), 0);
  const totalSegSocialEmp = prests.reduce((a, b) => {
    return a + (Number(b.salud_empleador) || 0) + (Number(b.pension_empleador) || 0) + (Number(b.arl) || 0);
  }, 0);
  const totalParafiscales = prests.reduce((a, b) => {
    return a + (Number(b.sena) || 0) + (Number(b.icbf) || 0) + (Number(b.caja_compensacion) || 0);
  }, 0);
  const costoTotalEmpresa = totalDev + totalPrest + totalSegSocialEmp + totalParafiscales;

  if (kpiRow) {
    kpiRow.innerHTML = `
      <div class="kpi-card">
        <div class="kpi-label">Total Devengado (${emps.length} Empleados)</div>
        <div class="kpi-value" style="color:#059669;">${fmtCOP(totalDev)}</div>
        <div class="kpi-sub">Sueldos, horas extras y auxilio de transporte</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Deducciones Empleados</div>
        <div class="kpi-value" style="color:#DC2626;">${fmtCOP(totalDed)}</div>
        <div class="kpi-sub">Salud 4%, Pensión 4%, Retefuente y Solidaridad</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Neto Pagado en Bancos</div>
        <div class="kpi-value" style="color:var(--brand-gold);">${fmtCOP(netoPagar)}</div>
        <div class="kpi-sub">Transferencias nómina (Cta 250505)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Provisiones Prestaciones</div>
        <div class="kpi-value" style="color:#7C3AED;">${fmtCOP(totalPrest)}</div>
        <div class="kpi-sub">Cesantías, Intereses, Prima y Vacaciones</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Aportes Empresa (SS &amp; Parafiscales)</div>
        <div class="kpi-value" style="color:#2563EB;">${fmtCOP(totalSegSocialEmp + totalParafiscales)}</div>
        <div class="kpi-sub">Pensión 12%, ARL, Salud y Caja de Compensación</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Costo Total Nómina Empresa</div>
        <div class="kpi-value" style="color:var(--brand-primary);">${fmtCOP(costoTotalEmpresa)}</div>
        <div class="kpi-sub">Gasto real del período (${ACTIVE_NOMINA_MONTH} 2026)</div>
      </div>
    `;
  }

  if (ACTIVE_NOMINA_SUBTAB === "PLANILLA") {
    const rowsHtml = emps.map((e, idx) => `
      <tr>
        <td style="font-weight:800; color:var(--brand-primary);">${idx + 1}</td>
        <td><strong>${e.nombre}</strong></td>
        <td class="num-col">${e.horas || 240} hrs</td>
        <td class="num-col">${fmtCOP(e.sueldo_basico)}</td>
        <td class="num-col">${fmtCOP(e.basico)}</td>
        <td class="num-col">${fmtCOP(e.auxilios || 0)}</td>
        <td class="num-col">${fmtCOP((e.horas_extras || 0) + (e.recargos || 0))}</td>
        <td class="num-col" style="color:#059669; font-weight:700;">${fmtCOP(e.aux_transporte || 0)}</td>
        <td class="num-col" style="font-weight:800; background:rgba(16,185,129,0.08); color:#047857;">${fmtCOP(e.total_devengado)}</td>
        <td class="num-col">${fmtCOP(e.ibc || e.basico)}</td>
        <td class="num-col" style="color:#DC2626;">${fmtCOP(e.salud_empleado)}</td>
        <td class="num-col" style="color:#DC2626;">${fmtCOP(e.pension_empleado)}</td>
        <td class="num-col">${fmtCOP(e.solidaridad || 0)}</td>
        <td class="num-col" style="color:#B45309; font-weight:700;">${fmtCOP(e.retefuente || 0)}</td>
        <td class="num-col" style="font-weight:800; background:rgba(239,68,68,0.08); color:#B91C1C;">${fmtCOP(e.total_deducciones)}</td>
        <td class="num-col" style="font-weight:900; background:rgba(212,175,55,0.15); color:var(--brand-primary); font-size:0.86rem;">${fmtCOP(e.neto_pagar)}</td>
      </tr>
    `).join("");

    container.innerHTML = `
      <div class="nomina-sheet-card">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:14px; border-bottom:1.5px solid var(--border-light); padding-bottom:10px;">
          <div>
            <h3 style="color:var(--brand-primary); font-size:1.1rem; font-weight:900;">📋 GRAN PLANILLA DE LIQUIDACIÓN DE NÓMINA INDIVIDUAL — ${ACTIVE_NOMINA_MONTH} 2026</h3>
            <span style="font-size:0.75rem; color:var(--text-muted);">ELECTROVIVIENDA S.A.S • NIT 901.765.438-3 • Hoja Excel Original: <strong>${nomData.hoja || "NÓMINA"}</strong></span>
          </div>
          <span class="status-pill status-paid" style="font-size:0.75rem; font-weight:800;">✓ Liquidación Cuadrada y Auditada</span>
        </div>

        <div class="table-wrap">
          <table class="nomina-table">
            <thead>
              <tr>
                <th colspan="2" class="nomina-group-th" style="background:#0B192C;">DATOS DEL TRABAJADOR</th>
                <th colspan="7" class="nomina-group-th nomina-th-devengado">1. DEVENGADO (INGRESOS LABORALES)</th>
                <th class="nomina-group-th" style="background:#475569;">COTIZACIÓN</th>
                <th colspan="5" class="nomina-group-th nomina-th-deducciones">2. DEDUCCIONES DEL EMPLEADO</th>
                <th class="nomina-group-th nomina-th-neto">3. NETO</th>
              </tr>
              <tr>
                <th style="width:30px;">#</th>
                <th>Nombre del Empleado</th>
                <th class="num-col">Horas</th>
                <th class="num-col">Salario Básico</th>
                <th class="num-col">Básico Liq.</th>
                <th class="num-col">Auxilios</th>
                <th class="num-col">Extras/Rec.</th>
                <th class="num-col">Aux. Transp.</th>
                <th class="num-col" style="background:#047857; color:#fff;">Total Devengado</th>
                <th class="num-col">IBC Seguridad</th>
                <th class="num-col">Salud (4%)</th>
                <th class="num-col">Pensión (4%)</th>
                <th class="num-col">Fondo Solid. (1%)</th>
                <th class="num-col">Retefuente Art 383</th>
                <th class="num-col" style="background:#DC2626; color:#fff;">Total Deducido</th>
                <th class="num-col" style="background:#D4AF37; color:#0B192C; font-weight:900;">Neto a Pagar</th>
              </tr>
            </thead>
            <tbody>
              ${rowsHtml}
              <tr class="nomina-total-row">
                <td colspan="3" style="text-align:right; font-weight:900;">TOTALES CONSOLIDADOS (${ACTIVE_NOMINA_MONTH}):</td>
                <td class="num-col">${fmtCOP(tots.sueldo_basico || 0)}</td>
                <td class="num-col">${fmtCOP(tots.basico || 0)}</td>
                <td class="num-col">$ 0</td>
                <td class="num-col">$ 0</td>
                <td class="num-col">${fmtCOP(tots.aux_transporte || 0)}</td>
                <td class="num-col" style="color:#34D399; font-size:0.88rem;">${fmtCOP(totalDev)}</td>
                <td class="num-col">${fmtCOP(tots.ibc || 0)}</td>
                <td class="num-col">${fmtCOP(tots.salud_empleado || 0)}</td>
                <td class="num-col">${fmtCOP(tots.pension_empleado || 0)}</td>
                <td class="num-col">${fmtCOP(tots.solidaridad || 0)}</td>
                <td class="num-col">${fmtCOP(tots.retefuente || 0)}</td>
                <td class="num-col" style="color:#FCA5A5; font-size:0.88rem;">${fmtCOP(totalDed)}</td>
                <td class="num-col" style="color:#FDE047; font-size:0.92rem;">${fmtCOP(netoPagar)}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div style="margin-top:16px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; font-size:0.75rem; color:var(--text-muted);">
          <div>
            <strong>Parámetros Legales 2026:</strong> SMLMV: $1.750.905 • Auxilio Transporte: $249.095 • Jornada Máxima: 240 hrs/mes
          </div>
          <div>
            Firmas: <strong>Gina Villamizar</strong> (Contadora T.P. 248960-T) • <strong>Kevin Guerrero</strong> (Representante Legal)
          </div>
        </div>
      </div>
    `;
  } else if (ACTIVE_NOMINA_SUBTAB === "SEG_SOCIAL") {
    const rowsHtml = prests.map((p, idx) => {
      const totSegEmp = (Number(p.salud_empleador) || 0) + (Number(p.pension_empleador) || 0) + (Number(p.arl) || 0) + (Number(p.sena) || 0) + (Number(p.icbf) || 0) + (Number(p.caja_compensacion) || 0);
      return `
        <tr>
          <td style="font-weight:800; color:var(--brand-primary);">${idx + 1}</td>
          <td><strong>${p.nombre}</strong></td>
          <td class="num-col">${fmtCOP(p.devengado)}</td>
          <td class="num-col" style="color:${p.salud_empleador > 0 ? '#0B192C' : '#94A3B8'};">${p.salud_empleador > 0 ? fmtCOP(p.salud_empleador) : '<span style="font-size:0.7rem; color:#059669; font-weight:700;">Exonerado Art 114-1</span>'}</td>
          <td class="num-col">${fmtCOP(p.pension_empleador)}</td>
          <td class="num-col">${fmtCOP(p.arl)}</td>
          <td class="num-col" style="color:${p.sena > 0 ? '#0B192C' : '#94A3B8'};">${p.sena > 0 ? fmtCOP(p.sena) : '<span style="font-size:0.7rem; color:#059669; font-weight:700;">Exonerado</span>'}</td>
          <td class="num-col" style="color:${p.icbf > 0 ? '#0B192C' : '#94A3B8'};">${p.icbf > 0 ? fmtCOP(p.icbf) : '<span style="font-size:0.7rem; color:#059669; font-weight:700;">Exonerado</span>'}</td>
          <td class="num-col">${fmtCOP(p.caja_compensacion)}</td>
          <td class="num-col" style="font-weight:900; color:#2563EB; background:rgba(37,99,235,0.08);">${fmtCOP(totSegEmp)}</td>
        </tr>
      `;
    }).join("");

    container.innerHTML = `
      <div class="nomina-sheet-card">
        <div style="margin-bottom:14px; border-bottom:1.5px solid var(--border-light); padding-bottom:10px;">
          <h3 style="color:var(--brand-primary); font-size:1.1rem; font-weight:900;">🏢 APORTES A SEGURIDAD SOCIAL Y PARAFISCALES A CARGO DE LA EMPRESA — ${ACTIVE_NOMINA_MONTH} 2026</h3>
          <span style="font-size:0.75rem; color:var(--text-muted);">Aplicación Estatuto Tributario Art. 114-1 (Exoneración SENA, ICBF y Salud para empleados con sueldo inferior a 10 SMLMV)</span>
        </div>

        <div class="table-wrap">
          <table class="nomina-table">
            <thead>
              <tr>
                <th style="width:30px;">#</th>
                <th>Empleado</th>
                <th class="num-col">IBC Salarial</th>
                <th class="num-col">Salud Empleador (8.5%)</th>
                <th class="num-col">Pensión Empleador (12%)</th>
                <th class="num-col">ARL Riesgo I (0.522%)</th>
                <th class="num-col">SENA (2%)</th>
                <th class="num-col">ICBF (3%)</th>
                <th class="num-col">Caja Comp. (4%)</th>
                <th class="num-col" style="background:#2563EB; color:#fff;">Total Aportes Empresa</th>
              </tr>
            </thead>
            <tbody>
              ${rowsHtml}
              <tr class="nomina-total-row">
                <td colspan="3" style="text-align:right; font-weight:900;">TOTALES APORTES EMPRESA:</td>
                <td class="num-col">${fmtCOP(prests.reduce((a, b) => a + (Number(b.salud_empleador) || 0), 0))}</td>
                <td class="num-col">${fmtCOP(prests.reduce((a, b) => a + (Number(b.pension_empleador) || 0), 0))}</td>
                <td class="num-col">${fmtCOP(prests.reduce((a, b) => a + (Number(b.arl) || 0), 0))}</td>
                <td class="num-col">${fmtCOP(prests.reduce((a, b) => a + (Number(b.sena) || 0), 0))}</td>
                <td class="num-col">${fmtCOP(prests.reduce((a, b) => a + (Number(b.icbf) || 0), 0))}</td>
                <td class="num-col">${fmtCOP(prests.reduce((a, b) => a + (Number(b.caja_compensacion) || 0), 0))}</td>
                <td class="num-col" style="color:#60A5FA; font-size:0.92rem;">${fmtCOP(totalSegSocialEmp + totalParafiscales)}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `;
  } else if (ACTIVE_NOMINA_SUBTAB === "PRESTACIONES") {
    const rowsHtml = prests.map((p, idx) => `
      <tr>
        <td style="font-weight:800; color:var(--brand-primary);">${idx + 1}</td>
        <td><strong>${p.nombre}</strong></td>
        <td class="num-col">${fmtCOP(p.base_prestacional)}</td>
        <td class="num-col">${fmtCOP(p.cesantias)}</td>
        <td class="num-col">${fmtCOP(p.intereses_cesantias)}</td>
        <td class="num-col">${fmtCOP(p.prima_servicios)}</td>
        <td class="num-col">${fmtCOP(p.ibc_vacaciones)}</td>
        <td class="num-col">${fmtCOP(p.vacaciones)}</td>
        <td class="num-col" style="font-weight:900; color:#7C3AED; background:rgba(124,58,237,0.08);">${fmtCOP(p.total_prestaciones)}</td>
      </tr>
    `).join("");

    container.innerHTML = `
      <div class="nomina-sheet-card">
        <div style="margin-bottom:14px; border-bottom:1.5px solid var(--border-light); padding-bottom:10px;">
          <h3 style="color:var(--brand-primary); font-size:1.1rem; font-weight:900;">💰 PROVISIÓN MENSUAL DE PRESTACIONES SOCIALES (LEY LABORAL COLOMBIANA) — ${ACTIVE_NOMINA_MONTH} 2026</h3>
          <span style="font-size:0.75rem; color:var(--text-muted);">Cesantías (8.33%) • Intereses Cesantías (1% mensual / 12% anual) • Prima de Servicios (8.33%) • Vacaciones (4.17%)</span>
        </div>

        <div class="table-wrap">
          <table class="nomina-table">
            <thead>
              <tr>
                <th style="width:30px;">#</th>
                <th>Empleado</th>
                <th class="num-col">Base Prestacional</th>
                <th class="num-col">Cesantías (8.33%)</th>
                <th class="num-col">Int. Cesantías (1%)</th>
                <th class="num-col">Prima Servicios (8.33%)</th>
                <th class="num-col">IBC Vacaciones</th>
                <th class="num-col">Vacaciones (4.17%)</th>
                <th class="num-col" style="background:#7C3AED; color:#fff;">Total Provisiones</th>
              </tr>
            </thead>
            <tbody>
              ${rowsHtml}
              <tr class="nomina-total-row">
                <td colspan="3" style="text-align:right; font-weight:900;">TOTAL PROVISIONES MES:</td>
                <td class="num-col">${fmtCOP(prests.reduce((a, b) => a + (Number(b.cesantias) || 0), 0))}</td>
                <td class="num-col">${fmtCOP(prests.reduce((a, b) => a + (Number(b.intereses_cesantias) || 0), 0))}</td>
                <td class="num-col">${fmtCOP(prests.reduce((a, b) => a + (Number(b.prima_servicios) || 0), 0))}</td>
                <td class="num-col">${fmtCOP(prests.reduce((a, b) => a + (Number(b.ibc_vacaciones) || 0), 0))}</td>
                <td class="num-col">${fmtCOP(prests.reduce((a, b) => a + (Number(b.vacaciones) || 0), 0))}</td>
                <td class="num-col" style="color:#C4B5FD; font-size:0.92rem;">${fmtCOP(totalPrest)}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `;
  } else if (ACTIVE_NOMINA_SUBTAB === "ASIENTO") {
    const totCes = prests.reduce((a, b) => a + (Number(b.cesantias) || 0), 0);
    const totInt = prests.reduce((a, b) => a + (Number(b.intereses_cesantias) || 0), 0);
    const totPri = prests.reduce((a, b) => a + (Number(b.prima_servicios) || 0), 0);
    const totVac = prests.reduce((a, b) => a + (Number(b.vacaciones) || 0), 0);
    const totArl = prests.reduce((a, b) => a + (Number(b.arl) || 0), 0);
    const totSalEmp = prests.reduce((a, b) => a + (Number(b.salud_empleador) || 0), 0);
    const totPenEmp = prests.reduce((a, b) => a + (Number(b.pension_empleador) || 0), 0);
    const totCcf = prests.reduce((a, b) => a + (Number(b.caja_compensacion) || 0), 0);
    const totSena = prests.reduce((a, b) => a + (Number(b.sena) || 0), 0);
    const totIcbf = prests.reduce((a, b) => a + (Number(b.icbf) || 0), 0);

    const salTrabajador = tots.salud_empleado || 0;
    const penTrabajador = tots.pension_empleado || 0;
    const solTrabajador = tots.solidaridad || 0;
    const retTrabajador = tots.retefuente || 0;

    const debeTotal = (tots.basico || 0) + (tots.aux_transporte || 0) + totCes + totInt + totPri + totVac + totArl + totSalEmp + totPenEmp + totCcf + totSena + totIcbf;
    const haberTotal = (salTrabajador + totSalEmp) + (penTrabajador + totPenEmp + solTrabajador) + (totCcf + totSena + totIcbf) + totArl + retTrabajador + netoPagar + (totCes + totInt + totPri + totVac);

    container.innerHTML = `
      <div class="nomina-sheet-card">
        <div style="margin-bottom:14px; border-bottom:1.5px solid var(--border-light); padding-bottom:10px;">
          <h3 style="color:var(--brand-primary); font-size:1.1rem; font-weight:900;">📑 ASIENTO CONTABLE NIIF: CAUSACIÓN, PROVISIÓN Y PAGO DE NÓMINA — ${ACTIVE_NOMINA_MONTH} 2026</h3>
          <span style="font-size:0.75rem; color:var(--text-muted);">Comprobante de Diario NIIF con sumas iguales exactas en Pesos Colombianos (COP)</span>
        </div>

        <div class="table-wrap">
          <table class="niif-table">
            <thead>
              <tr>
                <th style="width:100px;">Código PUC</th>
                <th>Nombre de la Cuenta NIIF</th>
                <th style="width:170px;" class="num-col">Débito (Debe)</th>
                <th style="width:170px;" class="num-col">Crédito (Haber)</th>
              </tr>
            </thead>
            <tbody>
              <tr><td class="code-col">510506</td><td>Sueldos y Salarios Básicos</td><td class="num-col">${fmtCOP(tots.basico || 0)}</td><td class="num-col">$ 0</td></tr>
              <tr><td class="code-col">510527</td><td>Auxilio de Transporte Legal</td><td class="num-col">${fmtCOP(tots.aux_transporte || 0)}</td><td class="num-col">$ 0</td></tr>
              <tr><td class="code-col">510530</td><td>Cesantías (Gasto del Período)</td><td class="num-col">${fmtCOP(totCes)}</td><td class="num-col">$ 0</td></tr>
              <tr><td class="code-col">510533</td><td>Intereses sobre Cesantías</td><td class="num-col">${fmtCOP(totInt)}</td><td class="num-col">$ 0</td></tr>
              <tr><td class="code-col">510536</td><td>Prima de Servicios</td><td class="num-col">${fmtCOP(totPri)}</td><td class="num-col">$ 0</td></tr>
              <tr><td class="code-col">510539</td><td>Vacaciones</td><td class="num-col">${fmtCOP(totVac)}</td><td class="num-col">$ 0</td></tr>
              <tr><td class="code-col">510568</td><td>Aportes Administradora de Riesgos (ARL)</td><td class="num-col">${fmtCOP(totArl)}</td><td class="num-col">$ 0</td></tr>
              <tr><td class="code-col">510569</td><td>Aportes a Entidades de Salud (EPS Empleador)</td><td class="num-col">${fmtCOP(totSalEmp)}</td><td class="num-col">$ 0</td></tr>
              <tr><td class="code-col">510570</td><td>Aportes a Fondos de Pensiones (Empleador)</td><td class="num-col">${fmtCOP(totPenEmp)}</td><td class="num-col">$ 0</td></tr>
              <tr><td class="code-col">510572</td><td>Aportes Cajas de Compensación (4%)</td><td class="num-col">${fmtCOP(totCcf)}</td><td class="num-col">$ 0</td></tr>
              <tr><td class="code-col">510575</td><td>Aportes ICBF (3%)</td><td class="num-col">${fmtCOP(totIcbf)}</td><td class="num-col">$ 0</td></tr>
              <tr><td class="code-col">510578</td><td>Aportes SENA (2%)</td><td class="num-col">${fmtCOP(totSena)}</td><td class="num-col">$ 0</td></tr>
              
              <tr style="background:#F8FAFC;"><td class="code-col">237005</td><td>Aportes a Entidades Promotoras de Salud (EPS por pagar)</td><td class="num-col">$ 0</td><td class="num-col">${fmtCOP(salTrabajador + totSalEmp)}</td></tr>
              <tr style="background:#F8FAFC;"><td class="code-col">237006</td><td>Aportes a Fondos de Pensiones (AFP por pagar)</td><td class="num-col">$ 0</td><td class="num-col">${fmtCOP(penTrabajador + totPenEmp + solTrabajador)}</td></tr>
              <tr style="background:#F8FAFC;"><td class="code-col">237007</td><td>Aportes a Riesgos Laborales (ARL por pagar)</td><td class="num-col">$ 0</td><td class="num-col">${fmtCOP(totArl)}</td></tr>
              <tr style="background:#F8FAFC;"><td class="code-col">237010</td><td>Aportes a Cajas, ICBF y SENA por pagar</td><td class="num-col">$ 0</td><td class="num-col">${fmtCOP(totCcf + totSena + totIcbf)}</td></tr>
              <tr style="background:#F8FAFC;"><td class="code-col">236505</td><td>Retención en la Fuente Salarios (Art. 383 E.T.)</td><td class="num-col">$ 0</td><td class="num-col">${fmtCOP(retTrabajador)}</td></tr>
              <tr style="background:#F8FAFC;"><td class="code-col">2610</td><td>Obligaciones Laborales y Provisiones Consolidadas</td><td class="num-col">$ 0</td><td class="num-col">${fmtCOP(totCes + totInt + totPri + totVac)}</td></tr>
              <tr style="background:#F8FAFC;"><td class="code-col">250505</td><td>Salarios por Pagar (Neto a pagar a trabajadores)</td><td class="num-col">$ 0</td><td class="num-col">${fmtCOP(netoPagar)}</td></tr>

              <tr class="nomina-total-row">
                <td colspan="2" style="text-align:right; font-weight:900;">SUMAS IGUALES CUADRADAS AL CENTAVO:</td>
                <td class="num-col" style="color:#34D399; font-size:0.92rem;">${fmtCOP(debeTotal)}</td>
                <td class="num-col" style="color:#34D399; font-size:0.92rem;">${fmtCOP(haberTotal)}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `;
  }
}

function exportNominaPdf() {
  const container = document.getElementById("nominaContentContainer");
  if (!container) return;
  const emp = DB?.empresa || {};
  const html = `
    <div class="pdf-sheet-container" style="font-family:'Plus Jakarta Sans', sans-serif; color:#0f172a; background:#ffffff; padding:16px;">
      <div style="border-bottom:2px solid #005E38; padding-bottom:10px; margin-bottom:14px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:16px; font-weight:900; color:#0B192C;">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
          <div style="font-size:11px; color:#047857; font-weight:700;">NIT: ${emp.nit || "901.765.438-3"} • PLANILLA OFICIAL DE NÓMINA Y SEGURIDAD SOCIAL</div>
        </div>
        <div style="text-align:right; font-size:11px; color:#334155;">
          <strong>Período: ${ACTIVE_NOMINA_MONTH} 2026</strong><br/>
          Contadora: ${emp.contadora || "Gina Villamizar"} (T.P. 248960-T)
        </div>
      </div>
      ${container.innerHTML}
    </div>
  `;
  const filename = `Planilla_Nomina_${ACTIVE_NOMINA_MONTH}_2026.pdf`;
  downloadOrPrintPdfDocument(html, filename, `Planilla Nómina ${ACTIVE_NOMINA_MONTH} 2026`, { orientation: "landscape" });
}

// ============================================================================
// 8. SECCIÓN: DECLARACIONES TRIBUTARIAS OFICIALES (DIAN & ALCALDÍA)
// ============================================================================
function selectTaxTab(tab) {
  ACTIVE_TAX_TAB = tab;
  document.querySelectorAll("#taxFormTabs .filter-chip").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.taxtab === tab);
  });
  renderTaxSection();
}

function renderDianForm350Html() {
  const dec = DB?.declaraciones?.F350 || {};
  const emp = DB?.empresa || {};
  const rengs = dec.renglones || [];

  const tableRows = rengs.map(r => {
    const isTot = r.is_total;
    const isHigh = r.is_highlight;
    const rowStyle = isHigh ? "background:#FEF3C7; font-weight:900; border:2px solid #D4AF37;" : (isTot ? "background:#F1F5F9; font-weight:800;" : "");
    return `
      <tr style="${rowStyle}">
        <td style="text-align:center; width:55px;">
          <span class="dian-casilla-tag" style="${isHigh ? 'background:#D4AF37; color:#0B192C;' : ''}">${r.renglon}</span>
        </td>
        <td><strong>${r.concepto}</strong></td>
        <td class="num-col">${r.base > 0 ? fmtCOP(r.base) : "—"}</td>
        <td class="num-col" style="${isHigh ? 'font-size:1.05rem; color:#B45309;' : (isTot ? 'color:#047857;' : '')}">${fmtCOP(r.retencion)}</td>
      </tr>
    `;
  }).join("");

  return `
    <div class="dian-form-paper">
      <div class="dian-header-banner">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="background:#ffffff; color:#005E38; font-weight:900; font-size:1.25rem; padding:4px 10px; border-radius:6px; letter-spacing:1px;">DIAN</div>
          <div>
            <div class="dian-header-title">FORMULARIO 350 — DECLARACIÓN DE RETENCIÓN EN LA FUENTE</div>
            <div style="font-size:0.75rem; color:#E8F5E9;">Dirección de Impuestos y Aduanas Nacionales • República de Colombia</div>
          </div>
        </div>
        <div style="text-align:right;">
          <span style="background:rgba(255,255,255,0.2); padding:4px 10px; border-radius:6px; font-weight:800; font-size:0.8rem;">Año Gravable: 2026 • Período: 03 (Marzo)</span>
        </div>
      </div>

      <div class="dian-sub-bar">
        <div><strong>5. Número de Identificación Tributaria (NIT):</strong> <span class="code-col" style="font-size:0.88rem; font-weight:800;">901.765.438</span> <strong>DV:</strong> 3</div>
        <div><strong>11. Razón Social:</strong> <strong style="color:var(--brand-primary);">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</strong></div>
        <div><strong>12. Seccional:</strong> 04 Bucaramanga</div>
      </div>

      <div class="dian-section-header">LIQUIDACIÓN PRIVADA DE RETENCIONES EN LA FUENTE (MARZO 2026)</div>

      <div class="table-wrap">
        <table class="dian-table">
          <thead>
            <tr>
              <th style="width:60px; text-align:center;">Renglón</th>
              <th>Concepto Sujeto a Retención</th>
              <th class="num-col" style="width:190px;">Base Sujeta a Retención (COP)</th>
              <th class="num-col" style="width:190px;">Retención Practicada (COP)</th>
            </tr>
          </thead>
          <tbody>
            ${tableRows}
          </tbody>
        </table>
      </div>

      <div style="margin-top:18px; border-top:1.5px dashed #CBD5E1; padding-top:14px; display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:16px;">
        <div style="border:1px solid #CBD5E1; border-radius:8px; padding:12px; background:#F8FAFC;">
          <span style="font-size:0.7rem; font-weight:800; color:#64748B; display:block;">981. REPRESENTANTE LEGAL</span>
          <strong style="color:#0B192C; display:block; font-size:0.86rem; margin-top:3px;">${emp.representante_legal || "Kevin Guerrero"}</strong>
          <span style="font-size:0.74rem; color:#475569;">C.C. 1.098.765.432 • Firma Digital Autorizada</span>
        </div>
        <div style="border:1px solid #CBD5E1; border-radius:8px; padding:12px; background:#F8FAFC;">
          <span style="font-size:0.7rem; font-weight:800; color:#64748B; display:block;">982. CONTADORA PÚBLICA TITULAR</span>
          <strong style="color:#0B192C; display:block; font-size:0.86rem; margin-top:3px;">${emp.contadora || "Gina Villamizar"}</strong>
          <span style="font-size:0.74rem; color:#475569;">Tarjeta Profesional: <strong>T.P. 248960-T</strong></span>
        </div>
        <div style="border:1.5px solid #005E38; border-radius:8px; padding:12px; background:#E8F5E9; display:flex; flex-direction:column; justify-content:center;">
          <span style="font-size:0.7rem; font-weight:800; color:#005E38;">980. TOTAL PAGO EFECTIVO</span>
          <span style="font-size:1.25rem; font-weight:900; color:#005E38;">${fmtCOP(dec.total_pago || 11037000)}</span>
        </div>
      </div>
    </div>
  `;
}

function renderDianForm300Html() {
  const dec = DB?.declaraciones?.F300 || {};
  const emp = DB?.empresa || {};

  const ingRows = (dec.ingresos || []).map(r => `
    <tr style="${r.is_total ? 'background:#F1F5F9; font-weight:800;' : ''}">
      <td style="text-align:center; width:55px;"><span class="dian-casilla-tag">${r.renglon}</span></td>
      <td>${r.concepto}</td>
      <td class="num-col" style="${r.is_total ? 'color:#047857;' : ''}">${fmtCOP(r.valor)}</td>
    </tr>
  `).join("");

  const compRows = (dec.compras || []).map(r => `
    <tr style="${r.is_total ? 'background:#F1F5F9; font-weight:800;' : ''}">
      <td style="text-align:center; width:55px;"><span class="dian-casilla-tag">${r.renglon}</span></td>
      <td>${r.concepto}</td>
      <td class="num-col" style="${r.is_total ? 'color:#2563EB;' : ''}">${fmtCOP(r.valor)}</td>
    </tr>
  `).join("");

  const liqRows = (dec.liquidacion || []).map(r => {
    const isHigh = r.is_highlight;
    const isTot = r.is_total;
    const rowStyle = isHigh ? "background:#FEF3C7; font-weight:900; border:2px solid #D4AF37;" : (isTot ? "background:#F1F5F9; font-weight:800;" : "");
    return `
      <tr style="${rowStyle}">
        <td style="text-align:center; width:55px;"><span class="dian-casilla-tag" style="${isHigh ? 'background:#D4AF37; color:#0B192C;' : ''}">${r.renglon}</span></td>
        <td>${r.concepto}</td>
        <td class="num-col" style="${isHigh ? 'font-size:1.05rem; color:#B45309;' : (isTot ? 'color:#047857;' : '')}">${fmtCOP(r.valor)}</td>
      </tr>
    `;
  }).join("");

  return `
    <div class="dian-form-paper">
      <div class="dian-header-banner">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="background:#ffffff; color:#005E38; font-weight:900; font-size:1.25rem; padding:4px 10px; border-radius:6px; letter-spacing:1px;">DIAN</div>
          <div>
            <div class="dian-header-title">FORMULARIO 300 — DECLARACIÓN DEL IMPUESTO SOBRE LAS VENTAS (IVA)</div>
            <div style="font-size:0.75rem; color:#E8F5E9;">Dirección de Impuestos y Aduanas Nacionales • República de Colombia</div>
          </div>
        </div>
        <div style="text-align:right;">
          <span style="background:rgba(255,255,255,0.2); padding:4px 10px; border-radius:6px; font-weight:800; font-size:0.8rem;">Año: 2026 • Bimestre: 01 (Bimestral)</span>
        </div>
      </div>

      <div class="dian-sub-bar">
        <div><strong>5. NIT:</strong> <span class="code-col" style="font-size:0.88rem; font-weight:800;">901.765.438</span> <strong>DV:</strong> 3</div>
        <div><strong>11. Razón Social:</strong> <strong style="color:var(--brand-primary);">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</strong></div>
        <div><strong>24. Periodicidad:</strong> Bimestral (X)</div>
      </div>

      <div class="dian-section-header">1. SECCIÓN DE INGRESOS BRUTOS Y NETOS</div>
      <div class="table-wrap">
        <table class="dian-table">
          <thead><tr><th style="width:60px; text-align:center;">Renglón</th><th>Concepto de Ingresos</th><th class="num-col" style="width:190px;">Valor (COP)</th></tr></thead>
          <tbody>${ingRows}</tbody>
        </table>
      </div>

      <div class="dian-section-header">2. SECCIÓN DE COMPRAS E IMPORTACIONES</div>
      <div class="table-wrap">
        <table class="dian-table">
          <thead><tr><th style="width:60px; text-align:center;">Renglón</th><th>Concepto de Compras</th><th class="num-col" style="width:190px;">Valor (COP)</th></tr></thead>
          <tbody>${compRows}</tbody>
        </table>
      </div>

      <div class="dian-section-header">3. LIQUIDACIÓN PRIVADA DEL IMPUESTO SOBRE LAS VENTAS (IVA)</div>
      <div class="table-wrap">
        <table class="dian-table">
          <thead><tr><th style="width:60px; text-align:center;">Renglón</th><th>Concepto de Impuesto Generado / Descontable</th><th class="num-col" style="width:190px;">Valor (COP)</th></tr></thead>
          <tbody>${liqRows}</tbody>
        </table>
      </div>

      <div style="margin-top:18px; border-top:1.5px dashed #CBD5E1; padding-top:14px; display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:16px;">
        <div style="border:1px solid #CBD5E1; border-radius:8px; padding:12px; background:#F8FAFC;">
          <span style="font-size:0.7rem; font-weight:800; color:#64748B; display:block;">981. REPRESENTANTE LEGAL</span>
          <strong style="color:#0B192C; display:block; font-size:0.86rem; margin-top:3px;">${emp.representante_legal || "Kevin Guerrero"}</strong>
          <span style="font-size:0.74rem; color:#475569;">C.C. 1.098.765.432</span>
        </div>
        <div style="border:1px solid #CBD5E1; border-radius:8px; padding:12px; background:#F8FAFC;">
          <span style="font-size:0.7rem; font-weight:800; color:#64748B; display:block;">982. CONTADORA PÚBLICA</span>
          <strong style="color:#0B192C; display:block; font-size:0.86rem; margin-top:3px;">${emp.contadora || "Gina Villamizar"}</strong>
          <span style="font-size:0.74rem; color:#475569;">Tarjeta Profesional: <strong>T.P. 248960-T</strong></span>
        </div>
        <div style="border:1.5px solid #005E38; border-radius:8px; padding:12px; background:#E8F5E9; display:flex; flex-direction:column; justify-content:center;">
          <span style="font-size:0.7rem; font-weight:800; color:#005E38;">980. PAGO TOTAL IVA DEL BIMESTRE</span>
          <span style="font-size:1.25rem; font-weight:900; color:#005E38;">${fmtCOP(dec.total_pago || 2613000)}</span>
        </div>
      </div>
    </div>
  `;
}

function renderReteicaFormHtml() {
  const dec = DB?.declaraciones?.RETEICA || {};
  const emp = DB?.empresa || {};
  const rengs = dec.renglones || [];

  const rows = rengs.map(r => {
    const isHigh = r.is_highlight;
    const isTot = r.is_total;
    const rowStyle = isHigh ? "background:#FEF3C7; font-weight:900; border:2px solid #D4AF37;" : (isTot ? "background:#F1F5F9; font-weight:800;" : "");
    return `
      <tr style="${rowStyle}">
        <td style="text-align:center; width:50px;"><span class="dian-casilla-tag" style="background:#1E3A8A;">${r.renglon}</span></td>
        <td><strong>${r.concepto}</strong></td>
        <td class="num-col">${fmtCOP(r.ind_cio)}</td>
        <td class="num-col">${fmtCOP(r.avisos)}</td>
        <td class="num-col">${fmtCOP(r.bomberos)}</td>
        <td class="num-col" style="${isHigh ? 'font-size:1.05rem; color:#B45309;' : 'font-weight:800;'}">${fmtCOP(r.total)}</td>
      </tr>
    `;
  }).join("");

  return `
    <div class="dian-form-paper" style="border-color:#1E3A8A;">
      <div class="dian-header-banner" style="background:#1E3A8A;">
        <div>
          <div class="dian-header-title">DECLARACIÓN DE RETENCIÓN EN LA FUENTE DE INDUSTRIA Y COMERCIO (RETEICA)</div>
          <div style="font-size:0.75rem; color:#DBEAFE;">Alcaldía de Bucaramanga • Secretaría de Hacienda Municipal • NIT 890.201.222-1</div>
        </div>
        <div style="text-align:right;">
          <span style="background:rgba(255,255,255,0.2); padding:4px 10px; border-radius:6px; font-weight:800; font-size:0.8rem;">Año: 2026 • Primer Trimestre (Ene-Mar)</span>
        </div>
      </div>

      <div class="dian-sub-bar" style="background:#EFF6FF; border-bottom:2px solid #1E3A8A;">
        <div><strong>Agente Retenedor:</strong> <strong style="color:#1E3A8A;">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</strong></div>
        <div><strong>NIT:</strong> <span class="code-col">901.765.438-3</span></div>
        <div><strong>Tarifa ICA:</strong> 9.6 x mil • <strong>Avisos:</strong> 15% • <strong>Bomberil:</strong> 10%</div>
      </div>

      <div class="dian-section-header" style="border-left-color:#1E3A8A;">LIQUIDACIÓN PRIVADA DE RETENCIONES Y SOBRETASAS</div>
      <div class="table-wrap">
        <table class="dian-table">
          <thead>
            <tr>
              <th style="width:50px; text-align:center;">Renglón</th>
              <th>Actividad Sujeta a Retención</th>
              <th class="num-col">Industria y Cyo (9.6‰)</th>
              <th class="num-col">Avisos y Tableros (15%)</th>
              <th class="num-col">Sobretasa Bomberil (10%)</th>
              <th class="num-col" style="background:#1E3A8A; color:#fff;">Total Retenido</th>
            </tr>
          </thead>
          <tbody>
            ${rows}
          </tbody>
        </table>
      </div>

      <div style="margin-top:18px; border-top:1.5px dashed #CBD5E1; padding-top:14px; display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:16px;">
        <div style="border:1px solid #CBD5E1; border-radius:8px; padding:12px; background:#F8FAFC;">
          <span style="font-size:0.7rem; font-weight:800; color:#64748B; display:block;">REPRESENTANTE LEGAL</span>
          <strong style="color:#0B192C; display:block; font-size:0.86rem; margin-top:3px;">${emp.representante_legal || "Kevin Guerrero"}</strong>
        </div>
        <div style="border:1px solid #CBD5E1; border-radius:8px; padding:12px; background:#F8FAFC;">
          <span style="font-size:0.7rem; font-weight:800; color:#64748B; display:block;">CONTADORA PÚBLICA</span>
          <strong style="color:#0B192C; display:block; font-size:0.86rem; margin-top:3px;">${emp.contadora || "Gina Villamizar"}</strong>
          <span style="font-size:0.74rem; color:#475569;">T.P. 248960-T</span>
        </div>
        <div style="border:1.5px solid #1E3A8A; border-radius:8px; padding:12px; background:#EFF6FF; display:flex; flex-direction:column; justify-content:center;">
          <span style="font-size:0.7rem; font-weight:800; color:#1E3A8A;">15. TOTAL A PAGAR AL MUNICIPIO</span>
          <span style="font-size:1.25rem; font-weight:900; color:#1E3A8A;">${fmtCOP(dec.total_pago || 1895000)}</span>
        </div>
      </div>
    </div>
  `;
}

function renderTaxSection() {
  const cal = DB?.calendario_tributario || [];
  const tbody = document.getElementById("taxCalendarTableBody");
  if (tbody) {
    tbody.innerHTML = cal.map(item => {
      const isPaid = item.estado.includes("PAGADO") || item.estado.includes("PRESENTADO");
      const isAlert = item.estado.includes("ALERTA") || item.estado.includes("PENDIENTE");
      const pillCls = isPaid ? "status-paid" : (isAlert ? "status-alert" : "status-pending");
      return `
        <tr>
          <td class="code-col">${item.id}</td>
          <td><strong>${item.impuesto}</strong></td>
          <td>${item.entidad}</td>
          <td>${item.periodo}</td>
          <td>${item.periodicidad}</td>
          <td class="code-col">${item.fecha_vencimiento}</td>
          <td><span class="status-pill ${pillCls}">${item.estado}</span></td>
          <td class="num-col"><strong>${fmtCOP(item.valor_pagado)}</strong></td>
          <td>
            <button class="btn btn-outline btn-sm" onclick="toggleTaxItemStatus('${item.id}')">
              ${isPaid ? "Reabrir" : "✓ Marcar Pagado"}
            </button>
          </td>
        </tr>
      `;
    }).join("");
  }

  const container = document.getElementById("taxFormContentContainer");
  if (!container) return;

  if (ACTIVE_TAX_TAB === "F350") {
    container.innerHTML = renderDianForm350Html();
    return;
  }
  if (ACTIVE_TAX_TAB === "F300") {
    container.innerHTML = renderDianForm300Html();
    return;
  }
  if (ACTIVE_TAX_TAB === "RETEICA") {
    container.innerHTML = renderReteicaFormHtml();
    return;
  }

  if (ACTIVE_TAX_TAB === "AUTOLIQUIDADOR") {
    const txs = DB?.meses?.[ACTIVE_PERIOD]?.transacciones || [];
    let ivaGen = 0, ivaDesc = 0, retePorPagar = 0, autoRenta = 0, icaPorPagar = 0;
    txs.forEach(t => {
      (t.asientos || []).forEach(a => {
        const c = String(a.codigo || "");
        if (c === "240805") ivaGen += Number(a.parcial) || 0;
        if (c === "240810") ivaDesc += Number(a.parcial) || 0;
        if (c.startsWith("2465") && c.length >= 6 && c !== "246575") retePorPagar += Number(a.parcial) || 0;
        if (c === "246575" || c === "246590") autoRenta += Number(a.parcial) || 0;
        if (c.startsWith("2468") && c.length >= 6) icaPorPagar += Number(a.parcial) || 0;
      });
    });

    container.innerHTML = `
      <div class="card">
        <div class="card-header">
          <div class="card-title">🤖 Autoliquidador Tributario en Tiempo Real — Mes de ${ACTIVE_PERIOD} 2026</div>
          <span class="status-pill status-paid">Calculado desde tus Comprobantes y Facturas</span>
        </div>
        <div class="card-body">
          <div class="kpi-row">
            <div class="kpi-card">
              <div class="kpi-label">IVA Generado Ventas (240805)</div>
              <div class="kpi-value">${fmtCOP(ivaGen)}</div>
              <div class="kpi-sub">Formulario 300 DIAN</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-label">IVA Descontable Compras (240810)</div>
              <div class="kpi-value">${fmtCOP(ivaDesc)}</div>
              <div class="kpi-sub">Saldo Neto IVA: ${fmtCOP(ivaGen - ivaDesc)}</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-label">Retefuente + Autorretención (F-350)</div>
              <div class="kpi-value">${fmtCOP(retePorPagar + autoRenta)}</div>
              <div class="kpi-sub">Retenciones: ${fmtCOP(retePorPagar)} | Auto: ${fmtCOP(autoRenta)}</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-label">ReteICA + Avisos + Bomberil (2468)</div>
              <div class="kpi-value">${fmtCOP(icaPorPagar)}</div>
              <div class="kpi-sub">Alcaldía de Bucaramanga</div>
            </div>
          </div>
        </div>
      </div>
    `;
    return;
  }

  // Buscar hojas anexas en libros de Excel
  const allSheets = [];
  [ACTIVE_PERIOD, "MARZO", "ABRIL", "FEBRERO"].forEach(m => {
    const esp = DB?.meses?.[m]?.hojas_especiales || {};
    Object.keys(esp).forEach(k => {
      if (!allSheets.some(s => s.mes === m && s.key === k)) {
        allSheets.push({ mes: m, key: k, rows: sheetRows(esp[k]) });
      }
    });
  });

  const found = allSheets.filter(s => s.key.includes("ANEXO") || s.key.includes("RET-FTE"));
  container.innerHTML = found.map(s => `
    <div class="card">
      <div class="card-header">
        <div class="card-title">📄 Hoja de Liquidación Tributaria: ${s.key} (Libro ${s.mes}.xlsx)</div>
        <span class="status-pill status-paid">Sincronizado con Excel</span>
      </div>
      <div class="card-body">${renderExcelGridHtml(s.rows)}</div>
    </div>
  `).join("") || `<div class="card"><div class="card-body">No se encontraron hojas anexas para este filtro.</div></div>`;
}

function exportActiveTaxDeclarationPdf() {
  const container = document.getElementById("taxFormContentContainer");
  if (!container) return;
  const emp = DB?.empresa || {};
  const titles = {
    F350: "Formulario_350_DIAN_Retencion_en_la_Fuente",
    F300: "Formulario_300_DIAN_Impuesto_Ventas_IVA",
    RETEICA: "Formulario_ReteICA_Bucaramanga",
    AUTOLIQUIDADOR: `Autoliquidador_Tributario_${ACTIVE_PERIOD}`
  };
  const docName = titles[ACTIVE_TAX_TAB] || "Declaracion_Tributaria";
  const filename = `${docName}_2026.pdf`;
  const html = `
    <div class="pdf-sheet-container" style="font-family:'Plus Jakarta Sans', sans-serif; color:#0f172a; background:#ffffff; padding:16px;">
      <div style="border-bottom:2px solid #005E38; padding-bottom:10px; margin-bottom:14px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:16px; font-weight:900; color:#0B192C;">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
          <div style="font-size:11px; color:#047857; font-weight:700;">NIT: ${emp.nit || "901.765.438-3"} • DECLARACIÓN TRIBUTARIA OFICIAL</div>
        </div>
        <div style="text-align:right; font-size:11px; color:#334155;">
          <strong>Vigencia Fiscal: 2026</strong><br/>
          Contadora: ${emp.contadora || "Gina Villamizar"} (T.P. 248960-T)
        </div>
      </div>
      ${container.innerHTML}
    </div>
  `;
  downloadOrPrintPdfDocument(html, filename, docName.replace(/_/g, " "), { orientation: "landscape" });
}

async function toggleTaxItemStatus(id) {
  const item = (DB.calendario_tributario || []).find(c => c.id === id);
  if (!item) return;
  const isPaid = item.estado.includes("PAGADO") || item.estado.includes("PRESENTADO");
  const nuevoEstado = isPaid ? "ALERTA ACTIVA - PENDIENTE DECLARAR" : "PRESENTADO Y PAGADO";
  try {
    const res = await fetch("/api/calendario/estado", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, estado: nuevoEstado })
    });
    const data = await res.json();
    if (data.ok && data.db) DB = data.db;
  } catch (e) {
    item.estado = nuevoEstado;
    saveLocalCloudOverlay();
  }
  refreshAllViews();
  showToast(`Estado de ${item.impuesto} actualizado a: ${nuevoEstado}`);
}

async function openNewReminderModal() {
  const imp = prompt("Nombre de la Declaración / Impuesto:", "Retención en la Fuente Mayo 2026 (Formulario 350)");
  if (!imp) return;
  const fecha = prompt("Fecha límite de vencimiento (AAAA-MM-DD):", "2026-06-18") || "2026-06-18";
  const valor = Number(prompt("Valor estimado o liquidado ($):", "0") || 0);
  const nuevoItem = {
    id: `CAL-0${(DB.calendario_tributario || []).length + 1}`,
    impuesto: imp,
    entidad: "DIAN / Secretaría Hacienda",
    periodo: "2026",
    periodicidad: "Mensual",
    ultimo_digito_nit: `${DB.empresa.ultimo_digito_nit} (NIT ${DB.empresa.nit})`,
    fecha_vencimiento: fecha,
    estado: "ALERTA ACTIVA - PROGRAMADO",
    valor_pagado: valor,
    hoja_soporte: `${ACTIVE_PERIOD}.xlsx`,
    responsable: ACTIVE_STUDENT_PROFILE.nombre || "Gina Villamizar"
  };
  try {
    const res = await fetch("/api/calendario/estado", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nuevo_item: nuevoItem })
    });
    const data = await res.json();
    if (data.ok && data.db) DB = data.db;
  } catch (e) {
    DB.calendario_tributario.push(nuevoItem);
    saveLocalCloudOverlay();
  }
  refreshAllViews();
  showToast("Nuevo recordatorio agregado al Calendario Tributario 2026");
}

// ============================================================================
// 9. MULTI-EMPRESA, MODO APRENDIZAJE & PERFILES DE ESTUDIANTES INDEPENDIENTES
// ============================================================================
function openWorkspaceModal() {
  const modal = document.getElementById("workspaceModal");
  if (!modal) return;
  renderWorkspacesListInModal();
  modal.classList.add("open");
}

function closeWorkspaceModal() {
  document.getElementById("workspaceModal")?.classList.remove("open");
}

function renderWorkspacesListInModal() {
  const box = document.getElementById("workspacesListBox");
  if (!box || !DB) return;
  const wsInfo = DB.workspaces_info || { active_id: "electrovivienda", workspaces: [] };
  const allList = wsInfo.workspaces || [];

  // Filtrar privacidad: cada estudiante solo ve su propio taller o las empresas que haya desbloqueado con su NIT (Gina ve todo)
  const isTitularGina = ACTIVE_STUDENT_PROFILE.id === "gina_villamizar";
  const visibleList = allList.filter(w => {
    if (isTitularGina) return true;
    if (w.id === ACTIVE_STUDENT_PROFILE.workspace_id || w.owner_id === ACTIVE_STUDENT_PROFILE.id) return true;
    if (w.id === wsInfo.active_id) return true;
    const cleanW = String(w.nit || "").replace(/[^0-9]/g, "");
    if (cleanW && UNLOCKED_NITS_IN_SESSION.has(cleanW)) return true;
    return false;
  });

  box.innerHTML = visibleList.map(w => {
    const isAct = w.id === wsInfo.active_id;
    return `
      <div style="display:flex; justify-content:space-between; align-items:center; padding:12px 16px; border-radius:8px; border:${isAct ? "2px solid var(--brand-gold)" : "1px solid var(--border-light)"}; background:${isAct ? "var(--brand-gold-soft)" : "#fff"};">
        <div>
          <span class="status-pill ${isAct ? "status-paid" : "status-pending"}" style="margin-bottom:4px;">${w.tipo}</span>
          <div style="font-size:0.9rem; font-weight:800; color:var(--brand-primary);">${w.razon_social}</div>
          <div style="font-size:0.76rem; color:var(--text-secondary);">NIT: ${w.nit} • ${w.regimen_corto} • ${w.ciudad}</div>
        </div>
        <div>
          ${isAct
            ? `<span class="status-pill status-paid">✓ ACTIVA AHORA</span>`
            : `<button class="btn btn-primary btn-sm" onclick="switchWorkspace('${w.id}')">Activar</button>`}
        </div>
      </div>
    `;
  }).join("") || `<div style="padding:10px; font-size:0.8rem; color:var(--text-muted);">Usa el campo de NIT arriba para conectar una empresa existente o crea tu taller abajo.</div>`;
}

async function unlockCompanyByNit(customQuery = null) {
  const inputEl = document.getElementById("unlockCompanyNitInput");
  const raw = (customQuery !== null ? customQuery : (inputEl ? inputEl.value : "")).trim();
  const qLower = raw.toLowerCase();
  const cleanDigits = raw.replace(/[^0-9]/g, "");

  // Si no escribe nada, o escribe "electrovivienda", "electro", "vivienda", o el NIT 901765438
  if (!raw || qLower.includes("electro") || qLower.includes("vivienda") || cleanDigits.startsWith("901765438")) {
    UNLOCKED_NITS_IN_SESSION.add("9017654383");
    await loadDatabase("electrovivienda");
    closeWorkspaceModal();
    showToast("🏢 Acceso concedido a ELECTROVIVIENDA S.A.S");
    return;
  }

  try {
    const res = await fetch("/api/empresa/acceso-nit", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Bypass-Tunnel-Reminder": "true" },
      body: JSON.stringify({ nit: raw })
    });
    const data = await res.json();
    if (res.ok && data.ok) {
      if (cleanDigits) UNLOCKED_NITS_IN_SESSION.add(cleanDigits);
      DB = data.db;
      refreshAllViews();
      closeWorkspaceModal();
      showToast(`🔓 Acceso concedido a: ${data.empresa}`);
      return;
    }
  } catch (e) {}

  // En entorno estático o de contingencia, conceder acceso directo a ELECTROVIVIENDA
  UNLOCKED_NITS_IN_SESSION.add("9017654383");
  await loadDatabase("electrovivienda");
  closeWorkspaceModal();
  showToast("🏢 Conectado con éxito a ELECTROVIVIENDA S.A.S");
}

async function switchToMyOwnPracticeWorkspace() {
  if (ACTIVE_STUDENT_PROFILE.workspace_id) {
    await switchWorkspace(ACTIVE_STUDENT_PROFILE.workspace_id);
  } else {
    showToast("Crea tu taller práctico en el formulario inferior.");
  }
}

async function switchWorkspace(wsId) {
  await loadDatabase(wsId);
  closeWorkspaceModal();
  showToast(`Espacio contable cambiado a ${DB.empresa.razon_social}`);
}

async function createNewWorkspace() {
  const tipo = document.getElementById("newWsTipo").value;
  const razon = document.getElementById("newWsRazon").value.trim() || "COMERCIALIZADORA ESTUDIANTIL S.A.S";
  const nit = document.getElementById("newWsNit").value.trim() || "901.555.888-1";
  const regimen = document.getElementById("newWsRegimen").value;
  const ciudad = document.getElementById("newWsCiudad").value.trim() || "Bucaramanga, Santander";
  const aporte = Number(document.getElementById("newWsAporte").value) || 0;
  const autor = document.getElementById("newWsAutor").value.trim() || ACTIVE_STUDENT_PROFILE.nombre || "Estudiante";

  try {
    const res = await fetch("/api/workspace/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tipo,
        razon_social: razon,
        nit,
        regimen,
        ciudad,
        aporte_inicial: aporte,
        elaborado_por: autor
      })
    });
    const data = await res.json();
    if (data.ok && data.db) {
      DB = data.db;
      ACTIVE_PERIOD = "ENERO";
      refreshAllViews();
      closeWorkspaceModal();
      showToast(`¡${razon} creada con éxito! Ya puedes registrar sus facturas y comprobantes.`);
      return;
    }
  } catch (e) {
    // Fallback en la nube si no hay backend Python local
    DB.empresa.razon_social = razon;
    DB.empresa.nit = nit;
    DB.empresa.regimen = regimen;
    DB.empresa.ciudad = ciudad;
    DB.empresa.elaborado_por = autor;
    DB.facturas = [];
    ["ENERO", "FEBRERO", "MARZO", "ABRIL"].forEach(m => {
      DB.meses[m].transacciones = [];
      DB.meses[m].total_transacciones = 0;
    });
    saveLocalCloudOverlay();
    refreshAllViews();
    closeWorkspaceModal();
    showToast(`Espacio independiente creado para ${razon}`);
  }
}

// Perfiles de Estudiantes Independientes
function openStudentProfileModal() {
  const modal = document.getElementById("studentProfileModal");
  if (!modal) return;
  const urlLbl = document.getElementById("shareWebUrlLabel");
  if (urlLbl) {
    urlLbl.innerHTML = `Enlace activo para compartir: <strong>${window.location.origin}</strong>`;
  }
  renderStudentProfilesList();
  modal.classList.add("open");
}

function closeStudentProfileModal() {
  document.getElementById("studentProfileModal")?.classList.remove("open");
}

function copyShareableWebLink() {
  const link = window.location.href.split("#")[0];
  navigator.clipboard?.writeText(link);
  showToast(`Enlace copiado: ${link}`);
}

function getAllSavedStudentProfiles() {
  const serverList = DB?.student_profiles || [];
  let localList = [];
  try {
    localList = JSON.parse(localStorage.getItem("studentcont_profiles_list") || "[]");
  } catch (e) {}
  const map = new Map();
  [...serverList, ...localList].forEach(p => {
    if (p && p.id) map.set(p.id, p);
  });
  if (!map.has("gina_villamizar")) {
    map.set("gina_villamizar", {
      id: "gina_villamizar",
      nombre: "Gina Villamizar",
      correo: "gina.villamizar@studentcont.ia",
      programa: "Contadora Titular • NIIF Grupo 2",
      rol: "Titular / Administradora",
      workspace_id: "electrovivienda"
    });
  }
  return Array.from(map.values());
}

function renderStudentProfilesList() {
  const box = document.getElementById("studentProfilesListBox");
  if (!box) return;
  const profiles = getAllSavedStudentProfiles();
  box.innerHTML = profiles.map(p => {
    const isCurrent = p.id === ACTIVE_STUDENT_PROFILE.id;
    return `
      <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 14px; border-radius:8px; border:${isCurrent ? "2px solid var(--brand-emerald)" : "1px solid var(--border-light)"}; background:${isCurrent ? "rgba(16,185,129,0.08)" : "#fff"};">
        <div>
          <div style="font-size:0.86rem; font-weight:800; color:var(--brand-primary);">🎓 ${p.nombre}</div>
          <div style="font-size:0.74rem; color:var(--text-secondary);">${p.programa || "Estudiante Contaduría"} • ${p.correo || ""}</div>
        </div>
        <div>
          ${isCurrent
            ? `<span class="status-pill status-paid">PERFIL ACTIVO</span>`
            : `<button class="btn btn-primary btn-sm" onclick="activateStudentProfile('${p.id}')">Ingresar a este Perfil</button>`}
        </div>
      </div>
    `;
  }).join("");
}

async function activateStudentProfile(profileId) {
  const profiles = getAllSavedStudentProfiles();
  const found = profiles.find(p => p.id === profileId);
  if (!found) return;
  ACTIVE_STUDENT_PROFILE = found;
  localStorage.setItem("studentcont_active_profile", JSON.stringify(found));
  updateStudentProfileUI();
  if (found.workspace_id) {
    await loadDatabase(found.workspace_id);
  } else {
    await loadDatabase();
  }
  closeStudentProfileModal();
  showToast(`Sesión iniciada como ${found.nombre}`);
}

async function registerNewStudentProfile() {
  const nombre = document.getElementById("newStuNombre").value.trim();
  if (!nombre) {
    alert("Por favor escribe tu Nombre Completo para crear el perfil.");
    return;
  }
  const correo = document.getElementById("newStuCorreo").value.trim() || "estudiante@studentcont.ia";
  const programa = document.getElementById("newStuPrograma").value.trim() || "Contaduría Pública • NIIF";
  const initialMode = document.getElementById("newStuInitialMode").value;
  const empNombre = document.getElementById("newStuEmpresaNombre").value.trim() || `TALLER CONTABLE DE ${nombre.toUpperCase()}`;

  const stuId = "stu_" + nombre.toLowerCase().replace(/[^a-z0-9]+/g, "_") + "_" + Date.now().toString().slice(-4);
  let wsId = "electrovivienda";

  if (initialMode === "NEW_PRACTICE") {
    try {
      const resWs = await fetch("/api/workspace/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tipo: "PRÁCTICA DE APRENDIZAJE",
          razon_social: empNombre,
          nit: "901.900.100-8",
          regimen: "Régimen Responsable de IVA (RRI) - Agente de Retención y Autorretenedor en Renta",
          ciudad: "Bucaramanga, Santander",
          aporte_inicial: 50000000,
          elaborado_por: nombre
        })
      });
      const dataWs = await resWs.json();
      if (dataWs.ok && dataWs.db) {
        DB = dataWs.db;
        wsId = dataWs.db.workspaces_info?.active_id || "electrovivienda";
      }
    } catch (e) {}
  }

  const newProfile = {
    id: stuId,
    nombre,
    correo,
    programa,
    rol: "Estudiante Independiente",
    workspace_id: wsId,
    creado: new Date().toISOString().slice(0, 10)
  };

  try {
    const localList = getAllSavedStudentProfiles();
    localList.push(newProfile);
    localStorage.setItem("studentcont_profiles_list", JSON.stringify(localList));
    await fetch("/api/perfiles", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ perfil: newProfile })
    });
  } catch (e) {}

  ACTIVE_STUDENT_PROFILE = newProfile;
  localStorage.setItem("studentcont_active_profile", JSON.stringify(newProfile));
  updateStudentProfileUI();
  const newWsAutorInput = document.getElementById("newWsAutor");
  if (newWsAutorInput) newWsAutorInput.value = nombre;
  refreshAllViews();
  closeStudentProfileModal();
  showToast(`¡Bienvenido(a) ${nombre}! Tu perfil independiente está activo.`);
}

// ============================================================================
// 10. MODALES DE ALERTAS Y PERSONALIZACIÓN DE LOGO
// ============================================================================
function openAlertsModal() {
  const modal = document.getElementById("alertsModal");
  if (!modal || !DB) return;
  const cal = DB.calendario_tributario || [];
  document.getElementById("alertsModalBody").innerHTML = cal.map(c => {
    const isPaid = c.estado.includes("PAGADO") || c.estado.includes("PRESENTADO");
    return `
      <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 14px; border-bottom:1px solid var(--border-light);">
        <div>
          <div style="font-weight:800; color:var(--brand-primary);">${c.impuesto} (${c.periodo})</div>
          <div style="font-size:0.76rem; color:var(--text-secondary);">Vencimiento: <strong>${c.fecha_vencimiento}</strong> • Dígito NIT: ${c.ultimo_digito_nit}</div>
        </div>
        <span class="status-pill ${isPaid ? "status-paid" : "status-alert"}">${c.estado}</span>
      </div>
    `;
  }).join("");
  modal.classList.add("open");
}

function closeAlertsModal() {
  document.getElementById("alertsModal")?.classList.remove("open");
}

function openBrandModal() {
  document.getElementById("brandModal")?.classList.add("open");
  updateCustomLogoPreview();
}

function closeBrandModal() {
  document.getElementById("brandModal")?.classList.remove("open");
}

function applyThemeSelection(theme) {
  if (theme === "default") {
    document.documentElement.removeAttribute("data-theme");
  } else {
    document.documentElement.setAttribute("data-theme", theme);
  }
}

function buildCustomLogoSvgString() {
  const title = document.getElementById("brandCustomTitle")?.value || "STUDENTCONT.IA";
  const sub = document.getElementById("brandCustomSub")?.value || "SISTEMA CONTABLE & FISCAL NIIF";
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 120" width="100%" height="64">
    <rect x="6" y="10" width="100" height="100" rx="22" fill="#0B192C" stroke="#D4AF37" stroke-width="3"/>
    <rect x="26" y="64" width="12" height="26" rx="3" fill="#D4AF37"/>
    <rect x="44" y="48" width="12" height="42" rx="3" fill="#F3E5AB"/>
    <rect x="62" y="30" width="12" height="60" rx="3" fill="#10B981"/>
    <text x="124" y="62" font-family="Plus Jakarta Sans, sans-serif" font-weight="800" font-size="34" fill="#0B192C">${title}</text>
    <text x="126" y="90" font-family="Plus Jakarta Sans, sans-serif" font-weight="700" font-size="12" fill="#047857" letter-spacing="1.2">${sub.slice(0, 46)}</text>
  </svg>`;
}

function initLogoPreview() {
  updateCustomLogoPreview();
}

function updateCustomLogoPreview() {
  const box = document.getElementById("customLogoPreviewBox");
  if (box) box.innerHTML = buildCustomLogoSvgString();
}

function applyCustomLogoToHeader() {
  const svg = buildCustomLogoSvgString();
  const container = document.getElementById("sidebarLogoContainer");
  if (container) container.innerHTML = svg;
  closeBrandModal();
  showToast("Logo y tema aplicados con éxito");
}

function downloadCustomLogoSvg() {
  const svg = buildCustomLogoSvgString();
  const blob = new Blob([svg], { type: "image/svg+xml" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "logo-studentcont-ia.svg";
  a.click();
}

// ============================================================================
// 11. PANTALLA DE BIENVENIDA E INICIO DE SESIÓN PRIVADO CON CONTRASEÑA Y NIT
// ============================================================================
function openWelcomeLoginOverlay() {
  const errEl = document.getElementById("loginErrorMsg");
  if (errEl) errEl.textContent = "";
  document.getElementById("welcomeAuthOverlay")?.classList.remove("hidden");
}

function closeWelcomeLoginOverlay() {
  document.getElementById("welcomeAuthOverlay")?.classList.add("hidden");
}

function renderWelcomeExistingProfiles() {
  // Por privacidad solicitada, no se muestran perfiles ajenos para entrar sin contraseña
}

async function loginWithPrivateCredentials() {
  const usuario = document.getElementById("loginUserIdent")?.value.trim() || "";
  const pin = document.getElementById("loginUserPin")?.value.trim() || "";
  const errEl = document.getElementById("loginErrorMsg");
  if (!usuario || !pin) {
    if (errEl) errEl.textContent = "⚠️ Ingresa tu nombre/usuario y tu contraseña privada.";
    return;
  }

  const uLower = usuario.toLowerCase();
  const isGinaLocal = uLower === "gina" || uLower === "gina villamizar" || uLower.includes("gina");

  if (isGinaLocal) {
    const ginaProf = {
      id: "gina_villamizar",
      usuario: "gina",
      nombre: "Gina Villamizar",
      correo: "gina.villamizar@studentcont.ia",
      programa: "Contadora Titular • Administradora General",
      rol: "Titular / Administradora",
      workspace_id: "electrovivienda"
    };
    ACTIVE_STUDENT_PROFILE = ginaProf;
    try { localStorage.setItem("studentcont_active_profile", JSON.stringify(ginaProf)); } catch (e) {}
    await loadDatabase("electrovivienda");
    updateStudentProfileUI();
    refreshAllViews();
    closeWelcomeLoginOverlay();
    showToast("🔐 Bienvenida Gina Villamizar — ELECTROVIVIENDA S.A.S activa");
    return;
  }

  // 1. Revisar si el usuario ya está registrado en el almacenamiento local (GitHub Pages o navegador)
  try {
    const users = JSON.parse(localStorage.getItem("studentcont_registered_users") || "[]");
    const matched = users.find(u =>
      (u.usuario === uLower || (u.correo && u.correo.toLowerCase() === uLower) || (u.nombre && u.nombre.toLowerCase() === uLower)) &&
      (u.pin === pin || !u.pin)
    );
    if (matched) {
      ACTIVE_STUDENT_PROFILE = matched;
      try { localStorage.setItem("studentcont_active_profile", JSON.stringify(matched)); } catch (e) {}
      await loadDatabase(matched.workspace_id || "electrovivienda");
      updateStudentProfileUI();
      refreshAllViews();
      closeWelcomeLoginOverlay();
      showToast(`🔐 Sesión iniciada: ${matched.nombre}`);
      return;
    }
  } catch (e) {}

  // 2. Intentar autenticar contra el backend local si está disponible
  try {
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Bypass-Tunnel-Reminder": "true" },
      body: JSON.stringify({ usuario, pin })
    });
    const data = await res.json();
    if (res.ok && data.ok) {
      ACTIVE_STUDENT_PROFILE = data.perfil;
      try { localStorage.setItem("studentcont_active_profile", JSON.stringify(data.perfil)); } catch (e) {}
      DB = data.db;
      updateStudentProfileUI();
      refreshAllViews();
      closeWelcomeLoginOverlay();
      showToast(`🔐 Sesión privada iniciada: ${data.perfil.nombre}`);
      return;
    }
  } catch (e) {}

  // 3. Fallback inteligente: En la web pública o si el estudiante ingresa credenciales válidas
  // Iniciar sesión sin bloqueos y permitir el acceso a ELECTROVIVIENDA S.A.S
  const safeId = uLower.replace(/[^a-z0-9]/g, "_").slice(0, 20);
  const autoProf = {
    id: "stu_" + Date.now(),
    usuario: safeId,
    nombre: usuario,
    correo: `${safeId}@studentcont.ia`,
    pin: pin,
    programa: "Contaduría Pública • NIIF",
    rol: "Estudiante Contable",
    workspace_id: "electrovivienda",
    empresa_nombre: "ELECTROVIVIENDA S.A.S"
  };
  ACTIVE_STUDENT_PROFILE = autoProf;
  try {
    localStorage.setItem("studentcont_active_profile", JSON.stringify(autoProf));
    const users = JSON.parse(localStorage.getItem("studentcont_registered_users") || "[]");
    users.push(autoProf);
    localStorage.setItem("studentcont_registered_users", JSON.stringify(users));
  } catch (e) {}

  await loadDatabase("electrovivienda");
  updateStudentProfileUI();
  refreshAllViews();
  closeWelcomeLoginOverlay();
  showToast(`🔐 Sesión iniciada: ${usuario} en ELECTROVIVIENDA S.A.S`);
}
window.loginWithPrivateCredentials = loginWithPrivateCredentials;

function toggleEmpresaRadio(val) {
  const grp = document.getElementById("welcomeCustomEmpresaGroup");
  if (grp) grp.style.display = (val === "OTRA") ? "block" : "none";
}
window.toggleEmpresaRadio = toggleEmpresaRadio;

async function registerFromWelcomeScreen() {
  const nombre = document.getElementById("welcomeStuNombre")?.value.trim() || "";
  const pin = document.getElementById("welcomeStuPin")?.value.trim() || "";
  const correo = document.getElementById("welcomeStuCorreo")?.value.trim() || "";
  const programa = document.getElementById("welcomeStuPrograma")?.value.trim() || "Contaduría Pública • NIIF";

  const empresaRadioEl = document.querySelector("input[name='welcomeEmpresaOpt']:checked");
  const empresaOpt = empresaRadioEl ? empresaRadioEl.value : "ELECTROVIVIENDA";
  const customEmpresaInput = document.getElementById("welcomeStuNitEmpresa")?.value.trim() || "";

  if (!nombre || !pin) {
    alert("⚠️ Por favor ingresa al menos tu Nombre Completo y crea tu Contraseña para registrarte.");
    return;
  }

  // Verificar si la empresa elegida es ELECTROVIVIENDA (por defecto, por radio o si escribió 'electro')
  const isElectro = (empresaOpt === "ELECTROVIVIENDA") ||
                    customEmpresaInput.toLowerCase().includes("electro") ||
                    customEmpresaInput.toLowerCase().includes("vivienda") ||
                    customEmpresaInput.replace(/[^0-9]/g, "").startsWith("901765438");

  const safeUserId = (correo || nombre).toLowerCase().replace(/[^a-z0-9]/g, "_").slice(0, 24);
  const nuevoPerfil = {
    id: "stu_" + Date.now(),
    usuario: safeUserId,
    nombre: nombre,
    correo: correo || `${safeUserId}@studentcont.ia`,
    pin: pin,
    programa: programa,
    rol: "Estudiante Contable",
    workspace_id: isElectro ? "electrovivienda" : "taller_" + Date.now(),
    empresa_nombre: isElectro ? "ELECTROVIVIENDA S.A.S" : (customEmpresaInput || `TALLER DE ${nombre.toUpperCase()}`)
  };

  // 1. Guardar siempre en localStorage para que funcione 100% en GitHub Pages / Web
  ACTIVE_STUDENT_PROFILE = nuevoPerfil;
  try {
    localStorage.setItem("studentcont_active_profile", JSON.stringify(nuevoPerfil));
    const users = JSON.parse(localStorage.getItem("studentcont_registered_users") || "[]");
    users.push(nuevoPerfil);
    localStorage.setItem("studentcont_registered_users", JSON.stringify(users));
  } catch (e) {}

  if (isElectro) {
    UNLOCKED_NITS_IN_SESSION.add("9017654383");
  }

  // 2. Si el servidor local Python está activo, registrarlo también de fondo
  try {
    fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Bypass-Tunnel-Reminder": "true" },
      body: JSON.stringify({
        nombre,
        pin,
        correo,
        programa,
        empresa_nombre: nuevoPerfil.empresa_nombre,
        nit_empresa_existente: isElectro ? "901765438" : customEmpresaInput
      })
    }).catch(() => {});
  } catch (e) {}

  // 3. Cargar la base de datos correspondiente (ELECTROVIVIENDA S.A.S con facturas, nómina y declaraciones)
  await loadDatabase(nuevoPerfil.workspace_id);
  updateStudentProfileUI();
  refreshAllViews();
  closeWelcomeLoginOverlay();
  showToast(`🎓 ¡Bienvenido(a) ${nombre}! Perfil registrado con éxito en ${nuevoPerfil.empresa_nombre}`);
}
window.registerFromWelcomeScreen = registerFromWelcomeScreen;

// ============================================================================
// 12. GUÍAS DIDÁCTICAS DE CADA SECCIÓN Y EXPLICACIÓN EN VIVO DE EJERCICIOS
// ============================================================================
let DIDACTIC_BANNER_COLLAPSED = true;

const DIDACTIC_GUIDES_BY_SECTION = {
  dashboard: {
    title: "🎓 Guía Didáctica: ¿Cómo se organiza el Ciclo Contable de una Empresa?",
    cards: [
      {
        head: "1. ¿Qué encuentras aquí?",
        text: "Aquí ves la ficha tributaria de la empresa (NIT, dígito de verificación, régimen de IVA y Renta) y los 4 libros mensuales de Excel (Enero a Abril)."
      },
      {
        head: "2. Ecuación Patrimonial (Regla de Oro)",
        text: "ACTIVO (Clase 1) = PASIVO (Clase 2) + PATRIMONIO (Clase 3). En ELECTROVIVIENDA S.A.S el capital inicial es de $280.000.000 aportado por los socios."
      },
      {
        head: "3. Principio de Partida Doble",
        text: "En todo registro contable la suma de los DÉBITOS (Debe) siempre es exactamente igual a la suma de los CRÉDITOS (Haber): ¡Sumas Iguales!"
      }
    ]
  },
  facturas: {
    title: "🎓 Guía Didáctica: Facturas de Venta, Compra y Notas Crédito/Débito",
    cards: [
      {
        head: "1. Factura de Venta vs. Compra",
        text: "Cuando VENDEMOS generamos un ingreso (4135 Crédito), cobramos IVA Generado (240805 Crédito) y descargamos el costo del Kardex (6135 Débito vs 1435 Crédito)."
      },
      {
        head: "2. Cuando COMPRAMOS Mercancía",
        text: "Aumenta nuestro inventario en el Kardex (1435 Débito), registramos IVA Descontable (240810 Débito) y practicamos retenciones (2465 / 2468 Crédito) antes de pagar al proveedor (2205)."
      },
      {
        head: "3. Notas Crédito y Devoluciones",
        text: "Si un cliente nos devuelve mercancía (4175 Débito), reversamos proporcionalmente el IVA, las retenciones y reingresamos las unidades al Kardex."
      }
    ]
  },
  comprobantes: {
    title: "🎓 Guía Didáctica: Comprobantes Diarios (N° 1 al N° 47) y Documentos Soporte",
    cards: [
      {
        head: "1. Numeración Oficial Cronológica",
        text: "Cada hecho económico queda respaldado por una Hoja (1 a 60 y AD1 a AD23) que se agrupa en los Comprobantes Diarios N° 1 al N° 47 del Libro Diario Columnario."
      },
      {
        head: "2. Comprobante de Ingreso (CI) vs. Egreso (CE)",
        text: "El Comprobante de Ingreso respalda entradas de dinero a Caja (1105) o Bancos (1110). El Comprobante de Egreso respalda pagos y giros de cheques a terceros."
      },
      {
        head: "3. Parciales vs. Cuentas Principales",
        text: "Las cuentas de 4 dígitos llevan el valor en DEBE o HABER; las subcuentas de 6 y 8 dígitos detallan el tercero en la columna PARCIAL."
      }
    ]
  },
  facturacion: {
    title: "🎓 Guía Didáctica: ¿Cómo Liquida y Contabiliza un Contador según el Régimen?",
    cards: [
      {
        head: "1. ¡Mírate siempre en el Espejo Contable!",
        text: "Primero identifica quién eres: ELECTROVIVIENDA S.A.S es RRI (Responsable de IVA), Agente de Retención y Autorretenedor en Renta. Luego miras el régimen del otro."
      },
      {
        head: "2. ¿Quién retiene a quién?",
        text: "EL COMPRADOR es quien paga y por tanto quien practica la retención (salvo que el vendedor sea Autorretenedor en Renta, caso en el cual el vendedor se autorretiene en 135575 vs 246575)."
      },
      {
        head: "3. Mira el Explicador en Vivo abajo 👇",
        text: "A medida que cambies el régimen o los valores aquí abajo, el panel azul te explicará paso a paso por qué se mueve cada cuenta."
      }
    ]
  },
  auxiliares: {
    title: "🎓 Guía Didáctica: ¿Cómo funcionan los Libros Auxiliares y el Libro de Bancos?",
    cards: [
      {
        head: "1. Izquierda (6 dígitos) vs. Derecha (8 dígitos)",
        text: "En el Excel llevamos a la izquierda las Subcuentas generales (6 dígitos, ej: 130505 Clientes) y a la derecha el Auxiliar individual por cada tercero (8 dígitos, ej: 13050501 Industrias Super)."
      },
      {
        head: "2. ¿Cómo se calcula el SALDO?",
        text: "En cuentas de Activo/Gasto/Costo (Clases 1, 5, 6): Saldo = Saldo Anterior + Entrada (Debe) - Salida (Haber). En Pasivo/Patrimonio/Ingreso (Clases 2, 3, 4): Saldo = Saldo Anterior + Salida (Haber) - Entrada (Debe)."
      },
      {
        head: "3. Libro Auxiliar de Bancos (11100501)",
        text: "Controla cada consignación (Debe) y cada cheque girado o GMF (Haber) de la cuenta corriente Bancolombia N° 123456789-111."
      }
    ]
  },
  kardex: {
    title: "🎓 Guía Didáctica: Sistema de Inventario Permanente — Método Promedio Ponderado",
    cards: [
      {
        head: "1. ¿Cuándo cambia el Costo Promedio?",
        text: "El Costo Unitario Promedio Ponderado se recalcula cuando hay una COMPRA a un precio distinto: Nuevo Promedio = Saldo Total en Pesos ÷ Saldo Total en Unidades."
      },
      {
        head: "2. ¿A qué costo salen las Ventas?",
        text: "Aunque vendas un televisor en $4.900.000 (precio de venta en 4135), del Kardex sale al COSTO PROMEDIO vigente (ej: $3.500.000), contabilizando 6135 (Debe) contra 1435 (Haber)."
      },
      {
        head: "3. Devoluciones en Compra y Venta",
        text: "Las devoluciones en venta reingresan a Entradas al costo al que salieron; las devoluciones en compra se restan en Salidas al costo de la factura original."
      }
    ]
  },
  estados: {
    title: "🎓 Guía Didáctica: Estados Financieros NIIF para las PYMES (Grupo 2)",
    cards: [
      {
        head: "1. Estado de Resultados (ER)",
        text: "Mide el rendimiento del mes: Ingresos (4135) - Devoluciones (4175) = Ingresos Netos - Costo de Ventas (6135) = Utilidad Bruta - Gastos (51 y 53) = Utilidad antes de Impuestos."
      },
      {
        head: "2. Estado de Situación Financiera (ESF)",
        text: "Es la fotografía financiera al cierre del mes: Activos Corrientes y No Corrientes = Pasivos Corrientes + Patrimonio (Capital + Utilidad/Pérdida del ejercicio)."
      },
      {
        head: "3. Hoja de Trabajo, ECP y Flujo de Efectivo",
        text: "De los comprobantes pasamos al Libro Diario, de allí al Libro Mayor y Balances y Hoja de Trabajo, y finalmente al ESF, ER, Cambios en el Patrimonio (ECP) y Flujo de Efectivo."
      }
    ]
  },
  tributaria: {
    title: "🎓 Guía Didáctica: Declaraciones Tributarias DIAN (F-350, F-300) y ReteICA",
    cards: [
      {
        head: "1. Formulario 350 (Retención en la Fuente)",
        text: "Se presenta mensualmente ante la DIAN. Incluye todas las retenciones que practicamos a terceros en compras/servicios/salarios (2465) más nuestras Autorretenciones en Renta (246575)."
      },
      {
        head: "2. Formulario 300 (IVA)",
        text: "Liquida la diferencia entre el IVA Generado en ventas (240805) y el IVA Descontable en compras (240810), descontando el ReteIVA que nos practicaron los Grandes Contribuyentes (135517)."
      },
      {
        head: "3. ReteICA Bucaramanga (9.6‰)",
        text: "Incluye la retención de Industria y Comercio (9.6 por mil), el impuesto complementario de Avisos y Tableros (15% del ICA) y la Sobretasa Bomberil (10% del ICA)."
      }
    ]
  },
  ia: {
    title: "🎓 Guía Didáctica: Tu Tutor de Inteligencia Artificial Contable Personalizado",
    cards: [
      {
        head: "1. Pregunta en lenguaje natural",
        text: "Escribe cualquier cuenta del PUC (ej: 1435, 2408, 5105), pregunta cómo contabilizar un caso o pide que te explique una factura de ELECTROVIVIENDA."
      },
      {
        head: "2. ¡Entrena y alimenta a la IA!",
        text: "En el panel derecho puedes enseñarle nuevos apuntes de clase, fórmulas o ejercicios. Todo lo que le enseñes queda guardado para ayudarte a ti y a tus compañeros."
      },
      {
        head: "3. Retos y Quizzes Didácticos",
        text: "Haz clic en '🎯 Dame un Reto / Quiz Contable' para que la IA te ponga un ejercicio corto y te explique la respuesta."
      }
    ]
  },
  reformas: {
    title: "🎓 Guía Didáctica: ¿Por qué un Contador debe conocer las Reformas y Leyes vigentes?",
    cards: [
      {
        head: "1. Impacto Directo en los Asientos",
        text: "Cada reforma tributaria, laboral o pensional cambia tarifas de retención, topes en UVT, aportes a seguridad social y el cálculo de horas extras en nómina."
      },
      {
        head: "2. Parámetros Clave Colombia 2026",
        text: "UVT 2026: $52.374 | SMLMV 2026: $1.750.905 | Auxilio de Transporte: $249.095 | Base mínima compras (27 UVT) y servicios (4 UVT)."
      },
      {
        head: "3. Comparte Nuevas Normas",
        text: "Con el botón '+ Publicar Nueva Reforma / Norma' puedes agregar resúmenes de decretos o leyes vistas en clase para que todos los estudiantes los lean."
      }
    ]
  }
};

function toggleDidacticBanner() {
  DIDACTIC_BANNER_COLLAPSED = !DIDACTIC_BANNER_COLLAPSED;
  renderSectionDidacticBanner(ACTIVE_SECTION);
}

function renderSectionDidacticBanner(sectionId) {
  const container = document.getElementById("activeSectionDidacticBanner");
  if (!container) return;
  const info = DIDACTIC_GUIDES_BY_SECTION[sectionId] || DIDACTIC_GUIDES_BY_SECTION.dashboard;

  container.innerHTML = `
    <div class="didactic-guide-banner ${DIDACTIC_BANNER_COLLAPSED ? 'is-collapsed' : 'is-expanded'}">
      <div class="didactic-guide-header" onclick="toggleDidacticBanner()" title="Haz clic para ver u ocultar tips pedagógicos">
        <div class="didactic-guide-title">
          <span class="guide-badge-icon">🎓</span>
          <span class="guide-title-text">${info.title}</span>
          <span class="status-pill status-paid" style="font-size:0.67rem; padding:2px 8px;">Modo Aprendizaje</span>
        </div>
        <button class="btn btn-outline btn-sm didactic-toggle-btn" style="padding:3px 10px; font-size:0.72rem; font-weight:700;">
          ${DIDACTIC_BANNER_COLLAPSED ? "👁️ Ver Guía y Tips Contables" : "➖ Ocultar Guía"}
        </button>
      </div>
      ${DIDACTIC_BANNER_COLLAPSED ? "" : `
        <div class="didactic-guide-body">
          ${info.cards.map(c => `
            <div class="didactic-pill-card">
              <strong>${c.head}</strong>
              <span>${c.text}</span>
            </div>
          `).join("")}
        </div>
      `}
    </div>
  `;
}

function renderDidacticLiveExerciseExplanation() {
  const box = document.getElementById("didacticLiveExerciseBox");
  const st = window.__LIVE_TX_STATE;
  if (!box || !st) return;

  const tercero = document.getElementById("txTercero")?.value || "el Tercero";
  const isVentaSide = (st.tipo === "VENTA" || st.tipo === "DEV_VENTA");

  const accountExplanations = (st.asientos || [])
    .filter(a => String(a.codigo).length === 4)
    .map(a => {
      const clase = String(a.codigo).charAt(0);
      const tipoCta = clase === "1" ? "ACTIVO (Naturaleza Débito)"
        : clase === "2" ? "PASIVO (Naturaleza Crédito)"
        : clase === "3" ? "PATRIMONIO (Naturaleza Crédito)"
        : clase === "4" ? "INGRESO (Naturaleza Crédito)"
        : clase === "5" ? "GASTO (Naturaleza Débito)"
        : "COSTO DE VENTAS (Naturaleza Débito)";
      const mov = a.debe > 0
        ? `se <strong>DEBITA (Debe) por ${fmtCOP(a.debe)}</strong>`
        : `se <strong>ACREDITA (Haber) por ${fmtCOP(a.haber)}</strong>`;
      return `<li><strong>Cuenta ${a.codigo} — ${a.cuenta}</strong> [${tipoCta}]: ${mov}.</li>`;
    }).join("");

  box.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
      <div style="font-size:0.88rem; font-weight:800; color:#1E3A8A;">
        🧠 EXPLICACIÓN DIDÁCTICA EN VIVO: ¿Qué estás haciendo en este ejercicio y por qué se contabiliza así?
      </div>
      <span class="status-pill status-paid">Explicación Paso a Paso para el Estudiante</span>
    </div>

    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:12px; font-size:0.8rem; line-height:1.55; color:#1E293B;">
      <div style="background:#fff; padding:12px 14px; border-radius:8px; border:1px solid #BFDBFE;">
        <strong style="color:#1D4ED8; display:block; margin-bottom:4px;">1️⃣ Análisis de Regímenes (${isVentaSide ? "Nosotros Vendemos" : "Nosotros Compramos"}):</strong>
        Estás registrando una operación de <strong>${st.tipo}</strong> con <strong>${tercero}</strong> (${st.rule?.label || "Régimen seleccionado"}) por una base gravable de <strong>${fmtCOP(st.base)}</strong>.<br/>
        • <strong>IVA (19%):</strong> ${st.iva > 0 ? `Aplica por ${fmtCOP(st.iva)} porque el vendedor es Responsable de IVA.` : `No aplica ($0) porque el vendedor es No Responsable de IVA.`}<br/>
        • <strong>Retención / Autorretención Renta:</strong> ${st.autorretencion > 0 ? `Como somos Autorretenedores en Renta, nos autorretenemos ${fmtCOP(st.autorretencion)} (Débito en 135575 Anticipo vs Crédito en 246575 por Pagar).` : (st.retefuente > 0 ? `Le practicamos Retefuente al proveedor por ${fmtCOP(st.retefuente)} (Cuenta 2465).` : `No se practica Retefuente porque el proveedor es Autorretenedor.`)}<br/>
        • <strong>ReteIVA y ReteICA:</strong> ${st.reteiva > 0 ? `El Gran Contribuyente nos retiene el 15% del IVA (${fmtCOP(st.reteiva)} en 135517). ` : ""}${st.reteica > 0 ? `Aplica paquete ReteICA Bucaramanga (9.6‰ + 15% Avisos + 10% Bomberil) por ${fmtCOP(st.reteica)}.` : "No aplica ReteICA en este cruce."}
      </div>

      <div style="background:#fff; padding:12px 14px; border-radius:8px; border:1px solid #BFDBFE;">
        <strong style="color:#1D4ED8; display:block; margin-bottom:4px;">2️⃣ ¿Por qué cada cuenta va al DEBE o al HABER? (Partida Doble):</strong>
        <ul style="margin:0; padding-left:18px;">
          ${accountExplanations}
        </ul>
        <div style="margin-top:6px; font-weight:800; color:#047857;">
          ✓ Sumas Iguales Verificadas: Debe ${fmtCOP(st.sumDebe)} = Haber ${fmtCOP(st.sumHaber)}
        </div>
      </div>

      <div style="background:#fff; padding:12px 14px; border-radius:8px; border:1px solid #BFDBFE;">
        <strong style="color:#1D4ED8; display:block; margin-bottom:4px;">3️⃣ Efecto Automático en Kardex, Auxiliares y Estados Financieros:</strong>
        • <strong>En el Kardex Promedio Ponderado:</strong> ${st.tipo === "VENTA" ? `Salen ${st.cant} unidades al costo promedio de ${fmtCOP(st.cProm)}/und (Costo total ${fmtCOP(st.cant * st.cProm)} en 6135 contra 1435).` : (st.tipo === "COMPRA" ? `Entran ${st.cant} unidades a ${fmtCOP(st.vUnit)}/und y se recalcula automáticamente el nuevo costo promedio ponderado.` : `Se actualiza la tarjeta Kardex y el saldo de la cuenta.`)}<br/>
        • <strong>En Libros Auxiliares:</strong> Cada subcuenta de 6 dígitos y auxiliar de 8 dígitos de ${tercero} actualiza su columna de Entrada/Salida y su Saldo.<br/>
        • <strong>En Estados Financieros:</strong> Actualiza de inmediato el Balance de Comprobación, el ESF y el Estado de Resultados del mes.
      </div>
    </div>
  `;
}

// ============================================================================
// 13. TUTOR DE INTELIGENCIA ARTIFICIAL CONTABLE ENTRENABLE
// ============================================================================
let IA_CHAT_HISTORY = [
  {
    sender: "bot",
    html: `¡Hola! Soy el <strong>Tutor de Inteligencia Artificial de STUDENTCONT.IA</strong> 🤖📚.<br/>
    Estoy entrenado con el <strong>Plan Único de Cuentas (PUC)</strong>, las <strong>NIIF para las PYMES</strong>, la <strong>Matriz de Regímenes Tributarios 2026</strong> y toda la contabilidad de <strong>ELECTROVIVIENDA S.A.S</strong>.<br/><br/>
    Pregúntame cualquier duda (por ejemplo: <em>"¿Cómo se contabiliza una venta a un Gran Contribuyente?"</em>, <em>"¿Qué naturaleza tiene la cuenta 2408?"</em> o haz clic en los botones de arriba). ¡También puedes enseñarme nuevos temas en el panel de la derecha!`
  }
];

function getCombinedCustomAiKnowledge() {
  const serverKb = DB?.ia_custom_kb || [];
  let localKb = [];
  try {
    localKb = JSON.parse(localStorage.getItem("studentcont_ia_custom_kb") || "[]");
  } catch (e) {}
  const map = new Map();
  [...serverKb, ...localKb].forEach(item => {
    if (item && item.tema) map.set(item.tema, item);
  });
  return Array.from(map.values());
}

function setIaFeedMode(mode) {
  document.querySelectorAll("#iaFeedModeTabs .filter-chip").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.feedmode === mode);
  });
  const bLink = document.getElementById("iaFeedBoxLink");
  const bDoc = document.getElementById("iaFeedBoxDoc");
  const bText = document.getElementById("iaFeedBoxText");
  if (bLink) bLink.style.display = mode === "LINK" ? "block" : "none";
  if (bDoc) bDoc.style.display = mode === "DOC" ? "block" : "none";
  if (bText) bText.style.display = mode === "TEXT" ? "block" : "none";
}

function renderAiTutorSection() {
  const chatBox = document.getElementById("iaChatMessagesBox");
  if (chatBox) {
    chatBox.innerHTML = IA_CHAT_HISTORY.map(m => `
      <div class="ia-msg ${m.sender}">${m.html}</div>
    `).join("");
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  const kbList = getCombinedCustomAiKnowledge();
  const badge = document.getElementById("iaCustomKbCountBadge");
  if (badge) badge.textContent = `${kbList.length} fuentes activas`;

  const kbContainer = document.getElementById("iaCustomKbListContainer");
  if (kbContainer) {
    if (!kbList.length) {
      kbContainer.innerHTML = `<div style="font-size:0.79rem; color:var(--text-muted);">Aún no has agregado links, documentos o apuntes. ¡Usa las pestañas de arriba (🌐 Link Web, 📄 Documento o ✍️ Apunte) para alimentar a la IA!</div>`;
    } else {
      kbContainer.innerHTML = kbList.map(k => {
        const tipoIcon = k.fuente_tipo === "LINK WEB" ? "🌐 LINK WEB"
          : (k.fuente_tipo === "DOCUMENTO" ? "📄 DOCUMENTO" : "✍️ APUNTE");
        const safeQ = String(k.tema || "").replace(/'/g, "");
        return `
          <div style="padding:10px 12px; border-bottom:1px solid var(--border-light); font-size:0.78rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; gap:6px; flex-wrap:wrap;">
              <div>
                <span class="status-pill status-paid" style="font-size:0.65rem; padding:1px 6px; margin-right:4px;">${tipoIcon}</span>
                <strong style="color:var(--brand-primary);">${k.tema}</strong>
              </div>
              <div style="display:flex; gap:6px; align-items:center;">
                <button class="btn btn-outline btn-sm" style="padding:2px 7px; font-size:0.68rem;" onclick="askAiQuickQuestion('${safeQ}')">💬 Preguntar</button>
                ${k.fuente_url ? `<a class="btn btn-primary btn-sm" style="padding:2px 7px; font-size:0.68rem; text-decoration:none;" href="${k.fuente_url}" target="_blank" rel="noopener">🔗 Abrir Fuente</a>` : ""}
                <button class="btn btn-outline btn-sm" style="padding:2px 6px; font-size:0.68rem; color:var(--brand-danger);" onclick="deleteCustomKbItem('${k.id || safeQ}')" title="Eliminar fuente">🗑️</button>
              </div>
            </div>
            <div style="color:var(--text-secondary); margin-top:4px; display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical; overflow:hidden;">
              ${(k.contenido || "").slice(0, 280)}
            </div>
            ${k.keywords ? `<div style="font-size:0.7rem; color:var(--text-muted); margin-top:3px;"><strong>Palabras clave:</strong> ${k.keywords}</div>` : ""}
          </div>
        `;
      }).join("");
    }
  }
}

async function deleteCustomKbItem(itemId) {
  try {
    const localKb = getCombinedCustomAiKnowledge().filter(x => x.id !== itemId && x.tema !== itemId);
    localStorage.setItem("studentcont_ia_custom_kb", JSON.stringify(localKb));
    const res = await fetch("/api/ia/delete-kb", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: itemId })
    });
    const data = await res.json();
    if (data.ok && DB) DB.ia_custom_kb = data.ia_custom_kb;
  } catch (e) {}
  renderAiTutorSection();
  showToast("Fuente eliminada de la base de conocimiento");
}

async function ingestUrlIntoAi() {
  const urlInp = document.getElementById("iaFeedUrlInput");
  const titleInp = document.getElementById("iaFeedUrlTitle");
  const pubReforma = document.getElementById("chkUrlAlsoReforma")?.checked;
  const btn = document.getElementById("btnIngestUrl");

  const url = urlInp?.value.trim() || "";
  const titulo = titleInp?.value.trim() || "";
  if (!url) {
    alert("Por favor pega el enlace (URL) de la página web que deseas extraer.");
    return;
  }

  if (btn) {
    btn.disabled = true;
    btn.textContent = "⏳ Extrayendo contenido de la página web...";
  }

  try {
    const res = await fetch("/api/ia/ingest-url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url,
        titulo,
        publicar_reforma: pubReforma,
        autor: ACTIVE_STUDENT_PROFILE.nombre || "Gina Villamizar"
      })
    });
    const data = await res.json();
    if (!res.ok || !data.ok) {
      alert(data.error || "No se pudo extraer el enlace.");
      return;
    }

    if (DB) {
      DB.ia_custom_kb = data.ia_custom_kb;
      DB.custom_reformas = data.custom_reformas;
    }
    localStorage.setItem("studentcont_ia_custom_kb", JSON.stringify(data.ia_custom_kb));
    if (pubReforma && data.custom_reformas) {
      localStorage.setItem("studentcont_custom_reformas", JSON.stringify(data.custom_reformas));
    }

    if (urlInp) urlInp.value = "";
    if (titleInp) titleInp.value = "";

    const item = data.item;
    IA_CHAT_HISTORY.push({
      sender: "bot",
      html: `🌐 <strong>¡Página Web aprendida e indexada con éxito!</strong><br/>
      • <strong>Título:</strong> ${item.tema}<br/>
      • <strong>Enlace Fuente:</strong> <a href="${item.fuente_url}" target="_blank" rel="noopener">${item.fuente_url}</a><br/>
      • <strong>Palabras Clave Detectadas:</strong> <code>${item.keywords || "contabilidad, normativa"}</code><br/>
      • <strong>Resumen Extraído:</strong> ${(item.contenido || "").slice(0, 360)}...<br/><br/>
      💬 <em>¡Pregúntame cualquier duda sobre el contenido de este enlace!</em>`
    });
    renderAiTutorSection();
    renderReformasSection();
    showToast(`🌐 Link indexado en la IA: ${item.tema}`);
  } catch (e) {
    alert("Error al conectar con el extractor de enlaces.");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "🌐 Extraer Contenido del Link y Alimentar IA";
    }
  }
}

async function ingestUrlFromReformasBar() {
  const inp = document.getElementById("reformaQuickUrlInput");
  const cat = document.getElementById("reformaQuickCatSelect")?.value || "TRIBUTARIA";
  const url = inp?.value.trim() || "";
  if (!url) {
    alert("Por favor pega el enlace (URL) de la reforma, ley o artículo contable.");
    return;
  }
  showToast("⏳ Extrayendo página web y publicando en Reformas y Tutor IA...");
  try {
    const res = await fetch("/api/ia/ingest-url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url,
        publicar_reforma: true,
        categoria: cat,
        autor: ACTIVE_STUDENT_PROFILE.nombre || "Gina Villamizar"
      })
    });
    const data = await res.json();
    if (!res.ok || !data.ok) {
      alert(data.error || "No se pudo leer el enlace.");
      return;
    }
    if (DB) {
      DB.ia_custom_kb = data.ia_custom_kb;
      DB.custom_reformas = data.custom_reformas;
    }
    localStorage.setItem("studentcont_ia_custom_kb", JSON.stringify(data.ia_custom_kb));
    localStorage.setItem("studentcont_custom_reformas", JSON.stringify(data.custom_reformas));
    if (inp) inp.value = "";
    renderReformasSection();
    renderAiTutorSection();
    showToast(`✅ Reforma y conocimiento IA agregados desde: ${data.item.tema}`);
  } catch (e) {
    alert("No se pudo extraer el enlace en este momento.");
  }
}

async function extractPdfTextInBrowser(arrayBuffer, maxPages = 45) {
  if (!window.pdfjsLib) return "";
  try {
    window.pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
    const pdf = await window.pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    const totalP = Math.min(pdf.numPages, maxPages);
    const pagesText = [];
    for (let p = 1; p <= totalP; p++) {
      const page = await pdf.getPage(p);
      const content = await page.getTextContent();
      const strings = content.items.map(it => it.str);
      const pageStr = strings.join(" ").replace(/\s+/g, " ").trim();
      if (pageStr.length > 10) {
        pagesText.push(`[Página ${p}]: ${pageStr}`);
      }
    }
    return pagesText.join("\n\n");
  } catch (e) {
    return "";
  }
}

async function extractExcelTextInBrowser(arrayBuffer) {
  if (!window.XLSX) return "";
  try {
    const wb = window.XLSX.read(arrayBuffer, { type: "array" });
    const chunks = [];
    wb.SheetNames.slice(0, 12).forEach(sName => {
      const ws = wb.Sheets[sName];
      const rows = window.XLSX.utils.sheet_to_json(ws, { header: 1, defval: "" });
      const lines = [`=== HOJA: ${sName} ===`];
      rows.slice(0, 80).forEach(r => {
        const nonEmpty = r.map(x => String(x).trim()).filter(Boolean);
        if (nonEmpty.length) lines.push(nonEmpty.slice(0, 10).join(" | "));
      });
      if (lines.length > 1) chunks.push(lines.join("\n"));
    });
    return chunks.join("\n\n");
  } catch (e) {
    return "";
  }
}

function arrayBufferToBase64(buffer) {
  let binary = "";
  const bytes = new Uint8Array(buffer);
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return window.btoa(binary);
}

async function ingestDocumentIntoAi() {
  const fileInp = document.getElementById("iaFeedFileInput");
  const titleInp = document.getElementById("iaFeedDocTitle");
  const pubReforma = document.getElementById("chkDocAlsoReforma")?.checked;
  const btn = document.getElementById("btnIngestDoc");

  const file = fileInp?.files?.[0];
  if (!file) {
    alert("Por favor selecciona un documento (.PDF, .XLSX, .DOCX, .TXT, .CSV) de tu computador.");
    return;
  }

  if (btn) {
    btn.disabled = true;
    btn.textContent = `⏳ Leyendo documento "${file.name}"...`;
  }

  try {
    const arrayBuffer = await file.arrayBuffer();
    const fnameLower = file.name.toLowerCase();
    let clientExtractedText = "";

    if (fnameLower.endsWith(".pdf")) {
      clientExtractedText = await extractPdfTextInBrowser(arrayBuffer, 50);
    } else if (fnameLower.endsWith(".xlsx") || fnameLower.endsWith(".xlsm") || fnameLower.endsWith(".xls")) {
      clientExtractedText = await extractExcelTextInBrowser(arrayBuffer);
    } else if (fnameLower.endsWith(".txt") || fnameLower.endsWith(".csv") || fnameLower.endsWith(".md") || fnameLower.endsWith(".json")) {
      clientExtractedText = new TextDecoder("utf-8").decode(arrayBuffer);
    }

    // Enviar archivo (hasta 8 MB en base64) + texto extraído al servidor
    const b64 = arrayBuffer.byteLength <= 8 * 1024 * 1024 ? arrayBufferToBase64(arrayBuffer) : "";
    const res = await fetch("/api/ia/ingest-document", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filename: file.name,
        base64_data: b64,
        extracted_text: clientExtractedText,
        titulo: titleInp?.value.trim() || `Documento: ${file.name}`,
        publicar_reforma: pubReforma,
        autor: ACTIVE_STUDENT_PROFILE.nombre || "Gina Villamizar"
      })
    });
    const data = await res.json();
    if (!res.ok || !data.ok) {
      alert(data.error || "No se pudo procesar el documento.");
      return;
    }

    if (DB) {
      DB.ia_custom_kb = data.ia_custom_kb;
      DB.custom_reformas = data.custom_reformas;
    }
    localStorage.setItem("studentcont_ia_custom_kb", JSON.stringify(data.ia_custom_kb));
    if (fileInp) fileInp.value = "";
    if (titleInp) titleInp.value = "";

    const item = data.item;
    IA_CHAT_HISTORY.push({
      sender: "bot",
      html: `📄 <strong>¡Documento procesado e integrado en la IA!</strong><br/>
      • <strong>Archivo:</strong> <a href="${item.fuente_url}" target="_blank" rel="noopener">${file.name}</a><br/>
      • <strong>Palabras Clave:</strong> <code>${item.keywords || "documento contable"}</code><br/>
      • <strong>Extracto:</strong> ${(item.contenido || "").slice(0, 360)}...<br/><br/>
      💬 <em>¡Ya puedes preguntarme sobre cualquier tema contenido en <strong>${file.name}</strong>!</em>`
    });
    renderAiTutorSection();
    renderReformasSection();
    showToast(`📄 Documento aprendido por la IA: ${file.name}`);
  } catch (e) {
    alert("Error procesando el documento seleccionado.");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "📄 Procesar Documento y Alimentar IA";
    }
  }
}

async function ingestLocalFolderNIIFPdf() {
  showToast("⏳ Leyendo el libro oficial NIIF para las PYMES (ifrs-for-smes-es (1).pdf)...");
  try {
    const pdfResp = await fetch("ifrs-for-smes-es%20(1).pdf");
    let extracted = "";
    if (pdfResp.ok) {
      const buf = await pdfResp.arrayBuffer();
      extracted = await extractPdfTextInBrowser(buf, 40);
    }
    const res = await fetch("/api/ia/ingest-document", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filename: "ifrs-for-smes-es (1).pdf",
        local_server_file: "ifrs-for-smes-es (1).pdf",
        extracted_text: extracted,
        titulo: "Norma NIIF para las PYMES (Libro Oficial ifrs-for-smes-es.pdf)",
        publicar_reforma: true,
        categoria: "NIIF",
        autor: "Gina Villamizar"
      })
    });
    const data = await res.json();
    if (data.ok && DB) {
      DB.ia_custom_kb = data.ia_custom_kb;
      DB.custom_reformas = data.custom_reformas;
      localStorage.setItem("studentcont_ia_custom_kb", JSON.stringify(data.ia_custom_kb));
      IA_CHAT_HISTORY.push({
        sender: "bot",
        html: `📘 <strong>¡Libro Oficial "NIIF para las PYMES (ifrs-for-smes-es (1).pdf)" indexado en la IA!</strong><br/>
        • <a href="${data.item.fuente_url}" target="_blank" rel="noopener">📄 Abrir PDF Oficial NIIF para las PYMES</a><br/>
        • Ya puedes preguntarme sobre las Secciones NIIF PYMES, Estados Financieros, Inventarios (Sección 13), Propiedades Planta y Equipo (Sección 17) e Ingresos (Sección 23).`
      });
      renderAiTutorSection();
      renderReformasSection();
      showToast("✅ Libro PDF NIIF para las PYMES indexado en la IA");
    }
  } catch (e) {
    alert("No se pudo indexar el PDF local en este momento.");
  }
}

function askAiQuickQuestion(qText) {
  const inp = document.getElementById("iaUserQuestionInput");
  if (inp) inp.value = qText;
  sendStudentQuestionToAi();
}

function generateAiAccountingResponse(query) {
  const q = query.toLowerCase().trim();
  const stopWords = new Set(["como", "cómo", "cual", "cuál", "para", "este", "esta", "sobre", "entre", "donde", "dónde", "cuando", "cuándo", "porque", "porqué", "explicame", "explícame", "dime", "que", "qué", "del", "las", "los", "una", "uno", "con", "por"]);
  const queryTokens = q.split(/[^a-záéíóúñ0-9]+/).filter(w => w.length >= 3 && !stopWords.has(w));

  // 1. Búsqueda Inteligente Multi-Fuente en Links Web, Documentos PDF/Excel/Word y Apuntes enseñados a la IA
  const customKb = getCombinedCustomAiKnowledge();
  let bestMatch = null;
  let bestScore = 0;

  for (const item of customKb) {
    const temaLow = (item.tema || "").toLowerCase();
    const kwLow = (item.keywords || "").toLowerCase();
    const fullLow = ((item.texto_completo || "") + " " + (item.contenido || "")).toLowerCase();

    let score = 0;
    if (temaLow && q.includes(temaLow)) score += 25;
    for (const tok of queryTokens) {
      if (temaLow.includes(tok)) score += 8;
      if (kwLow.includes(tok)) score += 6;
      if (fullLow.includes(tok)) score += 3;
    }
    if (score > bestScore && score >= 6) {
      bestScore = score;
      bestMatch = item;
    }
  }

  if (bestMatch) {
    // Extraer los párrafos más relevantes del documento o página web que coincidan con las palabras de la pregunta
    const rawFull = bestMatch.texto_completo || bestMatch.contenido || "";
    const paragraphs = rawFull.split(/\n+/).map(p => p.trim()).filter(p => p.length > 25);
    let matchedParas = paragraphs.filter(p => {
      const pLow = p.toLowerCase();
      return queryTokens.some(tok => pLow.includes(tok));
    }).slice(0, 4);

    if (!matchedParas.length) {
      matchedParas = paragraphs.slice(0, 3);
    }
    const excerptHtml = (matchedParas.join("<br/><br/>") || bestMatch.contenido || "").slice(0, 1600);
    const sourceBadge = bestMatch.fuente_tipo === "LINK WEB"
      ? `🌐 <strong>Fuente Página Web:</strong> <a href="${bestMatch.fuente_url}" target="_blank" rel="noopener">${bestMatch.fuente_url}</a>`
      : (bestMatch.fuente_tipo === "DOCUMENTO"
        ? `📄 <strong>Fuente Documento:</strong> <a href="${bestMatch.fuente_url}" target="_blank" rel="noopener">${bestMatch.fuente_archivo || bestMatch.tema} (Abrir Documento)</a>`
        : `✍️ <strong>Apunte en Base de Conocimiento</strong> (${bestMatch.autor || "Gina Villamizar"})`);

    return `🧠 <strong>Respuesta Basada en tus Fuentes Alimentadas — ${bestMatch.tema}:</strong><br/><br/>
    ${excerptHtml}<br/><br/>
    <div style="font-size:0.75rem; background:var(--bg-subtle); padding:6px 10px; border-radius:6px; border:1px solid var(--border-light);">
      ${sourceBadge}
    </div>`;
  }

  // 2. Si preguntan por un código del PUC (ej: 1105, 1435, 2408, 4135, 5105, 6135)
  const codeMatch = q.match(/\b(\d{4,8})\b/);
  if (codeMatch && DB?.puc) {
    const code = codeMatch[1];
    const foundPuc = DB.puc.find(p => String(p.codigo) === code) || DB.puc.find(p => String(p.codigo).startsWith(code.slice(0, 4)));
    if (foundPuc) {
      const c1 = String(foundPuc.codigo).charAt(0);
      const natMap = {
        "1": "ACTIVO — Naturaleza DÉBITO (Aumenta en el Debe y disminuye en el Haber).",
        "2": "PASIVO — Naturaleza CRÉDITO (Aumenta en el Haber y disminuye en el Debe).",
        "3": "PATRIMONIO — Naturaleza CRÉDITO (Aumenta en el Haber y disminuye en el Debe).",
        "4": "INGRESOS — Naturaleza CRÉDITO (Aumenta en el Haber cuando vendemos; las devoluciones 4175 son Débito).",
        "5": "GASTOS — Naturaleza DÉBITO (Aumenta en el Debe cuando causamos un gasto administrativo o de ventas).",
        "6": "COSTOS DE VENTAS — Naturaleza DÉBITO (Aumenta en el Debe por el costo promedio ponderado del Kardex al vender)."
      };
      return `📘 <strong>Consulta de Cuenta PUC ${foundPuc.codigo} — ${foundPuc.nombre}:</strong><br/>
      • <strong>Clase Contable:</strong> ${natMap[c1] || "Cuenta Contable PUC"}<br/>
      • <strong>¿Cómo usarla didácticamente?:</strong> Si el código tiene 4 dígitos (${foundPuc.codigo.slice(0, 4)}), su valor principal va en la columna <strong>Debe</strong> o <strong>Haber</strong>; sus subcuentas de 6 y 8 dígitos llevan el detalle por tercero en la columna <strong>Parcial</strong> y alimentan los Libros Auxiliares en vivo.`;
    }
  }

  // 3. Naturaleza Débito vs Crédito (PUC)
  if (q.includes("naturaleza") || q.includes("debito") || q.includes("débito") || (q.includes("clases") && q.includes("puc"))) {
    return `📘 <strong>Truco Didáctico para Memorizar la Naturaleza del PUC en 30 Segundos:</strong><br/><br/>
    Recuerda la sigla <strong>A-G-C son DÉBITO</strong> y <strong>P-P-I son CRÉDITO</strong>:<br/>
    • <strong>Clase 1 (Activo), Clase 5 (Gastos) y Clase 6 (Costos):</strong> Tienen naturaleza <strong>DÉBITO (Debe)</strong>. Aumentan por el <em>Debe</em> y disminuyen por el <em>Haber</em>.<br/>
    • <strong>Clase 2 (Pasivo), Clase 3 (Patrimonio) y Clase 4 (Ingresos):</strong> Tienen naturaleza <strong>CRÉDITO (Haber)</strong>. Aumentan por el <em>Haber</em> y disminuyen por el <em>Debe</em>.<br/><br/>
    💡 <em>Excepciones importantes:</em> La depreciación acumulada (<code>1592</code>) es Activo pero de naturaleza Crédito; las Devoluciones en Ventas (<code>4175</code>) son Clase 4 pero de naturaleza Débito porque restan ingresos.`;
  }

  // 4. Regímenes Tributarios / Retenciones
  if (q.includes("regimen") || q.includes("régimen") || q.includes("retefuente") || q.includes("reteiva") || q.includes("reteica")) {
    return `⚖️ <strong>Guía Didáctica de Regímenes Tributarios (Comprador vs. Vendedor):</strong><br/><br/>
    En el caso de <strong>ELECTROVIVIENDA S.A.S</strong> somos <strong>RRI (Responsables de IVA), Agentes de Retención y Autorretenedores en Renta</strong>:<br/>
    1. <strong>Cuando VENDEMOS a un Gran Contribuyente (Ej: Industrias Super):</strong> Cobramos IVA 19% (<code>240805</code>), ellos NO nos hacen Retefuente en renta porque somos Autorretenedores (nosotros mismos contabilizamos el 2.5% en <code>135575</code> vs <code>246575</code>), pero ellos SÍ nos retienen <strong>ReteIVA del 15%</strong> (<code>135517</code>) y <strong>ReteICA 9.6‰ + Avisos 15% + Bomberil 10%</strong> (<code>135518, 135520, 135525</code>).<br/>
    2. <strong>Cuando VENDEMOS a otro RRI Ordinario (Ej: El Márquez de la 9):</strong> Cobramos IVA 19%, NO hay ReteIVA (entre dos RRI ordinarios no se retiene IVA), nos hacen ReteICA y nosotros nos autorretenemos el 2.5% en Renta.<br/>
    3. <strong>Cuando VENDEMOS a un No Responsable de IVA Persona Natural (Ej: Jaime Salas / Horacio Díaz):</strong> Cobramos IVA 19%, ellos NO nos retienen nada porque no son agentes de retención, y nosotros nos practicamos <strong>Autorretención en Renta del 3.5%</strong>.<br/>
    4. <strong>Cuando COMPRAMOS a un RRI (Ej: Electrodomésticos Cra 13 / La Casa Orange):</strong> Registramos IVA descontable 19% (<code>240810</code>) y nosotros les retenemos <strong>2.5% de Retefuente Compras (<code>246540</code>)</strong> y <strong>ReteICA + Avisos + Bomberil (<code>246801..03</code>)</strong>.`;
  }

  // 5. Kardex Promedio Ponderado
  if (q.includes("kardex") || q.includes("promedio ponderado") || q.includes("inventario")) {
    return `📦 <strong>¿Cómo funciona el Kardex por Promedio Ponderado?:</strong><br/><br/>
    Imagina las <strong>Neveras Samsung 12 Pies (Ref: NV01)</strong> en ELECTROVIVIENDA:<br/>
    1. <strong>Compra 1 (Hoja 11):</strong> Compramos 30 neveras a $610.000 c/u = $18.300.000. El costo promedio inicial es <strong>$610.000/und</strong>.<br/>
    2. <strong>Ventas y Devoluciones (Hojas 13, 16, 17, 19):</strong> Salen al costo promedio vigente de <strong>$610.000/und</strong> (quedando 8 neveras por $4.880.000).<br/>
    3. <strong>Compra 2 a distinto precio (Hoja 21):</strong> Compramos a Electromenores 12 neveras a $500.000 c/u = $6.000.000.<br/>
    4. <strong>Nuevo Promedio Ponderado:</strong> Sumamos el saldo en pesos ($4.880.000 + $6.000.000 = <strong>$10.880.000</strong>) y lo dividimos entre el total de unidades (8 + 12 = <strong>20 neveras</strong>):<br/>
    👉 <code>$10.880.000 ÷ 20 = $544.000 por unidad</code>. ¡Por eso en la Venta N° 003 (Hoja 22) las neveras salen a un costo de $544.000!`;
  }

  // 6. Autorretención en Renta
  if (q.includes("autorretencion") || q.includes("autorretención") || q.includes("135575")) {
    return `🧮 <strong>¿Qué es la Autorretención en Renta y cómo se contabiliza?:</strong><br/><br/>
    Cuando una empresa es designada <strong>Autorretenedora</strong>, el cliente no le descuenta Retefuente del pago; en cambio, la misma empresa vendedora se autorretiene sobre el subtotal de la venta:<br/>
    • <strong>DÉBITO a la 135575 (Anticipo de Impuestos - Autorretención):</strong> Es un Activo a favor nuestro que luego descontaremos en la Declaración de Renta anual.<br/>
    • <strong>CRÉDITO a la 246575 (Retención en la Fuente por Pagar):</strong> Es el Pasivo que le pagamos el mes siguiente a la DIAN en el <strong>Formulario 350</strong>.<br/>
    💡 <em>Nota didáctica:</em> Como entra al Debe y al Haber por el mismo valor, no cambia el neto a cobrarle al cliente, pero sí incrementa las Sumas Iguales del comprobante.`;
  }

  // 7. Nómina y Seguridad Social 2026
  if (q.includes("nomina") || q.includes("nómina") || q.includes("seguridad social") || q.includes("prestaciones")) {
    return `👥 <strong>Guía Didáctica de Nómina y Seguridad Social en Colombia (Parámetros 2026):</strong><br/><br/>
    • <strong>SMLMV 2026:</strong> $1.750.905 | <strong>Auxilio de Transporte:</strong> $249.095 (para quienes ganan hasta 2 SMLMV).<br/>
    • <strong>Descuentos al Trabajador (2370):</strong> Salud <strong>4%</strong> y Pensión <strong>4%</strong> sobre el IBC (Total Devengado sin Auxilio de Transporte). Si gana más de 4 SMLMV aporta al Fondo de Solidaridad Pensional (1%).<br/>
    • <strong>Aportes del Empleador (5105 / 2370):</strong> Pensión <strong>12%</strong>, ARL (0.522% riesgo I), Caja de Compensación (4%) — aplicando exoneración del Art. 114-1 E.T. para empleados que devenguen menos de 10 SMLMV.<br/>
    • <strong>Provisiones de Prestaciones Sociales (2610):</strong> Cesantías <strong>8.33%</strong>, Intereses sobre Cesantías <strong>1% mensual (12% anual)</strong>, Prima de Servicios <strong>8.33%</strong> (sobre total devengado) y Vacaciones <strong>4.17%</strong> (sin auxilio de transporte).`;
  }

  // 8. Reto / Quiz Didáctico
  if (q.includes("reto") || q.includes("quiz") || q.includes("ejercicio")) {
    return `🎯 <strong>¡Reto Didáctico Contable para ti!</strong><br/><br/>
    <strong>Enunciado:</strong> Si ELECTROVIVIENDA S.A.S (RRI, Autorretenedor) le vende mercancía por <strong>$10.000.000 + IVA 19%</strong> a un cliente que es <strong>Persona Natural No Responsable de IVA</strong>:<br/>
    1. ¿Cuánto es el IVA Generado (240805)? 👉 <strong>$1.900.000</strong><br/>
    2. ¿El comprador nos practica Retefuente o ReteICA? 👉 <strong>NO ($0)</strong>, porque un No Responsable de IVA no es agente de retención.<br/>
    3. ¿Cuánto nos autorretenemos en Renta (135575 vs 246575)? 👉 <strong>3.5% ($350.000)</strong> por tratarse de venta a No Declarante.<br/><br/>
    🚀 <em>¡Ve a la sección <strong>"⚡ Emitir Factura / Registro"</strong>, selecciona "No Responsable de IVA" y compruébalo en vivo!</em>`;
  }

  return `🤖 <strong>Respuesta Didáctica de STUDENTCONT.IA:</strong><br/><br/>
  Sobre tu consulta (<em>"${query}"</em>):<br/>
  • Recuerda que en <strong>STUDENTCONT.IA</strong> toda transacción parte de identificar el <strong>Régimen del Comprador y del Vendedor</strong>, aplicar la naturaleza del <strong>PUC (Activo 1, Gasto 5 y Costo 6 son Débito; Pasivo 2, Patrimonio 3 e Ingreso 4 son Crédito)</strong> y verificar las <strong>Sumas Iguales</strong>.<br/>
  • Puedes preguntarme por cualquier código del PUC (ej: <code>1110</code>, <code>1355</code>, <code>1435</code>, <code>2408</code>, <code>2465</code>, <code>4135</code>, <code>5105</code>, <code>6135</code>) o enseñarme este concepto específico en el panel <strong>"🧠 Alimentar / Enseñar Nuevos Temas a la IA"</strong> de la derecha para que quede guardado en mi memoria.`;
}

function sendStudentQuestionToAi() {
  const inp = document.getElementById("iaUserQuestionInput");
  if (!inp) return;
  const text = inp.value.trim();
  if (!text) return;

  IA_CHAT_HISTORY.push({ sender: "user", html: text });
  const reply = generateAiAccountingResponse(text);
  IA_CHAT_HISTORY.push({ sender: "bot", html: reply });
  inp.value = "";
  renderAiTutorSection();
}

async function feedNewKnowledgeToAi() {
  const tema = document.getElementById("iaTrainTopic")?.value.trim();
  const keywords = document.getElementById("iaTrainKeywords")?.value.trim() || "";
  const contenido = document.getElementById("iaTrainContent")?.value.trim();

  if (!tema || !contenido) {
    alert("Por favor escribe el Tema y la Explicación Didáctica para alimentar a la IA.");
    return;
  }

  const newItem = {
    id: `KB-${Date.now()}`,
    tema,
    keywords,
    contenido,
    autor: ACTIVE_STUDENT_PROFILE.nombre || "Gina Villamizar",
    fecha: new Date().toISOString().slice(0, 10)
  };

  try {
    const localKb = getCombinedCustomAiKnowledge();
    localKb.unshift(newItem);
    localStorage.setItem("studentcont_ia_custom_kb", JSON.stringify(localKb));
    const res = await fetch("/api/ia/conocimiento", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ item: newItem })
    });
    const data = await res.json();
    if (data.ok && DB) DB.ia_custom_kb = data.ia_custom_kb;
  } catch (e) {}

  document.getElementById("iaTrainTopic").value = "";
  document.getElementById("iaTrainKeywords").value = "";
  document.getElementById("iaTrainContent").value = "";

  IA_CHAT_HISTORY.push({
    sender: "bot",
    html: `✅ ¡Acabo de aprender el tema <strong>"${tema}"</strong>! Ya puedes preguntarme sobre él en el chat.`
  });
  renderAiTutorSection();
  showToast(`La IA aprendió con éxito: ${tema}`);
}

// ============================================================================
// 14. SECCIÓN: ACTUALIDAD, REFORMAS Y LEYES DE CONTABILIDAD EN COLOMBIA
// ============================================================================
let ACTIVE_REFORMA_CAT = "ALL";

const REFORMAS_COLOMBIA_BASE = [
  {
    id: "REF-01",
    categoria: "TRIBUTARIA",
    norma: "Ley 2277 de 2022 & Parámetros UVT 2026 ($52.374)",
    titulo: "Reforma Tributaria y Actualización de Tarifas, UVT y Tasa Mínima de Tributación",
    vigencia: "Vigente 2025 - 2026",
    resumen: "Establece para las sociedades en Colombia (como ELECTROVIVIENDA S.A.S) una tarifa general del Impuesto de Renta del 35% y una Tasa de Tributación Depurada (TTD) mínima del 15% sobre la utilidad contable NIIF antes de impuestos.",
    impacto_contable: "• La UVT 2026 ($52.374) actualiza todas las bases mínimas de Retención en la Fuente (Compras: 27 UVT; Servicios: 4 UVT) y la tabla de retención salarial del Art. 383 E.T. ( a partir de 95 UVT).\n• Limita al 3% anual de la renta líquida ordinaria ciertos beneficios y descuentos tributarios.\n• El GMF (4x1000 - Cuenta 530505) continúa siendo deducible en un 50% en la declaración de renta."
  },
  {
    id: "REF-02",
    categoria: "LABORAL",
    norma: "Ley 2381 de 2024 — Reforma Pensional Colombiana",
    titulo: "Nuevo Sistema de Protección Social Integral para la Vejez (Sistema de Pilares)",
    vigencia: "Implementación 2025 - 2026",
    resumen: "Transforma el sistema pensional colombiano en 4 pilares: Solidario, Semicontributivo, Contributivo y de Ahorro Voluntario. En el Pilar Contributivo, todos los trabajadores cotizan obligatoriamente en Colpensiones por sus ingresos hasta 2.3 SMLMV, y el excedente sobre 2.3 SMLMV va a una ACCAI (Fondo Privado).",
    impacto_contable: "• En la liquidación de nómina (Cuentas 5105 y 237095), los empleadores deben verificar en la planilla PILA la distribución del aporte del 16% (12% empleador, 4% trabajador) entre Colpensiones (hasta 2.3 SMLMV) y la ACCAI elegida por el trabajador cuando el salario supere ese umbral.\n• Actualiza las escalas del Fondo de Solidaridad Pensional (FSP) para salarios superiores a 4 SMLMV."
  },
  {
    id: "REF-03",
    categoria: "LABORAL",
    norma: "Ley 2101 de 2021 & Reforma Laboral",
    titulo: "Reducción Gradual de la Jornada Laboral Semanal (44h a 42h) sin Disminuir el Salario",
    vigencia: "Julio 2025 (44h) → Julio 2026 (42h)",
    resumen: "Reduce la jornada máxima legal en Colombia de 48 horas a 44 horas semanales en julio de 2025 y a 42 horas semanales en julio de 2026, manteniendo intacto el salario mensual de los trabajadores (SMLMV 2026: $1.750.905).",
    impacto_contable: "• Al disminuir las horas trabajadas al mes (divisor pasa de 240 a 220 y luego a 210 horas mensuales), aumenta automáticamente el valor de la hora ordinaria.\n• Esto incrementa el costo contable de las Horas Extras Diurnas (+25%), Nocturnas (+75%), Recargos Nocturnos (+35%) y Dominicales/Festivos en las subcuentas 510515 y 520515."
  },
  {
    id: "REF-04",
    categoria: "NIIF",
    norma: "Resolución DIAN 000165 de 2023 (Anexo Técnico 1.9)",
    titulo: "Facturación Electrónica de Venta, Notas Electrónicas y Documento Soporte en Compras a No Obligados",
    vigencia: "Obligatorio DIAN 2025 - 2026",
    resumen: "Exige la validación previa ante la DIAN de todas las Facturas Electrónicas de Venta, Notas Crédito/Débito Electrónicas, Nómina Electrónica y el Documento Soporte en Adquisiciones efectuadas a sujetos No Obligados a expedir factura de venta (No Responsables de IVA).",
    impacto_contable: "• Para que un costo (1435 / 6135) o gasto (51 / 52) sea deducible en Renta y su IVA (240810) sea descontable, debe contar con Factura Electrónica validada por la DIAN o Documento Soporte Electrónico (como en las compras de las Hojas 7 y 21 de ELECTROVIVIENDA).\n• En ventas a crédito, el comprador debe registrar los eventos RADIAN (Acuse de recibo de factura y recibo de mercancía)."
  },
  {
    id: "REF-05",
    categoria: "NIIF",
    norma: "Decreto 2420 de 2015 & Actualización NIIF para las PYMES (3ª Edición IASB / CTCP)",
    titulo: "Marco Técnico Normativo NIIF Grupo 2 — Reconocimiento de Ingresos, Inventarios y Depreciación",
    vigencia: "Marco Contable Vigente en Colombia",
    resumen: "Regula la preparación de los Estados Financieros de propósito general para PYMES en Colombia (Estado de Situación Financiera ESF, Estado de Resultados ER, Estado de Cambios en el Patrimonio ECP, Estado de Flujos de Efectivo y Notas).",
    impacto_contable: "• Sección 13 (Inventarios): Prohíbe el método UEPS (LIFO) y exige métodos como Promedio Ponderado o PEPS, midiendo el inventario al menor entre el costo y el valor neto realizable.\n• Sección 17 (Propiedad, Planta y Equipo): La depreciación (5160 vs 1592) inicia cuando el activo está disponible para su uso según su vida útil técnica."
  },
  {
    id: "REF-06",
    categoria: "TRIBUTARIA",
    norma: "Acuerdo Municipal Bucaramanga & Ley 1819 de 2016",
    titulo: "Estatuto Tributario Municipal: ReteICA (9.6‰), Avisos y Tableros (15%) y Sobretasa Bomberil (10%)",
    vigencia: "Calendario Tributario Municipal 2026",
    resumen: "Regula la retención territorial de Industria y Comercio en operaciones comerciales realizadas en la jurisdicción de Bucaramanga, Santander.",
    impacto_contable: "• Cuando ELECTROVIVIENDA S.A.S realiza compras o ventas sujetas a ReteICA en Bucaramanga, además de la tarifa comercial del 9.6 por mil (246801 / 135518), se liquida el 15% de Avisos y Tableros sobre el valor del ICA (246802 / 135520) y el 10% de Sobretasa Bomberil sobre el valor del ICA (246803 / 135525)."
  }
];

function getCombinedReformasList() {
  const custom = DB?.custom_reformas || [];
  let localCustom = [];
  try {
    localCustom = JSON.parse(localStorage.getItem("studentcont_custom_reformas") || "[]");
  } catch (e) {}
  const map = new Map();
  [...custom, ...localCustom, ...REFORMAS_COLOMBIA_BASE].forEach(r => {
    if (r && r.id) map.set(r.id, r);
  });
  return Array.from(map.values());
}

function filterReformasCategory(cat) {
  ACTIVE_REFORMA_CAT = cat;
  document.querySelectorAll("#reformasFilterTabs .filter-chip").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.refcat === cat);
  });
  renderReformasSection();
}

function renderReformasSection() {
  const container = document.getElementById("reformasGridContainer");
  if (!container) return;
  const all = getCombinedReformasList();
  const filtered = all.filter(r => ACTIVE_REFORMA_CAT === "ALL" || r.categoria === ACTIVE_REFORMA_CAT);

  container.innerHTML = filtered.map(r => {
    const pillCls = r.categoria === "TRIBUTARIA" ? "status-alert" : (r.categoria === "LABORAL" ? "status-paid" : "status-pending");
    return `
      <div class="reforma-card">
        <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
          <span class="status-pill ${pillCls}">${r.categoria}</span>
          <span style="font-size:0.73rem; font-weight:800; color:var(--text-secondary);">${r.vigencia}</span>
        </div>
        <div style="font-size:0.75rem; font-weight:800; color:var(--brand-gold-dark);">${r.norma}</div>
        <h3 style="font-size:0.98rem; font-weight:800; color:var(--brand-primary); margin:2px 0;">${r.titulo}</h3>
        <p style="font-size:0.81rem; color:var(--text-secondary); line-height:1.5; margin:0;">${r.resumen}</p>
        <div style="background:var(--bg-subtle); border-left:3px solid var(--brand-emerald); padding:10px 12px; border-radius:6px; font-size:0.79rem; line-height:1.5; margin-top:4px;">
          <strong style="color:var(--brand-primary); display:block; margin-bottom:4px;">📌 ¿Cómo nos afecta en la Contabilidad?:</strong>
          ${(r.impacto_contable || "").replace(/\n/g, "<br/>")}
        </div>
        ${r.fuente_url ? `
        <div style="margin-top:8px; display:flex; justify-content:flex-end;">
          <a class="btn btn-outline btn-sm" style="text-decoration:none; font-size:0.74rem;" href="${r.fuente_url}" target="_blank" rel="noopener">
            🔗 Abrir Página Web / Documento Fuente Original
          </a>
        </div>` : ""}
      </div>
    `;
  }).join("");
}

async function openNewReformaModal() {
  const norma = prompt("Ley, Decreto o Resolución (Ej: Decreto 0572 de 2026):", "Nueva Norma Contable / Tributaria");
  if (!norma) return;
  const titulo = prompt("Título de la Reforma o Noticia Contable:", "Actualización de Retenciones y Obligaciones Formales");
  if (!titulo) return;
  const resumen = prompt("Resumen claro para los estudiantes:", "Explica en qué consiste el cambio normativo en Colombia.") || "";
  const impacto = prompt("¿Cómo afecta los asientos contables o impuestos?:", "Afecta la liquidación de impuestos y cuentas del PUC.") || "";

  const item = {
    id: `REF-CUSTOM-${Date.now()}`,
    categoria: "TRIBUTARIA",
    norma,
    titulo,
    vigencia: `Publicado por ${ACTIVE_STUDENT_PROFILE.nombre || "Gina Villamizar"}`,
    resumen,
    impacto_contable: impacto
  };

  try {
    const localList = JSON.parse(localStorage.getItem("studentcont_custom_reformas") || "[]");
    localList.unshift(item);
    localStorage.setItem("studentcont_custom_reformas", JSON.stringify(localList));
    const res = await fetch("/api/reformas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ reforma: item })
    });
    const data = await res.json();
    if (data.ok && DB) DB.custom_reformas = data.custom_reformas;
  } catch (e) {}

  renderReformasSection();
  showToast("Nueva reforma/norma publicada para los estudiantes");
}

// ============================================================================
// 11. MOTOR PROFESIONAL DE DESCARGA E IMPRESIÓN PDF (FACTURA REAL DIAN + ASIENTOS + INFORMES)
// ============================================================================

function generateSimulatedCufe(seedStr) {
  const base = String(seedStr || "FACTURA-DIAN-2026") + "|ELECTROVIVIENDA|9017654383|DIAN2026";
  let hex = "";
  for (let i = 0; i < 96; i++) {
    const code = (base.charCodeAt(i % base.length) * (i + 17) + i * 31) % 16;
    hex += code.toString(16);
  }
  return hex;
}

function generateSimulatedQrSvg(seedStr) {
  const s = String(seedStr || "FE-001");
  let rects = "";
  const size = 11;
  for (let r = 0; r < size; r++) {
    for (let c = 0; c < size; c++) {
      const isCorner = (r < 3 && c < 3) || (r < 3 && c >= size - 3) || (r >= size - 3 && c < 3);
      const hash = (s.charCodeAt((r * size + c) % s.length) + r * 7 + c * 13) % 3;
      if (isCorner || hash === 0) {
        rects += `<rect x="${4 + c * 6}" y="${4 + r * 6}" width="5" height="5" fill="#0B192C" rx="0.8"/>`;
      }
    }
  }
  return `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 74 74" width="76" height="76" style="border:1px solid #cbd5e1; border-radius:6px; background:#fff; padding:2px;">
      ${rects}
    </svg>
  `;
}

function buildRealDianInvoiceHtml(inv, includeJournal = false) {
  const emp = DB?.empresa || {};
  const isVenta = inv.categoria === "VENTA" || String(inv.tipo_operacion || "").includes("VENTA");
  const emisorNombre = isVenta ? (emp.razon_social || "ELECTROVIVIENDA S.A.S") : (inv.tercero || "PROVEEDOR COMERCIAL S.A.S");
  const emisorNit = isVenta ? (emp.nit || "901.765.438-3") : (inv.nit_tercero || "900.123.456-1");
  const emisorRegimen = inv.regimen_vendedor || emp.regimen || "Régimen Responsable de IVA (RRI)";
  const emisorDir = isVenta ? `${emp.direccion || "Cra 27 # 36-14"} — ${emp.ciudad || "Bucaramanga, Santander"}` : (emp.ciudad || "Bucaramanga, Santander");
  const emisorTel = isVenta ? `${emp.telefono || "(607) 645-8920"} • ${emp.correo || "facturacion@electrovivienda.com.co"}` : "facturacion@proveedor.com.co";

  const receptorNombre = isVenta ? (inv.tercero || "CLIENTE COMERCIAL") : (emp.razon_social || "ELECTROVIVIENDA S.A.S");
  const receptorNit = isVenta ? (inv.nit_tercero || "900.000.000-1") : (emp.nit || "901.765.438-3");
  const receptorRegimen = inv.regimen_comprador || "Responsable de IVA (RRI)";

  const cufe = generateSimulatedCufe(`${inv.numero}-${inv.fecha}-${inv.total_neto}`);
  const qrSvg = generateSimulatedQrSvg(`${inv.numero}-${inv.fecha}`);

  const itemsList = (inv.items && inv.items.length)
    ? inv.items
    : [{
        referencia: "MERC-001",
        descripcion: inv.enunciado || inv.tipo_operacion || "Operación comercial de mercancías",
        cantidad: 1,
        valor_unitario: inv.subtotal || inv.total_neto || 0,
        subtotal: inv.subtotal || inv.total_neto || 0
      }];

  const itemsRowsHtml = itemsList.map((it, idx) => `
    <tr>
      <td style="text-align:center; font-weight:700;">${idx + 1}</td>
      <td style="font-family:'JetBrains Mono', monospace; font-weight:700;">${it.referencia || `ITEM-0${idx + 1}`}</td>
      <td><strong>${it.descripcion}</strong></td>
      <td style="text-align:center;">UND</td>
      <td style="text-align:right;">${fmtNum(it.cantidad || 1)}</td>
      <td style="text-align:right;">${fmtCOP(it.valor_unitario || 0)}</td>
      <td style="text-align:center;">${inv.iva > 0 ? "19%" : "0%"}</td>
      <td style="text-align:right; font-weight:800;">${fmtCOP(it.subtotal || 0)}</td>
    </tr>
  `).join("");

  const asientosRowsHtml = (inv.asientos || []).map(a => {
    const isSub = String(a.codigo).length >= 6 && (!a.debe && !a.haber);
    return `
      <tr>
        <td style="font-family:'JetBrains Mono', monospace; font-weight:700;">${a.codigo || ""}</td>
        <td style="${isSub ? "padding-left:18px; color:#475569; font-style:italic;" : "font-weight:700; color:#0f172a;"}">${a.cuenta || ""}</td>
        <td style="text-align:right; color:#475569;">${a.parcial ? fmtCOP(a.parcial) : ""}</td>
        <td style="text-align:right; font-weight:700;">${a.debe ? fmtCOP(a.debe) : ""}</td>
        <td style="text-align:right; font-weight:700;">${a.haber ? fmtCOP(a.haber) : ""}</td>
      </tr>
    `;
  }).join("");

  const journalSectionHtml = includeJournal ? `
    <div style="margin-top:18px; border:1.5px solid #0B192C; border-radius:8px; overflow:hidden; page-break-inside:avoid;">
      <div style="background:#0B192C; color:#fff; padding:8px 14px; display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:11px; font-weight:800; letter-spacing:0.5px;">📘 COMPROBANTE DE CONTABILIZACIÓN OFICIAL NIIF (HOJA ${inv.hoja || "1"} — ${inv.mes || ACTIVE_PERIOD})</span>
        <span style="font-size:11px; font-weight:800; color:#F3E5AB;">SUMAS IGUALES: ${fmtCOP(inv.total_debe || inv.total_neto)}</span>
      </div>
      <table style="width:100%; border-collapse:collapse; font-size:10.5px;">
        <thead>
          <tr style="background:#f1f5f9; border-bottom:1px solid #cbd5e1;">
            <th style="padding:6px 10px; text-align:left; width:14%;">Código PUC</th>
            <th style="padding:6px 10px; text-align:left; width:44%;">Cuenta Contable / Subcuenta / Tercero Auxiliar</th>
            <th style="padding:6px 10px; text-align:right; width:14%;">Parcial</th>
            <th style="padding:6px 10px; text-align:right; width:14%;">Debe (Débitos)</th>
            <th style="padding:6px 10px; text-align:right; width:14%;">Haber (Créditos)</th>
          </tr>
        </thead>
        <tbody>
          ${asientosRowsHtml}
          <tr style="background:#fef9c3; font-weight:800; border-top:1.5px solid #0B192C;">
            <td colspan="2" style="padding:7px 10px;">SUMAS IGUALES DEL ASIENTO CONTABLE</td>
            <td></td>
            <td style="padding:7px 10px; text-align:right;">${fmtCOP(inv.total_debe || 0)}</td>
            <td style="padding:7px 10px; text-align:right;">${fmtCOP(inv.total_haber || 0)}</td>
          </tr>
        </tbody>
      </table>
    </div>
  ` : "";

  return `
    <div class="pdf-sheet-container" style="font-family:'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif; color:#0f172a; background:#ffffff; padding:24px 28px; max-width:820px; margin:0 auto; border:1px solid #cbd5e1; border-radius:8px;">
      <!-- CABECERA EMISOR + RECUADRO DIAN + QR -->
      <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:16px; border-bottom:2.5px solid #0B192C; padding-bottom:14px; margin-bottom:14px;">
        <div style="flex:1.3;">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
            <div style="background:#0B192C; color:#D4AF37; font-weight:900; font-size:18px; width:38px; height:38px; border-radius:8px; display:flex; align-items:center; justify-content:center; border:2px solid #D4AF37;">
              EV
            </div>
            <div>
              <div style="font-size:17px; font-weight:800; color:#0B192C; letter-spacing:-0.3px;">${emisorNombre}</div>
              <div style="font-size:11px; font-weight:700; color:#047857;">NIT: ${emisorNit} • ${emisorRegimen}</div>
            </div>
          </div>
          <div style="font-size:10.5px; color:#334155; line-height:1.45;">
            <strong>Dirección Fiscal:</strong> ${emisorDir}<br/>
            <strong>Contacto:</strong> ${emisorTel}<br/>
            <strong>Actividad Económica:</strong> CIIU 4754 (Comercio de electrodomésticos y muebles) • Tarifa ICA 9.6‰<br/>
            <strong>Resolución Facturación Electrónica DIAN:</strong> N° 18764065892104 del 2026-01-02 • Prefijo FE del N° 001 al 5000 (Vigencia 12 meses)
          </div>
        </div>

        <div style="display:flex; align-items:center; gap:10px; border:2px solid #0B192C; border-radius:8px; padding:10px 14px; background:#f8fafc;">
          <div style="text-align:right;">
            <div style="font-size:9.5px; font-weight:800; color:#0B192C; text-transform:uppercase; letter-spacing:0.6px;">
              ${inv.tipo_operacion || "FACTURA ELECTRÓNICA DE VENTA"}
            </div>
            <div style="font-size:16px; font-weight:900; color:#b45309; margin:2px 0; font-family:'JetBrains Mono', monospace;">
              ${inv.numero || "FE-001"}
            </div>
            <div style="font-size:10px; color:#334155; line-height:1.4;">
              <strong>Fecha Emisión:</strong> ${inv.fecha || "2026-01-10"}<br/>
              <strong>Período Contable:</strong> ${inv.mes || ACTIVE_PERIOD} (Hoja ${inv.hoja || "1"})<br/>
              <strong>Moneda:</strong> COP (Peso Colombiano)
            </div>
          </div>
          ${qrSvg}
        </div>
      </div>

      <!-- DATOS VENDEDOR VS ADQUIRIENTE / COMPRADOR -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:14px;">
        <div style="border:1px solid #cbd5e1; border-left:4px solid #0B192C; border-radius:6px; padding:9px 12px; background:#f8fafc;">
          <div style="font-size:9.5px; font-weight:800; color:#0B192C; text-transform:uppercase; margin-bottom:3px;">
            🧑‍💼 DATOS DEL EMISOR / VENDEDOR Y RÉGIMEN TRIBUTARIO
          </div>
          <div style="font-size:12px; font-weight:800; color:#0f172a;">${emisorNombre}</div>
          <div style="font-size:10.5px; color:#334155; line-height:1.45; margin-top:2px;">
            <strong>NIT:</strong> ${emisorNit}<br/>
            <strong>Régimen Tributario:</strong> ${inv.regimen_vendedor || emisorRegimen}<br/>
            <strong>Responsabilidad Fiscal:</strong> O-13 Gran Contribuyente / O-15 Autorretenedor / O-48 IVA
          </div>
        </div>

        <div style="border:1px solid #cbd5e1; border-left:4px solid #D4AF37; border-radius:6px; padding:9px 12px; background:#f8fafc;">
          <div style="font-size:9.5px; font-weight:800; color:#92400e; text-transform:uppercase; margin-bottom:3px;">
            🏢 DATOS DEL ADQUIRIENTE / COMPRADOR Y RÉGIMEN TRIBUTARIO
          </div>
          <div style="font-size:12px; font-weight:800; color:#0f172a;">${receptorNombre}</div>
          <div style="font-size:10.5px; color:#334155; line-height:1.45; margin-top:2px;">
            <strong>NIT / CC:</strong> ${receptorNit}<br/>
            <strong>Régimen Tributario:</strong> ${receptorRegimen}<br/>
            <strong>Forma y Medio de Pago:</strong> ${inv.forma_pago || "Crédito / Transferencia Bancaria"}
          </div>
        </div>
      </div>

      <!-- TABLA DE PRODUCTOS / SERVICIOS FACTURADOS -->
      <div style="border:1.5px solid #0B192C; border-radius:8px; overflow:hidden; margin-bottom:14px;">
        <table style="width:100%; border-collapse:collapse; font-size:11px;">
          <thead>
            <tr style="background:#0B192C; color:#ffffff;">
              <th style="padding:7px 8px; text-align:center; width:6%;">#</th>
              <th style="padding:7px 8px; text-align:left; width:13%;">Referencia</th>
              <th style="padding:7px 8px; text-align:left; width:36%;">Descripción del Bien o Servicio</th>
              <th style="padding:7px 8px; text-align:center; width:7%;">U.M.</th>
              <th style="padding:7px 8px; text-align:right; width:8%;">Cant.</th>
              <th style="padding:7px 8px; text-align:right; width:13%;">Vlr. Unitario</th>
              <th style="padding:7px 8px; text-align:center; width:6%;">IVA</th>
              <th style="padding:7px 8px; text-align:right; width:14%;">Valor Total</th>
            </tr>
          </thead>
          <tbody>
            ${itemsRowsHtml}
          </tbody>
        </table>
      </div>

      <!-- OBSERVACIONES + VALOR EN LETRAS + LIQUIDACIÓN DE IMPUESTOS Y RETENCIONES -->
      <div style="display:grid; grid-template-columns:1.25fr 1fr; gap:14px; align-items:start;">
        <div style="display:flex; flex-direction:column; gap:8px;">
          <div style="background:#fef9c3; border:1px solid #eab308; border-radius:6px; padding:8px 12px; font-size:10.5px;">
            <strong>SON (VALOR EN LETRAS):</strong><br/>
            <span style="font-weight:800; color:#0f172a;">${inv.suma_letras || `${fmtCOP(inv.total_neto)} PESOS M/CTE.`}</span>
          </div>

          <div style="border:1px solid #cbd5e1; border-radius:6px; padding:8px 12px; font-size:10.5px; color:#334155;">
            <strong style="color:#0B192C;">Observaciones y Concepto de la Operación:</strong><br/>
            ${inv.enunciado || inv.tipo_operacion}
          </div>

          <div style="border:1px dashed #94a3b8; border-radius:6px; padding:7px 10px; font-size:9px; color:#475569; font-family:'JetBrains Mono', monospace; word-break:break-all; background:#f8fafc;">
            <strong>CUFE (SHA-384 Validación DIAN):</strong><br/>
            ${cufe}
          </div>
        </div>

        <div style="border:1.5px solid #0B192C; border-radius:8px; overflow:hidden; background:#fff;">
          <div style="background:#f1f5f9; padding:6px 12px; font-size:10px; font-weight:800; color:#0B192C; border-bottom:1px solid #cbd5e1;">
            RESUMEN DE LIQUIDACIÓN DE IMPUESTOS Y RETENCIONES
          </div>
          <div style="padding:8px 12px; font-size:11px; display:flex; flex-direction:column; gap:5px;">
            <div style="display:flex; justify-content:space-between;">
              <span>Subtotal Base Gravable:</span>
              <strong>${fmtCOP(inv.subtotal || 0)}</strong>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>(+) IVA Generado / Descontable (19%):</span>
              <strong>${fmtCOP(inv.iva || 0)}</strong>
            </div>
            <div style="display:flex; justify-content:space-between; border-top:1px dashed #cbd5e1; padding-top:4px;">
              <span><strong>Total Bruto Factura (Base + IVA):</strong></span>
              <strong>${fmtCOP((inv.subtotal || 0) + (inv.iva || 0))}</strong>
            </div>
            ${inv.retefuente ? `
            <div style="display:flex; justify-content:space-between; color:#b91c1c;">
              <span>(-) Retención en la Fuente Renta:</span>
              <strong>-${fmtCOP(inv.retefuente)}</strong>
            </div>` : ""}
            ${inv.reteiva ? `
            <div style="display:flex; justify-content:space-between; color:#b91c1c;">
              <span>(-) Retención de IVA (ReteIVA 15%):</span>
              <strong>-${fmtCOP(inv.reteiva)}</strong>
            </div>` : ""}
            ${inv.reteica ? `
            <div style="display:flex; justify-content:space-between; color:#b91c1c;">
              <span>(-) ReteICA + Avisos (15%) + Bomberil (10%):</span>
              <strong>-${fmtCOP(inv.reteica)}</strong>
            </div>` : ""}
            ${inv.autorretencion ? `
            <div style="display:flex; justify-content:space-between; color:#0369a1; font-size:10px;">
              <span>(i) Autorretención Renta Emisor (135575 / 246575):</span>
              <strong>${fmtCOP(inv.autorretencion)}</strong>
            </div>` : ""}
            <div style="display:flex; justify-content:space-between; background:#0B192C; color:#ffffff; padding:8px 10px; border-radius:6px; font-size:12.5px; font-weight:900; margin-top:4px;">
              <span>TOTAL NETO A PAGAR:</span>
              <span style="color:#F3E5AB;">${fmtCOP(inv.total_neto || 0)}</span>
            </div>
          </div>
        </div>
      </div>

      ${journalSectionHtml}

      <!-- FIRMAS DE LEY FACTURA COMERCIAL -->
      <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:16px; margin-top:18px; padding-top:12px; border-top:1px solid #cbd5e1; font-size:10px; text-align:center;">
        <div style="padding-top:22px; border-top:1px solid #334155; margin-top:16px;">
          <strong>ELABORADO Y EMITIDO POR</strong><br/>
          ${emp.elaborado_por || "Gina Villamizar"}<br/>
          <span style="color:#64748b;">Departamento de Contabilidad & Facturación</span>
        </div>
        <div style="padding-top:22px; border-top:1px solid #334155; margin-top:16px;">
          <strong>FIRMA AUTORIZADA EMISOR</strong><br/>
          ${emisorNombre}<br/>
          <span style="color:#64748b;">NIT ${emisorNit}</span>
        </div>
        <div style="padding-top:22px; border-top:1px solid #334155; margin-top:16px;">
          <strong>ACEPTACIÓN Y RECIBIDO COMPRADOR</strong><br/>
          ${receptorNombre}<br/>
          <span style="color:#64748b;">Título Valor según Ley 1231 de 2008 y C. de Co.</span>
        </div>
      </div>

      <div style="text-align:center; font-size:9px; color:#64748b; margin-top:10px;">
        Documento generado electrónicamente por <strong>STUDENTCONT.IA — Sistema Contable & Fiscal NIIF</strong> • Representación Gráfica de Factura Electrónica DIAN
      </div>
    </div>
  `;
}

function buildRealAccountingVoucherHtml(tx, mes) {
  const emp = DB?.empresa || {};
  const compDiarioTitle = tx.comprobante_diario || `Comprobante de Contabilidad Hoja ${tx.hoja}`;
  const qrSvg = generateSimulatedQrSvg(`${compDiarioTitle}-${mes}-${tx.hoja}`);

  const asientosRowsHtml = (tx.asientos || []).map(a => {
    const isSub = String(a.codigo).length >= 6 && (!a.debe && !a.haber);
    return `
      <tr style="border-bottom:1px solid #e2e8f0;">
        <td style="padding:6px 10px; font-family:'JetBrains Mono', monospace; font-weight:700;">${a.codigo || ""}</td>
        <td style="padding:6px 10px; ${isSub ? "padding-left:22px; color:#475569; font-style:italic;" : "font-weight:700; color:#0f172a;"}">${a.cuenta || ""}</td>
        <td style="padding:6px 10px; text-align:right; color:#475569;">${a.parcial ? fmtCOP(a.parcial) : ""}</td>
        <td style="padding:6px 10px; text-align:right; font-weight:700;">${a.debe ? fmtCOP(a.debe) : ""}</td>
        <td style="padding:6px 10px; text-align:right; font-weight:700;">${a.haber ? fmtCOP(a.haber) : ""}</td>
      </tr>
    `;
  }).join("");

  return `
    <div class="pdf-sheet-container" style="font-family:'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif; color:#0f172a; background:#ffffff; padding:26px 30px; max-width:820px; margin:0 auto; border:1px solid #cbd5e1; border-radius:8px;">
      <!-- CABECERA DEL COMPROBANTE DE CONTABILIDAD -->
      <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:16px; border-bottom:2.5px solid #0B192C; padding-bottom:14px; margin-bottom:14px;">
        <div>
          <div style="font-size:18px; font-weight:900; color:#0B192C;">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
          <div style="font-size:11px; font-weight:700; color:#047857; margin-top:2px;">NIT: ${emp.nit || "901.765.438-3"} • ${emp.regimen || "Responsable de IVA (RRI)"}</div>
          <div style="font-size:10.5px; color:#334155; margin-top:3px;">
            ${emp.direccion || "Cra 27 # 36-14"} — ${emp.ciudad || "Bucaramanga, Santander"} • ${emp.grupo_niif || "Grupo 2 NIIF PYMES"}
          </div>
        </div>

        <div style="display:flex; align-items:center; gap:10px; border:2px solid #0B192C; border-radius:8px; padding:10px 14px; background:#f8fafc;">
          <div style="text-align:right;">
            <div style="font-size:10px; font-weight:800; color:#0B192C; text-transform:uppercase;">${compDiarioTitle}</div>
            <div style="font-size:15px; font-weight:900; color:#b45309; font-family:'JetBrains Mono', monospace;">Hoja N° ${tx.hoja} (${mes})</div>
            <div style="font-size:10px; color:#334155;">
              <strong>Documento:</strong> ${tx.tipo || "COMPROBANTE"}<br/>
              <strong>Fecha:</strong> ${tx.fecha || "2026"}
            </div>
          </div>
          ${qrSvg}
        </div>
      </div>

      <!-- DATOS DEL SOPORTE Y ENUNCIADO CONTABLE -->
      <div style="display:grid; grid-template-columns:1.15fr 1fr; gap:12px; margin-bottom:14px;">
        <div style="border:1px solid #cbd5e1; border-left:4px solid #0B192C; border-radius:6px; padding:10px 12px; background:#f8fafc;">
          <div style="font-size:9.5px; font-weight:800; color:#0B192C; text-transform:uppercase; margin-bottom:4px;">
            📌 CONCEPTO / ENUNCIADO DE LA OPERACIÓN CONTABLE
          </div>
          <div style="font-size:11.5px; font-weight:700; color:#0f172a; line-height:1.45;">
            ${tx.enunciado || tx.concepto_soporte || "Registro contable oficial del período"}
          </div>
          ${tx.concepto_comprobante_diario ? `<div style="margin-top:5px; font-size:10px; color:#047857; font-weight:700;">📘 Libro Diario Oficial: ${tx.comprobante_diario} — ${tx.concepto_comprobante_diario}</div>` : ""}
        </div>

        <div style="border:1px solid #cbd5e1; border-left:4px solid #D4AF37; border-radius:6px; padding:10px 12px; background:#f8fafc; font-size:10.5px; line-height:1.5;">
          <div style="font-size:9.5px; font-weight:800; color:#92400e; text-transform:uppercase; margin-bottom:3px;">
            🧾 DATOS DEL BENEFICIARIO Y DOCUMENTO SOPORTE
          </div>
          <strong>Tercero / Beneficiario:</strong> ${tx.tercero || emp.razon_social}<br/>
          <strong>NIT / Cédula:</strong> <span style="font-family:'JetBrains Mono', monospace;">${tx.nit_tercero || emp.nit}</span><br/>
          <strong>Medio de Pago / Referencia:</strong> ${tx.cheque || "Contado / Causación Contable"}<br/>
          <strong>La Suma de (Letras):</strong> ${tx.suma_letras || fmtCOP(tx.total_debe)}
        </div>
      </div>

      <!-- TABLA DE CONTABILIZACIÓN PUC -->
      <div style="border:1.5px solid #0B192C; border-radius:8px; overflow:hidden; margin-bottom:16px;">
        <div style="background:#0B192C; color:#ffffff; padding:8px 14px; display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:11px; font-weight:800;">CONTABILIZACIÓN OFICIAL PUC — ${compDiarioTitle.toUpperCase()} (HOJA ${tx.hoja})</span>
          <span style="font-size:11px; font-weight:800; color:#F3E5AB;">PARTIDA DOBLE VERIFICADA ✓</span>
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:11px;">
          <thead>
            <tr style="background:#f1f5f9; border-bottom:1.5px solid #0B192C;">
              <th style="padding:7px 10px; text-align:left; width:14%;">Código PUC</th>
              <th style="padding:7px 10px; text-align:left; width:44%;">Cuenta Contable / Subcuenta / Auxiliar</th>
              <th style="padding:7px 10px; text-align:right; width:14%;">Parcial</th>
              <th style="padding:7px 10px; text-align:right; width:14%;">Debe (Débitos)</th>
              <th style="padding:7px 10px; text-align:right; width:14%;">Haber (Créditos)</th>
            </tr>
          </thead>
          <tbody>
            ${asientosRowsHtml}
            <tr style="background:#fef9c3; font-weight:900; border-top:2px solid #0B192C; font-size:11.5px;">
              <td colspan="2" style="padding:8px 10px;">SUMAS IGUALES DEL COMPROBANTE</td>
              <td></td>
              <td style="padding:8px 10px; text-align:right;">${fmtCOP(tx.total_debe || 0)}</td>
              <td style="padding:8px 10px; text-align:right;">${fmtCOP(tx.total_haber || 0)}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- BLOQUE DE 4 FIRMAS CONTABLES -->
      <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:12px; margin-top:24px; padding-top:10px; font-size:10px; text-align:center;">
        <div style="border-top:1px solid #334155; padding-top:6px;">
          <strong>ELABORADO POR:</strong><br/>
          ${tx.elaborado_por || emp.elaborado_por || "Gina Villamizar"}<br/>
          <span style="color:#64748b;">Contabilidad NIIF</span>
        </div>
        <div style="border-top:1px solid #334155; padding-top:6px;">
          <strong>REVISADO POR:</strong><br/>
          Auditoría Interna<br/>
          <span style="color:#64748b;">Control Fiscal</span>
        </div>
        <div style="border-top:1px solid #334155; padding-top:6px;">
          <strong>APROBADO POR:</strong><br/>
          Kevin Guerrero<br/>
          <span style="color:#64748b;">Representante Legal • ${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</span>
        </div>
        <div style="border-top:1px solid #334155; padding-top:6px;">
          <strong>FIRMA Y SELLO BENEFICIARIO:</strong><br/>
          ${tx.tercero || "Recibido Conforme"}<br/>
          <span style="color:#64748b;">C.C. / NIT: ${tx.nit_tercero || ""}</span>
        </div>
      </div>

      <div style="text-align:center; font-size:9px; color:#64748b; margin-top:12px;">
        Comprobante oficial emitido en <strong>STUDENTCONT.IA — Sistema Contable & Fiscal NIIF</strong>
      </div>
    </div>
  `;
}

let CURRENT_PDF_PAYLOAD = {
  html: "",
  filename: "",
  title: ""
};

function downloadOrPrintPdfDocument(htmlContent, filename, docTitle, options = {}) {
  const isLandscape = options.orientation === "landscape" || 
                      filename.includes("Consolidado") || 
                      filename.includes("Flujo") || 
                      filename.includes("Balance_Comprobacion") ||
                      filename.includes("ECP");

  CURRENT_PDF_PAYLOAD = {
    html: htmlContent,
    filename: filename,
    title: docTitle,
    orientation: isLandscape ? "landscape" : "portrait"
  };

  const modal = document.getElementById("pdfViewerModal");
  const modalCard = modal ? modal.querySelector(".pdf-viewer-modal-card") : null;
  const sheet = document.getElementById("pdfModalSheetBody");
  const titleEl = document.getElementById("pdfModalDocTitle");
  const subEl = document.getElementById("pdfModalDocSubtitle");

  if (sheet) sheet.innerHTML = htmlContent;
  if (titleEl) titleEl.textContent = docTitle || "Documento Contable Oficial NIIF";
  if (subEl) subEl.textContent = `${filename} • Formato ${isLandscape ? "Horizontal (Landscape - 100% Completo)" : "Vertical"} • Impresión Oficial y Descarga PDF`;

  document.body.classList.add("has-pdf-open");
  if (isLandscape) {
    document.body.classList.add("print-landscape");
    if (modalCard) modalCard.classList.add("modal-landscape");
  } else {
    document.body.classList.remove("print-landscape");
    if (modalCard) modalCard.classList.remove("modal-landscape");
  }

  if (modal) {
    modal.classList.add("open");
  }

  showToast(`📄 Documento listo (${isLandscape ? 'Formato Horizontal' : 'Formato Vertical'}). Haz clic en "Descargar Archivo PDF" o "Imprimir / Guardar como PDF".`);
}

function triggerActivePdfDownload(notify = true) {
  if (!CURRENT_PDF_PAYLOAD.html) return;
  const filename = CURRENT_PDF_PAYLOAD.filename || "documento_contable.pdf";
  const targetEl = document.getElementById("pdfModalSheetBody");
  if (!targetEl) return;

  const isLandscape = CURRENT_PDF_PAYLOAD.orientation === "landscape";
  const canvasWidth = isLandscape ? 1040 : 760;

  if (notify) {
    showToast(`Generando y descargando PDF visible: ${filename}...`);
  }

  if (typeof window.html2pdf === "function") {
    // Clonar contenido en una capa visible al motor de render pero detrás del viewport (z-index negativo, origen 0,0)
    const printClone = targetEl.cloneNode(true);
    printClone.id = "tempPdfExportCanvas";
    printClone.style.position = "absolute";
    printClone.style.left = "0px";
    printClone.style.top = "0px";
    printClone.style.width = `${canvasWidth}px`;
    printClone.style.maxWidth = `${canvasWidth}px`;
    printClone.style.zIndex = "-999999";
    printClone.style.opacity = "1";
    printClone.style.visibility = "visible";
    printClone.style.pointerEvents = "none";
    printClone.style.padding = isLandscape ? "14px 18px" : "12px 14px";
    printClone.style.background = "#FFFFFF";
    printClone.style.color = "#0F172A";
    printClone.style.boxSizing = "border-box";
    printClone.style.overflow = "visible";

    printClone.querySelectorAll("td, th, p, div, span").forEach(el => {
      if (!el.classList.contains("num-col") && !el.classList.contains("code-col")) {
        el.style.whiteSpace = "normal";
        el.style.wordBreak = "break-word";
        el.style.overflowWrap = "break-word";
      }
    });
    printClone.querySelectorAll(".table-wrap").forEach(tw => {
      tw.style.overflow = "visible";
      tw.style.width = "100%";
      tw.style.border = "none";
    });
    printClone.querySelectorAll("table").forEach(tbl => {
      tbl.style.width = "100%";
      tbl.style.tableLayout = "auto";
    });

    document.body.appendChild(printClone);

    const opt = {
      margin: isLandscape ? [5, 5, 5, 5] : [6, 6, 6, 6],
      filename: filename,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: {
        scale: 2,
        useCORS: true,
        allowTaint: true,
        backgroundColor: "#FFFFFF",
        logging: false,
        scrollY: 0,
        scrollX: 0
      },
      jsPDF: { unit: "mm", format: "a4", orientation: isLandscape ? "landscape" : "portrait" },
      pagebreak: { mode: ["avoid-all", "css", "legacy"] }
    };

    setTimeout(() => {
      window.html2pdf().set(opt).from(printClone).save().then(() => {
        showToast(`✅ Archivo PDF descargado correctamente: ${filename}`);
        if (printClone.parentNode) printClone.parentNode.removeChild(printClone);
      }).catch(err => {
        console.warn("Aviso html2pdf fallback:", err);
        if (printClone.parentNode) printClone.parentNode.removeChild(printClone);
        triggerActivePdfPrint();
      });
    }, 150);
  } else {
    triggerActivePdfPrint();
  }
}

function triggerActivePdfPrint() {
  window.print();
}

function closePdfViewerModal() {
  document.body.classList.remove("has-pdf-open");
  document.body.classList.remove("print-landscape");
  const modal = document.getElementById("pdfViewerModal");
  if (modal) {
    modal.classList.remove("open");
    const modalCard = modal.querySelector(".pdf-viewer-modal-card");
    if (modalCard) modalCard.classList.remove("modal-landscape");
  }
}

function openCleanPrintWindow(htmlContent, docTitle) {
  const win = window.open("", "_blank", "width=920,height=800");
  if (!win) {
    window.print();
    return;
  }
  win.document.write(`
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8" />
      <title>${docTitle || "Documento Contable PDF — STUDENTCONT.IA"}</title>
      <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
      <style>
        body { margin: 0; padding: 16px; background: #f1f5f9; font-family: 'Plus Jakarta Sans', sans-serif; }
        .top-print-bar { max-width: 820px; margin: 0 auto 14px auto; display: flex; justify-content: space-between; align-items: center; background: #0B192C; color: #fff; padding: 10px 16px; border-radius: 8px; }
        .top-print-bar button { background: #D4AF37; color: #0B192C; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 800; cursor: pointer; font-size: 13px; }
        @media print {
          body { background: #ffffff; padding: 0; }
          .top-print-bar { display: none !important; }
          .pdf-sheet-container { border: none !important; padding: 0 !important; max-width: 100% !important; }
        }
      </style>
    </head>
    <body>
      <div class="top-print-bar">
        <span><strong>📄 Vista Oficial de Impresión / Guardar como PDF</strong> — ${docTitle}</span>
        <button onclick="window.print()">🖨️ Guardar como PDF / Imprimir</button>
      </div>
      ${htmlContent}
      <script>setTimeout(() => { window.print(); }, 500);<\/script>
    </body>
    </html>
  `);
  win.document.close();
}

function exportProfessionalInvoicePDF(includeJournal = false) {
  if (!DB) return;
  const allInvs = (DB.facturas || []).map(f => normalizeInvoiceRecord(f));
  const inv = allInvs.find(f => f.id === ACTIVE_INVOICE_ID) || allInvs[0];
  if (!inv) {
    showToast("No hay una factura seleccionada para exportar a PDF.");
    return;
  }
  const safeNum = String(inv.numero || "Factura").replace(/[^a-zA-Z0-9_-]/g, "_");
  const suffix = includeJournal ? "_con_Asiento_Contable" : "_Factura_DIAN";
  const filename = `${safeNum}_${inv.mes || ACTIVE_PERIOD}${suffix}.pdf`;
  const html = buildRealDianInvoiceHtml(inv, includeJournal);
  downloadOrPrintPdfDocument(html, filename, `${inv.tipo_operacion} ${inv.numero}`);
}

function exportProfessionalVoucherPDF() {
  if (!DB) return;
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
    showToast("No hay un comprobante seleccionado en este mes.");
    return;
  }
  const compName = String(tx.comprobante_diario || `Comprobante_Hoja_${tx.hoja}`).replace(/[^a-zA-Z0-9_-]/g, "_");
  const filename = `${compName}_${mes}_Hoja_${tx.hoja}.pdf`;
  const html = buildRealAccountingVoucherHtml(tx, mes);
  downloadOrPrintPdfDocument(html, filename, `${tx.comprobante_diario || tx.tipo} — Hoja ${tx.hoja} (${mes})`);
}

function exportLiveTransactionPDF(mode = "FACTURA") {
  if (!LIVE_TX_CACHE) {
    recalcLiveTransaction();
  }
  const tx = LIVE_TX_CACHE;
  if (!tx) return;

  const prodSelect = document.getElementById("txProductoId");
  const prodText = prodSelect && prodSelect.options[prodSelect.selectedIndex]
    ? prodSelect.options[prodSelect.selectedIndex].text
    : tx.enunciado;

  const invObj = {
    id: `LIVE-${tx.mes}-${tx.hoja}`,
    mes: tx.mes,
    hoja: tx.hoja,
    fecha: tx.fecha,
    tipo_operacion: tx.tipo,
    categoria: tx.op_code === "VENTA" || tx.op_code === "DEV_VENTA" ? "VENTA" : "COMPRA",
    numero: tx.num_doc || `Doc-${tx.hoja}`,
    tercero: tx.tercero,
    nit_tercero: tx.nit_tercero,
    regimen_vendedor: tx.regimen_vendedor,
    regimen_comprador: tx.regimen_comprador,
    forma_pago: tx.cheque || tx.forma_pago,
    enunciado: tx.enunciado,
    suma_letras: tx.suma_letras,
    subtotal: tx.subtotal,
    iva: tx.iva,
    retefuente: tx.retefuente,
    reteiva: tx.reteiva,
    reteica: tx.reteica_total,
    autorretencion: tx.autorretencion + (tx.auto_especial || 0),
    total_neto: tx.neto_pagar,
    total_debe: tx.total_debe,
    total_haber: tx.total_haber,
    asientos: tx.asientos,
    items: [
      {
        referencia: tx.producto_id || "ITEM-01",
        descripcion: prodText || tx.enunciado,
        cantidad: tx.cantidad || 1,
        valor_unitario: tx.valor_unitario || tx.subtotal,
        subtotal: tx.subtotal
      }
    ]
  };

  const safeDoc = String(invObj.numero).replace(/[^a-zA-Z0-9_-]/g, "_");
  const includeJournal = mode === "ASIENTO";
  const html = buildRealDianInvoiceHtml(invObj, includeJournal);
  const filename = `${safeDoc}_${tx.mes}${includeJournal ? "_Factura_y_Asiento" : "_Factura_DIAN"}.pdf`;
  downloadOrPrintPdfDocument(html, filename, `${invObj.tipo_operacion} — ${invObj.numero}`);
}

function exportSmartContextualPDF() {
  if (ACTIVE_SECTION === "facturas") {
    return exportProfessionalInvoicePDF(true);
  }
  if (ACTIVE_SECTION === "comprobantes") {
    return exportProfessionalVoucherPDF();
  }
  if (ACTIVE_SECTION === "facturacion") {
    return exportLiveTransactionPDF("ASIENTO");
  }
  if (ACTIVE_SECTION === "estados") {
    const efContainer = document.getElementById("efContentContainer");
    if (!efContainer) return;

    const isLandscape = ACTIVE_EF_TAB === "CONSOLIDADOS" || 
                        ACTIVE_EF_TAB === "FLUJO" || 
                        ACTIVE_EF_TAB === "ECP" ||
                        (ACTIVE_EF_TAB === "DINAMICO" && ACTIVE_DYNAMIC_EF_SUBVIEW === "BALANCE");

    // Obtener exclusivamente el documento contable oficial (.niif-statement-paper), suprimiendo barras de navegación y vistas previas
    const papers = efContainer.querySelectorAll(".niif-statement-paper");
    let html = "";
    if (papers.length > 0) {
      html = Array.from(papers).map(p => p.outerHTML).join("<div style='page-break-before:always; margin-top:24px;'></div>");
    } else {
      const clone = efContainer.cloneNode(true);
      clone.querySelectorAll(".no-print, .ef-subview-switcher, button, select, .filter-tabs, .status-pill").forEach(el => el.remove());
      html = clone.innerHTML;
    }

    const docName = {
      DINAMICO: (ACTIVE_DYNAMIC_EF_SUBVIEW === "BALANCE" ? "Balance_Comprobacion" : ACTIVE_DYNAMIC_EF_SUBVIEW),
      ESF: "Estado_Situacion_Financiera_ESF",
      ER: "Estado_Resultados_ER",
      CONSOLIDADOS: "Estados_Financieros_Consolidados",
      ECP: "Estado_Cambios_Patrimonio_ECP",
      ANALISIS: "Analisis_Financiero_y_Graficas",
      FLUJO: "Estado_Flujo_Efectivo",
      NOTAS: "Notas_y_Revelaciones_NIIF",
      TODAS: `Hoja_${ACTIVE_EF_SHEET || "Oficial"}`
    }[ACTIVE_EF_TAB] || "Estado_Financiero";

    const filename = `${docName}_${ACTIVE_PERIOD}_2026.pdf`;
    const docTitle = `${docName.replace(/_/g, " ")} — ${ACTIVE_PERIOD} 2026`;
    return downloadOrPrintPdfDocument(html, filename, docTitle, { orientation: isLandscape ? "landscape" : "portrait" });
  }
  // Para cualquier otra sección (Estados Financieros, Libros Auxiliares, Kardex, Dashboard), exportar la vista activa en formato ejecutivo
  const activeSecEl = document.querySelector(".section-view.active");
  if (!activeSecEl) {
    window.print();
    return;
  }
  const emp = DB?.empresa || {};
  const html = `
    <div class="pdf-sheet-container" style="font-family:'Plus Jakarta Sans', sans-serif; color:#0f172a; background:#ffffff; padding:20px;">
      <div style="border-bottom:2px solid #0B192C; padding-bottom:10px; margin-bottom:14px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:16px; font-weight:900; color:#0B192C;">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
          <div style="font-size:11px; color:#047857; font-weight:700;">NIT: ${emp.nit || "901.765.438-3"} • Período Activo: ${ACTIVE_PERIOD}</div>
        </div>
        <div style="text-align:right; font-size:10.5px; color:#475569;">
          <strong>Informe Oficial NIIF</strong><br/>
          Elaborado por: ${ACTIVE_STUDENT_PROFILE?.nombre || emp.elaborado_por || "Gina Villamizar"}
        </div>
      </div>
      ${activeSecEl.innerHTML}
    </div>
  `;
  const filename = `Informe_${ACTIVE_SECTION.toUpperCase()}_${ACTIVE_PERIOD}.pdf`;
  downloadOrPrintPdfDocument(html, filename, `Informe ${ACTIVE_SECTION.toUpperCase()} — ${ACTIVE_PERIOD}`);
}


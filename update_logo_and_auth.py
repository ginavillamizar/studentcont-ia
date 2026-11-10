import os
import re

base_dir = "/Users/ginavillamizar/Downloads/CONTABILIDAD"
app_path = os.path.join(base_dir, "app.js")
index_path = os.path.join(base_dir, "index.html")

# 1. Update index.html
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Add Logout/User indicator in sidebar
old_sidebar_comp = '''      <h3 id="sidebarCompanyName">ELECTROVIVIENDA S.A.S</h3>
      <p id="sidebarCompanyNit">NIT: 901.765.438-3 • Dígito 8</p>
      <p id="sidebarCompanyRegimen">RRI • Agente Retenedor y Autorretenedor</p>
    </div>'''

new_sidebar_comp = '''      <h3 id="sidebarCompanyName">ELECTROVIVIENDA S.A.S</h3>
      <p id="sidebarCompanyNit">NIT: 901.765.438-3 • Dígito 8</p>
      <p id="sidebarCompanyRegimen">RRI • Agente Retenedor y Autorretenedor</p>
      <div style="margin-top:8px; border-top:1px dashed rgba(255,255,255,0.18); padding-top:6px; display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:0.7rem; color:#CBD5E1;">Perfil: <strong id="sidebarUserProfileName" style="color:#F1F5F9;">Gina Villamizar</strong></span>
        <button onclick="logoutToWelcomeScreen()" style="background:rgba(212,175,55,0.18); border:1px solid var(--brand-gold); color:var(--brand-gold); font-size:0.68rem; font-weight:800; padding:2px 7px; border-radius:4px; cursor:pointer;" title="Cerrar sesión o cambiar de estudiante">🔒 Salir</button>
      </div>
    </div>'''

if old_sidebar_comp in html:
    html = html.replace(old_sidebar_comp, new_sidebar_comp)

# Bump cache buster in index.html
html = re.sub(r'href="styles\.css\?v=[^"]+"', 'href="styles.css?v=20261110_26"', html)
html = re.sub(r'src="app\.js\?v=[^"]+"', 'src="app.js?v=20261110_26"', html)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated index.html successfully.")

# 2. Update app.js
with open(app_path, "r", encoding="utf-8") as f:
    js = f.read()

# Update loadSavedStudentProfileFromStorage
old_load_profile = '''function loadSavedStudentProfileFromStorage() {
  ACTIVE_STUDENT_PROFILE = {
    id: "gina_villamizar",
    nombre: "Gina Villamizar",
    programa: "Contadora Titular • NIIF Grupo 2",
    rol: "Titular"
  };
  document.getElementById("welcomeAuthOverlay")?.classList.add("hidden");
  updateStudentProfileUI();
}'''

new_load_profile = '''function loadSavedStudentProfileFromStorage() {
  const saved = localStorage.getItem("studentcont_active_profile");
  if (saved) {
    try {
      ACTIVE_STUDENT_PROFILE = JSON.parse(saved);
      document.getElementById("welcomeAuthOverlay")?.classList.add("hidden");
      updateStudentProfileUI();
      return;
    } catch (e) {}
  }
  // Si es la primera vez que se entra (ej. desde el enlace web publicado), mostrar la pantalla de bienvenida y login
  openWelcomeLoginOverlay();
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
window.logoutToWelcomeScreen = logoutToWelcomeScreen;'''

if old_load_profile in js:
    js = js.replace(old_load_profile, new_load_profile)
    print("Updated loadSavedStudentProfileFromStorage and added loginAsGinaDirect")
else:
    print("Could not find exact old_load_profile in app.js")

# Add renderCorporateHeaderBoxHtml
header_box_helper = '''
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
'''

if "renderCorporateHeaderBoxHtml" not in js:
    # Insert helper before renderExecutiveNIIFStatementHtml
    pos = js.find("function renderExecutiveNIIFStatementHtml")
    if pos != -1:
        js = js[:pos] + header_box_helper + "\n" + js[pos:]
        print("Added renderCorporateHeaderBoxHtml helper")

with open(app_path, "w", encoding="utf-8") as f:
    f.write(js)
print("Updated app.js successfully.")

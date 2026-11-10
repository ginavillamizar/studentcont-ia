import os

app_path = '/Users/ginavillamizar/Downloads/CONTABILIDAD/app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. ESF and ER
old_esf_header = '''      <div class="niif-header-box">
        <div class="niif-company-title">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
        <div class="niif-company-sub">NIT: ${emp.nit || "901.765.438-3"} • ${emp.regimen || "RRI — Agente Autorretenedor de Renta"}</div>
        <div class="niif-statement-badge">
          <div class="niif-statement-name">${statementTitle || "ESTADO FINANCIERO OFICIAL NIIF"}</div>
          <span class="niif-period-tag">Al corte del período: ${month} 2026</span>
          <span style="font-size:0.7rem; color:#94A3B8; display:block; margin-top:3px;">Cifras en Pesos Colombianos (COP) • NIIF para las PYMES (Grupo 2)</span>
        </div>
      </div>'''

new_esf_header = '${renderCorporateHeaderBoxHtml(statementTitle || "ESTADO FINANCIERO OFICIAL NIIF", `Al corte del período: ${month} 2026`, "Cifras en Pesos Colombianos (COP) • NIIF para las PYMES (Grupo 2)")}'

if old_esf_header in js:
    js = js.replace(old_esf_header, new_esf_header)
    print('Updated ESF/ER header')

# 2. Consolidados
old_cons_header = '''      <div class="niif-header-box">
        <div class="niif-company-title">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
        <div class="niif-company-sub">NIT: ${emp.nit || "901.765.438-3"} • ${emp.regimen || "RRI — Agente Autorretenedor de Renta"}</div>
        <div class="niif-statement-badge">
          <div class="niif-statement-name">${statementTitle || "ESTADO FINANCIERO CONSOLIDADO NIIF"}</div>
          <span class="niif-period-tag">Corte Consolidado Comparativo — ${month} 2026</span>
          <span style="font-size:0.7rem; color:#94A3B8; display:block; margin-top:3px;">Cifras en Pesos Colombianos (COP) • NIIF para las PYMES (Grupo 2) • Variaciones y Sumas Corridas</span>
        </div>
      </div>'''

new_cons_header = '${renderCorporateHeaderBoxHtml(statementTitle || "ESTADO FINANCIERO CONSOLIDADO NIIF", `Corte Consolidado Comparativo — ${month} 2026`, "Cifras en Pesos Colombianos (COP) • NIIF para las PYMES (Grupo 2) • Variaciones y Sumas Corridas")}'

if old_cons_header in js:
    js = js.replace(old_cons_header, new_cons_header)
    print('Updated Consolidados header')

# 3. ECP
old_ecp_header = '''      <div class="niif-header-box">
        <div class="niif-company-title">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
        <div class="niif-company-sub">NIT: ${emp.nit || "901.765.438-3"} • ${emp.regimen || "RRI — Agente Autorretenedor de Renta"}</div>
        <div class="niif-statement-badge">
          <div class="niif-statement-name">ESTADO DE CAMBIOS EN EL PATRIMONIO (ECP)</div>
          <span class="niif-period-tag">${periodText}</span>
          <span style="font-size:0.7rem; color:#94A3B8; display:block; margin-top:3px;">
            NIIF para las PYMES (Sección 6) • Cifras en Pesos Colombianos (COP) • Sumas Corridas
          </span>
        </div>
      </div>'''

new_ecp_header = '${renderCorporateHeaderBoxHtml("ESTADO DE CAMBIOS EN EL PATRIMONIO (ECP)", periodText, "NIIF para las PYMES (Sección 6) • Cifras en Pesos Colombianos (COP) • Sumas Corridas")}'

if old_ecp_header in js:
    js = js.replace(old_ecp_header, new_ecp_header)
    print('Updated ECP header')

# 4. Flujo
old_flujo_header = '''      <div class="niif-header-box">
        <div class="niif-company-title">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
        <div class="niif-company-sub">NIT: ${emp.nit || "901.765.438-3"} • ${emp.regimen || "RRI — Agente Autorretenedor de Renta"}</div>
        <div class="niif-statement-badge">
          <div class="niif-statement-name">ESTADO DE FLUJOS DE EFECTIVO — MÉTODO INDIRECTO</div>
          <span class="niif-period-tag">Período Contable: ${month} 2026</span>
          <span style="font-size:0.7rem; color:#94A3B8; display:block; margin-top:3px;">
            NIIF para las PYMES (Sección 7) • Cifras en Pesos Colombianos (COP) • Sumas Corridas
          </span>
        </div>
      </div>'''

new_flujo_header = '${renderCorporateHeaderBoxHtml("ESTADO DE FLUJOS DE EFECTIVO — MÉTODO INDIRECTO", `Período Contable: ${month} 2026`, "NIIF para las PYMES (Sección 7) • Cifras en Pesos Colombianos (COP) • Sumas Corridas")}'

if old_flujo_header in js:
    js = js.replace(old_flujo_header, new_flujo_header)
    print('Updated Flujo header')

# 5. Analisis
old_analisis_header = '''      <!-- Encabezado Corporativo Oficial -->
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
      </div>'''

new_analisis_header = '${renderCorporateHeaderBoxHtml("📊 INFORME EJECUTIVO DE ANÁLISIS FINANCIERO & GRÁFICAS INTERACTIVAS", "Período Comparativo: MARZO 2026 vs ABRIL 2026", "Diagnóstico Financiero Integral NIIF para las PYMES • Indicadores de Liquidez, Endeudamiento y Rentabilidad")}'

if old_analisis_header in js:
    js = js.replace(old_analisis_header, new_analisis_header)
    print('Updated Analisis header')

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(js)
print('Successfully applied header updates in app.js')

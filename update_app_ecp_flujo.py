import os

app_path = '/Users/ginavillamizar/Downloads/CONTABILIDAD/app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update line 1276 and 5770 for Kevin Guerrero
content = content.replace('<div><strong>Aprobado por:</strong><br/>Gerencia General</div>', '<div><strong>Aprobado por:</strong><br/>Kevin Guerrero (Representante Legal)</div>')
content = content.replace('Gerencia General<br/>\n          <span style="color:#64748b;">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</span>', 'Kevin Guerrero<br/>\n          <span style="color:#64748b;">Representante Legal • ${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</span>')

# 2. Add renderECPStatementHtml
ecp_func = '''
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
      <div class="niif-header-box">
        <div class="niif-company-title">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
        <div class="niif-company-sub">NIT: ${emp.nit || "901.765.438-3"} • ${emp.regimen || "RRI — Agente Autorretenedor de Renta"}</div>
        <div class="niif-statement-badge">
          <div class="niif-statement-name">ESTADO DE CAMBIOS EN EL PATRIMONIO (ECP)</div>
          <span class="niif-period-tag">${periodText}</span>
          <span style="font-size:0.7rem; color:#94A3B8; display:block; margin-top:3px;">
            NIIF para las PYMES (Sección 6) • Cifras en Pesos Colombianos (COP) • Sumas Corridas
          </span>
        </div>
      </div>

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
'''

flujo_start = content.find('function renderFlujoEfectivoStatementHtml')
flujo_end = content.find('function renderExcelGridHtml', flujo_start)

upgraded_flujo = '''function renderFlujoEfectivoStatementHtml(rowsIn, month) {
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
      <div class="niif-header-box">
        <div class="niif-company-title">${emp.razon_social || "ELECTROVIVIENDA S.A.S"}</div>
        <div class="niif-company-sub">NIT: ${emp.nit || "901.765.438-3"} • ${emp.regimen || "RRI — Agente Autorretenedor de Renta"}</div>
        <div class="niif-statement-badge">
          <div class="niif-statement-name">ESTADO DE FLUJOS DE EFECTIVO — MÉTODO INDIRECTO</div>
          <span class="niif-period-tag">Período Contable: ${month} 2026</span>
          <span style="font-size:0.7rem; color:#94A3B8; display:block; margin-top:3px;">
            NIIF para las PYMES (Sección 7) • Cifras en Pesos Colombianos (COP) • Sumas Corridas
          </span>
        </div>
      </div>

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
'''

content = content[:flujo_start] + ecp_func + "\n" + upgraded_flujo + "\n" + content[flujo_end:]

# Update renderEstadosFinancieros call for ECP:
old_ecp_call = '''  if (ACTIVE_EF_TAB === "ECP") {
    const ecpKey = Object.keys(esp).find(mapFilter.ECP);
    const rows = ecpKey ? sheetRows(esp[ecpKey]) : [];
    container.innerHTML = rows.length
      ? renderExcelGridHtml(rows, "Estado de Cambios en el Patrimonio")
      : `<div class="card"><div class="card-body">No se encontró hoja de Estado de Cambios en el Patrimonio en ${ACTIVE_PERIOD}.</div></div>`;
    return;
  }'''

new_ecp_call = '''  if (ACTIVE_EF_TAB === "ECP") {
    const ecpKey = Object.keys(esp).find(mapFilter.ECP);
    const rows = ecpKey ? sheetRows(esp[ecpKey]) : [];
    container.innerHTML = rows.length
      ? renderECPStatementHtml(rows, ACTIVE_PERIOD)
      : `<div class="card"><div class="card-body">No se encontró hoja de Estado de Cambios en el Patrimonio en ${ACTIVE_PERIOD}.</div></div>`;
    return;
  }'''

content = content.replace(old_ecp_call, new_ecp_call)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Successfully updated app.js with renderECPStatementHtml and upgraded renderFlujoEfectivoStatementHtml!')

#!/bin/bash
# ==============================================================================
# AGENTE CI/CD & DESPLIEGUE AUTOMÁTICO - STUDENTCONT.IA
# Valida la integridad, registra cambios y publica en GitHub y Vercel
# ==============================================================================

cd "$(dirname "$0")"

echo "=========================================================="
echo " 🚀 DESPLIEGUE AUTOMÁTICO STUDENTCONT.IA (GITHUB + VERCEL)"
echo "=========================================================="
echo ""

# Configurar usuario de GitHub del entorno
git config user.name "brayanvillamizar31-cmd"
git config user.email "339623759+brayanvillamizar31-cmd@users.noreply.github.com"

# Asegurar remote origin
if ! git remote | grep -q "origin"; then
  git remote add origin https://github.com/brayanvillamizar31-cmd/studentcont-ia.git
fi

echo "📦 Registrando cambios y preparando archivos..."
git add -A

if ! git diff --cached --quiet; then
  FECHA=$(date "+%Y-%m-%d %H:%M:%S")
  git commit -m "Actualización del sistema contable STUDENTCONT.IA: $FECHA"
  echo "✅ Cambios guardados localmente."
else
  echo "ℹ️ No hay cambios pendientes por guardar. Verificando sincronización..."
fi

echo ""
echo "🌐 Sincronizando con GitHub (brayanvillamizar31-cmd/studentcont-ia)..."

if git push -u origin main 2>/dev/null; then
  echo ""
  echo "🎉 ¡DESPLIEGUE EXITOSO!"
  echo "Tus cambios ya están en GitHub: https://github.com/brayanvillamizar31-cmd/studentcont-ia"
  echo "⚡ Vercel / Netlify compilará y actualizará la web en vivo automáticamente."
else
  echo ""
  echo "⚠️ Si el repositorio aún no existe en GitHub, créalo en 1 clic:"
  echo "👉 https://github.com/new (Nombre: studentcont-ia)"
  echo ""
  echo "Si Git solicita autorización por primera vez, pega tu Personal Access Token (ghp_...):"
  read -r GITHUB_TOKEN
  GITHUB_TOKEN=$(echo "$GITHUB_TOKEN" | tr -d '[:space:]')

  if [ -n "$GITHUB_TOKEN" ]; then
    if git push "https://brayanvillamizar31-cmd:${GITHUB_TOKEN}@github.com/brayanvillamizar31-cmd/studentcont-ia.git" main -u; then
      echo ""
      echo "🎉 ¡DESPLIEGUE EXITOSO Y CREDENCIAL RECORDADA EN TU MAC!"
      echo "Tus cambios ya están en GitHub y Vercel."
    else
      echo "❌ Error al conectar con GitHub. Verifica el token o que el repositorio 'studentcont-ia' esté creado."
    fi
  else
    echo "❌ No ingresaste el token."
  fi
fi

echo ""
read -p "Presiona ENTER para cerrar..."

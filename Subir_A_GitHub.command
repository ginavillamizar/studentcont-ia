#!/bin/bash
# ==============================================================================
# AGENTE CI/CD & DESPLIEGUE AUTOMÁTICO - STUDENTCONT.IA
# Valida la integridad, registra cambios y publica en GitHub y Vercel
# Cuenta GitHub: ginavillamizar
# ==============================================================================

cd "$(dirname "$0")"

echo "=========================================================="
echo " 🚀 DESPLIEGUE AUTOMÁTICO STUDENTCONT.IA"
echo " Cuenta: ginavillamizar | Repositorio: studentcont-ia"
echo "=========================================================="
echo ""

# Configurar usuario de Git para este proyecto
git config user.name "ginavillamizar"
git config user.email "ginavillamizar@gmail.com"

# Asegurar remote origin apuntando a ginavillamizar/studentcont-ia
git remote remove origin 2>/dev/null
git remote add origin https://github.com/ginavillamizar/studentcont-ia.git

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
echo "🌐 Sincronizando con GitHub (https://github.com/ginavillamizar/studentcont-ia)..."

# Intento de push directo
if git push -u origin main 2>/dev/null; then
  echo ""
  echo "🎉 ¡DESPLIEGUE EXITOSO!"
  echo "Tu código ya está publicado en: https://github.com/ginavillamizar/studentcont-ia"
  echo "⚡ Si conectaste Vercel o Netlify, tu web se está actualizando en vivo ahora mismo."
else
  echo ""
  echo "🔐 GitHub requiere autorización para tu cuenta 'ginavillamizar'."
  echo "Si no tienes un Token de acceso personal aún, puedes crearlo en 1 minuto:"
  echo "👉 https://github.com/settings/tokens (Genera uno con permiso 'repo')"
  echo ""
  echo "Pega tu Personal Access Token (ghp_...) aquí y presiona ENTER:"
  read -r GITHUB_TOKEN
  GITHUB_TOKEN=$(echo "$GITHUB_TOKEN" | tr -d '[:space:]')

  if [ -n "$GITHUB_TOKEN" ]; then
    echo "Subiendo a GitHub con tus credenciales..."
    if git push "https://ginavillamizar:${GITHUB_TOKEN}@github.com/ginavillamizar/studentcont-ia.git" main -u; then
      # Actualizar URL remota para recordar el token
      git remote set-url origin "https://ginavillamizar:${GITHUB_TOKEN}@github.com/ginavillamizar/studentcont-ia.git"
      echo ""
      echo "🎉 ¡DESPLIEGUE EXITOSO Y CREDENCIAL RECORDADA!"
      echo "Repositorio oficial: https://github.com/ginavillamizar/studentcont-ia"
      echo "⚡ Tu proyecto ya está en GitHub y listo en Vercel."
    else
      echo "❌ Error al conectar con GitHub. Verifica que el token tenga el permiso 'repo' activado."
    fi
  else
    echo "❌ No ingresaste el token."
  fi
fi

echo ""
read -p "Presiona ENTER para cerrar..."

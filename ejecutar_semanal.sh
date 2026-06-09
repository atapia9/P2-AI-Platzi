#!/bin/bash
# ─────────────────────────────────────────────────────────────────
# Script de ejecución semanal - Infografías Educativas
# Proyecto 2 Platzi Challenge
#
# Configurar en cron:
#   crontab -e
#   0 9 * * 1 /ruta/al/proyecto/ejecutar_semanal.sh  # Cada lunes a las 9am
# ─────────────────────────────────────────────────────────────────

# Directorio del proyecto (ajustar según tu instalación)
PROYECTO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$PROYECTO_DIR/infografias_output/$(date +%Y-semana%V)"
LOG_FILE="$PROYECTO_DIR/logs/ejecucion_$(date +%Y%m%d_%H%M%S).log"

# Crear directorio de logs
mkdir -p "$PROYECTO_DIR/logs"

echo "========================================" | tee -a "$LOG_FILE"
echo "🎨 Generador de Infografías Educativas" | tee -a "$LOG_FILE"
echo "📅 Fecha: $(date '+%d/%m/%Y %H:%M:%S')" | tee -a "$LOG_FILE"
echo "📁 Output: $OUTPUT_DIR" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# Verificar API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "❌ ERROR: Variable ANTHROPIC_API_KEY no configurada" | tee -a "$LOG_FILE"
  echo "   Agrega al .bashrc o .zshrc: export ANTHROPIC_API_KEY='tu-key'" | tee -a "$LOG_FILE"
  exit 1
fi

# Ejecutar generador
cd "$PROYECTO_DIR" && python3 generador_infografias.py \
  --batch temas.yaml \
  --output "$OUTPUT_DIR" \
  2>&1 | tee -a "$LOG_FILE"

# Resultado
if [ $? -eq 0 ]; then
  echo "" | tee -a "$LOG_FILE"
  echo "✅ Completado exitosamente" | tee -a "$LOG_FILE"
  echo "📂 Ver resultados en: $OUTPUT_DIR" | tee -a "$LOG_FILE"
else
  echo "❌ Error durante la ejecución. Revisar log: $LOG_FILE" | tee -a "$LOG_FILE"
fi

# 🧩 Generador Automático de Infografías Educativas

> **Proyecto 2 — Platzi Challenge: Automatiza el flujo que nadie quiere hacer**

Genera infografías educativas completas con diseño profesional a partir de un tema, usando Claude AI como motor de contenido. Un solo comando produce un archivo HTML listo para compartir, imprimir o publicar — sin tocar Canva, sin copiar/pegar, sin formatear manualmente.

---

## Demo

```
python generador_infografias.py --tema "Docker y Contenedores"
```

**Output:** `infografias_output/infografia_docker_y_contenedores_20260608_220012.html`

Cada infografía incluye: título impactante · resumen · 5 conceptos clave · 3 estadísticas · 5 pasos para empezar · dato curioso · 3 recursos recomendados · cita inspiradora · tags.

---

## El problema que resuelve

Crear una infografía educativa de calidad toma entre **2 y 3 horas**: investigar el tema, estructurar la información, redactar copy conciso, diseñarlo en Canva o Figma. Si tienes que hacer esto cada semana para varios temas, rápidamente se convierte en el trabajo que todos posponen.

Este proyecto lo lleva a **~20 segundos por infografía**, con cero intervención manual en el proceso de creación.

---

## Instalación

```bash
pip install anthropic pyyaml
export ANTHROPIC_API_KEY="sk-ant-..."   # console.anthropic.com
```

---

## Uso

```bash
# Tema único
python generador_infografias.py --tema "Machine Learning"
python generador_infografias.py --tema "Docker" --nivel principiante
python generador_infografias.py --tema "APIs REST" --nivel avanzado --output ./mis_infografias

# Batch desde archivo YAML
python generador_infografias.py --batch temas.yaml
python generador_infografias.py --batch temas.yaml --output ./mis_infografias

# Automatización semanal con cron (lunes, miércoles y viernes a las 10pm)
chmod +x ejecutar_semanal.sh
crontab -e
# → 0 22 * * 1,3,5 /ruta/al/proyecto/ejecutar_semanal.sh
```

**Niveles disponibles:** `principiante` · `intermedio` · `avanzado`

---

## Resultado

| | Manual | Automatizado |
|---|---|---|
| Tiempo por infografía | 2–3 horas | ~20 segundos |
| Batch de 8 temas | ~1 día | ~3 minutos |
| Intervención humana | Todo el proceso | Solo editar `temas.yaml` |
| Consistencia visual | Variable | 100% uniforme |

**Ahorro estimado: 95% del tiempo.**

---

## Archivos

```
.
├── generador_infografias.py   # Script principal
├── temas.yaml                 # Lista de temas para batch
├── ejecutar_semanal.sh        # Script para cron
└── infografias_output/        # Carpeta de outputs (se crea automáticamente)
    ├── index.html             # Índice navegable (modo batch)
    └── infografia_*.html      # Infografías generadas
```

---

## Código

### `generador_infografias.py`

```python
#!/usr/bin/env python3
"""
Generador Automático de Infografías Educativas
Proyecto 2 - Automatiza el flujo que nadie quiere hacer
Platzi Challenge

Uso:
    python generador_infografias.py --tema "Machine Learning"
    python generador_infografias.py --batch temas.yaml
    python generador_infografias.py --batch temas.yaml --output ./infografias

Requiere:
    pip install anthropic pyyaml
    export ANTHROPIC_API_KEY="tu-api-key"
"""

import anthropic
import json
import os
import sys
import argparse
import yaml
import re
from datetime import datetime
from pathlib import Path

# ─── CONFIG ────────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = "claude-opus-4-6"
OUTPUT_DIR = Path("./infografias_output")

# ─── PROMPT PARA CLAUDE ────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Eres un experto en pedagogía y diseño instruccional.
Tu tarea es generar contenido educativo estructurado para infografías visuales.
SIEMPRE responde ÚNICAMENTE con JSON válido, sin texto adicional, sin markdown, sin bloques de código."""

def build_user_prompt(tema: str, nivel: str = "intermedio", idioma: str = "español") -> str:
    return f"""Genera contenido educativo estructurado para una infografía sobre: "{tema}"

Nivel: {nivel}
Idioma: {idioma}

Devuelve SOLO este JSON (sin markdown, sin bloques de código):

{{
  "titulo": "título impactante de la infografía",
  "subtitulo": "descripción breve de 1 línea",
  "emoji_principal": "emoji representativo",
  "color_tema": "uno de: azul|verde|morado|naranja|rojo|turquesa",
  "resumen": "párrafo de 2-3 oraciones que explica el tema",
  "conceptos_clave": [
    {{
      "icono": "emoji",
      "nombre": "nombre del concepto",
      "descripcion": "explicación en 1-2 oraciones"
    }}
  ],
  "estadisticas": [
    {{
      "valor": "número o porcentaje llamativo",
      "descripcion": "qué representa este dato",
      "fuente": "fuente o contexto"
    }}
  ],
  "pasos_o_tips": [
    {{
      "numero": 1,
      "titulo": "título del paso/tip",
      "detalle": "descripción breve"
    }}
  ],
  "dato_curioso": "hecho sorprendente o poco conocido sobre el tema",
  "recursos_recomendados": [
    {{
      "tipo": "Libro|Curso|Herramienta|Comunidad",
      "nombre": "nombre del recurso",
      "descripcion": "por qué es útil"
    }}
  ],
  "cita_inspiradora": {{
    "texto": "cita relevante al tema",
    "autor": "nombre del autor"
  }},
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
}}

Incluye exactamente: 4-5 conceptos_clave, 3 estadisticas, 4-5 pasos_o_tips, 3 recursos_recomendados."""


# ─── GENERACIÓN DE CONTENIDO CON CLAUDE ────────────────────────────────────────

def generar_contenido(tema: str, nivel: str = "intermedio", idioma: str = "español") -> dict:
    if not ANTHROPIC_API_KEY:
        raise ValueError("❌ Variable ANTHROPIC_API_KEY no configurada. Ejecuta: export ANTHROPIC_API_KEY='tu-key'")

    cliente = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    print(f"  🤖 Consultando Claude para: '{tema}'...")

    mensaje = cliente.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(tema, nivel, idioma)}]
    )

    texto = mensaje.content[0].text.strip()
    texto = re.sub(r'^```(?:json)?\s*', '', texto)
    texto = re.sub(r'\s*```$', '', texto)

    try:
        datos = json.loads(texto)
        print(f"  ✅ Contenido generado correctamente")
        return datos
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Error parseando JSON: {e}")
        raise


# ─── TEMPLATE HTML ─────────────────────────────────────────────────────────────

COLORES = {
    "azul":     {"primario": "#1e40af", "claro": "#dbeafe", "acento": "#3b82f6", "gradiente": "linear-gradient(135deg, #1e3a8a, #3b82f6)"},
    "verde":    {"primario": "#15803d", "claro": "#dcfce7", "acento": "#22c55e", "gradiente": "linear-gradient(135deg, #14532d, #22c55e)"},
    "morado":   {"primario": "#7e22ce", "claro": "#f3e8ff", "acento": "#a855f7", "gradiente": "linear-gradient(135deg, #581c87, #a855f7)"},
    "naranja":  {"primario": "#c2410c", "claro": "#ffedd5", "acento": "#f97316", "gradiente": "linear-gradient(135deg, #9a3412, #f97316)"},
    "rojo":     {"primario": "#be123c", "claro": "#ffe4e6", "acento": "#f43f5e", "gradiente": "linear-gradient(135deg, #9f1239, #f43f5e)"},
    "turquesa": {"primario": "#0f766e", "claro": "#ccfbf1", "acento": "#14b8a6", "gradiente": "linear-gradient(135deg, #134e4a, #14b8a6)"},
}

def generar_html(datos: dict, tema: str, timestamp: str) -> str:
    color_key = datos.get("color_tema", "azul").lower()
    if color_key not in COLORES:
        color_key = "azul"
    c = COLORES[color_key]

    conceptos_html = ""
    for concepto in datos.get("conceptos_clave", []):
        conceptos_html += f"""
        <div class="concepto-card">
            <div class="concepto-icono">{concepto.get('icono', '📌')}</div>
            <div class="concepto-contenido">
                <h4>{concepto.get('nombre', '')}</h4>
                <p>{concepto.get('descripcion', '')}</p>
            </div>
        </div>"""

    stats_html = ""
    for stat in datos.get("estadisticas", []):
        stats_html += f"""
        <div class="stat-card">
            <div class="stat-valor">{stat.get('valor', '')}</div>
            <div class="stat-desc">{stat.get('descripcion', '')}</div>
            <div class="stat-fuente">{stat.get('fuente', '')}</div>
        </div>"""

    pasos_html = ""
    for paso in datos.get("pasos_o_tips", []):
        pasos_html += f"""
        <div class="paso-item">
            <div class="paso-numero">{paso.get('numero', '')}</div>
            <div class="paso-contenido">
                <strong>{paso.get('titulo', '')}</strong>
                <span>{paso.get('detalle', '')}</span>
            </div>
        </div>"""

    recursos_html = ""
    iconos_tipo = {"Libro": "📚", "Curso": "🎓", "Herramienta": "🛠️", "Comunidad": "👥"}
    for recurso in datos.get("recursos_recomendados", []):
        icono = iconos_tipo.get(recurso.get("tipo", ""), "🔗")
        recursos_html += f"""
        <div class="recurso-item">
            <span class="recurso-tipo">{icono} {recurso.get('tipo', '')}</span>
            <strong>{recurso.get('nombre', '')}</strong>
            <span>{recurso.get('descripcion', '')}</span>
        </div>"""

    tags_html = " ".join([f'<span class="tag">#{tag}</span>' for tag in datos.get("tags", [])])
    cita = datos.get("cita_inspiradora", {})

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{datos.get('titulo', tema)} - Infografía Educativa</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f1f5f9; color: #1e293b; }}
  .infografia {{ max-width: 900px; margin: 0 auto; background: white; box-shadow: 0 20px 60px rgba(0,0,0,0.15); }}
  .header {{ background: {c['gradiente']}; color: white; padding: 48px 40px 40px; position: relative; overflow: hidden; }}
  .header::before {{ content: ''; position: absolute; top: -50px; right: -50px; width: 250px; height: 250px; border-radius: 50%; background: rgba(255,255,255,0.08); }}
  .header::after {{ content: ''; position: absolute; bottom: -80px; left: -30px; width: 300px; height: 300px; border-radius: 50%; background: rgba(255,255,255,0.05); }}
  .header-emoji {{ font-size: 64px; display: block; margin-bottom: 16px; }}
  .header h1 {{ font-size: 2.4rem; font-weight: 800; line-height: 1.2; margin-bottom: 12px; position: relative; z-index: 1; }}
  .header .subtitulo {{ font-size: 1.1rem; opacity: 0.9; position: relative; z-index: 1; }}
  .header-meta {{ margin-top: 24px; font-size: 0.8rem; opacity: 0.7; position: relative; z-index: 1; }}
  .resumen {{ background: {c['claro']}; border-left: 5px solid {c['acento']}; padding: 24px 32px; margin: 0; font-size: 1.05rem; line-height: 1.7; color: #334155; }}
  .seccion {{ padding: 36px 40px; border-bottom: 1px solid #f1f5f9; }}
  .seccion-titulo {{ display: flex; align-items: center; gap: 10px; font-size: 1.2rem; font-weight: 700; color: {c['primario']}; margin-bottom: 24px; text-transform: uppercase; letter-spacing: 0.05em; }}
  .seccion-titulo::after {{ content: ''; flex: 1; height: 2px; background: {c['claro']}; }}
  .conceptos-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  .concepto-card {{ display: flex; gap: 14px; align-items: flex-start; background: #f8fafc; border-radius: 12px; padding: 16px; border: 1px solid #e2e8f0; transition: transform 0.2s; }}
  .concepto-card:hover {{ transform: translateY(-2px); border-color: {c['acento']}; }}
  .concepto-icono {{ font-size: 2rem; flex-shrink: 0; }}
  .concepto-contenido h4 {{ font-size: 0.95rem; font-weight: 700; color: #1e293b; margin-bottom: 4px; }}
  .concepto-contenido p {{ font-size: 0.85rem; color: #64748b; line-height: 1.5; }}
  .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
  .stat-card {{ text-align: center; background: {c['gradiente']}; color: white; border-radius: 16px; padding: 24px 16px; }}
  .stat-valor {{ font-size: 2.5rem; font-weight: 900; display: block; margin-bottom: 8px; }}
  .stat-desc {{ font-size: 0.85rem; opacity: 0.95; font-weight: 600; margin-bottom: 6px; }}
  .stat-fuente {{ font-size: 0.72rem; opacity: 0.7; }}
  .pasos-lista {{ display: flex; flex-direction: column; gap: 12px; }}
  .paso-item {{ display: flex; gap: 16px; align-items: flex-start; }}
  .paso-numero {{ width: 36px; height: 36px; border-radius: 50%; background: {c['gradiente']}; color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.95rem; flex-shrink: 0; margin-top: 2px; }}
  .paso-contenido {{ background: #f8fafc; border-radius: 10px; padding: 12px 16px; flex: 1; border: 1px solid #e2e8f0; }}
  .paso-contenido strong {{ display: block; font-size: 0.95rem; color: #1e293b; margin-bottom: 4px; }}
  .paso-contenido span {{ font-size: 0.85rem; color: #64748b; }}
  .dato-curioso {{ background: {c['gradiente']}; color: white; border-radius: 16px; padding: 28px 32px; margin: 0 40px 36px; position: relative; overflow: hidden; }}
  .dato-curioso::before {{ content: '💡'; position: absolute; right: 24px; top: 50%; transform: translateY(-50%); font-size: 4rem; opacity: 0.2; }}
  .dato-curioso-label {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.8; margin-bottom: 8px; }}
  .dato-curioso-texto {{ font-size: 1.05rem; font-weight: 600; line-height: 1.6; }}
  .recursos-lista {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }}
  .recurso-item {{ background: #f8fafc; border-radius: 12px; padding: 16px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; gap: 4px; }}
  .recurso-tipo {{ font-size: 0.75rem; color: {c['acento']}; font-weight: 700; text-transform: uppercase; }}
  .recurso-item strong {{ font-size: 0.9rem; color: #1e293b; }}
  .recurso-item span {{ font-size: 0.8rem; color: #64748b; }}
  .cita {{ background: #f8fafc; border-left: 4px solid {c['acento']}; margin: 0 40px 36px; padding: 24px 32px; border-radius: 0 12px 12px 0; }}
  .cita-texto {{ font-size: 1.1rem; font-style: italic; color: #334155; line-height: 1.7; margin-bottom: 8px; }}
  .cita-autor {{ font-size: 0.85rem; color: {c['primario']}; font-weight: 700; }}
  .tags-section {{ padding: 24px 40px; background: #f8fafc; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
  .tags-label {{ font-size: 0.8rem; color: #94a3b8; font-weight: 600; margin-right: 4px; }}
  .tag {{ background: {c['claro']}; color: {c['primario']}; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }}
  .footer {{ background: #1e293b; color: #94a3b8; padding: 20px 40px; font-size: 0.8rem; display: flex; justify-content: space-between; align-items: center; }}
  .footer strong {{ color: white; }}
  @media (max-width: 640px) {{
    .conceptos-grid, .stats-grid, .recursos-lista {{ grid-template-columns: 1fr; }}
    .header h1 {{ font-size: 1.8rem; }}
  }}
  @media print {{
    body {{ background: white; }}
    .infografia {{ box-shadow: none; }}
  }}
</style>
</head>
<body>
<div class="infografia">
  <div class="header">
    <span class="header-emoji">{datos.get('emoji_principal', '📚')}</span>
    <h1>{datos.get('titulo', tema)}</h1>
    <p class="subtitulo">{datos.get('subtitulo', '')}</p>
    <p class="header-meta">Generado automáticamente el {timestamp} · Nivel: Intermedio</p>
  </div>
  <div class="resumen">{datos.get('resumen', '')}</div>
  <div class="seccion">
    <div class="seccion-titulo">🧠 Conceptos Clave</div>
    <div class="conceptos-grid">{conceptos_html}</div>
  </div>
  <div class="seccion">
    <div class="seccion-titulo">📊 En Números</div>
    <div class="stats-grid">{stats_html}</div>
  </div>
  <div class="seccion">
    <div class="seccion-titulo">🚀 Pasos para Empezar</div>
    <div class="pasos-lista">{pasos_html}</div>
  </div>
  <div class="dato-curioso">
    <div class="dato-curioso-label">¿Sabías que...?</div>
    <div class="dato-curioso-texto">{datos.get('dato_curioso', '')}</div>
  </div>
  <div class="seccion">
    <div class="seccion-titulo">📖 Recursos Recomendados</div>
    <div class="recursos-lista">{recursos_html}</div>
  </div>
  <div class="cita">
    <div class="cita-texto">"{cita.get('texto', '')}"</div>
    <div class="cita-autor">— {cita.get('autor', '')}</div>
  </div>
  <div class="tags-section">
    <span class="tags-label">Tags:</span>
    {tags_html}
  </div>
  <div class="footer">
    <span>Generado con <strong>Claude AI</strong> · Proyecto 2 Platzi Challenge</span>
    <span>Tema: <strong>{tema}</strong></span>
  </div>
</div>
</body>
</html>"""


# ─── PROCESAMIENTO DE UN TEMA ──────────────────────────────────────────────────

def procesar_tema(tema: str, nivel: str = "intermedio", idioma: str = "español",
                  output_dir: Path = OUTPUT_DIR) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    nombre_archivo = tema.lower().replace(" ", "_").replace("/", "-")[:50]
    nombre_archivo = re.sub(r'[^\w\-]', '', nombre_archivo)
    ts_corto = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_dir.mkdir(parents=True, exist_ok=True)
    ruta_salida = output_dir / f"infografia_{nombre_archivo}_{ts_corto}.html"

    datos = generar_contenido(tema, nivel, idioma)
    html = generar_html(datos, tema, timestamp)

    ruta_salida.write_text(html, encoding="utf-8")
    print(f"  💾 Guardado: {ruta_salida}")
    return ruta_salida


# ─── PROCESAMIENTO BATCH ───────────────────────────────────────────────────────

def procesar_batch(archivo_yaml: str, output_dir: Path = OUTPUT_DIR) -> list[Path]:
    with open(archivo_yaml, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    temas = config.get("temas", [])
    archivos_generados = []

    print(f"\n📋 Procesando {len(temas)} temas desde {archivo_yaml}...\n")

    for i, item in enumerate(temas, 1):
        if isinstance(item, str):
            tema, nivel, idioma = item, "intermedio", "español"
        else:
            tema = item.get("tema", "")
            nivel = item.get("nivel", "intermedio")
            idioma = item.get("idioma", "español")

        print(f"[{i}/{len(temas)}] 🎨 Generando infografía: {tema}")
        try:
            ruta = procesar_tema(tema, nivel, idioma, output_dir)
            archivos_generados.append(ruta)
            print()
        except Exception as e:
            print(f"  ❌ Error con '{tema}': {e}\n")

    return archivos_generados


def generar_indice(archivos: list[Path], output_dir: Path):
    cards = ""
    for ruta in archivos:
        nombre = ruta.stem.replace("infografia_", "").replace("_", " ").title()
        nombre = re.sub(r'\d{8} \d{6}$', '', nombre).strip()
        cards += f"""
    <a href="{ruta.name}" class="card">
      <div class="card-icon">📄</div>
      <div class="card-name">{nombre}</div>
      <div class="card-meta">Ver infografía →</div>
    </a>"""

    html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><title>Infografías Educativas</title>
<style>
  body {{ font-family: 'Segoe UI', sans-serif; background: #f1f5f9; color: #1e293b; padding: 40px; }}
  h1 {{ font-size: 2rem; margin-bottom: 8px; }}
  p {{ color: #64748b; margin-bottom: 32px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }}
  .card {{ background: white; border-radius: 16px; padding: 28px 20px; text-align: center; text-decoration: none; color: inherit; box-shadow: 0 4px 16px rgba(0,0,0,0.08); transition: transform 0.2s; }}
  .card:hover {{ transform: translateY(-4px); }}
  .card-icon {{ font-size: 2.5rem; margin-bottom: 12px; }}
  .card-name {{ font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; }}
  .card-meta {{ font-size: 0.8rem; color: #3b82f6; }}
</style></head>
<body>
<h1>📚 Infografías Educativas</h1>
<p>Generadas automáticamente con Claude AI · {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
<div class="grid">{cards}</div>
</body></html>"""

    ruta_indice = output_dir / "index.html"
    ruta_indice.write_text(html, encoding="utf-8")
    print(f"\n📑 Índice generado: {ruta_indice}")
    return ruta_indice


# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generador automático de infografías educativas con Claude AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python generador_infografias.py --tema "Inteligencia Artificial"
  python generador_infografias.py --tema "Python" --nivel "principiante"
  python generador_infografias.py --batch temas.yaml
  python generador_infografias.py --batch temas.yaml --output ./mis_infografias
        """
    )
    parser.add_argument("--tema", type=str, help="Tema único para generar infografía")
    parser.add_argument("--nivel", type=str, default="intermedio",
                        choices=["principiante", "intermedio", "avanzado"])
    parser.add_argument("--idioma", type=str, default="español")
    parser.add_argument("--batch", type=str, help="Archivo YAML con lista de temas")
    parser.add_argument("--output", type=str, default="./infografias_output")

    args = parser.parse_args()
    output_dir = Path(args.output)

    print("\n🎨 Generador de Infografías Educativas")
    print("=" * 40)
    print(f"📁 Directorio de salida: {output_dir.resolve()}")
    print(f"🤖 Modelo: {MODEL}\n")

    if args.batch:
        archivos = procesar_batch(args.batch, output_dir)
        if archivos:
            generar_indice(archivos, output_dir)
            print(f"\n✅ Completado: {len(archivos)} infografías generadas")
    elif args.tema:
        print(f"🎯 Generando infografía: {args.tema}")
        ruta = procesar_tema(args.tema, args.nivel, args.idioma, output_dir)
        print(f"\n✅ Infografía lista: {ruta.resolve()}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
```

---

### `temas.yaml`

```yaml
# Configuración de temas para procesamiento batch
# Uso: python generador_infografias.py --batch temas.yaml

temas:
  # Formato simple
  - "Inteligencia Artificial Generativa"
  - "Prompt Engineering"
  - "Python para Data Science"

  # Formato extendido (con nivel e idioma)
  - tema: "Machine Learning desde cero"
    nivel: principiante
    idioma: español

  - tema: "APIs REST y GraphQL"
    nivel: intermedio
    idioma: español

  - tema: "Docker y Contenedores"
    nivel: intermedio
    idioma: español

  - tema: "Seguridad en Aplicaciones Web"
    nivel: avanzado
    idioma: español

  - tema: "Design Thinking para Productos Digitales"
    nivel: principiante
    idioma: español
```

---

### `ejecutar_semanal.sh`

```bash
#!/bin/bash
# Automatización con cron — lunes, miércoles y viernes a las 10pm:
#   crontab -e
#   0 22 * * 1,3,5 /ruta/al/proyecto/ejecutar_semanal.sh

PROYECTO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$PROYECTO_DIR/infografias_output/$(date +%Y-semana%V)"
LOG_FILE="$PROYECTO_DIR/logs/ejecucion_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$PROYECTO_DIR/logs"

echo "========================================" | tee -a "$LOG_FILE"
echo "🎨 Generador de Infografías Educativas"  | tee -a "$LOG_FILE"
echo "📅 Fecha: $(date '+%d/%m/%Y %H:%M:%S')"  | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "❌ ERROR: ANTHROPIC_API_KEY no configurada" | tee -a "$LOG_FILE"
  exit 1
fi

cd "$PROYECTO_DIR" && python3 generador_infografias.py \
  --batch temas.yaml \
  --output "$OUTPUT_DIR" \
  2>&1 | tee -a "$LOG_FILE"

[ $? -eq 0 ] \
  && echo "✅ Completado. Ver resultados: $OUTPUT_DIR" | tee -a "$LOG_FILE" \
  || echo "❌ Error. Revisar log: $LOG_FILE"           | tee -a "$LOG_FILE"
```

---

## Stack

- **Claude API** (`claude-opus-4-6`) — generación de contenido estructurado
- **Claude Cowork** — agente de escritorio para tareas programadas conversacionales
- **Python 3.10+** — orquestación del flujo
- **HTML + CSS puro** — output visual sin dependencias externas
- **cron / Cowork Scheduler** — automatización de la ejecución recurrente

---

*Proyecto 2 — Platzi Challenge: Automatiza el flujo que nadie quiere hacer*

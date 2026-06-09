"""Script auxiliar para generar la infografía de ejemplo."""
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '.')
from generador_infografias import generar_html

datos = {
  "titulo": "Prompt Engineering: El Arte de Hablar con la IA",
  "subtitulo": "Como disenar instrucciones efectivas para modelos de lenguaje",
  "emoji_principal": "🧩",
  "color_tema": "morado",
  "resumen": "El Prompt Engineering es la habilidad de disenar y optimizar instrucciones para que los modelos de lenguaje como GPT o Claude produzcan los resultados que necesitamos. No se trata de magia: es una disciplina sistematica que combina psicologia cognitiva, logica y creatividad para comunicarnos de forma precisa con sistemas de IA.",
  "conceptos_clave": [
    {"icono": "🎯", "nombre": "Zero-Shot Prompting", "descripcion": "Dar instrucciones directas sin ejemplos previos. El modelo infiere que se espera solo a partir de la descripcion de la tarea."},
    {"icono": "📖", "nombre": "Few-Shot Prompting", "descripcion": "Incluir 2-5 ejemplos en el prompt para que el modelo aprenda el patron y lo replique en casos nuevos."},
    {"icono": "🔗", "nombre": "Chain of Thought", "descripcion": "Pedir al modelo que razone paso a paso antes de dar la respuesta. Mejora drasticamente la precision en problemas complejos."},
    {"icono": "🎭", "nombre": "Role Prompting", "descripcion": "Asignar un rol al modelo (Eres un experto en...) para obtener respuestas mas especializadas y contextualizadas."},
    {"icono": "🔁", "nombre": "Self-Consistency", "descripcion": "Generar multiples respuestas y seleccionar la mas frecuente o coherente, aumentando la confiabilidad del resultado."}
  ],
  "estadisticas": [
    {"valor": "63%", "descripcion": "de empresas Fortune 500 usan IA generativa", "fuente": "McKinsey Global Survey 2024"},
    {"valor": "10x", "descripcion": "mejora en calidad de outputs con tecnicas avanzadas de prompting", "fuente": "OpenAI Research"},
    {"valor": "$200K+", "descripcion": "salario promedio de Prompt Engineers senior en EE.UU.", "fuente": "LinkedIn Jobs Report 2024"}
  ],
  "pasos_o_tips": [
    {"numero": 1, "titulo": "Define el contexto y rol", "detalle": "Empieza siempre indicando quien es el modelo y cual es su expertise. Ej: Eres un experto en marketing digital con 10 anos de experiencia."},
    {"numero": 2, "titulo": "Se especifico en la tarea", "detalle": "Evita instrucciones vagas. En vez de 'escribe algo sobre X', di: escribe un articulo de 300 palabras sobre X dirigido a estudiantes universitarios."},
    {"numero": 3, "titulo": "Usa ejemplos concretos", "detalle": "Incluye 2-3 ejemplos del formato o estilo esperado. Los modelos aprenden mejor con ejemplos que con descripciones abstractas."},
    {"numero": 4, "titulo": "Pide razonamiento explicito", "detalle": "Agrega 'Piensa paso a paso' para tareas complejas. Reduce alucinaciones significativamente."},
    {"numero": 5, "titulo": "Itera y refina", "detalle": "Trata cada prompt como un experimento. Ajusta una variable a la vez y registra que mejora los resultados."}
  ],
  "dato_curioso": "Un estudio de Stanford (2024) demostro que anadir 'respiremos y pensemos paso a paso' al final de un prompt mejora la precision en matematicas hasta un 40%. Las IAs responden mejor cuando se les pide que 'piensen' antes de responder.",
  "recursos_recomendados": [
    {"tipo": "Curso", "nombre": "Prompt Engineering for Developers", "descripcion": "Curso gratuito de DeepLearning.AI con Andrew Ng, cubre tecnicas avanzadas con ejemplos practicos."},
    {"tipo": "Herramienta", "nombre": "PromptPerfect", "descripcion": "Plataforma para optimizar y testear prompts automaticamente, con metricas de rendimiento."},
    {"tipo": "Libro", "nombre": "The Art of Prompt Engineering", "descripcion": "Guia comprehensiva con patrones probados y casos de uso reales en produccion."}
  ],
  "cita_inspiradora": {
    "texto": "El lenguaje es el sistema operativo de la mente humana. Los prompts son el codigo fuente de la IA.",
    "autor": "Andrej Karpathy, Co-fundador de OpenAI"
  },
  "tags": ["PromptEngineering", "InteligenciaArtificial", "LLM", "ChatGPT", "Claude"]
}

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
html = generar_html(datos, 'Prompt Engineering', timestamp)

Path('infografias_output').mkdir(exist_ok=True)
ruta = Path('infografias_output/infografia_ejemplo_prompt_engineering.html')
ruta.write_text(html, encoding='utf-8')
print(f'Infografia generada: {ruta}')
print(f'Tamano: {ruta.stat().st_size:,} bytes')

# Clasificador de Hábitos de Ahorro Universitario 🎀

Sistema inteligente de diagnóstico financiero para estudiantes universitarios basado en un **Árbol Binario de Decisión**, un catálogo estructurado de **50 Soluciones Técnicas Estudiantiles**, un **Prompt Maestro de Alto Nivel** y un tutor contextualizado con **Ollama (Phi-3)**.

---

## 🏛️ Arquitectura del Sistema

El flujo secuencial consta de 3 fases:

1. **Clasificación (Árbol Binario de 5 Niveles):**
   - Árbol de **63 nodos** (31 preguntas estructuradas y 32 hojas de perfil).
   - Cada estudiante recorre **5 preguntas exactas** de Sí/No que evalúan flujo de caja, rendimientos, diversificación, gastos hormiga, tipos de deuda, amortización, meal prep y redes de apoyo institucional.
   - Diagnóstica con precisión quirúrgica uno de los **32 Arquetipos Universitarios**:
     - *Ahorradores:* Visionario de Alto Rendimiento, Visionario Práctico, Conservador Blindado, Conservador en Construcción, Metódico Tradicional, Disciplinado Manual, Tentado e Inestable, Pasivo Estancado.
     - *Consumistas:* Consciente en Regulación, Consciente Desbordado, Impulsivo Crónico, Social Ocasional, Comprador de Temporada Reflexivo, Comprador de Temporada Impulsivo, Acumulador Inconsciente con Fugas, Superávit Relajado.
     - *Endeudados:* Estratégico Disciplinado, Estratégico Reincidente, Consciente Activo, Consciente Estancado, Crítico de Alto Riesgo, Crítico en Bola de Nieve, Informal Vulnerable, Ciego Financiero.
     - *Supervivientes:* Proactivo Generador, Proactivo Ahorrador, Ajustable Planificado, Ajustable Postergador, Con Apoyo Gestionado, Con Apoyo Pasivo, Crítico en Alerta Roja, Resiliente en Déficit.

2. **Mapeo de Soluciones Dinámicas:**
   - Diccionario en Python que vincula el arquetipo diagnosticado con 6 a 8 soluciones técnicas pre-aprobadas del catálogo de 50 estrategias de campus.

3. **Inferencia y Prompt Maestro con Ollama (Phi-3):**
   - System Prompt de mentoría financiera con estructura en 4 bloques: Diagnóstico del Perfil, Plan de Choque en 3 Pasos (24h, semanal y semestral), Regla de Oro con micro-meta cuantificable y Frase de Poder.
   - Inferencia con latencia optimizada (`num_predict: 280`, `num_ctx: 1536`) y fallback local garantizado.

---

## 🌸 Interfaz Gráfica Cute Minimalista (Estilo Hello Kitty)

- **Modo Claro Cute:** Fondo pastel blush pink (`#fff1f5`), tarjetas blancas puras con bordes rosados redondeados (`#fbcfe8`) y acentos en hot pink Hello Kitty (`#ec4899`).
- **Navegación Visual:** Contador `🌸 Pregunta #X de 5`, barra de progreso interactiva, botones `🎀 SÍ` y `🌸 NO`.
- **Resultados Inmediatos:** Al responder la quinta pregunta, la pantalla de resultados carga instantáneamente el arquetipo, el gráfico de balance con Matplotlib y las soluciones técnicas, mientras Phi-3 enriquece el plan en segundo plano.

---

## 🚀 Instalación y Uso

### 1. Requisitos Previos
- Python 3.10+
- Ollama instalado con el modelo `phi3`:
  ```bash
  ollama pull phi3
  ```

### 2. Entrenar / Crear el Modelo Personalizado con el Modelfile
```bash
ollama create tutor-financiero -f ./Modelfile
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación

**Modo Gráfico (GUI Hello Kitty):**
```bash
python ahorro/main.py
```

**Modo Consola (CLI):**
```bash
python ahorro/main.py --cli
```

### 5. Ejecutar Pruebas Unitarias
```bash
pytest
```

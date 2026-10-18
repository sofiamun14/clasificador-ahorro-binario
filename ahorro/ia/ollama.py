"""Integración de alto rendimiento con Ollama Phi-3 con respuestas contundentes y motivadoras."""

import os
from typing import Callable, Optional

try:
    import ollama
except ImportError:
    ollama = None

import requests


def construir_prompt_maestro(perfil_estudiante: str, respuestas_formateadas: str, soluciones_mapeadas: str) -> str:
    """Construye un prompt de mentoría financiera cálido, contundente y motivador para estudiantes."""
    return f"""Eres un mentor y coach financiero de élite especializado en estudiantes universitarios. Tu misión es transformar la mentalidad y hábitos financieros del estudiante con una asesoría contundente, profunda, inspiradora y llena de energía positiva. Valora su esfuerzo en la universidad, reconoce que cada peso cuenta y anímalo con entusiasmo hacia su tranquilidad e independencia financiera.

CONTEXTO DEL ESTUDIANTE:
- Arquetipo diagnosticado por el árbol: {perfil_estudiante}
- Historial de respuestas en el cuestionario:
{respuestas_formateadas}
- Soluciones técnicas pre-aprobadas para su perfil:
{soluciones_mapeadas}

INSTRUCCIONES DE RESPUESTA:
Redacta una respuesta completa, profunda y estructurada (sin introducciones vacías, ve directo al impacto):

1. DIAGNÓSTICO CONTUNDENTE Y RECONOCIMIENTO:
Explica con claridad y empatía qué significa su arquetipo para su vida presente y futura. Reconoce los aciertos que ya tiene o la valentía de enfrentar su realidad financiera. Explica con contundencia por qué este momento en su carrera universitaria es la oportunidad perfecta para transformar sus finanzas.

2. PLAN DE ACCIÓN DE 3 PASOS ESTRATÉGICOS Y DETALLADOS:
Toma las soluciones pre-aprobadas y desarróllalas a profundidad con ejemplos universitarios reales (fotocopias, almuerzos de campus, transporte, billeteras digitales, amortización):
- PASO 1 (Para ejecutar en las próximas 24 horas): Una acción inmediata, práctica y tangible que le devuelva el control (ej. abrir un bolsillo digital de ahorro automático, listar pasivos con fechas de corte, o desinstalar tentaciones de delivery). Explica exactamente cómo hacerlo.
- PASO 2 (Para consolidar esta misma semana en el campus): Un cambio de hábito inteligente en su rutina universitaria (ej. meal prep semanal para ahorrar en cafeterías, transporte en bicicleta o rutas compartidas, topes semanales en efectivo o débito). Detalla cuánto dinero puede liberar.
- PASO 3 (Meta estructural para cerrar el semestre con éxito): Una meta financiera sólida (creación de un fondo de emergencia de 3 meses, CDT a 90 días, o liquidación total de su deuda más costosa).

3. REGLA DE ORO PERSONALIZADA Y MICRO-META CUANTIFICABLE:
Establece una cifra realista y motivadora (ej. un microahorro diario de $3.000 a $5.000 COP, o no destinar más de $25.000 semanales a ocio efímero). Explica cuánto representará esa cifra acumulada al finalizar el semestre.

4. MENSAJE DE PODER, ÁNIMO Y VISIÓN DE FUTURO:
Dedica un párrafo apasionado y motivador a recordarle su capacidad, su talento y el valor de su carrera universitaria. Transmítele convicción absoluta de que dominar el dinero durante la universidad es el superpoder que lo distinguirá en su vida personal y profesional. ¡Haz que se sienta capaz, empoderado y orgulloso de dar este paso hoy!"""


class ClienteOllama:
    """Cliente para inferencia con Ollama Phi-3 con respuestas ricas y motivadoras."""

    def __init__(self, modelo_por_defecto: str = "phi3"):
        self.modelo = os.environ.get("OLLAMA_MODEL", modelo_por_defecto)
        self.url = "http://localhost:11434/api/chat"
        self.timeout = 100

    def generar_plan_financiero(
        self,
        perfil: str,
        respuestas: str | list[str],
        soluciones: str | list[str],
        callback_token: Optional[Callable[[str], None]] = None,
    ) -> Optional[str]:
        """Envía el contexto enriquecido a Phi-3 para generar una asesoría contundente y motivadora."""
        respuestas_str = "\n".join(respuestas) if isinstance(respuestas, list) else str(respuestas)
        soluciones_str = "\n".join(soluciones) if isinstance(soluciones, list) else str(soluciones)
        system_prompt = construir_prompt_maestro(perfil, respuestas_str, soluciones_str)

        opciones = {
            "temperature": 0.35,
            "num_predict": 700,
            "num_ctx": 2048,
            "num_thread": max(2, (os.cpu_count() or 4) - 1),
        }

        mensaje_usuario = "Basado en mi diagnóstico, bríndame mi asesoría financiera completa, contundente, motivadora y mi plan de acción estratégico."

        if ollama is not None:
            try:
                if callback_token:
                    respuesta_completa = []
                    stream = ollama.chat(
                        model=self.modelo,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": mensaje_usuario},
                        ],
                        options=opciones,
                        stream=True,
                    )
                    for chunk in stream:
                        fragmento = chunk.get("message", {}).get("content", "")
                        if fragmento:
                            respuesta_completa.append(fragmento)
                            callback_token(fragmento)
                    return "".join(respuesta_completa)
                else:
                    respuesta = ollama.chat(
                        model=self.modelo,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": mensaje_usuario},
                        ],
                        options=opciones,
                    )
                    return respuesta.get("message", {}).get("content", "")
            except Exception:
                pass

        try:
            payload = {
                "model": self.modelo,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": mensaje_usuario},
                ],
                "stream": False,
                "options": opciones,
            }
            res = requests.post(self.url, json=payload, timeout=self.timeout)
            res.raise_for_status()
            data = res.json()
            return data.get("message", {}).get("content", "")
        except Exception:
            return None

    def generar_consejo(self, nombre_perfil: str) -> Optional[str]:
        """Compatibilidad con consultas simples."""
        return self.generar_plan_financiero(
            perfil=nombre_perfil,
            respuestas="Diagnóstico universitario integral.",
            soluciones="Soluciones estratégicas de campus.",
        )
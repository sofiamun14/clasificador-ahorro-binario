# ahorro/ia/ollama.py

import requests
import json
import os

class ClienteOllama:
    def __init__(self, modelo_por_defecto="phi3"):
        # Se cambia a phi3 por ser más rápido y evitar el timeout (SH-04)
        self.modelo = os.environ.get("OLLAMA_MODEL", modelo_por_defecto)
        self.url = "http://localhost:11434/api/generate"
        self.timeout = 300  # Obligatorio por el contrato: 30 segundos (9.1)

    def generar_consejo(self, nombre_perfil):
        """
        Envía el perfil a Ollama (Phi-3) y redacta el consejo sin alterar el árbol.
        """
        system_prompt = (
            "Eres un asistente de educación financiera y hábitos de ahorro en Colombia. "
            "Recibirás un perfil elegido exclusivamente por un árbol binario. No cambies el perfil "
            "ni inventes ingresos o deudas. Redacta en español: (1) diagnóstico educativo máximo "
            "tres líneas; (2) tres acciones específicas, económicas y realizables; (3) una frase motivacional. "
            "Usa pesos colombianos (COP) y, si corresponde, ejemplos de microahorros de $2.000 o $5.000; "
            "aclara que son ejemplos y deben ajustarse a la capacidad de cada persona. Evita prometer "
            "rendimientos, indicar inversiones como seguras o recomendar endeudamiento riesgoso. "
            "No solicites datos personales."
        )

        prompt = f"Perfil clasificado: {nombre_perfil}."

        payload = {
            "model": self.modelo,
            "system": system_prompt,
            "prompt": prompt,
            "stream": False
        }

        try:
            # Petición a la IA local
            respuesta = requests.post(self.url, json=payload, timeout=self.timeout)
            respuesta.raise_for_status() 
            
            datos = respuesta.json()
            return datos.get("response", "")
            
        except requests.exceptions.Timeout:
             print("\n[Aviso IA] Ollama se demoró más de 30 segundos en pensar. Activando Plan B...")
             return None
        except requests.exceptions.ConnectionError:
            print("\n[Aviso IA] Ollama no está encendido. Ejecuta 'ollama serve' o abre la aplicación. Activando Plan B...")
            return None
        except requests.exceptions.RequestException as e:
            print(f"\n[Aviso IA] Error de conexión con la IA ({e}). Activando Plan B...")
            return None 
        except json.JSONDecodeError:
            print("\n[Aviso IA] Ollama devolvió un formato inválido. Activando Plan B...")
            return None
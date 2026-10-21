"""Interfaz de consola interactiva para el clasificador de ahorro estudiantil."""

from ahorro.core.perfil import Perfil
from ahorro.core.soluciones import obtener_soluciones_perfil
from ahorro.ia.consejos import obtener_consejo_local
from ahorro.ia.ollama import ClienteOllama


class MenuConsola:
    """Gestiona el flujo por consola del árbol de decisión y la interacción con Ollama."""

    def __init__(self, arbol):
        self.arbol = arbol
        self.ia = ClienteOllama()

    def iniciar(self):
        """Ciclo principal de opciones en la consola."""
        while True:
            print("\n" + "=" * 55)
            print(" SISTEMA CLASIFICADOR DE HÁBITOS DE AHORRO UNIVERSITARIO ")
            print("=" * 55)
            print("1. Iniciar diagnóstico financiero")
            print("2. Ver catálogo de preguntas y perfiles (Inorden)")
            print("3. Ayuda")
            print("4. Salir")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self._ejecutar_diagnostico()
            elif opcion == "2":
                self._mostrar_catalogo()
            elif opcion == "3":
                self._mostrar_ayuda()
            elif opcion == "4":
                print("\nDesmontando el árbol de memoria...")
                self.arbol.desmontar_postorden()
                print("Saliendo del sistema. ¡Éxitos en tus finanzas universitarias!")
                break
            else:
                print("\nOpción no válida. Por favor ingrese un número del 1 al 4.")

    def _ejecutar_diagnostico(self):
        """Ejecuta el cuestionario binario y genera el plan financiero con Ollama Phi-3."""
        print("\n--- Diagnóstico Financiero Estudiantil ---")

        if not self.arbol or not self.arbol.raiz:
            print("Error: El árbol de decisión no está inicializado.")
            return

        nodo_actual = self.arbol.raiz
        ruta = []
        historial_respuestas = []

        while not nodo_actual.es_hoja():
            print(f"\nPregunta: {nodo_actual.texto}")
            respuesta = input("Responda Sí (S) o No (N): ").strip().upper()

            if respuesta in ["S", "SI", "SÍ"]:
                ruta.append(True)
                historial_respuestas.append(f"- {nodo_actual.texto} => SÍ")
                nodo_actual = self.arbol.avanzar(nodo_actual, True)
            elif respuesta in ["N", "NO"]:
                ruta.append(False)
                historial_respuestas.append(f"- {nodo_actual.texto} => NO")
                nodo_actual = self.arbol.avanzar(nodo_actual, False)
            else:
                print("Entrada no reconocida. Ingrese 'S' para Sí o 'N' para No.")

        perfil_id = nodo_actual.perfil.id if nodo_actual.perfil else "sin_perfil"
        print(f"\n==========================================")
        print(f" Arquetipo diagnosticado: {nodo_actual.texto}")
        print(f"==========================================")

        soluciones = obtener_soluciones_perfil(perfil_id)

        print("\nConsultando a Ollama (Phi-3) para generar tu plan de acción financiero...")
        plan = self.ia.generar_plan_financiero(
            perfil=nodo_actual.texto,
            respuestas=historial_respuestas,
            soluciones=soluciones,
        )

        if plan:
            print("\n--- Plan de Acción Financiero (Ollama Phi-3) ---")
            print(plan)
        else:
            print("\n--- Plan de Acción de Respaldo Local ---")
            print(obtener_consejo_local(perfil_id))

        self._gestionar_aprendizaje(ruta, nodo_actual)

    def _gestionar_aprendizaje(self, ruta, nodo_actual):
        """Permite refinar el árbol agregando una nueva pregunta y perfil si el usuario no se siente identificado."""
        while True:
            conforme = input("\n¿Te sientes identificado con este perfil? (S/N): ").strip().upper()
            if conforme in ["S", "SI", "SÍ"]:
                break
            if conforme in ["N", "NO"]:
                print("\nVamos a enseñar al sistema un nuevo arquetipo.")
                nuevo_nombre = input("¿Cuál es el nombre de tu arquetipo?: ").strip()
                nueva_pregunta = input(
                    f"¿Qué pregunta de Sí/No te diferenciaría de '{nodo_actual.texto}'? (Sí = {nuevo_nombre}, No = {nodo_actual.texto}): "
                ).strip()

                if not nuevo_nombre or not nueva_pregunta:
                    print("El nombre y la pregunta no pueden estar vacíos.")
                    continue

                nuevo_id = (
                    nuevo_nombre.lower()
                    .replace(" ", "_")
                    .replace("á", "a")
                    .replace("é", "e")
                    .replace("í", "i")
                    .replace("ó", "o")
                    .replace("ú", "u")
                )
                nuevo_perfil = Perfil(id_perfil=nuevo_id, nombre=nuevo_nombre)
                exito = self.arbol.aprender(ruta, nueva_pregunta, nuevo_perfil)
                if exito:
                    print(f"\n¡Aprendizaje registrado con éxito! Nuevo arquetipo: '{nuevo_nombre}'.")
                break
            print("Por favor responda 'S' o 'N'.")

    def _mostrar_catalogo(self):
        """Muestra los elementos del árbol recorridos en orden estructural (Inorden)."""
        print("\n--- Catálogo de Nodos (Recorrido Inorden) ---")
        if not self.arbol:
            print("El árbol no está inicializado.")
            return

        for idx, item in enumerate(self.arbol.listar_inorden(), 1):
            print(f"{idx}. {item}")

    def _mostrar_ayuda(self):
        """Muestra directrices de uso y contexto pedagógico."""
        print("\n--- Información del Sistema ---")
        print("1. Clasificación binaria en 3 niveles adaptada a la realidad universitaria.")
        print("2. Mapeo de soluciones técnicas específicas a partir de 50 estrategias estudiantiles.")
        print("3. Inferencia y asesoría personalizada mediante Ollama (modelo Phi-3 local).")
        print("4. Respaldo sin conexión en caso de que el servicio de IA no esté activo.")
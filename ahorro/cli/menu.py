# ahorro/cli/menu.py

from ahorro.core.perfil import Perfil
from ahorro.ia.ollama import ClienteOllama
from ahorro.ia.consejos import obtener_consejo_local

class MenuConsola:
    def __init__(self, arbol):
        """
        Recibe la instancia del árbol binario.
        El menú invoca métodos públicos del árbol (contrato 2.1).
        """
        self.arbol = arbol
        self.ia = ClienteOllama()

    def iniciar(self):
        """Punto de entrada principal del menú (SH-01)."""
        while True:
            print("\n" + "="*45)
            print(" SISTEMA CLASIFICADOR DE HÁBITOS DE AHORRO ")
            print("="*45)
            print("1. Iniciar diagnóstico")
            print("2. Ver catálogo de perfiles (Inorden)")
            print("3. Ayuda")
            print("4. Salir")
            
            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == '1':
                self._ejecutar_diagnostico()
            elif opcion == '2':
                self._mostrar_catalogo()
            elif opcion == '3':
                self._mostrar_ayuda()
            elif opcion == '4':
                print("\nDesmontando el árbol de memoria...")
                # Llama a la función de desmontaje postorden (SM-04 y T-08)
                self.arbol.desmontar_postorden()
                print("Saliendo del sistema. ¡Hasta pronto!")
                break
            else:
                print("\nOpción no válida. Por favor, seleccione una opción del 1 al 4.")

    def _ejecutar_diagnostico(self):
        """
        Maneja el flujo del cuestionario Sí/No y el diagnóstico (SH-02).
        """
        print("\n--- Iniciando Diagnóstico ---")
        
        if not self.arbol or not self.arbol.raiz:
             print("Error: El árbol no está inicializado.")
             return
             
        nodo_actual = self.arbol.raiz
        ruta = []

        # Navegación binaria: las hojas (perfiles) no tienen hijos
        while nodo_actual.izquierdo is not None and nodo_actual.derecho is not None:
            print(f"\nPregunta: {nodo_actual.texto}")
            respuesta = input("Responda Sí (S) o No (N): ").strip().upper()

            # True = Izquierda (Sí), False = Derecha (No)
            if respuesta in ['S', 'SI', 'SÍ']:
                ruta.append(True)
                nodo_actual = self.arbol.avanzar(nodo_actual, True)
            elif respuesta in ['N', 'NO']:
                ruta.append(False)
                nodo_actual = self.arbol.avanzar(nodo_actual, False)
            else:
                # Prueba T-11: Solicitar corrección sin modificar el árbol
                print("Por favor, ingrese solo 'S' para Sí o 'N' para No.")

        # Al salir del bucle, estamos en una hoja (Perfil)
        print(f"\n¡Diagnóstico finalizado! Tu perfil inicial es: {nodo_actual.texto}")
        
        # Generar consejo con IA o Plan B (SH-04 y SH-05)
        print("\nGenerando consejo educativo...")
        consejo = self.ia.generar_consejo(nodo_actual.texto)
        
        if consejo:
            print("\n--- Consejo de Ollama ---")
            print(consejo)
        else:
            print("\n--- Consejo de Respaldo ---")
            print(obtener_consejo_local(nodo_actual.perfil.id))

        # Flujo de aprendizaje dinámico (SH-03)
        self._gestionar_aprendizaje(ruta, nodo_actual)

    def _gestionar_aprendizaje(self, ruta, nodo_actual):
        """Permite al usuario rechazar el perfil y enseñar uno nuevo."""
        while True:
            conforme = input("\n¿Te sientes identificado con este perfil? (S/N): ").strip().upper()
            if conforme in ['S', 'SI', 'SÍ']:
                break
            elif conforme in ['N', 'NO']:
                print("\nVamos a enseñar al sistema un nuevo perfil.")
                
                nuevo_nombre = input("¿Cuál sería el nombre de tu perfil real?: ").strip()
                nueva_pregunta = input(f"¿Qué pregunta de Sí/No te separaría de '{nodo_actual.texto}'? (Si respondes Sí, serás '{nuevo_nombre}'): ").strip()
                
                if not nuevo_nombre or not nueva_pregunta:
                    print("La pregunta y el perfil no pueden estar vacíos. Intenta de nuevo.")
                    continue
                
                # Crear ID simple para el TXT
                nuevo_id = nuevo_nombre.lower().replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                nuevo_perfil = Perfil(id=nuevo_id, nombre=nuevo_nombre)
                
                # Ejecutar inserción en el núcleo
                exito = self.arbol.aprender(ruta, nueva_pregunta, nuevo_perfil)
                if exito:
                    print(f"\n¡Aprendizaje exitoso! Se ha agregado el perfil '{nuevo_nombre}'.")
                break
            else:
                print("Por favor, responda 'S' o 'N'.")

    def _mostrar_catalogo(self):
        """Muestra el catálogo usando el recorrido inorden del núcleo (SH-03)."""
        print("\n--- Catálogo del Árbol (Orden Estructural) ---")
        if not self.arbol:
            print("El árbol no está inicializado.")
            return
            
        elementos = self.arbol.listar_inorden()
        for idx, elemento in enumerate(elementos, 1):
            print(f"{idx}. {elemento}")

    def _mostrar_ayuda(self):
        print("\n--- Ayuda del Sistema ---")
        print("1. El sistema te hará preguntas de Sí/No para determinar tu perfil de ahorro.")
        print("2. Si el perfil final no te representa, podrás enseñar al sistema un nuevo perfil.")
        print("3. Recibirás recomendaciones financieras generadas por IA (Ollama).")
        print("4. Todas las recomendaciones son estrictamente educativas y en pesos colombianos (COP).")
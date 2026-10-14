from ahorro.core.nodo import Nodo
from ahorro.core.perfil import Perfil

class ArbolDecision:
    def __init__(self):
        # La interfaz accederá a self.raiz para comenzar el cuestionario
        self.raiz = self._construir_arbol_inicial()

    def _construir_arbol_inicial(self) -> Nodo:
        """Construye los 7 nodos iniciales del sistema clasificador."""
        # 1. Crear las hojas (Perfiles)
        consolidado = Nodo(texto="Ahorrador Consolidado", perfil=Perfil("consolidado", "Ahorrador Consolidado"))
        esporadico = Nodo(texto="Ahorrador Esporádico", perfil=Perfil("esporadico", "Ahorrador Esporádico"))
        apagafuegos = Nodo(texto="Perfil Apagafuegos", perfil=Perfil("apagafuegos", "Perfil Apagafuegos"))
        fuga = Nodo(texto="Fuga de Capital", perfil=Perfil("fuga_capital", "Fuga de Capital"))

        # 2. Crear las preguntas secundarias vinculando las hojas
        # Izquierdo = SÍ, Derecho = NO
        preg_apartas = Nodo(texto="¿Apartas el ahorro cuando cobras?", izquierdo=consolidado, derecho=esporadico)
        preg_deudas = Nodo(texto="¿Tus deudas superan el 30 % de tus ingresos?", izquierdo=apagafuegos, derecho=fuga)

        # 3. Crear la pregunta raíz vinculando las secundarias
        raiz = Nodo(texto="¿Te sobra dinero al final de mes?", izquierdo=preg_apartas, derecho=preg_deudas)
        
        return raiz

    def avanzar(self, nodo: Nodo, respuesta_si: bool) -> Nodo:
        """
        Navega hacia el siguiente nodo.
        True = hijo izquierdo (Sí), False = hijo derecho (No).
        """
        if respuesta_si:
            if nodo.izquierdo is None:
                raise ValueError("Ruta inválida: no hay hijo izquierdo.")
            return nodo.izquierdo
        else:
            if nodo.derecho is None:
                raise ValueError("Ruta inválida: no hay hijo derecho.")
            return nodo.derecho
    
    def aprender(self, ruta: list[bool], pregunta: str, nuevo_perfil: Perfil) -> bool:
        """
        Convierte una hoja existente en una nueva pregunta.
        Izquierdo (SÍ) = nuevo perfil, Derecho (NO) = perfil original.
        """
        if self.raiz is None:
            return False

        # 1. Navegar hasta la hoja correspondiente usando la ruta
        nodo_actual = self.raiz
        try:
            for respuesta in ruta:
                nodo_actual = self.avanzar(nodo_actual, respuesta)
        except ValueError:
            return False  # La ruta entregada fue inválida

        # 2. Validar que realmente llegamos a una hoja
        if not nodo_actual.es_hoja():
            return False

        # 3. Guardar los datos de la hoja original (que ahora será la respuesta NO)
        perfil_original = nodo_actual.perfil
        texto_original = nodo_actual.texto

        # 4. Transformar el nodo actual en un nodo de pregunta
        nodo_actual.texto = pregunta
        nodo_actual.perfil = None

        # 5. Crear los dos nuevos hijos
        # Izquierdo = SÍ = Nuevo perfil
        nodo_actual.izquierdo = Nodo(texto=nuevo_perfil.nombre, perfil=nuevo_perfil)
        
        # Derecho = NO = Perfil original
        nodo_actual.derecho = Nodo(texto=texto_original, perfil=perfil_original)

        return True

    def listar_inorden(self) -> list[str]:
        """
        Recorrido Inorden: Izquierda, Raíz, Derecha.
        Devuelve el catálogo de preguntas y perfiles en orden estructural.
        """
        resultado = []
        def _recorrer(nodo: Nodo):
            if nodo is not None:
                _recorrer(nodo.izquierdo)
                resultado.append(nodo.texto)
                _recorrer(nodo.derecho)
        
        _recorrer(self.raiz)
        return resultado

    def obtener_preorden(self) -> list:
        """
        Recorrido Preorden: Raíz, Izquierda, Derecha.
        Incluye valores None para los hijos vacíos, necesario para la serialización.
        """
        resultado = []
        def _recorrer(nodo):
            if nodo is None:
                resultado.append(None)
                return
            
            resultado.append(nodo)
            _recorrer(nodo.izquierdo)
            _recorrer(nodo.derecho)
                
        _recorrer(self.raiz)
        return resultado

    def desmontar_postorden(self) -> list[str]:
        """
        Recorrido Postorden: Izquierda, Derecha, Raíz.
        Registra la visita de hijos antes que el padre, elimina vínculos y deja la raíz en None.
        """
        traza = []
        def _recorrer(nodo: Nodo):
            if nodo is None:
                return
            
            _recorrer(nodo.izquierdo)
            _recorrer(nodo.derecho)
            
            traza.append(f"Visitado para desmontaje: {nodo.texto}")
            nodo.izquierdo = None
            nodo.derecho = None
            
        _recorrer(self.raiz)
        self.raiz = None  # Se retira la referencia principal para que Python limpie la memoria
        return traza



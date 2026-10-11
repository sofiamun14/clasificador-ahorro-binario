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
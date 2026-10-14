from dataclasses import dataclass
from typing import Optional
from ahorro.core.perfil import Perfil

@dataclass
class Nodo:
    texto: str  # Puede ser la pregunta o el nombre del perfil
    # En Python 3.11+ usamos el tipado para indicar que pueden ser None
    izquierdo: Optional['Nodo'] = None  # Respuesta SÍ
    derecho: Optional['Nodo'] = None    # Respuesta NO
    perfil: Optional[Perfil] = None     # Solo tiene datos si es una hoja

    def es_hoja(self) -> bool:
        """Devuelve True si el nodo no tiene hijos (es decir, es un perfil final)."""
        return self.izquierdo is None and self.derecho is None
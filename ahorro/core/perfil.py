from dataclasses import dataclass

@dataclass
class Perfil:
    id_perfil: str
    nombre: str

    @property
    def id(self) -> str:
        return self.id_perfil
"""Punto de entrada del clasificador de hábitos de ahorro."""

from pathlib import Path

from ahorro.cli.menu import MenuConsola
from ahorro.core.arbol import ArbolDecision
from ahorro.data_access.txt import RepositorioArbolTxt

DIRECTORIO_DATOS = Path(__file__).resolve().parent.parent / "data"
RUTA_USUARIO = DIRECTORIO_DATOS / "arbol_usuario.txt"
RUTA_INICIAL = DIRECTORIO_DATOS / "arbol_inicial.txt"


def _cargar_arbol() -> ArbolDecision:
    for ruta in (RUTA_USUARIO, RUTA_INICIAL):
        if ruta.is_file():
            return RepositorioArbolTxt.cargar(ruta)
    return ArbolDecision()


def main() -> None:
    arbol = _cargar_arbol()
    traza: list[str] = []
    desmontar_original = arbol.desmontar_postorden

    def desmontar_con_guardado() -> list[str]:
        # El menú desmonta al salir; se persiste antes de perder la raíz.
        if arbol.raiz is not None:
            try:
                RepositorioArbolTxt.guardar(arbol, RUTA_USUARIO)
            except (OSError, ValueError) as error:
                print(f"No se pudo guardar el árbol: {error}")
        pasos = desmontar_original()
        traza.extend(pasos)
        return pasos

    arbol.desmontar_postorden = desmontar_con_guardado

    try:
        MenuConsola(arbol).iniciar()
    except (KeyboardInterrupt, EOFError):
        print("\nEjecución interrumpida.")
    finally:
        if arbol.raiz is not None:
            arbol.desmontar_postorden()
        print("\n--- Traza de desmontaje (postorden) ---")
        for paso in traza:
            print(paso)
        print(f"Raíz tras el desmontaje: {arbol.raiz}")


if __name__ == "__main__":
    main()

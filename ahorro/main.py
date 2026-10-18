import sys
from pathlib import Path

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ahorro.cli.menu import MenuConsola
from ahorro.core.arbol import ArbolDecision
from ahorro.data_access.txt import RepositorioArbolTxt

DIRECTORIO_DATOS = Path(__file__).resolve().parent.parent / "data"
RUTA_USUARIO = DIRECTORIO_DATOS / "arbol_usuario.txt"
RUTA_INICIAL = DIRECTORIO_DATOS / "arbol_inicial.txt"


def _cargar_arbol() -> ArbolDecision:
    """Carga el árbol desde archivo de usuario o inicial si existen."""
    for ruta in (RUTA_USUARIO, RUTA_INICIAL):
        if ruta.is_file():
            return RepositorioArbolTxt.cargar(ruta)
    return ArbolDecision()


def main() -> None:
    """Inicia la aplicación en modo gráfico o en consola si se indica --cli."""
    arbol = _cargar_arbol()

    if "--cli" in sys.argv:
        traza: list[str] = []
        desmontar_original = arbol.desmontar_postorden

        def desmontar_con_guardado() -> list[str]:
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
    else:
        try:
            from ahorro.gui.app import AppGUI

            app = AppGUI(arbol)

            def al_cerrar():
                if arbol.raiz is not None:
                    try:
                        RepositorioArbolTxt.guardar(arbol, RUTA_USUARIO)
                    except Exception:
                        pass
                app.destroy()

            app.protocol("WM_DELETE_WINDOW", al_cerrar)
            app.mainloop()
        except Exception as error:
            print(f"No fue posible iniciar la GUI ({error}). Iniciando en consola...")
            MenuConsola(arbol).iniciar()


if __name__ == "__main__":
    main()

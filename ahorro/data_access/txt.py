"""Persistencia del árbol de decisión en archivo de texto UTF-8 (preorden con '#')."""

import os
from pathlib import Path
from typing import Iterator, Optional

from ahorro.core.arbol import ArbolDecision
from ahorro.core.nodo import Nodo
from ahorro.core.perfil import Perfil

_NULO = "#"
_ESCAPES = {"\\": "\\\\", "|": "\\|", "\n": "\\n", "\r": "\\r"}
_DESESCAPES = {"\\": "\\", "|": "|", "n": "\n", "r": "\r"}


class ArchivoInvalidoError(ValueError):
    """El contenido del archivo no cumple el formato esperado."""


def _escapar(texto: str) -> str:
    return "".join(_ESCAPES.get(c, c) for c in texto)


def _dividir_campos(linea: str) -> list[str]:
    """Separa por '|' no escapado y desescapa cada campo."""
    campos: list[str] = []
    actual: list[str] = []
    i = 0
    while i < len(linea):
        c = linea[i]
        if c == "\\":
            i += 1
            if i >= len(linea) or linea[i] not in _DESESCAPES:
                raise ArchivoInvalidoError("Secuencia de escape inválida.")
            actual.append(_DESESCAPES[linea[i]])
        elif c == "|":
            campos.append("".join(actual))
            actual = []
        else:
            actual.append(c)
        i += 1
    campos.append("".join(actual))
    return campos


class RepositorioArbolTxt:
    @staticmethod
    def guardar(arbol: ArbolDecision, ruta: str | os.PathLike) -> None:
        """Serializa en preorden y reemplaza el destino de forma atómica."""
        if arbol is None or arbol.raiz is None:
            raise ValueError("No se puede guardar un árbol vacío.")

        lineas: list[str] = []
        for nodo in arbol.obtener_preorden():
            if nodo is None:
                lineas.append(_NULO)
            elif nodo.es_hoja():
                if nodo.perfil is None:
                    raise ValueError(f"La hoja '{nodo.texto}' no tiene perfil.")
                lineas.append(
                    f"P|{_escapar(nodo.perfil.id_perfil)}|{_escapar(nodo.perfil.nombre)}"
                )
            else:
                lineas.append(f"Q|{_escapar(nodo.texto)}")

        destino = Path(ruta)
        destino.parent.mkdir(parents=True, exist_ok=True)
        temporal = destino.with_name(destino.name + ".tmp")
        try:
            with open(temporal, "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(lineas) + "\n")
                f.flush()
                os.fsync(f.fileno())
            os.replace(temporal, destino)
        finally:
            if temporal.exists():
                temporal.unlink()

    @staticmethod
    def cargar(ruta: str | os.PathLike) -> ArbolDecision:
        """Reconstruye el árbol; ante cualquier fallo devuelve un ArbolDecision() nuevo."""
        try:
            with open(ruta, "r", encoding="utf-8", newline="") as f:
                contenido = f.read()
            lineas = [l.removesuffix("\r") for l in contenido.split("\n")]
            if lineas and lineas[-1] == "":
                lineas.pop()

            iterador = iter(lineas)
            raiz = RepositorioArbolTxt._leer_nodo(iterador)
            if raiz is None or next(iterador, None) is not None:
                raise ArchivoInvalidoError("Estructura incompleta o con datos sobrantes.")

            arbol = ArbolDecision()
            arbol.raiz = raiz
            return arbol
        except (OSError, UnicodeDecodeError, ArchivoInvalidoError, RecursionError):
            return ArbolDecision()

    @staticmethod
    def _leer_nodo(lineas: Iterator[str]) -> Optional[Nodo]:
        try:
            linea = next(lineas)
        except StopIteration:
            raise ArchivoInvalidoError("Fin de archivo inesperado.") from None

        if linea == _NULO:
            return None

        campos = _dividir_campos(linea)
        tipo = campos[0]

        if tipo == "Q" and len(campos) == 2 and campos[1]:
            izquierdo = RepositorioArbolTxt._leer_nodo(lineas)
            derecho = RepositorioArbolTxt._leer_nodo(lineas)
            if izquierdo is None or derecho is None:
                raise ArchivoInvalidoError("Una pregunta requiere dos hijos.")
            return Nodo(texto=campos[1], izquierdo=izquierdo, derecho=derecho)

        if tipo == "P" and len(campos) == 3 and campos[1] and campos[2]:
            if (
                RepositorioArbolTxt._leer_nodo(lineas) is not None
                or RepositorioArbolTxt._leer_nodo(lineas) is not None
            ):
                raise ArchivoInvalidoError("Un perfil no puede tener hijos.")
            return Nodo(texto=campos[2], perfil=Perfil(campos[1], campos[2]))

        raise ArchivoInvalidoError(f"Registro inválido: {linea!r}")

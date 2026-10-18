"""Módulo de respaldo offline para consejos financieros locales."""

import os
from pathlib import Path


def obtener_consejo_local(id_perfil: str) -> str:
    """Obtiene el diagnóstico y plan de acción desde el archivo local consejos_base.txt."""
    ruta_archivo = Path(__file__).resolve().parent.parent.parent / "data" / "consejos_base.txt"
    if not ruta_archivo.is_file():
        return f"No se encontró el archivo de consejos de respaldo en {ruta_archivo}."

    id_normalizado = id_perfil.strip().lower()
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea or "|" not in linea:
                    continue
                clave, contenido = linea.split("|", 1)
                if clave.strip().lower() == id_normalizado:
                    return contenido.replace("\\n", "\n")
        return f"No se encontró un consejo local para el perfil '{id_perfil}'."
    except Exception as error:
        return f"Error al leer el archivo de consejos locales: {error}"
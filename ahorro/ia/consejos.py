# ahorro/ia/consejos.py

import os

def obtener_consejo_local(id_perfil):
    """
    Lee un consejo base local usando el identificador de perfil (Plan B - 9.3).
    Busca en el archivo data/consejos_base.txt.
    """
    # Navega hacia arriba: ahorro/ia -> ahorro -> raíz -> data/consejos_base.txt
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_proyecto = os.path.dirname(os.path.dirname(ruta_actual))
    ruta_archivo = os.path.join(ruta_proyecto, 'data', 'consejos_base.txt')
    
    print("[Modo Offline] Mostrando consejo educativo guardado localmente.\n")
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea or '|' not in linea:
                    continue
                    
                partes = linea.split('|', 1)
                
                # Se compara ignorando mayúsculas/minúsculas
                if partes[0].strip().lower() == id_perfil.lower():
                    return partes[1].replace("\\n", "\n")
                    
        return f"No se encontró un consejo local detallado para el perfil '{id_perfil}'."
        
    except FileNotFoundError:
        return f"Error: No se encontró el archivo {ruta_archivo}. Verifica que exista en la carpeta 'data'."# ahorro/ia/consejos.py

import os

def obtener_consejo_local(id_perfil):
    """
    Lee un consejo base local usando el identificador de perfil (Plan B - 9.3).
    Busca en el archivo data/consejos_base.txt.
    """
    # Navega hacia arriba: ahorro/ia -> ahorro -> raíz -> data/consejos_base.txt
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_proyecto = os.path.dirname(os.path.dirname(ruta_actual))
    ruta_archivo = os.path.join(ruta_proyecto, 'data', 'consejos_base.txt')
    
    print("[Modo Offline] Mostrando consejo educativo guardado localmente.\n")
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea or '|' not in linea:
                    continue
                    
                partes = linea.split('|', 1)
                
                # Se compara ignorando mayúsculas/minúsculas
                if partes[0].strip().lower() == id_perfil.lower():
                    return partes[1].replace("\\n", "\n")
                    
        return f"No se encontró un consejo local detallado para el perfil '{id_perfil}'."
        
    except FileNotFoundError:
        return f"Error: No se encontró el archivo {ruta_archivo}. Verifica que exista en la carpeta 'data'."
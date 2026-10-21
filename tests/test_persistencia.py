"""Pruebas unitarias para la persistencia del árbol de 63 nodos en formato TXT preorden."""

from ahorro.core.arbol import ArbolDecision
from ahorro.core.perfil import Perfil
from ahorro.data_access.txt import RepositorioArbolTxt


def _estructura(arbol):
    return [
        None if n is None else (n.texto, n.perfil)
        for n in arbol.obtener_preorden()
    ]


def test_guardar_y_cargar_preserva_estructura(tmp_path):
    ruta = tmp_path / "arbol.txt"
    original = ArbolDecision()

    RepositorioArbolTxt.guardar(original, ruta)
    cargado = RepositorioArbolTxt.cargar(ruta)

    assert _estructura(cargado) == _estructura(original)
    assert not (tmp_path / "arbol.txt.tmp").exists()


def test_formato_preorden_con_marcadores(tmp_path):
    ruta = tmp_path / "arbol.txt"
    RepositorioArbolTxt.guardar(ArbolDecision(), ruta)

    lineas = ruta.read_text(encoding="utf-8").splitlines()
    assert lineas[0].startswith("Q|¿Tus ingresos mensuales")
    assert "P|ahorrador_visionario_avanzado|Ahorrador Visionario de Alto Rendimiento" in lineas
    assert len(lineas) == 63 + 64


def test_caracteres_especiales_se_escapan_y_restauran(tmp_path):
    ruta = tmp_path / "arbol.txt"
    arbol = ArbolDecision()
    pregunta = "¿A|B\\C\nlinea?"
    assert arbol.aprender([True, True, True, True, True], pregunta, Perfil("a|b", "Nom|bre\\x\ny"))

    RepositorioArbolTxt.guardar(arbol, ruta)
    cargado = RepositorioArbolTxt.cargar(ruta)

    nodo = cargado.avanzar(cargado.avanzar(cargado.avanzar(cargado.avanzar(cargado.avanzar(cargado.raiz, True), True), True), True), True)
    assert nodo.texto == pregunta
    assert nodo.izquierdo.perfil == Perfil("a|b", "Nom|bre\\x\ny")
    assert _estructura(cargado) == _estructura(arbol)


def test_guardar_sobrescribe_archivo_existente(tmp_path):
    ruta = tmp_path / "arbol.txt"
    ruta.write_text("basura", encoding="utf-8")

    RepositorioArbolTxt.guardar(ArbolDecision(), ruta)

    assert ruta.read_text(encoding="utf-8").startswith("Q|")


def test_cargar_archivo_inexistente_devuelve_arbol_por_defecto(tmp_path):
    cargado = RepositorioArbolTxt.cargar(tmp_path / "no_existe.txt")
    assert _estructura(cargado) == _estructura(ArbolDecision())


def test_cargar_archivo_corrupto_devuelve_arbol_por_defecto(tmp_path):
    por_defecto = _estructura(ArbolDecision())
    contenidos = [
        "",
        "#\n",
        "Q|solo pregunta\n",
        "X|desconocido\n",
        "P|id|nombre\n#\n",
        "P|id|nombre\n#\n#\nsobrante\n",
        "Q|pregunta \\z\nP|a|b\n#\n#\nP|c|d\n#\n#\n",
    ]
    for i, contenido in enumerate(contenidos):
        ruta = tmp_path / f"corrupto_{i}.txt"
        ruta.write_text(contenido, encoding="utf-8")
        assert _estructura(RepositorioArbolTxt.cargar(ruta)) == por_defecto, contenido


def test_cargar_archivo_no_utf8_devuelve_arbol_por_defecto(tmp_path):
    ruta = tmp_path / "binario.txt"
    ruta.write_bytes(b"\xff\xfe\x00Q|\x80\n")
    assert _estructura(RepositorioArbolTxt.cargar(ruta)) == _estructura(ArbolDecision())

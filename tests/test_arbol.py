from ahorro.core.arbol import ArbolDecision
from ahorro.core.perfil import Perfil


def _contar(nodo) -> int:
    if nodo is None:
        return 0
    return 1 + _contar(nodo.izquierdo) + _contar(nodo.derecho)


def _navegar(arbol, respuestas):
    nodo = arbol.raiz
    for r in respuestas:
        nodo = arbol.avanzar(nodo, r)
    return nodo


def test_arbol_inicial_tiene_siete_nodos():
    assert _contar(ArbolDecision().raiz) == 7


def test_navegacion_determinista():
    arbol = ArbolDecision()
    assert _navegar(arbol, [True, True]).perfil.id_perfil == "consolidado"
    assert _navegar(arbol, [True, False]).perfil.id_perfil == "esporadico"
    assert _navegar(arbol, [False, True]).perfil.id_perfil == "apagafuegos"
    assert _navegar(arbol, [False, False]).perfil.id_perfil == "fuga_capital"


def test_aprender_agrega_exactamente_dos_nodos():
    arbol = ArbolDecision()
    antes = _contar(arbol.raiz)
    nuevo = Perfil("inversor", "Inversor")

    assert arbol.aprender([True, True], "¿Inviertes tu ahorro?", nuevo) is True

    assert _contar(arbol.raiz) == antes + 2
    pregunta = _navegar(arbol, [True, True])
    assert pregunta.texto == "¿Inviertes tu ahorro?"
    assert pregunta.perfil is None
    assert pregunta.izquierdo.perfil == nuevo
    assert pregunta.derecho.perfil.id_perfil == "consolidado"


def test_aprender_rechaza_ruta_invalida_o_no_hoja():
    arbol = ArbolDecision()
    nuevo = Perfil("x", "X")
    assert arbol.aprender([True], "¿Pregunta?", nuevo) is False
    assert arbol.aprender([True, True, True], "¿Pregunta?", nuevo) is False
    assert _contar(arbol.raiz) == 7


def test_desmontar_postorden_traza_y_raiz_none():
    arbol = ArbolDecision()
    traza = arbol.desmontar_postorden()

    textos = [t.removeprefix("Visitado para desmontaje: ") for t in traza]
    assert textos == [
        "Ahorrador Consolidado",
        "Ahorrador Esporádico",
        "¿Apartas el ahorro cuando cobras?",
        "Perfil Apagafuegos",
        "Fuga de Capital",
        "¿Tus deudas superan el 30 % de tus ingresos?",
        "¿Te sobra dinero al final de mes?",
    ]
    assert arbol.raiz is None

"""Pruebas unitarias para el árbol binario ampliado de 63 nodos y 32 arquetipos."""

from ahorro.core.arbol import ArbolDecision
from ahorro.core.perfil import Perfil
from ahorro.core.soluciones import SOLUCIONES_CATALOGO, obtener_soluciones_perfil
from ahorro.ia.ollama import construir_prompt_maestro


def _contar(nodo) -> int:
    if nodo is None:
        return 0
    return 1 + _contar(nodo.izquierdo) + _contar(nodo.derecho)


def _navegar(arbol, respuestas):
    nodo = arbol.raiz
    for r in respuestas:
        nodo = arbol.avanzar(nodo, r)
    return nodo


def test_arbol_inicial_tiene_sesenta_y_tres_nodos():
    assert _contar(ArbolDecision().raiz) == 63


def test_navegacion_determinista_rutas_clave():
    arbol = ArbolDecision()
    assert _navegar(arbol, [True, True, True, True, True]).perfil.id_perfil == "ahorrador_visionario_avanzado"
    assert _navegar(arbol, [True, True, True, True, False]).perfil.id_perfil == "ahorrador_visionario_practico"
    assert _navegar(arbol, [True, True, True, False, True]).perfil.id_perfil == "ahorrador_conservador_blindado"
    assert _navegar(arbol, [True, True, False, True, True]).perfil.id_perfil == "ahorrador_metodico_tradicional"
    assert _navegar(arbol, [True, False, True, True, True]).perfil.id_perfil == "consumista_consciente_controlado"
    assert _navegar(arbol, [False, True, True, True, True]).perfil.id_perfil == "endeudado_recuperacion_disciplinado"
    assert _navegar(arbol, [False, True, False, True, True]).perfil.id_perfil == "endeudado_critico_alto_riesgo"
    assert _navegar(arbol, [False, False, True, True, True]).perfil.id_perfil == "superviviente_proactivo_generador"
    assert _navegar(arbol, [False, False, False, False, False]).perfil.id_perfil == "superviviente_emergencia_resistente"


def test_aprender_agrega_exactamente_dos_nodos():
    arbol = ArbolDecision()
    antes = _contar(arbol.raiz)
    nuevo = Perfil("inversor_cripto_avanzado", "Inversor Cripto Avanzado")

    assert arbol.aprender([True, True, True, True, True], "¿Inviertes en staking y DeFi?", nuevo) is True
    assert _contar(arbol.raiz) == antes + 2

    pregunta = _navegar(arbol, [True, True, True, True, True])
    assert pregunta.texto == "¿Inviertes en staking y DeFi?"
    assert pregunta.perfil is None
    assert pregunta.izquierdo.perfil == nuevo
    assert pregunta.derecho.perfil.id_perfil == "ahorrador_visionario_avanzado"


def test_aprender_rechaza_ruta_invalida_o_no_hoja():
    arbol = ArbolDecision()
    nuevo = Perfil("x", "X")
    assert arbol.aprender([True], "¿Pregunta?", nuevo) is False
    assert arbol.aprender([True, True, True, True, True, True], "¿Pregunta?", nuevo) is False
    assert _contar(arbol.raiz) == 63


def test_desmontar_postorden_limpia_raiz():
    arbol = ArbolDecision()
    traza = arbol.desmontar_postorden()
    assert len(traza) == 63
    assert arbol.raiz is None


def test_catalogo_cincuenta_soluciones_y_arquetipos():
    assert len(SOLUCIONES_CATALOGO) == 50
    soluciones_vis = obtener_soluciones_perfil("ahorrador_visionario_avanzado")
    assert len(soluciones_vis) >= 5
    for sol in soluciones_vis:
        assert sol.startswith("- ")


def test_construccion_prompt_maestro_profundo():
    prompt = construir_prompt_maestro(
        perfil_estudiante="Ahorrador Visionario de Alto Rendimiento",
        respuestas_formateadas="- ¿Ingresos superan gastos? => SÍ",
        soluciones_mapeadas="- Inversión en CDT y fondos",
    )
    assert "Ahorrador Visionario de Alto Rendimiento" in prompt
    assert "PLAN DE ACCIÓN DE 3 PASOS" in prompt
    assert "REGLA DE ORO" in prompt

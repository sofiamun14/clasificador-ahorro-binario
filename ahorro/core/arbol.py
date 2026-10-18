"""Árbol binario universitario ampliado con 31 preguntas y 32 arquetipos estudiantiles."""

from ahorro.core.nodo import Nodo
from ahorro.core.perfil import Perfil


class ArbolDecision:
    """Gestiona el árbol binario de 5 niveles para diagnóstico financiero estudiantil profundo."""

    def __init__(self):
        self.raiz = self._construir_arbol_inicial()

    def _construir_arbol_inicial(self) -> Nodo:
        """Construye un árbol balanceado de 63 nodos con 31 preguntas y 32 arquetipos."""
        # 1. Rama Superávit -> Ahorro Sí -> Rendimiento Sí -> Diversifica Sí
        p01 = Nodo("Ahorrador Visionario de Alto Rendimiento", perfil=Perfil("ahorrador_visionario_avanzado", "Ahorrador Visionario de Alto Rendimiento"))
        p02 = Nodo("Ahorrador Visionario Práctico", perfil=Perfil("ahorrador_visionario_practico", "Ahorrador Visionario Práctico"))
        q05 = Nodo("¿Revisas y optimizas mensualmente tus costos de inversión (comisiones, 4x1000, tasas efectivas anuales)?", izquierdo=p01, derecho=p02)

        # 2. Rama Superávit -> Ahorro Sí -> Rendimiento Sí -> Diversifica No
        p03 = Nodo("Ahorrador Conservador Blindado", perfil=Perfil("ahorrador_conservador_blindado", "Ahorrador Conservador Blindado"))
        p04 = Nodo("Ahorrador Conservador en Construcción", perfil=Perfil("ahorrador_conservador_vulnerable", "Ahorrador Conservador en Construcción"))
        q06 = Nodo("¿Tienes una reserva de emergencias equivalente a al menos 3 meses de tus gastos académicos esenciales?", izquierdo=p03, derecho=p04)

        q04 = Nodo("¿Diversificas tu ahorro en metas a mediano/largo plazo (fondos indexados, certificaciones, emprendimiento) además de tu fondo de emergencias?", izquierdo=q05, derecho=q06)

        # 3. Rama Superávit -> Ahorro Sí -> Rendimiento No -> Meta Sí
        p05 = Nodo("Ahorrador Metódico Tradicional", perfil=Perfil("ahorrador_metodico_tradicional", "Ahorrador Metódico Tradicional"))
        p06 = Nodo("Ahorrador Disciplinado Manual", perfil=Perfil("ahorrador_disciplinado_manual", "Ahorrador Disciplinado Manual"))
        q08 = Nodo("¿Automatizas el traslado de tu ahorro el mismo día en que recibes tus ingresos?", izquierdo=p05, derecho=p06)

        # 4. Rama Superávit -> Ahorro Sí -> Rendimiento No -> Meta No
        p07 = Nodo("Ahorrador Tentado e Inestable", perfil=Perfil("ahorrador_tentado_inestable", "Ahorrador Tentado e Inestable"))
        p08 = Nodo("Ahorrador Pasivo Estancado", perfil=Perfil("ahorrador_pasivo_estancado", "Ahorrador Pasivo Estancado"))
        q09 = Nodo("¿Sueles retirar dinero de ese fondo guardado para compras no esenciales durante el semestre?", izquierdo=p07, derecho=p08)

        q07 = Nodo("¿Tienes una meta o propósito específico definido con fecha y monto para ese dinero guardado?", izquierdo=q08, derecho=q09)

        q03 = Nodo("¿Tienes tu ahorro en algún instrumento que genere rendimientos (CDT, billetera digital con rentabilidad) en lugar de tenerlo quieto en efectivo o en una cuenta tradicional?", izquierdo=q04, derecho=q07)

        # 5. Rama Superávit -> Ahorro No -> Hormiga Sí -> Registro Sí
        p09 = Nodo("Consumista Consciente en Regulación", perfil=Perfil("consumista_consciente_controlado", "Consumista Consciente en Regulación"))
        p10 = Nodo("Consumista Consciente Desbordado", perfil=Perfil("consumista_consciente_desbordado", "Consumista Consciente Desbordado"))
        q12 = Nodo("¿Fijas un tope máximo semanal en efectivo o bolsillo digital exclusivo para tus salidas de ocio?", izquierdo=p09, derecho=p10)

        # 6. Rama Superávit -> Ahorro No -> Hormiga Sí -> Registro No
        p11 = Nodo("Consumista Impulsivo Crónico", perfil=Perfil("consumista_impulsivo_cronico", "Consumista Impulsivo Crónico"))
        p12 = Nodo("Consumista Social Ocasional", perfil=Perfil("consumista_social_ocasional", "Consumista Social Ocasional"))
        q13 = Nodo("¿Sueles comprar antojos o comidas fuera del campus diariamente por impulso o desorganización?", izquierdo=p11, derecho=p12)

        q11 = Nodo("¿Llevas algún registro semanal o presupuesto en apps de lo que gastas en ocio y antojos universitarios?", izquierdo=q12, derecho=q13)

        # 7. Rama Superávit -> Ahorro No -> Hormiga No -> Compras Grandes Sí
        p13 = Nodo("Comprador de Temporada Reflexivo", perfil=Perfil("comprador_temporada_reflexivo", "Comprador de Temporada Reflexivo"))
        p14 = Nodo("Comprador de Temporada Impulsivo", perfil=Perfil("comprador_temporada_impulsivo", "Comprador de Temporada Impulsivo"))
        q15 = Nodo("¿Aplicas la regla de esperar 48 horas antes de efectuar una compra importante no académica?", izquierdo=p13, derecho=p14)

        # 8. Rama Superávit -> Ahorro No -> Hormiga No -> Compras Grandes No
        p15 = Nodo("Acumulador Inconsciente con Fugas", perfil=Perfil("acumulador_inconsciente", "Acumulador Inconsciente con Fugas"))
        p16 = Nodo("Consumista con Superávit Relajado", perfil=Perfil("consumista_superavit_relajado", "Consumista con Superávit Relajado"))
        q16 = Nodo("¿Dejas tu excedente quieto en tu cuenta principal gastándolo sin darte cuenta a fin de mes?", izquierdo=p15, derecho=p16)

        q14 = Nodo("¿Tus excedentes se van principalmente en compras grandes esporádicas de ropa, tecnología o viajes no planificados?", izquierdo=q15, derecho=q16)

        q10 = Nodo("¿Sueles gastar la mayor parte de ese dinero sobrante en \"gastos hormiga\", domicilios o salidas de fin de semana?", izquierdo=q11, derecho=q14)

        q02 = Nodo("¿Destinas sistemáticamente al menos el 10% de ese dinero sobrante a un fondo de ahorro antes de gastar en entretenimiento?", izquierdo=q03, derecho=q10)

        # 9. Rama Déficit -> Deuda Sí -> Conoce Sí -> Plan Pagos Sí
        p17 = Nodo("Endeudado Estratégico Disciplinado", perfil=Perfil("endeudado_recuperacion_disciplinado", "Endeudado Estratégico Disciplinado"))
        p18 = Nodo("Endeudado Estratégico Reincidente", perfil=Perfil("endeudado_recuperacion_reincidente", "Endeudado Estratégico Reincidente"))
        q20 = Nodo("¿Has suspendido totalmente el uso de tarjetas de crédito mientras amortizas tu deuda actual?", izquierdo=p17, derecho=p18)

        # 10. Rama Déficit -> Deuda Sí -> Conoce Sí -> Plan Pagos No
        p19 = Nodo("Endeudado Consciente Activo", perfil=Perfil("endeudado_consciente_activo", "Endeudado Consciente Activo"))
        p20 = Nodo("Endeudado Consciente Estancado", perfil=Perfil("endeudado_consciente_estancado", "Endeudado Consciente Estancado"))
        q21 = Nodo("¿Pagas más de la cuota mínima mensual requerida por tus acreedores o bancos?", izquierdo=p19, derecho=p20)

        q19 = Nodo("¿Tienes un plan activo de pagos priorizados (método bola de nieve o avalancha) para amortizar la deuda?", izquierdo=q20, derecho=q21)

        # 11. Rama Déficit -> Deuda Sí -> Conoce No -> Paga Mínimo Sí
        p21 = Nodo("Endeudado Crítico de Alto Riesgo", perfil=Perfil("endeudado_critico_alto_riesgo", "Endeudado Crítico de Alto Riesgo"))
        p22 = Nodo("Endeudado Crítico en Bola de Nieve", perfil=Perfil("endeudado_critico_bancario", "Endeudado Crítico en Bola de Nieve"))
        q23 = Nodo("¿Acudes a aplicaciones de préstamos rápidos (gota a gota digital o plataformas no vigiladas)?", izquierdo=p21, derecho=p22)

        # 12. Rama Déficit -> Deuda Sí -> Conoce No -> Paga Mínimo No
        p23 = Nodo("Endeudado Informal Vulnerable", perfil=Perfil("endeudado_informal_vulnerable", "Endeudado Informal Vulnerable"))
        p24 = Nodo("Endeudado Ciego Financiero", perfil=Perfil("endeudado_ciego_financiero", "Endeudado Ciego Financiero"))
        q24 = Nodo("¿Tus deudas son principalmente préstamos informales con familiares o amigos de confianza?", izquierdo=p23, derecho=p24)

        q22 = Nodo("¿Pagas únicamente el monto mínimo exigido o solicitas nuevos créditos/préstamos para pagar los anteriores?", izquierdo=q23, derecho=q24)

        q18 = Nodo("¿Conoces exactamente a cuánto asciende el total de tu deuda y la tasa de interés que estás pagando por ella?", izquierdo=q19, derecho=q22)

        # 13. Rama Déficit -> Deuda No -> Recorte Sí -> Acciones Cotidianas Sí
        p25 = Nodo("Superviviente Proactivo Generador", perfil=Perfil("superviviente_proactivo_generador", "Superviviente Proactivo Generador"))
        p26 = Nodo("Superviviente Proactivo Ahorrador", perfil=Perfil("superviviente_proactivo_ahorrador", "Superviviente Proactivo Ahorrador"))
        q27 = Nodo("¿Generas ingresos complementarios en tus tiempos libres (tutorías, freelance, ventas entre clases)?", izquierdo=p25, derecho=p26)

        # 14. Rama Déficit -> Deuda No -> Recorte Sí -> Acciones Cotidianas No
        p27 = Nodo("Superviviente Ajustable Planificado", perfil=Perfil("superviviente_ajustable_planificado", "Superviviente Ajustable Planificado"))
        p28 = Nodo("Superviviente Ajustable Postergador", perfil=Perfil("superviviente_ajustable_postergador", "Superviviente Ajustable Postergador"))
        q28 = Nodo("¿Cuentas con un plan semanal por escrito para empezar a recortar esos gastos identificados?", izquierdo=p27, derecho=p28)

        q26 = Nodo("¿Has implementado acciones de ahorro cotidiano (preparar comida en casa, usar bicicleta o tarifa universitaria de transporte)?", izquierdo=q27, derecho=q28)

        # 15. Rama Déficit -> Deuda No -> Recorte No -> Apoyos Sí
        p29 = Nodo("Superviviente con Apoyo Gestionado", perfil=Perfil("superviviente_apoyo_gestionado", "Superviviente con Apoyo Gestionado"))
        p30 = Nodo("Superviviente con Apoyo Pasivo", perfil=Perfil("superviviente_apoyo_pasivo", "Superviviente con Apoyo Pasivo"))
        q30 = Nodo("¿Has acudido a Bienestar Universitario o a la coordinación de tu carrera para gestionar auxilios adicionales?", izquierdo=p29, derecho=p30)

        # 16. Rama Déficit -> Deuda No -> Recorte No -> Apoyos No
        p31 = Nodo("Superviviente Crítico en Alerta Roja", perfil=Perfil("superviviente_emergencia_extrema", "Superviviente Crítico en Alerta Roja"))
        p32 = Nodo("Superviviente Resiliente en Déficit", perfil=Perfil("superviviente_emergencia_resistente", "Superviviente Resiliente en Déficit"))
        q31 = Nodo("¿Tus gastos fijos obligatorios amenazan la continuidad de tu semestre académico?", izquierdo=p31, derecho=p32)

        q29 = Nodo("¿Cuentas con apoyos institucionales (bonos de alimentación, monitorías, becas) o familiares para amortiguar tu déficit?", izquierdo=q30, derecho=q31)

        q25 = Nodo("¿Tienes identificados al menos dos gastos variables que podrías recortar inmediatamente sin afectar tu desempeño académico?", izquierdo=q26, derecho=q29)

        q17 = Nodo("¿Recurres frecuentemente a deudas (tarjetas de crédito, préstamos de aplicaciones o amigos) para poder llegar a fin de mes?", izquierdo=q18, derecho=q25)

        raiz = Nodo(
            "¿Tus ingresos mensuales (mesada, trabajo, emprendimiento) superan tus gastos fijos obligatorios (transporte, alimentación, materiales de la universidad)?",
            izquierdo=q02,
            derecho=q17,
        )

        return raiz

    def avanzar(self, nodo: Nodo, respuesta_si: bool) -> Nodo:
        """Avanza al hijo izquierdo (Sí) o derecho (No)."""
        if respuesta_si:
            if nodo.izquierdo is None:
                raise ValueError("Ruta inválida: no hay hijo izquierdo.")
            return nodo.izquierdo
        if nodo.derecho is None:
            raise ValueError("Ruta inválida: no hay hijo derecho.")
        return nodo.derecho

    def aprender(self, ruta: list[bool], pregunta: str, nuevo_perfil: Perfil) -> bool:
        """Convierte una hoja en nueva pregunta: Sí es el nuevo perfil y No es el original."""
        if self.raiz is None:
            return False

        nodo_actual = self.raiz
        try:
            for respuesta in ruta:
                nodo_actual = self.avanzar(nodo_actual, respuesta)
        except ValueError:
            return False

        if not nodo_actual.es_hoja():
            return False

        perfil_original = nodo_actual.perfil
        texto_original = nodo_actual.texto

        nodo_actual.texto = pregunta
        nodo_actual.perfil = None
        nodo_actual.izquierdo = Nodo(nuevo_perfil.nombre, perfil=nuevo_perfil)
        nodo_actual.derecho = Nodo(texto_original, perfil=perfil_original)
        return True

    def listar_inorden(self) -> list[str]:
        """Recorrido Inorden (Izquierda, Raíz, Derecha)."""
        resultado = []

        def _recorrer(nodo: Nodo):
            if nodo is not None:
                _recorrer(nodo.izquierdo)
                resultado.append(nodo.texto)
                _recorrer(nodo.derecho)

        _recorrer(self.raiz)
        return resultado

    def obtener_preorden(self) -> list:
        """Recorrido Preorden con marcadores None para serialización."""
        resultado = []

        def _recorrer(nodo):
            if nodo is None:
                resultado.append(None)
                return
            resultado.append(nodo)
            _recorrer(nodo.izquierdo)
            _recorrer(nodo.derecho)

        _recorrer(self.raiz)
        return resultado

    def desmontar_postorden(self) -> list[str]:
        """Recorrido Postorden liberando enlaces y limpiando la raíz."""
        traza = []

        def _recorrer(nodo: Nodo):
            if nodo is None:
                return
            _recorrer(nodo.izquierdo)
            _recorrer(nodo.derecho)
            traza.append(f"Visitado para desmontaje: {nodo.texto}")
            nodo.izquierdo = None
            nodo.derecho = None

        _recorrer(self.raiz)
        self.raiz = None
        return traza

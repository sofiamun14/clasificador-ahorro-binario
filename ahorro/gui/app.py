"""Interfaz gráfica estilo Hello Kitty, rosadita, cute y minimalista con CustomTkinter."""

import threading
import tkinter as tk
from typing import Optional

import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ahorro.core.arbol import ArbolDecision
from ahorro.core.nodo import Nodo
from ahorro.core.perfil import Perfil
from ahorro.core.soluciones import obtener_soluciones_perfil
from ahorro.ia.consejos import obtener_consejo_local
from ahorro.ia.ollama import ClienteOllama


class AppGUI(ctk.CTk):
    """Aplicación de diagnóstico financiero con estética cute minimalista estilo Hello Kitty."""

    def __init__(self, arbol: Optional[ArbolDecision] = None):
        super().__init__()
        self.arbol = arbol or ArbolDecision()
        self.ia = ClienteOllama()

        self.title("🎀 Clasificador Financiero Universitario • Hello Kitty Edition 🌸")
        self.geometry("1040x740")
        self.minsize(920, 660)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        self.nodo_actual: Nodo = self.arbol.raiz
        self.ruta: list[bool] = []
        self.historial: list[str] = []
        self.nivel: int = 1
        self.total_niveles: int = 5
        self.ingreso_val: float = 0.0
        self.gasto_val: float = 0.0

        self.contenedor_principal = ctk.CTkFrame(self, corner_radius=0, fg_color="#fff1f5")
        self.contenedor_principal.pack(fill="both", expand=True)

        self._crear_encabezado()
        self._mostrar_pantalla_diagnostico()

    def _crear_encabezado(self):
        """Barra superior cute con moñitos y tonos pastel."""
        barra = ctk.CTkFrame(
            self.contenedor_principal,
            height=68,
            fg_color="#fce7f3",
            corner_radius=0,
            border_width=1,
            border_color="#fbcfe8",
        )
        barra.pack(fill="x", side="top")

        box_izq = ctk.CTkFrame(barra, fg_color="transparent")
        box_izq.pack(side="left", padx=24, pady=12)

        lbl_logo = ctk.CTkLabel(box_izq, text="🎀", font=ctk.CTkFont(size=26))
        lbl_logo.pack(side="left", padx=(0, 10))

        lbl_titulo = ctk.CTkLabel(
            box_izq,
            text="Clasificador Financiero Universitario",
            font=ctk.CTkFont(size=19, weight="bold"),
            text_color="#831843",
        )
        lbl_titulo.pack(side="left")

        box_der = ctk.CTkFrame(barra, fg_color="transparent")
        box_der.pack(side="right", padx=24, pady=12)

        lbl_badge_sub = ctk.CTkLabel(
            box_der,
            text="✨ Hello Kitty Edition • Ollama Phi-3 🐱",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#be185d",
            fg_color="#ffffff",
            corner_radius=14,
            padx=12,
            pady=4,
        )
        lbl_badge_sub.pack()

    def _limpiar_cuerpo(self):
        """Limpia el área central preservando el encabezado."""
        for widget in self.contenedor_principal.winfo_children()[1:]:
            widget.destroy()

    def _mostrar_pantalla_diagnostico(self):
        """Pantalla 1: Tarjeta suave con bordes redondeados y botones Sí/No estilo Hello Kitty."""
        self._limpiar_cuerpo()

        cuerpo = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True, padx=36, pady=20)

        tarjeta_progreso = ctk.CTkFrame(
            cuerpo,
            fg_color="#ffffff",
            corner_radius=18,
            border_width=1.5,
            border_color="#fbcfe8",
        )
        tarjeta_progreso.pack(fill="x", pady=(0, 16), padx=12)

        lbl_paso = ctk.CTkLabel(
            tarjeta_progreso,
            text=f"🌸 Pregunta #{self.nivel} de {self.total_niveles} • Descubriendo tu Arquetipo",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#db2777",
        )
        lbl_paso.pack(anchor="w", padx=24, pady=(12, 4))

        progreso = min(1.0, self.nivel / float(self.total_niveles))
        barra = ctk.CTkProgressBar(
            tarjeta_progreso,
            height=10,
            progress_color="#ec4899",
            fg_color="#fce7f3",
            corner_radius=5,
        )
        barra.set(progreso)
        barra.pack(fill="x", padx=24, pady=(0, 14))

        tarjeta_pregunta = ctk.CTkFrame(
            cuerpo,
            fg_color="#ffffff",
            corner_radius=22,
            border_width=1.5,
            border_color="#fbcfe8",
        )
        tarjeta_pregunta.pack(fill="both", expand=True, padx=12, pady=6)

        lbl_icono = ctk.CTkLabel(tarjeta_pregunta, text="🌷", font=ctk.CTkFont(size=38))
        lbl_icono.pack(pady=(22, 6))

        lbl_texto = ctk.CTkLabel(
            tarjeta_pregunta,
            text=self.nodo_actual.texto,
            font=ctk.CTkFont(size=18, weight="bold"),
            wraplength=760,
            justify="center",
            text_color="#4a044e",
        )
        lbl_texto.pack(padx=28, pady=(6, 16))

        if self.historial:
            traza = "Ruta: " + " → ".join(["Sí 🎀" if "SÍ" in h else "No 🌸" for h in self.historial])
            lbl_traza = ctk.CTkLabel(
                tarjeta_pregunta,
                text=traza,
                font=ctk.CTkFont(size=12),
                text_color="#be185d",
            )
            lbl_traza.pack(pady=(0, 14))

        if self.nivel == 1:
            frame_montos = ctk.CTkFrame(
                tarjeta_pregunta,
                fg_color="#fdf2f8",
                corner_radius=14,
                border_width=1,
                border_color="#fbcfe8",
            )
            frame_montos.pack(padx=36, pady=(0, 16), fill="x")

            lbl_montos_tit = ctk.CTkLabel(
                frame_montos,
                text="👛 Opcional: Ingresa tus valores mensuales para tu gráfico personalizado",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#9d174d",
            )
            lbl_montos_tit.pack(pady=(8, 4))

            box_inputs = ctk.CTkFrame(frame_montos, fg_color="transparent")
            box_inputs.pack(pady=(0, 10))

            lbl_ing = ctk.CTkLabel(box_inputs, text="Ingresos ($):", font=ctk.CTkFont(size=12), text_color="#701a75")
            lbl_ing.grid(row=0, column=0, padx=8, pady=4)
            self.entry_ingreso = ctk.CTkEntry(
                box_inputs,
                placeholder_text="ej: 800000",
                width=135,
                border_color="#f472b6",
                fg_color="#ffffff",
                text_color="#831843",
            )
            self.entry_ingreso.grid(row=0, column=1, padx=8, pady=4)

            lbl_gas = ctk.CTkLabel(box_inputs, text="Gastos fijos ($):", font=ctk.CTkFont(size=12), text_color="#701a75")
            lbl_gas.grid(row=0, column=2, padx=8, pady=4)
            self.entry_gasto = ctk.CTkEntry(
                box_inputs,
                placeholder_text="ej: 520000",
                width=135,
                border_color="#f472b6",
                fg_color="#ffffff",
                text_color="#831843",
            )
            self.entry_gasto.grid(row=0, column=3, padx=8, pady=4)

        frame_botones = ctk.CTkFrame(tarjeta_pregunta, fg_color="transparent")
        frame_botones.pack(pady=(12, 22))

        btn_si = ctk.CTkButton(
            frame_botones,
            text="🎀 SÍ",
            width=210,
            height=54,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#ec4899",
            hover_color="#db2777",
            text_color="#ffffff",
            corner_radius=26,
            command=lambda: self._responder(True),
        )
        btn_si.grid(row=0, column=0, padx=18)

        btn_no = ctk.CTkButton(
            frame_botones,
            text="🌸 NO",
            width=210,
            height=54,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#fda4af",
            hover_color="#fb7185",
            text_color="#ffffff",
            corner_radius=26,
            command=lambda: self._responder(False),
        )
        btn_no.grid(row=0, column=1, padx=18)

        btn_reiniciar = ctk.CTkButton(
            cuerpo,
            text="↺ Reiniciar",
            width=110,
            height=30,
            fg_color="#fce7f3",
            hover_color="#fbcfe8",
            text_color="#9d174d",
            font=ctk.CTkFont(size=12),
            corner_radius=15,
            command=self._reiniciar,
        )
        btn_reiniciar.pack(anchor="e", padx=12, pady=(4, 0))

    def _responder(self, respuesta_si: bool):
        """Registra la respuesta y navega en el árbol binario."""
        if self.nivel == 1 and hasattr(self, "entry_ingreso"):
            try:
                txt_ing = self.entry_ingreso.get().strip().replace(".", "").replace(",", "")
                txt_gas = self.entry_gasto.get().strip().replace(".", "").replace(",", "")
                if txt_ing:
                    self.ingreso_val = float(txt_ing)
                if txt_gas:
                    self.gasto_val = float(txt_gas)
            except ValueError:
                pass

        if self.ingreso_val == 0.0 and self.gasto_val == 0.0:
            if respuesta_si and self.nivel == 1:
                self.ingreso_val, self.gasto_val = 800000.0, 520000.0
            elif not respuesta_si and self.nivel == 1:
                self.ingreso_val, self.gasto_val = 550000.0, 720000.0

        tag_resp = "SÍ" if respuesta_si else "NO"
        self.historial.append(f"- {self.nodo_actual.texto} => {tag_resp}")
        self.ruta.append(respuesta_si)
        self.nodo_actual = self.arbol.avanzar(self.nodo_actual, respuesta_si)
        self.nivel += 1

        if self.nodo_actual.es_hoja():
            self._mostrar_pantalla_resultados_inmediata()
        else:
            self._mostrar_pantalla_diagnostico()

    def _mostrar_pantalla_resultados_inmediata(self):
        """Pantalla 3: Muestra el arquetipo y soluciones de inmediato, consultando a Phi-3 en paralelo."""
        self._limpiar_cuerpo()

        perfil_id = self.nodo_actual.perfil.id if self.nodo_actual.perfil else "sin_perfil"
        soluciones = obtener_soluciones_perfil(perfil_id)
        consejo_base = obtener_consejo_local(perfil_id)

        cuerpo = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True, padx=28, pady=14)

        barra_perfil = ctk.CTkFrame(
            cuerpo,
            fg_color="#ffffff",
            corner_radius=16,
            border_width=1.5,
            border_color="#fbcfe8",
        )
        barra_perfil.pack(fill="x", pady=(0, 10))

        box_tit = ctk.CTkFrame(barra_perfil, fg_color="transparent")
        box_tit.pack(side="left", padx=20, pady=12)

        lbl_icono_arquetipo = ctk.CTkLabel(box_tit, text="🎀", font=ctk.CTkFont(size=24))
        lbl_icono_arquetipo.pack(side="left", padx=(0, 8))

        lbl_resultado = ctk.CTkLabel(
            box_tit,
            text=f"Arquetipo: {self.nodo_actual.texto}",
            font=ctk.CTkFont(size=19, weight="bold"),
            text_color="#831843",
        )
        lbl_resultado.pack(side="left")

        dif = self.ingreso_val - self.gasto_val
        estado_badge = f"✨ Superávit: +${dif:,.0f}" if dif >= 0 else f"⚠️ Déficit: -${abs(dif):,.0f}"
        color_badge = "#ec4899" if dif >= 0 else "#f43f5e"

        lbl_badge = ctk.CTkLabel(
            barra_perfil,
            text=estado_badge,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ffffff",
            fg_color=color_badge,
            corner_radius=12,
            padx=14,
            pady=6,
        )
        lbl_badge.pack(side="right", padx=20, pady=12)

        panel_central = ctk.CTkFrame(cuerpo, fg_color="transparent")
        panel_central.pack(fill="both", expand=True)

        panel_izquierdo = ctk.CTkFrame(
            panel_central,
            fg_color="#ffffff",
            corner_radius=18,
            border_width=1.5,
            border_color="#fbcfe8",
            width=390,
        )
        panel_izquierdo.pack(side="left", fill="both", padx=(0, 8), pady=2)
        panel_izquierdo.pack_propagate(False)

        lbl_grafico_tit = ctk.CTkLabel(
            panel_izquierdo,
            text="👛 Balance Financiero Mensual",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#831843",
        )
        lbl_grafico_tit.pack(pady=(10, 4))

        self._incrustar_grafico(panel_izquierdo)

        lbl_sol_tit = ctk.CTkLabel(
            panel_izquierdo,
            text="🌸 Soluciones Pre-aprobadas",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#be185d",
        )
        lbl_sol_tit.pack(pady=(6, 2))

        frame_sol = ctk.CTkScrollableFrame(panel_izquierdo, fg_color="#fff1f5", height=140, corner_radius=12)
        frame_sol.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        for sol in soluciones:
            lbl_item = ctk.CTkLabel(
                frame_sol,
                text=sol,
                font=ctk.CTkFont(size=11),
                wraplength=330,
                justify="left",
                text_color="#701a75",
            )
            lbl_item.pack(anchor="w", pady=2)

        panel_derecho = ctk.CTkFrame(
            panel_central,
            fg_color="#ffffff",
            corner_radius=18,
            border_width=1.5,
            border_color="#fbcfe8",
        )
        panel_derecho.pack(side="right", fill="both", expand=True, padx=(8, 0), pady=2)

        cabecera_derecha = ctk.CTkFrame(panel_derecho, fg_color="transparent")
        cabecera_derecha.pack(fill="x", padx=16, pady=(10, 4))

        lbl_plan_tit = ctk.CTkLabel(
            cabecera_derecha,
            text="✨ Plan de Acción Personalizado (Ollama Phi-3)",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#831843",
        )
        lbl_plan_tit.pack(side="left")

        self.lbl_estado_ia = ctk.CTkLabel(
            cabecera_derecha,
            text="🎀 Consultando a Phi-3...",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#ec4899",
        )
        self.lbl_estado_ia.pack(side="right")

        self.txt_plan = ctk.CTkTextbox(
            panel_derecho,
            fg_color="#fff1f5",
            text_color="#4a044e",
            font=ctk.CTkFont(size=13),
            wrap="word",
            corner_radius=12,
        )
        self.txt_plan.pack(fill="both", expand=True, padx=16, pady=(0, 10))
        self.txt_plan.insert("1.0", f"✨ Diagnóstico instantáneo cargado:\n\n{consejo_base}\n\n[Conectando con Phi-3 para optimizar tu plan...]")

        barra_acciones = ctk.CTkFrame(cuerpo, fg_color="transparent")
        barra_acciones.pack(fill="x", pady=(8, 0))

        btn_nuevo = ctk.CTkButton(
            barra_acciones,
            text="↺ Nuevo Diagnóstico",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#ec4899",
            hover_color="#db2777",
            corner_radius=20,
            command=self._reiniciar,
        )
        btn_nuevo.pack(side="left", padx=4)

        btn_aprender = ctk.CTkButton(
            barra_acciones,
            text="🌸 Enseñar Nuevo Arquetipo",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#fce7f3",
            hover_color="#fbcfe8",
            text_color="#831843",
            corner_radius=20,
            command=self._abrir_modal_aprendizaje,
        )
        btn_aprender.pack(side="left", padx=10)

        hilo = threading.Thread(
            target=self._generar_plan_asincrono,
            args=(self.nodo_actual.texto, self.historial, soluciones),
            daemon=True,
        )
        hilo.start()

    def _generar_plan_asincrono(self, perfil: str, respuestas: list[str], soluciones: list[str]):
        """Consulta a Ollama en segundo plano y actualiza el texto en la interfaz."""
        plan = self.ia.generar_plan_financiero(
            perfil=perfil,
            respuestas=respuestas,
            soluciones=soluciones,
        )

        def _actualizar_ui():
            if plan:
                self.txt_plan.delete("1.0", "end")
                self.txt_plan.insert("1.0", plan.strip())
                self.lbl_estado_ia.configure(text="✔ Plan Phi-3 Listo ✨", text_color="#059669")
            else:
                self.lbl_estado_ia.configure(text="🌸 Modo Respaldo Activo", text_color="#be185d")

        self.after(0, _actualizar_ui)

    def _incrustar_grafico(self, frame_padre):
        """Genera un gráfico cute rosadito en Matplotlib incrustado en el canvas."""
        fig = Figure(figsize=(3.4, 2.2), dpi=95, facecolor="#ffffff")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#ffffff")

        categorias = ["Ingresos", "Gastos"]
        valores = [self.ingreso_val, self.gasto_val]
        colores = ["#f472b6", "#fda4af"]

        barras = ax.bar(categorias, valores, color=colores, width=0.42, edgecolor="#fbcfe8", linewidth=1.5)
        ax.tick_params(colors="#831843", labelsize=9)

        for spine in ax.spines.values():
            spine.set_color("#fbcfe8")
            spine.set_linewidth(1.2)

        max_val = max(valores) if max(valores) > 0 else 1.0
        ax.set_ylim(0, max_val * 1.25)

        for barra in barras:
            h = barra.get_height()
            ax.text(
                barra.get_x() + barra.get_width() / 2.0,
                h + (max_val * 0.03),
                f"${h:,.0f}",
                ha="center",
                va="bottom",
                color="#831843",
                fontsize=8,
                fontweight="bold",
            )

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame_padre)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=6, pady=(0, 4))

    def _abrir_modal_aprendizaje(self):
        """Modal con estilo cute para enseñar una nueva distinción al árbol."""
        modal = ctk.CTkToplevel(self)
        modal.title("🌸 Enseñar Nuevo Arquetipo")
        modal.geometry("520x360")
        modal.resizable(False, False)
        modal.configure(fg_color="#fff1f5")
        modal.grab_set()

        lbl_t = ctk.CTkLabel(
            modal,
            text=f"🎀 Diferenciar de '{self.nodo_actual.texto}'",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#831843",
        )
        lbl_t.pack(pady=(20, 8))

        lbl_nom = ctk.CTkLabel(modal, text="Nombre del nuevo arquetipo:", text_color="#701a75")
        lbl_nom.pack(anchor="w", padx=32, pady=(6, 2))
        entry_nom = ctk.CTkEntry(modal, width=450, border_color="#f472b6", fg_color="#ffffff", text_color="#831843")
        entry_nom.pack(padx=32, pady=(0, 10))

        lbl_preg = ctk.CTkLabel(
            modal,
            text=f"Pregunta Sí/No (Sí = nuevo, No = {self.nodo_actual.texto}):",
            wraplength=450,
            justify="left",
            text_color="#701a75",
        )
        lbl_preg.pack(anchor="w", padx=32, pady=(6, 2))
        entry_preg = ctk.CTkEntry(modal, width=450, border_color="#f472b6", fg_color="#ffffff", text_color="#831843")
        entry_preg.pack(padx=32, pady=(0, 16))

        def _guardar_nuevo():
            nom = entry_nom.get().strip()
            preg = entry_preg.get().strip()
            if not nom or not preg:
                return

            nid = nom.lower().replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
            nperfil = Perfil(id_perfil=nid, nombre=nom)
            self.arbol.aprender(self.ruta, preg, nperfil)
            modal.destroy()
            self._reiniciar()

        btn_guardar = ctk.CTkButton(
            modal,
            text="🎀 Guardar en el Árbol",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#ec4899",
            hover_color="#db2777",
            corner_radius=20,
            command=_guardar_nuevo,
        )
        btn_guardar.pack(pady=10)

    def _reiniciar(self):
        """Reinicia el cuestionario a la raíz del árbol."""
        self.nodo_actual = self.arbol.raiz
        self.ruta = []
        self.historial = []
        self.nivel = 1
        self._mostrar_pantalla_diagnostico()

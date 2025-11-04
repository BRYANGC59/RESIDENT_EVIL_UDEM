import tkinter as tk
from tkinter import messagebox, Toplevel
from model import Tablero
import random


class SimuladorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🧬 Resident Evil UDEM - Simulación de infección")
        self.root.geometry("600x400")
        self.root.configure(bg="#111")

        # Pantalla de inicio
        self.titulo = tk.Label(
            self.root,
            text="🧬 Resident Evil UDEM",
            fg="#00ffcc",
            bg="#111",
            font=("Arial Black", 24)
        )
        self.titulo.pack(pady=60)

        self.subtitulo = tk.Label(
            self.root,
            text="Simulación de propagación de infección\nUniversidad de Medellín",
            fg="white",
            bg="#111",
            font=("Arial", 12)
        )
        self.subtitulo.pack(pady=20)

        self.boton_inicio = tk.Button(
            self.root,
            text="🚀 Comenzar Simulación",
            font=("Arial", 14, "bold"),
            bg="#00ffcc",
            fg="#111",
            padx=20, pady=10,
            relief="flat",
            command=self.mostrar_configuracion
        )
        self.boton_inicio.pack(pady=40)

    # ================== PANTALLA DE CONFIGURACIÓN ==================
    def mostrar_configuracion(self):
        # Cerrar pantalla de inicio
        self.titulo.pack_forget()
        self.subtitulo.pack_forget()
        self.boton_inicio.pack_forget()

        self.config_window = Toplevel(self.root)
        self.config_window.title("Configuración inicial")
        self.config_window.geometry("400x300")
        self.config_window.configure(bg="#1a1a1a")

        tk.Label(
            self.config_window, text="Configuración de la simulación",
            fg="#00ffcc", bg="#1a1a1a", font=("Arial Black", 16)
        ).pack(pady=20)

        # Entradas
        tk.Label(self.config_window, text="Tamaño del tablero (N):", fg="white", bg="#1a1a1a").pack()
        self.entry_tamano = tk.Entry(self.config_window, justify="center")
        self.entry_tamano.pack(pady=5)

        tk.Label(self.config_window, text="Cantidad de jugadores:", fg="white", bg="#1a1a1a").pack()
        self.entry_cantidad = tk.Entry(self.config_window, justify="center")
        self.entry_cantidad.pack(pady=5)

        tk.Button(
            self.config_window,
            text="✅ Iniciar Simulación",
            command=self.iniciar_simulacion,
            bg="#00ffcc",
            fg="#111",
            font=("Arial", 12, "bold")
        ).pack(pady=20)

    # ================== CREAR EL TABLERO ==================
    def iniciar_simulacion(self):
        try:
            tamano = int(self.entry_tamano.get())
            cantidad = int(self.entry_cantidad.get())
            if tamano < 3 or tamano > 15:
                raise ValueError
            if cantidad < 2 or cantidad > tamano * tamano:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos.")
            return

        self.config_window.destroy()

        # Crear tablero
        self.root.configure(bg="white")
        random.seed()
        self.tablero = Tablero(tamano=tamano, cantidad=cantidad)

        # Interfaz principal
        self.crear_interfaz_principal()

    # ================== INTERFAZ PRINCIPAL ==================
    def crear_interfaz_principal(self):
        self.canvas = tk.Canvas(self.root, width=360, height=360, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.info_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.info_label.grid(row=1, column=0, pady=5)

        self.panel_botones = tk.Frame(self.root, bg="white")
        self.panel_botones.grid(row=0, column=1, padx=10)

        botones = [
            ("▶ Siguiente ronda", self.siguiente_ronda),
            ("💉 Curar persona", self.curar_persona),
            ("➕ Agregar persona", self.agregar_persona),
            ("🌳 Ver árbol de infección", self.mostrar_arbol),
            ("🛑 Salir", self.root.quit),
        ]

        for texto, comando in botones:
            b = tk.Button(self.panel_botones, text=texto, command=comando, width=22, bg="#222", fg="white")
            b.pack(pady=5)

        self.actualizar_tablero()

    # ================== LÓGICA DEL TABLERO ==================
    def actualizar_tablero(self):
        self.canvas.delete("all")
        celdas = self.tablero.tamano
        tam = 360 // celdas

        for i in range(celdas):
            for j in range(celdas):
                x1, y1 = j * tam, i * tam
                x2, y2 = x1 + tam, y1 + tam
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray")

        for persona in self.tablero.personas:
            x, y = persona.y, persona.x
            x1, y1 = x * tam + 5, y * tam + 5
            x2, y2 = x1 + tam - 10, y1 + tam - 10
            color = "red" if persona.infectada else "green"
            self.canvas.create_oval(x1, y1, x2, y2, fill=color)
            self.canvas.create_text(x1 + (tam / 2) - 5, y1 + (tam / 2) - 5, text=persona.id, fill="white")

        sanos = sum(not p.infectada for p in self.tablero.personas)
        infectados = sum(p.infectada for p in self.tablero.personas)
        self.info_label.config(text=f"Ronda: {self.tablero.ronda} | 🟩 Sanos: {sanos} | 🟥 Infectados: {infectados}")

    # ================== BOTONES ==================
    def siguiente_ronda(self):
        self.tablero.ronda_manual()
        self.actualizar_tablero()
        if all(p.infectada for p in self.tablero.personas):
            messagebox.showinfo("Fin de simulación", "Todas las personas están infectadas 🧟‍♂")
            self.root.quit()

    def curar_persona(self):
        from tkinter import simpledialog
        persona_id = simpledialog.askstring("Curar", "Ingrese el ID de la persona (p1, p2, ...):")
        if persona_id:
            self.tablero.curar(persona_id)
            self.actualizar_tablero()

    def agregar_persona(self):
        from tkinter import simpledialog
        x = simpledialog.askinteger("Agregar persona", "Coordenada X:")
        y = simpledialog.askinteger("Agregar persona", "Coordenada Y:")
        if x is not None and y is not None:
            nuevo_id = f"p{len(self.tablero.personas) + 1}"
            self.tablero.agregar_persona(nuevo_id, x, y)
            self.actualizar_tablero()

    # ================== ÁRBOL ==================
    def mostrar_arbol(self):
        for window in self.root.winfo_children():
            if isinstance(window, Toplevel) and window.title() == "🌳 Árbol de infección":
                window.destroy()

        ventana_arbol = Toplevel(self.root)
        ventana_arbol.title("🌳 Árbol de infección")
        canvas_arbol = tk.Canvas(ventana_arbol, width=800, height=500, bg="white")
        canvas_arbol.pack(padx=10, pady=10)

        relaciones = self.tablero.arbol.relaciones
        if not relaciones or all(len(hijos) == 0 for hijos in relaciones.values()):
            tk.Label(ventana_arbol, text="No hay contagios registrados aún").pack()
            return

        niveles, nodos_pos = self._calcular_niveles(relaciones)
        self._dibujar_arbol(canvas_arbol, niveles, relaciones, nodos_pos)

    def _calcular_niveles(self, relaciones):
        niveles = {}
        visitados = set()
        hijos = {h for hijos in relaciones.values() for h in hijos}
        raices = [r for r in relaciones.keys() if r not in hijos]
        if not raices:
            raices = list(relaciones.keys())

        def dfs(nodo, nivel):
            if nodo not in niveles:
                niveles.setdefault(nivel, []).append(nodo)
            visitados.add(nodo)
            for hijo in relaciones.get(nodo, []):
                if hijo not in visitados:
                    dfs(hijo, nivel + 1)

        for raiz in raices:
            dfs(raiz, 0)

        nodos_pos = {}
        for nivel, nodos in niveles.items():
            x_espaciado = 800 // (len(nodos) + 1)
            for i, nodo in enumerate(nodos):
                nodos_pos[nodo] = ((i + 1) * x_espaciado, 80 + nivel * 100)
        return niveles, nodos_pos

    def _dibujar_arbol(self, canvas, niveles, relaciones, nodos_pos):
        canvas.delete("all")
        for infectador, hijos in relaciones.items():
            if infectador in nodos_pos:
                x1, y1 = nodos_pos[infectador]
                for hijo in hijos:
                    if hijo in nodos_pos:
                        x2, y2 = nodos_pos[hijo]
                        canvas.create_line(x1, y1 + 20, x2, y2 - 20, arrow=tk.LAST)

        for nodo, (x, y) in nodos_pos.items():
            persona = next((p for p in self.tablero.personas if p.id == nodo), None)
            color = "red" if persona and persona.infectada else "green"
            canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline="black")
            canvas.create_text(x, y, text=nodo, fill="white", font=("Arial", 10, "bold"))


# ================== EJECUCIÓN ==================
if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel
from model import Tablero
import random


class SimuladorApp:
    def _init_(self, root: tk.Tk):
        self.root = root
        self.root.title("🧬 Resident Evil UDEM - Simulación de infección")


        random.seed(1)
        self.tablero = Tablero(tamano=6, cantidad=6)

        self.canvas = tk.Canvas(root, width=360, height=360, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.info_label = tk.Label(root, text="", font=("Arial", 10))
        self.info_label.grid(row=1, column=0, pady=5)

        self.panel_botones = tk.Frame(root)
        self.panel_botones.grid(row=0, column=1, padx=10)

        botones = [
            ("▶ Siguiente ronda", self.siguiente_ronda),
            ("💉 Curar persona", self.curar_persona),
            ("➕ Agregar persona", self.agregar_persona),
            ("🌳 Ver árbol de infección", self.mostrar_arbol),
            ("🛑 Salir", root.quit),
        ]

        for texto, comando in botones:
            b = tk.Button(self.panel_botones, text=texto, command=comando, width=22)
            b.pack(pady=5)

        self.actualizar_tablero()


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
        self.info_label.config(
            text=f"Ronda: {self.tablero.ronda} | 🟩 Sanos: {sanos} | 🟥 Infectados: {infectados}"
        )

 

    def siguiente_ronda(self):
        self.tablero.ronda_manual()
        self.actualizar_tablero()


        if all(p.infectada for p in self.tablero.personas):
            messagebox.showinfo("Fin de simulación", "Todas las personas están infectadas 🧟‍♂")
            self.root.quit()

    def curar_persona(self):
        persona_id = simpledialog.askstring("Curar", "Ingrese el ID de la persona (p1, p2, ...):")
        if persona_id:
            self.tablero.curar(persona_id)
            self.actualizar_tablero()

    def agregar_persona(self):
        x = simpledialog.askinteger("Agregar persona", "Coordenada X:")
        y = simpledialog.askinteger("Agregar persona", "Coordenada Y:")
        if x is not None and y is not None:
            nuevo_id = f"p{len(self.tablero.personas) + 1}"
            self.tablero.agregar_persona(nuevo_id, x, y)
            self.actualizar_tablero()

    def mostrar_arbol(self):
        ventana_arbol = Toplevel(self.root)
        ventana_arbol.title("🌳 Árbol de infección")
        canvas_arbol = tk.Canvas(ventana_arbol, width=600, height=400, bg="white")
        canvas_arbol.pack(padx=10, pady=10)

        relaciones = self.tablero.arbol.relaciones

        if not relaciones:
            tk.Label(ventana_arbol, text="No hay contagios registrados").pack()
            return

        niveles = self._calcular_niveles(relaciones)
        self._dibujar_arbol(canvas_arbol, niveles, relaciones)

   

    def _calcular_niveles(self, relaciones):
        niveles = {}
        visitados = set()

        hijos = {h for hijos in relaciones.values() for h in hijos}
        raiz = next(iter(set(relaciones.keys()) - hijos), None)

        def dfs(nodo, nivel):
            if nodo not in niveles:
                niveles[nivel] = []
            niveles[nivel].append(nodo)
            visitados.add(nodo)
            for hijo in relaciones.get(nodo, []):
                dfs(hijo, nivel + 1)

        if raiz:
            dfs(raiz, 0)
        return niveles

    def _dibujar_arbol(self, canvas, niveles, relaciones):
        nivel_y = 80
        nodos_pos = {}

        for nivel, nodos in niveles.items():
            x_espaciado = 600 // (len(nodos) + 1)
            for i, nodo in enumerate(nodos):
                x = (i + 1) * x_espaciado
                y = 50 + nivel * nivel_y
                canvas.create_oval(x - 20, y - 20, x + 20, y + 20,
                                   fill="red", outline="black" if nodo else "")
                canvas.create_text(x, y, text=nodo, fill="white", font=("Arial", 10, "bold"))
                nodos_pos[nodo] = (x, y)

        for infectador, hijos in relaciones.items():
            if infectador in nodos_pos:
                x1, y1 = nodos_pos[infectador]
                for hijo in hijos:
                    if hijo in nodos_pos:
                        x2, y2 = nodos_pos[hijo]
                        canvas.create_line(x1, y1 + 20, x2, y2 - 20, arrow=tk.LAST)


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorApp(root)
    root.mainloop()
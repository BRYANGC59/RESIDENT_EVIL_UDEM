import random

class Persona:
    def __init__(self, id: str, x: int, y: int, infectada=False):
        self.id = id
        self.x = x
        self.y = y
        self.infectada = infectada
        self.defensa = 3  

    def mover(self, limite):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.x = (self.x + dx) % limite
        self.y = (self.y + dy) % limite
        print(f"➡️ {self.id} se movió a ({self.x}, {self.y})")


class ArbolInfeccion:
    def __init__(self):
        self.relaciones = {}  

    def agregar_contagio(self, infectador, infectado):
        if infectador not in self.relaciones:
            self.relaciones[infectador] = []
        self.relaciones[infectador].append(infectado)
        print(f"🌳 {infectador} contagió a {infectado}")

    def establecer_raiz_si_vacia(self, root_id):
        """Si el árbol no tiene relaciones, establece un nodo raíz vacío."""
        if not self.relaciones:
            self.relaciones[root_id] = []
            print(f"🌱 {root_id} establecido como raíz del árbol de infección (único infectado).")

    def eliminar_nodo(self, nodo):
        if nodo in self.relaciones:
            self.relaciones.pop(nodo)
        for hijos in self.relaciones.values():
            if nodo in hijos:
                hijos.remove(nodo)


class Tablero:
    def __init__(self, tamano=6, cantidad=5):
        self.tamano = tamano
        self.personas = []
        self.arbol = ArbolInfeccion()
        self.ronda = 0
        self.poder_infectados = 1
        self.infectado_furioso = None  

        for i in range(cantidad):
            x, y = random.randint(0, tamano - 1), random.randint(0, tamano - 1)
            infectada = (i == 0)
            persona = Persona(f"p{i + 1}", x, y, infectada)
            self.personas.append(persona)
            print(f"🧍 {persona.id} creada en ({x}, {y}) - {'INFECTADA' if infectada else 'sana'}")

        # 🔹 Si solo hay un infectado, se convierte en raíz del árbol
        infectados = [p for p in self.personas if p.infectada]
        if len(infectados) == 1:
            self.arbol.establecer_raiz_si_vacia(infectados[0].id)

    def mostrar_estado(self):
        print("\n📋 ESTADO DEL TABLERO:")
        for p in self.personas:
            estado = "😷 INFECTADA" if p.infectada else "🟩 SANA"
            furia = "🔥 (FURIA)" if p.id == self.infectado_furioso else ""
            print(f"   {p.id}: pos=({p.x},{p.y}) def={p.defensa} {estado} {furia}")
        print("")

    def agregar_persona(self, id, x, y):
        self.personas.append(Persona(id, x, y, infectada=False))
        print(f"➕ Nueva persona {id} añadida en ({x}, {y})")

    def curar(self, id):
        persona = next((p for p in self.personas if p.id == id), None)
        if persona:
            persona.infectada = False
            persona.defensa = 3
            self.arbol.eliminar_nodo(persona.id)
            if persona.id == self.infectado_furioso:
                self.infectado_furioso = None
            print(f"🩺 {id} fue curado con éxito.")

    def mover_personas(self):
        print("\n🚶 Moviendo personas...")
        for p in self.personas:
            p.mover(self.tamano)

    def procesar_contagio(self):
        print("\n🧫 Procesando contagios...")
        nuevas_infecciones = []
        furia_usada = False 

        for x in range(self.tamano):
            for y in range(self.tamano):
                celda = [p for p in self.personas if p.x == x and p.y == y]
                if not celda:
                    continue

                infectados = [p for p in celda if p.infectada]
                sanos = [p for p in celda if not p.infectada]

                if not infectados or not sanos:
                    continue

                print(f"📍 Celda ({x}, {y}): {len(infectados)} infectados, {len(sanos)} sanos")

                for s in sanos:
                    if self.infectado_furioso and any(
                            p.id == self.infectado_furioso for p in infectados) and not furia_usada:
                        print(f"💥 {s.id} fue infectado por el furioso {self.infectado_furioso}")
                        nuevas_infecciones.append((self.infectado_furioso, s))
                        furia_usada = True 
                    else:
                        s.defensa -= len(infectados) * self.poder_infectados
                        print(f"🛡️ {s.id} pierde defensa, ahora tiene {s.defensa}")
                        if s.defensa <= 0:
                            infectador = random.choice(infectados)
                            nuevas_infecciones.append((infectador.id, s))

        for infectador_id, persona_obj in nuevas_infecciones:
            if not persona_obj.infectada:
                persona_obj.infectada = True
                persona_obj.defensa = 0
                self.arbol.agregar_contagio(infectador_id, persona_obj.id)
                print(f"😷 {persona_obj.id} fue infectado por {infectador_id}")

        if furia_usada:
            print(f"😴 {self.infectado_furioso} ha perdido el modo furia tras infectar a una persona.")
            self.infectado_furioso = None

    def ronda_manual(self):
        print(f"\n🔁 ---- RONDA {self.ronda + 1} ----")
        self.mover_personas()
        self.procesar_contagio()
        self.ronda += 1
        self.mostrar_estado()

    def lanzar_bomba_sanacion(self, x: int, y: int, radio: int = None):
        if radio is None:
            radio = max(1, self.tamano // 4)

        print(f"\n💚 Bomba de sanación activada en ({x}, {y}) con radio {radio}")

        for persona in self.personas:
            if abs(persona.x - x) <= radio and abs(persona.y - y) <= radio:
                # 🔹 Si hay solo un infectado, se cura totalmente
                infectados = [p for p in self.personas if p.infectada]
                if len(infectados) == 1 and persona.infectada:
                    persona.defensa = 5
                    persona.infectada = False
                    self.arbol.eliminar_nodo(persona.id)
                    print(f"💥 {persona.id} era el único infectado y fue curado totalmente por la bomba!")
                    self.infectado_furioso = None
                    continue

                persona.defensa = min(persona.defensa + 1, 5)
                if persona.infectada and persona.defensa >= 3:
                    persona.infectada = False
                    if hasattr(self, "arbol"):
                        self.arbol.eliminar_nodo(persona.id)
                    if persona.id == self.infectado_furioso:
                        self.infectado_furioso = None
                    print(f"🩺 {persona.id} fue curado por la bomba de sanación")
                else:
                    print(f"🧍 {persona.id} recibió curación parcial (defensa={persona.defensa})")

    def activar_modo_furia(self, persona_id: str) -> bool:
        persona = next((p for p in self.personas if p.id == persona_id), None)
        if persona and persona.infectada:
            self.infectado_furioso = persona_id
            print(f"😈 {persona_id} ha entrado en MODO FURIA!")
            return True
        else:
            print(f"❌ {persona_id} no está infectado o no existe.")
            return False
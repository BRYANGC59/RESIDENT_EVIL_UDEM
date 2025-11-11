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
    def __init__(self, tamano, cantidad):
        self.tamano = tamano
        self.personas = []
        self.arbol = ArbolInfeccion()
        self.ronda = 0
        self.infectado_furioso = None

        for i in range(cantidad):
            x, y = random.randint(0, tamano - 1), random.randint(0, tamano - 1)
            if i == 0:
                infectada = True
            else:
                infectada = False
            persona = Persona(f"p{i + 1}", x, y, infectada)
            self.personas.append(persona)
            print(f"🧍 {persona.id} creada en ({x}, {y}) - {'INFECTADA' if infectada else 'sana'}")

        infectados = [p for p in self.personas if p.infectada]
        if len(infectados) == 1:
            self.arbol.establecer_raiz_si_vacia(infectados[0].id)

    def mostrar_estado(self):
        print("\n📋 ESTADO DEL TABLERO:")
        for p in self.personas:
            if p.infectada:
                estado = "😷 INFECTADA"
            else:
                estado = "🟩 SANA"
            if p.id == self.infectado_furioso:
                furia = "🔥 (FURIA)"
            else:
                furia = ""
            print(f"   {p.id}: pos=({p.x},{p.y}) def={p.defensa} {estado} {furia}")
        print("")

    def agregar_persona(self, id, x, y):
        self.personas.append(Persona(id, x, y, infectada=False))
        print(f"➕ Nueva persona {id} añadida en ({x}, {y})")

    def curar(self, id):
        persona = None
        for p in self.personas:
            if p.id == id:
                persona = p
                break
        if persona:
            persona.infectada = False
            persona.defensa = 3
            self.arbol.eliminar_nodo(persona.id)
            if persona.id == self.infectado_furioso:
                self.infectado_furioso = None
            print(f"🩺 {id} fue curado con éxito.")


    def curar_k_nivel(self, k: int):
        def bfs(gt: ArbolInfeccion):
            if not gt:
                return 'The tree is empty'

            root = next(iter(gt.relaciones))
            pv = [(root, 1)]
            account = {}

            while pv:
                current = pv.pop(0)
                if current[1] not in account:
                    account[current[1]] = [current[0]]
                else:
                    account[current[1]].append(current[0])

                if gt.relaciones[current[0]]:
                    for i in gt.relaciones[current[0]]:
                        pv.append((i, current[1] + 1))
            return account
        niveles = bfs(self.arbol)
        if not k in niveles:
            raise ValueError('El nivel ingresado no es valido')
        eliminar = niveles[k]
        while eliminar:
            self.curar(eliminar.pop())
        print(f'Se han curado todos los infectados del nivel {k}')

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
                celda = []
                for p in self.personas:
                    if p.x == x and p.y == y:
                        celda.append(p)
                if not celda:
                    continue

                infectados = [p for p in celda if p.infectada]
                sanos = [p for p in celda if not p.infectada]

                if not infectados or not sanos:
                    continue

                for s in sanos:
                    if self.infectado_furioso:
                        furioso_presente = any(p.id == self.infectado_furioso for p in infectados)

                        if furioso_presente and not furia_usada:
                            print(f"💥 {s.id} fue infectado por el furioso {self.infectado_furioso}")
                            nuevas_infecciones.append((self.infectado_furioso, s))
                            furia_usada = True
                            continue

                        if furioso_presente:
                            print(f"💥 {s.id} fue infectado por {infectados[0]}")
                            nuevas_infecciones.append((infectados[0], s))
                            furia_usada = True
                    else:
                        s.defensa -= 1
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

    def lanzar_bomba_sanacion(self):
        # Genera coordenadas aleatorias dentro del tablero
        x = random.randint(0, self.tamano - 1)
        y = random.randint(0, self.tamano - 1)
        print(f"\n💚 Bomba de sanación lanzada en ({x}, {y})")

        posiciones_afectadas = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nueva_x = x + dx
                nueva_y = y + dy

                if 0 <= nueva_x < self.tamano and 0 <= nueva_y < self.tamano:
                    posiciones_afectadas.append((nueva_x, nueva_y))

        for persona in self.personas:
            if (persona.x, persona.y) in posiciones_afectadas:
                persona.defensa = min(persona.defensa + 1, 5)
                if persona.infectada and persona.defensa >= 3:
                    persona.infectada = False
                    self.arbol.eliminar_nodo(persona.id)
                    print(f"🩺 {persona.id} fue curado por la bomba")
                else:
                    print(f"🧍 {persona.id} recibió curación parcial (defensa={persona.defensa})")

        if self.infectado_furioso and not any(p.id == self.infectado_furioso and p.infectada for p in self.personas):
            print("😴 El infectado furioso ha sido curado y perdió su furia.")
            self.infectado_furioso = None
        if self.infectado_furioso and not any(p.id == self.infectado_furioso and p.infectada for p in self.personas):
            self.infectado_furioso = None
            print("😴 El infectado furioso ha sido curado y perdió su furia.")
        return x, y

    def activar_modo_furia(self, persona_id):
        persona_encontrada = None

        for p in self.personas:
            if p.id == persona_id:
                persona_encontrada = p
                break

        if persona_encontrada and persona_encontrada.infectada:
            self.infectado_furioso = persona_id
            return True

        return False
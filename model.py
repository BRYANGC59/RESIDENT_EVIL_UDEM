import random
from typing import List, Optional, Dict


class Persona:
    def __init__(self, id_persona: str, x: int, y: int):
        self.id = id_persona
        self.x = x
        self.y = y
        self.infectada = False
        self.defensa = 3

    def __repr__(self):
        estado = "🟥" if self.infectada else "🟩"
        return f"{self.id}({estado}, D={self.defensa})"


class ArbolInfeccion:
    def __init__(self):
        self.relaciones: Dict[str, List[str]] = {}
        self.infectadores: Dict[str, Optional[str]] = {}

    def agregar_contagio(self, infectador: str, infectado: str) -> None:
        if infectador not in self.relaciones:
            self.relaciones[infectador] = []
        self.relaciones[infectador].append(infectado)
        self.infectadores[infectado] = infectador

    def eliminar_nodo(self, persona_id: str) -> None:
        if persona_id in self.infectadores:
            padre = self.infectadores[persona_id]
            hijos = self.relaciones.get(persona_id, [])
            # reparenting: conectar hijos con el infectador original
            if padre:
                self.relaciones[padre].extend(hijos)
            for h in hijos:
                self.infectadores[h] = padre
            self.relaciones.pop(persona_id, None)
            self.infectadores.pop(persona_id, None)

    def mostrar(self) -> None:
        print("🌳 Árbol de infección:")
        for infectador, hijos in self.relaciones.items():
            print(f"  {infectador} → {', '.join(hijos)}")
        print()


class Tablero:
    def __init__(self, tamano: int, cantidad: int):
        self.tamano = tamano
        self.personas: List[Persona] = []
        self.arbol = ArbolInfeccion()
        self.ronda = 0

        posiciones = set()
        for i in range(cantidad):
            while True:
                x = random.randint(0, tamano - 1)
                y = random.randint(0, tamano - 1)
                if (x, y) not in posiciones:
                    posiciones.add((x, y))
                    break
            persona = Persona(f"p{i + 1}", x, y)
            self.personas.append(persona)

        # Paciente cero
        paciente_cero = random.choice(self.personas)
        paciente_cero.infectada = True
        self.arbol.relaciones[paciente_cero.id] = []
        print(f"🧬 Paciente cero: {paciente_cero.id}\n")

    def obtener_celda(self, x: int, y: int) -> List[Persona]:
        return [p for p in self.personas if p.x == x and p.y == y]

    def mover(self) -> None:
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for persona in self.personas:
            dx, dy = random.choice(movimientos)
            nx, ny = persona.x + dx, persona.y + dy
            # modo rebote
            if nx < 0 or nx >= self.tamano:
                nx = persona.x
            if ny < 0 or ny >= self.tamano:
                ny = persona.y
            persona.x, persona.y = nx, ny
            
    def procesar_contagio(self) -> None:
        """
        Procesa contagios *solo* entre personas que comparten exactamente la misma celda.
        Se calcula todo en una pasada y se aplica al final para evitar contagios encadenados en la misma ronda.
        """
        # lista de (infectador_id, objeto_persona_infectado) a aplicar después
        nuevas_infecciones: List[(str, "Persona")] = []

        # recorrer cada celda del tablero
        for x in range(self.tamano):
            for y in range(self.tamano):
                celda = [p for p in self.personas if p.x == x and p.y == y]
                if not celda:
                    continue

                infectados = [p for p in celda if p.infectada]
                sanos = [p for p in celda if not p.infectada]

                if not infectados or not sanos:
                    continue

                # Cada sano pierde 1 defensa por cada infectado en la misma celda
                for s in sanos:
                    s.defensa -= len(infectados)
                    # debug opcional: imprimir lo ocurrido
                    # print(f"DEBUG: {s.id} perdió {len(infectados)} defensa en ({x},{y}), queda {s.defensa}")
                    if s.defensa <= 0:
                        # marcar para infectar al final; elegimos un infectador al azar entre los infectados actuales
                        infectador = random.choice(infectados)
                        nuevas_infecciones.append((infectador.id, s))

        # aplicar las infecciones ya decididas (una sola vez por persona)
        for infectador_id, persona_obj in nuevas_infecciones:
            if not persona_obj.infectada:  # doble chequeo para evitar re-infectar
                persona_obj.infectada = True
                persona_obj.defensa = 0
                self.arbol.agregar_contagio(infectador_id, persona_obj.id)
                # debug opcional:
                # print(f"DEBUG: {persona_obj.id} fue infectado por {infectador_id}")

    def aumentar_defensa(self) -> None:
        for p in self.personas:
            if not p.infectada:
                p.defensa += 1

    def curar(self, persona_id: str) -> None:
        for p in self.personas:
            if p.id == persona_id and p.infectada:
                p.infectada = False
                p.defensa = 3
                self.arbol.eliminar_nodo(p.id)
                print(f"💉 {persona_id} ha sido curado.")
                return
        print(f"No se encontró persona infectada con ID {persona_id}.")

    def agregar_persona(self, id_persona: str, x: int, y: int) -> None:
        if not (0 <= x < self.tamano and 0 <= y < self.tamano):
            print("⚠ Coordenadas fuera del tablero.")
            return
        nueva = Persona(id_persona, x, y)
        self.personas.append(nueva)
        print(f"🧍‍♂ {id_persona} agregada en ({x},{y})")

    def mostrar_tablero(self) -> None:
        matriz = [["⚪" for _ in range(self.tamano)] for _ in range(self.tamano)]
        for p in self.personas:
            matriz[p.x][p.y] = "🟥" if p.infectada else "🟩"
        print("🧫 Estado del tablero:")
        for fila in matriz:
            print(" ".join(fila))
        print()

    def mostrar_personas(self) -> None:
        print("👥 Estado de las personas:")
        for p in self.personas:
            estado = "INFECTADO" if p.infectada else "SANO"
            print(f"  {p.id} → {estado}, Defensa={p.defensa}, Pos=({p.x},{p.y})")
        print()

    def ronda_manual(self) -> None:
        self.ronda += 1
        print(f"\n===== RONDA {self.ronda} =====")
        self.mover()
        self.procesar_contagio()
        if self.ronda % 3 == 0:
            self.aumentar_defensa()
        self.mostrar_tablero()
        self.mostrar_personas()
        self.arbol.mostrar()
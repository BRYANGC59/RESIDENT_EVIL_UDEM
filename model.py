import random
from typing import Dict, List, Optional


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

            if padre:
                self.relaciones[padre].extend(hijos)
            self.relaciones.pop(persona_id, None)
            self.infectadores.pop(persona_id, None)

    def mostrar(self) -> None:
        print("🌳 Árbol de infección:")
        for infectador, hijos in self.relaciones.items():
            print(f"  {infectador} → {', '.join(hijos)}")
        print()

class Tablero:
    def __init__(self, medida_tablero: int):
        self.tablero = [[0 for _ in range(medida_tablero)] for _ in range(medida_tablero)]
        self.inicializado = False

    def agregar_personaje(self, personaje):
        x, y = personaje.x, personaje.y

        if not (0 <= x < len(self.tablero) and 0 <= y < len(self.tablero)):
            raise ValueError(f"Coordenadas fuera del tablero: ({x}, {y})")

        if not self.inicializado:
            if self.tablero[x][y] != 0:
                raise ValueError(f"La posición ({x}, {y}) ya está ocupada en la inicialización.")
            self.tablero[x][y] = personaje

        else:
            actual = self.tablero[x][y]
            if actual == 0:
                self.tablero[x][y] = personaje
            elif isinstance(actual, list):
                actual.append(personaje)
            else:
                self.tablero[x][y] = [actual, personaje]

    def mover_personaje(self, personaje):
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        x, y = personaje.x, personaje.y
        posibles_movimientos = []

        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.tablero) and 0 <= ny < len(self.tablero):
                posibles_movimientos.append((nx, ny))

        if not posibles_movimientos:
            return False

        nx, ny = random.choice(posibles_movimientos)
        actual = self.tablero[x][y]
        if isinstance(actual, list):
            actual.remove(personaje)
            if len(actual) == 1:
                self.tablero[x][y] = actual[0]
            elif len(actual) == 0:
                self.tablero[x][y] = 0
        else:
            self.tablero[x][y] = 0

        personaje.x, personaje.y = nx, ny

        nuevo = self.tablero[nx][ny]
        if nuevo == 0:
            self.tablero[nx][ny] = personaje
        elif isinstance(nuevo, list):
            nuevo.append(personaje)
        else:
            self.tablero[nx][ny] = [nuevo, personaje]

        return True

    def mostrar_tablero(self):
        for fila in self.tablero:
            fila_str = []
            for celda in fila:
                if celda == 0:
                    fila_str.append(".")
                elif isinstance(celda, list):
                    # Mostrar 'S' o 'I' si solo hay un tipo, o el número si hay mezcla
                    tipos = set(type(p) for p in celda)
                    if len(tipos) == 1:
                        tipo = tipos.pop()
                        if tipo == Sanos:
                            fila_str.append("S")
                        elif tipo == Infectado:
                            fila_str.append("I")
                        else:
                            fila_str.append("?")
                    else:
                        # Mezcla de tipos en la celda, mostrar número de personajes
                        fila_str.append(str(len(celda)))
                else:
                    if isinstance(celda, Sanos):
                        fila_str.append("S")
                    elif isinstance(celda, Infectado):
                        fila_str.append("I")
                    else:
                        fila_str.append("?")
            print(" ".join(fila_str))
        print()

    def marcar_inicializado(self):
        self.inicializado = True


class Sanos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nd = 3

    def curar(self, x, y):
        pass

class Infectado:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def infectar(self, x, y):
        pass



t = Tablero(5)
s1 = Sanos(1, 2)
i1 = Infectado(3, 4)
s2 = Sanos(1,3)
t.agregar_personaje(s1)
t.agregar_personaje(i1)
t.marcar_inicializado()
t.agregar_personaje(s2)

t.mostrar_tablero()
t.mover_personaje(s1)
t.mostrar_tablero()
t.mover_personaje(s1)
t.mostrar_tablero()


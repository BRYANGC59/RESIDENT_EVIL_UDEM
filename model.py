class Tablero:
    def __init__(self, medida_tablero: int):
        self.tablero = [[0 for _ in range(medida_tablero)] for _ in range(medida_tablero)]

    def agregar_personaje(self, x, y):
        self.tablero[x][y] = x,y
        if not 0 <= x < len(self.tablero) and 0 <= y < len(self.tablero):
            raise ValueError(f"Coordenadas fuera del tablero: ({x}, {y})")

        if not self.inicializado:
            if self.tablero[x][y] != 0:
                raise ValueError(f"La posición ({x}, {y}) ya está ocupada en la inicialización.")
            self.tablero[x][y] = x,y

    def marcar_inicializado(self):
        self.inicializado = True
        
class Sanos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nd = 3

    def mover(self, x, y):
        pass

    def curar(self, x, y):
        pass

class Infectado:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mover(self, x, y):
        pass

    def infectar(self, x, y):
        pass




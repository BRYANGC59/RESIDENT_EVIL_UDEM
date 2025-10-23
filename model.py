class Tablero:
    def __init__(self, medida_tablero: int):
        self.tablero: list[list[int]] = [[0 for _ in range(medida_tablero)] for _ in range(medida_tablero)]


class Sanos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nd = 3

    def mover(self, x, y):
        pass

    def curar(self, x, y):





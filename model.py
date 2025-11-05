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


class ArbolInfeccion:
    def __init__(self):
        self.relaciones = {}  

    def agregar_contagio(self, infectador, infectado):
        if infectador not in self.relaciones:
            self.relaciones[infectador] = []
        self.relaciones[infectador].append(infectado)

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
            self.personas.append(Persona(f"p{i + 1}", x, y, infectada))

    def agregar_persona(self, id, x, y):
        self.personas.append(Persona(id, x, y, infectada=False))

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
        for p in self.personas:
            p.mover(self.tamano)

    def procesar_contagio(self):
        """
        Procesa contagios entre personas que comparten la misma celda.
        Si hay un infectado furioso, infecta automáticamente UNA VEZ y luego se desactiva el modo furia.
        """
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

                for s in sanos:
                    
                    if self.infectado_furioso and any(
                            p.id == self.infectado_furioso for p in infectados) and not furia_usada:
                        print(f"💥 {s.id} fue infectado por el furioso {self.infectado_furioso}")
                        nuevas_infecciones.append((self.infectado_furioso, s))
                        furia_usada = True 
                    else:
                        
                        s.defensa -= len(infectados) * self.poder_infectados
                        if s.defensa <= 0:
                            infectador = random.choice(infectados)
                            nuevas_infecciones.append((infectador.id, s))

        
        for infectador_id, persona_obj in nuevas_infecciones:
            if not persona_obj.infectada:
                persona_obj.infectada = True
                persona_obj.defensa = 0
                self.arbol.agregar_contagio(infectador_id, persona_obj.id)

        
        if furia_usada:
            print(f"😴 {self.infectado_furioso} ha perdido el modo furia tras infectar a una persona.")
            self.infectado_furioso = None

    def ronda_manual(self):
        self.mover_personas()
        self.procesar_contagio()
        self.ronda += 1

    def lanzar_bomba_sanacion(self, x: int, y: int, radio: int = None):
        """
        Crea una zona de sanación centrada en (x, y) con radio = tamaño_tablero / 4.
        """
        if radio is None:
            radio = max(1, self.tamano // 4)

        print(f"💚 Bomba de sanación activada en ({x}, {y}) con radio {radio}")

        for persona in self.personas:
            if abs(persona.x - x) <= radio and abs(persona.y - y) <= radio:
                persona.defensa = min(persona.defensa + 1, 5)
                if persona.infectada and persona.defensa >= 3:
                    persona.infectada = False
                    if hasattr(self, "arbol"):
                        self.arbol.eliminar_nodo(persona.id)
                    if persona.id == self.infectado_furioso:
                        self.infectado_furioso = None
                    print(f"🩺 {persona.id} fue curado por la bomba de sanación")

    def activar_modo_furia(self, persona_id: str) -> bool:
        """
        Activa el modo furia para un infectado.
        """
        persona = next((p for p in self.personas if p.id == persona_id), None)
        if persona and persona.infectada:
            self.infectado_furioso = persona_id
            print(f"😈 {persona_id} ha entrado en MODO FURIA!")
            return True
        else:
            print(f"❌ {persona_id} no está infectado o no existe.")
            return False
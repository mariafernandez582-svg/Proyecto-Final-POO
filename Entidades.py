from abc import ABC, abstractmethod
import random
from typing import List

class Item:
    def __init__(self, n, e, t): self.nombre=n; self.efecto=e; self.tipo=t
    def __str__(self): return f"{self.nombre} (+{self.efecto} {self.tipo})"

class Inventario:
    def __init__(self): self.items: List[Item] = []
    def agregar_item(self, i): self.items.append(i)
    def usar_item(self, i): return self.items.pop(i) if 0<=i<len(self.items) else None

class Entidad(ABC):
    def __init__(self, nombre, vida, daño_base, defensa=0):
        self.__nombre=nombre; self.vida=vida; self.vida_maxima=vida
        self.daño_base=daño_base; self.defensa=defensa
    @property
    def nombre(self): return self.__nombre
    @nombre.setter
    def nombre(self, v): self.__nombre=v
    @abstractmethod
    def atacar(self, o): pass
    @abstractmethod
    def recibir_daño(self, d): pass
    def esta_vivo(self): return self.vida>0

class Jugador(Entidad):
    def __init__(self, nombre):
        super().__init__(nombre, 100, 0, 5)
        self.inventario=Inventario(); self.defendiendo=False; self.puntos=0
    def atacar(self, e):
        self.defendiendo=False
        d=random.randint(20,150)                # Daño base random
        if random.random()<0.10: return {"tipo":"fallo","dano":0,"msg":f"{self.nombre} falló el ataque!"}
        c=random.random()<0.22                  # Probabilidad de crítico
        if c: d=int(d*1.85)
        e.recibir_daño(d)
        return {"tipo":"critico" if c else "normal","dano":d,"msg":f"{'⚡ GOLPE CRÍTICO! ' if c else ''}Daño: {d}"}
    def defender(self):
        self.defendiendo=True
        return {"msg":f"{self.nombre} alza su escudo."}
    def recibir_daño(self, d):
        if self.defendiendo: d//=2
        r=max(0,d-self.defensa); self.vida=max(0,self.vida-r); return r
    def sanar(self, c):
        antes=self.vida; self.vida=min(self.vida+c,self.vida_maxima); return self.vida-antes

class Ataque:
    def __init__(self, n, d, p): self.nombre=n; self.dano_base=d; self.prob_critico=p
    def ejecutar(self, atk, obj):
        c=random.random()<self.prob_critico; d=self.dano_base*(2 if c else 1)
        r=obj.recibir_daño(d)
        return {"tipo":"critico" if c else "normal","dano":r,"msg":f"{atk.nombre} usa {self.nombre}{'  ¡CRÍTICO!' if c else ''}"}

class Enemigo(Entidad):
    NOMBRES=["Bastardo del Norte","Caminante Blanco","Guardia de la Noche","Salvaje del Norte",
             "Hombre sin Rostro","El Gran Sparrow","Lord Mano","Lobo Gigante"]
    ATAQUES=[("Furia de Valyria",18,.25),("Golpe del Invierno",22,.20),("Ataque Veloz",15,.35),
             ("Fuego valyrio",30,.30),("Zarpazo",19,.28),("Flecha Obsidiana",25,.18),
             ("Veneno de Basilisco",17,.25),("Grito de Muerte",20,.22)]
    def __init__(self, nb=None):
        nb=nb or random.choice(self.NOMBRES)
        super().__init__(nb,random.randint(65,135),random.randint(12,26),random.randint(2,9))
        self.ataques=[Ataque(n,d,p) for n,d,p in random.sample(self.ATAQUES,3)]
    def atacar(self, o): return random.choice(self.ataques).ejecutar(self,o)
    def recibir_daño(self, d):
        r=max(0,d-self.defensa); self.vida=max(0,self.vida-r); return r

class Dragon(Enemigo):
    def __init__(self):
        super().__init__("Drogon")
        self.nombre="Drogon, el Oscuro"
        self.vida=random.randint(170,220); self.vida_maxima=self.vida
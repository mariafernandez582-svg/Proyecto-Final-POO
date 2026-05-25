# ⚔ Game of Thrones — Torneos de Combate

Juego de combate por turnos ambientado en el universo de *Game of Thrones*, desarrollado en Python con interfaz gráfica en tkinter. El jugador debe enfrentarse a 7 enemigos (3 combates cada uno) para reclamar el Trono de Hierro.

---

## 🎮 Descripción del juego

El jugador elige un nombre para su guerrero y entra al torneo. Cada adversario tiene 3 rondas de combate. En cada turno el jugador puede:

- **Atacar** — golpe normal o crítico aleatorio
- **Defender** — reduce el daño del siguiente ataque enemigo a la mitad
- **Usar ítem** — pociones de curación del inventario
- **Huir** — intento de escapar con probabilidad del 45 %

Al derrotar todos los enemigos aparece la pantalla de victoria. Al morir, la pantalla de derrota. En ambos casos la puntuación queda guardada en el **Salón de la Fama**.

---

## 🗂 Estructura del proyecto

```
Taller Final - POO/
├── main.py                  ← Punto de entrada
├── app.py                   ← Interfaz gráfica (GotApp)
├── Entidades.py             ← Clases: Entidad, Jugador, Enemigo, Dragon, Item, Inventario, Ataque
├── Estilos.py               ← Paleta de colores, logotipos y función LOGO
├── datos_highscores.py      ← Carga, guardado y ranking de puntuaciones
├── highscores.json          ← Persistencia de puntuaciones (generado automáticamente)
├── requirements.txt         ← Dependencias del proyecto
└── README.md
```

---

## ⚙ Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/taller-final-poo.git
cd taller-final-poo
```

### 2. Crear y activar el entorno virtual

```bash
# Crear
python -m venv .venv

# Activar en Windows
.venv\Scripts\activate

# Activar en Mac/Linux
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> Este proyecto usa únicamente la biblioteca estándar de Python 3.
> `tkinter` viene incluido con Python — no requiere instalación adicional.

### 4. Ejecutar el juego

```bash
python main.py
```

---

## 🛠 Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3 | Lenguaje principal |
| tkinter | Interfaz gráfica (biblioteca estándar) |
| abc (ABC, abstractmethod) | Abstracción de clases base |
| json / os | Persistencia de highscores |
| random | Lógica de combate y generación de enemigos |

---

## 👤 Autora

**María Camila Fernández Patiño**  
Programación Orientada a Objetos — Proyecto Final

# ══════════════════════ PALETA GOT ══════════════════════
C = {
    "bg":        "#0c0b09",
    "panel":     "#111009",
    "card":      "#161410",
    "borde":     "#3a2e1a",
    "oro":       "#c9a84c",
    "oro2":      "#e8c96a",
    "rojo":      "#8b1a1a",
    "rojo2":     "#c0392b",
    "gris":      "#9a9080",
    "gris2":     "#d4cfc0",
    "texto":     "#e0d8c8",
    "dim":       "#6a6050",
    "hielo":     "#8ab4cc",
    "verde":     "#3a7a3a",
    "verde2":    "#5ab05a",
    "critico":   "#e67e22",
}

LOGOTIPOS = {
    "Bastardo del Norte": "⚔",  "Caminante Blanco": "❄",
    "Guardia de la Noche": "🌑", "Salvaje del Norte": "⚔",
    "Hombre sin Rostro": "🎭",   "El gran Sparrow": "✝",
    "Lord Mano": "🛡","Lobo Gigante": "🐺",
    "Drogon": "🐉",
}

def LOGO(nombre):
    for k,v in LOGOTIPOS.items():
        if k in nombre: return v
    return "⚔"
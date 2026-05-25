import json, os

# ══════════════════════ HIGHSCORES ══════════════════════
FILE = "highscores.json"
def cargar_hs():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return []
    return []
def guardar_hs(hs):
    try:
        with open(FILE, "w", encoding="utf-8") as f: json.dump(hs, f, ensure_ascii=False, indent=2)
    except: pass
def guardar_puntuacion(nombre, pts):
    global high_scores
    high_scores.append((nombre, pts))
    high_scores.sort(key=lambda x: x[1], reverse=True)
    high_scores = high_scores[:20]
    guardar_hs(high_scores)

high_scores = cargar_hs()
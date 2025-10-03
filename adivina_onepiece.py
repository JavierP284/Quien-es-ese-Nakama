import json
import os

# =========================
# CONFIGURACIÓN Y CONSTANTES
# =========================

DATA_FILE = "onepiece_chars.json"  # Archivo JSON con todos los personajes

ATTRS = [
    "es_miembro_mugiwara", "es_yonko", "tiene_fruta_del_diablo", "fruta_logia",
    "es_espadachin", "es_cocinero", "es_doctor", "es_cyborg", "es_esqueleto",
    "usa_pistola", "es_mujer", "tiene_sombrero", "es_revolucionario", "es_marine",
    "tiene_cicatriz", "usa_espada_grande", "es_navegante", "tiene_arma_especial",
    "es_almirante","es_shichibukai"
]

ATTR_TEXT = {
    "es_miembro_mugiwara": "¿Es miembro de los Sombrero de Paja?",
    "es_yonko": "¿Es un Yonkō?",
    "tiene_fruta_del_diablo": "¿Tiene una Fruta del Diablo?",
    "fruta_logia": "¿Su Fruta del Diablo es del tipo Logia?",
    "es_espadachin": "¿Es espadachín?",
    "es_cocinero": "¿Es cocinero?",
    "es_doctor": "¿Es doctor/doctor(a)?",
    "es_cyborg": "¿Es un cyborg?",
    "es_esqueleto": "¿Es un esqueleto?",
    "usa_pistola": "¿Usa pistola o arma de fuego?",
    "es_mujer": "¿Es mujer?",
    "tiene_sombrero": "¿Usa sombrero característico?",
    "es_revolucionario": "¿Es revolucionario?",
    "es_marine": "¿Pertenece a los Marines?",
    "tiene_cicatriz": "¿Tiene cicatrices visibles?",
    "usa_espada_grande": "¿Usa una espada grande?",
    "es_navegante": "¿Es navegante?",
    "tiene_arma_especial": "¿Tiene un arma especial?",
    "es_almirante": "¿Es un almirante?",
    "es_shichibukai": "¿Es un Shichibukai?",
}

# =========================
# UTILIDADES DE ARCHIVO
# =========================

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Error cargando el JSON:", e)
    else:
        print(f"No se encontró el archivo {DATA_FILE}. Asegúrate de tener tu JSON.")
    return []

def save_data(chars):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(chars, f, ensure_ascii=False, indent=2)

# =========================
# LÓGICA DE PREGUNTAS
# =========================

def info_gain(candidates, attr):
    n = len(candidates)
    if n == 0:
        return -1
    t = [c for c in candidates if c.get(attr)]
    f = [c for c in candidates if not c.get(attr)]
    gain = n - ((len(t) ** 2 + len(f) ** 2) / n)  # preferir divisiones balanceadas
    return gain

def best_question(candidates, asked):
    best = None
    best_gain = -1
    for a in ATTRS:
        if a in asked:
            continue
        g = info_gain(candidates, a)
        if g > best_gain:
            best_gain = g
            best = a
    return best

def respuesta_usuario(preg):
    while True:
        r = input(preg + " (s/n/nd para No sé): ").strip().lower()
        if r in ("s", "n", "nd"):
            return r
        print("Respuesta no válida. Escribe 's', 'n' o 'nd'.")

def filtrar(candidates, attr, resp):
    if resp == "s":
        return [c for c in candidates if c.get(attr)]
    elif resp == "n":
        return [c for c in candidates if not c.get(attr)]
    else:
        return candidates

# =========================
# JUEGO PRINCIPAL
# =========================

def jugar():
    chars = load_data()
    if not chars:
        print("No hay personajes cargados. Saliendo del juego.")
        return

    print("=== Juego: Adivina Quién (One Piece) ===")
    candidates = chars.copy()
    asked = set()

    while True:
        print(f"\nCandidatos restantes: {len(candidates)}")
        if len(candidates) == 1:
            print("Mi suposición es:", candidates[0]["nombre"])
            r = input("¿Adiviné? (s/n): ").strip().lower()
            if r == "s":
                print("¡Genial! He acertado.")
            else:
                print("Oh, fallé.")
            break

        q = best_question(candidates, asked)
        if not q:
            print("No tengo más preguntas útiles. Los candidatos posibles son:")
            for c in candidates:
                print(" -", c["nombre"])
            break

        asked.add(q)
        resp = respuesta_usuario(ATTR_TEXT[q])
        candidates = filtrar(candidates, q, resp)

    # Aprender nuevo personaje si falla
    r = input("¿Quieres enseñar al sistema un personaje nuevo? (s/n): ").strip().lower()
    if r == "s":
        nombre = input("Nombre del personaje: ").strip()
        new = {"nombre": nombre}
        for a in ATTRS:
            val = input(f"{ATTR_TEXT[a]} (s/n): ").strip().lower()
            new[a] = (val == "s")
        chars.append(new)
        save_data(chars)
        print(f"Personaje '{nombre}' guardado. Gracias por enseñar al sistema.")

# =========================
# EJECUCIÓN
# =========================

if __name__ == "__main__":
    jugar()

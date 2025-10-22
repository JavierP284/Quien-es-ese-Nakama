import json
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Para manejar la imagen del logo

# =========================
# CONFIGURACIÓN Y CONSTANTES
# =========================

DATA_FILE = os.path.join(os.path.dirname(__file__), "onepiece_chars.json")

ATTRS = [
    "es_miembro_mugiwara", "es_yonko", "tiene_fruta_del_diablo", "fruta_logia",
    "es_espadachin", "es_cocinero", "es_doctor", "es_cyborg", "es_esqueleto",
    "usa_pistola", "es_mujer", "tiene_sombrero", "es_revolucionario", "es_marine",
    "tiene_cicatriz", "usa_espada_grande", "es_navegante",
    "es_almirante","es_shichibukai",
    "tiene_tatuaje", "usa_arma_a_distancia"
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
    "tiene_tatuaje": "¿Tiene tatuajes visibles?",
    "usa_arma_a_distancia": "¿Usa un arma a distancia?"
}

# =========================
# FUNCIONES DE LÓGICA
# =========================

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando JSON: {e}")
    else:
        messagebox.showerror("Error", f"No se encontró {DATA_FILE}")
    return []

def save_data(chars):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(chars, f, ensure_ascii=False, indent=2)

def info_gain(candidates, attr):
    n = len(candidates)
    if n == 0:
        return -1
    t = [c for c in candidates if c.get(attr)]
    f = [c for c in candidates if not c.get(attr)]
    gain = n - ((len(t) ** 2 + len(f) ** 2) / n)
    return gain

def best_question(candidates, asked, respuestas_previas=None):
    if respuestas_previas is None:
        respuestas_previas = {}
    best = None
    best_gain = -1
    for a in ATTRS:
        if a in asked:
            continue

        # Solo preguntar por fruta_logia si tiene_fruta_del_diablo fue "s"
        if a == "fruta_logia" and respuestas_previas.get("tiene_fruta_del_diablo") != "s":
            continue

        # No preguntar si es revolucionario si es marine
        if a == "es_revolucionario" and respuestas_previas.get("es_marine") == "s":
            continue

        g = info_gain(candidates, a)
        if g > best_gain:
            best_gain = g
            best = a
    return best

def filtrar(candidates, attr, resp):
    if resp == "s":
        return [c for c in candidates if c.get(attr)]
    elif resp == "n":
        return [c for c in candidates if not c.get(attr)]
    else:
        return candidates

# =========================
# INTERFAZ GRÁFICA
# =========================

class AkinatorGUI:
    def __init__(self, root):
        self.root = root
      ##  self.root.title("Adivina Quién (One Piece)")
        self.root.configure(bg="#1976d2")  # Fondo azul acorde al logo

        self.chars = load_data()
        if not self.chars:
            self.root.destroy()
            return

        # Logo del juego (ruta absoluta)
        logo_path = os.path.join(os.path.dirname(__file__), "Images", "Logo.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            img = img.resize((150, 150))
            self.logo_img = ImageTk.PhotoImage(img)
            self.logo_label = tk.Label(root, image=self.logo_img, bg="#1976d2")
            self.logo_label.pack(pady=(10, 5))
        else:
            self.logo_label = tk.Label(root, text="Logo no encontrado", bg="#1976d2", fg="white", font=("Arial", 12, "italic"))
            self.logo_label.pack(pady=(10, 5))

        # Nombre del juego visible siempre
        ##self.title_label = tk.Label(
          ##  root,
           ## text="=== Adivina Quién (One Piece) ===",
            ##font=("Arial", 18, "bold"),
            ##fg="#ffd600",  # Amarillo vibrante
          ##  bg="#1976d2"
      ##  )
        ##self.title_label.pack(pady=(0, 10))

        # Marco para la pregunta
        self.question_frame = tk.Frame(root, bg="#e3f2fd", bd=2, relief="groove")
        self.question_frame.pack(pady=10, padx=20, fill="x")

        # Label de pregunta
        self.label = tk.Label(
            self.question_frame,
            text="Bienvenido al juego!",
            wraplength=400,
            font=("Arial", 14),
            bg="#e3f2fd",
            fg="#263238"
        )
        self.label.pack(pady=12, padx=10)

        # Botones de respuesta
        self.button_frame = tk.Frame(root, bg="#1976d2")
        self.button_frame.pack(pady=10)

        btn_style = {
            "font": ("Arial", 12, "bold"),
            "width": 10,
            "height": 2,
            "bd": 2,
            "relief": "raised",
            "activebackground": "#ffe082"
        }
        self.s_button = tk.Button(self.button_frame, text="Sí", bg="#ffd600", fg="black", command=lambda: self.answer("s"), **btn_style)
        self.n_button = tk.Button(self.button_frame, text="No", bg="#e53935", fg="white", command=lambda: self.answer("n"), **btn_style)
        self.nd_button = tk.Button(self.button_frame, text="No sé", bg="#fff176", fg="black", command=lambda: self.answer("nd"), **btn_style)

        self.s_button.grid(row=0, column=0, padx=8)
        self.n_button.grid(row=0, column=1, padx=8)
        self.nd_button.grid(row=0, column=2, padx=8)

        # Botón de reinicio
        self.reset_button = tk.Button(
            root,
            text="Reiniciar Juego",
            bg="#ffb300",
            fg="black",
            font=("Arial", 12, "bold"),
            width=18,
            height=1,
            bd=2,
            relief="groove",
            activebackground="#ffe082",
            command=self.reset_game
        )
        self.reset_button.pack(pady=(10, 5))

        # Botón de agregar personaje
        self.add_button = tk.Button(
            root,
            text="Agregar Personaje",
            bg="#00e676",
            fg="black",
            font=("Arial", 12, "bold"),
            width=18,
            height=1,
            bd=2,
            relief="groove",
            activebackground="#b9f6ca",
            command=self.teach_new
        )
        self.add_button.pack(pady=(0, 15))

        # Botón de salir
        self.exit_button = tk.Button(
            root,
            text="Salir",
            bg="#e53935",
            fg="white",
            font=("Arial", 12, "bold"),
            width=18,
            height=1,
            bd=2,
            relief="groove",
            activebackground="#ff8a65",
            command=self.root.quit
        )
        self.exit_button.pack(pady=(0, 15))

        self.respuestas_previas = {}
        self.reset_game()  # Inicializa el juego

    def reset_game(self):
        self.candidates = self.chars.copy()
        self.asked = set()
        self.respuestas_previas = {}
        self.update_question()

    def update_question(self):
        # Si solo queda un candidato, adivina directamente
        if len(self.candidates) == 1:
            name = self.candidates[0]["nombre"]
            if messagebox.askyesno("Mi suposición", f"¿Tu personaje es {name}?"):
                messagebox.showinfo("¡Acerté!", "¡Genial! He acertado.")
                self.reset_game()
                return
            else:
                self.candidates.pop(0)
                self.update_question()
                return

        # Busca la mejor pregunta disponible
        q = best_question(self.candidates, self.asked, self.respuestas_previas)

        # Si no hay preguntas útiles, entonces muestra los candidatos restantes
        if not q:
            if len(self.candidates) == 0:
                if messagebox.askyesno("Sin coincidencias", "No encontré ningún personaje con esas características.\n¿Quieres agregar el personaje correcto?"):
                    self.teach_new()
                self.reset_game()
                return

            # Si hay varios candidatos pero ya no hay preguntas útiles
            names = "\n".join([c["nombre"] for c in self.candidates])
            if messagebox.askyesno("Candidatos restantes", f"No tengo más preguntas útiles.\nPosibles candidatos:\n{names}\n¿Quieres agregar el personaje correcto?"):
                self.teach_new()
            self.reset_game()
            return

        # Si hay preguntas útiles, sigue preguntando
        self.current_question = q
        self.asked.add(q)
        self.label.config(text=ATTR_TEXT[q])

    def answer(self, resp):
        self.respuestas_previas[self.current_question] = resp
        self.candidates = filtrar(self.candidates, self.current_question, resp)
        self.update_question()

    def teach_new(self):
        new_window = tk.Toplevel()
        new_window.title("Nuevo personaje")
        tk.Label(new_window, text="Nombre del personaje:").pack()
        name_entry = tk.Entry(new_window)
        name_entry.pack()

        attrs_vars = {}
        for a in ATTRS:
            var = tk.IntVar()
            tk.Checkbutton(new_window, text=ATTR_TEXT[a], variable=var).pack(anchor="w")
            attrs_vars[a] = var

        def save_new():
            nombre = name_entry.get().strip()
            if not nombre:
                messagebox.showerror("Error", "Debe poner un nombre.")
                return
            new_char = {"nombre": nombre}
            for a in ATTRS:
                new_char[a] = bool(attrs_vars[a].get())
            self.chars.append(new_char)
            save_data(self.chars)
            messagebox.showinfo("Guardado", f"Personaje '{nombre}' guardado.")
            new_window.destroy()

        tk.Button(new_window, text="Guardar", command=save_new).pack(pady=10)

# =========================
# EJECUCIÓN
# =========================

if __name__ == "__main__":
    root = tk.Tk()
    gui = AkinatorGUI(root)
    root.mainloop()

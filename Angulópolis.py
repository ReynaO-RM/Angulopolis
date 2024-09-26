import tkinter as tk
from tkinter import messagebox
import random
from tkinter import TclError

# Lista de 30 preguntas de ejemplo sobre ángulos complementarios
questions = {
    1: [("¿Cuál es el complemento de 30°?", 60), ("¿Cuál es el complemento de 45°?", 45),
        ("¿Cuál es el complemento de 10°?", 80),
        ("¿Cuál es el complemento de 20°?", 70), ("¿Cuál es el complemento de 25°?", 65),
        ("¿Cuál es el complemento de 15°?", 75),
        ("¿Cuál es el complemento de 50°?", 40), ("¿Cuál es el complemento de 70°?", 20),
        ("¿Cuál es el complemento de 60°?", 30),
        ("¿Cuál es el complemento de 40°?", 50)],
    2: [("¿Cuál es el complemento de 80°?", 10), ("¿Cuál es el complemento de 90°?", 0),
        ("¿Cuál es el complemento de 55°?", 35),
        ("¿Cuál es el complemento de 30°?", 60), ("¿Cuál es el complemento de 25°?", 65),
        ("¿Cuál es el complemento de 35°?", 55),
        ("¿Cuál es el complemento de 15°?", 75), ("¿Cuál es el complemento de 5°?", 85),
        ("¿Cuál es el complemento de 45°?", 45),
        ("¿Cuál es el complemento de 10°?", 80)],
    3: [("¿Cuál es el complemento de 22°?", 68), ("¿Cuál es el complemento de 19°?", 71),
        ("¿Cuál es el complemento de 33°?", 57),
        ("¿Cuál es el complemento de 17°?", 73), ("¿Cuál es el complemento de 24°?", 66),
        ("¿Cuál es el complemento de 29°?", 61),
        ("¿Cuál es el complemento de 11°?", 79), ("¿Cuál es el complemento de 42°?", 48),
        ("¿Cuál es el complemento de 38°?", 52),
        ("¿Cuál es el complemento de 32°?", 58)]
}


class AngleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Bienvenido a Angulópolis")
        self.root.configure(bg="lightblue")  # Color de fondo del menú
        self.scores = [0, 0, 0]  # Puntuaciones por nivel
        self.level = 0
        self.current_question = None
        self.errors = 0
        self.timer = 30
        self.timer_running = False
        self.error_penalty = False
        self.timer_id = None  # ID del temporizador
        self.questions_answered = 0  # Contador de preguntas respondidas en el nivel

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Juego de Ángulos Complementarios", font=("Roboto", 16, "bold italic"),
                 bg="lightblue").pack(pady=20)

        tk.Button(self.root, text="Iniciar Juego", command=self.start_game, bg="green", fg="white").pack(pady=10)
        tk.Button(self.root, text="Instrucciones", command=self.show_instructions, bg="red", fg="white").pack(pady=10)
        tk.Button(self.root, text="Tabla de Puntuaciones", command=self.show_scores, bg="orange", fg="white").pack(
            pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_game(self):
        self.level = 0
        self.scores = [0, 0, 0]  # Reiniciar puntuaciones acumuladas
        self.errors = 0
        self.timer = 30
        self.questions_answered = 0  # Reiniciar contador de preguntas respondidas
        self.start_level()

    def start_level(self):
        if self.level < 3:
            self.clear_window()
            self.current_question = random.choice(questions[self.level + 1])
            self.setup_question_screen()
        else:
            # Asegurarse de no acceder a un índice fuera de rango
            if self.level >= len(self.scores):
                self.level = len(self.scores) - 1  # Limitar al último nivel si fuera necesario
            self.show_scores()

    def setup_question_screen(self):
        self.change_background_color("green")  # Cambiar el color de fondo

        tk.Label(self.root, text=f"Nivel {self.level + 1}", font=("Roboto", 14, "bold italic"), bg="green").pack(
            pady=10)

        question_label = tk.Label(self.root, text=self.current_question[0], font=("Helvetica", 14), bg="green")
        question_label.pack(pady=10)

        self.answer_entry = tk.Entry(self.root, justify='center')  # Centrar entrada de texto
        self.answer_entry.pack(pady=10)

        # Botón para enviar la respuesta
        tk.Button(self.root, text="Enviar Respuesta", command=self.check_answer, bg="purple", fg="white").pack(pady=10)

        self.score_label = tk.Label(self.root, text=f"Puntos: {self.scores[self.level]}",
                                    font=("Roboto", 14, "bold italic"), bg="green")
        self.score_label.pack(pady=10)

        self.timer_label = tk.Label(self.root, text=f"Tiempo: {self.timer}", font=("Roboto", 14, "bold italic"),
                                    bg="green")
        self.timer_label.pack(pady=10)

        self.start_timer()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer > 0:
            self.timer -= 1
            self.timer_label.config(text=f"Tiempo: {self.timer}")
            self.timer_id = self.root.after(1000, self.update_timer)  # Guardar ID del temporizador
        else:
            self.end_level()

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
            if user_answer == self.current_question[1]:
                # Respuesta correcta
                self.error_penalty = False  # Reiniciar la penalización al acertar
                self.scores[self.level] += 10  # 10 puntos por respuesta correcta
                self.timer += 5  # Recuperar 5 segundos por respuesta correcta
                self.questions_answered += 1  # Incrementar contador de preguntas respondidas
                self.answer_entry.delete(0, tk.END)

                # Si se han respondido 10 preguntas, terminar el nivel
                if self.questions_answered >= 10:
                    self.end_level()  # Terminar el nivel
                else:
                    self.start_level()  # Cargar nueva pregunta
            else:
                # Respuesta incorrecta
                self.errors += 1
                self.scores[self.level] -= 10  # Penalizar con 10 puntos por error
                if self.scores[self.level] < 0:  # Asegurarse de que no haya puntaje negativo
                    self.scores[self.level] = 0

                self.error_penalty = True  # Activar penalización por errores
                self.change_color()  # Cambiar color según número de errores
                self.answer_entry.delete(0, tk.END)

                # Si se cometen 4 errores, terminar el juego
                if self.errors >= 4:
                    self.end_game()  # Terminar el juego

            # Aquí es donde ocurre el error de actualización del widget, y es donde aplicamos el try-except.
            try:
                self.score_label.config(text=f"Puntos: {self.scores[self.level]}")
            except TclError:
                # Manejar la excepción si el widget ya no existe
                print("El widget score_label ha sido destruido y no se puede actualizar.")

        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido.")
        except IndexError as e:
            messagebox.showerror("Error", f"Error de índice: {e}")

    def end_game(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)  # Detener el temporizador
            self.timer_id = None
        self.timer_running = False

        # Mostrar mensaje de que el juego ha terminado
        messagebox.showinfo("Juego Terminado",
                            f"Has cometido 4 errores. El juego ha terminado.\nPuntuación Nivel {self.level + 1}: {self.scores[self.level]} puntos.")

        self.change_background_color("lightblue")  # Volver al color de menú
        self.show_scores()  # Mostrar la tabla de puntuaciones

    def change_color(self):
        colors = ["yellow", "orange", "red"]
        if self.errors <= 3:
            self.change_background_color(colors[self.errors - 1])

    def change_background_color(self, color):
        # Cambiar el color de fondo de la ventana principal
        self.root.configure(background=color)

        # Cambiar el color de fondo de todos los widgets para que coincidan con el nuevo fondo
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=color)

    def end_level(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)  # Detener el temporizador
            self.timer_id = None
        self.timer_running = False

        if self.questions_answered >= 10:
            messagebox.showinfo("Nivel Completado",
                                f"Has completado el Nivel {self.level + 1}. Puntuación: {self.scores[self.level]} puntos.")
        else:
            messagebox.showinfo("Juego Terminado",
                                f"El tiempo ha terminado o has cometido demasiados errores. Puntuación: {self.scores[self.level]} puntos.")

        self.level += 1
        if self.level < len(self.scores):  # Asegurarse de que no exceda el número de niveles
            self.questions_answered = 0  # Reiniciar preguntas respondidas
            self.errors = 0  # Reiniciar errores
            self.timer = 30  # Reiniciar el tiempo del temporizador
            self.root.configure(bg="lightblue")
            self.start_level()
        else:
            self.root.configure(bg="lightblue")
            self.show_scores()

    def show_instructions(self):
        self.clear_window()
        tk.Label(self.root, text="Instrucciones del Juego", font=("Roboto", 16, "bold italic"), bg="lightblue").pack(pady=10)
        instructions = (
            "1. Responde a cada pregunta con el complemento del ángulo dado.\n"
            "2. Tienes 30 segundos para responder cada pregunta.\n"
            "3. Obtienes 10 puntos por cada respuesta correcta.\n"
            "4. Cometer errores te penaliza. Si cometes 4 errores, el juego termina.\n"
            "5. Intenta obtener la puntuación máxima en cada nivel.\n"
            "6. ¡Buena suerte!"
        )
        tk.Label(self.root, text=instructions, font=("Roboto", 12, " italic"), bg="lightblue", justify="left").pack(pady=10)
        tk.Button(self.root, text="Volver al Menú", command=self.create_main_menu, bg="blue", fg="white").pack(pady=10)

    def show_scores(self):
        self.clear_window()
        total_score = sum(self.scores)
        tk.Label(self.root, text="Tabla de Puntuaciones", font=("Roboto", 16, "bold italic"), bg="lightblue").pack(
            pady=20)
        for i, score in enumerate(self.scores, start=1):
            tk.Label(self.root, text=f"Nivel {i}: {score} puntos", font=("Roboto", 14), bg="lightblue").pack(pady=5)
        tk.Label(self.root, text=f"Puntaje Global: {total_score} puntos", font=("Roboto", 14, "bold"),
                 bg="lightblue").pack(pady=20)
        tk.Button(self.root, text="Volver al Menú Principal", command=self.create_main_menu, bg="orange",
                  fg="white").pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    game = AngleGame(root)
    root.iconbitmap("icon.ico")
    root.mainloop()
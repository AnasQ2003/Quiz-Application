import tkinter as tk
from tkinter import messagebox, ttk
import time
import json

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Quiz Challenge")
        self.root.geometry("900x700")
        self.root.configure(bg="#2C3E50")

        self.load_questions()
        self.current_question = 0
        self.score = 0
        self.user_answers = []
        self.question_times = []
        self.start_time = time.time()
        self.time_limit = 30
        self.timer_running = False
        self.setup_ui()

    def load_questions(self):
        try:
            with open("questions.json", "r") as file:
                self.questions = json.load(file)
        except FileNotFoundError:
            self.questions = [
                {"question": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"],
                 "answer": "Paris"},
                {"question": "Which planet is known as the Red Planet?",
                 "options": ["Earth", "Mars", "Jupiter", "Saturn"], "answer": "Mars"},
                {"question": "Who wrote the play 'Romeo and Juliet'?",
                 "options": ["William Shakespeare", "Charles Dickens", "Mark Twain", "Jane Austen"],
                 "answer": "William Shakespeare"},
                {"question": "What is the chemical symbol for water?", "options": ["O2", "H2O", "CO2", "NaCl"],
                 "answer": "H2O"},
                {"question": "Which is the largest ocean on Earth?",
                 "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
                 "answer": "Pacific Ocean"},
                {"question": "What is the powerhouse of the cell?",
                 "options": ["Nucleus", "Mitochondria", "Ribosome", "Endoplasmic Reticulum"], "answer": "Mitochondria"},
                {"question": "Which gas do plants absorb from the atmosphere?",
                 "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "answer": "Carbon Dioxide"},
                {"question": "What is the square root of 64?", "options": ["6", "7", "8", "9"], "answer": "8"},
                {"question": "Which country is famous for the Great Wall?",
                 "options": ["India", "China", "Japan", "Russia"], "answer": "China"},
                {"question": "Who discovered gravity?",
                 "options": ["Albert Einstein", "Isaac Newton", "Galileo Galilei", "Nikola Tesla"],
                 "answer": "Isaac Newton"}
            ]
            self.save_questions()

    def save_questions(self):
        with open("questions.json", "w") as file:
            json.dump(self.questions, file, indent=4)

    def setup_ui(self):
        self.frame = tk.Frame(self.root, bg="#34495E")
        self.frame.pack(expand=True)

        self.title_label = tk.Label(self.frame, text="Quiz Challenge", font=("Arial", 28, "bold"), bg="#34495E",
                                    fg="#ECF0F1")
        self.title_label.pack(pady=20)

        self.question_number_label = tk.Label(self.frame, text="", font=("Arial", 16, "bold"), bg="#34495E",
                                              fg="#E74C3C")
        self.question_number_label.pack()

        self.question_label = tk.Label(self.frame, text="", font=("Arial", 20), wraplength=700, bg="#34495E",
                                       fg="#ECF0F1")
        self.question_label.pack(pady=10)

        self.options_var = tk.StringVar()
        self.option_buttons = []

        for i in range(4):
            btn = tk.Radiobutton(self.frame, text="", variable=self.options_var, value="", font=("Arial", 16),
                                 bg="#2C3E50", fg="black", indicatoron=0, width=30, height=2, relief="raised", bd=3)
            btn.pack(pady=5)
            self.option_buttons.append(btn)

        self.time_heading = tk.Label(self.frame, text="Time Remaining 30 seconds:", font=("Arial", 14, "bold"),
                                     bg="#34495E", fg="#F1C40F")
        self.time_heading.pack(pady=(15, 0))

        self.time_bar = ttk.Progressbar(self.frame, length=300, mode='determinate', maximum=100)
        self.time_bar.pack(pady=10)

        self.next_button = tk.Button(self.frame, text="Next", font=("Arial", 18, "bold"), bg="#27AE60", fg="white",
                                     command=self.next_question)
        self.next_button.pack(pady=20)

        self.load_question()

    def load_question(self):
        self.start_time = time.time()
        self.time_bar["value"] = 100
        self.timer_running = True
        self.update_timer()

        question_data = self.questions[self.current_question]
        self.question_label.config(text=question_data["question"])
        self.question_number_label.config(text=f"Question {self.current_question + 1} of {len(self.questions)}")

        self.options_var.set("")

        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=option, value=option)

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            remaining_time = self.time_limit - elapsed_time

            if remaining_time <= 0:
                self.timer_running = False
                self.time_bar["value"] = 0
                self.next_question()
            else:
                self.time_bar["value"] = (remaining_time / self.time_limit) * 100
                self.root.after(100, self.update_timer)

    def next_question(self):
        self.timer_running = False
        end_time = time.time()
        time_taken = round(end_time - self.start_time, 2)
        self.question_times.append(time_taken)

        selected_answer = self.options_var.get()
        correct_answer = self.questions[self.current_question]["answer"]

        if selected_answer == correct_answer:
            self.score += 1
            comment = "Good job!"
        else:
            comment = "Better luck next time!"

        self.user_answers.append(
            (self.questions[self.current_question]["question"], selected_answer or "No Answer", correct_answer,
             time_taken, comment))

        self.current_question += 1

        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.show_results()

    def show_results(self):
        self.frame.destroy()
        result_frame = tk.Frame(self.root, bg="#2C3E50")
        result_frame.pack(expand=True)

        title_label = tk.Label(result_frame, text="Quiz Results", font=("Arial", 28, "bold"), bg="#2C3E50",
                               fg="#ECF0F1")
        title_label.pack(pady=20)

        score_label = tk.Label(result_frame, text=f"Your Score: {self.score} / {len(self.questions)}",
                               font=("Arial", 20), bg="#2C3E50", fg="#F39C12")
        score_label.pack(pady=10)

        table = ttk.Treeview(result_frame,
                             columns=("Question", "Your Answer", "Correct Answer", "Time Taken", "Comment"),
                             show='headings')
        table.heading("Question", text="Question")
        table.heading("Your Answer", text="Your Answer")
        table.heading("Correct Answer", text="Correct Answer")
        table.heading("Time Taken", text="Time Taken (s)")
        table.heading("Comment", text="Comment")

        for entry in self.user_answers:
            table.insert("", tk.END, values=entry)

        table.pack(pady=20)

        exit_button = tk.Button(result_frame, text="Exit", font=("Arial", 18, "bold"), bg="#E74C3C", fg="white",
                                command=self.root.quit)
        exit_button.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

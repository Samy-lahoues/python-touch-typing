from tkinter import Tk, Frame, Label,Entry, Button, StringVar, messagebox, font
from random import shuffle
import time


class TypingTuter:
    def __init__(self,root):
        self.root = root;
        self.root.title("Typing Tutor")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Custom fonts
        self.title_font = font.Font(family="Arial", size=20, weight="bold")
        self.heading_font = font.Font(family="Arial", size=16, weight="bold")
        self.text_font = font.Font(family="Courier", size=14)
        self.status_font = font.Font(family="Arial", size=12)

        # Typing variable
        self.index = 0
        self.list_index = 0
        self.words_list = []
        self.word_count = 10
        self.truth_array = []

        # Timing variables
        self.start_timer = time.time()
        self.end_time = 0
        self.word_per_minute = 0

        #* Game variables
        self.lives = 3
        self.score = 0
        self.sentence = []

        # Load words
        self.load_words()

        # Create intro frame
        self.create_intro_frame()

    def load_words(self):
        try:
            with open("words.txt", "r") as file:
                for word in file:
                    self.words_list.append(word.strip())
        except FileNotFoundError:
            # Fallback word list in case the file is not found
            self.words_list = ["the", "be", "to", "of", "and", "a", "in", "that",
                                "have", "I", "it", "for", "not", "on", "with", "he",
                                "as", "you", "do", "at", "this", "but", "his", "by",
                                "from", "they", "we", "say", "her", "she", "or", "an"]
        shuffle(self.words_list)
    def create_intro_frame(self):
        self.intro_frame = Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        self.intro_frame.pack(fill="both", expand=True)

        # Welcome label
        Label(self.intro_frame, text="Welcome to Typing Tutor",
            font=self.title_font, bg="#f0f0f0", fg="#333333").pack(pady=(50, 30))

        # Words Selection frame
        selection_frame = Frame(self.intro_frame, bg="#f0f0f0")
        selection_frame.pack(pady=20)

        Label(selection_frame, font=self.status_font, text=f"how many words do you want to type? (10-){len(self.words_list)}"
            , bg="#f0f0f0").pack(side="left",padx=5)
        self.words_var = StringVar(value="10");
        self.words_entry = Entry(selection_frame,textvariable=self.words_var,
            justify="center", width=5, font=self.status_font )
        self.words_entry.pack(side="left", padx=5)

        # Start Button
        Button(self.intro_frame, text="Start typing", command=self.start_game,
            font=self.heading_font, bg="#4CAF50", fg="white",
            activebackground="#45a049", padx=20, pady=10).pack(pady=30)
    def start_game(self):
        try:
            words_number = int(self.words_var.get())
            if words_number < 10 or words_number > len(self.words_list):
                messagebox.showerror("Invalid Input",
                    f"Please enter a number between 10 and {len(self.words_list)}")
                return
            # Set word count and slice word list
            self.words_list = self.words_list[:words_number]
            # Clear intro frame
            self.intro_frame.destroy()
            # Setup game frame
            self.create_game_frame()
            # Start timer
            self.start_timer = time.time()

            # Focus the window to capture keystrokes
            self.root.focus_force()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
    def create_game_frame(self):
        self.game_frame = Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        self.game_frame.pack(fill="both", expand=True)
        # Stats frame at the top
        stats_frame = Frame(self.game_frame, bg="#e0e0e0", padx=10, pady=10)
        stats_frame.pack(fill="x", pady=(0, 20))

        # lives and score labels
        self.lives_var = StringVar(value=f"Lives: {'❤️' * self.lives}")
        self.score_var = StringVar(value=f"Score: {self.score}")
        self.progress_var = StringVar(value=f"Word : 1 of {len(self.words_list)}")

        Label(stats_frame, textvariable=self.lives_var, font=self.status_font,
            bg="#e0e0e0").pack(side="left", padx=10)
        Label(stats_frame, textvariable=self.score_var, font=self.status_font,
            bg="#e0e0e0").pack(side="left", padx=10)
        Label(stats_frame, textvariable=self.progress_var, font=self.status_font,
            bg="#e0e0e0").pack(side="right", padx=10)

        # Word to type
        self.word_frame = Frame(self.game_frame, bg="#f0f0f0", padx=10, pady=20)
        self.word_frame.pack(fill="x")

        Label(self.word_frame, text="Type this word:", font=self.heading_font,
            bg="#f0f0f0").pack()
        self.current_word_var = StringVar(value=self.words_list[0])
        self.word_label = Label(self.word_frame, textvariable=self.current_word_var,
                               font=self.text_font, bg="white", fg="#333333",
                               padx=20, pady=15, borderwidth=2, relief="groove")
        self.word_label.pack(pady=10)
        # Feedback frame
        self.feedback_frame = Frame(self.game_frame, bg="#f0f0f0", height=50)
        self.feedback_frame.pack(fill="x", pady=10)

        self.feedback_var = StringVar(value="Start typing...")
        self.feedback_label = Label(self.feedback_frame, textvariable=self.feedback_var)

        # Bind keypress events
        self.root.bind("<Key>", self.keypress)

    def keypress(self, event):
        # Ignore special keys
        if len(event.char) == 0 or event.char == '\r' or event.char == '\n':
            return
        word = self.words_list[self.list_index]

        if self.words_list[self.list_index]:
            if event.char == word[self.index]:
                self.score += 1
                self.score_var.set(f"Score: {self.score}")
                self.truth_array.append(' ')
                self.feedback_var.set("Correct!")
                self.feedback_label.config(fg="green")
            else:
                self.truth_array.append('-')
                self.feedback_var.set(f"Wrong! Expected '{word[self.index]}', got '{event.char}'" )
                self.feedback_label.config(fg="red")
                self.lives -= 1
                self.lives_var.set(f"Lives: {'❤️' * self.lives}")

                if self.lives == 0:
                    self.game_over()
                    return

            self.index += 1

            # If word is complete
            if self.index == len(word):
                self.truth_array.append('|')
                self.index = 0
                self.list_index += 1
                self.sentence.append(word)

                # Update progress
                if self.list_index < len(self.words_list):
                    self.current_word_var.set(self.words_list[self.list_index])
                    self.progress_var.set(f"Word: {self.list_index }+ of { len(self.words_list)}")
                    self.feedback_var.set("Next word!")
                    self.feedback_label.config(fg="blue")
                else:
                    self.game_completed()
    def game_over(self):
        self.root.unbind('<Key>')
        # Clear game frame
        self.game_frame.destroy()
        # Create results frame
        self.create_results_frame("Game Over!")
    def game_completed(self):
        self.root.unbind('<Key>')
        # Calculate WPM
        end_time = time.time()
        total_time = (end_time - self.start_timer) / 60
        wpm = len(self.sentence) / total_time if total_time > 0 else 0
        self.word_per_minute = round(wpm, 2)
        # Clear game frame
        self.game_frame.destroy()
        # Create results frame
        self.create_results_frame("Congratulations!")

    def create_results_frame(self, text_title):
        self.result_frame = Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        self.result_frame.pack(fill="both", expand=True)

        # Title
        Label(self.result_frame, text=text_title, font=self.title_font,
            bg="#f0f0f0", fg="#333333").pack(pady=(30,20))
        # Stats
        stats_frame = Frame(self.result_frame, bg="#e0e0e0", padx=20, pady=15)
        stats_frame.pack(fill="x", pady=10)

        Label(stats_frame, text=f"Final Score:{self.score}", font=self.heading_font,
            bg="#e0e0e0").pack(pady=5)

        if hasattr(self, 'word_per_minute') and self.word_per_minute > 0:
            Label(stats_frame, text=f"Your WPM: {self.word_per_minute}", font=self.heading_font,
                bg="#e0e0e0").pack(pady=5)

        # Words typed
        Label(self.result_frame, text="Words you typed:", font=self.status_font,
            bg="#f0f0f0").pack(pady=(15, 5))
        typed_text = ' '.join(self.sentence)
        Label(self.result_frame, text=typed_text, font=self.text_font,
            bg="white", fg="#333333", wraplength=700, padx=10, pady=10).pack(fill="x")
        accuracy_text = ''.join(self.truth_array)
        Label(self.result_frame, text=accuracy_text, font=self.text_font, bg="white", fg="#666666",
            wraplength=700, padx=10, pady=10).pack(fill="x")
        # Botton frame
        buttons_frame = Frame(self.result_frame, bg="#f0f0f0", pady=20)
        buttons_frame.pack()

        Button(buttons_frame, text="Play Again", command=self.restart_game, font=self.status_font, bg="#4CAF50", fg="white",
        activebackground="#45a049", padx=15, pady=8).pack(side="left", padx=10)

    def restart_game(self):
        #Reset game variables
        self.index = 0
        self.list_index = 0
        self.truth_array = []
        self.lives = 3
        self.score = 0
        self.sentence = []

        # Shuffle words again
        shuffle(self.words_list)

        # Clear results frame
        self.result_frame.destroy()

        # Create intro frame again
        self.create_intro_frame()

if __name__ == "__main__":
    root = Tk()
    app = TypingTuter(root)
    root.mainloop()

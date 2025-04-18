from tkinter import Tk, Frame, Label,Entry, Button, StringVar, messagebox, font
from random import shuffle
import time


class TypingTuter:
    def __init__(self,root):
        self.root = root;
        self.root.title("Typing Tutor")
        self.root.geomitry("800x600")
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
# # Introduction
# with open("words.txt", "r") as file:
#     for word in file:
#         words_list.append(word.strip())
# shuffle(words_list)
# words_number = int(input(f"How many words do you want to type ? from 10 to {len(words_list)}"))
# words_list = words_list[:words_number]
# print("-------------------- Welcome Typing Tutor --------------------")
# time.sleep(2)
# clear()
# print("Total words ", len(words_list))
# time.sleep(2)
# clear()

# # Logic
# def keypress(event):
#     global words_list
#     global sentence
#     global truth_array
#     global word_count
#     global index
#     global list_index
#     global time_multiplier
#     global word_per_minute
#     global start_timer
#     global end_time
#     global lives
#     global score

#     # select the first word from words_list
#     word = words_list[list_index]
#     print("---- type the word ----")
#     print(word)

#     if event.char == word[index]:
#         index += 1
#         score += 1
#         truth_array.append(' ')
#     else:
#         index += 1
#         truth_array.append('-')
#         clear()
#         print("Word "+ str(list_index+1) + " out of "+str(word_count)+": " + words_list[list_index])
#         print("wrong letter")
#         lives -= 1
#         if lives == 0:
#             print(' '.join(sentence))
#             print(''.join(truth_array))
#             print("Game Over!")
#             print("finale score ", score)
#             root.destroy()
#             return
#     if index == len(word):
#         truth_array.append('|')
#         index = 0
#         list_index += 1
#         sentence.append(word)
#     if list_index == len(words_list):
#             clear()
#             end_time = time.time()
#             total_time = int(end_time - start_timer) / 60  # in minutes
#             wpm = len(sentence) / total_time
#             print(f"Your WPM: {wpm:.2f}")
#             print(' '.join(sentence))
#             print(''.join(truth_array))
#             print("Congratulations! you have beaten the game!")
#             print("Final Score: ", score)
#             root.destroy()

# root = Tk()
# root.bind_all('<Key>', keypress)
# root.withdraw()
# root.mainloop()

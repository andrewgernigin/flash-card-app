from tkinter import *
import pandas
from random import choice

# ------------------ CONSTANTS -------------------

BACKGROUND_COLOR = "#B1DDC6"
TIME_DELAY_SECONDS = 3

# ------------------ VARIABLES -------------------

entry = {}

# ------------------ POPULATE WORD LIST -----------------------------
try:
    word_df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    word_df = pandas.read_csv("data/french_words.csv")
    word_dict = word_df.to_dict(orient="records")
    word_df.to_csv("data/words_to_learn.csv", index=False)
else:
    word_dict = word_df.to_dict(orient="records")


# ------------ GENERATE NEW CARD WITH RANDOM WORD ------------------
def new_card():
    global entry, timer
    window.after_cancel(timer)
    entry = choice(word_dict)
    french_word = entry["French"]
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=french_word, fill="black")
    # Flip Card after global TIME_DELAY_SECONDS seconds
    timer = window.after(TIME_DELAY_SECONDS * 1000, flip_card)


# ---------------------- Flip Card --------------------------
def flip_card():
    english_word = entry["English"]
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=english_word, fill="white")


# --------------------BUTTON CODE ----------------------------
def update_words_to_learn():
    word_dict.remove(entry)
    df = pandas.DataFrame(word_dict)
    df.to_csv("data/words_to_learn.csv", index=False)
    new_card()


# ------------------ UI CREATION ---------------------
window = Tk()
window.title("Flashy")
window.resizable(width=False, height=False)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# set images for front and back of cards
card_front = PhotoImage(file="images/card_front.png/")
card_back = PhotoImage(file="images/card_back.png")

# set button images
wrong_image = PhotoImage(file="images/wrong.png")
right_image = PhotoImage(file="images/right.png")

canvas = Canvas()
canvas.config(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_image = canvas.create_image(0, 0, anchor=NW)
card_title = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2, rowspan=2)

right_button = Button(image=right_image, command=update_words_to_learn)
right_button.config(highlightthickness=0, borderwidth=0, bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR)
right_button.grid(column=1, row=2)

wrong_button = Button(image=wrong_image, command=new_card)
wrong_button.config(highlightthickness=0, borderwidth=0, bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR)
wrong_button.grid(column=0, row=2)

# start program by initializing global timer and populating initial card
timer = window.after(3000, flip_card)
new_card()


window.mainloop()

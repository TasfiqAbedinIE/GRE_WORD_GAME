############### MODULES ################

import pandas as pd
import random as rand
from tkinter import *

############### DESIGN VARIABLES ################

background = "#EAF5FF"
word_color = "#393E46"
button_word_color = "#F6F5F5"
font = "Comic Sans MS"
yes_button_color_bg = "#71EFA3"
no_button_color_bg = "#D54C4C"
yes_button_color_active_bg = "#50CB93"
no_button_color_active_bg = "#D83A56"
start_button_color = "#AA2EE6"
swap_button_color = "#5767FF"
canvas_bg = "#7C83FD"
canvas_def_bg = "#8AD7C1"
canvas_text_color = "#FDF6F0"

############### DATA FILE ################

core_data_file = pd.read_csv("word_data.csv")

########### STORING DATA INTO SEPARATE VARIABLES ##########

serial_number = core_data_file.Serial
main_word = core_data_file.Word
description = core_data_file.Meaning
study_score = core_data_file.Study_score

######### CONTROLING VARIABLES #########

start = 0
batch = 30
count_word = 0
unknown = 0
word_tracker = []
swap_count = 0
swap_activation = 0

len_of_serial_number = len(serial_number)  # Determining the length of serial number


######## GENERATING RANDOM NUMBER ########

def random_number():
    global count_word
    global game_value

    if start == 1 and count_word < 30:
        game_value = rand.randint(1, len_of_serial_number) - 1
        print(game_value)

        for i in word_tracker:  # ELIMINATING ANY REPEAT VALUE
            if game_value == i:
                game_value = rand.randint(1, len_of_serial_number) - 1

        count_word += 1
        word_tracker.append(game_value)
        show_word()
    else:
        result()
        print(word_tracker)


######## FUNCTION DISPLAYING THE WORD INTO THE CANVAS ########

def show_word():
    global swap_activation
    canvas.itemconfig(word_view, text=main_word[game_value].upper())
    canvas.config(bg=canvas_bg)

    if count_word <= 1:
        appeared_label.config(text=f"Word Appeared {study_score[game_value]} Time.")
    else:
        appeared_label.config(text=f"Word Appeared {study_score[game_value]} Times.")

    swap_activation = 0
    update_study_score()


###### FUNCTION DISPLAYING THE MEANING OF THE WORD INTO CANVAS ######

def show_def():
    global unknown, swap_activation

    game_description = description[game_value].upper()
    canvas.itemconfig(word_view, text=game_description)
    canvas.config(bg=canvas_def_bg)

    unknown += 1
    swap_activation = 1


###### SWAPING THE CARD FOR WORD AND MEANING ########

def swap():
    global swap_count, swap_activation

    if swap_count == 0 and swap_activation == 1:
        canvas.itemconfig(word_view, text=description[game_value].upper())
        canvas.config(bg=canvas_def_bg)
        swap_count = 1
    elif swap_count == 1 and swap_activation == 1:
        canvas.itemconfig(word_view, text=main_word[game_value].upper())
        canvas.config(bg=canvas_bg)
        swap_count = 0


####### UPDATING THE APPEARANCE VALUE OF THE WORD INTO MAIN CSV FILE ########

def update_study_score():
    new_score = study_score[game_value] + 1
    core_data_file.loc[game_value, "Study_score"] = new_score
    core_data_file.to_csv("word_data.csv", index=False)


######## FUNCTION DISPLAYING THE RESULT ########

def result():
    global start, count_word, unknown
    comment = f"You know {round(100 - (unknown / count_word) * 100)}% of Words"
    canvas.itemconfig(word_view, text=comment)

    print(count_word)
    print(unknown)
    print((unknown / count_word) * 100)

    # RETURNING EVERYTHING INTO INITIAL STATE
    start = 0
    count_word = 0
    unknown = 0


######## FUNCTION OF START BUTTON ACTION ########

def start_button_action():
    global start
    if start == 0:
        start = 1
        random_number()
        start_button.config(text="RESULT")
    else:
        result()
        start_button.config(text="START")


##################### UI DESIGN ######################

window = Tk()
window.title("GRE WORD GAME")
window.config(padx=0, pady=0, bg=background)

win_width = round(window.winfo_screenwidth() * 0.68)
win_height = round(window.winfo_screenheight() * 0.75)
window.geometry(f"{win_width}x{win_height}")

# print(win_width)
# print(win_height)

canvas = Canvas(width=win_width, height=300, bg=canvas_bg, highlightthickness=0)
word_view = canvas.create_text(win_width / 2, 150, text="PRESS START TO BEGIN", fill=canvas_text_color,
                               font=(font, int(win_width * 0.03), "bold"), width=int(win_width * 0.9))
canvas.place(x=0, y=0)

question_view = Label(text="DO YOU KNOW THIS WORD?", fg=word_color, bg=background, font=(font, 20))
question_view.place(x=(win_width/2)-180, y=400)

swap_button = Button(text="SWAP", highlightthickness=0, height=2, width=10, bg=swap_button_color,
                     fg=button_word_color, font=(font, 10, "bold"), relief="flat", command=swap)
swap_button.place(x=(win_width/2)-20, y=580)

yes_button = Button(text="YES", highlightthickness=0, height=round(win_height * 0.001), width=round(win_width * 0.01),
                    fg=button_word_color, bg=yes_button_color_bg, font=(font, 30, "bold"), relief="flat",
                    cursor="circle",
                    activebackground=yes_button_color_active_bg, activeforeground=button_word_color,
                    command=random_number)
yes_button.place(x=(win_width/2)-280, y=500)

no_button = Button(text="NO", highlightthickness=0, height=round(win_height * 0.001), width=round(win_width * 0.01),
                   bg=no_button_color_bg, fg=button_word_color, font=(font, 30, "bold"), relief="flat", cursor="circle",
                   activebackground=no_button_color_active_bg, activeforeground=button_word_color, command=show_def)
no_button.place(x=(win_width/2)+100, y=500)

appeared_label = Label(text="", bg=background, fg="black", font=(font, 15, "bold"))
appeared_label.place(x=10, y=300)

start_button = Button(text="START", highlightthickness=0, height=2, width=10, bg=start_button_color,
                      fg=button_word_color, font=(font, 15, "bold"), relief="flat", activebackground=start_button_color,
                      command=start_button_action)
start_button.place(x=(win_width/2)-50, y=300)

window.mainloop()

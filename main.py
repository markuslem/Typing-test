import tkinter as tk
from text_generator import get_text
import unidecode


window = tk.Tk()

window.geometry("1350x900")
window.title("Type Tester")
window.config(background="lightblue")

label = tk.Label(window, text="To begin, start typing", font=("Arial", 18))
label.pack()

correct_words = 0
minutes = 1
seconds = 0
typing = False
end = False

wpm = round(correct_words * 60 / (60 - seconds), 2)
wpm_label = tk.Label(window, text=wpm, font=("Arial", 24))
wpm_label.place(x=1200, y=25)

timer = tk.Label(window, text=str(minutes) + ":" + str(seconds) + "0", font=("Arial", 24))
timer.place(x=900, y=25)

textbox_str = tk.StringVar()
textbox = tk.Entry(window, font=("Arial", 18), textvariable=textbox_str)
textbox.pack(pady=15)


text_obj_list = list()


# creating a tuple of the words on the Wikipedia page to word_tuple
word_list = list()
for sentence in get_text():
    sentence = sentence.split(" ")
    for word in sentence:
        word_list.append(word)




line_length = 0 # character count in one line
for i in range(len(word_list)):
    text = tk.Label(window, text=word_list[i], font=("Arial", 18))
    text_obj_list.append(text)
    line_length += len(word_list[i])

    if i == 0:
        first_in_line = text
        text.place(y=100, x=40)
        text.config(fg="grey")

    
    elif line_length >= 70: # The maximum length of a line in characters
        
        text.place(in_=first_in_line, rely=1.0, x=-1)
        first_in_line = text #first word/object in the next line
        line_length = 0

    else:
        text.place(in_=text_obj_list[i-1], relx=1.0, y=-1)
    window.update()

wpm = 0
def update_timer(): #updates timer and wpm (words per minute)
    global end
    global seconds
    global minutes
    global timer
    global wpm_label
    
    if seconds == 0 and minutes > 0:
        minutes -= 1
        seconds = 59
    elif seconds > 0:
        seconds -= 1
    elif seconds == 0 and minutes == 0:
        end = True

    wpm_label.destroy()

    wpm = round(correct_words * 60 / (60 - seconds), 2)
    wpm_label = tk.Label(window, text=wpm, font=("Arial", 24))
    wpm_label.place(x=1200, y=25)

    timer.destroy()

    if seconds < 10: seconds = "0" + str(seconds)
    timer = tk.Label(window, text=str(minutes) + ":" + str(seconds), font=("Arial", 24))
    seconds = int(seconds)
    timer.place(x=900, y=25)
    window.after(1000, update_timer)

def word_written(*args):
    input = textbox.get() # input - the word written

    if len(input) > 0 and end == False:
        global typing
        typing = True

    # the word turns red, if the input is incorrect and back to grey if it's correct
    global correct_words
    current_word = word_list[correct_words] + " "
    if unidecode.unidecode(current_word[:len(input)]) != unidecode.unidecode(input):
        text_obj_list[correct_words].config(fg="red")
        textbox.config(fg="red")
    else:
        text_obj_list[correct_words].config(fg="grey")
        textbox.config(fg="black")

    # moves on to the next word if correct
    if len(input) > 0 and input[-1] == " " and end == False and unidecode.unidecode(input[:-1]) == unidecode.unidecode(word_list[correct_words]):
        textbox.delete(0, tk.END)
        text_obj_list[correct_words+1].config(fg="grey")
        text_obj_list[correct_words].config(fg="black")
        
        correct_words += 1

    if end:
        textbox.delete(0, tk.END)
        



def ctrl_backspace(event):
    global textbox
    textbox.delete(0, tk.END)

textbox_str.trace("w", word_written)
textbox.bind("<Control-BackSpace>", ctrl_backspace)

def typing_started():
    if typing == True:
        update_timer()
    else:
        window.after(10, typing_started)

window.after(10, typing_started)



window.mainloop()

    
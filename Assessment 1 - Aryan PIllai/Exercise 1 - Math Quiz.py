from tkinter import *
import random
import pygame
from PIL import ImageTk, Image
from tkinter import messagebox

pygame.mixer.init()

#adds the music in the background for a fun experience
try:
    pygame.mixer.music.load("backgroundgui.mp3")
    pygame.mixer.music.play(-1)
except pygame.error:
    print("Warning: backgroundgui.mp3 not found. Music will not play.")

#color palette, makes it MUCH easier for me to set the colos
BG_COLOR = "#0A0F1E"
PANEL_COLOR = "#1C2A3A"
TEXT_COLOR = "#C0D8E0"
ACTION_COLOR = "#00BFFF"
DANGER_COLOR = "#FF5733"
SUCCESS_COLOR = "#00FF7F"

# Difficulty ranges and score
ranges = {
    "Easy": (1, 9),
    "Moderate": (10, 99),
    "Advanced": (1000, 9999)
}

# Globals (streamlines the process and cuts time)
score = 0
question_number = 0
max_questions = 10
attempt = 1
current_answer = None
current_level = None
is_muted = False
mute_button = None
frame_results = None
results_score_label = None
results_rank_label = None

# Mute Button!!
def toggle_mute():
    global is_muted
    if is_muted:
        # Currently muted, so unmute
        pygame.mixer.music.unpause()
        mute_button.config(text="🔊")
        is_muted = False
    else:
        # Currently playing, so mute
        pygame.mixer.music.pause()
        mute_button.config(text="🔇")
        is_muted = True

# Function: displayMenu
def displayMenu():
    switch_to_frame(frame_main)

# Function: randomInt
def randomInt(level):
    low, high = ranges[level]
    return random.randint(low, high)

# Function: decideOperation
def decideOperation():
    return random.choice(['+', '-'])

# Function: isCorrect
def isCorrect(user_answer):
    return user_answer == current_answer

# Function: displayProblem
def displayProblem(level, entry_box, question_label):
    global current_answer, attempt
    attempt = 1  # Reset attempt

    a = randomInt(level)
    b = randomInt(level)
    op = decideOperation()
    current_answer = eval(f"{a}{op}{b}")

    question_label.config(text=f"Q{question_number+1}: {a} {op} {b} = ?")
    entry_box.delete(0, END)

# Function: displayResults
def displayResults():
    global score 
    
    final_rank = getRank(score)
    
    # Shows your score!
    results_score_label.config(text=f"Final Score: {score}/100")
    results_rank_label.config(text=f"Rank: {final_rank}")
    
    # Switch to the results frame
    switch_to_frame(frame_results)

# Ranks you at the end of the quiz
def getRank(final_score):
    if final_score >= 90:
        return "Rank: A+"
    elif final_score >= 80:
        return "Rank: A"
    elif final_score >= 70:
        return "Rank: B"
    elif final_score >= 60:
        return "Rank: C"
    else:
        return "Rank: D"

def switch_to_frame(frame):
    frame.tkraise()
    if mute_button:
        mute_button.tkraise() # Keeps the mute button on top

root = Tk()
root.config(bg=BG_COLOR)
root.title("Math Quiz Game")
root.geometry('800x700')
root.iconbitmap('CodeLogo.ico')

# Main Menu Frame 
frame_main = Frame(root, bg=BG_COLOR)
frame_main.place(relx=0.5, rely=0.5, anchor=CENTER, width=500, height=500)

# Labels (Shows the text)
Label(frame_main, text="Math Quiz Game!", font=('Consolas', 20, 'bold'), 
      bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

Label(frame_main, text="Choose Difficulty", font=('Consolas', 15), 
      bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

# Clickable buttons!!
Button(frame_main, text="Easy", width=20, fg=BG_COLOR, bg=ACTION_COLOR, 
       font=('Consolas', 12, 'bold'), relief=FLAT,
       command=lambda: start_quiz("Easy")).pack(pady=10, ipady=5) 

Button(frame_main, text="Moderate", width=20, fg=BG_COLOR, bg=ACTION_COLOR, 
       font=('Consolas', 12, 'bold'), relief=FLAT,
       command=lambda: start_quiz("Moderate")).pack(pady=10, ipady=5) 

Button(frame_main, text="Advanced", width=20, fg=BG_COLOR, bg=ACTION_COLOR, 
       font=('Consolas', 12, 'bold'), relief=FLAT,
       command=lambda: start_quiz("Advanced")).pack(pady=10, ipady=5) 


#  Quiz Frame(s) 
def create_quiz_frame(level):
    frame = Frame(root, bg=BG_COLOR) 
    
    Label(frame, text=level, font=('Consolas', 16, 'bold'), 
          bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)

    question = Label(frame, text="", font=("Consolas", 14), 
                     bg=BG_COLOR, fg=TEXT_COLOR)
    question.pack(pady=10)

    entry = Entry(frame, font=("Consolas", 12), bg=PANEL_COLOR, fg=TEXT_COLOR, 
                  insertbackground=TEXT_COLOR, width=20)
    entry.pack(pady=5)
    entry.bind('<Return>', lambda event: handle_answer(level, entry, feedback, score_label, question)) #Makes it so that the enter key can be pressed to submit the answer!!

    feedback = Label(frame, text="", bg=BG_COLOR, fg=TEXT_COLOR, 
                     font=("Consolas", 12))
    feedback.pack(pady=10)

    score_label = Label(frame, text="Score: 0/0", bg=BG_COLOR, fg=TEXT_COLOR, 
                        font=("Consolas", 12))
    score_label.pack(pady=5)

    Button(frame, text="Submit", fg=BG_COLOR, bg=ACTION_COLOR,
           font=("Consolas", 12, "bold"), width=15, relief=FLAT,
           command=lambda: handle_answer(level, entry, feedback, score_label, question)).pack(pady=5, ipady=5)# Submits the answer

    Button(frame, text="Main Menu", fg=TEXT_COLOR, bg=DANGER_COLOR,
           font=('Consolas', 12), width=15, relief=FLAT,
           command=lambda: displayMenu()).pack(pady=10, ipady=5)# Send you back to the main page

    frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=500, height=500)

    return {
        "frame": frame, "entry": entry, "question": question,
        "feedback": feedback, "score": score_label
    }
#  Results Frame  
def create_results_frame():
    global frame_results, results_score_label, results_rank_label

    frame_results = Frame(root, bg=BG_COLOR)
    frame_results.place(relx=0.5, rely=0.5, anchor=CENTER, width=500, height=500)

    Label(frame_results, text="Quiz Complete!", font=('Consolas', 22, 'bold'),
          bg=BG_COLOR, fg=ACTION_COLOR).pack(pady=(80, 20))

    results_score_label = Label(frame_results, text="Final Score: 0/100", font=('Consolas', 16),
                                bg=BG_COLOR, fg=TEXT_COLOR)
    results_score_label.pack(pady=10)

    results_rank_label = Label(frame_results, text="Rank: N/A", font=('Consolas', 16),
                                bg=BG_COLOR, fg=TEXT_COLOR)
    results_rank_label.pack(pady=20)

    Button(frame_results, text="Play Again", fg=BG_COLOR, bg=ACTION_COLOR,
           font=('Consolas', 12, 'bold'), width=15, relief=FLAT,
           borderwidth=0, activebackground=TEXT_COLOR,
           command=displayMenu).pack(pady=10, ipady=5) # Calls displayMenu

    Button(frame_results, text="Quit", fg=TEXT_COLOR, bg=DANGER_COLOR,
           font=('Consolas', 12), width=15, relief=FLAT,
           borderwidth=0, activebackground=TEXT_COLOR,
           command=root.quit).pack(pady=5, ipady=5) # Exits the program


frame_dict = {
    "Easy": create_quiz_frame("Easy"),
    "Moderate": create_quiz_frame("Moderate"),
    "Advanced": create_quiz_frame("Advanced")
}

create_results_frame()

def start_quiz(level):
    global score, question_number, current_level
    score = 0
    question_number = 0
    current_level = level
    
    fdict = frame_dict[level]
    fdict["entry"].config(state=NORMAL)
    fdict["feedback"].config(text="", fg=TEXT_COLOR)
    fdict["score"].config(text="Score: 0/0")
    
    switch_to_frame(fdict["frame"])
    displayProblem(level, fdict["entry"], fdict["question"])

def handle_answer(level, entry, feedback, score_label, question_label):
    global score, question_number, attempt
    user_input = entry.get()
    
    if user_input == "":
        feedback.config(text="Enter a number first!", fg=DANGER_COLOR)
        return

    try:
        user_answer = int(user_input)
    except:
        feedback.config(text="Numbers only!", fg=DANGER_COLOR)
        return

    if isCorrect(user_answer):
        if attempt == 1:
            score += 10
            feedback.config(text="✅ Correct (First Attempt)!", fg=SUCCESS_COLOR)
        else:
            score += 5
            feedback.config(text="✅ Correct (Second Attempt)!", fg=SUCCESS_COLOR)
        
        question_number += 1
        score_label.config(text=f"Score: {score}/{question_number*10}")
        
        if question_number >= max_questions:
            displayResults()
            entry.config(state=DISABLED)
            return
        
        displayProblem(level, entry, question_label)
        
    else:
        if attempt == 1:
            feedback.config(text=f"❌ Wrong! Try once more.", fg=DANGER_COLOR)
            attempt += 1
            entry.delete(0, END)
        else:
            feedback.config(text=f"❌ Wrong again! Correct: {current_answer}", fg=DANGER_COLOR)
            question_number += 1
            score_label.config(text=f"Score: {score}/{question_number*10}")
            
            if question_number >= max_questions:
                displayResults()
                entry.config(state=DISABLED)
                return
                
            displayProblem(level, entry, question_label)

# Creates the mute button on the ROOT window
mute_button = Button(root, text="🔊", 
                     font=("Consolas", 14), 
                     fg=TEXT_COLOR, 
                     bg=BG_COLOR,
                     relief=FLAT,
                     borderwidth=0,
                     activebackground=PANEL_COLOR,
                     command=toggle_mute)

# Place it in the top-right corner
mute_button.place(x=760, y=10)

switch_to_frame(frame_main)
root.mainloop()# Finally done. Hope you had fun with the game!!
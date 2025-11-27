import tkinter as tk
from PIL import Image, ImageTk 
import pygame 
import random
import os

#Setup 
jokes = []
punchline = ""

#Dark Mode Colour Palette
COLOR_CONTAINER_BG = "#2c3e50"  
COLOR_TEXT = "#ecf0f1"          
COLOR_BTN = "#2980b9"           
COLOR_QUIT = "#c0392b"          
COLOR_PUNCHLINE = "#2ecc71"     
FONT_MAIN = ("Segoe UI", 14)
FONT_PUNCH = ("Segoe UI", 16, "bold")
FONT_BTN = ("Segoe UI", 12, "bold")

#Window Dimensions
WIN_WIDTH = 600
WIN_HEIGHT = 500

#Initialize Audio Mixer
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Could not initialize audio: {e}")

#Reads the file
try:
    with open("randomJokes.txt", "r", encoding="utf-8") as file:
        for line in file:
            if line.strip() and "?" in line:
                jokes.append(line.strip())
except FileNotFoundError:
    print("Error: randomJokes.txt file not found.")
    jokes.append("Why did the chicken cross the road? To get to the other side.")

#Functions 
def show_joke():
    global punchline
    if not jokes: 
        setupLabel.config(text="No jokes loaded!")
        return

    mainJ = random.choice(jokes)
    parts = mainJ.split("?", 1)
    setup = parts[0] + "?" 
    if len(parts) > 1:
        punchline = parts[1]
    else:
        punchline = "Error in joke format."
    
    setupLabel.config(text=setup)
    punchlineLabel.config(text="")
    
    J_Answer.pack_forget()
    next.pack_forget()
    PunchButton.pack(pady=20, ipadx=10, ipady=5)

def show_punchline():
    punchlineLabel.config(text=punchline)
    PunchButton.pack_forget()
    next.pack(pady=20, ipadx=10, ipady=5)
    
    #Plays the laughtrack
    try:
    
        sound_file = "Laugh Track.mp3" 
        
        if os.path.exists(sound_file):
            sound = pygame.mixer.Sound(sound_file)
            sound.set_volume(0.5) #Sets volume (0.0 to 1.0)
            sound.play(maxtime=2000) #Play for only 2 seconds
        else:
            print(f"Warning: {sound_file} not found.")
    except Exception as e:
        print(f"Error playing sound: {e}")

#Setup
root = tk.Tk()
root.title("Alexa, Tell me a Joke")
root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
root.configure(bg=COLOR_CONTAINER_BG) 

image_path = "AlexaBG.png" #Adds an image to bg
bg_photo = None 

if os.path.exists(image_path):
    try:
        pil_image = Image.open(image_path)
        resized_image = pil_image.resize((WIN_WIDTH, WIN_HEIGHT), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(resized_image)
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()
        print("Background image loaded successfully.")
    except Exception as e:
        print(f"Error processing background image: {e}")
else:
    print(f"Warning: '{image_path}' not found. Running with solid background.")

#Content Container
container = tk.Frame(root, bg=COLOR_CONTAINER_BG, bd=2, relief="ridge")
container.place(relx=0.5, rely=0.5, anchor="center", width=WIN_WIDTH-80, height=WIN_HEIGHT-80)

#Labels
setupLabel = tk.Label(container, text="Press the button for a laugh!", 
                      font=FONT_MAIN, bg=COLOR_CONTAINER_BG, fg=COLOR_TEXT, 
                      wraplength=480, justify="center")
setupLabel.pack(pady=(20, 20))

punchlineLabel = tk.Label(container, text="", 
                          font=FONT_PUNCH, bg=COLOR_CONTAINER_BG, fg=COLOR_PUNCHLINE, 
                          wraplength=480, justify="center")
punchlineLabel.pack(pady=(0, 30))

#Button Styling 
def get_styled_button(parent, text, cmd, bg_color=COLOR_BTN):
    btn = tk.Button(parent, text=text, command=cmd,
                    bg=bg_color, fg="white",
                    activebackground=COLOR_TEXT, activeforeground=COLOR_CONTAINER_BG,
                    font=FONT_BTN, relief="flat", cursor="hand2",
                    width=20)
    return btn

#Buttons
J_Answer = get_styled_button(container, "Alexa tell me a Joke", show_joke)
J_Answer.pack(pady=20, ipadx=10, ipady=5)

PunchButton = get_styled_button(container, "Show Punchline", show_punchline)
next = get_styled_button(container, "Next Joke", show_joke)

# Quit Button
quit_frame = tk.Frame(container, bg=COLOR_CONTAINER_BG)
quit_frame.pack(side="bottom", pady=20)

btn_quit = get_styled_button(quit_frame, "Quit", root.destroy, bg_color=COLOR_QUIT)
btn_quit.pack(ipadx=10, ipady=5)

root.mainloop()
#Finally done!!!
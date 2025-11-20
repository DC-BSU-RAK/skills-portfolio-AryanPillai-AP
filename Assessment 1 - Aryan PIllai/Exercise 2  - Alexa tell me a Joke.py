import tkinter as tk
import random

#Setup 
jokes = []
punchline = ""

#Reads the file
try:
    with open("randomJokes.txt", "r", encoding="utf-8") as file:
        for line in file:
            #Checks if the line is not empty and has a '?'
            if line.strip() and "?" in line:
                jokes.append(line.strip())
except FileNotFoundError:
    print("Error: randomJokes.txt file not found.")

#Defines the functions (makes it much more streamlined)

def show_joke():
    global punchline
    
    #Picks a random joke
    mainJ = random.choice(jokes)
    
    #Splits the beginning of the joke and the ending
    #split('?', 1) splits at the first question mark only
    parts = mainJ.split("?", 1)
    
    setup = parts[0] + "?"  #Adds the question mark back
    punchline = parts[1]
    
    #Update the labels
    setupLabel.config(text=setup)
    punchlineLabel.config(text="") #Clears the old punchline
    
    #Buttons
    J_Answer.pack_forget()  #Hides the "Tell me a joke" button
    next.pack_forget()       #Hides the "Next Joke" button
    PunchButton.pack(pady=5)   #Shows the "Show Punchline" button

def show_punchline():
    #Shows the text that's being stored in the global variable
    punchlineLabel.config(text=punchline)
    
    #Switch buttons
    PunchButton.pack_forget()  #Hides the "Show Punchline" button
    next.pack(pady=5)        #Shows the "Next Joke" button

#Creates the window
root = tk.Tk()
root.title("Alexa, Tell me a Joke")
root.geometry("400x300")

#Labels
setupLabel = tk.Label(root, text="Press the button for a laugh!", font=("Arial", 12), wraplength=380)
setupLabel.pack(pady=20)

punchlineLabel = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="blue", wraplength=380)
punchlineLabel.pack(pady=20)

#Buttons
J_Answer = tk.Button(root, text="Alexa tell me a Joke", command=show_joke)
J_Answer.pack(pady=5)

PunchButton = tk.Button(root, text="Show Punchline", command=show_punchline)

next = tk.Button(root, text="Next Joke", command=show_joke)

btn_quit = tk.Button(root, text="Quit", bg="red", fg="white", command=root.destroy)
btn_quit.pack(side="bottom", pady=10)

root.mainloop()
#Finally done!
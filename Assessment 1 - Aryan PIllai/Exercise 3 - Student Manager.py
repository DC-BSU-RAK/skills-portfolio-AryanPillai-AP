import tkinter as tk
from tkinter import messagebox

#Main Variables
all_students = [] 
bg_photo = None 

root = tk.Tk()
root.title("Student Manager")
root.geometry("850x600")

#Define the frames
menu_frame = tk.Frame(root)
results_frame = tk.Frame(root)

#Background Image
def load_background_image():
    global bg_photo
    try:
        bg_photo = tk.PhotoImage(file="background.png")
        print("Background image loaded successfully.")
    except Exception as e:
        print("No background image found (or format not supported). Running without it.")

def add_bg_to_frame(frame):
    
    if bg_photo is not None:
        #Creates a Label containing the image
        bg_label = tk.Label(frame, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

#Loads the data
def load_data():
    try:
        f = open("studentMarks.txt", "r")
        lines = f.readlines()
        f.close()
        
        #Skips the first line
        for i in range(1, len(lines)):
            line = lines[i].strip()
            parts = line.split(',')
            
            if len(parts) == 6:
                all_students.append(parts)     
    except:
        messagebox.showerror("Error", "Could not find studentMarks.txt")

#Calculations
def get_grade(percentage):
    if percentage >= 70:
        return 'A'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

def calculate_score(student_row):
    c1 = int(student_row[2])
    c2 = int(student_row[3])
    c3 = int(student_row[4])
    exam = int(student_row[5])
    return c1 + c2 + c3 + exam

#Helps the display look sleeker
def print_header():
    report_text.delete("1.0", tk.END)
    
    header = f"{'Code':<10} {'Name':<25} {'Total':<10} {'Percent':<10} {'Grade':<10}"
    divider = "-" * 70
    
    report_text.insert(tk.END, header + "\n")
    report_text.insert(tk.END, divider + "\n")

def print_student(code, name, total, pct, grade):
    #Formats the row exactly like the header
    row = f"{code:<10} {name:<25} {total:<10} {pct:<10} {grade:<10}"
    report_text.insert(tk.END, row + "\n")

# BUTTON ACTIONS

def view_all():
    print_header()
    
    total_percentage = 0
    count = 0
    
    for student in all_students:
        code = student[0]
        name = student[1]
        
        total_score = calculate_score(student)
        percentage = (total_score / 160) * 100
        grade = get_grade(percentage)
        
        total_percentage += percentage
        count += 1
        
        pct_str = str(round(percentage, 1)) + "%"
        
        #Prints to the text box
        print_student(code, name, total_score, pct_str, grade)

    #Summary
    if count > 0:
        avg = round(total_percentage / count, 1)
        summary_label.config(text="Total Students: " + str(count) + " | Class Average: " + str(avg) + "%")
    
    show_results_page()
    title_label.config(text="All Student Records")

def view_individual():
    search_text = search_entry.get().lower()
    
    if search_text == "":
        messagebox.showwarning("Warning", "Please enter a name or ID")
        return

    print_header()
    found = False
    
    for student in all_students:
        code = student[0].lower()
        name = student[1].lower()
        
        if search_text in code or search_text in name:
            found = True
            
            total_score = calculate_score(student)
            percentage = (total_score / 160) * 100
            grade = get_grade(percentage)
            pct_str = str(round(percentage, 1)) + "%"
            
            print_student(student[0], student[1], total_score, pct_str, grade)
            
    if found:
        summary_label.config(text="Search Complete.")
        show_results_page()
        title_label.config(text="Search Results")
    else:
        messagebox.showinfo("Result", "No student found.")

def show_highest():
    if len(all_students) == 0:
        return
        
    best_student = all_students[0]
    best_score = calculate_score(best_student)
    
    for student in all_students:
        current_score = calculate_score(student)
        if current_score > best_score:
            best_score = current_score
            best_student = student
            
    print_header()
    pct = (best_score / 160) * 100
    grade = get_grade(pct)
    pct_str = str(round(pct, 1)) + "%"
    
    print_student(best_student[0], best_student[1], best_score, pct_str, grade)
    
    summary_label.config(text="Highest Score Found.")
    show_results_page()
    title_label.config(text="Highest Scoring Student")

def show_lowest():
    if len(all_students) == 0:
        return
        
    worst_student = all_students[0]
    worst_score = calculate_score(worst_student)
    
    for student in all_students:
        current_score = calculate_score(student)
        if current_score < worst_score:
            worst_score = current_score
            worst_student = student
            
    print_header()
    pct = (worst_score / 160) * 100
    grade = get_grade(pct)
    pct_str = str(round(pct, 1)) + "%"
    
    print_student(worst_student[0], worst_student[1], worst_score, pct_str, grade)
    
    summary_label.config(text="Lowest Score Found.")
    show_results_page()
    title_label.config(text="Lowest Scoring Student")

#Navigation
def show_menu():
    results_frame.pack_forget()
    menu_frame.pack(fill="both", expand=True)

def show_results_page():
    menu_frame.pack_forget()
    results_frame.pack(fill="both", expand=True)

#Setup

load_background_image()

#Frame 1

add_bg_to_frame(menu_frame)

tk.Label(menu_frame, text="Student Manager", font=("Arial", 22, "bold")).pack(pady=40)

btn_font = ("Arial", 12)

tk.Button(menu_frame, text="1. View All Records", command=view_all, font=btn_font, width=25).pack(pady=10)

tk.Label(menu_frame, text="Search (Enter ID or Name):").pack(pady=(20, 5))
search_entry = tk.Entry(menu_frame, font=("Arial", 12))
search_entry.pack(pady=5)

tk.Button(menu_frame, text="2. View Individual", command=view_individual, font=btn_font, width=25).pack(pady=5)
tk.Button(menu_frame, text="3. Show Highest Score", command=show_highest, font=btn_font, width=25).pack(pady=10)
tk.Button(menu_frame, text="4. Show Lowest Score", command=show_lowest, font=btn_font, width=25).pack(pady=10)
tk.Button(menu_frame, text="Exit", command=root.quit, bg="red", fg="white", font=btn_font, width=15).pack(pady=30)


#Frame 2
add_bg_to_frame(results_frame)

top_bar = tk.Frame(results_frame)
top_bar.pack(fill="x", pady=10, padx=10)

title_label = tk.Label(top_bar, text="Results", font=("Arial", 18, "bold"))
title_label.pack(side="left")

tk.Button(top_bar, text="Back to Menu", command=show_menu).pack(side="right")

report_text = tk.Text(results_frame, font=("Courier", 12), width=80, height=20)
report_text.pack(padx=20, pady=10)

summary_label = tk.Label(results_frame, text="Summary info will appear here.", font=("Arial", 12))
summary_label.pack(pady=10)

load_data()
show_menu()
root.mainloop()

#Finally done!!!! 
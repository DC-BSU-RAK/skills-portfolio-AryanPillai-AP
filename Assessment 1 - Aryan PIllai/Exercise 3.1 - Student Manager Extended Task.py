import tkinter as tk
from tkinter import messagebox, simpledialog
import os

#Uses the provided file
FILE_NAME = "studentMarks.txt"

#Color palette for the app to make it much more cleaner
COLORS = {
    "bg_main": "#121212",
    "bg_surface": "#1E1E1E",
    "bg_sidebar": "#252526",
    "text_main": "#E0E0E0",
    "text_muted": "#A0A0A0",
    "accent": "#00C853",
    "danger": "#CF6679",
    "highlight": "#3700B3",
    "input_bg": "#2D2D2D",
    "input_fg": "#FFFFFF",
    "border": "#333333"
}

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager Pro (Dark)")
        self.root.geometry("1100x650")
        self.root.configure(bg=COLORS["bg_main"])

        self.students = []
        self.sort_descending = True #Helps us toggle for the sorting of the records (Ascending or Descending)
        
        self.load_data()
        self.setup_styles()
        self.create_widgets()
        self.show_frame("menu")

    #Data management

    def load_data(self):
        """Loads data: Line 1 is count, rest are CSVs."""
        self.students.clear()
        if not os.path.exists(FILE_NAME):
            return

        try:
            with open(FILE_NAME, "r") as f:
                lines = f.readlines()
                
                for line in lines[1:]: 
                    parts = line.strip().split(',')
                    if len(parts) == 6:
                        self.students.append({
                            'code': parts[0],
                            'name': parts[1],
                            'c1': int(parts[2]),
                            'c2': int(parts[3]),
                            'c3': int(parts[4]),
                            'exam': int(parts[5])
                        })
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def save_data(self):
        """Writes data: Line 1 must be the count of students."""
        try:
            with open(FILE_NAME, "w") as f:
                f.write(f"{len(self.students)}\n")
                
                for s in self.students:
                    line = f"{s['code']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n"
                    f.write(line)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    #Calculations!!
    def calculate_stats(self, s):
        total_cw = s['c1'] + s['c2'] + s['c3']
        total_overall = total_cw + s['exam']
        
        percent = (total_overall / 160) * 100
        
        if percent >= 70: grade = 'A'
        elif percent >= 60: grade = 'B'
        elif percent >= 50: grade = 'C'
        elif percent >= 40: grade = 'D'
        else: grade = 'F'
        
        return total_cw, s['exam'], percent, grade

    #Basis of the UI
    def setup_styles(self):
        self.font_title = ("Segoe UI", 24, "bold")
        self.font_head = ("Segoe UI", 16, "bold")
        self.font_btn = ("Segoe UI", 11, "bold")
        self.font_mono = ("Consolas", 10)
        
    def create_btn(self, parent, text, cmd, bg_color, width=20):
        return tk.Button(
            parent, text=text, command=cmd, font=self.font_btn, 
            bg=bg_color, fg="white", relief="flat", 
            activebackground=COLORS["text_muted"], activeforeground="black",
            cursor="hand2", width=width, pady=8 
        )

    def create_widgets(self):
        #Main Menu Frame(VERY important)
        self.menu_frame = tk.Frame(self.root, bg=COLORS["bg_main"])
        content_area = tk.Frame(self.menu_frame, bg=COLORS["bg_main"])
        content_area.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(content_area, text="Student Manager Dashboard", font=self.font_title, 
                 bg=COLORS["bg_main"], fg=COLORS["text_main"]).pack(pady=(0, 30))

        search_lbl = tk.Label(content_area, text="Search Student (ID/Name):", 
                              bg=COLORS["bg_main"], fg=COLORS["text_muted"], font=("Segoe UI", 11))
        search_lbl.pack(anchor="w")
        
        self.search_entry = tk.Entry(content_area, font=("Segoe UI", 14), width=35, 
                                     bg=COLORS["input_bg"], fg=COLORS["input_fg"], 
                                     relief="flat", bd=0, insertbackground="white")
        self.search_entry.pack(pady=(5, 10), ipady=8)
        
        tk.Frame(content_area, height=1, bg=COLORS["border"], width=300).pack(fill="x", pady=(0, 25))

        btns = [
            ("View All Records", lambda: self.render_report(self.students, "All Class Records")),
            ("View Individual", self.view_individual),
            ("Show Highest", self.view_highest),
            ("Show Lowest", self.view_lowest),
        ]
        for text, cmd in btns:
            self.create_btn(content_area, text, cmd, COLORS["accent"], width=25).pack(pady=5)

        tk.Frame(content_area, height=20, bg=COLORS["bg_main"]).pack() 
        self.create_btn(content_area, "Exit Application", self.root.quit, COLORS["danger"], width=15).pack()

        #Results Frame
        self.results_frame = tk.Frame(self.root, bg=COLORS["bg_main"])
        sidebar = tk.Frame(self.results_frame, bg=COLORS["bg_sidebar"], width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False) 

        tk.Label(sidebar, text="ACTIONS", font=("Segoe UI", 14, "bold"), 
                 bg=COLORS["bg_sidebar"], fg=COLORS["text_muted"]).pack(pady=(40, 30))

        side_btns = [
            ("Toggle Sort (Asc/Desc)", self.sort_records, COLORS["highlight"]),
            ("Add New", self.add_student, COLORS["accent"]),
            ("Update", self.update_student, COLORS["accent"]),
            ("Delete", self.delete_student, COLORS["danger"]),
        ]
        for text, cmd, col in side_btns:
            btn = tk.Button(sidebar, text=text, command=cmd, font=("Segoe UI", 10, "bold"),
                            bg=col, fg="white", relief="flat", cursor="hand2", pady=8)
            btn.pack(fill="x", padx=20, pady=8)

        tk.Frame(sidebar, bg=COLORS["bg_sidebar"], height=50).pack() 
        tk.Button(sidebar, text="← Back to Menu", command=lambda: self.show_frame("menu"),
                  font=("Segoe UI", 10), bg="#333333", fg="white", relief="flat", cursor="hand2").pack(side="bottom", fill="x", pady=20)

        content = tk.Frame(self.results_frame, bg=COLORS["bg_main"])
        content.pack(side="right", fill="both", expand=True, padx=40, pady=40)

        self.results_title = tk.Label(content, text="Results", font=self.font_title, 
                                      bg=COLORS["bg_main"], fg=COLORS["text_main"])
        self.results_title.pack(anchor="w", pady=(0, 20))

        frame_text = tk.Frame(content, bg=COLORS["border"], padx=1, pady=1) 
        frame_text.pack(fill="both", expand=True)
        
        self.report_text = tk.Text(frame_text, font=self.font_mono, height=20, state="disabled",
                                   bg=COLORS["bg_surface"], fg=COLORS["text_main"], 
                                   relief="flat", padx=15, pady=15)
        self.report_text.pack(fill="both", expand=True)
        
        self.summary_frame = tk.Frame(content, bg=COLORS["bg_main"], height=50)
        self.summary_frame.pack(fill="x", pady=(10,0))
        self.summary_label = tk.Label(self.summary_frame, text="Ready", font=("Segoe UI", 11, "bold"), 
                                      bg=COLORS["bg_main"], fg=COLORS["accent"])
        self.summary_label.pack(pady=12)

    def show_frame(self, name):
        if name == "menu":
            self.results_frame.pack_forget()
            self.menu_frame.pack(fill="both", expand=True)
        else:
            self.menu_frame.pack_forget()
            self.results_frame.pack(fill="both", expand=True)

    def render_report(self, data_list, title_text, custom_msg=None):
        self.results_title.config(text=title_text)
        self.report_text.config(state="normal")
        self.report_text.delete("1.0", tk.END)

        if not data_list:
            self.report_text.insert(tk.END, "\n   No records found.")
            self.summary_label.config(text="Count: 0")
        else:
            #Splits the Total marks for the Coursework and Exam
            header = f"{'Code':<8} {'Name':<22} {'CW Total':<10} {'Exam':<8} {'Percent':<10} {'Grade':<6}\n"
            self.report_text.insert(tk.END, header)
            self.report_text.insert(tk.END, "-"*85 + "\n")

            total_pct_sum = 0
            
            for s in data_list:
                cw, exam, pct, grade = self.calculate_stats(s)
                total_pct_sum += pct
                row = f"{s['code']:<8} {s['name']:<22} {cw:<10} {exam:<8} {pct:.1f}%{'':<5} {grade:<6}\n"
                self.report_text.insert(tk.END, row)

            avg = total_pct_sum / len(data_list)
            summary = custom_msg if custom_msg else f"Total Records: {len(data_list)}   |   Class Average: {avg:.1f}%"
            self.summary_label.config(text=summary)

        self.report_text.config(state="disabled")
        self.show_frame("results")

    #Actions
    def view_individual(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showwarning("Warning", "Enter ID or Name.")
            return
        matches = [s for s in self.students if query in s['code'].lower() or query in s['name'].lower()]
        if matches:
            self.render_report(matches, f"Search Results: '{query}'")
        else:
            messagebox.showinfo("Result", "No student found.")

    def view_highest(self):
        if not self.students: return
        best = max(self.students, key=lambda s: self.calculate_stats(s)[2]) # Index 2 is percent
        self.render_report([best], "Highest Scorer", "Top performing student")

    def view_lowest(self):
        if not self.students: return
        worst = min(self.students, key=lambda s: self.calculate_stats(s)[2])
        self.render_report([worst], "Lowest Scorer", "Lowest performing student")

    def sort_records(self):
        if not self.students: return
        #Sorts Ascending OR Descending (SUPER HELFFUL)
        self.sort_descending = not self.sort_descending
        mode = "Descending" if self.sort_descending else "Ascending"
        
        self.students.sort(key=lambda s: self.calculate_stats(s)[2], reverse=self.sort_descending)
        self.render_report(self.students, f"Sorted Records ({mode})")
    
    def get_valid_mark(self, prompt, max_val, existing_val=None):
        """Validates input based on the specific Max Value (20 or 100)."""
        while True:
            val = simpledialog.askstring("Input", f"{prompt} (Max {max_val}):", initialvalue=existing_val)
            if val is None: return None 
            try:
                num = int(val)
                if 0 <= num <= max_val: return num
                else: messagebox.showerror("Error", f"Mark must be 0-{max_val}")
            except ValueError:
                messagebox.showerror("Error", "Enter a valid whole number")

    def add_student(self):
        code = simpledialog.askstring("Add", "Enter Code:")
        if not code: return
        if any(s['code'].lower() == code.lower() for s in self.students):
            messagebox.showerror("Error", "ID already exists.")
            return

        name = simpledialog.askstring("Add", "Enter Name:")
        if not name: return

        #Total Marks: Coursework = 20, Exam = 100

        c1 = self.get_valid_mark("Enter C1 Mark", 20)
        if c1 is None: return
        c2 = self.get_valid_mark("Enter C2 Mark", 20)
        if c2 is None: return
        c3 = self.get_valid_mark("Enter C3 Mark", 20)
        if c3 is None: return
        exam = self.get_valid_mark("Enter Exam Mark", 100)
        if exam is None: return

        self.students.append({'code': code, 'name': name, 'c1': c1, 'c2': c2, 'c3': c3, 'exam': exam})
        self.save_data()
        self.render_report(self.students, "All Records")
        messagebox.showinfo("Success", "Student Added.")

    def delete_student(self):
        query = simpledialog.askstring("Delete", "Enter ID or Name to delete:")
        if not query: return
        
        matches = [s for s in self.students if query.lower() in s['code'].lower() or query.lower() in s['name'].lower()]
        if not matches:
            messagebox.showinfo("Result", "No match found.")
            return
        
        target = matches[0] 
        if messagebox.askyesno("Confirm", f"Delete {target['name']} ({target['code']})?"):
            self.students.remove(target)
            self.save_data()
            self.render_report(self.students, "All Records")

    def update_student(self):
        query = simpledialog.askstring("Update", "Enter ID or Name to update:")
        if not query: return
        
        target = next((s for s in self.students if query.lower() in s['code'].lower() or query.lower() in s['name'].lower()), None)
        if not target:
            messagebox.showinfo("Result", "No match found.")
            return

        c1 = self.get_valid_mark(f"New C1 (Current: {target['c1']})", 20, target['c1'])
        if c1 is not None: target['c1'] = c1
        
        c2 = self.get_valid_mark(f"New C2 (Current: {target['c2']})", 20, target['c2'])
        if c2 is not None: target['c2'] = c2

        c3 = self.get_valid_mark(f"New C3 (Current: {target['c3']})", 20, target['c3'])
        if c3 is not None: target['c3'] = c3

        exam = self.get_valid_mark(f"New Exam (Current: {target['exam']})", 100, target['exam'])
        if exam is not None: target['exam'] = exam

        self.save_data()
        self.render_report(self.students, "All Records")
        messagebox.showinfo("Success", "Record Updated.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
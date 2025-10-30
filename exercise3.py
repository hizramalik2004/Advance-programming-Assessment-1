import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ---------------- Load and Save Data ----------------
def load_students():
    data = []
    try:
        with open("studentMarks.txt", "r") as f:
            lines = f.read().strip().splitlines()
            for line in lines[1:]:
                parts = line.split(",")
                if len(parts) >= 6:
                    sid, name, cw1, cw2, cw3, exam = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
                    cw1, cw2, cw3, exam = int(cw1), int(cw2), int(cw3), int(exam)
                    cw_total = cw1 + cw2 + cw3
                    overall = cw_total + exam
                    percent = (overall / 160) * 100
                    grade = (
                        "A" if percent >= 70 else
                        "B" if percent >= 60 else
                        "C" if percent >= 50 else
                        "D" if percent >= 40 else "F"
                    )
                    data.append({
                        "id": sid, "name": name,
                        "cw1": cw1, "cw2": cw2, "cw3": cw3, "exam": exam,
                        "cw_total": cw_total, "overall": overall,
                        "percent": percent, "grade": grade
                    })
    except FileNotFoundError:
        print("Note: studentMarks.txt will be created when you add first student")
    except Exception as e:
        messagebox.showerror("Error", f"Problem loading file: {str(e)}")
    return data

def save_students():
    try:
        with open("studentMarks.txt", "w") as f:
            f.write(str(len(students)) + "\n")
            for s in students:
                f.write(f"{s['id']},{s['name']},{s['cw1']},{s['cw2']},{s['cw3']},{s['exam']}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save data: {str(e)}")

# ---------------- Helper Functions ----------------
def show_output(text):
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)
    output_box.config(state="disabled")

def format_student(s):
    return (f"Student Name: {s['name']}\n"
            f"Student ID: {s['id']}\n"
            f"Coursework Marks: {s['cw1']}, {s['cw2']}, {s['cw3']}\n"
            f"Coursework Total: {s['cw_total']}/60\n"
            f"Exam Mark: {s['exam']}/100\n"
            f"Overall Percentage: {s['percent']:.1f}%\n"
            f"Final Grade: {s['grade']}\n"
            f"{'-'*40}\n")

def refresh_combo():
    student_combo["values"] = [f"{s['name']} ({s['id']})" for s in students]
    if students:
        student_combo.set(students[0]['name'] + " (" + students[0]['id'] + ")")

def validate_mark(subject, min_val, max_val, current_val=None):
    if current_val is not None:
        prompt = f"Enter {subject} mark ({min_val}-{max_val})\nCurrent: {current_val}"
    else:
        prompt = f"Enter {subject} mark ({min_val}-{max_val})"
    
    mark = simpledialog.askstring("Input Mark", prompt)
    if mark is None:
        return None
    try:
        mark_int = int(mark)
        if min_val <= mark_int <= max_val:
            return mark_int
        else:
            messagebox.showerror("Error", f"{subject} must be between {min_val} and {max_val}")
            return None
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number")
        return None

def get_selected_student():
    sel = student_combo.get()
    if not sel:
        messagebox.showwarning("Warning", "Please select a student first")
        return None
    try:
        student_id = sel.split("(")[-1].rstrip(")")
        for s in students:
            if s['id'] == student_id:
                return s
    except:
        pass
    messagebox.showerror("Error", "Student not found")
    return None

# ---------------- Core Functionalities ----------------
def view_all():
    if not students:
        show_output("No student records available.\nUse 'Add Student' to create new records.")
        return
    
    text = "ALL STUDENT RECORDS\n" + "="*50 + "\n\n"
    total_percent = 0
    
    for i, s in enumerate(students, 1):
        text += f"Record {i}:\n"
        text += format_student(s)
        total_percent += s["percent"]
    
    avg = total_percent / len(students)
    text += f"\nSummary:\n"
    text += f"Total Students: {len(students)}\n"
    text += f"Average Percentage: {avg:.1f}%\n"
    
    show_output(text)

def view_individual():
    student = get_selected_student()
    if student:
        text = "INDIVIDUAL STUDENT RECORD\n" + "="*50 + "\n\n"
        text += format_student(student)
        show_output(text)

def show_highest():
    if not students:
        show_output("No student records available")
        return
    best = max(students, key=lambda x: x["percent"])
    text = "HIGHEST PERFORMING STUDENT\n" + "="*50 + "\n\n"
    text += format_student(best)
    show_output(text)

def show_lowest():
    if not students:
        show_output("No student records available")
        return
    lowest = min(students, key=lambda x: x["percent"])
    text = "LOWEST PERFORMING STUDENT\n" + "="*50 + "\n\n"
    text += format_student(lowest)
    show_output(text)

def sort_records():
    if not students:
        show_output("No student records available")
        return
    
    if messagebox.askyesno("Sort Records", "Sort by percentage in descending order?"):
        students.sort(key=lambda x: x["percent"], reverse=True)
    else:
        students.sort(key=lambda x: x["percent"], reverse=False)
    
    refresh_combo()
    view_all()

def add_student():
    sid = simpledialog.askstring("Add Student", "Enter student ID:")
    if not sid:
        return
    
    if any(s['id'] == sid for s in students):
        messagebox.showerror("Error", "This student ID already exists")
        return
    
    name = simpledialog.askstring("Add Student", "Enter student name:")
    if not name:
        return
    
    cw1 = validate_mark("Coursework 1", 0, 20)
    if cw1 is None: return
    
    cw2 = validate_mark("Coursework 2", 0, 20)
    if cw2 is None: return
    
    cw3 = validate_mark("Coursework 3", 0, 20)
    if cw3 is None: return
    
    exam = validate_mark("Exam", 0, 100)
    if exam is None: return

    cw_total = cw1 + cw2 + cw3
    overall = cw_total + exam
    percent = (overall / 160) * 100
    grade = ("A" if percent >= 70 else "B" if percent >= 60 else
             "C" if percent >= 50 else "D" if percent >= 40 else "F")
    
    new_student = {
        "id": sid, "name": name,
        "cw1": cw1, "cw2": cw2, "cw3": cw3, "exam": exam,
        "cw_total": cw_total, "overall": overall,
        "percent": percent, "grade": grade
    }
    
    students.append(new_student)
    save_students()
    refresh_combo()
    
    text = "NEW STUDENT ADDED SUCCESSFULLY\n" + "="*50 + "\n\n"
    text += format_student(new_student)
    show_output(text)

def delete_student():
    student = get_selected_student()
    if not student:
        return
    
    if messagebox.askyesno("Confirm Delete", f"Delete {student['name']}? This cannot be undone."):
        students.remove(student)
        save_students()
        refresh_combo()
        show_output(f"Student {student['name']} has been deleted successfully.\nRemaining students: {len(students)}")

def update_student():
    student = get_selected_student()
    if not student:
        return
    
    cw1 = validate_mark("Coursework 1", 0, 20, student["cw1"])
    if cw1 is None: return
    
    cw2 = validate_mark("Coursework 2", 0, 20, student["cw2"])
    if cw2 is None: return
    
    cw3 = validate_mark("Coursework 3", 0, 20, student["cw3"])
    if cw3 is None: return
    
    exam = validate_mark("Exam", 0, 100, student["exam"])
    if exam is None: return

    student["cw1"] = cw1
    student["cw2"] = cw2
    student["cw3"] = cw3
    student["exam"] = exam
    student["cw_total"] = cw1 + cw2 + cw3
    student["overall"] = student["cw_total"] + exam
    student["percent"] = (student["overall"] / 160) * 100
    student["grade"] = ("A" if student["percent"] >= 70 else
                      "B" if student["percent"] >= 60 else
                      "C" if student["percent"] >= 50 else
                      "D" if student["percent"] >= 40 else "F")
    
    save_students()
    refresh_combo()
    
    text = "STUDENT RECORD UPDATED\n" + "="*50 + "\n\n"
    text += format_student(student)
    show_output(text)

def search_student():
    search_term = simpledialog.askstring("Search", "Enter student name or ID to search:")
    if not search_term:
        return
    
    results = []
    for s in students:
        if search_term.lower() in s['name'].lower() or search_term in s['id']:
            results.append(s)
    
    if not results:
        show_output(f"No students found matching '{search_term}'")
        return
    
    text = f"SEARCH RESULTS FOR '{search_term}'\n" + "="*50 + "\n\n"
    for s in results:
        text += format_student(s)
    
    text += f"\nFound {len(results)} matching record(s)"
    show_output(text)

def show_statistics():
    if not students:
        show_output("No student data available for statistics")
        return
    
    percentages = [s['percent'] for s in students]
    grades = [s['grade'] for s in students]
    
    text = "CLASS STATISTICS AND GRADE DISTRIBUTION\n" + "="*50 + "\n\n"
    text += f"Total Students: {len(students)}\n"
    text += f"Average Percentage: {sum(percentages)/len(percentages):.1f}%\n"
    text += f"Highest Percentage: {max(percentages):.1f}%\n"
    text += f"Lowest Percentage: {min(percentages):.1f}%\n\n"
    text += "Grade Distribution:\n"
    text += f"A Grades: {grades.count('A')}\n"
    text += f"B Grades: {grades.count('B')}\n"
    text += f"C Grades: {grades.count('C')}\n"
    text += f"D Grades: {grades.count('D')}\n"
    text += f"F Grades: {grades.count('F')}\n"
    
    show_output(text)

# ---------------- GUI Setup ----------------
students = load_students()

root = tk.Tk()
root.title("Student Manager")
root.geometry("900x650")
root.configure(bg='#f5f7fa')

# Colors
PRIMARY_COLOR = '#3498db'
SECONDARY_COLOR = '#2ecc71'
ACCENT_COLOR = '#e74c3c'
BG_COLOR = '#f5f7fa'
CARD_COLOR = '#ffffff'
TEXT_COLOR = '#2c3e50'

main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill='both', expand=True, padx=15, pady=15)

header_frame = tk.Frame(main_frame, bg=PRIMARY_COLOR, height=80)
header_frame.pack(fill='x', pady=(0, 15))
header_frame.pack_propagate(False)

tk.Label(header_frame, text="Student Manager", 
          font=('Arial', 20, 'bold'), 
          bg=PRIMARY_COLOR, fg='white').pack(expand=True)

content_frame = tk.Frame(main_frame, bg=BG_COLOR)
content_frame.pack(fill='both', expand=True)

left_panel = tk.Frame(content_frame, bg=CARD_COLOR, relief=tk.RAISED, bd=1)
left_panel.pack(side='left', fill='y', padx=(0, 15))

right_panel = tk.Frame(content_frame, bg=BG_COLOR)
right_panel.pack(side='right', fill='both', expand=True)

tk.Label(left_panel, text="View Individual Student Record:", 
         font=('Arial', 11, 'bold'), bg=CARD_COLOR, fg=TEXT_COLOR).pack(anchor='w', pady=(15, 5), padx=15)

student_combo = ttk.Combobox(left_panel, width=25, font=('Arial', 10))
student_combo.pack(fill='x', padx=15, pady=(0, 10))
refresh_combo()

tk.Button(left_panel, text="View Record", font=('Arial', 10, 'bold'), 
          bg=PRIMARY_COLOR, fg='white', command=view_individual, width=15).pack(pady=(0, 20))

nav_buttons = [
    ("View All Student Records", view_all, PRIMARY_COLOR),
    ("Show Highest Score", show_highest, SECONDARY_COLOR),
    ("Show Lowest Score", show_lowest, SECONDARY_COLOR),
]

for text, command, color in nav_buttons:
    tk.Button(left_panel, text=text, font=('Arial', 10, 'bold'),
              bg=color, fg='white', command=command, width=20).pack(pady=8, padx=15)

separator = tk.Frame(left_panel, height=2, bg='#e0e0e0')
separator.pack(fill='x', pady=20, padx=10)

edit_buttons = [
    ("Add Student", add_student, SECONDARY_COLOR),
    ("Update Student", update_student, '#f39c12'),
    ("Delete Student", delete_student, ACCENT_COLOR),
    ("Search Student", search_student, PRIMARY_COLOR),
    ("Class Statistics", show_statistics, '#9b59b6'),
    ("Sort Records", sort_records, '#1abc9c'),
]

for text, command, color in edit_buttons:
    tk.Button(left_panel, text=text, font=('Arial', 10),
              bg=color, fg='white', command=command, width=15).pack(pady=5, padx=15)

output_frame = tk.Frame(right_panel, bg=CARD_COLOR, relief=tk.RAISED, bd=1)
output_frame.pack(fill='both', expand=True)

tk.Label(output_frame, text="Student Records", 
          font=('Arial', 12, 'bold'), 
          bg=PRIMARY_COLOR, fg='white').pack(fill='x')

# Output Textbox with Scrollbar
output_box = tk.Text(output_frame, width=60, height=25, wrap=tk.WORD,
                     bg='#fafafa', fg=TEXT_COLOR, font=('Consolas', 10),
                     relief=tk.FLAT, bd=0)
output_box.pack(fill='both', expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(output_frame, command=output_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_box.config(yscrollcommand=scrollbar.set)

# Status Bar
if students:
    avg_percent = sum(s['percent'] for s in students) / len(students)
else:
    avg_percent = 0

status_bar = tk.Label(root, text=f"Total Students: {len(students)} | Average Percentage: {avg_percent:.1f}%", 
                     bg='#34495e', fg='white', font=('Arial', 10), anchor='w')
status_bar.pack(fill='x', side=tk.BOTTOM)

welcome_msg = f"""Welcome to Student Manager

Loaded {len(students)} student records from file.

Use the buttons to:
• View all student records
• Search for specific students
• Add new students
• Update existing records
• Analyze class performance
• Sort and organize data

All changes are automatically saved to file.
"""
show_output(welcome_msg)

root.mainloop()

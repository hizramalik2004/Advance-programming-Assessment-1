import tkinter as tk
from tkinter import ttk, messagebox
import random


class MathQuiz:
    def __init__(self, window):
        self.window = window
        self.window.title("Math Quiz Challenge")
        self.window.geometry("500x450")
        self.window.config(bg="#2C3E50")  # Dark blue background
        self.window.resizable(False, False)
        
        # Center the window on screen
        self.window.eval('tk::PlaceWindow . center')
        
        # Game variables
        self.score = 0
        self.question_count = 0
        self.difficulty_level = 1
        self.attempts = 1
        self.first_number = 0
        self.second_number = 0
        self.math_operator = '+'
        self.correct_answer = 0
        
        self.display_main_menu()

    def display_main_menu(self):
        """Show the main menu with difficulty options"""
        self.clear_screen()
        
        # Main title
        title_label = tk.Label(
            self.window, 
            text="🧮 Math Quiz Challenge", 
            font=('Arial', 22, 'bold'),
            bg="#2C3E50", 
            fg="#E74C3C",
            relief='raised',
            bd=3,
            padx=20,
            pady=10
        )
        title_label.pack(pady=30)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.window, 
            text="Choose Your Difficulty Level", 
            font=('Verdana', 13, 'italic'),
            bg="#2C3E50",
            fg="#F39C12"
        )
        subtitle_label.pack(pady=15)
        
        # Difficulty buttons
        button_style = {'width': 25, 'style': 'Accent.TButton'}
        
        easy_button = ttk.Button(
            self.window, 
            text="🎯 Easy (1-digit numbers)", 
            command=lambda: self.initialize_game(1),
            **button_style
        )
        easy_button.pack(pady=8)
        
        moderate_button = ttk.Button(
            self.window, 
            text="🎯 Moderate (2-digit numbers)", 
            command=lambda: self.initialize_game(2),
            **button_style
        )
        moderate_button.pack(pady=8)
        
        advanced_button = ttk.Button(
            self.window, 
            text="🎯 Advanced (4-digit numbers)", 
            command=lambda: self.initialize_game(3),
            **button_style
        )
        advanced_button.pack(pady=8)
        
        # Exit button
        exit_button = ttk.Button(
            self.window, 
            text="🚪 Exit Game", 
            command=self.window.quit,
            style='Exit.TButton'
        )
        exit_button.pack(pady=25)
        
        # Configure button styles
        style = ttk.Style()
        style.configure('Accent.TButton', 
                       font=('Arial', 11, 'bold'),
                       background='#3498DB',
                       foreground='#2C3E50')
        style.configure('Exit.TButton', 
                       font=('Arial', 11, 'bold'), 
                       foreground='#2C3E50',
                       background='#E74C3C')

    def initialize_game(self, level):
        """Start the game with selected difficulty level"""
        self.difficulty_level = level
        self.score = 0
        self.question_count = 0
        self.display_question()

    def generate_random_numbers(self):
        """Generate random numbers based on difficulty level"""
        if self.difficulty_level == 1:
            min_val, max_val = 1, 9
        elif self.difficulty_level == 2:
            min_val, max_val = 10, 99
        else:
            min_val, max_val = 1000, 9999

        num1 = random.randint(min_val, max_val)
        num2 = random.randint(min_val, max_val)

        # Ensure no negative results for easier levels
        if self.math_operator == '-' and self.difficulty_level < 3 and num1 < num2:
            num1, num2 = num2, num1
            
        return num1, num2

    def get_random_operator(self):
        """Randomly select addition or subtraction operator"""
        return random.choice(['+', '-'])

    def display_question(self):
        """Display the current math question"""
        self.question_count += 1
        self.attempts = 1
        
        # Check if game is complete
        if self.question_count > 10:
            self.show_final_results()
            return

        self.clear_screen()
        
        self.math_operator = self.get_random_operator()
        self.first_number, self.second_number = self.generate_random_numbers()

        # Calculate correct answer
        if self.math_operator == '+':
            self.correct_answer = self.first_number + self.second_number
        else:
            self.correct_answer = self.first_number - self.second_number

        # Progress indicator
        progress_label = tk.Label(
            self.window, 
            text=f"Question {self.question_count} of 10", 
            font=('Georgia', 14, 'bold'),
            bg="#2C3E50", 
            fg="#F39C12",
            relief='groove',
            bd=2,
            padx=15,
            pady=5
        )
        progress_label.pack(pady=15)

        # Math problem display
        self.problem_label = tk.Label(
            self.window, 
            text=f"{self.first_number} {self.math_operator} {self.second_number} = ?",
            font=('Courier New', 20, 'bold'), 
            bg="#E74C3C", 
            fg="#2C3E50",
            relief='raised',
            bd=4,
            padx=30,
            pady=15
        )
        self.problem_label.pack(pady=25)

        # Answer input
        self.user_answer = tk.StringVar()
        answer_entry = ttk.Entry(
            self.window, 
            textvariable=self.user_answer, 
            font=('Arial', 16, 'bold'),
            width=15,
            justify='center',
            style='Entry.TEntry'
        )
        answer_entry.pack(pady=15)
        answer_entry.focus()
        answer_entry.bind("<Return>", lambda event: self.validate_answer())

        # Submit button
        submit_button = ttk.Button(
            self.window, 
            text="✅ Submit Answer", 
            command=self.validate_answer,
            style='Submit.TButton'
        )
        submit_button.pack(pady=10)

        # Navigation buttons
        back_button = ttk.Button(
            self.window, 
            text="↩ Back to Main Menu", 
            command=self.return_to_menu,
            style='Nav.TButton'
        )
        back_button.pack(pady=5)

        # Current score display
        score_label = tk.Label(
            self.window, 
            text=f"Current Score: {self.score}", 
            font=('Trebuchet MS', 13, 'bold'),
            bg="#27AE60", 
            fg="#2C3E50",
            relief='ridge',
            bd=3,
            padx=20,
            pady=8
        )
        score_label.pack(pady=20)
        
        # Configure additional styles
        style = ttk.Style()
        style.configure('Submit.TButton', 
                       font=('Arial', 11, 'bold'),
                       background='#2980B9',
                       foreground='#2C3E50')
        style.configure('Nav.TButton', 
                       font=('Arial', 10),
                       background='#F39C12',
                       foreground='#2C3E50')
        style.configure('Entry.TEntry', 
                       font=('Arial', 16, 'bold'),
                       fieldbackground='#BDC3C7')

    def validate_answer(self):
        """Check if the user's answer is correct"""
        try:
            user_response = int(self.user_answer.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        if user_response == self.correct_answer:
            if self.attempts == 1:
                self.score += 10
                messagebox.showinfo("Correct!", "Perfect! 🎉 +10 points")
            else:
                self.score += 5
                messagebox.showinfo("Correct!", "Good job! 👍 +5 points")
            self.display_question()
        else:
            if self.attempts == 1:
                self.attempts = 2
                messagebox.showwarning("Try Again", "Not quite right! You get one more attempt.")
                self.user_answer.set("")
                self.problem_label.config(
                    text=f"{self.first_number} {self.math_operator} {self.second_number} = ? (Second try)")
            else:
                messagebox.showerror(
                    "Incorrect", 
                    f"Wrong answer! The correct answer was {self.correct_answer}"
                )
                self.display_question()

    def show_final_results(self):
        """Display the final results after completing the quiz"""
        self.clear_screen()
        
        # Results header
        results_title = tk.Label(
            self.window, 
            text="Quiz Completed! 🏆", 
            font=('Impact', 24, 'bold'),
            bg="#E74C3C", 
            fg="#2C3E50",
            relief='raised',
            bd=5,
            padx=30,
            pady=15
        )
        results_title.pack(pady=30)

        # Final score
        score_display = tk.Label(
            self.window, 
            text=f"Final Score: {self.score} / 100",
            font=('Arial Rounded MT Bold', 18, 'bold'), 
            bg="#3498DB",
            fg="#2C3E50",
            relief='groove',
            bd=4,
            padx=25,
            pady=10
        )
        score_display.pack(pady=15)

        # Grade evaluation
        grade = self.calculate_grade()
        grade_label = tk.Label(
            self.window, 
            text=f"Performance: {grade}", 
            font=('Verdana', 16, 'bold'),
            bg="#9B59B6", 
            fg="#2C3E50",
            relief='raised',
            bd=3,
            padx=20,
            pady=8
        )
        grade_label.pack(pady=10)

        # Action buttons
        replay_button = ttk.Button(
            self.window, 
            text="🔄 Play Again", 
            command=self.display_main_menu,
            style='Replay.TButton'
        )
        replay_button.pack(pady=12)

        exit_button = ttk.Button(
            self.window, 
            text="🚪 Exit Game", 
            command=self.window.quit,
            style='Exit.TButton'
        )
        exit_button.pack(pady=8)
        
        # Configure result screen button styles
        style = ttk.Style()
        style.configure('Replay.TButton', 
                       font=('Arial', 12, 'bold'),
                       background='#27AE60',
                       foreground='#2C3E50')
        style.configure('Exit.TButton', 
                       font=('Arial', 12, 'bold'),
                       background='#E74C3C',
                       foreground='#2C3E50')

    def return_to_menu(self):
        """Return to main menu with confirmation"""
        confirm_exit = messagebox.askyesno(
            "Return to Menu", 
            "Are you sure you want to return to the main menu?\nYour current progress will be lost."
        )
        if confirm_exit:
            self.display_main_menu()

    def calculate_grade(self):
        """Calculate performance grade based on score"""
        if self.score >= 90:
            return "A+ Outstanding!"
        elif self.score >= 80:
            return "A  Excellent!"
        elif self.score >= 70:
            return "B  Very Good!"
        elif self.score >= 60:
            return "C  Good Effort"
        elif self.score >= 50:
            return "D  Keep Practicing"
        else:
            return "F  Never Give Up!"

    def clear_screen(self):
        """Clear all widgets from the window"""
        for widget in self.window.winfo_children():
            widget.destroy()


# Launch the application
if __name__ == "__main__":
    root = tk.Tk()
    game_app = MathQuiz(root)
    root.mainloop()
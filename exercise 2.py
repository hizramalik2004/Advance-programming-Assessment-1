import tkinter as tk
from tkinter import scrolledtext
import random

class JokeBoxApp:
    def __init__(self, main_window):
        self.window = main_window
        self.window.title("Joke Box - Your Daily Dose of Laughter")
        self.window.geometry("550x500")
        self.window.configure(bg='#FFF5F5')  # Soft pink background
        
        # Color scheme for the app
        self.app_colors = {
            'primary_bg': '#FFF5F5',
            'header_bg': '#FF6B8B',
            'secondary_bg': '#FFE8E8',
            'accent_color': '#9370DB',
            'accent_hover': '#7B68EE',
            'joke_display_bg': '#FFFFFF',
            'success_color': '#4CAF50',
            'warning_color': '#FF9800'
        }
        
        # Load jokes from file
        self.joke_collection = self.load_jokes_from_file("randomJokes.txt")
        
        # Create main container
        self.main_container = tk.Frame(self.window, bg=self.app_colors['primary_bg'])
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.setup_main_interface()
    
    def load_jokes_from_file(self, filename):
        """Load jokes from text file with error handling"""
        jokes = []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if "?" in line:
                        question, answer = line.split("?", 1)
                        jokes.append((question + "?", answer.strip()))
            print(f"Successfully loaded {len(jokes)} jokes!")
        except FileNotFoundError:
            print(f"Could not find {filename}. Please make sure it exists.")
        except Exception as e:
            print(f"Error reading file: {e}")
        
        return jokes
    
    def create_styled_button(self, parent, text, command, bg_color=None, is_primary=False):
        """Create a styled button with hover effects"""
        button_bg = bg_color if bg_color else self.app_colors['accent_color']
        hover_color = self.app_colors['accent_hover']
        
        button_font = ('Arial', 12, 'bold') if is_primary else ('Arial', 10)
        
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=button_bg,
            fg='white',
            font=button_font,
            relief='raised',
            bd=2,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        
        # Add hover effects
        def on_enter(event):
            button['bg'] = hover_color
            button['relief'] = 'sunken'
        
        def on_leave(event):
            button['bg'] = button_bg
            button['relief'] = 'raised'
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    def setup_main_interface(self):
        """Create the main screen layout"""
        self.clear_interface()
        
        # Main content area
        content_frame = tk.Frame(self.main_container, bg=self.app_colors['primary_bg'])
        content_frame.pack(fill='both', expand=True)
        
        # App header
        header_frame = tk.Frame(content_frame, bg=self.app_colors['header_bg'], relief='flat', bd=0)
        header_frame.pack(fill='x', pady=(0, 20))
        
        header_label = tk.Label(header_frame, 
                              text="😂 Joke Box - Spread Smiles! 😂", 
                              font=('Comic Sans MS', 20, 'bold'),
                              bg=self.app_colors['header_bg'],
                              fg='white',
                              pady=15)
        header_label.pack()
        
        # Welcome message
        welcome_frame = tk.Frame(content_frame, bg=self.app_colors['secondary_bg'], relief='flat')
        welcome_frame.pack(fill='x', pady=10)
        
        welcome_label = tk.Label(welcome_frame, 
                               text="Ready for some laughter? Click below to get a random joke!",
                               font=('Arial', 11, 'italic'),
                               bg=self.app_colors['secondary_bg'],
                               fg='#D32F2F',
                               pady=8)
        welcome_label.pack()
        
        # Joke display area
        display_frame = tk.Frame(content_frame, bg='#E3F2FD', relief='groove', bd=2)
        display_frame.pack(fill='both', expand=True, pady=15)
        
        self.joke_display = scrolledtext.ScrolledText(
            display_frame, 
            height=8, 
            width=60,
            font=('Arial', 11),
            wrap=tk.WORD,
            bg=self.app_colors['joke_display_bg'],
            fg='#2C3E50',
            relief='flat',
            padx=10,
            pady=10
        )
        self.joke_display.pack(fill='both', expand=True, padx=3, pady=3)
        self.joke_display.config(state='normal')
        
        # Main action button
        button_frame = tk.Frame(content_frame, bg=self.app_colors['primary_bg'])
        button_frame.pack(pady=15)
        
        joke_button = self.create_styled_button(
            button_frame, 
            "🎭 Tell Me a Joke! 🎭",
            self.display_random_joke,
            bg_color='#FF4081',
            is_primary=True
        )
        joke_button.pack(pady=8)
        
        # Footer with exit
        footer_frame = tk.Frame(content_frame, bg=self.app_colors['primary_bg'])
        footer_frame.pack(pady=10)
        
        exit_button = self.create_styled_button(
            footer_frame, 
            "Exit Application", 
            self.window.quit,
            bg_color='#757575'
        )
        exit_button.pack()
        
        # Display initial welcome message
        self.update_display("Welcome to Joke Box! 🤗\n\nI'm your friendly joke teller, here to brighten your day with some humor.\n\nClick the 'Tell Me a Joke!' button above to get started and let's spread some laughter together! 😄")
    
    def display_random_joke(self):
        """Select and display a random joke"""
        if not self.joke_collection:
            self.update_display("Oops! I couldn't find any jokes. 😕\n\nPlease make sure the 'randomJokes.txt' file is in the same directory as this application.\n\nThe file should contain jokes in the format: 'Question? Answer'")
            return
        
        selected_joke = random.choice(self.joke_collection)
        self.show_joke_question(selected_joke[0], selected_joke[1])
    
    def show_joke_question(self, question, answer):
        """Display the joke setup screen"""
        self.clear_interface()
        
        # Content container
        content_frame = tk.Frame(self.main_container, bg='#E8F5E8')
        content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header
        header_frame = tk.Frame(content_frame, bg='#4CAF50', relief='flat')
        header_frame.pack(fill='x', pady=(0, 20))
        
        header_label = tk.Label(header_frame, 
                              text="Get Ready to Smile! 😊", 
                              font=('Comic Sans MS', 18, 'bold'),
                              bg='#4CAF50',
                              fg='white',
                              pady=12)
        header_label.pack()
        
        # Joke question display
        question_frame = tk.Frame(content_frame, bg='#81C784', relief='ridge', bd=2)
        question_frame.pack(fill='x', pady=20, padx=10)
        
        question_label = tk.Label(question_frame, 
                                text=question, 
                                font=('Arial', 13, 'italic'),
                                wraplength=500,
                                bg='#81C784',
                                fg='white',
                                pady=20,
                                padx=15)
        question_label.pack()
        
        # Action buttons
        button_frame = tk.Frame(content_frame, bg='#E8F5E8')
        button_frame.pack(pady=20)
        
        reveal_button = self.create_styled_button(
            button_frame, 
            "🤔 Show Me the Punchline! 🤔",
            lambda: self.show_complete_joke(question, answer),
            bg_color='#FF5722',
            is_primary=True
        )
        reveal_button.pack(pady=10)
        
        back_button = self.create_styled_button(
            button_frame, 
            "← Back to Main Menu", 
            self.setup_main_interface,
            bg_color='#607D8B'
        )
        back_button.pack(pady=5)
    
    def show_complete_joke(self, question, answer):
        """Display the complete joke with punchline"""
        self.clear_interface()
        
        # Content container
        content_frame = tk.Frame(self.main_container, bg='#FFF3E0')
        content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Success header
        header_frame = tk.Frame(content_frame, bg='#FF9800', relief='flat')
        header_frame.pack(fill='x', pady=(0, 20))
        
        header_label = tk.Label(header_frame, 
                              text="Here's the Punchline! 🎉", 
                              font=('Comic Sans MS', 18, 'bold'),
                              bg='#FF9800',
                              fg='white',
                              pady=12)
        header_label.pack()
        
        # Complete joke display
        joke_frame = tk.Frame(content_frame, bg='#FFB74D', relief='ridge', bd=3)
        joke_frame.pack(fill='both', expand=True, pady=20, padx=10)
        
        complete_joke = f"❓ {question}\n\n" + "―" * 50 + f"\n\n💡 {answer}"
        
        joke_label = tk.Label(joke_frame, 
                             text=complete_joke,
                             font=('Arial', 12),
                             wraplength=480,
                             justify=tk.CENTER,
                             bg='#FFB74D',
                             fg='#37474F',
                             pady=30,
                             padx=20)
        joke_label.pack(expand=True)
        
        # Navigation buttons
        button_frame = tk.Frame(content_frame, bg='#FFF3E0')
        button_frame.pack(pady=20)
        
        another_joke_button = self.create_styled_button(
            button_frame, 
            "🔄 Get Another Joke",
            self.display_random_joke,
            bg_color='#2196F3'
        )
        another_joke_button.pack(pady=8)
        
        main_menu_button = self.create_styled_button(
            button_frame, 
            "🏠 Return to Main Menu", 
            self.setup_main_interface,
            bg_color='#795548'
        )
        main_menu_button.pack(pady=5)
    
    def update_display(self, message):
        """Safely update the text display area"""
        if hasattr(self, 'joke_display') and self.joke_display.winfo_exists():
            self.joke_display.config(state='normal')
            self.joke_display.delete(1.0, tk.END)
            self.joke_display.insert(1.0, message)
            self.joke_display.config(state='disabled')
    
    def clear_interface(self):
        """Clear all widgets from the main container"""
        for widget in self.main_container.winfo_children():
            widget.destroy()

# Launch the application
if __name__ == "__main__":
    root = tk.Tk()
    app = JokeBoxApp(root)
    root.mainloop()
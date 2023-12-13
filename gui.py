import tkinter as tk
from tkinter import messagebox
from main import NumberNode, BinOpNode, run

# Constants for circle size and spacing
RADIUS = 30
SPACING = 80

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Parse Tree Login")
        self.geometry('640x440')
        self.configure(bg='#333333')

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self, bg='#333333')
        frame.pack()

        login_label = tk.Label(frame, text="Login", bg='#333333', fg="#1AA260", font=("Arial", 30))
        login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)

        username_label = tk.Label(frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
        username_label.grid(row=1, column=0)

        self.username_entry = tk.Entry(frame, font=("Arial", 16))
        self.username_entry.grid(row=1, column=1, pady=20)

        password_label = tk.Label(frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
        password_label.grid(row=2, column=0)

        self.password_entry = tk.Entry(frame, show="*", font=("Arial", 16))
        self.password_entry.grid(row=2, column=1, pady=20)

        login_button = tk.Button(frame, text="Login", bg='#1AA260', fg="#FFFFFF", font=("Arial", 16),
                                 command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=30)

    def login(self):
        username = 'Bob'
        password = '12345'

        if self.username_entry.get() == username and self.password_entry.get() == password:
            messagebox.showinfo(title="Login Success", message="Successfully logged in.")
            self.destroy()

            self.open_new_label()
        else:
            messagebox.showerror(title="Login Declined", message="Invalid password or username. Try again.")

    def open_new_label(self):
        new_window = ParseTreeGUI()
        new_window.show()

class ParseTreeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Parse Tree GUI")
        self.geometry('1920x1080')
        self.configure(bg='#333333')

        self.create_widgets()
        self.current_theme = 'dark'
        self.configure_theme()

    def create_widgets(self):
        self.frame = tk.Frame(self, bg='#333333')
        self.frame.pack()

        self.text_label = tk.Label(self.frame, text="Enter Expression:", bg='#333333', fg="#1AA260", font=("Arial", 20))
        self.text_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=5)

        self.text_entry = tk.Text(self.frame, height=2, width=40, bg='white')
        self.text_entry.grid(row=1, column=0, columnspan=2, pady=10)

        parse_button = tk.Button(self.frame, text="Parse", command=self.run_visualization, bg="#1AA260", fg="#FFFFFF",
                                 font=("Arial", 16), relief="solid", bd=0, width=10, height=1)
        parse_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.canvas = tk.Canvas(self, bg='#333333', highlightthickness=0, width=800, height=600)
        self.canvas.pack()

        self.toggle_theme_button = tk.Button(self, text="Toggle Theme", command=self.toggle_theme, bg='#1AA260', fg="#FFFFFF",
                                             font=("Arial", 12), relief="solid", bd=0)
        self.toggle_theme_button.place(relx=0.95, rely=0.05, anchor='ne')

    def run_visualization(self):
        expression = self.text_entry.get("1.0", "end-1c")
        #get the text from the first character of the first line to
        # the last character of the last line, excluding the trailing newline character.

        ast, error = run(expression)
        if error:
            messagebox.showerror(title="Error", message=error.as_string())
            return

        self.canvas.delete("all")
        self.create_parse_tree_visual(ast, 400, 50, self.canvas)

    def create_parse_tree_visual(self, node, x, y, canvas, depth=20):
        if depth == 0 or node is None:
            return

        if isinstance(node, NumberNode):
            # Draw a circle for the number node
            canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill="#1AA260")
            canvas.create_text(x, y, text=str(node.tok.value))
        elif isinstance(node, BinOpNode):
            # Calculate the x and y coordinates for the operator node
            operator_x = x
            operator_y = y

            # Recursively create the visual representation for the left child node
            self.create_parse_tree_visual(node.left_node, x - SPACING, y + SPACING, canvas, depth - 1)



            # Draw line connecting the operator node to its left child
            canvas.create_line(operator_x, operator_y + RADIUS, x - SPACING, y + SPACING - RADIUS, fill="black")

            # Recursively create the visual representation for the right child node
            self.create_parse_tree_visual(node.right_node, x + SPACING, y + SPACING, canvas, depth - 1)

            # Draw line connecting the operator node to its right child
            canvas.create_line(operator_x, operator_y + RADIUS, x + SPACING, y + SPACING - RADIUS, fill="black")

            # Draw a circle for the operator node
            canvas.create_oval(operator_x - RADIUS, operator_y - RADIUS, operator_x + RADIUS, operator_y + RADIUS,
                               fill="orange")
            canvas.create_text(operator_x, operator_y, text=str(node.op_tok.type))

    def toggle_theme(self):
        if self.current_theme == 'dark':
            self.current_theme = 'light'
        else:
            self.current_theme = 'dark'

        self.configure_theme()

    def configure_theme(self):
        if self.current_theme == 'dark':
            self.configure(bg='#333333')
            self.canvas.configure(bg='#333333')
            self.frame.configure(bg='#333333')
            self.toggle_theme_button.configure(bg='#1AA260', fg='#FFFFFF')
            self.text_label.configure(bg='#333333', fg='#1AA260')
        else:
            self.configure(bg='#F0F0F0')
            self.canvas.configure(bg='#F0F0F0')
            self.frame.configure(bg='#F0F0F0')
            self.toggle_theme_button.configure(bg='#1AA260', fg='#FFFFFF')
            self.text_label.configure(bg='#F0F0F0', fg='#1AA260')

    def show(self):
        self.mainloop()

def run_application():
    login_window = LoginWindow()
    login_window.mainloop()

if __name__ == "__main__":
    run_application()

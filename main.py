import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class TodoListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List App")

        # Initialize task list
        self.tasks = []

        # Load tasks from file
        self.load_tasks()

        # Task Entry
        self.task_entry = ttk.Entry(master, width=40, font=("Helvetica", 12))
        self.task_entry.grid(row=0, column=0, padx=10, pady=5, columnspan=2, sticky="ew")

        # Date Entry
        self.date_label = ttk.Label(master, text="Due Date (MM/DD/YY hh:mm AM/PM):", font=("Helvetica", 12))
        self.date_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.date_entry = ttk.Entry(master, width=30, font=("Helvetica", 12))
        self.date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Add Button
        self.add_button = ttk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        # Remove Button
        self.remove_button = ttk.Button(master, text="Remove Task", command=self.remove_task)
        self.remove_button.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        # Task Listbox
        self.task_listbox = tk.Listbox(master, width=50, height=15, font=("Helvetica", 12))
        self.task_listbox.grid(row=2, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")

        # Populate listbox with tasks
        self.populate_task_listbox()

        # Configure grid weights
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=1)

        # Schedule the due date checking function to run periodically
        self.master.after(1000, self.check_due_dates)

        # Center the window on the screen
        self.center_window()

        # Save tasks when closing the window
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_task(self):
        task = self.task_entry.get()
        date = self.date_entry.get()
        if task:
            if date:
                try:
                    # Attempt to parse the date string
                    due_date = datetime.strptime(date, "%m/%d/%y %I:%M %p")
                    if due_date < datetime.now():
                        messagebox.showwarning("Warning", "Due date must be in the future.")
                        return
                    task_with_date = f"{task} (Due: {due_date.strftime('%m/%d/%y %I:%M %p')})"
                except ValueError:
                    messagebox.showwarning("Warning", "Invalid date format. Please use MM/DD/YY hh:mm AM/PM.")
                    return
            else:
                task_with_date = task
            self.tasks.append(task_with_date)
            self.task_listbox.insert(tk.END, task_with_date)
            self.task_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            # Save tasks to file
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            task = self.tasks.pop(task_index)
            self.task_listbox.delete(task_index)
            messagebox.showinfo("Success", f'Task "{task}" removed.')
            # Save tasks to file
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def check_due_dates(self):
        current_date = datetime.now().date()
        for task in self.tasks:
            if "(Due: " in task:
                due_date_str = task.split("(Due: ")[1].split(")")[0]
                due_date = datetime.strptime(due_date_str, "%m/%d/%y %I:%M %p").date()
                if due_date == current_date:
                    self.show_due_date_message(task)
        # Schedule the next due date checking
        self.master.after(86400000, self.check_due_dates)  # Check every day (24 hours)

    def show_due_date_message(self, task):
        messagebox.showinfo("Reminder", f"Task '{task}' is due today!")

    def center_window(self):
        # Center the window on the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.master.geometry(f"+{x}+{y}")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                self.tasks = file.readlines()
        except FileNotFoundError:
            # If the file doesn't exist, do nothing
            pass

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(task + "\n")

    def populate_task_listbox(self):
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task.strip())

    def on_closing(self):
        # Save tasks before closing the window
        self.save_tasks()
        self.master.destroy()

def main():
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()





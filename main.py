import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Log Viewer")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # Big title
        self.title_label = tk.Label(self.root, text="Log Viewer", font=("Helvetica", 24, "bold"), fg="#2c3e50", bg="#f0f0f0")
        self.title_label.pack(pady=20)

        # Customize label and button
        self.label = tk.Label(self.root, text="Select a CSV file:", font=("Helvetica", 14), fg="#34495e", bg="#f0f0f0")
        self.label.pack(pady=10)

        self.button = tk.Button(self.root, text="Browse...", command=self.load_file, font=("Helvetica", 12), bg="#3498db", fg="white", relief="raised")
        self.button.pack(pady=10)

        self.dropdown_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.dropdown_frame.pack(pady=10)

        self.selected_columns = tk.StringVar(value=[])
        self.dropdown = ttk.Combobox(self.dropdown_frame, textvariable=self.selected_columns, font=("Helvetica", 12))
        self.dropdown.pack(side=tk.LEFT, padx=10, pady=10)

        self.add_button = tk.Button(self.dropdown_frame, text="Add", command=self.add_selection, font=("Helvetica", 12), bg="#2ecc71", fg="white", relief="raised")
        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.remove_button = tk.Button(self.dropdown_frame, text="Remove", command=self.remove_selection, font=("Helvetica", 12), bg="#e74c3c", fg="white", relief="raised")
        self.remove_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.plot_button = tk.Button(self.root, text="Plot Selected Data", command=self.plot_data, bg="#f39c12", fg="white", font=("Helvetica", 12), relief="raised")
        self.plot_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save Graph as Image", command=self.save_graph, bg="#9b59b6", fg="white", font=("Helvetica", 12), relief="raised")
        self.save_button.pack(pady=10)

        self.figure = plt.Figure(figsize=(10, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack(padx=10, pady=10)

        self.df = None
        self.selected_columns_list = []
        self.filename = ""  # To store the name of the loaded file

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            self.filename = file_path.split("/")[-1]  # Extract the filename from the path
            self.update_dropdown(self.df)

    def update_dropdown(self, df):
        self.dropdown['values'] = df.columns.tolist()

    def add_selection(self):
        selection = self.selected_columns.get()
        if selection and selection not in self.selected_columns_list:
            self.selected_columns_list.append(selection)
            self.dropdown.set('')
            self.plot_data()

    def remove_selection(self):
        selection = self.selected_columns.get()
        if selection in self.selected_columns_list:
            self.selected_columns_list.remove(selection)
            self.dropdown.set('')
            self.plot_data()
        else:
            messagebox.showwarning("Not Selected", "Please select a parameter to remove.")

    def plot_data(self):
        self.ax.clear()
        if not self.selected_columns_list:
            messagebox.showwarning("No Selection", "Please select at least one parameter to plot.")
            return

        for col in self.selected_columns_list:
            self.ax.plot(self.df.index, self.df[col], label=col)

        # Set the title to the filename
        self.ax.set_title(f"{self.filename}", fontsize=16)
        self.ax.legend()
        self.canvas.draw()

    def save_graph(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.figure.savefig(file_path)
            messagebox.showinfo("Save Successful", f"Graph saved as {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataViewerApp(root)
    root.mainloop()


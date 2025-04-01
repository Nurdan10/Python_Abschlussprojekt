import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import plotly.express as px
import webbrowser


class PlotWindow:
    def __init__(self, root, csv_file):
        self.root = root
        self.root.title("Data Visualization App")
        self.df = pd.read_csv(csv_file)

        self.create_layout()

    def create_layout(self):
        # Main window layout using PanedWindow
        self.pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.pane.pack(fill=tk.BOTH, expand=True)

        # Navigator Frame
        self.nav_frame = tk.Frame(self.pane, width=250, bg="lightgray")
        self.pane.add(self.nav_frame)

        # Visualization Frame (Placeholder)
        self.vis_frame = tk.Frame(self.pane, width=600, bg="white")
        self.pane.add(self.vis_frame)

        self.create_widgets()

    def create_widgets(self):
        # Dropdown for Plot Type
        self.plot_types = ["Bar", "Pie", "Box", "Histogram"]
        self.selected_plot = tk.StringVar(value=self.plot_types[0])
        ttk.Label(self.nav_frame, text="Select Plot Type:").pack(pady=5)
        self.plot_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_plot, values=self.plot_types)
        self.plot_dropdown.pack(pady=5)

        # Dropdown for First Column (Categorical or Numeric)
        self.columns = self.df.columns.tolist()
        self.selected_col1 = tk.StringVar(value=self.columns[0])
        ttk.Label(self.nav_frame, text="Select First Column:").pack(pady=5)
        self.col_dropdown1 = ttk.Combobox(self.nav_frame, textvariable=self.selected_col1, values=self.columns)
        self.col_dropdown1.pack(pady=5)

        # Dropdown for Second Column (Categorical or Numeric)
        self.selected_col2 = tk.StringVar(value=self.columns[1])
        ttk.Label(self.nav_frame, text="Select Second Column:").pack(pady=5)
        self.col_dropdown2 = ttk.Combobox(self.nav_frame, textvariable=self.selected_col2, values=self.columns)
        self.col_dropdown2.pack(pady=5)

        # Button to plot
        self.plot_button = ttk.Button(self.nav_frame, text="Plot", command=self.plot_graph)
        self.plot_button.pack(pady=5)

        # Checkbutton
        self.show_grid = tk.BooleanVar()
        self.grid_check = ttk.Checkbutton(self.nav_frame, text="Show Grid", variable=self.show_grid)
        self.grid_check.pack(pady=5)

        # Button to open message box
        self.info_button = ttk.Button(self.nav_frame, text="Info", command=self.show_message)
        self.info_button.pack(pady=5)

        # Quit button
        self.quit_button = ttk.Button(self.nav_frame, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=5)

    def plot_graph(self):
        plot_type = self.selected_plot.get()
        col1 = self.selected_col1.get()
        col2 = self.selected_col2.get()

        is_col1_numeric = pd.api.types.is_numeric_dtype(self.df[col1])
        is_col2_numeric = pd.api.types.is_numeric_dtype(self.df[col2])

        # Validate column selection based on plot type
        if plot_type in ["Bar", "Pie"] and (is_col1_numeric and is_col2_numeric):
            messagebox.showerror("Error", "Bar and Pie charts require at least one categorical column!")
            return
        elif plot_type in ["Box", "Histogram"] and not is_col1_numeric:
            messagebox.showerror("Error", "Box and Histogram plots require a numeric column!")
            return

        self.plot_handler = PlotHandler(self.df, plot_type, col1, col2)
        self.plot_handler.generate_plot()

    def show_message(self):
        MessageBoxHandler(self.df)


class PlotHandler:
    def __init__(self, df, plot_type, col1, col2):
        self.df = df
        self.plot_type = plot_type
        self.col1 = col1
        self.col2 = col2

    def generate_plot(self):
        if self.plot_type == "bar":
            fig = px.bar(self.df, x=self.col1, color=self.col2)
        elif self.plot_type == "pie":
            fig = px.pie(self.df, names=self.col1, title=f"Distribution of {self.col1}")
        elif self.plot_type == "box":
            fig = px.box(self.df, x=self.col2, y=self.col1, points="all")
        elif self.plot_type == "histogram":
            fig = px.histogram(self.df, x=self.col1, color=self.col2)
        else:
            messagebox.showerror("Error", "Invalid plot type selected!")
            return

        fig.write_html("plot.html")  # Save the plot as an HTML file
        webbrowser.open("plot.html")  # Open the plot in a web browser


class MessageBoxHandler:
    def __init__(self, df):
        self.df = df
        self.show_info()

    def show_info(self):
        info_text = f"Dataset Info:\nRows: {self.df.shape[0]}\nColumns: {self.df.shape[1]}\nMissing Values: {self.df.isnull().sum().sum()}"
        messagebox.showinfo("Dataset Information", info_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = PlotWindow(root, "adult_eda.csv")
    root.mainloop()

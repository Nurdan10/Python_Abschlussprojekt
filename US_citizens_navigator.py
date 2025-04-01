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
        self.nav_frame = tk.Frame(self.pane, width=200, bg="lightgray")
        self.pane.add(self.nav_frame)

        # Visualization Frame (Placeholder)
        self.vis_frame = tk.Frame(self.pane, width=600, bg="white")
        self.pane.add(self.vis_frame)

        self.create_widgets()

    def create_widgets(self):
        # Dropdown for Plot Type
        self.plot_types = ["Histogram", "Box", "Pie", "Bar", "Line"]
        self.selected_plot = tk.StringVar(value=self.plot_types[0])
        ttk.Label(self.nav_frame, text="Select Plot Type:").pack(pady=5)
        self.plot_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_plot, values=self.plot_types)
        self.plot_dropdown.pack(pady=5)

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
        if plot_type == "Histogram":
            self.plot_handler = PlotHandler(self.df, "histogram")
        elif plot_type == "Box":
            self.plot_handler = PlotHandler(self.df, "box")
        elif plot_type == "Pie":
            self.plot_handler = PlotHandler(self.df, "pie")
        elif plot_type == "Bar":
            self.plot_handler = PlotHandler(self.df, "bar")
        elif plot_type == "Line":
            self.plot_handler = PlotHandler(self.df, "line")
        else:
            messagebox.showerror("Error", "Invalid plot type selected!")
            return

        self.plot_handler.generate_plot()

    def show_message(self):
        MessageBoxHandler(self.df)


class PlotHandler:
    def __init__(self, df, plot_type):
        self.df = df
        self.plot_type = plot_type

    def generate_plot(self):
        if self.plot_type == "histogram":
            fig = px.histogram(self.df, x=self.df.columns[0])
        elif self.plot_type == "box":
            fig = px.box(self.df, x=self.df.columns[0])
        elif self.plot_type == "pie":
            if len(self.df[self.df.columns[0]].unique()) > 10:
                messagebox.showwarning("Warning", "Too many unique values for a pie chart!")
                return
            fig = px.pie(self.df, names=self.df.columns[0])
        elif self.plot_type == "bar":
            fig = px.bar(self.df, x=self.df.columns[0], y=self.df.columns[1])
        elif self.plot_type == "line":
            fig = px.line(self.df, x=self.df.columns[0], y=self.df.columns[1])
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

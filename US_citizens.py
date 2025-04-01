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

        self.create_widgets()

    def create_widgets(self):
        # Dropdown for Plot Type
        self.plot_types = ["Histogram", "Box", "Pie", "Bar", "Line"]
        self.selected_plot = tk.StringVar(value=self.plot_types[0])
        ttk.Label(self.root, text="Select Plot Type:").pack()
        self.plot_dropdown = ttk.Combobox(self.root, textvariable=self.selected_plot, values=self.plot_types)
        self.plot_dropdown.pack()

        # Button to plot
        self.plot_button = ttk.Button(self.root, text="Plot", command=self.plot_graph)
        self.plot_button.pack()

        # Checkbutton
        self.show_grid = tk.BooleanVar()
        self.grid_check = ttk.Checkbutton(self.root, text="Show Grid", variable=self.show_grid)
        self.grid_check.pack()

        # Button to open message box
        self.info_button = ttk.Button(self.root, text="Info", command=self.show_message)
        self.info_button.pack()

        # Quit button
        self.quit_button = ttk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack()

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

        fig.show()


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

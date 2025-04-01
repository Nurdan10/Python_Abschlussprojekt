import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import webbrowser


def mapping_education(x):
    if x in ["Preschool", "1st-4th", "5th-6th", "7th-8th", "9th", "10th", "11th", "12th"]:
        return "low_level_grade"
    elif x in ["HS-grad", "Some-college", "Assoc-voc", "Assoc-acdm"]:
        return "medium_level_grade"
    elif x in ["Bachelors", "Masters", "Prof-school", "Doctorate"]:
        return "high_level_grade"
    return None

class PlotWindow:
    def __init__(self, root, csv_file):
        self.root = root
        self.root.title("Data Visualization App")
        self.df = pd.read_csv(csv_file)
        self.df["education_level"] = self.df["education"].apply(mapping_education)
        
        self.create_layout()

    def create_layout(self):
        self.pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.pane.pack(fill=tk.BOTH, expand=True)

        self.nav_frame = tk.Frame(self.pane, width=250, bg="lightgray")
        self.pane.add(self.nav_frame)

        self.vis_frame = tk.Frame(self.pane, width=600, bg="white")
        self.pane.add(self.vis_frame)

        self.create_widgets()

    def create_widgets(self):
        self.plot_types = ["Bar", "Pie", "Histogram", "Line", "Box", "Scatter"]
        self.selected_plot = tk.StringVar(value=self.plot_types[0])
        ttk.Label(self.nav_frame, text="Select Plot Type:").pack(pady=5)
        self.plot_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_plot, values=self.plot_types)
        self.plot_dropdown.pack(pady=5)
        self.plot_dropdown.bind("<<ComboboxSelected>>", self.update_column_dropdown)

        self.all_columns = self.df.columns.tolist()
        self.all_columns_with_dash = self.all_columns + ["---"]
        self.selected_col1 = tk.StringVar(value=self.all_columns[0])
        ttk.Label(self.nav_frame, text="Select First Column:").pack(pady=5)
        self.col1_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_col1, values=self.all_columns)
        self.col1_dropdown.pack(pady=5)

        self.selected_col2 = tk.StringVar(value=self.all_columns_with_dash[0])
        ttk.Label(self.nav_frame, text="Select Second Column:").pack(pady=5)
        self.col2_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_col2, values=self.all_columns_with_dash)
        self.col2_dropdown.pack(pady=5)

        # Radio Buttons for Plotting Libraries
        self.selected_lib = tk.StringVar(value="plotly")  # Default is plotly
        ttk.Label(self.nav_frame, text="Select Plotting Library:").pack(pady=5)
        plotly_radio = ttk.Radiobutton(self.nav_frame, text="Plotly", variable=self.selected_lib, value="plotly")
        plotly_radio.pack(pady=5)
        matplotlib_radio = ttk.Radiobutton(self.nav_frame, text="Matplotlib", variable=self.selected_lib, value="matplotlib")
        matplotlib_radio.pack(pady=5)
        seaborn_radio = ttk.Radiobutton(self.nav_frame, text="Seaborn", variable=self.selected_lib, value="seaborn")
        seaborn_radio.pack(pady=5)

        # Button to plot
        self.plot_button = ttk.Button(self.nav_frame, text="Plot", command=self.plot_graph)
        self.plot_button.pack(pady=5)

        # Checkbutton for Grid Option
        self.show_grid = tk.BooleanVar()
        self.grid_check = ttk.Checkbutton(self.nav_frame, text="Show Grid", variable=self.show_grid)
        self.grid_check.pack(pady=5)

        # Button to open message box
        self.info_button = ttk.Button(self.nav_frame, text="Info", command=self.show_message)
        self.info_button.pack(pady=5)

        # Quit button
        self.quit_button = ttk.Button(self.nav_frame, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=5)

    def update_column_dropdown(self, event=None):
        plot_type = self.selected_plot.get()

        if plot_type in ["Bar", "Pie"]:
            self.col1_dropdown.config(values=self.df.select_dtypes(include=['object']).columns.tolist())
            self.col2_dropdown.config(values=self.df.select_dtypes(include=['object']).columns.tolist() + ["---"])
        else:
            self.col1_dropdown.config(values=self.df.columns.tolist())
            self.col2_dropdown.config(values=self.df.columns.tolist() + ["---"])

    def plot_graph(self):
        plot_type = self.selected_plot.get()
        col1 = self.selected_col1.get()
        col2 = self.selected_col2.get()

        if plot_type == "Bar" and not (self.df[col1].dtype == 'object' and (self.df[col2].dtype == 'object' or col2 == "---")):
            messagebox.showwarning("Warning", "For Bar charts, both columns should be categorical!")
            return
        elif plot_type == "Pie" and not (self.df[col1].dtype == 'object'):
            messagebox.showwarning("Warning", "For Pie charts, the first column should be categorical!")
            return
        elif plot_type == "Histogram" and not (self.df[col1].dtype in ['float64', 'int64']):
            messagebox.showwarning("Warning", "For Histogram, the first column should be numerical!")
            return
        elif plot_type == "Line" and not (self.df[col1].dtype in ['float64', 'int64'] and self.df[col2].dtype in ['float64', 'int64']):
            messagebox.showwarning("Warning", "For Line charts, both columns should be numerical!")
            return
        elif plot_type == "Scatter" and not (self.df[col1].dtype in ['float64', 'int64'] and self.df[col2].dtype in ['float64', 'int64']):
            messagebox.showwarning("Warning", "For Scatter plots, both columns should be numerical!")
            return
        elif plot_type == "Box" and not (self.df[col2].dtype in ['float64', 'int64']):
            messagebox.showwarning("Warning", "For Box plots, the second column should be numerical!")
            return

        if self.df[col1].nunique() > 50 and plot_type in ["Bar", "Pie"]:
            messagebox.showwarning("Warning", "The selected plot type may not be suitable due to too many unique values!")

        plot_lib = self.selected_lib.get()

        if plot_lib == "plotly":
            self.plot_handler = PlotHandler(self.df, "plotly", plot_type, col1, col2)
        elif plot_lib == "matplotlib":
            self.plot_handler = PlotHandler(self.df, "matplotlib", plot_type, col1, col2)
        elif plot_lib == "seaborn":
            self.plot_handler = PlotHandler(self.df, "seaborn", plot_type, col1, col2)
        else:
            messagebox.showerror("Error", "Invalid plot library selected!")
            return

        self.plot_handler.generate_plot()

    def show_message(self):
        MessageBoxHandler(self.df)


class PlotHandler:
    def __init__(self, df, lib, plot_type, col1, col2):
        self.df = df
        self.lib = lib
        self.plot_type = plot_type
        self.col1 = col1
        self.col2 = col2

    def generate_plot(self):
        if self.lib == "plotly":
            self._plotly_plot()
        elif self.lib == "matplotlib":
            self._matplotlib_plot()
        elif self.lib == "seaborn":
            self._seaborn_plot()

    def _plotly_plot(self):
        if self.plot_type == "bar":
            if self.col2 == "---":
                count_df = self.df[self.col1].value_counts().reset_index(name="Count")
                fig = px.bar(count_df, x="index", y="Count")
            else:
                count_df = self.df.groupby([self.col1, self.col2]).size().reset_index(name="Count")
                fig = px.bar(count_df, x=self.col1, y="Count", color=self.col2, barmode="group")
        elif self.plot_type == "pie":
            if self.col2 == "---":
                count_df = self.df[self.col1].value_counts().reset_index(name="Count")
                fig = px.pie(count_df, names="index", values="Count")
            else:
                count_df = self.df.groupby([self.col1, self.col2]).size().reset_index(name="Count")
                fig = px.pie(count_df, names=self.col1, color=self.col2, values="Count")
        elif self.plot_type == "histogram":
            fig = px.histogram(self.df, x=self.col1)
        elif self.plot_type == "line":
            fig = px.line(self.df, x=self.col1, y=self.col2)
        elif self.plot_type == "box":
            fig = px.box(self.df, x=self.col1, y=self.col2)
        elif self.plot_type == "scatter":
            fig = px.scatter(self.df, x=self.col1, y=self.col2)
        else:
            messagebox.showerror("Error", "Invalid plot type selected!")
            return

        fig.write_html("plot.html")
        webbrowser.open("plot.html")

    def _matplotlib_plot(self):
        if self.plot_type == "bar":
            if self.col2 == "---":
                self.df[self.col1].value_counts().plot(kind="bar")
            else:
                self.df.groupby([self.col1, self.col2]).size().unstack().plot(kind="bar", stacked=True)
        elif self.plot_type == "pie":
            if self.col2 == "---":
                self.df[self.col1].value_counts().plot(kind="pie", autopct="%.2f%%")
            else:
                self.df.groupby([self.col1, self.col2]).size().unstack().plot(kind="pie", autopct="%.2f%%")
        elif self.plot_type == "histogram":
            self.df[self.col1].plot(kind="hist")
        elif self.plot_type == "line":
            self.df.plot(kind="line", x=self.col1, y=self.col2)
        elif self.plot_type == "box":
            self.df.boxplot(column=self.col2, by=self.col1)
        elif self.plot_type == "scatter":
            self.df.plot(kind="scatter", x=self.col1, y=self.col2)
        plt.show()

    def _seaborn_plot(self):
        if self.plot_type == "bar":
            if self.col2 == "---":
                sns.countplot(x=self.col1, data=self.df)
            else:
                sns.countplot(x=self.col1, hue=self.col2, data=self.df)
        elif self.plot_type == "pie":
            if self.col2 == "---":
                sns.countplot(x=self.col1, data=self.df)
            else:
                sns.countplot(x=self.col1, hue=self.col2, data=self.df)
        elif self.plot_type == "histogram":
            sns.histplot(self.df[self.col1])
        elif self.plot_type == "line":
            sns.lineplot(x=self.col1, y=self.col2, data=self.df)
        elif self.plot_type == "box":
            sns.boxplot(x=self.col1, y=self.col2, data=self.df)
        elif self.plot_type == "scatter":
            sns.scatterplot(x=self.col1, y=self.col2, data=self.df)
        plt.show()


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

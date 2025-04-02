import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import webbrowser

def mapping_education(x):
    if x in ["Preschool", "1st-4th", "5th-6th", "7th-8th", "9th", "10th", "11th", "12th"]:
        return "low_level_grade"
    elif x in ["HS-grad", "Some-college", "Assoc-voc", "Assoc-acdm"]:
        return "medium_level_grade"
    elif x in ["Bachelors", "Masters", "Prof-school", "Doctorate"]:
        return "high_level_grade"
    return None

def setup_styles():
    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12, "bold"), foreground="#1565c0", background="#e3f2fd")
    style.configure("Soft.TButton", padding=6, relief="flat", background="#a0c4ff", font=("Arial", 12, "bold"))
    style.map("Soft.TButton", foreground=[("active", "#ffffff")], background=[("active", "#6a9aef")])

class PlotWindow:
    def __init__(self, root, csv_file):
        self.root = root
        self.root.title("Data Visualization App")
        self.df = pd.read_csv(csv_file)
        self.df["occupation"].replace("?", "Unknown", inplace=True)
        self.df["education_level"] = self.df["education"].apply(mapping_education)

        self.create_layout()

    def create_layout(self):
        self.pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.pane.pack(fill=tk.BOTH, expand=True)

        self.nav_frame = tk.Frame(self.pane, width=250, bg="#e3f2fd")
        self.pane.add(self.nav_frame)

        self.vis_frame = tk.Frame(self.pane, width=600, bg="white")
        self.pane.add(self.vis_frame)
        
        self.create_widgets()

    def create_widgets(self):
        self.plot_types = ["Bar", "Pie", "Histogram", "Line", "Box", "Scatter"]
        self.selected_plot = tk.StringVar(value=self.plot_types[0])

        ttk.Label(self.nav_frame, text="Select Plot Type:", style="TLabel").pack(pady=5)
        self.plot_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_plot, values=self.plot_types)
        self.plot_dropdown.pack(pady=5)
        self.plot_dropdown.bind("<<ComboboxSelected>>", self.update_column_dropdown)
        
        self.all_columns = self.df.columns.tolist()
        self.selected_col1 = tk.StringVar(value=self.all_columns[0])
        self.selected_col2 = tk.StringVar(value=self.all_columns[0])
        
        ttk.Label(self.nav_frame, text="Select First Column:", style="TLabel").pack(pady=5)
        self.col1_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_col1, values=self.all_columns)
        self.col1_dropdown.pack(pady=5)
        
        ttk.Label(self.nav_frame, text="Select Second Column:", style="TLabel").pack(pady=5)
        self.col2_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_col2, values=self.all_columns)
        self.col2_dropdown.pack(pady=5)
        
        self.plot_button = ttk.Button(self.nav_frame, text="Plot", style="Soft.TButton", command=self.plot_graph)
        self.plot_button.pack(pady=5)
        
        self.show_grid = tk.BooleanVar()
        ttk.Checkbutton(self.nav_frame, text="Show Grid", variable=self.show_grid).pack(pady=5)
        
        self.info_button = ttk.Button(self.nav_frame, text="Info", style="Soft.TButton", command=self.show_message)
        self.info_button.pack(pady=5)
        
        self.quit_button = ttk.Button(self.nav_frame, text="Quit", style="Soft.TButton", command=self.root.quit)
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

        if plot_type == "Pie Subplots":
            self.plot_pie_subplots(col1, col2)
            return

        fig = None

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

        #if self.df[col1].nunique() > 50 and plot_type in ["Bar", "Pie"]:
            #messagebox.showwarning("Warning", "The selected plot type may not be suitable due to too many unique values!")

        if plot_type == "Bar":
            self.plot_handler = PlotHandler(self.df, "bar", col1, col2)
        elif plot_type == "Pie":
            self.plot_handler = PlotHandler(self.df, "pie", col1, col2)
        elif plot_type == "Histogram":
            self.plot_handler = PlotHandler(self.df, "histogram", col1, None)
        elif plot_type == "Line":
            self.plot_handler = PlotHandler(self.df, "line", col1, col2)
        elif plot_type == "Box":
            self.plot_handler = PlotHandler(self.df, "box", col1, col2)
        elif plot_type == "Scatter":
            self.plot_handler = PlotHandler(self.df, "scatter", col1, col2)
        else:
            messagebox.showerror("Error", "Invalid plot type selected!")
            return
        
        if fig:
            fig.write_html("plot.html")
            webbrowser.open("plot.html")

        self.plot_handler.generate_plot()

    def plot_pie_subplots(self, col1, col2):
        """Generates Pie Subplots."""
        unique_values = self.df[col1].unique()
        num_plots = min(len(unique_values), 6)
        
        fig = make_subplots(rows=1, cols=num_plots, subplot_titles=[str(val) for val in unique_values[:num_plots]], specs=[[{'type':'domain'}]*num_plots])
        
        for i, value in enumerate(unique_values[:num_plots]):
            subset = self.df[self.df[col1] == value][col2].value_counts(normalize=True)
            fig.add_trace(go.Pie(labels=subset.index, values=subset.values, name=str(value)), row=1, col=i+1)
        
        fig.update_layout(title_text=f"Pie Subplots of {col1}")
        fig.write_html("plot.html")
        webbrowser.open("plot.html")


    def show_message(self):
        MessageBoxHandler(self.df)

    def setup_styles():
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12, "bold"), foreground="#1565c0", background="#e3f2fd")
    
        style.configure("Soft.TButton",
                    padding=6,
                    relief="flat",
                    background="#a0c4ff",  # Soft mavi
                    font=("Arial", 12, "bold"))

        # Add hover effect for buttons
        style.map("Soft.TButton",
              foreground=[("active", "#ffffff")],
              background=[("active", "#6a9aef")])  # Slightly darker blue when hovered


class PlotHandler:
    def __init__(self, df, plot_type, col1, col2):
        self.df = df
        self.plot_type = plot_type
        self.col1 = col1
        self.col2 = col2

    def generate_plot(self):
        plot_title = f"{self.plot_type} plot of {self.col1} and {self.col2}".title()
        title_style = dict(font=dict(size=20, color="blue", family="Arial", weight="bold"))

        if self.plot_type == "bar":
            if self.col2 == "---":  # If no second column is selected
                count_df = self.df[self.col1].value_counts().reset_index(name="Count")
                fig = px.bar(count_df, x="index", y="Count")
            else:
                count_df = self.df.groupby([self.col1, self.col2]).size().reset_index(name="Count")
                fig = px.bar(count_df, x=self.col1, y="Count", color=self.col2, barmode="group")
            fig.update_layout(title=plot_title, title_font=dict(size=20, color="blue", family="Arial", weight="bold"))

        elif self.plot_type == "pie_subplots":
            unique_values = self.df[self.col1].unique()
            num_plots = min(len(unique_values), 6)  # En fazla 6 subplot olacak şekilde sınırlandırıyoruz.
            
            fig = make_subplots(rows=1, cols=num_plots, subplot_titles=[str(val) for val in unique_values[:num_plots]], specs=[[{'type':'domain'}]*num_plots])
            
            for i, value in enumerate(unique_values[:num_plots]):
                subset = self.df[self.df[self.col1] == value][self.col2].value_counts(normalize=True)
                fig.add_trace(go.Pie(labels=subset.index, values=subset.values, name=str(value)), row=1, col=i+1)
            
            fig.update_layout(title_text=plot_title,title_font=dict(size=20, color="blue", family="Arial", weight="bold"))
            fig.write_html("plot.html")
            webbrowser.open("plot.html")
            return

        elif self.plot_type == "histogram":
            fig = px.histogram(self.df, x=self.col1, color=self.col2 if self.col2 != "---" else None)
            fig.update_layout(title=plot_title, title_font=dict(size=20, color="blue", family="Arial", weight="bold"))

        elif self.plot_type == "line":
            fig = px.line(self.df, x=self.col1, y=self.col2)
            fig.update_layout(title=plot_title, title_font=dict(size=20, color="blue", family="Arial", weight="bold"))

        elif self.plot_type == "box":
            fig = px.box(self.df, x=self.col1, y=self.col2)
            fig.update_layout(title=plot_title, title_font=dict(size=20, color="blue", family="Arial", weight="bold"))

        elif self.plot_type == "scatter":
            fig = px.scatter(self.df, x=self.col1, y=self.col2)
            fig.update_layout(title=plot_title, title_font=dict(size=20, color="blue", family="Arial", weight="bold"))

        else:
            messagebox.showerror("Error", "Invalid plot type selected!")
            return

        fig.write_html("plot.html")
        webbrowser.open("plot.html")


class MessageBoxHandler:
    def __init__(self, df):
        self.df = df
        self.show_info()

    def show_info(self):
        info_text = f"Dataset Info:\nRows: {self.df.shape[0]}\nColumns: {self.df.shape[1]}\nMissing Values: {self.df.isnull().sum().sum()}"
        messagebox.showinfo("Dataset Information", info_text)


if __name__ == "__main__":
    root = tk.Tk()
    setup_styles()
    app = PlotWindow(root, "adult_eda.csv")
    root.mainloop()

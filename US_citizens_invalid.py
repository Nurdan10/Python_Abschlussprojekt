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
        self.plot_types = ["Bar", "Pie", "Histogram", "Line"]
        self.selected_plot = tk.StringVar(value=self.plot_types[0])
        ttk.Label(self.nav_frame, text="Select Plot Type:").pack(pady=5)
        self.plot_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_plot, values=self.plot_types)
        self.plot_dropdown.pack(pady=5)
        self.plot_dropdown.bind("<<ComboboxSelected>>", self.update_column_dropdown)

        # Dropdown for First Column (Either categorical or numerical)
        self.all_columns = self.df.columns.tolist()
        self.selected_col1 = tk.StringVar(value=self.all_columns[0])
        ttk.Label(self.nav_frame, text="Select First Column:").pack(pady=5)
        self.col1_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_col1, values=self.all_columns)
        self.col1_dropdown.pack(pady=5)

        # Dropdown for Second Column (Either categorical or numerical)
        self.selected_col2 = tk.StringVar(value=self.all_columns[1] if len(self.all_columns) > 1 else self.all_columns[0])
        ttk.Label(self.nav_frame, text="Select Second Column:").pack(pady=5)
        self.col2_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_col2, values=self.all_columns)
        self.col2_dropdown.pack(pady=5)

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

    def update_column_dropdown(self, event=None):
        plot_type = self.selected_plot.get()

        # Update dropdown values based on selected plot type
        if plot_type in ["Bar", "Pie"]:
            # For Bar/Pie charts, we can select any column
            self.col1_dropdown.config(values=self.df.select_dtypes(include=['object']).columns.tolist())
            self.col2_dropdown.config(values=self.df.select_dtypes(include=['object']).columns.tolist())
        else:
            # For Histogram/Line charts, allow numerical columns as well
            self.col1_dropdown.config(values=self.df.columns.tolist())
            self.col2_dropdown.config(values=self.df.columns.tolist())

    def plot_graph(self):
        plot_type = self.selected_plot.get()
        col1 = self.selected_col1.get()
        col2 = self.selected_col2.get()

        # Validation based on plot type
        if plot_type == "Bar" and not (self.df[col1].dtype == 'object' and self.df[col2].dtype == 'object'):
            messagebox.showwarning("Warning", "For Bar charts, both columns should be categorical!")
            return
            
    # Pie Plot: Sadece birinci sütunun kategorik olması yeterli
        elif plot_type == "Pie" and self.df[col1].dtype != 'object':
            messagebox.showwarning("Warning", "For Pie charts, the first column should be categorical!")
            return

    # Histogram: Sadece birinci sütun sayısal olmalı
        elif plot_type == "Histogram" and self.df[col1].dtype not in ['float64', 'int64']:
            messagebox.showwarning("Warning", "For Histogram, the first column should be numerical!")
            return

    # Line Plot: Hem birinci hem ikinci sütun sayısal olmalı
        elif plot_type == "Line" and (self.df[col1].dtype not in ['float64', 'int64'] or self.df[col2].dtype not in ['float64', 'int64']):
            messagebox.showwarning("Warning", "For Line charts, both columns should be numerical!")
            return

    # Scatter Plot: Hem birinci hem ikinci sütun sayısal olmalı
        elif plot_type == "Scatter" and (self.df[col1].dtype not in ['float64', 'int64'] or self.df[col2].dtype not in ['float64', 'int64']):
            messagebox.showwarning("Warning", "For Scatter plots, both columns should be numerical!")
            return

    # Box Plot: İkinci sütunun sayısal olması gerekiyor
        elif plot_type == "Box" and self.df[col2].dtype not in ['float64', 'int64']:
            messagebox.showwarning("Warning", "For Box plots, the second column should be numerical!")
            return

        # Plot handling
        # Eğer Bar veya Pie seçilmişse ve çok fazla unique değer varsa uyarı ver
        if plot_type in ["Bar", "Pie"] and self.df[col1].nunique() > 50:
            messagebox.showwarning("Warning", "The selected plot type may not be suitable due to too many unique values!")

    # Grafik çizimi
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
            # Create a bar chart with count of categorical data
            count_df = self.df.groupby([self.col1, self.col2]).size().reset_index(name="Count")
            fig = px.bar(count_df, x=self.col1, y="Count", color=self.col2, barmode="group")
        elif self.plot_type == "pie":
            # Create a pie chart for categorical data
            count_df = self.df.groupby([self.col1]).size().reset_index(name="Count")
            fig = px.pie(count_df, names=self.col1, values="Count", title=f"Distribution of {self.col1}")
        elif self.plot_type == "histogram":
            # Create a histogram for numerical data
            fig = px.histogram(self.df, x=self.col1, title=f"Histogram of {self.col1}")
        elif self.plot_type == "line":
            # Create a line chart for numerical data
            fig = px.line(self.df, x=self.col1, y=self.col2, title=f"Line Chart of {self.col2} over {self.col1}")
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
    app = PlotWindow(root, "adult_eda.csv")  # Use your CSV file here
    root.mainloop()


# olmadi show grid dogru calismiyor, her durumda grid ile geliyor grafik. 
# o yüzden check butonu baska bir islev yapsin, mesela veri kümesini filtreleme isini nasil yapabiliriz? 
# buraya ekleyecegim kodda baska hic bir degisiklik yapmaksizin sadece o kismi düzenle!!!
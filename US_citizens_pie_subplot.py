"""
Dieses Programm ist eine Tkinter-basierte Anwendung zur Visualisierung von CSV-Daten mit Plotly.

Funktionalitäten:
- Laden einer CSV-Datei über eine Dateiauswahl.
- Auswahl eines Diagrammtyps (Balken-, Kreis-, Histogramm-, Linien-, Box- und Streudiagramme).
- Auswahl von Spalten für die Diagrammerstellung.
- Visualisierung der Daten in einem interaktiven Plotly-Graphen.
- Speicherung und Anzeige der generierten Diagramme in einem Webbrowser.

Technische Umsetzung:
- Tkinter für die Haupt-GUI und `ttk` für die stilisierten Widgets.
- Pandas für die CSV-Verarbeitung.
- Plotly für die Diagrammerstellung:
    plotly.express für schnelle und interaktive Diagramme,
    plotly.graph_objects für komplexe und anpassbare Diagramme,
    plotly.subplots für das Erstellen von Subplots.
- Webbrowser-Modul zur Anzeige von Diagrammen: webbrowser zum Öffnen von Diagrammen im Standard-Webbrowser.
- Pillow für die Bildbearbeitung:
    PIL.ImageTk für die Integration von Bildern in Tkinter, 
    PIL.ImageDraw und PIL.ImageFont für das Hinzufügen von Text auf Bildern.

Autor: Nurdan Cakir
Datum: 04.04.2025
"""


import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import messagebox, ttk, filedialog, simpledialog
import pandas as pd
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import webbrowser

def mapping_education(x):
    """
    Weist jeder Bildungsstufe eine allgemeine Kategorie zu.
    """
    if x in ["Preschool", "1st-4th", "5th-6th", "7th-8th", "9th", "10th", "11th", "12th"]:
        return "low_level_grade"
    elif x in ["HS-grad", "Some-college", "Assoc-voc", "Assoc-acdm"]:
        return "medium_level_grade"
    elif x in ["Bachelors", "Masters", "Prof-school", "Doctorate"]:
        return "high_level_grade"
    return None

def mapping_marital_status(x):
    """
    Die Funktion weist dem Familienstand eine allgemeine Kategorie zu:
    """
    if x in ["Never-married", "Divorced", "Separated", "Widowed"]:
        return "unmarried"
    elif x in ["Married-civ-spouse", "Married-AF-spouse", "Married-spouse-absent"]:
        return "married"

def setup_styles():
    """
    Konfiguriert das visuelle Erscheinungsbild der GUI mit Tkinter Style.
    """
    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12, "bold"), foreground="#1565c0", background="#e3f2fd")
    style.configure("Soft.TButton", padding=6, relief="flat", background="#a0c4ff", font=("Arial", 12, "bold"))
    style.map("Soft.TButton", foreground=[("active", "#ffffff")], background=[("active", "#6a9aef")])

class PlotWindow:
    """Erstellt das Hauptfenster für die Datenvisualisierung."""
    def __init__(self, root, csv_file):
        self.root = root
        self.root.title("Data Visualization App")
        self.df = pd.read_csv(csv_file)
        self.df["occupation"].replace("?", "Unknown", inplace=True)
        self.df["education_level"] = self.df["education"].apply(mapping_education)
        self.df["marital_status_summary"] = self.df["marital-status"].apply(mapping_marital_status)

        self.create_layout()

    def create_layout(self):
        """Richtet das GUI-Layout mit Navigations- und Visualisierungsbereich ein."""
        self.pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.pane.pack(fill=tk.BOTH, expand=True)

        # Navigation Frame für Buttons und Optionen
        self.nav_frame = tk.Frame(self.pane, width=250, bg="#e3f2fd")
        self.nav_frame.pack_propagate(False)  # İçeriğin boyutlandırmasını engeller
        self.pane.add(self.nav_frame)
    
        # Erstellen eines zusätzlichen Rahmens für das Hinzufügen 
        # von Padding an der oberen Seite des Navigationsrahmens.

        top_frame = tk.Frame(self.nav_frame, bg="#e3f2fd", height=100)  # 50px padding için bir frame
        top_frame.pack(fill=tk.X)
        
        # Visualisierungsbereich
        self.vis_frame = tk.Frame(self.pane, width=600, bg="white")
        self.pane.add(self.vis_frame)

        self.add_image_with_text()
        
    def add_image_with_text(self):
        """
        Das Hinzufügen von Anwendungstitel oder Nachricht auf das Bild zur Anzeige auf dem Bildschirm.

        """
        img_path = "C:/Users/nurda/Python_Abschlussprojekt/images/data_visualization.jpg"  # Resmin yolunu buraya yazın
        img = Image.open(img_path)
        img = img.resize((400, 400), Image.Resampling.LANCZOS)  # Resmin boyutunu büyütüyoruz
    
        # Der Beginn des Zeichnens zum Hinzufügen von Text.
        img_tk = ImageTk.PhotoImage(img)

        text = "Welcome to DataViz App"
        label_text = Label(self.vis_frame, text=text, font=("Arial", 24, "bold"), bg="white", fg="black")
        label_text.pack(pady=(20, 10))
    
        # Zeigt das Bild in einem Label
        self.image_label = Label(self.vis_frame, image=img_tk)
        self.image_label.image = img_tk  # Referansı kaybetmemek için
        self.image_label.pack(padx=10, pady=10)

        self.create_widgets()

    def create_widgets(self):
        """Erstellt die Widgets zur Steuerung der Anwendung."""
        # Liste der verfügbaren Diagrammtypen
        self.plot_types = ["Bar", "Pie", "Histogram", "Line", "Box", "Scatter"]
        # Standardmäßig ausgewählter Diagrammtyp
        self.selected_plot = tk.StringVar(value=self.plot_types[0])
        
        # Label für die Auswahl des Diagrammtyps
        ttk.Label(self.nav_frame, text="Select Plot Type:", style="TLabel").pack(pady=5)
        
        # Dropdown-Menü für die Auswahl des Diagrammtyps
        self.plot_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_plot, values=self.plot_types)
        self.plot_dropdown.pack(pady=5)
        # Ereignisbindung: Wenn der Benutzer einen Diagrammtyp auswählt, wird die Spaltenauswahl aktualisiert
        self.plot_dropdown.bind("<<ComboboxSelected>>", self.update_column_dropdown)
        
        # Liste der Spalten aus dem DataFrame
        self.all_columns = self.df.columns.tolist()
        # Standardmäßig ausgewählte Spalte für die erste und zweite Auswahl
        self.selected_col1 = tk.StringVar(value=self.all_columns[0])
        self.selected_col2 = tk.StringVar(value=self.all_columns[0])
        
        # Label für die Auswahl der ersten Spalte
        ttk.Label(self.nav_frame, text="Select First Column:", style="TLabel").pack(pady=5)
        # Dropdown-Menü für die Auswahl der ersten Spalte
        self.col1_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_col1, values=self.all_columns)
        self.col1_dropdown.pack(pady=5)
        
        # Label für die Auswahl der zweiten Spalte
        ttk.Label(self.nav_frame, text="Select Second Column:", style="TLabel").pack(pady=5)
        # Dropdown-Menü für die Auswahl der zweiten Spalte
        self.col2_dropdown = ttk.Combobox(self.nav_frame, textvariable=self.selected_col2, values=self.all_columns)
        self.col2_dropdown.pack(pady=5)
        
        # Button zum Erstellen des Diagramms
        self.plot_button = ttk.Button(self.nav_frame, text="Plot", style="Soft.TButton", command=self.plot_graph)
        self.plot_button.pack(pady=5)
        
        # Button für eine Informationsnachricht
        self.info_button = ttk.Button(self.nav_frame, text="Info", style="Soft.TButton", command=self.show_message)
        self.info_button.pack(pady=5)
        
        # Button zum Beenden der Anwendung
        self.quit_button = ttk.Button(self.nav_frame, text="Quit", style="Soft.TButton", command=self.root.quit)
        self.quit_button.pack(pady=5)

    def update_column_dropdown(self, event=None):
        """Aktualisiert die Drop-down-Menüs mit den CSV-Spaltennamen."""
        # Der aktuell ausgewählte Diagrammtyp wird ermittelt
        plot_type = self.selected_plot.get()

        # Wenn der Diagrammtyp "Histogram" ist, werden nur die erste Spalte ausgeführt und die zweite Dropdown-Liste wird auf "---" gesetzt
        if plot_type == "Histogram":
            self.col2_dropdown.config(values=["---"])
            # Wenn der Diagrammtyp "Bar" oder "Pie" ist, wird nur mit Spalten vom Datentyp 'object' 
            # (kategorische Spalten) gearbeitet
        elif plot_type in ["Bar", "Pie"]:
            # Die Spalten mit dem Datentyp 'object' (kategorische Daten) werden als Werte 
            # für die Dropdown-Menüs verwendet
            self.col1_dropdown.config(values=self.df.select_dtypes(include=['object']).columns.tolist())
            # Für die zweite Spalte wird zusätzlich ein "---" als Auswahloption hinzugefügt
            self.col2_dropdown.config(values=self.df.select_dtypes(include=['object']).columns.tolist() + ["---"])
            # Für alle anderen Diagrammtypen werden alle Spalten des DataFrames als Optionen 
            # für die Dropdown-Listen angeboten
        else:
            self.col1_dropdown.config(values=self.df.columns.tolist())
            # Für die zweite Spalte wird ebenfalls ein "---" als Auswahloption hinzugefügt
            self.col2_dropdown.config(values=self.df.columns.tolist() + ["---"])


    def plot_graph(self):
        """Erstellt ein Diagramm basierend auf den Benutzereinstellungen."""
        # Der ausgewählte Diagrammtyp und die ausgewählten Spalten werden abgerufen
        plot_type = self.selected_plot.get()
        col1 = self.selected_col1.get()
        col2 = self.selected_col2.get()

        # Überprüfen der Eingaben basierend auf dem ausgewählten Diagrammtyp und den Daten
        # Überprüfung für Balkendiagramme: Beide Spalten sollten kategorisch sein
        if plot_type == "Bar" and not (self.df[col1].dtype == 'object' and (self.df[col2].dtype == 'object' or col2 == "---")):
            messagebox.showwarning("Warning", "For Bar charts, both columns should be categorical!")
            return
        # Überprüfung für Tortendiagramme: Die erste Spalte sollte kategorisch sein
        elif plot_type == "Pie" and not (self.df[col1].dtype == 'object'):
            messagebox.showwarning("Warning", "For Pie charts, the first column should be categorical!")
            return
        # Überprüfung für Histogramme: Die erste Spalte sollte numerisch sein
        elif plot_type == "Histogram" and not (self.df[col1].dtype in ['float64', 'int64']):
            messagebox.showwarning("Warning", "For Histogram, the first column should be numerical!")
            return
        # Überprüfung für Liniendiagramme: Beide Spalten sollten numerisch sein
        elif plot_type == "Line" and not (self.df[col1].dtype in ['float64', 'int64'] and self.df[col2].dtype in ['float64', 'int64']):
            messagebox.showwarning("Warning", "For Line charts, both columns should be numerical!")
            return
        # Überprüfung für Streudiagramme: Beide Spalten sollten numerisch sein
        elif plot_type == "Scatter" and not (self.df[col1].dtype in ['float64', 'int64'] and self.df[col2].dtype in ['float64', 'int64']):
            messagebox.showwarning("Warning", "For Scatter plots, both columns should be numerical!")
            return
        # Überprüfung für Boxplots: Die zweite Spalte sollte numerisch sein
        elif plot_type == "Box" and not (self.df[col2].dtype in ['float64', 'int64']):
            messagebox.showwarning("Warning", "For Box plots, the second column should be numerical!")
            return

        # Warnung, wenn die Anzahl der einzigartigen Werte zu hoch ist für Balken- oder Tortendiagramme
        if self.df[col1].nunique() > 50 and plot_type in ["Bar", "Pie"]:
            messagebox.showwarning("Warning", "The selected plot type may not be suitable due to too many unique values!")

        # Erstellen und Initialisieren des PlotHandlers entsprechend dem Diagrammtyp
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

        # Erstellen des Diagramms
        self.plot_handler.generate_plot()

        # Anzeige einer Informationsnachricht
    def show_message(self):
        MessageBoxHandler(self.df)



class PlotHandler:
    """
    Eine Klasse zur Generierung verschiedener Diagrammtypen mit Plotly.

    Attribute:
    -----------
    df : pandas.DataFrame
        Der geladene DataFrame mit den CSV-Daten.
    plot_type : str
        Der gewählte Diagrammtyp (z. B. "bar", "pie", "histogram", "line", "box", "scatter").
    col1 : str
        Die erste ausgewählte Spalte für die Diagrammerstellung.
    col2 : str
        Die zweite ausgewählte Spalte (falls benötigt, sonst "---").

    Methoden:
    ---------
    generate_plot():
        Erstellt ein Diagramm basierend auf den ausgewählten Parametern und zeigt es an.
    """
    def __init__(self, df, plot_type, col1, col2):
        """
        Initialisiert den PlotHandler mit den übergebenen Parametern.
        """
        # DataFrame mit den CSV-Daten
        self.df = df
        # Der gewählte Diagrammtyp (z.B. 'bar', 'pie', 'histogram', etc.)
        self.plot_type = plot_type
        # Die erste Spalte für das Diagramm
        self.col1 = col1
        # Die zweite Spalte für das Diagramm (oder "---", falls nicht benötigt)
        self.col2 = col2

    def generate_plot(self):
        """
        Erstellt und zeigt ein Diagramm basierend auf den ausgewählten Parametern.

        Der Diagrammtyp wird basierend auf der Benutzerauswahl erstellt. Es werden 
        verschiedene Diagrammtypen unterstützt, einschließlich Bar, Pie, Histogramm,
        Line, Box und Scatter. Alle Diagramme erhalten einen Titel und eine 
        angepasste Formatierung.

        Wenn der Diagrammtyp oder die Spaltenkombination nicht geeignet ist, wird
        eine Fehlermeldung angezeigt.
        """
        plot_title = f"{self.plot_type} plot of {self.col1} and {self.col2}".title()
        title_style = dict(font=dict(size=20, color="blue", family="Arial", weight="bold"))

        # Erstellen eines Bar-Diagramms
        if self.plot_type == "bar":
            if self.col2 == "---":  # Wenn keine zweite Spalte ausgewählt ist
                count_df = self.df[self.col1].value_counts().reset_index(name="Count")
                fig = px.bar(count_df, x="index", y="Count")
            else:
                count_df = self.df.groupby([self.col1, self.col2]).size().reset_index(name="Count")
                fig = px.bar(count_df, x=self.col1, y="Count", color=self.col2, barmode="group")
            fig.update_layout(title=plot_title, title_font=dict(size=20, color="blue", family="Arial", weight="bold"))

        # Erstellen eines Pie-Diagramms
        elif self.plot_type == "pie":
            # We handle only the subplot version of the pie chart
            if self.col1 == "salary":  # Gruppierung nach Gehalt
                fig = make_subplots(rows=1, cols=2, subplot_titles=("<=50K", ">50K"), specs=[[{"type": "domain"}, {"type": "domain"}]])
            
                for i, salary_group in enumerate(["<=50K", ">50K"]):
                    df_grouped = self.df[self.df["salary"] == salary_group][self.col2].value_counts().reset_index()
                    df_grouped.columns = [self.col2, "Count"]
                    fig.add_trace(go.Pie(labels=df_grouped[self.col2], values=df_grouped["Count"]), row=1, col=i+1)
                fig.update_layout(title_text=plot_title, title_font=dict(size=20, color="blue", family="Arial", weight="bold"))
                fig.show()
            else:
                count_df = self.df.groupby([self.col1, self.col2]).size().reset_index(name="Count")
                fig = px.pie(count_df, names=self.col1, color=self.col2, values="Count")
                fig.update_layout(title=plot_title, title_font=dict(size=20, color="blue", family="Arial", weight="bold"))
                fig.show()

        # Erstellen eines Histogramms
        elif self.plot_type == "histogram":
            fig = px.histogram(self.df, x=self.col1, color=self.col2 if self.col2 != "---" else None)
            fig.update_layout(title=plot_title, title_font=dict(size=20, color="blue", family="Arial", weight="bold"))

        # Erstellen eines Liniendiagramms
        elif self.plot_type == "line":
            fig = px.line(self.df, x=self.col1, y=self.col2)
            fig.update_layout(title=plot_title, title_font=dict(size=20, color="blue", family="Arial", weight="bold"))

        # Erstellen eines Box-Diagramms
        elif self.plot_type == "box":
            fig = px.box(self.df, x=self.col1, y=self.col2)
            fig.update_layout(title=plot_title, title_font=dict(size=20, color="blue", family="Arial", weight="bold"))

        # Erstellen eines Scatter-Diagramms
        elif self.plot_type == "scatter":
            fig = px.scatter(self.df, x=self.col1, y=self.col2)
            fig.update_layout(title=plot_title, title_font=dict(size=20, color="blue", family="Arial", weight="bold"))

         # Fehlerbehandlung bei ungültigem Diagrammtyp
        else:
            messagebox.showerror("Error", "Invalid plot type selected!")
            return
        
        # Speichern und Öffnen des Diagramms
        fig.write_html("plot.html")
        webbrowser.open("plot.html")

        # Speicherung des Plots
        # Abfrage, ob der Benutzer das Diagramm speichern möchte
        save_plot = messagebox.askyesno("Save Plot", "Do you want to save this plot?")
        
        if save_plot:
             # Optionen für Dateitypen (PNG oder PDF)
            filetypes = [("PNG file", "*.png"), ("PDF file", "*.pdf")]
            # Dialog zur Dateiauswahl und -speicherung
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filetypes)
            
            if file_path:
                # Das Diagramm im gewählten Dateiformat speichern
                fig.write_image(file_path)
                # Erfolgsmeldung anzeigen
                messagebox.showinfo("Success", f"Plot saved as {file_path}")

        """save_plot = messagebox.askyesno("Save Plot", "Do you want to save this plot?")
        
        if save_plot:
            # Kaydetme penceresini aç
            filetypes = [("PNG file", "*.png"), ("PDF file", "*.pdf")]
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png", filetypes=filetypes, title="Save Plot As"
            )

            if file_path:
                try:
                    # Grafiği PNG veya PDF olarak kaydet
                    # fig.io.to_image ile görseli kaydediyoruz
                    img_data = pio.to_image(fig, format='png')  # PNG formatında döndürüyoruz
                    with open(file_path, "wb") as f:
                        f.write(img_data)
                    messagebox.showinfo("Success", f"Plot saved successfully at:\n{file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save plot: {e}")
        else:
            messagebox.showwarning("Warning", "No directory selected. Plot not saved.")"""


class MessageBoxHandler:
    """
    Diese Klasse wird verwendet, um eine Informationsbox über das Dataset anzuzeigen.
    
    Methoden:
    ---------
    show_info(): Zeigt die Informationen des Datensatzes an, einschließlich der Anzahl der Zeilen, Spalten und fehlenden Werte.
    """
    def __init__(self, df):
        # Der DataFrame wird als Argument übergeben
        self.df = df
        # Ruft die Methode zur Anzeige der Datensatzinformationen au
        self.show_info()

    def show_info(self):
        """
        Zeigt eine Informationsbox mit den grundlegenden Details des DataFrames an:
        - Anzahl der Zeilen
        - Anzahl der Spalten
        - Anzahl der fehlenden Werte
        """
        info_text = f"Dataset Info:\nRows: {self.df.shape[0]}\nColumns: {self.df.shape[1]}\nMissing Values: {self.df.isnull().sum().sum()}"
        # Zeigt das Info-Fenster mit den Daten an
        messagebox.showinfo("Dataset Information", info_text)

# Der Hauptcode, um die Anwendung zu starten
if __name__ == "__main__":
    root = tk.Tk()  # Erstellt das Haupt-Tkinter-Fenster
    setup_styles()  # Wendet die Styles für die GUI an
    # Erstellt das PlotWindow mit dem DataFrame aus der CSV-Datei
    app = PlotWindow(root, "adult_eda.csv")
    root.mainloop()

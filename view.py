import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
import os
from pdf2image import convert_from_path
import threading

# Rutas y configuraciones
POPPLER_PATH = r"C:\Program Files\poppler-24.02.0\Library\bin"
DEFAULT_DPI = 500

class PDFConverterView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF to PNG Converter")
        self.geometry("500x250")

        # Etiqueta y campo de entrada para la ruta del archivo PDF
        self.label_pdf = tk.Label(self, text="Ruta del archivo PDF:")
        self.label_pdf.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.input_var_pdf = tk.StringVar()
        self.entry_pdf = tk.Entry(self, textvariable=self.input_var_pdf, width=40)
        self.entry_pdf.grid(row=0, column=1, padx=5, pady=5)
        self.browse_button = tk.Button(self, text="Browse", command=self.browse_pdf_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Campo de entrada para la ruta de guardado de archivos PNG
        self.label_save = tk.Label(self, text="Guardar en:")
        self.label_save.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.input_var_save = tk.StringVar()
        self.entry_save = tk.Entry(self, textvariable=self.input_var_save, width=40)
        self.entry_save.grid(row=1, column=1, padx=5, pady=5)
        self.browse_save_button = tk.Button(self, text="Browse", command=self.browse_save_directory)
        self.browse_save_button.grid(row=1, column=2, padx=5, pady=5)

        # Botón de convertir
        self.convert_button = tk.Button(self, text="Convertir", command=self.start_conversion)
        self.convert_button.grid(row=2, column=1, padx=5, pady=15)

        # Indicador giratorio (spinner)
        self.spinner_var = tk.BooleanVar()
        self.spinner_var.set(False)
        self.spinner = ttk.Spinbox(self, from_=0, to=100, textvariable=self.spinner_var, state="readonly")
        self.spinner.grid(row=3, column=1, padx=5, pady=5)

        # Cuadro de texto para mostrar mensaje de conversión completada
        self.conversion_label = tk.Label(self, text="", fg="green")
        self.conversion_label.grid(row=4, column=1, padx=5, pady=5)

        # Variables para controlar la conversión
        self.converting = False

    def browse_pdf_file(self):
        try:
            file_path = fd.askopenfilename(filetypes=(('PDF files', '*.pdf'), ('All files', '*.*')))
            if file_path:
                self.input_var_pdf.set(file_path)
        except Exception as e:
            print(f"Error al abrir el archivo: {e}")

    def browse_save_directory(self):
        try:
            save_path = fd.askdirectory()
            if save_path:
                self.input_var_save.set(save_path)
        except Exception as e:
            print(f"Error al abrir el directorio: {e}")

    def start_conversion(self):
        if self.converting:
            return  # Si ya se está realizando una conversión, sal del método

        pdf_path = self.input_var_pdf.get()
        save_to = self.input_var_save.get()

        # Valida que las rutas de archivo y de guardado no estén vacías
        if not pdf_path or not save_to:
            tk.messagebox.showerror("Error", "Por favor, seleccione un archivo PDF y una carpeta de destino.")
            return

        # Desactiva el botón de convertir y activa el spinner
        self.convert_button.config(state="disabled")
        self.spinner_var.set(True)
        self.converting = True

        # Crear un hilo para la conversión y actualizar el spinner
        self.progress_thread = threading.Thread(target=self.convert_pdf_to_png, args=(pdf_path, save_to))
        self.progress_thread.start()

    def convert_pdf_to_png(self, pdf_path, save_to):
        try:
            pages = convert_from_path(pdf_path, dpi=DEFAULT_DPI, poppler_path=POPPLER_PATH)
            total_pages = len(pages)
            for index, page in enumerate(pages):
                page.save(os.path.join(save_to, f"page_{index+1}.png"), "PNG")
            print("¡Conversión completada!")
            self.conversion_label.config(text="¡Conversión completada!")
        except Exception as e:
            print(f"Error durante la conversión: {e}")
        finally:
            # Reactiva el botón de convertir, desactiva el spinner y marca la conversión como completada
            self.convert_button.config(state="normal")
            self.spinner_var.set(False)
            self.converting = False

if __name__ == "__main__":
    app = PDFConverterView()
    app.mainloop()

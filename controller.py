from view import PDFConverterView
from model import PDFConverter  # Importa la clase PDFConverter desde el archivo model.py

class PDFConverterController:
    def __init__(self):
        self.view = PDFConverterView()
        self.view.convert_button.config(command=self.convert_pdf_to_png)
        self.view.mainloop()

    def convert_pdf_to_png(self):
        pdf_path = self.view.input_var_pdf.get()
        save_to = self.view.input_var_save.get()
        # self.view.progress_bar.start()
        self.view.update_idletasks()  # Actualiza la interfaz antes de iniciar la conversión

        try:
            PDFConverter.convert_pdf_to_png(pdf_path, save_to)  # Utiliza la clase PDFConverter correctamente
        finally:
            print("Converted")

import os
from pdf2image import convert_from_path

class PDFConverter:
    POPPLER_PATH = r"C:\Program Files\poppler-24.02.0\Library\bin"
    DEFAULT_DPI = 500

    @classmethod
    def convert_pdf_to_png(cls, pdf_path, save_to):
        try:
            pages = convert_from_path(pdf_path, dpi=cls.DEFAULT_DPI, poppler_path=cls.POPPLER_PATH)
            file_name = os.path.basename(pdf_path)
            png_filename = os.path.splitext(file_name)[0]

            for index, page in enumerate(pages):
                page.save(os.path.join(save_to, f"{png_filename}-{index}.png"), "PNG")
            print("¡Conversión completada!")
        except Exception as e:
            print(f"Error durante la conversión: {e}")

from pdf_parser import PdfParser
from docx_parser import DocxParser
import os


class UserInterface:
    def __init__(self, pdf_filename="odpis_aktualny_1.pdf"):
        self.datafields = {}
        self.filename = pdf_filename.strip(".pdf")

    def parse_pdf(self, pdf_file):
        parser = PdfParser(pdf_file)
        parser.load_pdf(env="venv")
        self.datafields = parser.parse_paragraphs()

    def print_pdf_data(self):
        print(f">>> Parsing... '{self.filename}'\n"
              f"> Nazwa sądu: {self.datafields['Oznaczenie sądu']},\n"
              f"> Województwo: {self.datafields['Siedziba_Wojewodztwo']}, "
              f"Powiat: {self.datafields['Siedziba_Powiat']}, Gmina: {self.datafields['Siedziba_Gmina']},"
              f" Miejscowość: {self.datafields['Siedziba_Miejscowosc']}, "
              f"Firma spółki: {self.datafields['Firma, pod którą spółka działa']}"
              f"\n> Numer KRS: {self.datafields['KRS']}, REGON: {self.datafields['REGON']},"
              f" NIP: {self.datafields['NIP']}")

    def print_pdf_all(self):
        for key, value in self.datafields.items():
            print(f"{key} : {value}")

    def parse_docx(self):
        parser = DocxParser(self.datafields)
        parser.parse_document()
        parser.save_document(f"{self.filename}.docx")
        print(f">>> {self.filename.capitalize()}.docx file created!")

    @staticmethod
    def parse_dir():
        for pdf_file in os.listdir(os.path.join("pdf", "")):
            if pdf_file.endswith(".pdf"):
                ui = UserInterface(pdf_file)
                ui.parse_pdf(pdf_file)  # initiate parser object with pdf file
                ui.print_pdf_data()
                ui.parse_docx()

        input(f">  Finished!\n>  Press Enter to exit")


if __name__ == "__main__":
    ui = UserInterface()
    ui.parse_dir()

from pdf_parser import PdfParser
from docx_parser import DocxParser
from sys import exit
import os


class UserInterface:
    def __init__(self, pdf_filename="odpis_aktualny_1.pdf"):
        self.datafields = {}
        self.filename = pdf_filename.strip(".pdf")

    def parse_pdf(self, pdf_file):
        parser = PdfParser(pdf_file)
        parser.load_pdf()
        self.datafields = parser.parse_paragraphs()

    def print_datafields(self):
        print(f">>> Parsing... '{self.filename}'\n"
              f"> Nazwa sądu: {self.datafields['Oznaczenie sądu']},\n"
              f"> Województwo: {self.datafields['Siedziba_Wojewodztwo']}, "
              f"Powiat: {self.datafields['Siedziba_Powiat']}, Gmina: {self.datafields['Siedziba_Gmina']},"
              f" Miejscowość: {self.datafields['Siedziba_Miejscowosc']}, "
              f"Firma spółki: {self.datafields['Firma, pod którą spółka działa']}"
              f"\n> Numer KRS: {self.datafields['KRS']}, REGON: {self.datafields['REGON']},"
              f" NIP: {self.datafields['NIP']}")

    def print_all_datafields(self):
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
                parser = UserInterface(pdf_file)
                parser.parse_pdf(pdf_file)  # initiate parser object with pdf file
                parser.print_datafields()
                parser.parse_docx()

    @staticmethod
    def parse_file(pdf_file):
        parser = UserInterface(pdf_file)
        parser.parse_pdf(pdf_file)
        parser.print_datafields()
        parser.parse_docx()

    @staticmethod
    def files():
        files = os.listdir(os.path.join("pdf", ""))
        [print(f"- {file}") for file in files]

    @staticmethod
    def help():
        print("> List of commands:\n"
              "- all - Parses all files in pdf directory.\n"
              "- parse 'filename' - Parses one pdf file. Eg. 'file odpis_aktualny_1.pdf'.\n"
              "- files - Prints all files in the pdf directory.\n"
              "- help - Lists all commands."
              "- exit - Exits the application.")

    def ui_loop(self):
        commands = {"all": self.parse_dir, "parse": self.parse_file,
                    "exit": exit, "files": self.files, "help": self.help}
        print(">>> Now running: Pdf-Docx\n> Enter 'help' for a list of commands.")
        while True:
            user_input = input("> Enter command:\n> ")
            try:
                try:
                    filename = user_input.split(" ")
                    command = filename[0]
                    pdf_file = filename[1]
                    commands[command](pdf_file)
                except IndexError:
                    command = user_input
                    commands[command]()
            except TypeError and KeyError:
                print(">> Invalid command.")


if __name__ == "__main__":
    ui = UserInterface()
    ui.ui_loop()

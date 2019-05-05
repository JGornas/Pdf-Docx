from pdf_parser import PdfParser


class UserInterface:
    def __init__(self):
        self.datafields = {}

    def parse_pdf(self):
        parser = PdfParser()
        parser.load_pdf(env="venv")
        self.datafields = parser.parse_paragraphs()

    def print_pdf_data(self):
        for key in self.datafields:
            print(f"{key} : {self.datafields[key]}")


def main():
    ui = UserInterface()
    ui.parse_pdf()


if __name__ == "__main__":
    main()

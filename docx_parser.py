from docx import Document
from docx.shared import Pt
from pdf_parser import PdfParser


class DocxParser:
    def __init__(self, pdf_datafields, docx_filename="template.docx"):
        self.document = Document(docx_filename)

        self.datafields = pdf_datafields
        self.cells = ["Oznaczenie sądu", "Siedziba_Wojewodztwo", "Siedziba_Powiat", "Siedziba_Gmina",
                      "Siedziba_Miejscowosc", "KRS", "Firma, pod którą spółka działa", "NIP", "REGON"]
        self.locked_cells = {key: False for key in self.cells}

    def parse_krs(self, cell, cell_name):
        cell.paragraphs[0].text = ""
        if len(self.datafields[cell_name]) is not 10:  # This should be in UI.
            print("> !!! INVALID KRS !!!")
        for liczba in self.datafields[cell_name]:
            paragraph = cell.paragraphs[0].add_run(liczba)
            paragraph.font.size = Pt(10)
            if int(liczba) < 5:
                for i in range(15):
                    paragraph_space = cell.paragraphs[0].add_run(" ")
                    paragraph_space.font.size = Pt(2)
            else:
                for i in range(16):
                    paragraph_space = cell.paragraphs[0].add_run(" ")
                    paragraph_space.font.size = Pt(2)

    def parse_cell(self,cell, cell_name):
        cell.paragraphs[1].style.font.size = Pt(10)
        cell.paragraphs[1].text = self.datafields[cell_name]
        self.locked_cells[cell_name] = True
        print(cell_name, "found and locked!!")

    def parse_dox(self, cell, startswith, cell_name):
        start = {"1.": self.parse_cell, "2.": self.parse_cell, "3.": self.parse_cell,
                 "4.": self.parse_cell, "5.": self.parse_cell, "<KRS>": self.parse_krs}
        if not self.locked_cells[cell_name]:
            start[startswith](cell, cell_name)
        else:
            pass


    def parse_document(self):
        for table in range(len(self.document.tables)):
            try:
                for cell in self.document.tables[table]._cells:
                    #self.parse_cell(cell, startswith="1.", cell_name="Oznaczenie sądu")
                    #self.parse_cell(cell, startswith="2.", cell_name="Siedziba_Wojewodztwo")
                    #self.parse_cell(cell, startswith="3.", cell_name="Siedziba_Powiat")
                    #self.parse_cell(cell, startswith="4.", cell_name="Siedziba_Gmina")
                    #self.parse_cell(cell, startswith="5.", cell_name="Siedziba_Miejscowosc")
                    #self.parse_cell(cell, startswith="<KRS>.", cell_name="KRS")
                    #self.parse_cell(cell, startswith="8.", cell_name="Firma, pod którą spółka działa")
                    #self.parse_cell(cell, startswith="<NIP>", cell_name="NIP")
                    #self.parse_cell(cell, startswith="<REGON>", cell_name="REGON")
                    #self.parse_cell(cell, startswith="DZ.MI", cell_name="Oznaczeniesądu")
                    self.parse_dox(cell, "1.", "Oznaczenie sądu")
            except:
                pass

    def save_document(self):
        self.document.save("test.docx")


parser = PdfParser()
parser.load_pdf(env="venv")
datafields = parser.parse_paragraphs()
print(datafields)
docx = DocxParser(datafields)
docx.parse_document()
docx.save_document()
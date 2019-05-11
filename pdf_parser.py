from subprocess import call
from sys import executable, exec_prefix
import re
import os


class PdfParser:
    def __init__(self, pdf_filename="odpis_aktualny_1.pdf"):
        self.pdf_filename = pdf_filename
        self.txt_filename = f"{pdf_filename.strip('.pdf')}.txt"

        self.datafields = {}  # Holds all parsed data.
        self.cells = ["Firma, pod którą spółka działa", "Oznaczenie sądu", "Siedziba", "Adres",
                      "KRS", "REGON/NIP", "Forma Prawna", "Kapitał Zakładowy", "Wspólnicy", "Zarząd"]
        self.locked_cells = {locked: False for locked in self.cells}  # Locks dictionary key after parsing data.

        self.active = 0  # "Wspólnik: int" or "Zarząd: int" currently worked on.
        self.unicode = "\u00D3\u0104\u0106\u0141\u0143\u015A\u0179\u017B"  # Uppercode for regex patterns.
        self.paragraphs = []  # list of all paragraphs, made from txt file.

    def load_pdf(self, env="default", debug=()):
        """Extracts text from pdf. Debug takes a tuple (from index to index2), empty tuple to skip."""
        os.makedirs("txt", exist_ok=True)
        if env is "default":  # default python path
            call([executable,
                  os.path.join(f"{exec_prefix}", "Scripts", "pdf2txt.py"),
                  os.path.join("pdf", f"{self.pdf_filename}"),
                  os.path.join(f"-otxt", f"{self.txt_filename}")])
        if env is "venv":  # virtual environment
            call([os.path.join("venv", "Scripts", "python.exe"),
                  os.path.join("venv", "Scripts", "pdf2txt.py"),
                  os.path.join("pdf", f"{self.pdf_filename}"),
                  os.path.join(f"-otxt", f"{self.txt_filename}")])
        with open(os.path.join("txt", f"{self.txt_filename}"), "r", encoding="utf-8") as file:
            self.paragraphs = [paragraph.rstrip('\n') for paragraph in file]
        os.remove(os.path.join("txt", f"{self.txt_filename}"))
        if debug:
            for counter, paragraph in enumerate(self.paragraphs):
                try:
                    if int(debug[0]) < counter < int(debug[1]):
                        print(counter, paragraph)
                except TypeError:
                    print("Debug must be a (x,y) touple.")

    def search_index(self, index, cell_name, paragraph):
        """Jumps a fixed number of indexes down the list and creates key: value pair. Next step parsing here.."""
        index = self.paragraphs.index(paragraph) + index
        if paragraph.startswith("1.Siedziba"):
            kraj, wojewodztwo, powiat, gmina, miejscowosc = self.paragraphs[index].split(",")
            miejscowosc = miejscowosc.strip("  miejsc.")
            self.datafields["Siedziba_Kraj"] = kraj.strip("kraj ")
            self.datafields["Siedziba_Wojewodztwo"] = wojewodztwo.strip("woj. ")
            self.datafields["Siedziba_Powiat"] = powiat.strip("  powiat ")
            self.datafields["Siedziba_Gmina"] = gmina.strip("  gmina ")
            self.datafields["Siedziba_Miejscowosc"] = miejscowosc
        if paragraph.startswith("2.Adres"):
            ulica, numer, lokal, miejscowosc, kod, poczta, kraj = self.paragraphs[index].split(",")
            self.datafields["Adres_Ulica"] = ulica.strip("ul.  ")
            self.datafields["Adres_Numer"] = numer.strip(" nr ")
            self.datafields["Adres_Lokal"] = lokal.strip("lok. ")
            self.datafields["Adres_Miejscowosc"] = miejscowosc.strip("  miejsc.")
            self.datafields["Adres_Kod"] = kod.strip(" kod ")
            self.datafields["Adres_Poczta"] = poczta.strip(" poczta ")
            self.datafields["Adres_Kraj"] = kraj.strip("kraj ")
        if paragraph.startswith("2.Numer REGON/NIP"):
            regon, nip = self.paragraphs[index].split(",")
            self.datafields["NIP"] = nip.strip("  NIP: ").split()[0].strip("---")
            self.datafields["REGON"] = regon.strip("REGON: ").split()[0]
        else:
            if self.paragraphs[index + 1] is not "":  # for multiline text cells
                self.paragraphs[index] += f" {self.paragraphs[index + 1]}"
            self.datafields[cell_name] = self.paragraphs[index]
        self.locked_cells[cell_name] = True

    def search_loop(self, pattern, parent, cell_name, paragraph):
        """Takes pattern for regex search and returns the outcome out of the loop."""
        index = self.paragraphs.index(paragraph)
        self.paragraphs[index] = ""
        while True:
            index += 1
            try:
                para = self.paragraphs[index].rstrip()
                try:
                    if re.match(pattern, para):
                        self.datafields[f"{parent} {self.active}"][cell_name] = para
                        self.paragraphs[index] = ""
                        break
                    if index is len(self.paragraphs):
                        break
                except KeyError:
                    pass
            except IndexError:
                break

    def parse_paragraphs(self):
        """Iterates through the string list. On match uses either search_index or search_loop."""
        paragraphs = self.paragraphs
        for paragraph in paragraphs:
            try:
                if paragraph == "Oznaczenie sądu" and not self.locked_cells["Oznaczenie sądu"]:
                    self.search_index(4, "Oznaczenie sądu", paragraph)

                if paragraph.startswith("3.Firma,") and not self.locked_cells["Firma, pod którą spółka działa"]:
                    self.search_index(2, "Firma, pod którą spółka działa", paragraph)

                if paragraph.startswith("3.Nazwa") and not self.locked_cells["Firma, pod którą spółka działa"]:
                    self.search_index(2, "Firma, pod którą spółka działa", paragraph)

                if paragraph.startswith("1.Siedziba") and not self.locked_cells["Siedziba"]:
                    self.search_index(4, "Siedziba", paragraph)

                if paragraph.startswith("2.Adres") and not self.locked_cells["Adres"]:
                    self.search_index(4, "Adres", paragraph)

                if paragraph.startswith("Numer KRS") and not self.locked_cells["KRS"]:
                    self.datafields["KRS"] = paragraph.split()[-1]
                    self.locked_cells["KRS"] = True

                if paragraph.startswith("2.Numer REGON/NIP") and not self.locked_cells["REGON/NIP"]:
                    self.search_index(2, "REGON/NIP", paragraph)

                if paragraph.startswith("1.Oznaczenie formy prawnej") and not self.locked_cells["Forma Prawna"]:
                    self.search_index(2, "Forma Prawna", paragraph)

                if paragraph.startswith("1.Wysokość kapitału zakładowego"):
                    self.search_index(2, "Kapitał Zakładowy", paragraph)

                if paragraph.startswith("5.Kwotowe określenie części kapitału wpłaconego"):
                    self.search_index(2, "Kapitał Wpłacony", paragraph)

                if paragraph.startswith("Rubryka 7 - Dane wspólników"):  # Open "Wspólnicy" parsing block.
                    self.locked_cells["Wspólnicy"] = True

                if paragraph.startswith("Rubryka 7 - Komitet założycielski"):  # STOWARZYSZENIE
                    break

                if paragraph.startswith("1.Nazwisko / Nazwa lub firma") and self.locked_cells["Wspólnicy"]:
                    self.active += 1
                    self.datafields[f"Wspólnik {self.active}"] = {}

                    pattern = rf"^[A-Z{self.unicode}]+"
                    self.search_loop(pattern, "Wspólnik", "Nazwisko/Nazwa", paragraph)

                if paragraph.startswith("2.Imiona") and self.locked_cells["Wspólnicy"]:
                    pattern = rf"[A-Z{self.unicode}]+\s[A-Z{self.unicode}]+$|^[A-Z{self.unicode}]+$|^[*]+$"
                    self.search_loop(pattern, "Wspólnik", "Imiona", paragraph)

                if paragraph.startswith("3.Numer PESEL/REGON") and self.locked_cells["Wspólnicy"]:
                    pattern = r"[-]+|[0-9]{9,11}"
                    self.search_loop(pattern, "Wspólnik", "PESEL/REGON", paragraph)

                if paragraph.startswith("4.Numer KRS") and self.locked_cells["Wspólnicy"]:
                    pattern = r"[-]+|[*]+|[0-9]{10}$"
                    self.search_loop(pattern, "Wspólnik", "KRS", paragraph)

                if paragraph.startswith("5.Posiadane przez wspólnika udziały"):
                    index = paragraphs.index(paragraph)
                    line_1 = paragraphs[index + 2].strip(" ")
                    line_2 = paragraphs[index + 3].strip(" ")
                    if line_2:
                        self.datafields[f"Wspólnik {self.active}"]["Udziały"] = f"{line_1} {line_2}"
                    else:
                        self.datafields[f"Wspólnik {self.active}"]["Udziały"] = f"{line_1}"

                if paragraph == "ZARZĄD":
                    self.locked_cells["Wspólnicy"] = False  # Close "Wspólnicy" parsing block.
                    self.locked_cells["Zarząd"] = True  # Open "Zarząd" parsing block.
                    self.active = 0

                if paragraph.startswith("1.Nazwisko") and self.locked_cells["Zarząd"]:
                    self.active += 1
                    self.datafields[f"Zarząd {self.active}"] = {}
                    pattern = rf"^[A-Z{self.unicode}]+"
                    self.search_loop(pattern, "Zarząd", "Nazwisko/Nazwa", paragraph)

                if paragraph.startswith("2.Imiona") and self.locked_cells["Zarząd"]:
                    pattern = rf"^[A-Z{self.unicode}]+\s[A-Z{self.unicode}]+$|^[A-Z{self.unicode}]+$|^[*]+$"
                    self.search_loop(pattern, "Zarząd", "Imiona", paragraph)

                if paragraph.startswith("5.Funkcja w organie ") and self.locked_cells["Zarząd"]:
                    paragraph = paragraph.strip("5.Funkcja w organie reprezentującym ")
                    self.datafields[f"Zarząd {self.active}"]["Funkcja"] = paragraph

                if paragraph.startswith("Rubryka 2 - Organ nadzoru"):
                    self.locked_cells["Zarząd"] = False  # Close "Zarząd" parsing block.
            except KeyError:
                pass
        return self.datafields


if __name__ == "__main__":  # DEBUG ONLY
    parser = PdfParser(pdf_filename="odpis_aktualny_4.pdf")
    parser.load_pdf(env="venv", debug=(0, 500))
    datafields = parser.parse_paragraphs()
    for key in datafields:
        print(f"{key} : {datafields[key]}")

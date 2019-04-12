from subprocess import call
import os
import re

class PdfParser:
    def __init__(self, pdf_filename="odpis_aktualny_1.pdf"):
        self.pdf_filename = pdf_filename
        self.txt_filename = f"{pdf_filename.strip('.pdf')}.txt"

        self.datafields = {}
        self.parsed_state = {
                            "Firma, pod którą spółka działa": False,  "Oznaczenie sądu": False, "Siedziba": False,
                            "KRS": False, "REGON/NIP": False, "Adres": False, "Forma Prawna": False,
                            "Kapitał Zakładowy": False, "Wspólnicy": False, "Zarząd": False,
                             }
        self.active = 0
        self.unicode = "\u00D3\u0104\u0106\u0141\u0143\u015A\u0179\u017B"

    def search_byindex(self, index, paragraph, paragraphs, cell_name):
        index = paragraphs.index(paragraph) + index
        if paragraphs[index + 1] is not "":  # for multiline text cells
            paragraphs[index] += f" {paragraphs[index + 1]}"
        self.datafields[cell_name] = paragraphs[index]
        self.parsed_state[cell_name] = True

    def search_byloop(self):
        pass

    def load_pdf(self, remove_txt=True, debug=False, debug_range=(0, 500)):
        call([os.path.join("venv", "Scripts", "python.exe"),
              os.path.join("venv", "Scripts", "pdf2txt.py"),
              os.path.join("pdf", f"{self.pdf_filename}"),
              os.path.join(f"-otxt", f"{self.txt_filename}")])
        with open(os.path.join("txt", f"{self.txt_filename}"), "r", encoding="utf-8") as file:
            paragraphs = [paragraph.rstrip('\n') for paragraph in file]
        if remove_txt:
            os.remove(os.path.join("txt", f"{self.txt_filename}"))
        if debug:
            for counter, paragraph in enumerate(paragraphs):
                if debug_range[0] < counter < debug_range[1]:
                    print(counter, paragraph)

        for paragraph in paragraphs:
            if paragraph == "Oznaczenie sądu" and self.parsed_state["Oznaczenie sądu"] is False:
                #index = paragraphs.index(paragraph) + 4
                #if paragraphs[index + 1] is not "":  # for multiline text cells
                #    paragraphs[index] += f" {paragraphs[index + 1]}"
                #self.datafields["Oznaczenie sądu"] = paragraphs[index]
                self.search_byindex(4, paragraph, paragraphs, "Oznaczenie sądu")

            if paragraph.startswith("3.Firma,") and self.parsed_state["Firma, pod którą spółka działa"] is False:
                index = paragraphs.index(paragraph) + 2
                self.datafields["Firma, pod którą spółka działa"] = paragraphs[index]
                self.parsed_state["Firma, pod którą spółka działa"] = True

            if paragraph.startswith("1.Siedziba") and self.parsed_state["Siedziba"] is False:
                index = paragraphs.index(paragraph) + 4
                kraj, wojewodztwo, powiat, gmina, miejscowosc = paragraphs[index].split(",")
                miejscowosc = miejscowosc.strip("  miejsc.")
                self.datafields["Siedziba_Kraj"] = kraj.strip("kraj ")
                self.datafields["Siedziba_Wojewodztwo"] = wojewodztwo.strip("woj. ")
                self.datafields["Siedziba_Powiat"] = powiat.strip("  powiat ")
                self.datafields["Siedziba_Gmina"] = gmina.strip("  gmina ")
                self.datafields["Siedziba_Miejscowosc"] = miejscowosc
                self.parsed_state["Siedziba"] = True

            if paragraph.startswith("2.Adres") and self.parsed_state["Adres"] is False:
                index = paragraphs.index(paragraph) + 4
                ulica, numer, lokal, miejscowosc, kod, poczta, kraj = paragraphs[index].split(",")
                miejscowosc = miejscowosc.strip("  miejsc.")
                if miejscowosc == "":  # checks for a newline
                    index = index + 1
                    miejscowosc = paragraphs[index]
                self.datafields["Adres_Ulica"] = ulica.strip("ul.  ")
                self.datafields["Adres_Numer"] = numer.strip(" nr ")
                self.datafields["Adres_Lokal"] = lokal.strip("lok. ")
                self.datafields["Adres_Miejscowosc"] = miejscowosc
                self.datafields["Adres_Kod"] = kod.strip(" kod ")
                self.datafields["Adres_Poczta"] = poczta.strip(" poczta ")
                self.datafields["Adres_Kraj"] = kraj.strip("kraj ")
                self.parsed_state["Adres"] = True

            if paragraph.startswith("Numer KRS") and self.parsed_state["KRS"] is False:
                self.datafields["KRS"] = paragraph.split()[-1]
                self.parsed_state["KRS"] = True

            if paragraph.startswith("2.Numer REGON/NIP") and self.parsed_state["REGON/NIP"] is False:
                index = paragraphs.index(paragraph) + 2
                regon, nip = paragraphs[index].split(",")
                self.datafields["NIP"] = nip.strip("  NIP: ").split()[0].strip("---")
                self.datafields["REGON"] = regon.strip("REGON: ").split()[0]
                self.parsed_state["KRS"] = True

            if paragraph.startswith("1.Oznaczenie formy prawnej") and self.parsed_state["Forma Prawna"] is False:
                index = paragraphs.index(paragraph) + 2
                self.datafields["Forma Prawna"] = paragraphs[index]
                self.parsed_state["Forma Prawna"] = True

            if paragraph.startswith("1.Wysokość kapitału zakładowego"):
                index = paragraphs.index(paragraph) + 2
                self.datafields["Kapitał Zakładowy"] = paragraphs[index]
                self.parsed_state["Kapitał Zakładowy"] = True

            if paragraph.startswith("1.Nazwisko / Nazwa lub firma"):
                self.parsed_state["Wspólnicy"] = True
                self.active += 1
                self.datafields[f"Wspólnik {self.active}"] = {}
                pattern = r"^[A-Z\u00D3\u0104\u0106\u0141\u0143\u015A\u0179\u017B]+"
                index = paragraphs.index(paragraph)
                paragraphs[index] = "parsed"
                while True:
                    index += 1
                    if re.match(pattern, paragraphs[index]):
                        self.datafields[f"Wspólnik {self.active}"]["Nazwisko/Nazwa"] = paragraphs[index].rstrip()
                        break

            if paragraph.startswith("2.Imiona") and self.parsed_state["Wspólnicy"]:
                pattern = rf"[A-Z{self.unicode}]+\s[A-Z{self.unicode}]+$|^[A-Z{self.unicode}]+$|^[*]+$"
                index = paragraphs.index(paragraph)
                paragraphs[index] = "parsed"
                while True:
                    index += 1
                    if re.match(pattern, paragraphs[index]):
                        self.datafields[f"Wspólnik {self.active}"]["Imiona"] = paragraphs[index].rstrip()
                        paragraphs[index] = "parsed"
                        break

            if paragraph.startswith("3.Numer PESEL/REGON") and self.parsed_state["Wspólnicy"]:
                pattern = r"[-]+|[0-9]{9,11}"
                index = paragraphs.index(paragraph)
                paragraphs[index] = "parsed"
                while True:
                    index += 1
                    if re.match(pattern, paragraphs[index]):
                        self.datafields[f"Wspólnik {self.active}"]["PESEL/REGON"] = paragraphs[index].rstrip()
                        paragraphs[index] = "parsed"
                        break
                    if index == len(paragraphs):
                        break

            if paragraph.startswith("4.Numer KRS") and self.parsed_state["Wspólnicy"]:
                pattern = r"[-]+|[*]+|[0-9]{10}$"
                index = paragraphs.index(paragraph)
                paragraphs[index] = "parsed"
                while True:
                    index += 1
                    if re.match(pattern, paragraphs[index]):
                        self.datafields[f"Wspólnik {self.active}"]["KRS"] = paragraphs[index].rstrip()
                        paragraphs[index] = "parsed"
                        break
                    if index == len(paragraphs):
                        break

            if paragraph.startswith("5.Posiadane przez wspólnika udziały"):
                index = paragraphs.index(paragraph)
                line_1 = paragraphs[index + 2].strip(" ")
                line_2 = paragraphs[index + 3].strip(" ")
                if line_2:
                    self.datafields[f"Wspólnik {self.active}"]["Udziały"] = f"{line_1} {line_2}"
                else:
                    self.datafields[f"Wspólnik {self.active}"]["Udziały"] = f"{line_1}"
            if paragraph == "ZARZĄD":
                self.parsed_state["Wspólnicy"] = False
                self.parsed_state["Zarząd"] = True
                self.active = 0

            if paragraph.startswith("1.Nazwisko / Nazwa lub Firma") and self.parsed_state["Zarząd"]:
                self.active += 1
                self.datafields[f"Zarząd {self.active}"] = {}
                pattern = r"^[A-Z\u00D3\u0104\u0106\u0141\u0143\u015A\u0179\u017B]+"
                index = paragraphs.index(paragraph)
                paragraphs[index] = "parsed"
                while True:
                    index += 1
                    if re.match(pattern, paragraphs[index].rstrip()):
                        self.datafields[f"Zarząd {self.active}"]["Nazwisko/Nazwa"] = paragraphs[index].rstrip()
                        break

            if paragraph.startswith("2.Imiona") and self.parsed_state["Zarząd"]:
                pattern = rf"^[A-Z{self.unicode}]+\s[A-Z{self.unicode}]+$|^[A-Z{self.unicode}]+$|^[*]+$"
                index = paragraphs.index(paragraph)
                paragraphs[index] = "parsed"
                while True:
                    if re.match(pattern, paragraphs[index].rstrip()):
                        self.datafields[f"Zarząd {self.active}"]["Imiona"] = paragraphs[index].rstrip()
                        paragraphs[index] = "parsed"
                        break
                    index += 1

            if paragraph.startswith("5.Funkcja w organie ") and self.parsed_state["Zarząd"]:
                paragraph = paragraph.strip("5.Funkcja w organie reprezentującym ")
                self.datafields[f"Zarząd {self.active}"]["Funkcja"] = paragraph

            if paragraph.startswith("Rubryka 2 - Organ nadzoru"):
                self.parsed_state["Zarząd"] = False
        return self.datafields


if __name__ == "__main__":
    parser = PdfParser(pdf_filename="odpis_aktualny_5.pdf")
    datafields = parser.load_pdf(debug=True, debug_range=(200, 365))
    for key in datafields:
        print(f"{key} : {datafields[key]}")


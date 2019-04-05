from subprocess import call
import os


class PdfParser:
    def __init__(self, pdf_filename="odpis_aktualny_1.pdf"):
        self.pdf_filename = pdf_filename
        self.txt_filename = f"{pdf_filename.strip('.pdf')}.txt"

        self.variables = {}
        self.parsed_state = {
                            "Firma, pod którą spółka działa": False, "Oznaczenie sądu": False, "Siedziba": False,
                            "KRS": False, "REGON/NIP": False, "Adres": False, "Forma Prawna": False,
                            "Kapitał Zakładowy": False, "Wspólnicy": 1, "Członków Zarządu": 0,
                             }

    def load_pdf(self, remove_txt=True, debug=False):
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
                if counter < 400:
                    print(counter, paragraph)
        for paragraph in paragraphs:

            if paragraph == "Oznaczenie sądu" and self.parsed_state["Oznaczenie sądu"] is False:
                index = paragraphs.index(paragraph) + 4
                oznaczenie = paragraphs[index]
                check = paragraphs[index + 1]
                if check is not "":  # checks for a newline (bugfix)
                    oznaczenie += f" {check}"
                self.variables["Oznaczenie sądu"] = oznaczenie

            if paragraph.startswith("3.Firma,") and self.parsed_state["Firma, pod którą spółka działa"] is False:
                index = paragraphs.index(paragraph) + 2
                self.variables["Firma, pod którą spółka działa"] = paragraphs[index]
                self.parsed_state["3.Firma"] = True

            if paragraph.startswith("1.Siedziba") and self.parsed_state["Siedziba"] is False:
                index = paragraphs.index(paragraph) + 4
                kraj, wojewodztwo, powiat, gmina, miejscowosc = paragraphs[index].split(",")
                miejscowosc = miejscowosc.strip("  miejsc.")
                if miejscowosc == "":  # checks for a newline
                    index = index + 1
                    miejscowosc = paragraphs[index]
                self.variables["Siedziba_Kraj"] = kraj.strip("kraj ")
                self.variables["Siedziba_Wojewodztwo"] = wojewodztwo.strip("woj. ")
                self.variables["Siedziba_Powiat"] = powiat.strip("  powiat ")
                self.variables["Siedziba_Gmina"] = gmina.strip("  gmina ")
                self.variables["Siedziba_Miejscowosc"] = miejscowosc
                self.parsed_state["Siedziba"] = True

            if paragraph.startswith("2.Adres") and self.parsed_state["Adres"] is False:
                index = paragraphs.index(paragraph) + 4
                ulica, numer, lokal, miejscowosc, kod, poczta, kraj = paragraphs[index].split(",")
                miejscowosc = miejscowosc.strip("  miejsc.")
                if miejscowosc == "":  # checks for a newline
                    index = index + 1
                    miejscowosc = paragraphs[index]
                self.variables["Adres_Ulica"] = ulica.strip("ul.  ")
                self.variables["Adres_Numer"] = numer.strip(" nr ")
                self.variables["Adres_Lokal"] = lokal.strip("lok. ")
                self.variables["Adres_Miejscowosc"] = miejscowosc
                self.variables["Adres_Kod"] = kod.strip(" kod ")
                self.variables["Adres_Poczta"] = poczta.strip(" poczta ")
                self.variables["Adres_Kraj"] = kraj.strip("kraj ")
                self.parsed_state["Adres"] = True

            if paragraph.startswith("Numer KRS") and self.parsed_state["KRS"] is False:
                self.variables["KRS"] = paragraph.split()[-1]
                self.parsed_state["KRS"] = True

            if paragraph.startswith("2.Numer REGON/NIP") and self.parsed_state["REGON/NIP"] is False:
                index = paragraphs.index(paragraph) + 2
                regon, nip = paragraphs[index].split(",")
                self.variables["NIP"] = nip.strip("  NIP: ").split()[0].strip("---")
                self.variables["REGON"] = regon.strip("REGON: ").split()[0]
                self.parsed_state["KRS"] = True

            if paragraph.startswith("1.Oznaczenie formy prawnej") and self.parsed_state["Forma Prawna"] is False:
                index = paragraphs.index(paragraph) + 2
                self.variables["Forma Prawna"] = paragraphs[index]
                self.parsed_state["Forma Prawna"] = True

            if paragraph.startswith("1.Wysokość kapitału zakładowego"):
                index = paragraphs.index(paragraph) + 2
                self.variables["Kapitał Zakładowy"] = paragraphs[index]
                self.parsed_state["Kapitał Zakładowy"] = True

            if paragraph.startswith("Rubryka 7 - Dane wspólników"):
                index = paragraphs.index(paragraph) + 2
                count = 0
                while True:
                    if paragraphs[index] == str(int(count) + 1):
                        count += 1
                        index += 2
                    else:
                        break
                self.variables["Wspólników"] = count
                for i in range(1, count+1):
                    self.variables[f"Wspólnik: {i}"] = {"Nazwisko / Nazwa lub firma": "", "Imiona": "",
                                                        "Numer PESEL/REGON": "", "Numer KRS": "",
                                                        "Posiadane Udziały": "", "Complete": False}

            if paragraph.startswith("1.Nazwisko / Nazwa lub firma") and self.parsed_state["Wspólnicy"] < self.variables["Wspólników"]+1:
                print(self.parsed_state["Wspólnicy"], self.variables["Wspólników"])
                index = paragraphs.index(paragraph) + 2
                paragraph = paragraphs[index]
                self.variables[f"Wspólnik: {self.parsed_state['Wspólnicy']}"]["Nazwisko / Nazwa lub firma"] = paragraph
                self.parsed_state["Wspólnicy"] += 1


            if paragraph.startswith("Dane osób wchodzących w skład organu"):
                index = paragraphs.index(paragraph) + 2
                count = 0
                while True:
                    if paragraphs[index] == str(int(count) + 1):
                        count += 1
                        index += 2
                    else:
                        break
                self.variables["Członków Zarządu"] = count
                for i in range(1, count+1):
                    self.variables[f"Członek Zarządu: {i}"] = {"Nazwisko / Nazwa lub firma": "", "Imiona": "",
                                                               "Numer PESEL/REGON": "", "Numer KRS": "",
                                                               "Funkcja": ""}

        return self.variables


if __name__ == "__main__":
    parser = PdfParser()
    variables = parser.load_pdf(debug=True)
    for key in variables:
        print(f"{key} : {variables[key]}")


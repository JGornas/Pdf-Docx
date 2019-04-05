import unittest
from new_parser import PdfParser


class TestPdfParser(unittest.TestCase):

    def test_extract_pdf(self):
        parser = PdfParser()
        parser.pdf_filename = "odpis_aktualny_1.pdf"
        variables = parser.load_pdf(remove_txt=False, debug=False)
        self.assertEqual(variables["Firma, pod którą spółka działa"],
                         "MODELARNIA SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ")
        self.assertEqual(variables["Oznaczenie sądu"],
                         "SĄD REJONOWY POZNAŃ - NOWE MIASTO I WILDA W POZNANIU,"
                         " VIII WYDZIAŁ GOSPODARCZY KRAJOWEGO REJESTRU SĄDOWEGO")
        self.assertEqual(variables["Siedziba_Kraj"], "POLSKA")
        self.assertEqual(variables["Siedziba_Wojewodztwo"], "WIELKOPOLSKIE")
        self.assertEqual(variables["Siedziba_Powiat"], "POZNAŃ")
        self.assertEqual(variables["Siedziba_Gmina"], "POZNAŃ")
        self.assertEqual(variables["Siedziba_Miejscowosc"], "POZNAŃ")
        self.assertEqual(variables["KRS"], "0000551026")
        self.assertEqual(variables["NIP"], "7831724589")
        self.assertEqual(variables["REGON"], "361131194")

        self.assertEqual(variables["Adres_Ulica"], "3 MAJA")
        self.assertEqual(variables["Adres_Numer"], "49C")
        self.assertEqual(variables["Adres_Lokal"], "2A")
        self.assertEqual(variables["Adres_Miejscowosc"], "POZNAŃ")
        self.assertEqual(variables["Adres_Kod"], "61-728")
        self.assertEqual(variables["Adres_Poczta"], "POZNAŃ")
        self.assertEqual(variables["Adres_Kraj"], "POLSKA")

        self.assertEqual(variables["Forma Prawna"], "SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ")
        self.assertEqual(variables["Kapitał Zakładowy"], "6 000,00 ZŁ")

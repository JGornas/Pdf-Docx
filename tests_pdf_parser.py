import unittest
from pdf_parser import PdfParser


class TestPdfParser(unittest.TestCase):

    def test_pdf_1(self):
        parser = PdfParser()
        parser.pdf_filename = "odpis_aktualny_1.pdf"
        parser.load_pdf(remove_txt=False, debug=False)
        datafields = parser.parse_paragraphs()
        self.assertEqual(datafields["Firma, pod którą spółka działa"],
                         "MODELARNIA SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ")
        self.assertEqual(datafields["Oznaczenie sądu"],
                         "SĄD REJONOWY POZNAŃ - NOWE MIASTO I WILDA W POZNANIU,"
                         " VIII WYDZIAŁ GOSPODARCZY KRAJOWEGO REJESTRU SĄDOWEGO")
        self.assertEqual(datafields["Forma Prawna"], "SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ")
        self.assertEqual(datafields["KRS"], "0000551026")
        self.assertEqual(datafields["NIP"], "7831724589")
        self.assertEqual(datafields["REGON"], "361131194")

        self.assertEqual(datafields["Siedziba_Kraj"], "POLSKA")
        self.assertEqual(datafields["Siedziba_Wojewodztwo"], "WIELKOPOLSKIE")
        self.assertEqual(datafields["Siedziba_Powiat"], "POZNAŃ")
        self.assertEqual(datafields["Siedziba_Gmina"], "POZNAŃ")
        self.assertEqual(datafields["Siedziba_Miejscowosc"], "POZNAŃ")

        self.assertEqual(datafields["Adres_Ulica"], "3 MAJA")
        self.assertEqual(datafields["Adres_Numer"], "49C")
        self.assertEqual(datafields["Adres_Lokal"], "2A")
        self.assertEqual(datafields["Adres_Miejscowosc"], "POZNAŃ")
        self.assertEqual(datafields["Adres_Kod"], "61-728")
        self.assertEqual(datafields["Adres_Poczta"], "POZNAŃ")
        self.assertEqual(datafields["Adres_Kraj"], "POLSKA")

        self.assertEqual(datafields["Kapitał Zakładowy"], "6 000,00 ZŁ")
        self.assertEqual(datafields["Wspólnik 1"]["Nazwisko/Nazwa"], "STĘPIEŃ")
        self.assertEqual(datafields["Wspólnik 1"]["Imiona"], "MIKOŁAJ DANIEL")
        self.assertEqual(datafields["Wspólnik 1"]["PESEL/REGON"], "81121003839")
        self.assertEqual(datafields["Wspólnik 1"]["KRS"], "*****")
        self.assertEqual(datafields["Wspólnik 1"]["Udziały"], "40 UDZIAŁÓW O ŁĄCZNEJ WARTOŚCI 2.000,00 ZŁ")

        self.assertEqual(datafields["Wspólnik 2"]["Nazwisko/Nazwa"], "GOLEC")
        self.assertEqual(datafields["Wspólnik 2"]["Imiona"], "NORBERT TOMASZ")
        self.assertEqual(datafields["Wspólnik 2"]["PESEL/REGON"], "81082106275")
        self.assertEqual(datafields["Wspólnik 2"]["KRS"], "*****")
        self.assertEqual(datafields["Wspólnik 2"]["Udziały"], "40 UDZIAŁÓW O ŁĄCZNEJ WARTOŚCI 2.000,00 ZŁ")

        self.assertEqual(datafields["Wspólnik 3"]["Nazwisko/Nazwa"], "ANDRYS")
        self.assertEqual(datafields["Wspólnik 3"]["Imiona"], "KORNEL FILIP")
        self.assertEqual(datafields["Wspólnik 3"]["PESEL/REGON"], "81103103078")
        self.assertEqual(datafields["Wspólnik 3"]["KRS"], "*****")
        self.assertEqual(datafields["Wspólnik 3"]["Udziały"], "40 UDZIAŁÓW O ŁĄCZNEJ WARTOŚCI 2.000,00 ZŁ")

        self.assertEqual(datafields["Zarząd 1"]["Nazwisko/Nazwa"], "STĘPIEŃ")
        self.assertEqual(datafields["Zarząd 1"]["Imiona"], "MIKOŁAJ DANIEL")
        self.assertEqual(datafields["Zarząd 1"]["Funkcja"], "CZŁONEK ZARZĄDU")

        self.assertEqual(datafields["Zarząd 2"]["Nazwisko/Nazwa"], "GOLEC")
        self.assertEqual(datafields["Zarząd 2"]["Imiona"], "NORBERT TOMASZ")
        self.assertEqual(datafields["Zarząd 2"]["Funkcja"], "CZŁONEK ZARZĄDU")

        self.assertEqual(datafields["Zarząd 3"]["Nazwisko/Nazwa"], "ANDRYS")
        self.assertEqual(datafields["Zarząd 3"]["Imiona"], "KORNEL FILIP")
        self.assertEqual(datafields["Zarząd 3"]["Funkcja"], "CZŁONEK ZARZĄDU")

    def test_pdf_3(self):
        parser = PdfParser()
        parser.pdf_filename = "odpis_aktualny_3.pdf"
        parser.load_pdf(remove_txt=False, debug=False)
        datafields = parser.parse_paragraphs()
        self.assertEqual(datafields["Firma, pod którą spółka działa"],
                         "SECO/WARWICK SERVICES SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ")
        self.assertEqual(datafields["Oznaczenie sądu"],
                         "SĄD REJONOWY  W ZIELONEJ GÓRZE,"
                         " VIII WYDZIAŁ GOSPODARCZY KRAJOWEGO REJESTRU SĄDOWEGO")
        self.assertEqual(datafields["Siedziba_Kraj"], "POLSKA")
        self.assertEqual(datafields["Siedziba_Wojewodztwo"], "LUBUSKIE")
        self.assertEqual(datafields["Siedziba_Powiat"], "ŚWIEBODZIŃSKI")
        self.assertEqual(datafields["Siedziba_Gmina"], "ŚWIEBODZIN")
        self.assertEqual(datafields["Siedziba_Miejscowosc"], "ŚWIEBODZIN")
        self.assertEqual(datafields["KRS"], "0000590289")
        self.assertEqual(datafields["NIP"], "9271938125")
        self.assertEqual(datafields["REGON"], "363190781")

        self.assertEqual(datafields["Adres_Ulica"], "ZACHODNIA")
        self.assertEqual(datafields["Adres_Numer"], "76")
        self.assertEqual(datafields["Adres_Lokal"], "---")
        self.assertEqual(datafields["Adres_Miejscowosc"], "ŚWIEBODZIN")
        self.assertEqual(datafields["Adres_Kod"], "66-200")
        self.assertEqual(datafields["Adres_Poczta"], "ŚWIEBODZIN")
        self.assertEqual(datafields["Adres_Kraj"], "POLSKA")

        self.assertEqual(datafields["Forma Prawna"], "SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ")
        self.assertEqual(datafields["Kapitał Zakładowy"], "2 410 000,00 ZŁ")
        self.assertEqual(datafields["Wspólnik 1"]["Nazwisko/Nazwa"], "SECO/WARWICK SPÓŁKA AKCYJNA")
        self.assertEqual(datafields["Wspólnik 1"]["Imiona"], "*****")
        self.assertEqual(datafields["Wspólnik 1"]["PESEL/REGON"], "970011679")
        self.assertEqual(datafields["Wspólnik 1"]["KRS"], "0000271014")
        self.assertEqual(datafields["Wspólnik 1"]["Udziały"], "24.100 UDZIAŁÓW O ŁĄCZNEJ WARTOŚCI 2.410.000,00 ZŁ")

        self.assertEqual(datafields["Zarząd 1"]["Nazwisko/Nazwa"], "SZADKOWSKI")
        self.assertEqual(datafields["Zarząd 1"]["Imiona"], "ROBERT")
        self.assertEqual(datafields["Zarząd 1"]["Funkcja"], "CZŁONEK ZARZĄDU")

        self.assertEqual(datafields["Zarząd 2"]["Nazwisko/Nazwa"], "TOMASZEWSKA KOWALSKA")
        self.assertEqual(datafields["Zarząd 2"]["Imiona"], "KATARZYNA ROBERTA")
        self.assertEqual(datafields["Zarząd 2"]["Funkcja"], "CZŁONEK ZARZĄDU")

    def test_pdf_mouser(self):
        parser = PdfParser()
        parser.pdf_filename = "odpis_aktualny_Mouser.pdf"
        parser.load_pdf(remove_txt=False, debug=False)
        datafields = parser.parse_paragraphs()
        self.assertEqual(datafields["Firma, pod którą spółka działa"],
                         "MOUSER POLAND SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ")
        self.assertEqual(datafields["Oznaczenie sądu"],
                         "------")
        self.assertEqual(datafields["Siedziba_Kraj"], "POLSKA")
        self.assertEqual(datafields["Siedziba_Wojewodztwo"], "DOLNOŚLĄSKIE")
        self.assertEqual(datafields["Siedziba_Powiat"], "WROCŁAW")
        self.assertEqual(datafields["Siedziba_Gmina"], "WROCŁAW")
        self.assertEqual(datafields["Siedziba_Miejscowosc"], "WROCŁAW")
        self.assertEqual(datafields["KRS"], "0000758939")
        self.assertEqual(datafields["NIP"], "8992853938")
        self.assertEqual(datafields["REGON"], "381866678")

        self.assertEqual(datafields["Adres_Ulica"], "WYŚCIGOWA")
        self.assertEqual(datafields["Adres_Numer"], "56E")
        self.assertEqual(datafields["Adres_Lokal"], "---")
        self.assertEqual(datafields["Adres_Miejscowosc"], "WROCŁAW")
        self.assertEqual(datafields["Adres_Kod"], "53-012")
        self.assertEqual(datafields["Adres_Poczta"], "WROCŁAW")
        self.assertEqual(datafields["Adres_Kraj"], "POLSKA")

        self.assertEqual(datafields["Forma Prawna"], "SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ")
        self.assertEqual(datafields["Kapitał Zakładowy"], "5 000,00 ZŁ")

        self.assertEqual(datafields["Wspólnik 1"]["Nazwisko/Nazwa"], "MOUSER ELECTRONICS INC.")
        self.assertEqual(datafields["Wspólnik 1"]["Imiona"], "*****")
        self.assertEqual(datafields["Wspólnik 1"]["PESEL/REGON"], "---")
        self.assertEqual(datafields["Wspólnik 1"]["KRS"], "----------")
        self.assertEqual(datafields["Wspólnik 1"]["Udziały"],
                         "49 (CZTERDZIEŚCI DZIEWIĘĆ) UDZIAŁÓW O ŁĄCZNEJ WYSOKOŚCI 4.950,00 (CZTERY TYSIĄCE"
                         " DZIEWIĘĆSET PIĘĆDZIESIĄT) ZŁOTYCH")

        self.assertEqual(datafields["Zarząd 1"]["Nazwisko/Nazwa"], "BROWN")
        self.assertEqual(datafields["Zarząd 1"]["Imiona"], "SCOTT LESLIE")
        self.assertEqual(datafields["Zarząd 1"]["Funkcja"], "PREZES ZARZĄDU")

    def test_pdf_Seco(self):
        parser = PdfParser()
        parser.pdf_filename = "odpis_aktualny_Seco.pdf"
        parser.load_pdf(remove_txt=False, debug=False)
        datafields = parser.parse_paragraphs()
        self.assertEqual(datafields["Firma, pod którą spółka działa"],
                         "SECO/WARWICK SPÓŁKA AKCYJNA")
        self.assertEqual(datafields["Oznaczenie sądu"],
                         "SĄD REJONOWY  W ZIELONEJ GÓRZE,"
                         " VIII WYDZIAŁ GOSPODARCZY KRAJOWEGO REJESTRU SĄDOWEGO")
        self.assertEqual(datafields["Forma Prawna"], "SPÓŁKA AKCYJNA")
        self.assertEqual(datafields["KRS"], "0000271014")
        self.assertEqual(datafields["NIP"], "9270100756")
        self.assertEqual(datafields["REGON"], "970011679")

        self.assertEqual(datafields["Siedziba_Kraj"], "POLSKA")
        self.assertEqual(datafields["Siedziba_Wojewodztwo"], "LUBUSKIE")
        self.assertEqual(datafields["Siedziba_Powiat"], "ŚWIEBODZIŃSKI")
        self.assertEqual(datafields["Siedziba_Gmina"], "ŚWIEBODZIN")
        self.assertEqual(datafields["Siedziba_Miejscowosc"], "ŚWIEBODZIN")

        self.assertEqual(datafields["Adres_Ulica"], "SOBIESKIEGO")
        self.assertEqual(datafields["Adres_Numer"], "8")
        self.assertEqual(datafields["Adres_Lokal"], "---")
        self.assertEqual(datafields["Adres_Miejscowosc"], "ŚWIEBODZIN")
        self.assertEqual(datafields["Adres_Kod"], "66-200")
        self.assertEqual(datafields["Adres_Poczta"], "ŚWIEBODZIN")
        self.assertEqual(datafields["Adres_Kraj"], "POLSKA")

        self.assertEqual(datafields["Kapitał Zakładowy"], "2 059 710,80 ZŁ")

        self.assertEqual(datafields["Zarząd 1"]["Nazwisko/Nazwa"], "WYRZYKOWSKI")
        self.assertEqual(datafields["Zarząd 1"]["Imiona"], "PAWEŁ")
        self.assertEqual(datafields["Zarząd 1"]["Funkcja"], "PREZES ZARZĄDU")

        self.assertEqual(datafields["Zarząd 2"]["Nazwisko/Nazwa"], "KLINOWSKI")
        self.assertEqual(datafields["Zarząd 2"]["Imiona"], "BARTOSZ MAREK")
        self.assertEqual(datafields["Zarząd 2"]["Funkcja"], "CZŁONEK ZARZĄDU")

        self.assertEqual(datafields["Zarząd 3"]["Nazwisko/Nazwa"], "WOŹNIAK")
        self.assertEqual(datafields["Zarząd 3"]["Imiona"], "SŁAWOMIR STANISŁAW")
        self.assertEqual(datafields["Zarząd 3"]["Funkcja"], "WICEPREZES ZARZĄDU")









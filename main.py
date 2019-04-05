from doc_parser import DocParser
import os

VERSION = 1.0


print(f">>> Now running: Pdf-Docx {VERSION}\n ")

for pdf_file in os.listdir("pdf\\"):
    try:
        if pdf_file.endswith(".pdf"):
            parser = DocParser(pdf_file)  # initiate parser object with pdf file
            if parser.docx_filename not in os.listdir("docx\\"):
                if parser.txt_filename not in os.listdir("txt\\"):
                    parser.extract_pdf()
                    parser.parse_all()  # runs a method pack for all parsing
                else:
                    parser.parse_all()
            else:
                print(f">>> Skipping file, already done...")
            parser.clear_temp()
    except:
        print(f">>> File '{pdf_file}' not parsed.\n")

input(f">  Finished!\n>  Press Enter to exit")

from meta_parser import DocParser
import os

for pdf_file in os.listdir("PDF\\"):
    try:
        if pdf_file.endswith(".pdf"):
            parser = DocParser(pdf_file)  # initiate parser object with pdf file
            if parser.docx_file not in os.listdir("DOCX\\"):
                if parser.txt_file not in os.listdir("txt\\"):
                    parser.extract_pdf()
                    parser.parse_all()
                else:
                    parser.parse_all()  # runs method pack for all parsing
            else:
                print(f">>> Skip file '{parser.docx_file}' already exists.")
            parser.clear_temp()
    except:
        print(f">>> File '{pdf_file}' not parsed, an error occured")

input(f">  Finished!\n>  Press Enter to exit")

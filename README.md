# Pdf-Docx

Pdf-Docx is a Python application with the purpose of extracting data from multiple .pdf files containing information equal to current "Odpis Aktualny" that's available on the Ministery of Justice website and saving that data to editable text files .docx using a document template.
## Installation

Use the package manager pip to install required libraries.

pip install -r requirements.txt

All dependant directories will be created upon first execution of the doc_parser.py.

## Usage

Pdf-Docx requires template.docx file. It's fields that are up to edit are filled with data tags eg "NIP".

Copy the 'odpis_aktualny.pdf' you want to parse into the pdf directory.

Main.py executes a loop that parse all files in pdf directory. Use start.bat to initiate main.py

App first extracts unicode text file from the pdf then loops through it looking for index-specific data.

The parses then loops the template document and swaps the tags with new data.

Logfile of the operation is also created in log directory .

## License

MIT
[MIT](https://choosealicense.com/licenses/mit/)

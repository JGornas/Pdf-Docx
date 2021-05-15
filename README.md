# Pdf-Docx

Pdf-Docx is a Python application with the purpose of extracting data from multiple .pdf
files containing information equal to current "Odpis Aktualny" that's available on 
the Ministery of Justice website and saving that data to editable text files .docx 
using a document template.

## Installation

Use the package manager pip to install required libraries.

```bash
pip install -r requirements.txt
```
Dependant directories docx and txt will be created upon first execution of the application.

## Usage

Copy all 'odpis_aktualny.pdf' files that needs to be parsed into the pdf directory.

```bash
python ui.py
```

Enter a command to access a function.
```bash
>>> Now running: Pdf-Docx
> Enter 'help' for a list of commands.
> Enter command:
> ...
```

List of commands:
- all -  Parses all files in the pdf directory.
- parse 'filename' - Parses one pdf file. Eg. 'file odpis_aktualny_1.pdf'.
- files - Prints all filenames in the pdf directory.
- help - Lists all commands.
- exit - Exits the application.


App extracts unicode text from the pdf and looks for an index or
a regex specific data.
Inserts and saves data to a template.docx file.


## License

[MIT](https://choosealicense.com/licenses/mit/)

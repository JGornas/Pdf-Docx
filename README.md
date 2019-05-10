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

Execute ui.py file. Enter a command to access a function.
```bash
>>> Now running: Pdf-Docx
> Enter 'help' for a list of commands.
> Enter command:
```
\
List of commands:

```bash
> all
```
Parses all files in pdf directory.

```bash
> file 'filename'
```
Parses one pdf file. Eg. 'file odpis_aktualny_1.pdf'.

```bash
> files
```
Prints all files in the pdf directory.

```bash
> exit
```
Exits the application.


App first extracts unicode text file from the pdf then loops through it looking for index or
regex specific data.

It then loops through the template.docx document file and fills the cells with new data,
saving new file under previous pdf file name.


## License

[MIT](https://choosealicense.com/licenses/mit/)

import subprocess
import os

print(os.path.join("venv", "Scripts", "python.exe"))
subprocess.call(["venv\\Scripts\\python.exe",
                 "venv\\Scripts\\pdf2txt.py",
                 "pdf\\odpis_aktualny_1.pdf", "-otxt\\odpis_aktualny_1.txt"])
print(f"\n>>> Extracting text from odpis_aktualny_1.pdf")

os.getcwd()

os.chdir(os.path.join("txt",""))

print(os.getcwd())
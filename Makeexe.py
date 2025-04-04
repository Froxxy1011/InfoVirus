import os

def make_exe():
    python_file = input("Enter the name of the file with the .py extension\n For example: example.py\n: ") 
    os.popen("python -m PyInstaller --windowed --onefile {python_file}".format(python_file=python_file))

make_exe()
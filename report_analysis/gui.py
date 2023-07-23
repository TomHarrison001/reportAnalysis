"""This is the main GUI interface"""

from tkinter import Tk, Label, Button, Entry, filedialog

from txt_parser import ExtractData
from pie_exporter import CreateDrawing, ExportDrawing
from table_exporter import CreateTable, ExportTable

def BrowseFiles():
    import_file = filedialog.askopenfilename(initialdir = '/',
        title = "Select a File",
        filetypes = (("XLSX File", '*.xlsx'),))
    if import_file:
        file_label.configure(text=import_file)
    else:
        file_label.configure(text='Select a File')

def BrowseDirs():
    output_path = filedialog.askdirectory(initialdir = '/',
        title = "Select an Output Directory",
        mustexist=True)
    if output_path:
        dir_label.configure(text=output_path)
    else:
        dir_label.configure(text='Select an Output Directory')

def Submit():
    error_label.configure(text='')
    import_file = file_label['text']
    sheet_name = sheet_entry.get()
    output_path = dir_label['text']
    try:
        ErrorHandling(import_file, sheet_name, output_path)
        data = ExtractData(import_file, sheet_name)
        drawing = CreateDrawing(800, 900, data)
        ExportDrawing(drawing, output_path)

        table = CreateTable(data)
        ExportTable(table, output_path)

        error_label.configure(text='Task Completed.', fg='green')
    except Exception as e:
        error_label.configure(text=e, fg='red')

def ErrorHandling(import_file, sheet_name, output_path):
    if import_file == 'Select a File':
        raise Exception('No file selected.')
    if sheet_name.strip() == '':
        raise Exception('No sheet name entered.')
    if output_path == 'Select an Output Directory':
        raise Exception('No directory selected.')

window = Tk()
window.title('File Explorer')
window.geometry("1280x720")
window.config(background='white')
file_label = Label(window, text='Select a File',
    width=50, height=2, fg='blue')
file_button = Button(window, text='Browse Files', command=BrowseFiles, bd=3, width=18)
sheet_label = Label(window, text="Sheet name", 
    width=50, height=2, fg='blue')
sheet_entry = Entry(window, bd=3, width=18)
dir_label = Label(window, text='Select an Output Directory',
    width=50, height=2, fg='blue')
dir_button = Button(window, text='Browse Directories', command=BrowseDirs, bd=3, width=18)
error_label = Label(window, text='', bg='white')
submit_button = Button(window, text='Submit', command=Submit)
file_label.grid(column=0, row=0, padx=5, pady=5)
file_button.grid(column=1, row=0)
sheet_label.grid(column=0, row=1, padx=5, pady=5)
sheet_entry.grid(column=1, row=1)
dir_label.grid(column=0, row=2, padx=5, pady=5)
dir_button.grid(column=1, row=2)
error_label.grid(column=0, row=3, columnspan=2, pady=5)
submit_button.grid(column=0, row=4, columnspan=2)
window.mainloop()
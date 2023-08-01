"""This is the GUI object"""

from tkinter import Tk, Label, Button, Entry, filedialog, HORIZONTAL
from tkinter.ttk import Progressbar
from threading import Thread

from txt_parser import ExtractData
from pie_exporter import CreateDrawing, ExportDrawing
from table_exporter import CreateTable, ExportTable

class Window():
    def __init__(self):
        self.window = Tk()
        self.window.title('Report Analysis')
        self.window.geometry("480x640")
        self.window.config(background='white')
        self.widgets = []
        for text in ['Select a File', 'Sheet name', 'Select an Output Directory']:
            self.widgets.append(self.CreateLabel(text))
        self.widgets.insert(1, self.CreateButton('Browse Files', self.BrowseFiles))
        self.widgets.insert(3, Entry(self.window, bd=3, width=18))
        self.widgets.insert(5, self.CreateButton('Browse Directories', self.BrowseDirs))
        self.widgets.append(Label(self.window, text='', bg='white'))
        self.widgets.append(Button(self.window, text='Submit', command=self.Submit))
        for widget in self.widgets:
            index = self.widgets.index(widget)
            pady = ((index + 1) % 2 * 20, (index + 1) % 2 * 5)
            widget.grid(column=0, row=index, padx=50, pady=pady)
        self.progress = Progressbar(self.window, orient=HORIZONTAL, length=200, mode='indeterminate')
        
    def CreateLabel(self, text):
        return Label(self.window, text=text, width=50, height=2, fg='blue')
    
    def CreateButton(self, text, command):
        return Button(self.window, text=text, command=command, bd=3, width=18)
    
    def BrowseFiles(self):
        import_file = filedialog.askopenfilename(initialdir = '/',
            title = "Select a File",
            filetypes = (("XLSX File", '*.xlsx'),))
        if import_file:
            self.widgets[0].configure(text=import_file)
        else:
            self.widgets[0].configure(text='Select a File')

    def BrowseDirs(self):
        output_path = filedialog.askdirectory(initialdir = '/',
            title = "Select an Output Directory",
            mustexist=True)
        if output_path:
            self.widgets[4].configure(text=output_path)
        else:
            self.widgets[4].configure(text='Select an Output Directory')

    def Submit(self):
        self.widgets[6].configure(text='')
        import_file = self.widgets[0]['text']
        sheet_name = self.widgets[3].get()
        output_path = self.widgets[4]['text']
        def real_submit():
            self.widgets[6]['state'] = 'disabled'
            self.widgets[7]['state'] = 'disabled'
            self.progress.grid(row=8, column=0, pady=20)
            self.progress.start()
            try:
                self.ErrorHandling(import_file, sheet_name, output_path)
                data = ExtractData(import_file, sheet_name)
                drawing = CreateDrawing(800, 900, data)
                ExportDrawing(drawing, output_path)

                table = CreateTable(data)
                ExportTable(table, output_path)

                self.widgets[6].configure(text='Task Completed.', fg='green')
            except Exception as e:
                if str(e).startswith("\"None of [Index(['Grounds', 'NPA'"):
                    e = Exception("Worksheet needs Grounds and NPA columns.")
                self.widgets[6].configure(text=e, fg='red')
            self.progress.stop()
            self.progress.grid_forget()
            self.widgets[6]['state'] = 'normal'
            self.widgets[7]['state'] = 'normal'
        Thread(target=real_submit).start()

    def ErrorHandling(self, import_file, sheet_name, output_path):
        if import_file == 'Select a File':
            raise Exception('No file selected.')
        if sheet_name.strip() == '':
            raise Exception('No sheet name entered.')
        if output_path == 'Select an Output Directory':
            raise Exception('No directory selected.')

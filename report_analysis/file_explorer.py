from tkinter import Tk, Label, Button, Entry, filedialog

def BrowseFiles():
    filename = filedialog.askopenfilename(initialdir = '/',
        title = "Select a file",
        filetypes = (("XLSX File", '*.xlsx'),))
    file_label.configure(text='File Opened: ' + filename)

def BrowseDirs():
    dirname = filedialog.askdirectory(mustexist=True)
    dir_label.configure(text='Output Dir: ' + dirname)

def Submit():
    error_label.configure(text='')
    filename = file_label['text']
    dirname = dir_label['text']
    sheet = sheet_entry.get()
    if not ErrorHandling(filename, dirname, sheet):
        return
    

def ErrorHandling(filename, dirname, sheet):
    if filename in ['Select a File', 'File Opened: ']:
        error_label.configure(text='No file selected.')
        return False
    if dirname in ['Select an Output Directory', 'Output Dir: ']:
        error_label.configure(text='No directory selected.')
        return False
    if sheet.strip() == '':
        error_label.configure(text='No sheet name entered.')
        return False
    return True

window = Tk()
window.title('File Explorer')
window.geometry("1280x720")
window.config(background='white')
file_label = Label(window, text='Select a File',
    width=50, height=2, fg='blue')
file_button = Button(window, text='Browse Files', command=BrowseFiles)
dir_label = Label(window, text='Select an Output Directory',
    width=50, height=2, fg='blue')
dir_button = Button(window, text='Browse Directories', command=BrowseDirs)
sheet_label = Label(window, text="Sheet name")
sheet_entry = Entry(window, bd=2)
error_label = Label(window, text='', fg='red', bg='white')
submit_button = Button(window, text='Submit', command=Submit)
file_label.grid(column=0, row=0, columnspan=5)
file_button.grid(column=5, row=0)
dir_label.grid(column=0, row=1, columnspan=5)
dir_button.grid(column=5, row=1)
sheet_label.grid(column=0, row=2)
sheet_entry.grid(column=2, row=2)
error_label.grid(column=3, row=3)
submit_button.grid(column=3, row=4)
window.mainloop()
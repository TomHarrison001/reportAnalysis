"""This is the main command line interface"""

from gui import Window

def api():
    w = Window()
    w.window.mainloop()

if __name__ == '__main__':
    api()

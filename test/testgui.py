from tkinter import *
from tkinter import filedialog
from tkinter import ttk


class FiledialogSampleApp(ttk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.pack()

        self.filename = StringVar()

        label = ttk.Label(self, text="FileName")
        label.pack(side='left')

        filenameEntry = ttk.Entry(self, text='', textvariable=self.filename)
        filenameEntry.pack(side='left')

        botton = ttk.Button(self, text='open', command=self.openfileDialog)
        botton.pack(side='left')

    def openfileDialog():
        
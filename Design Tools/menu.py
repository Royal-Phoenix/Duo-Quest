import tkinter as tk


class MenuBar:
    def __init__(self, root):
        self.menu = tk.Menu(root)
        self.createMenuButtons()
        self.attachMenuButtons()
        self.createDropdowns()
    
    def createMenuButtons(self):
        self.file = tk.Menu(self.menu)
        self.edit = tk.Menu(self.menu)
        self.options = tk.Menu(self.menu)
        self.settings = tk.Menu(self.menu)
    
    def attachMenuButtons(self):
        self.menu.add_cascade(label='File', menu=self.file)
        self.menu.add_cascade(label='Edit', menu=self.edit)
        self.menu.add_cascade(label='Options', menu=self.options)
        self.menu.add_cascade(label='Settings', menu=self.settings)
    
    def createDropdowns(self):
        self.file.add_command(label='New File', command=None)
        self.file.add_command(label='Save', command=None)
        self.edit.add_command(label='Edit', command=None)

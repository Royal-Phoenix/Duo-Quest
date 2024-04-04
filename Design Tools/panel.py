from tkinter.ttk import *
import tkinter as tk
from inventory import Inventory


class Panel():
    def __init__(self, root, editor):
        self.frame = Frame(root, width=360, height=768)
        self.createPanelItems(editor)
        self.attachPanelItems()
    
    def createPanelItems(self, editor):
        self.inventory = Inventory(self.frame, editor)
        self.textures = Button(self.frame, text='Textures', command=lambda: self.inventory.displayItems('screen_textures'), state=tk.DISABLED)
        self.objects = Button(self.frame, text='Objects', command=lambda: self.inventory.displayItems('objects'))
        self.players = Button(self.frame, text='Players', command=lambda: self.inventory.displayItems('players'))
        self.doors = Button(self.frame, text='Doors', command=lambda: self.inventory.displayItems('doors'))
    
    def attachPanelItems(self):
        self.textures.pack(side=tk.TOP)
        self.objects.pack(side=tk.TOP)
        self.players.pack(side=tk.TOP)
        self.doors.pack(side=tk.TOP)
        self.inventory.frame.pack(side=tk.TOP, pady=100)

from tkinter.ttk import *
import tkinter as tk
import os, json


class Inventory:
    def __init__(self, root, editor):
        self.frame = Frame(root, width=280, height=500)
        self.editor = editor
    
    def displayItems(self, category):
        self.clearItems()
        root = 'assets/sprites/'
        items = sorted([path for path in os.listdir(root+category)])
        self.items = [(item[:-4], tk.PhotoImage(file=root+category+'/'+item)) for item in items]
        count, size = 0, 4
        for name, item in self.items:
            inventoryItem = Button(self.frame, text=name, image=item, width=10,
                                   command=lambda id=name: self.editor.displayItemDetails(category, id),
                                   compound=tk.TOP)
            inventoryItem.grid(row=count//size, column=count%size, padx=3, pady=6)
            count += 1
    
    def clearItems(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
    
    def getItemDetails(self, category, id):
        self.editor.displayItemDetails(self.data[category][id])

from tkinter.ttk import *
import tkinter as tk


class Canvas:
    def __init__(self, root):
        self.frame = Frame(root, width=580, height=768, style='canvas.TFrame')
        self.canvas = tk.Canvas(self.frame, width=580, height=768, background='#BDBDBD')
        self.canvas.pack(fill='both', expand=True)
        self.images, self.labels = {}, []
    
    def placeItem(self, image, X, Y):
        if image is not None:
            if (X, Y) in self.images:
                self.removeItem(X, Y)
            item = self.canvas.create_image((X+2+image.width()//2, Y+2+image.height()//2), image=image, anchor=tk.CENTER)
            self.images[(X, Y)] = [item, image]
    
    def removeItem(self, X, Y, image=None):
        if (X, Y) in self.images:
            self.canvas.delete(self.images[(X, Y)][0])
            del self.images[(X, Y)]
    
    def makeBlock(self, category, id):
        pass

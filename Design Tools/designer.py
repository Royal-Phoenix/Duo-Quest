from tkinter.ttk import *
import tkinter as tk

from actions import *
from menu import MenuBar
from panel import Panel
from canvas import Canvas
from editor import Editor


window = tk.Tk()
window.title('Level Designer')
window.state('zoomed')
window.protocol('WM_DELETE_WINDOW', lambda: destroyRoot(window))
canvas = tk.Canvas(window)
canvas.pack(fill='both', expand=True)

menu_bar = MenuBar(window)
window.config(menu=menu_bar.menu)

mainFrame = Frame(canvas)
canva = Canvas(window)
editor = Editor(window, canva)
panel = Panel(window, editor)
editor.panel = panel
panel.frame.pack(side=tk.LEFT, padx=20)
canva.frame.pack(side=tk.LEFT)
editor.frame.pack(side=tk.LEFT, padx=40)
mainFrame.pack()

window.mainloop()

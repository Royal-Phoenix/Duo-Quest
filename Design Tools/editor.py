from tkinter.ttk import *
import tkinter as tk
import json


class Editor:
    def __init__(self, root, canvas):
        self.frame = Frame(root, width=462, height=768)
        self.canvas = canvas
        self.data = json.load(open('Design Tools/levels/data.json'))
        self.coords = {key:tk.IntVar() for key in ['X', 'Y', 'W', 'H', 'N', 'O', 'C', 'B', 'J']}
        self.count = {key:0 for category in self.data for key in self.data[category]}
        self.createEditorTools()
        self.attachEditorTools()
    
    def createEditorTools(self):
        self.image = None
        self.item_image = Label(self.frame, compound=tk.TOP)
        self.item_info = Label(self.frame)
        self.value_x = Label(self.frame, text='X: ')
        self.entry_x = Entry(self.frame, textvariable=self.coords['X'])
        self.value_y = Label(self.frame, text='Y: ')
        self.entry_y = Entry(self.frame, textvariable=self.coords['Y'])
        self.value_w = Label(self.frame, text='W: ')
        self.entry_w = Entry(self.frame, textvariable=self.coords['W'], state=tk.DISABLED)
        self.value_h = Label(self.frame, text='H: ')
        self.entry_h = Entry(self.frame, textvariable=self.coords['H'], state=tk.DISABLED)
        self.value_n = Label(self.frame, text='Number: ')
        self.entry_n = Entry(self.frame, textvariable=self.coords['N'], state=tk.DISABLED)
        self.value_o = Label(self.frame, text='Orient: ')
        self.entry_o = Entry(self.frame, textvariable=self.coords['O'], state=tk.DISABLED)
        self.value_c = Label(self.frame, text='Count: ')
        self.entry_c = Entry(self.frame, textvariable=self.coords['C'], state=tk.DISABLED)
        self.label_x = Label(self.frame, text='X: ')
        self.slide_x = Scale(self.frame, from_=0, to=544, variable=self.coords['X'], orient=tk.HORIZONTAL)
        self.label_y = Label(self.frame, text='Y: ')
        self.slide_y = Scale(self.frame, from_=0, to=544, variable=self.coords['Y'], orient=tk.HORIZONTAL)
        self.label_j = Label(self.frame, text='Joystick Mode: ')
        self.check_j = Checkbutton(self.frame, variable=self.coords['J'], command=self.joystickMode)
        self.label_w = Label(self.frame, text='Wall Mode: ')
        self.check_w = Checkbutton(self.frame, variable=self.coords['B'], command=self.wallMode)
        self.remove = Button(self.frame, text='Remove',
                             command=lambda: self.canvas.removeItem(self.coords['X'].get(),
                                                                    self.coords['Y'].get(), self.image))
        self.place = Button(self.frame, text='Place',
                            command=lambda: self.canvas.placeItem(self.image, self.coords['X'].get(),
                                                                  self.coords['Y'].get()))
    
    def attachEditorTools(self):
        self.item_image.grid(row=0, column=0, columnspan=2)
        self.item_info.grid(row=1, column=0, columnspan=2)
        self.value_x.grid(row=2, column=0, sticky=tk.W)
        self.entry_x.grid(row=2, column=0)
        self.value_y.grid(row=2, column=1, sticky=tk.W)
        self.entry_y.grid(row=2, column=1)
        self.value_w.grid(row=3, column=0, sticky=tk.W)
        self.entry_w.grid(row=3, column=0)
        self.value_h.grid(row=3, column=1, sticky=tk.W)
        self.entry_h.grid(row=3, column=1)
        self.value_n.grid(row=4, column=0, sticky=tk.W)
        self.entry_n.grid(row=4, column=0)
        self.value_o.grid(row=4, column=1, sticky=tk.W)
        self.entry_o.grid(row=4, column=1)
        self.value_c.grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=70)
        self.entry_c.grid(row=5, column=0, columnspan=2, padx=120)
        self.label_x.grid(row=6, column=0, sticky=tk.W)
        self.slide_x.grid(row=6, column=0)
        self.label_y.grid(row=6, column=1, sticky=tk.W)
        self.slide_y.grid(row=6, column=1)
        self.label_j.grid(row=7, column=0, sticky=tk.W)
        self.check_j.grid(row=7, column=0)
        self.label_w.grid(row=7, column=1, sticky=tk.W)
        self.check_w.grid(row=7, column=1)
        self.remove.grid(row=8, column=0)
        self.place.grid(row=8, column=1)
    
    def displayItemDetails(self, category, id):
        contents = self.data[category][id]
        self.canvas.makeBlock(category, id)
        self.image = tk.PhotoImage(file='assets/sprites/'+category+'/'+id+'.png')
        self.item_image.config(image=self.image, text=contents['name'])
        self.item_info.config(text=contents['info'])
        self.entry_w.config(self.coords['W'].set(self.image.width()))
        self.entry_h.config(self.coords['H'].set(self.image.height()))
        self.entry_c.config(self.coords['C'].set(self.count[id]))
    
    def clearEditorSection(self):
        pass

    def moveItem(self, dir):
        if dir == 'UP':
            pass
        if dir == 'DOWN':
            pass
        if dir == 'LEFT':
            pass
        if dir == 'RIGHT':
            pass
    
    def joystickMode(self):
        if self.coords['B'].get():
            self.frame.bind('<Up>', self.moveItem('UP'))
            self.frame.bind('<Down>', self.moveItem('DOWN'))
            self.frame.bind('<Left>', self.moveItem('LEFT'))
            self.frame.bind('<Right>', self.moveItem('RIGHT'))
    
    def wallMode(self):
        if self.coords['B'].get():
            self.panel.textures.config(state=tk.ACTIVE)
            self.panel.objects.config(state=tk.DISABLED)
            self.panel.players.config(state=tk.DISABLED)
            self.panel.doors.config(state=tk.DISABLED)
            self.entry_n.config(state=tk.ACTIVE)
            self.entry_o.config(state=tk.ACTIVE)
        else:
            self.panel.textures.config(state=tk.DISABLED)
            self.panel.objects.config(state=tk.ACTIVE)
            self.panel.players.config(state=tk.ACTIVE)
            self.panel.doors.config(state=tk.ACTIVE)
            self.entry_n.config(state=tk.DISABLED)
            self.entry_o.config(state=tk.DISABLED)

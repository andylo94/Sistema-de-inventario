from tkinter import *
import tkinter as tk 
from tkinter import ttk, messagebox

class Inventario (tk.Frame):
    def __init__ (self, padre):
        super().__init__ (padre)
        self.pack()
        self.widgets()

    def widgets(self):
        frame1 = tk.Frame(self, bg = '#dddddd', highlightbackground='gray',highlightthickness=1)
        frame1.pack()
        frame1.place(x=0,y=0,width=1100, height=100)

        titulo = tk.Label (self, text='INVENTARIOS', bg = '#dddddd', font= 'sans 30 bold ', anchor='center') # Definicion de texto "ventas" y configuracion de tipo de letra, tamaño, negrilla habilitado y centrado  
        titulo.pack()
        titulo.place(x=5,y=0, width=1090, height=90 )
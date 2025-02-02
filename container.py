from tkinter import *
import tkinter as tk
from ventas import Ventas
from inventario import Inventario

class Container (tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=800, height=400)
        self.config(bg='#FFC1CC')
        self.widgets()

    def show_frame(self, container):
        top_level = tk.Toplevel(self)  
        frame = container(top_level)
        frame.config(bg='#FFC1CC')# Color de fondo 
        frame.pack (fill='both', expand= True)
        top_level.geometry('1100x650, 120+20') # Tamaño y posicion de ventana  
        top_level.resizable(False, False) # EL maximizar o minimizar no esta disponible con el "False"
    
    def ventas(self):  # Ventana de ventas 
        self.show_frame(Ventas)

    def inventario (self):
        self.show_frame(Inventario)

    def widgets(self):
        frame1 = tk.Frame(self, bg='#FFC1CC')
        frame1.pack()
        frame1.place(x=0, y=0, width=800, height=400)
        
        btnventas = Button (frame1, bg = '#cc84bc ', fg= 'black',font='sans 18 bold', text='Ir a ventas', command=self.ventas) #Definicion de Color, color de texto, el texto y hacia donde me dirige 
        btnventas.place (x=500, y= 30, width=240,height=60)# Posicion  y tamaño del boton dentro de la ventana 


        btninventario = Button (frame1, bg = '#cc84bc ', fg= 'black',font='sans 18 bold', text='Ir a inventario', command=self.inventario) #Definicion de Color, color de texto, el texto y hacia donde me dirige 
        btninventario.place (x=500, y= 130, width=240,height=60)# Posicion  y tamaño del boton dentro de la ventana 
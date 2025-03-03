from tkinter import *
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from PIL import Image, ImageTk
import os
import sys

class Container (tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=800, height=400)
        self.config(bg='#e4e4e7')
        self.widgets()

    def show_frame(self, container):
        top_level = tk.Toplevel(self)  
        frame = container(top_level)
        frame.config(bg='#e4e4e7') 
        frame.pack(fill='both', expand= True)
        top_level.geometry('1100x650+120+20') # Tamaño y posicion de ventana  
        top_level.resizable(False, False) # EL maximizar o minimizar no esta disponible con el "False"
        top_level.transient(self.master)
        top_level.grab_set()
        top_level.focus_set()
        top_level.lift()
        ruta = self.rutas (r"icono.ico")
        top_level.iconbitmap(ruta)

    def rutas(self, ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase,ruta)
    
    def ventas(self):  # Ventana de ventas 
        self.show_frame(Ventas)

    def inventario (self):
        self.show_frame(Inventario)

    def widgets(self):
        frame1 = tk.Frame(self, bg='#e4e4e7')
        frame1.pack()
        frame1.place(x=0, y=0, width=800, height=400)
        
        btnventas = Button (frame1, bg = '#007790', fg= 'black',font='sans 18 bold', text='Ir a ventas', command=self.ventas) #Definicion de Color, color de texto, el texto y hacia donde me dirige 
        btnventas.place (x=500, y= 110, width=240,height=60)# Posicion  y tamaño del boton dentro de la ventana 


        btninventario = Button (frame1, bg = '#007790', fg= 'black',font='sans 18 bold', text='Ir a inventario', command=self.inventario) #Definicion de Color, color de texto, el texto y hacia donde me dirige 
        btninventario.place (x=500, y= 210, width=240,height=60)# Posicion  y tamaño del boton dentro de la ventana 

        ruta = self.rutas (r"Imagenes/logo.png")
        self.logo_image = Image.open(ruta)
        self.logo_image = self.logo_image.resize((200,200))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(frame1, image = self.logo_image, bg= '#e4e4e7')
        self.logo_label.place(x=100, y=90)

        copyright_label = tk.Label(frame1,bg= '#e4e4e7' ,font="sans 10 bold", fg="black", text="© 2025 ALZ Solutions. Todos los derechos reservados.")
        copyright_label.place(x=240,y=375)
from tkinter import *
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from PIL import Image, ImageTk

class Container (tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=800, height=400)
        self.config(bg='#FBECEC')
        self.widgets()

    def show_frame(self, container):
        top_level = tk.Toplevel(self)  
        frame = container(top_level)
        frame.config(bg='#FBECEC') 
        frame.pack(fill='both', expand= True)
        top_level.geometry('1100x650+120+20') # Tamaño y posicion de ventana  
        top_level.resizable(False, False) # EL maximizar o minimizar no esta disponible con el "False"
    
    def ventas(self):  # Ventana de ventas 
        self.show_frame(Ventas)

    def inventario (self):
        self.show_frame(Inventario)

    def widgets(self):
        frame1 = tk.Frame(self, bg='#FBECEC')
        frame1.pack()
        frame1.place(x=0, y=0, width=800, height=400)
        
        btnventas = Button (frame1, bg = '#CC84BC', fg= 'black',font='sans 18 bold', text='Ir a ventas', command=self.ventas) #Definicion de Color, color de texto, el texto y hacia donde me dirige 
        btnventas.place (x=500, y= 110, width=240,height=60)# Posicion  y tamaño del boton dentro de la ventana 


        btninventario = Button (frame1, bg = '#CC84BC', fg= 'black',font='sans 18 bold', text='Ir a inventario', command=self.inventario) #Definicion de Color, color de texto, el texto y hacia donde me dirige 
        btninventario.place (x=500, y= 210, width=240,height=60)# Posicion  y tamaño del boton dentro de la ventana 

        self.logo_image = Image.open("Imagenes/logo.jpg")
        self.logo_image = self.logo_image.resize((200,200))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(frame1, image = self.logo_image, bg= '#FBECEC')
        self.logo_label.place(x=100, y=90)

        copyright_label = tk.Label(frame1,bg= '#FBECEC' ,font="sans 10 bold", fg="black", text="© 2025 Von Makeup. Todos los derechos reservados.")
        copyright_label.place(x=240,y=375)
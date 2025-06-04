import sqlite3
from datetime import datetime
from tkinter import messagebox
from tkinter import *
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from admin import UserAdminWindow
from PIL import Image, ImageTk
import os
import sys
from login import Login

class Container (tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=800, height=400)
        self.config(bg='#e4e4e7')
        self.widgets()
        self.verificar_vencimientos()

    def show_frame(self, container):
        top_level = tk.Toplevel(self)  
        frame = container(top_level, self.controlador)
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
            rutabase=sys._MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase,ruta)
    
    def ventas(self):  # Ventana de ventas 
        self.show_frame(Ventas)

    def inventario (self):
        self.show_frame(Inventario)

    def admin (self):
        UserAdminWindow(self)


    def widgets(self):
        frame1 = tk.Frame(self, bg='#e4e4e7')
        frame1.pack()
        frame1.place(x=0, y=0, width=800, height=400)

        btn_login = Button(frame1, bg='#28a745', fg='white', font='sans 18 bold',
                       text='Iniciar sesión', command=self.iniciar_sesion)
        btn_login.place(x=75, y=290, width=250, height=40)
        
        self.btnventas = Button (frame1, bg = '#007790',state="disabled", font='sans 18 bold', text='Salidas',fg='white', command=self.ventas) #Definicion de Color, color de texto, el texto y hacia donde me dirige 
        self.btnventas.place (x=500, y= 70, width=250,height=60)# Posicion  y tamaño del boton dentro de la ventana 


        self.btninventario = Button (frame1, bg = '#007790',state="disabled", fg='white', font='sans 18 bold', text='Ir a inventario', command=self.inventario) #Definicion de Color, color de texto, el texto y hacia donde me dirige 
        self.btninventario.place (x=500, y= 170, width=250,height=60)# Posicion  y tamaño del boton dentro de la ventana 

        self.btn_admin_usuarios = Button(frame1, bg='#007790', state="disabled", fg='white', font='sans 18 bold', text='Administar usuarios', command=self.admin)
        self.btn_admin_usuarios.place(x=500, y=270, width=250, height=60)# Posicion  y tamaño del boton dentro de la ventana    

        ruta = self.rutas (r"Imagenes/logo.png")
        self.logo_image = Image.open(ruta)
        self.logo_image = self.logo_image.resize((200,200))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(frame1, image = self.logo_image, bg= '#e4e4e7')
        self.logo_label.place(x=100, y=60)

        copyright_label = tk.Label(frame1,bg= '#e4e4e7' ,font="sans 10 bold", fg="black", text="© 2025 ALZ Solutions. Todos los derechos reservados. (Versión: 1.3.0)")
        copyright_label.place(relx=0.5,y=375, anchor="center")

    def verificar_vencimientos(self):
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            hoy = datetime.now().date()

            # Productos con vencimientos
            cursor.execute("SELECT nombre, fecha_vencimiento FROM inventario")
            productos = cursor.fetchall()
            proximos_a_vencer = []

            for nombre, fecha_str in productos:
                if fecha_str:
                    try:
                        vencimiento = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                        dias_restantes = (vencimiento - hoy).days
                        if dias_restantes <= 30:
                            proximos_a_vencer.append((nombre, dias_restantes))
                    except Exception as e:
                        print(f"Error al procesar fecha de {nombre}: {e}")

            # Productos con bajo stock
            cursor.execute("SELECT nombre, stock FROM inventario WHERE stock <= 3")
            bajos_en_stock = cursor.fetchall()

            conn.close()

            # Crear mensaje combinado
            mensaje = ""

            if proximos_a_vencer:
                mensaje += "🔔 Productos próximos a vencer:\n\n"
                for nombre, dias in proximos_a_vencer:
                    mensaje += f"🧪 {nombre}: vence en {dias} días\n"
                mensaje += "\n"

            if bajos_en_stock:
                mensaje += "📉 Productos con stock bajo menor a 3 unidades:\n\n"
                for nombre, stock in bajos_en_stock:
                    mensaje += f"📦 {nombre}: {stock} unidades\n"

            if mensaje:
                messagebox.showwarning("⚠️ Alerta de inventario", mensaje)

        except Exception as e:
            print(f"Error al verificar vencimientos o stock: {e}")

    def iniciar_sesion(self):
        def on_login(usuario, rol):
            self.controlador.usuario_actual = usuario
            self.controlador.rol_actual = rol
            self.controlador.title(f"SIGE - Sesión de {usuario} ({rol})")

            # Habilitar botones comunes para todos los roles
            self.btnventas.config(state="normal")
            self.btninventario.config(state="normal")

            if rol == "admin":
                self.btn_admin_usuarios.config(state="normal")
                messagebox.showinfo("Bienvenido", f"Sesión iniciada como administrador: {usuario}")
            else:
                self.btn_admin_usuarios.config(state="disabled")
                messagebox.showinfo("Bienvenido", f"Sesión iniciada como usuario: {usuario}")

        Login(self.controlador, on_login)
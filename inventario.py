from tkinter import *
import tkinter as tk 
from tkinter import ttk, messagebox

class Inventario (tk.Frame):
    def __init__ (self, padre):
        super().__init__ (padre)
        self.pack()
        self.widgets()

    def widgets(self):
        frame1 = tk.Frame(self, bg = '#E99AC4', highlightbackground='#E99AC4',highlightthickness=1 )
        frame1.pack()
        frame1.place(x=0,y=0,width=1100, height=100) #Posicion de la barra.

        titulo = tk.Label (self, text="INVENTARIO", bg = '#E99AC4', font= 'sans 30 bold ', anchor='center') # Definicion de texto "ventas" y configuracion de tipo de letra, tamaño, negrilla habilitado y centrado  
        titulo.pack()
        titulo.place(x=5,y=0, width=1090, height=90)

        frame2 = tk.Frame (self, bg= "#FBECEC", highlightbackground= "#FBECEC", highlightthickness=1)
        frame2.place(x=0, y=100 , width=1100, height=550)

        labelframe = LabelFrame(frame2, text="Productos", font= "sans 22 bold", bg="#FBECEC")
        labelframe.place(x=20, y=30, width=400 , height=500)

        lblnombre = Label(labelframe, text= "Nombre: ", bg= "#FBECEC", font="sans 14 bold")
        lblnombre.place(x=10, y=20)
        self.nombre= ttk.Entry(labelframe, font="sans 14 bold")
        self.nombre.place(x=140, y=20, width=240, height=40)
         
        lblproveedor= Label(labelframe, text="Proveedor: ",bg= "#FBECEC", font="sans 14 bold")
        lblproveedor.place(x=10, y=80)
        self.proveedor = ttk.Entry(labelframe, font="sans 14 bold")
        self.proveedor.place(x=140, y=80,width=240, height=40)  

        lblprecio = Label(labelframe, text="Precio: ",bg= "#FBECEC", font="sans 14 bold")
        lblprecio.place(x=10, y=140)
        self.precio = ttk.Entry(labelframe, font="sans 14 bold")
        self.precio.place(x=140, y=140, width=240, height=40 )

        lblcosto = Label(labelframe, text="Costo: ",bg= "#FBECEC", font="sans 14 bold")
        lblcosto.place(x=10 , y=200)
        self.costo =ttk.Entry(labelframe, font="sans 14 bold")
        self.costo.place(x=140, y=200, width=240, height=40)

        lblstock = Label(labelframe, text="Stock: ", bg= "#FBECEC", font="sans 14 bold")
        lblstock.place(x=10, y=160)
        self.stock= ttk.Entry (labelframe, font="sans 14 bold")
        self.stock.place (x=140 , y=260, width=240, height=40)

        boton_agregar = tk.Button(labelframe, text="Ingresar", bg= "#CC84BC", font="sans 12 bold")
        boton_agregar.place(x=80,y=340, width=240, height=40)

        boton_editar = tk.Button(labelframe, text="Editar", bg= "#CC84BC", font="sans 12 bold")
        boton_editar.place(x=80,y=400, width=240, height=40)

        #tabla de productos 

        treframe = Frame(frame2, bg="white")
        treframe.place(x=450, y=50, width=620, height=400)

        scrol_y = ttk.Scrollbar(treframe)
        scrol_y.pack(side=RIGHT, fill= Y)

        scrol_x = ttk.Scrollbar(treframe, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill= X)

        self.tre = ttk.Treeview(treframe, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, columns=("ID","PRODUCTO", "PROVEEDOR", "PRECIO","COSTO", "STOCK"), show="headings")
        self.tre.pack(expand=True, fill= BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        self.tre.heading("ID", text= "Id")
        self.tre.heading("PRODUCTO", text= "Producto")
        self.tre.heading("PROVEEDOR", text= "Proveedor")
        self.tre.heading("PRECIO", text= "Precio")
        self.tre.heading("COSTO", text= "Costo")
        self.tre.heading("STOCK", text= "Stock")

        self.tre.column("ID", width=70, anchor= "center")
        self.tre.column("PRODUCTO", width=100, anchor= "center")
        self.tre.column("PROVEEDOR", width=100, anchor= "center")
        self.tre.column("PRECIO", width=100, anchor= "center")
        self.tre.column("COSTO", width=100, anchor= "center")
        self.tre.column("STOCK", width=70, anchor= "center")

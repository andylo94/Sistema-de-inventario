from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Ventas (tk.Frame): # definiendo la clase ventas 
    def __init__(self, parent):
        super().__init__(parent)
        self.widgets()

    def widgets(self): 
        frame1 = tk.Frame(self, bg = '#E99AC4', highlightbackground='#E99AC4',highlightthickness=1 )
        frame1.pack()
        frame1.place(x=0,y=0,width=1100, height=100) #Posicion de la barra. 

        titulo = tk.Label (self, text='VENTAS', bg = '#E99AC4', font= 'sans 30 bold ', anchor='center') # Definicion de texto "ventas" y configuracion de tipo de letra, tamaño, negrilla habilitado y centrado.  
        titulo.pack()
        titulo.place(x=5,y=0, width=1090, height=90 ) #Posicion de la palabra ventas.

        frame2 = tk.Frame (self, bg="#FBECEC", highlightbackground="#FBECEC", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550) #Cuadro de datos de factura.

        lblframe = LabelFrame (frame2, text="Informacion de la venta", bg= "#FBECEC", font="sans 16 bold")
        lblframe.place(x=10, y=10, width=1060, height=80) #Recuadro de la informacion de factura.

        label_num_factura = tk.Label(lblframe, text="Numero de \nfactura", bg= "#FBECEC", font="sans 12 bold")
        label_num_factura.place(x=10, y= 5) 
        self.num_factura = tk.StringVar ()

        self.entry_num_factura = ttk.Entry(lblframe, textvariable = self.num_factura, state= "readonly", font= "sans 12 bold" ) 
        self.entry_num_factura.place (x=100, y=5, width = 80)
        #etiqueta de producto con su entry
        label_nombre = tk.Label(lblframe, text="Productos:", bg= "#FBECEC", font="sans 12 bold")
        label_nombre.place(x=195, y=12 )
        self.entry_nombre = ttk.Entry(lblframe, font="sans 12 bold")
        self.entry_nombre.place(x=285, y=10, width=180)
        #Etiqueta del precio, con su entry
        label_valor = tk.Label(lblframe, text = "Precio:", bg= "#FBECEC", font="sans 12 bold")
        label_valor.place(x=475,y=12)
        self.entry_valor = ttk.Entry(lblframe, font="sans 12 bold" )
        self.entry_valor.place(x=535, y=10, width=180)
        #Etiqueta de la cantidad con su entry
        label_cantidad = tk.Label(lblframe, text="Cantidad: ", bg= "#FBECEC", font="sans 12 bold")
        label_cantidad.place(x=735,y=12)
        self.entry_cantidad = ttk.Entry(lblframe, font="sans 12 bold")
        self.entry_cantidad.place(x=815, y=10)


        #Tabla de la factura 
        treFrame = tk.Frame(frame2,bg= "#FBECEC")
        treFrame.place(x=150 ,y=120, width=800,height=200)

        #barra de desplazamiento vertical para moverse de arriba a abajo
        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side = RIGHT, fill= Y )
        #Barra de desplazamiento inferior para moverse lateralmente 
        scrol_x =ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill= X)

        self.tree = ttk.Treeview(treFrame, columns = ("Producto", "Precio", "Cantidad", "Subtotal"),show="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
        scrol_y.config(command=self.tree.yview)
        scrol_x.config(command=self.tree.xview)

        self.tree.heading("#1", text="Producto")
        self.tree.heading("#2", text="Precio")
        self.tree.heading("#3", text="Cantidad")
        self.tree.heading("#4", text="Subtotal")

        self.tree.column("Producto", anchor= "center")
        self.tree.column("Precio", anchor= "center")
        self.tree.column("Cantidad", anchor= "center")
        self.tree.column("Subtotal", anchor= "center")

        self.tree.pack(expand= True, fill = BOTH)  

        lblframe1 = LabelFrame(frame2, text="Opciones", bg= "#FBECEC", font="sans 12 bold")
        lblframe1.place(x=10,y=380, width=1060 , height=100)

        boton_agregar = tk.Button(lblframe1,text="Agregar articulo", bg= "#CC84BC", font="sans 12 bold")
        boton_agregar.place(x=50,y=10,width=240, height=50)

        boton_pagar = tk.Button(lblframe1,text="Generar factura", bg= "#CC84BC", font="sans 12 bold")
        boton_pagar.place(x=400,y=10,width=240, height=50)

        boton_ver_facturas = tk.Button(lblframe1,text="Ver facturas", bg= "#CC84BC", font="sans 12 bold")
        boton_ver_facturas.place(x=750,y=10,width=240, height=50)

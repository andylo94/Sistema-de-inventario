import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Ventas (tk.Frame): # definiendo la clase ventas 
    db_name ="database.db"


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
        self.entry_nombre = ttk.Combobox(lblframe, font="sans 12 bold", state="readonly")
        self.entry_nombre.place(x=285, y=10, width=180)

        self.cargar_productos()

        #Etiqueta del precio, con su entry
        label_valor = tk.Label(lblframe, text = "Precio:", bg= "#FBECEC", font="sans 12 bold")
        label_valor.place(x=475,y=12)
        self.entry_valor = ttk.Entry(lblframe, font="sans 12 bold", state= "readonly" )
        self.entry_valor.place(x=535, y=10, width=180)

        self.entry_nombre.bind("<<ComboboxSelected>>",self.actualizar_precio)

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

        self.label_suma_total = tk.Label(frame2, text="Total a pagar: COP 0",bg= "#FBECEC", font="sans 25 bold")
        self.label_suma_total.place(x= 360, y=335)

    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT nombre FROM inventario")
            productos = c.fetchall()
            self.entry_nombre ["values"] = [producto [0] for producto in productos]
            if not productos:
                print("No se encontraron pruductos en la base de datos.")
            conn.close()
        except sqlite3.Error as e:
            print("Error al cargar productos desde la base de datos.", e)

    def actualizar_precio(self, event):
        nombre_producto = self.entry_nombre.get()
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT precio FROM inventario WHERE nombre = ?", (nombre_producto,))
            precio = c.fetchone()
            if (precio):
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, precio [0])
                self.entry_valor.config(state="readonly")
            else:
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, "Precio no disponible.")
                self.entry_valor.config(state="readonly")
        except sqlite3.Error as e:
            messagebox.showerror("Error ", f"Error al obtener el precio: {e}")
        finally:
            conn.close()

    def actualizar_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values") [3])
            total += subtotal
        self.label_suma_total.config(text=f"Total a pagar: COP {total:.0f}")

    def registrar(self):
        producto = self.entry_nombre.get()
        precio = self.entry_valor.get()
        cantidad = self.entry_cantidad.get()

        if producto and precio and cantidad:
            try:
                cantidad = int(cantidad)
                if not self.verificar_stock(producto, cantidad):
                    messagebox.showerror("Error ", "Stock insuficiente para el producto seleccionado")

                precio = float(precio)
                subtotal = cantidad * precio

                self.tree.insert("", "end", values =(producto , f"{precio:.0f}", cantidad, f"subtotal:.0f"))

                self.entry_nombre.set("")
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.config(state="readonly")
                self.entry_cantidad.delete(0, tk.END)

                self.actualizar_total()
            except ValueError:
                messagebox.showerror("Error", "Cantidad o precio no validos")
            
        else:
            messagebox.showerror("Error", "Debe completar todos los campos")

    def verificar_stock(self, nombre_porducto, cantidad):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT stock FROM inventario WHERE nombre = ?", (nombre_porducto,))
            stock = c.fetchone()
            if stock and stock[0] >= cantidad:
                return True
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al verificar el stock: {e}")
            return False

        finally:
            conn.close()

    def obtener_total(self):

        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values" [3]))
            total += subtotal
        return total

    def pagar ()




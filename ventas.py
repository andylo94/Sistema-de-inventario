import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import datetime
import sys 
import os

class Ventas (tk.Frame): # definiendo la clase ventas 
    db_name ="database.db"


    def __init__(self, parent):
        super().__init__(parent)
        self.numero_factura_actual = self.obtener_numero_factura_actual()
        self.widgets()
        self.mostrar_numero_factura()
        

    def widgets(self): 
        frame1 = tk.Frame(self, bg = '#007790', highlightbackground='#007790',highlightthickness=1 )
        frame1.pack()
        frame1.place(x=0,y=0,width=1100, height=100) #Posicion de la barra. 

        titulo = tk.Label (self, text='VENTAS', bg = '#007790', font= 'sans 30 bold ', anchor='center') # Definicion de texto "ventas" y configuracion de tipo de letra, tamaño, negrilla habilitado y centrado.  
        titulo.pack()
        titulo.place(x=5,y=0, width=1090, height=90 ) #Posicion de la palabra ventas.

        frame2 = tk.Frame (self, bg="#21c0d5", highlightbackground="#21c0d5", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550) #Cuadro de datos de factura.

        lblframe = LabelFrame (frame2, text="Informacion de la venta", bg= "#21c0d5", font="sans 16 bold")
        lblframe.place(x=10, y=10, width=1060, height=80) #Recuadro de la informacion de factura.

        label_num_factura = tk.Label(lblframe, text="Numero de \nfactura", bg= "#21c0d5", font="sans 12 bold")
        label_num_factura.place(x=10, y= 5) 
        self.num_factura = tk.StringVar ()

        self.entry_num_factura = ttk.Entry(lblframe, textvariable = self.num_factura, state= "readonly", font= "sans 12 bold" ) 
        self.entry_num_factura.place (x=100, y=5, width = 80)
        #etiqueta de producto con su entry
        label_nombre = tk.Label(lblframe, text="Productos:", bg= "#21c0d5", font="sans 12 bold")
        label_nombre.place(x=195, y=12 )
        self.entry_nombre = ttk.Combobox(lblframe, font="sans 12 bold", state="readonly")
        self.entry_nombre.place(x=285, y=10, width=180)

        self.cargar_productos()

        #Etiqueta del precio, con su entry
        label_valor = tk.Label(lblframe, text = "Precio:", bg= "#21c0d5", font="sans 12 bold")
        label_valor.place(x=475,y=12)
        self.entry_valor = ttk.Entry(lblframe, font="sans 12 bold", state= "readonly" )
        self.entry_valor.place(x=535, y=10, width=180)

        self.entry_nombre.bind("<<ComboboxSelected>>",self.actualizar_precio)

        #Etiqueta de la cantidad con su entry
        label_cantidad = tk.Label(lblframe, text="Cantidad: ", bg= "#21c0d5", font="sans 12 bold")
        label_cantidad.place(x=735,y=12)
        self.entry_cantidad = ttk.Entry(lblframe, font="sans 12 bold")
        self.entry_cantidad.place(x=815, y=10)

        #Tabla de la factura 
        treFrame = tk.Frame(frame2,bg= "#21c0d5")
        treFrame.place(x=40 ,y=120, width=1030,height=200)

        #barra de desplazamiento vertical para moverse de arriba a abajo
        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side = RIGHT, fill= Y )
        #Barra de desplazamiento inferior para moverse lateralmente 
        scrol_x =ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill= X)

        self.tree = ttk.Treeview(treFrame, columns = ("Producto", "Precio", "Cantidad", "Subtotal", "Proveedor"),show="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
        scrol_y.config(command=self.tree.yview)
        scrol_x.config(command=self.tree.xview)

        self.tree.heading("#1", text="Producto")
        self.tree.heading("#2", text="Precio")
        self.tree.heading("#3", text="Cantidad")
        self.tree.heading("#4", text="Subtotal")
        self.tree.heading("#5", text="Proveedor")

        self.tree.column("Producto", anchor= "center")
        self.tree.column("Precio", anchor= "center")
        self.tree.column("Cantidad", anchor= "center")
        self.tree.column("Subtotal", anchor= "center")
        self.tree.column("Proveedor", anchor="center")

        self.tree.pack(expand= True, fill = BOTH)  

        lblframe1 = LabelFrame(frame2, text="Opciones", bg= "#21c0d5", font="sans 12 bold")
        lblframe1.place(x=10,y=380, width=1060 , height=100)

        # Etiqueta para mostrar el total a pagar
        self.label_suma_total = tk.Label(frame2, text="Total a pagar: COP 0", bg="#21c0d5", font="sans 16 bold")
        self.label_suma_total.place(x=750, y=330)  

        boton_agregar = tk.Button(lblframe1, text="Agregar articulo", bg="#007790", font="sans 12 bold", command=self.registrar)
        boton_agregar.place(x=50, y=10, width=200, height=50)

        boton_eliminar = tk.Button(lblframe1, text="Eliminar articulo", bg="#007790", font="sans 12 bold", command=self.eliminar_articulo)
        boton_eliminar.place(x=300, y=10, width=200, height=50)

        boton_pagar = tk.Button(lblframe1, text="Pagar", bg="#007790", font="sans 12 bold", command=self.abrir_ventana_pago)
        boton_pagar.place(x=550, y=10, width=200, height=50)

        boton_ver_facturas = tk.Button(lblframe1, text="Productos facturados", bg="#007790", font="sans 12 bold", command=self.abrir_ventana_factura)
        boton_ver_facturas.place(x=800, y=10, width=200, height=50)

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
            c.execute("SELECT precio, proveedor FROM inventario WHERE nombre = ?", (nombre_producto,))
            resultado = c.fetchone()
            if resultado:
                precio, proveedor = resultado
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, precio )
                self.entry_valor.config(state="readonly")
                self.proveedor_actual = proveedor
            else:
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, "Precio no disponible.")
                self.entry_valor.config(state="readonly")
                self.proveedor_actual = ""
        except sqlite3.Error as e:
            messagebox.showerror("Error ", f"Error al obtener el precio: {e}")
        finally:
            conn.close()

    def actualizar_total(self):
        total = 0.0
        
        for child in self.tree.get_children():
            valores = self.tree.item(child, "values")
            if valores and len(valores) >= 4:  # Asegurar que hay suficientes valores
                subtotal = float(valores[3])
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
                proveedor = self.proveedor_actual

                self.tree.insert("", "end", values =(producto , f"{precio:.0f}", cantidad, f"{subtotal:.0f}",proveedor))

                self.entry_nombre.set("")
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.config(state="readonly")
                self.entry_cantidad.delete(0, tk.END)
                self.proveedor_actual = ""  

                self.actualizar_total()
            except ValueError:
                messagebox.showerror("Error", "Cantidad o precio no validos")
            
        else:
            messagebox.showerror("Error", "Debe completar todos los campos")
    def eliminar_articulo(self):
    # Obtener el artículo seleccionado
        seleccionado = self.tree.selection()
    
        if not seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un artículo para eliminar")
            return

    # Confirmación antes de eliminar
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar el artículo seleccionado?")
    
        if respuesta:
        # Eliminar el artículo seleccionado
            self.tree.delete(seleccionado)
            self.actualizar_total()

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
            subtotal = float(self.tree.item(child, "values") [3])
            total += subtotal
        return total

    def abrir_ventana_pago(self):
        if not self.tree.get_children():
            messagebox.showerror("Error","No hay articulos para pagar")
            return
        ventana_pago = Toplevel(self)
        ventana_pago.title("Realizar pago")
        ventana_pago.geometry("400x400")
        ventana_pago.config(bg="#21c0d5")
        ventana_pago.resizable(False,False)

        label_total= tk.Label(ventana_pago, bg="#21c0d5", text= f"Total a pagar: COP {self.obtener_total():.0f}", font= "sans 18 bold")
        label_total.place(x=70, y=20)

        label_cantidad_pagada = tk.Label(ventana_pago, bg="#21c0d5", text="Cantidad pagada:", font= "sans 14 bold")
        label_cantidad_pagada.place (x=120, y=90)
        entry_cantidad_pagada = ttk.Entry(ventana_pago, font="sans 14 bold")
        entry_cantidad_pagada.place (x=80, y=130)

        label_nombre_cliente = tk.Label(ventana_pago,bg="#21c0d5",text="Nombre cliente: ",font="sans 14 bold")
        label_nombre_cliente.place(x=10, y=350)
        entry_nombre_cliente =ttk.Entry(ventana_pago, font="sans 14 bold")
        entry_nombre_cliente.place(x=165,y=350) 


        label_cambio =tk.Label(ventana_pago, bg="#21c0d5", text="", font="sans 14 bold")
        label_cambio.place(x=100, y=190)

        def calcular_cambio():
            try:
                cantidad_pagada = float(entry_cantidad_pagada.get())
                total = self.obtener_total()
                cambio = cantidad_pagada - total
                if cambio < 0:
                    messagebox.showerror("Error", "La cantidad pagada es insuficiente.")
                    return
                label_cambio.config(text=f"El cambio es: COP {cambio:.0f}")
            except ValueError:
                messagebox.showerror("Error", "Cantidad pagada no validad.")

        boton_calcular= tk.Button(ventana_pago, text="Calcular devolucion", bg="#007790", font= "sans 12 bold", command=calcular_cambio)
        boton_calcular.place(x=80, y= 240, width=240, height=40)

        boton_pagar= tk.Button(ventana_pago, text="Pagar", bg="#007790", font= "sans 12 bold", command=lambda: self.pagar(ventana_pago,entry_cantidad_pagada,entry_nombre_cliente, label_cambio))
        boton_pagar.place(x=80, y= 300, width=240, height=40)

    def pagar(self, ventana_pago, entry_cantidad_pagada, entry_nombre_cliente, label_cambio):
        try:
            nombre_cliente = entry_nombre_cliente.get()

            cantidad_pagada = float(entry_cantidad_pagada.get())
            total = self.obtener_total()
            cambio = cantidad_pagada - total
            if cambio <0:
                messagebox.showerror("Error", "La cantidad pagada es insuficiente")
                return
            conn = sqlite3.connect(self.db_name) 
            c = conn.cursor()
            try:
                productos = []
                for child in self.tree.get_children():
                    item = self.tree.item(child, "values")
                    producto = item[0]
                    precio = item[1]
                    cantidad_vendida = int(item[2])
                    subtotal = float(item[3])
                    productos.append([producto, precio, cantidad_vendida, subtotal])
                    
                    c.execute("INSERT INTO ventas (factura, nombre_articulo, valor_articulo, cantidad, subtotal) Values (?,?,?,?,?)",
                              (self.numero_factura_actual, producto, float(precio), cantidad_vendida, subtotal))
                    
                    c.execute("UPDATE inventario SET stock = stock - ? WHERE nombre = ?", (cantidad_vendida, producto))

                conn.commit()
                messagebox.showinfo("Exito", "Venta registrada exitosamente.")

                self.numero_factura_actual += 1
                self.mostrar_numero_factura()

                for child in self.tree.get_children():
                    self.tree.delete(child)
                self.label_suma_total.config(text= "Total a pagar: COP 0")
                
                ventana_pago.destroy()

                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.generar_factura_pdf(productos, total, self.numero_factura_actual - 1, fecha, nombre_cliente)


            except sqlite3.Error as e:
                conn.rollback()
                messagebox.showerror("Error", f"Error al registrar la venta: {e}")
            finally:
                conn.close()

        except ValueError:
            messagebox.showerror("Error", "Cantidad pagada no validad")

    def generar_factura_pdf(self, productos, total, factura_numero, fecha, nombre_cliente):
        archivo_pdf = f"Facturas/factura_{factura_numero}.pdf"
        c = canvas.Canvas(archivo_pdf, pagesize=letter)
        width, height = letter

    # Centrar los títulos en la página
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, height - 30, "RASGO S.A.S")
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 60, f"Factura número: {factura_numero}")

        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, height - 80, f"Nombre del cliente: {nombre_cliente}")

        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, height - 100, f"Fecha: {fecha}")

        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, height - 120, "Información de la venta:")

    # Crear tabla de productos dinámicamente
        data = [["Producto", "Precio", "Cantidad", "Subtotal"]] + productos
        table = Table(data, colWidths=[150, 100, 100, 100])  # Ancho de columnas
        # Definir el color manualmente con valores normalizados (RGB)
        color_fondo = colors.Color(33/255, 192/255, 213/255)

    # Estilo de la tabla
        style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), color_fondo),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)

    # Determinar la altura de la tabla dinámicamente
        table_height = 20 + (len(productos) * 20)  # Calcula el espacio necesario
        table_y_position = height - 160  # Altura inicial
        table.wrapOn(c, width, height)
        table.drawOn(c, (width - 450) / 2, table_y_position - table_height)  # Centrar la tabla

    # Ajustar posición de los textos siguientes
        nueva_pos_y = table_y_position - table_height - 40  # Baja según la tabla

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, nueva_pos_y, f"Total a pagar: COP {total:.0f}")

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, nueva_pos_y - 40, "Gracias por su compra.")

        c.save()

        messagebox.showinfo("Factura Generada", f"La factura # {factura_numero} ha sido creada exitosamente")

        os.startfile(os.path.abspath(archivo_pdf))
        
    def obtener_numero_factura_actual(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT MAX(factura) FROM ventas")
            max_factura = c.fetchone()[0]
            if max_factura:
                return max_factura +1
            else: 
                return 1
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el numero de factura: {e}")
            return 1
        finally:
            conn.close()
    def mostrar_numero_factura(self):
        self.num_factura.set(self.numero_factura_actual)

    def abrir_ventana_factura(self):
        ventana_facturas = Toplevel(self)
        ventana_facturas.title("Facturas")
        ventana_facturas.geometry("800x550")  # Ajuste para mostrar totales
        ventana_facturas.config(bg="#21c0d5")
        ventana_facturas.resizable(False, False)

        facturas = Label(ventana_facturas, bg="#21c0d5", text="Productos Facturados", font="sans 36 bold")
        facturas.place(x=150, y=15)

        treFrame = Frame(ventana_facturas, bg="#21c0d5")
        treFrame.place(x=10, y=100, width=780, height=380)
    
        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)
    
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        tree_facturas = ttk.Treeview(treFrame, columns=("ID", "Factura", "Producto", "Precio", "Cantidad", "Subtotal"), show="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
    
        scrol_y.config(command=tree_facturas.yview)
        scrol_x.config(command=tree_facturas.xview)

        tree_facturas.heading("#1", text="ID")
        tree_facturas.heading("#2", text="Factura")
        tree_facturas.heading("#3", text="Producto")
        tree_facturas.heading("#4", text="Precio")
        tree_facturas.heading("#5", text="Cantidad")
        tree_facturas.heading("#6", text="Subtotal")

        tree_facturas.column("ID", width=70, anchor="center")
        tree_facturas.column("Factura", width=100, anchor="center")
        tree_facturas.column("Producto", width=200, anchor="center")
        tree_facturas.column("Precio", width=130, anchor="center")
        tree_facturas.column("Cantidad", width=130, anchor="center")
        tree_facturas.column("Subtotal", width=130, anchor="center")

        tree_facturas.pack(expand=True, fill=BOTH)
    
        self.cargar_facturas(tree_facturas)
    
    # Sección de totales
        frame_totales = Frame(ventana_facturas, bg="#21c0d5")
        frame_totales.place(x=10, y=490, width=780, height=50)
    
        Label(frame_totales, text="Total Precio de venta:", bg="#21c0d5", font="sans 12 ").place(x=10, y=10)
        total_precio = Label(frame_totales, text="0.00", bg="#21c0d5", font="sans 12 bold")
        total_precio.place(x=170, y=10)
    
        Label(frame_totales, text="Total Cantidad:", bg="#21c0d5", font="sans 12 ").place(x=300, y=10)
        total_cantidad = Label(frame_totales, text="0", bg="#21c0d5", font="sans 12 bold")
        total_cantidad.place(x=450, y=10)
    
        Label(frame_totales, text=" Subtotal:", bg="#21c0d5", font="sans 12 ").place(x=580, y=10)
        total_subtotal = Label(frame_totales, text="0.00", bg="#21c0d5", font="sans 12 bold")
        total_subtotal.place(x=650, y=10)
    
    # Actualizar los totales después de cargar los datos
        self.actualizar_totales(tree_facturas, total_precio, total_cantidad, total_subtotal)

    def actualizar_totales(self, tree, lbl_precio, lbl_cantidad, lbl_subtotal):
        total_precio = 0
        total_cantidad = 0
        total_subtotal = 0
    
        for item in tree.get_children():
            valores = tree.item(item, "values")
            if valores:
                total_precio += float(valores[3])  # Precio
                total_cantidad += int(valores[4])  # Cantidad
                total_subtotal += float(valores[5])  # Subtotal
    
        lbl_precio.config(text=f"{total_precio:.0f}")
        lbl_cantidad.config(text=f"{total_cantidad}")
        lbl_subtotal.config(text=f"{total_subtotal:.0f}")

    def cargar_facturas(self, tree):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM ventas")
            facturas = c.fetchall()
            for factura in facturas:
                tree.insert("","end", values=factura)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar las facturas: {e}")

                    






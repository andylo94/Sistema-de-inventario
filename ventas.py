import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import datetime
import sys 
import os

class Ventas (tk.Frame): # definiendo la clase ventas 
    db_name ="database.db"

    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.numero_factura_actual = self.obtener_numero_factura_actual()
        self.controlador = controlador
        self.productos = []  # Inicializa la lista de productos aquí
        self.listbox_toplevel = None
        self.proveedor_actual = ""
        self.widgets()
        self.cargar_productos()  # Asegúrate de cargar los productos al inicio
        self.mostrar_numero_factura()
        
    def widgets(self): 
        frame1 = tk.Frame(self, bg = '#007790', highlightbackground='#007790',highlightthickness=1 )
        frame1.pack()
        frame1.place(x=0,y=0,width=1100, height=100) #Posicion de la barra. 

        titulo = tk.Label (self, text='SALIDAS', fg='white', bg = '#007790', font= 'sans 30 bold ', anchor='center')  
        titulo.pack()
        titulo.place(x=5,y=0, width=1090, height=90 ) 

        frame2 = tk.Frame (self, bg="#21c0d5", highlightbackground="#21c0d5", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550) 

        lblframe = LabelFrame (frame2, text="Informacion de la salida", bg= "#21c0d5", font="sans 16 bold")
        lblframe.place(x=10, y=10, width=1060, height=80) 

        label_num_factura = tk.Label(lblframe, text="Consecutivo \nde salida", bg= "#21c0d5", font="sans 10 bold")
        label_num_factura.place(x=10, y= 5) 
        self.num_factura = tk.StringVar ()

        self.entry_num_factura = ttk.Entry(lblframe, textvariable = self.num_factura, state= "readonly", font= "sans 12 bold" ) 
        self.entry_num_factura.place (x=100, y=5, width = 80)

        # Etiqueta de producto con su entry
        label_nombre = tk.Label(lblframe, text="Reactivo:", bg="#21c0d5", font="sans 12 bold")
        label_nombre.place(x=195, y=12)
        
        self.entry_nombre = ttk.Entry(lblframe, font="sans 12 bold")
        self.entry_nombre.place(x=285, y=10, width=180)
        self.entry_nombre.bind("<KeyRelease>", self.filtrar_productos)

        # Etiqueta del precio, con su entry
        label_valor = tk.Label(lblframe, text = "Lote:", bg= "#21c0d5", font="sans 12 bold")
        label_valor.place(x=475,y=12)
        self.entry_valor = ttk.Entry(lblframe, font="sans 12 bold", state= "readonly" )
        self.entry_valor.place(x=535, y=10, width=180)

        # Etiqueta de la cantidad con su entry
        label_cantidad = tk.Label(lblframe, text="Cantidad: ", bg= "#21c0d5", font="sans 12 bold")
        label_cantidad.place(x=735,y=12)
        self.entry_cantidad = ttk.Entry(lblframe, font="sans 12 bold")
        self.entry_cantidad.place(x=815, y=10)

        # Tabla de la factura 
        treFrame = tk.Frame(frame2,bg= "#21c0d5")
        treFrame.place(x=40 ,y=120, width=1030,height=200)

        # Barra de desplazamiento vertical
        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side = RIGHT, fill= Y )
        # Barra de desplazamiento horizontal
        scrol_x =ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill= X)

        self.tree = ttk.Treeview(treFrame, columns = ("Producto", "Lote", "Cantidad", "Proveedor"), show="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
        scrol_y.config(command=self.tree.yview)
        scrol_x.config(command=self.tree.xview)

        self.tree.heading("#1", text="Reactivo")
        self.tree.heading("#2", text="Lote")
        self.tree.heading("#3", text="Cantidad")
        self.tree.heading("#4", text="Proveedor")
        #self.tree.heading("#4", text="Subtotal")

        self.tree.column("Producto", anchor= "center")
        self.tree.column("Lote", anchor= "center")
        self.tree.column("Cantidad", anchor= "center")
        #self.tree.column("Subtotal", anchor= "center")
        self.tree.column("Proveedor", anchor="center")

        self.tree.pack(expand= True, fill = BOTH)  

        lblframe1 = LabelFrame(frame2, text="Opciones:", bg= "#21c0d5", font="sans 12 bold")
        lblframe1.place(x=10,y=380, width=1060 , height=100)

        # Etiqueta para mostrar el total a pagar
        self.label_suma_total = tk.Label(frame2, text="Total a pagar: COP 0", bg="#21c0d5", font="sans 16 bold")
        #self.label_suma_total.place(x=750, y=330)  

        boton_agregar = tk.Button(lblframe1, text="Retirar Reactivo",fg='white', bg="#007790", font="sans 12 bold", command=self.registrar)
        boton_agregar.place(x=50, y=10, width=200, height=50)

        boton_eliminar = tk.Button(lblframe1, text="Eliminar Reactivos",fg='white', bg="#007790", font="sans 12 bold", command=self.eliminar_articulo)
        boton_eliminar.place(x=300, y=10, width=200, height=50)

        boton_retiro = tk.Button(lblframe1, text="Consumir Reactivo",fg='white', bg="#007790", font="sans 12 bold", command=self.abrir_ventana_retiro)
        boton_retiro.place(x=550, y=10, width=200, height=50)

        boton_ver_facturas = tk.Button(lblframe1, text="Reactivos Consumidos",fg='white', bg="#007790", font="sans 12 bold", command=self.abrir_ventana_documento)
        boton_ver_facturas.place(x=800, y=10, width=200, height=50)

    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT nombre FROM inventario")
            productos = c.fetchall()
            self.productos = [producto[0] for producto in productos]  # Guardar productos en una lista
            conn.close()
        except sqlite3.Error as e:
            print("Error al cargar productos desde la base de datos.", e)

    def filtrar_productos(self, event):
        texto = self.entry_nombre.get().lower()

        if self.listbox_toplevel:
            self.listbox_toplevel.destroy()

        if texto:
            coincidencias = [p for p in self.productos if texto in p.lower()]

            if coincidencias:
                self.listbox_toplevel = tk.Toplevel(self)
                self.listbox_toplevel.wm_overrideredirect(True)
                self.listbox_toplevel.geometry(
                    f"300x150+{self.entry_nombre.winfo_rootx()}+{self.entry_nombre.winfo_rooty() + 30}"
                )
                self.listbox_toplevel.lift()

                listbox = Listbox(self.listbox_toplevel, font="sans 11")
                listbox.pack(expand=True, fill=tk.BOTH)

                self.productos_dict = {}  # ← Diccionario para vincular texto mostrado y nombre real

                try:
                    conn = sqlite3.connect(self.db_name)
                    c = conn.cursor()

                    for producto in coincidencias:
                        c.execute("SELECT precio FROM inventario WHERE nombre = ?", (producto,))
                        resultado = c.fetchone()
                        if resultado:
                            precio = resultado[0]
                            display = f"{producto} / {precio}"
                            listbox.insert(tk.END, display)
                            self.productos_dict[display] = producto
                        else:
                            display = f"{producto} / ?"
                            listbox.insert(tk.END, display)
                            self.productos_dict[display] = producto
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error al buscar precios: {e}")
                finally:
                    conn.close()

                listbox.bind("<<ListboxSelect>>", lambda event, lb=listbox: self.seleccionar_producto(event, lb))
            else:
                self.cerrar_listbox()
        else:
            self.cerrar_listbox()

    def seleccionar_producto(self, event, listbox):
        seleccion = listbox.curselection()
        if seleccion:
            item_texto = listbox.get(seleccion[0])
            producto = self.productos_dict.get(item_texto, "").strip()  # ← Obtener nombre exacto

            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, producto)
            self.cerrar_listbox()

            try:
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                c.execute("SELECT precio, proveedor FROM inventario WHERE nombre = ?", (producto,))
                resultado = c.fetchone()
                if resultado:
                    precio, proveedor = resultado
                    self.entry_valor.config(state="normal")
                    self.entry_valor.delete(0, tk.END)
                    self.entry_valor.insert(0, str(precio))
                    self.entry_valor.config(state="readonly")
                    self.proveedor_actual = proveedor
                else:
                    messagebox.showerror("Error", "Producto no encontrado en la base de datos.")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al obtener el precio: {e}")
            finally:
                conn.close()
    def cerrar_listbox(self):
        if self.listbox_toplevel:
            self.listbox_toplevel.destroy()
            self.listbox_toplevel = None


    def registrar(self):
        producto = self.entry_nombre.get()
        precio = self.entry_valor.get()
        cantidad = self.entry_cantidad.get()

        if producto and precio and cantidad:
            try:
                cantidad = int(cantidad)
                if not self.verificar_stock(producto, cantidad):
                    messagebox.showerror("Error ", "Stock insuficiente para el producto seleccionado")
                    return  # Salir de la función si no hay stock suficiente
                
                proveedor = self.proveedor_actual

                self.tree.insert("", "end", values =(producto , precio, cantidad, proveedor))

                # Limpiar los campos después de agregar el producto
                self.entry_nombre.delete(0, tk.END)
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.config(state="readonly")
                self.entry_cantidad.delete(0, tk.END)
                self.proveedor_actual = ""    

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


    def abrir_ventana_retiro(self):
        if not self.tree.get_children():
            messagebox.showerror("Error", "No hay artículos para retirar")
            return

        ventana_retiro = Toplevel(self)
        ventana_retiro.title("Confirmar retiro")
        ventana_retiro.geometry("400x250")
        ventana_retiro.update_idletasks()

        ancho_pantalla = ventana_retiro.winfo_screenwidth()
        alto_pantalla = ventana_retiro.winfo_screenheight()
        x = (ancho_pantalla // 2) - (400 // 2)
        y = (alto_pantalla // 2) - (250 // 2)
        ventana_retiro.geometry(f"420x200+{x}+{y}")
        ventana_retiro.config(bg="#21c0d5")
        ventana_retiro.resizable(False, False)

        label_info = tk.Label(ventana_retiro, bg="#21c0d5", text="¿Desea confirmar el retiro de los productos?", font="sans 14 bold")
        label_info.place(relx=0.5, y=40, anchor="center")

        label_total = tk.Label(ventana_retiro, bg="#21c0d5", text=f"Total de productos: {len(self.tree.get_children())}", font="sans 12 bold")
        label_total.place(relx=0.5, y=80, anchor="center")

        label_nombre_analista = tk.Label(ventana_retiro, bg="#21c0d5", text="Nombre del analista:", font="sans 12 bold")
        label_nombre_analista.place(x=20, y=110)
        entry_nombre_analista = ttk.Entry(ventana_retiro, font="sans 12")
        entry_nombre_analista.place(x=180, y=110, width=180)

        boton_confirmar = tk.Button(ventana_retiro, text="Confirmar Retiro",fg='white', bg="#007790", font="sans 12 bold",  command=lambda: self.retiro(ventana_retiro, entry_nombre_analista))
        boton_confirmar.place(x=100, y=150, width=200, height=40)

    def retiro(self, ventana_retiro, entry_nombre__analista):
        try:
            nombre_analista = entry_nombre__analista.get()
            if not nombre_analista:
                messagebox.showerror("Error", "Debe ingresar el nombre del analista.")
                return

            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            try:
                productos = []
                for child in self.tree.get_children():
                    item = self.tree.item(child, "values")
                    producto = item[0]
                    lote = item[1]
                    cantidad_utilizada = int(item[2])
                    proveedor = item[3] 
                    productos.append([producto, lote, cantidad_utilizada, proveedor])

                    # Registrar en tabla de ventas
                    c.execute("INSERT INTO ventas (factura, nombre_articulo, valor_articulo, cantidad) VALUES (?, ?, ?, ?)",
                            (self.numero_factura_actual, producto, lote, cantidad_utilizada))

                    # Actualizar stock
                    c.execute("UPDATE inventario SET stock = stock - ? WHERE nombre = ?", (cantidad_utilizada, producto))

                    # Eliminar si el stock llega a 0
                    c.execute("SELECT stock FROM inventario WHERE nombre = ?", (producto,))
                    nuevo_stock = c.fetchone()
                    if nuevo_stock and nuevo_stock[0] <= 0:
                        c.execute("DELETE FROM inventario WHERE nombre = ?", (producto,))

                conn.commit()
                messagebox.showinfo("Éxito", "Retiro registrado exitosamente.")

                self.numero_factura_actual += 1
                self.mostrar_numero_factura()

                for child in self.tree.get_children():
                    self.tree.delete(child)
                self.label_suma_total.config(text="Total a pagar: COP 0")

                ventana_retiro.destroy()

                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.generar_documento_pdf(productos, self.numero_factura_actual - 1, fecha, nombre_analista)

            except sqlite3.Error as e:
                conn.rollback()
                messagebox.showerror("Error", f"Error al registrar el retiro: {e}")
            finally:
                conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def generar_documento_pdf(self, productos, factura_numero, fecha, nombre_analista):
        archivo_pdf = f"Salidas/Registro_salida_{factura_numero}.pdf"
        c = canvas.Canvas(archivo_pdf, pagesize=letter)
        width, height = letter

        # Margen
        margen_izq = 50
        margen_sup = height - 50

        # --- Encabezado ---
        c.setFont("Helvetica-Bold", 18)
        c.drawString(margen_izq, margen_sup, "Retiro de Reactivos")

        # Línea bajo título
        c.setStrokeColor(colors.HexColor("#219CD5"))
        c.setLineWidth(2)
        c.line(margen_izq, margen_sup - 10, width - margen_izq, margen_sup - 10)

        # Datos arriba derecha: Número documento y fecha
        c.setFont("Helvetica", 12)
        c.drawRightString(width - margen_izq, margen_sup, f"N° Documento: {factura_numero}")
        c.drawRightString(width - margen_izq, margen_sup - 30, f"Fecha: {fecha}")

        # Espacio antes de la tabla
        y_inicio_tabla = margen_sup - 70

        # --- Tabla ---
        data = [["Producto", "Lote", "Cantidad", "Proveedor"]] + productos
        table = Table(data, colWidths=[150, 100, 100, 100])

        color_fondo = colors.Color(33/255, 192/255, 213/255)
        style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), color_fondo),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("GRID", (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)

        # Altura de tabla dinámica
        table_height = 20 + (len(productos) * 20)
        table.wrapOn(c, width, height)
        table.drawOn(c, (width - 450) / 2, y_inicio_tabla - table_height)

        # --- Cuadro de firma abajo ---
        firma_y = y_inicio_tabla - table_height - 80
        cuadro_ancho = 300
        cuadro_alto = 60
        cuadro_x = (width - cuadro_ancho) / 2

        # Dibujar recuadro
        c.setStrokeColor(colors.black)
        c.rect(cuadro_x, firma_y, cuadro_ancho, cuadro_alto, stroke=1, fill=0)

        # Texto "Firma"
        c.setFont("Helvetica-Bold", 12)
        c.drawString(cuadro_x + 5, firma_y + cuadro_alto - 20, "Nombre Analista:")

        # Nombre analista dentro del recuadro, centrado verticalmente y algo indentado
        c.setFont("Helvetica", 12)
        c.drawString(cuadro_x + 110, firma_y + cuadro_alto - 20, nombre_analista)

        # --- Número de página en pie ---
        c.setFont("Helvetica-Oblique", 10)
        c.drawRightString(width - margen_izq, 30, "Página 1")

        # Guardar PDF
        c.save()

        messagebox.showinfo("Documento Generado", f"El documento # {factura_numero} ha sido creado exitosamente")

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
            messagebox.showerror("Error", f"Error al obtener el numero de documento: {e}")
            return 1
        finally:
            conn.close()

    def mostrar_numero_factura(self):
        self.num_factura.set(self.numero_factura_actual)

    def abrir_ventana_documento(self):
        ventana_facturas = Toplevel(self)
        ventana_facturas.title("Reativos Conusmidos")
        ventana_facturas.config(bg="#21c0d5")
        ventana_facturas.resizable(False, False)
        ruta = self.rutas (r"icono.ico")
        ventana_facturas.iconbitmap(ruta)        

        ancho_ventana = 800
        alto_ventana = 500
        ancho_pantalla = ventana_facturas.winfo_screenwidth()
        alto_pantalla = ventana_facturas.winfo_screenheight()
        x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        y = int((alto_pantalla / 2) - (alto_ventana / 2))
        ventana_facturas.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")


        reactivos = Label(ventana_facturas, bg="#21c0d5", text="Reactivos consumidos",fg = 'white', font="sans 36 bold")
        reactivos.place(x=150, y=15)

        treFrame = Frame(ventana_facturas, bg="#21c0d5")
        treFrame.place(x=10, y=100, width=780, height=380)
    
        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)
    
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        tree_facturas = ttk.Treeview(treFrame, columns=("ID", "Documento", "Producto", "Lote", "Cantidad"), show="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
    
        scrol_y.config(command=tree_facturas.yview)
        scrol_x.config(command=tree_facturas.xview)

        tree_facturas.heading("#1", text="ID")
        tree_facturas.heading("#2", text="Documento de retiro")
        tree_facturas.heading("#3", text="Producto")
        tree_facturas.heading("#4", text="lote")
        tree_facturas.heading("#5", text="Cantidad")
        #tree_facturas.heading("#6", text="Subtotal")

        tree_facturas.column("ID", width=70, anchor="center")
        tree_facturas.column("Documento", width=100, anchor="center")
        tree_facturas.column("Producto", width=200, anchor="center")
        tree_facturas.column("Lote", width=130, anchor="center")
        tree_facturas.column("Cantidad", width=130, anchor="center")
        #tree_facturas.column("Subtotal", width=130, anchor="center")
        def _on_mouse_wheel(event):
            if event.num == 4:  # scroll up en Linux
                tree_facturas.yview_scroll(-1, "units")
            elif event.num == 5:  # scroll down en Linux
                tree_facturas.yview_scroll(1, "units")
            else:  # Windows y MacOS
                tree_facturas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        tree_facturas.pack(expand=True, fill=BOTH)
    
        self.cargar_documento(tree_facturas)
        

    def rutas(self, ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase,ruta)
    
    def cargar_documento(self, tree):
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

            
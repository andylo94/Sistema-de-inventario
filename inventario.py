import sqlite3 
from tkinter import *
import tkinter as tk 
from tkinter import ttk, messagebox
import os
import sys
from datetime import datetime
from tkinter import Toplevel, Label, Entry, Button, messagebox
from tkinter.ttk import Combobox

class Inventario (tk.Frame):
    db_name ="database.db"

    def __init__ (self, padre,controlador ):
        super().__init__ (padre)
        self.controlador = controlador  # referencia al Manager
        self.btn_admin = tk.Button(self, text="Función Admin", state="disabled")
        self.btn_admin.pack()

        self.verificar_rol()
        self.pack()
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.controlador = controlador
        self.rol_usuario = controlador.rol_actual 
        self.widgets()

    def verificar_rol(self):
        rol = getattr(self.controlador, 'rol_actual', None)
        if rol == "admin":
            self.btn_admin.config(state="normal")
        else:
            self.btn_admin.config(state="disabled")  

    def widgets(self):
        frame1 = tk.Frame(self, bg='#007790', highlightbackground='#007790', highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)

        titulo = tk.Label(self, text="INVENTARIO", fg='white', bg='#007790',
                        font='sans 30 bold', anchor='center')
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)

        self.boton_agregar_fabricante = tk.Button(titulo, text="Ingresar Fabricante", fg='white', bg="#21c0d5",
                                   font="sans 12 bold", command=self.agregar_categoria)
        self.boton_agregar_fabricante.place(x=850, y=10, width=200, height=30)

        self.boton_agregar_categoria = tk.Button(titulo, text="Ingresar Categoria", fg='white', bg="#21c0d5",
                                   font="sans 12 bold", command=self.agregar_categoria)
        self.boton_agregar_categoria.place(x=850, y=50, width=200, height=30)

        frame2 = tk.Frame(self, bg="#21c0d5", highlightbackground="#21c0d5", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        lbl_filtro_categoria = tk.Label(frame2, text="Filtrar por categoría:", bg="#21c0d5", font="sans 12 bold")
        lbl_filtro_categoria.place(x=570, y=10)

        self.combo_filtro_categoria = ttk.Combobox(frame2, font="sans 12", state="readonly")
        self.combo_filtro_categoria.place(x=740, y=10, width=200, height=30)

        self.boton_agregar_actualizar = tk.Button(frame2, text="🔄", fg='white', bg="#007790",
                                   font="sans 22 bold", anchor = 'center', command=self.actualizar_inventario)
        self.boton_agregar_actualizar.place(x=1020, y=10, width=25, height=25)
        
        # Cargar categorías en el filtro
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, categoria_nombre FROM tb_categorias")
        categorias = cursor.fetchall()
        conn.close()

        self.categorias_dict = {nombre: id_ for id_, nombre in categorias}
        self.combo_filtro_categoria['values'] = ["Todas"] + list(self.categorias_dict.keys())
        self.combo_filtro_categoria.set("Todas")
        self.combo_filtro_categoria.bind("<<ComboboxSelected>>", self.filtrar_por_categoria)

        labelframe = LabelFrame(frame2, text="Producto:", font="sans 22 bold", bg="#21c0d5")
        labelframe.place(x=20, y=30, width=400, height=500)

        lblnombre = Label(labelframe, text="Producto:", bg="#21c0d5", font="sans 14 bold")
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(labelframe, font="sans 14 bold")
        self.nombre.place(x=140, y=20, width=240, height=40)

        lblproveedor = Label(labelframe, text="Fabricante: ", bg="#21c0d5", font="sans 14 bold")
        lblproveedor.place(x=10, y=80)
        self.proveedor = ttk.Entry(labelframe, font="sans 14 bold")
        self.proveedor.place(x=140, y=80, width=240, height=40)

        lblprecio = Label(labelframe, text="Lote: ", bg="#21c0d5", font="sans 14 bold")
        lblprecio.place(x=10, y=140)
        self.precio = ttk.Entry(labelframe, font="sans 14 bold")
        self.precio.place(x=140, y=140, width=240, height=40)

        lblstock = Label(labelframe, text="Stock: ", bg= "#21c0d5", font="sans 14 bold")
        lblstock.place(x=10, y=200)
        self.stock= ttk.Entry (labelframe, font="sans 14 bold")
        self.stock.place (x=140 , y=200, width=240, height=40)
       
        # Obtener categorías desde la base de datos
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, categoria_nombre FROM tb_categorias")
        categorias = cursor.fetchall()
        conn.close()

        # Guardar diccionario y cargar combobox
        self.categorias_dict = {nombre: id_ for id_, nombre in categorias}
        self.combo_categoria = ttk.Combobox(labelframe, values=list(self.categorias_dict.keys()),
                                            font="sans 14", state="readonly")
        lblcategoria = Label(labelframe, text="Categoría: ", bg="#21c0d5", font="sans 14 bold")
        lblcategoria.place(x=10, y=260)

        self.combo_categoria.place(x=140, y=260, width=240, height=40)
        self.combo_categoria.set("Seleccionar")

        lblvencimiento = Label(labelframe, text="Vencimiento:", bg= "#21c0d5", font="sans 14 bold")
        lblvencimiento.place(x=10, y=320)
        self.vencimiento = ttk.Entry(labelframe, font="sans 14 bold")
        self.vencimiento.place(x=140, y=320, width=240, height=40)

        self.boton_agregar = tk.Button(labelframe, text="Ingresar", fg='white', bg="#007790",
                                   font="sans 12 bold", command=self.registrar)
        self.boton_agregar.place(x=110, y=390, width=180, height=40)

        # Desactivar si no es admin
        if self.rol_usuario != "admin":
            self.boton_agregar.config(state="disabled")
            #tabla de productos 

        treframe = Frame(frame2, bg="white")
        treframe.place(x=450, y=50, width=620, height=400)

        scrol_y = ttk.Scrollbar(treframe)
        scrol_y.pack(side=RIGHT, fill= Y)

        scrol_x = ttk.Scrollbar(treframe, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill= X)

        self.tre = ttk.Treeview(treframe, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, columns=("ID", "PRODUCTO", "PROVEEDOR", "PRECIO", "STOCK", "VENCIMIENTO", "CATEGORIA"), show="headings")      
        self.tre.pack(expand=True, fill= BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        self.tre.heading("ID", text= "ID")
        self.tre.heading("PRODUCTO", text= "Producto")
        self.tre.heading("PROVEEDOR", text= "Fabricante")
        self.tre.heading("PRECIO", text= "Lote")
        #self.tre.heading("COSTO", text= "Costo")
        self.tre.heading("STOCK", text= "Stock")
        self.tre.heading("VENCIMIENTO", text= "Vencimiento")
        self.tre.heading("CATEGORIA", text="Categoría")

        self.tre.column("ID", width=30, anchor= "center")
        self.tre.column("PRODUCTO", width=100, anchor= "center")
        self.tre.column("PROVEEDOR", width=100, anchor= "center")
        self.tre.column("PRECIO", width=100, anchor= "center")
        #self.tre.column("COSTO", width=100, anchor= "center")
        self.tre.column("STOCK", width=50, anchor= "center")
        self.tre.column("VENCIMIENTO", width=100, anchor="center")
        self.tre.column("CATEGORIA", width=120, anchor="center")

        self.mostrar()

        btn_actualizar = Button(frame2, text="Próximos a Vencer",fg='white', font= "sans 12 bold", bg= "#007790", command=self.proximo_vencer)
        btn_actualizar.place(x=890, y= 480, width=170 , height=40)

        self.boton_editar = tk.Button(frame2, text="Editar",fg='white', bg= "#007790", font="sans 12 bold", command=self.editar_producto)
        self.boton_editar.place(x=460,y=480, width=170, height=40)

        if self.rol_usuario != "admin":
            self.boton_editar.config(state="disabled")

        self.boton_eliminar = tk.Button(frame2, text="Eliminar ", bg="#ff4d4d", fg="white", font="sans 12 bold", command=self.eliminar_productos)
        self.boton_eliminar.place(x=675, y=480, width=170, height=40)

        if self.rol_usuario != "admin":
            self.boton_eliminar.config(state="disabled")


    def eje_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta, parametros)
            conn.commit()

        return result
        
    
    def eliminar_productos(self):
        seleccionados = self.tre.selection()
        if not seleccionados:
            messagebox.showwarning("Eliminar productos", "Seleccione uno o más productos para eliminar.")
            return

        nombres = [self.tre.item(item)["values"][1] for item in seleccionados]
        mensaje = "¿Está seguro de que desea eliminar los siguientes productos?\n\n" + "\n".join(nombres)

        confirmar = messagebox.askyesno("Confirmar eliminación", mensaje)
        if confirmar:
            try:
                for item in seleccionados:
                    item_id = self.tre.item(item)["values"][0]
                    consulta = "DELETE FROM inventario WHERE id = ?"
                    self.eje_consulta(consulta, (item_id,))
                self.actualizar_inventario()  # Refresca la tabla automáticamente
                messagebox.showinfo("Eliminación exitosa", "Los productos seleccionados fueron eliminados correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron eliminar los productos: {e}")

    def validacion(self, nombre, prov, precio, stock):
        if not nombre or not prov or not precio or not stock:
            messagebox.showwarning("Validación", "Rellene todos los campos.")
            return False
        try:
            
            int(stock)
        except ValueError:
            messagebox.showwarning("Validación", "Ingrese valores numéricos válidos para lote y stock.")
            return False
        return True
    
    def validar_fecha(self, fecha_str):
        try:
            # Verifica que la fecha esté en formato 'YYYY-MM-DD'
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def mostrar(self):
        self.tre.delete(*self.tre.get_children())  # Limpia la tabla
        consulta = """
                SELECT inventario.id, inventario.nombre, inventario.proveedor, inventario.precio,  
                    inventario.stock, inventario.fecha_vencimiento, tb_categorias.categoria_nombre
                FROM inventario
                LEFT JOIN tb_categorias ON inventario.categoria_id = tb_categorias.id
                ORDER BY inventario.nombre ASC
                """
        result = self.eje_consulta(consulta)

        for elem in result:
            id_ = elem[0]
            nombre = elem[1]
            proveedor = elem[2]
            costo = elem[3]
            stock = elem[4]
            vencimiento = elem[5]
            categoria = elem[6]

            self.tre.insert("", "end", values=(id_, nombre, proveedor, costo, stock, vencimiento, categoria))

    def proximo_vencer(self):
        
        hoy = datetime.now().date()
        proximos = []

        consulta = "SELECT * FROM inventario"
        result = self.eje_consulta(consulta)

        for elem in result:
            try:
                fecha_venc = datetime.strptime(elem[6], "%Y-%m-%d").date()
                dias_restantes = (fecha_venc - hoy).days

                if 0 <= dias_restantes <= 45:
                    lote = (elem[3])
                    proximos.append((elem[1], elem[2], lote, elem[6], dias_restantes))
            except Exception as e:
                print(f"Error al procesar fecha: {e}")

        if not proximos:
            messagebox.showinfo("Próximos a vencer", "No hay reactivos próximos a vencer en los próximos 45 días.")
            return

        # Crear ventana emergente
        popup = Toplevel(self)
        popup.title("Reactivos Próximos a Vencer")
        ruta = self.rutas(r"icono.ico")
        popup.iconbitmap(ruta)

        ancho_ventana = 750
        alto_ventana = 400

        # Obtener dimensiones de la pantalla
        ancho_pantalla = popup.winfo_screenwidth()
        alto_pantalla = popup.winfo_screenheight()

        # Calcular coordenadas para centrar
        x_centrado = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y_centrado = (alto_pantalla // 2) - (alto_ventana // 2)

        popup.geometry(f"{ancho_ventana}x{alto_ventana}+{x_centrado}+{y_centrado}")

        Label(popup, text="Reactivos que vencen en los próximos 45 días:", font=("Arial", 12, "bold")).pack(pady=5)

        tree = ttk.Treeview(popup, columns=("nombre", "cantidad", "presentacion", "vence", "dias"), show="headings")
        tree.heading("nombre", text="Nombre")
        tree.heading("cantidad", text="Cantidad")
        tree.heading("presentacion", text="lote")
        #tree.heading("ubicacion", text="Ubicación")
        tree.heading("vence", text="Fecha de Venc.")
        tree.heading("dias", text="Días Restantes")

        tree.column("nombre", width=180)
        tree.column("cantidad", width=70, anchor="center")
        tree.column("presentacion", width=100, anchor="center")
        #tree.column("ubicacion", width=100)
        tree.column("vence", width=100, anchor='center')
        tree.column("dias", width=100, anchor="center")

        tree.pack(expand=True, fill="both", padx=10, pady=10)

        tree.tag_configure("red", background="#ff9999")
        tree.tag_configure("yellow", background="#ffffcc")

        for elem in proximos:
            tag = "red" if elem[4] <= 30 else "yellow"
            tree.insert("", "end", values=elem, tags=(tag,))

    def actualizar_inventario(self):
        for item in self.tre.get_children():
            self.tre.delete(item)

        self.mostrar()
        
        messagebox.showinfo("Actualizacion", "El inventario se actualizó correctamente.")

    def registrar(self):
        nombre = self.nombre.get()
        prov = self.proveedor.get()
        precio = self.precio.get()
        costo = 0.0  # No estás pidiendo el costo en la interfaz
        stock = self.stock.get()
        vencimiento = self.vencimiento.get()
        categoria_nombre = self.combo_categoria.get()
        
        if not categoria_nombre or categoria_nombre == "Seleccionar":
            messagebox.showwarning("Validación", "Seleccione una categoría.")
            return
        
        categoria_id = self.categorias_dict.get(categoria_nombre)

        if self.validacion(nombre, prov, precio, stock):
            if not self.validar_fecha(vencimiento):
                messagebox.showwarning("Validación", "Ingrese una fecha válida con formato YYYY-MM-DD.")
                return
            try:
                consulta = "INSERT INTO inventario VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                parametros = (None, nombre, prov, precio, costo, stock, vencimiento, categoria_id)
                self.eje_consulta(consulta, parametros)
                self.actualizar_inventario()
                messagebox.showinfo("Registro", "Producto ingresado exitosamente.")
                self.nombre.delete(0, END)
                self.proveedor.delete(0, END)
                self.precio.delete(0, END)
                self.stock.delete(0, END)
                self.vencimiento.delete(0, END)
                self.combo_categoria.set("Seleccionar")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el producto: {e}")


    def editar_producto(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Editar producto", "Seleccione un producto para editar.")
            return

        item = self.tre.item(seleccion)
        item_id = item["values"][0]  # ID está en la primera columna
        item_values = item["values"]

        if len(item_values) < 7:
            messagebox.showerror("Error", f"El producto seleccionado no tiene todos los datos necesarios. Datos encontrados: {len(item_values)}")
            return

        ventana_editar = Toplevel(self)
        ventana_editar.title("Editar producto")
        ventana_editar.geometry("420x450")
        ventana_editar.config(bg="#21c0d5")
        try:
            ventana_editar.iconbitmap(self.rutas("icono.ico"))
        except:
            pass

        # Centrar ventana
        ventana_editar.update_idletasks()
        w = 420
        h = 450
        ws = ventana_editar.winfo_screenwidth()
        hs = ventana_editar.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        ventana_editar.geometry(f"{w}x{h}+{x}+{y}")

        # Reactivo
        lbl_nombre = Label(ventana_editar, text="Producto:", font="sans 14 bold", bg="#21c0d5")
        lbl_nombre.place(x=10, y=20)
        entry_nombre = Entry(ventana_editar, font="sans 14 bold")
        entry_nombre.place(x=140, y=20, width=240, height=30)
        entry_nombre.insert(0, item_values[1])  # nombre

        # Fabricante
        lbl_proveedor = Label(ventana_editar, text="Fabricante:", font="sans 14 bold", bg="#21c0d5")
        lbl_proveedor.place(x=10, y=70)
        entry_proveedor = Entry(ventana_editar, font="sans 14 bold")
        entry_proveedor.place(x=140, y=70, width=240, height=30)
        entry_proveedor.insert(0, item_values[2])  # proveedor

        # Lote
        lbl_lote = Label(ventana_editar, text="Lote:", font="sans 14 bold", bg="#21c0d5")
        lbl_lote.place(x=10, y=120)
        entry_lote = Entry(ventana_editar, font="sans 14 bold")
        entry_lote.place(x=140, y=120, width=240, height=30)
        entry_lote.insert(0, item_values[3])  # lote (antes precio)

        # Stock
        lbl_stock = Label(ventana_editar, text="Stock:", font="sans 14 bold", bg="#21c0d5")
        lbl_stock.place(x=10, y=170)
        entry_stock = Entry(ventana_editar, font="sans 14 bold")
        entry_stock.place(x=140, y=170, width=240, height=30)
        entry_stock.insert(0, item_values[4])  # stock

        # Vencimiento
        lbl_venc = Label(ventana_editar, text="Vencimiento:", font="sans 14 bold", bg="#21c0d5")
        lbl_venc.place(x=10, y=220)
        entry_venc = Entry(ventana_editar, font="sans 14 bold")
        entry_venc.place(x=140, y=220, width=240, height=30)
        entry_venc.insert(0, item_values[5])  # vencimiento

        # Categoría
        lbl_categoria = Label(ventana_editar, text="Categoría:", font="sans 14 bold", bg="#21c0d5")
        lbl_categoria.place(x=10, y=270)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, categoria_nombre FROM tb_categorias")
        categorias = cursor.fetchall()
        conn.close()

        categorias_dict = {nombre: id_ for id_, nombre in categorias}
        combo_categoria = ttk.Combobox(ventana_editar, values=list(categorias_dict.keys()),
                                    font="sans 14", state="readonly")
        combo_categoria.place(x=140, y=270, width=240, height=30)

        categoria_actual = item_values[6]
        if categoria_actual in categorias_dict:
            combo_categoria.set(categoria_actual)
        else:
            combo_categoria.set("Seleccionar")

        def guardar_cambios():
            nombre = entry_nombre.get()
            prov = entry_proveedor.get()
            lote = entry_lote.get()
            stock = entry_stock.get()
            vencimiento = entry_venc.get()
            categoria_nombre = combo_categoria.get()

            if not categoria_nombre or categoria_nombre == "Seleccionar":
                messagebox.showwarning("Validación", "Seleccione una categoría.")
                return

            categoria_id = categorias_dict.get(categoria_nombre)

            if self.validacion(nombre, prov, lote, stock):
                if not self.validar_fecha(vencimiento):
                    messagebox.showwarning("Validación", "Ingrese una fecha válida con formato YYYY-MM-DD.")
                    return
                try:
                    consulta = """
                        UPDATE inventario SET 
                            nombre = ?, 
                            proveedor = ?, 
                            precio = ?, 
                            stock = ?, 
                            fecha_vencimiento = ?, 
                            categoria_id = ?
                        WHERE id = ?
                    """
                    parametros = (nombre, prov, lote, stock, vencimiento, categoria_id, item_id)
                    self.eje_consulta(consulta, parametros)
                    self.actualizar_inventario()
                    messagebox.showinfo("Éxito", "Producto actualizado exitosamente.")
                    ventana_editar.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")

        btn_guardar = Button(ventana_editar, text="Guardar cambios", font="sans 14 bold",
                            bg="#007790", fg="white", command=guardar_cambios)
        btn_guardar.place(x=90, y=330, width=240, height=40)
  
    def rutas(self, ruta):
            try:
                rutabase=sys.__MEIPASS
            except Exception:
                rutabase = os.path.abspath(".")
            return os.path.join(rutabase,ruta)
    
    def agregar_categoria(self):
        ventana = tk.Toplevel(self)
        ventana.title("Agregar Categoría")
        ventana_width = 450
        ventana_height = 150

        # Obtener el tamaño de la pantalla
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()

        # Calcular coordenadas para centrar
        x = (screen_width // 2) - (ventana_width // 2)
        y = (screen_height // 2) - (ventana_height // 2)

        # Establecer geometría centrada
        ventana.geometry(f"{ventana_width}x{ventana_height}+{x}+{y}")
        ventana.config(bg="#21c0d5")

        try:
            ventana.iconbitmap(self.rutas("icono.ico"))
        except:
            pass  # Evita errores si no está el ícono

        # Etiqueta y entrada: Nombre de categoría
        lbl_nombre = tk.Label(ventana, text="Nombre de la categoría:", font="sans 12 bold", bg="#21c0d5")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_nombre = tk.Entry(ventana, font="sans 14")
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        # Etiqueta y entrada: Descripción (opcional)
        lbl_desc = tk.Label(ventana, text="Descripción:", font="sans 12 bold", bg="#21c0d5")
        lbl_desc.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_desc = tk.Entry(ventana, font="sans 14")
        entry_desc.grid(row=1, column=1, padx=10, pady=10)

        # Función para guardar en la base de datos
        def guardar_categoria():
            nombre = entry_nombre.get().strip()
            descripcion = entry_desc.get().strip()

            if not nombre:
                messagebox.showwarning("Campo obligatorio", "Debe ingresar un nombre para la categoría.")
                return

            try:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO tb_categorias (categoria_nombre, categoria_descripcion)
                    VALUES (?, ?)
                """, (nombre, descripcion if descripcion else None))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Categoría agregada correctamente.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la categoría.\n{str(e)}")

        # Botones
        btn_guardar = tk.Button(ventana, text="Guardar", command=guardar_categoria, font="sans 10")
        btn_guardar.grid(row=3, column=0, padx=10, pady=20)

        btn_cancelar = tk.Button(ventana, text="Cancelar", command=ventana.destroy, font="sans 10")
        btn_cancelar.grid(row=3, column=1, padx=10, pady=20)

    def filtrar_por_categoria(self, event=None):
        categoria = self.combo_filtro_categoria.get()
        self.tre.delete(*self.tre.get_children())

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        if categoria == "Todas":
            cursor.execute("""
                SELECT inventario.id, inventario.nombre, inventario.proveedor, inventario.precio,  
                    inventario.stock, inventario.fecha_vencimiento, tb_categorias.categoria_nombre
                FROM inventario
                LEFT JOIN tb_categorias ON inventario.categoria_id = tb_categorias.id
                ORDER BY inventario.nombre ASC
            """)
        else:
            categoria_id = self.categorias_dict[categoria]
            cursor.execute("""
                SELECT inventario.id, inventario.nombre, inventario.proveedor, inventario.precio,  
                    inventario.stock, inventario.fecha_vencimiento, tb_categorias.categoria_nombre
                FROM inventario
                LEFT JOIN tb_categorias ON inventario.categoria_id = tb_categorias.id
                WHERE inventario.categoria_id = ?
                ORDER BY inventario.nombre ASC
            """, (categoria_id,))

        for row in cursor.fetchall():
            self.tre.insert('', 'end', values=row)

        conn.close()
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os 
import sys 

class UserAdminWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Usuarios")
        self.resizable(False, False)
        self.centrar_ventana(500, 400)
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

        try:
            ruta = self.rutas("icono.ico")
            self.iconbitmap(ruta)
        except:
            pass

        self.tree = ttk.Treeview(self, columns=("Usuario", "Rol"), show="headings")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Rol", text="Rol")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        frame_form = tk.Frame(self)
        frame_form.pack(pady=5)

        tk.Label(frame_form, font =  'sans 12 bold', text="Usuario:").grid(row=0, column=0, sticky="e")
        self.entry_usuario = tk.Entry(frame_form, width=20)
        self.entry_usuario.grid(row=0, column=1)

        tk.Label(frame_form, font =  'sans 12 bold', text="Contraseña:").grid(row=1, column=0, sticky="e")
        self.entry_password = tk.Entry(frame_form, show="*", width=20)
        self.entry_password.grid(row=1, column=1)

        tk.Label(frame_form, font =  'sans 12 bold', text="Rol:").grid(row=2, column=0, sticky="e")
        self.combo_rol = ttk.Combobox(frame_form, values=["usuario", "admin"], state="readonly", width=16)
        self.combo_rol.grid(row=2, column=1)

        frame_buttons = tk.Frame(self)
        frame_buttons.pack(pady=5)

        tk.Button(frame_buttons, text="Agregar", command=self.agregar_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Modificar", command=self.modificar_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Eliminar", command=self.eliminar_usuario).pack(side=tk.LEFT, padx=5)

        self.tree.bind("<<TreeviewSelect>>", self.cargar_usuario)
        self.cargar_usuarios()

    def centrar_ventana(self, ancho, alto):
        self.update_idletasks()
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def rutas(self, ruta):
        try:
            rutabase = sys._MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    def cargar_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.cursor.execute("SELECT usuario, rol FROM tb_usuarios")
        for usuario, rol in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=(usuario, rol))

    def cargar_usuario(self, event):
        selected = self.tree.focus()
        if selected:
            valores = self.tree.item(selected)["values"]
            self.entry_usuario.delete(0, tk.END)
            self.entry_usuario.insert(0, valores[0])
            self.combo_rol.set(valores[1])
            self.entry_password.delete(0, tk.END)

    def agregar_usuario(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        rol = self.combo_rol.get()

        if not usuario or not password or not rol:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.",parent=self)
            return

        try:
            self.cursor.execute(
                "INSERT INTO tb_usuarios (usuario, clave, rol) VALUES (?, ?, ?)",
                (usuario, password, rol)
            )
            self.conn.commit()
            self.cargar_usuarios()
            messagebox.showinfo("Éxito", "Usuario agregado.", parent=self)

            self.limpiar_formulario()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe.",parent=self)

    def modificar_usuario(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        rol = self.combo_rol.get()

        if not usuario or not rol:
            messagebox.showwarning("Campos vacíos", "Selecciona un usuario y asigna un rol.",parent=self)
            return

        if password:
            self.cursor.execute(
                "UPDATE tb_usuarios SET clave=?, rol=? WHERE usuario=?",
                (password, rol, usuario)
            )
        else:
            self.cursor.execute(
                "UPDATE tb_usuarios SET rol=? WHERE usuario=?",
                (rol, usuario)
            )

        self.conn.commit()
        self.cargar_usuarios()
        messagebox.showinfo("Actualizado", "Usuario modificado.",parent=self)
        self.limpiar_formulario()

    def eliminar_usuario(self):
        usuario = self.entry_usuario.get().strip()
        if not usuario:
            messagebox.showwarning("Selección faltante", "Selecciona un usuario para eliminar.",parent=self)
            return

        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar usuario '{usuario}'?")
        if confirm:
            self.cursor.execute("DELETE FROM tb_usuarios WHERE usuario=?", (usuario,))
            self.conn.commit()
            self.cargar_usuarios()
            messagebox.showinfo("Eliminado", "Usuario eliminado.",parent=self)
            self.limpiar_formulario()

    def limpiar_formulario(self):
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.combo_rol.set("")

    def destroy(self):
        if self.conn:
            self.conn.close()
        super().destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana raíz para que no salga vacía
    ventana = UserAdminWindow(root)
    ventana.mainloop()
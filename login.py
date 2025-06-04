import tkinter as tk
from tkinter import messagebox
import sqlite3
import sys
import os

class Login(tk.Toplevel):
    def __init__(self, master, on_success):
        super().__init__(master)
        
        self.title("Inicio de Sesión")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.confirmar_salida)
        self.transient(master)
        self.grab_set()
        self.on_success = on_success

        try:
            ruta_icono = self.rutas("icono.ico")
            self.iconbitmap(ruta_icono)
        except:
            pass

        # Centrar ventana
        ancho = 300
        alto = 180
        self.update_idletasks()
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.configure(bg='#f0f0f0')

        self.usuario_var = tk.StringVar()
        self.clave_var = tk.StringVar()

        # Frame principal
        frame = tk.Frame(self, bg="#e0e0e0", bd=2, relief="groove")
        frame.place(x=0, y=0, width=300, height=180)

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#e0e0e0").place(x=20, y=20)
        self.usuario_entry = tk.Entry(frame, textvariable=self.usuario_var, font=("Arial", 12))
        self.usuario_entry.place(x=100, y=20, width=170)

        tk.Label(frame, text="Clave:", font=("Arial", 12), bg="#e0e0e0").place(x=20, y=60)
        self.clave_entry = tk.Entry(frame, textvariable=self.clave_var, font=("Arial", 12), show="*")
        self.clave_entry.place(x=100, y=60, width=170)

        tk.Button(frame, text="Entrar", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                  command=self.validar_login).place(x=100, y=110, width=100, height=30)

        # Enfocar automáticamente la entrada de usuario al abrir
        self.after(200, lambda: self.usuario_entry.focus())

        self.bind('<Return>', lambda event: self.validar_login())

    def confirmar_salida(self):
        if messagebox.askyesno("Salir", "¿Deseas cerrar el programa?"):
            self.master.destroy()

    def rutas(self, ruta):
        try:
            rutabase = sys._MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    def validar_login(self):
        usuario = self.usuario_var.get().strip()
        clave = self.clave_var.get().strip()

        if not usuario or not clave:
            messagebox.showwarning("Campos vacíos", "Por favor ingrese usuario y clave.")
            return

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT rol FROM tb_usuarios WHERE usuario=? AND clave=?", (usuario, clave))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            rol = resultado[0]
            self.destroy()
            self.on_success(usuario, rol)
        else:
            messagebox.showerror("Error", "Usuario o clave incorrectos")

# Test local
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    def dummy(usuario, rol):
        print(f"Sesión iniciada: {usuario} ({rol})")

    Login(root, dummy)
    root.mainloop()
from tkinter import Tk, Frame  
from container import Container
from ttkthemes import ThemedStyle
import sys
import os
from login import Login
from tkinter import messagebox
from admin import UserAdminWindow


class Manager(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('SIGE')
        self.resizable(False, False)
        self.configure(bg='#9db2b8')
        self.usuario_actual = None
        self.rol_actual = None

        # Centrar ventana
        ancho = 800
        alto = 400
        self.update_idletasks()
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        try:
            ruta = self.rutas(r"icono.ico")
            self.iconbitmap(ruta)
        except:
            pass

        self.container = Frame(self, bg='#FBECEC')
        self.container.pack(fill='both', expand=True)

        self.frames = {
            Container: None
        }
        self.load_frame()
        self.set_theme()


    def rutas(self, ruta):
        try:
            rutabase = sys._MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    def load_frame(self):
        for FrameClass in self.frames.keys():
            frame = FrameClass(self.container, self)
            self.frames[FrameClass] = frame

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def set_theme(self):
        style = ThemedStyle(self)
        style.set_theme("breeze")

    def mostrar_login(self):
        def on_login_exitoso(usuario, rol):
            self.usuario_actual = usuario
            self.rol_actual = rol
            self.title(f"SIGE - Sesión de {usuario} ({rol})")
            self.habilitar_funciones_por_rol()

        Login(self, on_login_exitoso)

    def habilitar_funciones_por_rol(self):
        if self.rol_actual == "admin":
            print("Habilitando funciones de administrador...")
            self.frames[Container].btn_admin_usuarios.config(state="normal")  # Habilita el botón
        else:
            print("Modo usuario restringido.")
            self.frames[Container].btn_admin_usuarios.config(state="disabled") 
    def abrir_gestion_usuarios(self):
        UserAdminWindow(self, es_admin=(self.rol_actual == "admin"))
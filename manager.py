from tkinter import Tk, Frame
from container import Container
from ttkthemes import ThemedStyle
import sys
import os

class Manager (Tk):
    def __init__ (self, *args, **kwargs):
        super().__init__ (*args, **kwargs)
        self.title ('LogiSales') # titulo
        self.resizable(False,False) # No maximizar 
        self.configure(bg='#9db2b8') #Color de fondo 
        self.geometry('800x400+120+20')  # Posicion de la ventana y tamaño 
        ruta = self.rutas (r"icono.ico")
        self.iconbitmap(ruta)

        self.container = Frame (self, bg='#FBECEC')
        self.container.pack (fill='both', expand=True)

        self.frames = {
            Container: None
        }
        self.load_frame()
        self.show_frame(Container)
        self.set_theme()
        
    def rutas(self, ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase,ruta)

    def load_frame(self):
        for FrameClass in self.frames.keys():
            frame = FrameClass(self.container, self)
            self.frames [FrameClass] = frame

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def set_theme(self):
        style = ThemedStyle(self)
        style.set_theme("breeze")


def main():
    app = Manager()
    app.mainloop()

if __name__ == "__main__":
    main()
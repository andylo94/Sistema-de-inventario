from tkinter import Tk, Frame
from container import Container

class Manager (Tk):
    def __init__ (self, *args, **kwargs):
        super().__init__ (*args, **kwargs)
        self.title ('Von Makeup') # titulo
        self.resizable(False,False) # No maximizar 
        self.configure(bg='#FBECEC') #Color de fondo 
        self.geometry('800x400+120+20')  # Posicion de la ventana y tamaño 

        self.container = Frame (self, bg='#FBECEC')
        self.container.pack (fill='both', expand=True)

        self.frames = {
            Container: None
        }
        self.load_frame()
        self.show_frame(Container)

    def load_frame(self):
        for FrameClass in self.frames.keys():
            frame = FrameClass(self.container, self)
            self.frames [FrameClass] = frame

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
def main():
    app = Manager()
    app.mainloop()

if __name__ == "__main__":
    main()
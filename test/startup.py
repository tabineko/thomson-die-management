import tkinter as tk
import os
from PIL import Image, ImageTk


class FrameBase(tk.Tk):
    def __init__(self, photo_dir_path='./data/photo', ext='jpg'):
        self.rfid = None
        self.photo_dir_path = photo_dir_path
        self.ext = ext
        self.photo_path = ''
        self.width = 1600
        self.height = 900
        
        tk.Tk.__init__(self)
        self.geometry("1600x900")
        # self.frame = StartPageFrame(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame = RFIDConfirmFrame(self, width=self.width, height=self.height)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # make sure that the directory exist
        if not os.path.exists(self.photo_dir_path):
            os.makedirs(self.photo_dir_path)

    def change(self, frame):
        # self.frame.destroy()
        self.frame = frame(master=self, width=self.width, height=self.height)
        self.frame.grid(row=0, column=0, sticky="nsew")
        # self.frame.pack(expand=True, fill="both") # make new frame

    def backToStart(self):
        # self.frame.destroy()
        self.frame = StartPageFrame(self, width=self.width, height=self.height)
        self.frame.grid(row=0, column=0, sticky="nsew")
        # self.frame.pack(expand=True, fill="both")


class StartPageFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        # master.title('Home')

        btn = tk.Button(master=self, text='Read RFID', width=5,
                        command=lambda: self.master.change(RFIDConfirmFrame))
        btn.grid(row=0, column=0)


class RFIDConfirmFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        # master.title('RFID Confirmation')

        # RFID読み込み
        self.master.rfid = 'rfid'

        self.master.photo_path = os.path.join(self.master.photo_dir_path,
                                              '{}.{}'.format(self.master.rfid,
                                                             self.master.ext))

        lbl = tk.Label(self, text='rfid: {}'.format(self.master.rfid),
                       height=5, font=("Migu 1M",20))
        lbl.grid(row=0, column=0, columnspan=2)

        btn = tk.Button(master=self, text='Cancel', width=5,
                        command=lambda: self.master.backToStart())
        btn.grid(row=1, column=0)
        btn = tk.Button(master=self, text='Continue', width=5,
                        command=lambda: self.fileconfirm())
        btn.grid(row=1, column=1)
    
    def fileconfirm(self):
        print(os.getcwd())
        print(self.master.photo_path)

        if os.path.isfile(self.master.photo_path):
            self.master.change(FileExist)
        else:
            self.master.change(FileNotExist)


class FileExist(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # https://daeudaeu.com/create_image_problem/
        self.img = Image.open(self.master.photo_path)
        self.img = self.img.resize((600, 360))
        self.img = ImageTk.PhotoImage(self.img)

        canvas = tk.Canvas(master=self, bg='black', width=600, height=360)
        canvas.grid(row=0, column=0, columnspan=2)
        canvas.create_image(300, 180, image=self.img)

        btn = tk.Button(master=self, text='Cancel', width=5,
                        command=lambda: self.master.backToStart())
        btn.grid(row=1, column=0)
        # btn.pack(fill='x', padx=20, side='left')
        btn = tk.Button(master=self, text='Recapture', width=5,
                        command=lambda: self.master.change(Cammera))
        btn.grid(row=1, column=1)
        # btn.pack(fill='x', padx=20, side='left')

    def say_hello(self):
        print('hello')


class FileNotExist(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        lbl = tk.Label(self, text='Cannot find the photo.',
                       height=5, font=("Migu 1M",20))
        lbl.pack()

        btn = tk.Button(master=self, text='Home', width=5,
                        command=lambda: self.master.backToStart())
        btn.pack(fill='x', padx=20, side='left')
        btn = tk.Button(master=self, text='Activate Camera', width=5,
                        command=lambda: self.master.change())
        btn.pack(fill='x', padx=20, side='left')

    def say_hello(self):
        print('hello, world!')

    # class Cammera(tk.Frame):


if __name__ == "__main__":
    root = FrameBase()
    root.mainloop()

import tkinter as tk
import os
from PIL import Image, ImageTk
import tkinter.filedialog as tkdialog
import cv2
from rfidreader import RfidReader as rr


class FrameBase(tk.Tk):
    def __init__(self, photo_dir_path='./data/photo', ext='jpg'):
        self.rfid = None
        self.photo_dir_path = os.path.abspath(photo_dir_path)
        self.ext = ext
        self.photo_path = ''
        self.width = 600
        self.height = 500

        tk.Tk.__init__(self)
        self.geometry("600x500")
        self.frame = StartPageFrame(self)
        # self.frame = RFIDConfirmFrame(self, width=self.width, height=self.height)
        self.frame.pack(anchor=tk.CENTER)

        # make sure that the directory exist
        if not os.path.exists(self.photo_dir_path):
            os.makedirs(self.photo_dir_path)

    def change(self, frame):
        self.frame.pack_forget()
        self.frame = frame(master=self, width=self.width, height=self.height)
        self.frame.pack(anchor=tk.CENTER)
        # self.frame.pack(expand=True, fill="both") # make new frame

    def back_to_start(self):
        self.frame.pack_forget()
        self.frame = StartPageFrame(self, width=self.width, height=self.height)
        self.frame.pack(anchor=tk.CENTER)
        # self.frame.pack(expand=True, fill="both")

    def exit_application(self):
        self.destroy()


class StartPageFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        # master.title('Home')

        lbl = tk.Label(self, text='Photo Capture',
                       height=5, font=("Migu 1M",20))
        lbl.grid(row=0, column=0, columnspan=2)

        btn = tk.Button(master=self, text='Quit', width=10,
                        command=lambda: self.master.quit())
        btn.grid(row=1, column=0)

        btn = tk.Button(master=self, text='Read RFID', width=10,
                        command=lambda: self.master.change(RFIDConfirmFrame))
        btn.grid(row=1, column=1)


class RFIDConfirmFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        # master.title('RFID Confirmation')

        # RFID読み込み
        reader = rr()
        # delete CR and save rfid
        self.master.rfid = reader.read_rfid().replace('\r', '')

        print('---------------')
        print((self.master.rfid))
        print(self.master.photo_dir_path)
        print('{}.{}'.format(self.master.rfid, self.master.ext))
        print(self.master.rfid + '.' + self.master.ext)

        self.master.photo_path = os.path.join(self.master.photo_dir_path,
                                              '{}.{}'.format(self.master.rfid,
                                                             self.master.ext))

        print(self.master.photo_path)
        print('---------------')

        lbl = tk.Label(self, text='rfid: {}'.format(self.master.rfid),
                       height=5, font=("Migu 1M",20))
        lbl.grid(row=0, column=0, columnspan=2)

        btn = tk.Button(master=self, text='Cancel', width=15,
                        command=lambda: self.master.back_to_start())
        btn.grid(row=1, column=0)
        btn = tk.Button(master=self, text='Continue', width=15,
                        command=lambda: self.fileconfirm())
        btn.grid(row=1, column=1)

    def fileconfirm(self):
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

        btn = tk.Button(master=self, text='Cancel', width=15,
                        command=lambda: self.master.back_to_start())
        btn.grid(row=1, column=0)
        btn = tk.Button(master=self, text='Recapture', width=15,
                        command=lambda: self.master.change(Cammera))
        btn.grid(row=1, column=1)

    def say_hello(self):
        print('hello')


class FileNotExist(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        lbl = tk.Label(self, text='Cannot find the photo.',
                       height=5, font=("Migu 1M", 20))
        lbl.pack()

        btn = tk.Button(master=self, text='Home', width=15,
                        command=lambda: self.master.backToStart())
        btn.pack(fill='x', padx=20, side='left')
        btn = tk.Button(master=self, text='Activate Camera', width=15,
                        command=lambda: self.master.change(Cammera))
        btn.pack(fill='x', padx=20, side='left')


class Cammera(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        self.canvas = tk.Canvas(master=self, bg='black', width=600, height=360)
        self.canvas.grid(row=0, column=0, columnspan=3)
        # self.canvas.create_image(300, 180, image=self.img)

        btn = tk.Button(master=self, text='Back', width=15,
                        command=lambda: self.master.change(RFIDConfirmFrame))
        btn.grid(row=1, column=0)
        btn = tk.Button(master=self, text='Capture', width=15,
                        command=lambda: self.save_current_frame())
        btn.grid(row=1, column=1)

        self.stream_img()

    def stream_img(self):
        ret, self.frame = self.cap.read()
        if ret:
            self.tk_frame = cv2.resize(self.frame, (600, 360))
            self.tk_frame = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self.tk_frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(300, 180, image=self.tk_frame)
        else:
            self.canvas.create_text(300, 180, text='None')
        
        self.after(30, self.stream_img)

    def save_current_frame(self):
        print(self.master.photo_path)
        cv2.imwrite(self.master.photo_path, self.frame)
        print('here!')
        self.cap.release()
        # cv2.destroyAllWindows()
        self.master.change(CheckCapturedPhoto)


class CheckCapturedPhoto(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        print(self.master.photo_path)
        img = Image.open(self.master.photo_path)
        img = img.resize((600, 360))
        img = ImageTk.PhotoImage(img)

        self.canvas = tk.Canvas(master=self, bg='black', width=600, height=360)
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.canvas.create_image(300, 180, image=img)

        btn = tk.Button(master=self, text='Recapture', width=15,
                        command=lambda: self.master.change(Cammera))
        btn.grid(row=1, column=0)
        btn = tk.Button(master=self, text='Save', width=15,
                        command=lambda: self.master.change(QuitorAgain))
        btn.grid(row=1, column=1)


# seems doesn't needed
class SelectOutputFile(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        cwd = os.path.dirname(__file__)
        prev_path_holder = os.path.join(cwd, '.path_holder.txt')
            
        with open(prev_path_holder, 'r') as f:
            self.iDir = f.readline().strip()
            
        if not os.path.isfile(self.iDir):
            self.iDir = os.path.abspath(os.path.dirname(__file__))

        lbl = tk.Label(self, text='filename: ')
        lbl.pack(side='left')

        filenameEntry = tk.Entry(self, text="", textvariable= self.iDir)
        filenameEntry.pack(side='left')

        btn = tk.Button(master=self, text='Browse', width=15,
                        command=lambda: self.file_open())
        btn.pack(side='left')
            
    def file_open(self):
        accepting_file_types = [('All Excel Files', '.xl* .xlsx .xlsm .xlsb .xlam .xltx .xltm .xls .xlt .htm .html .mht .mhtml .xml .xla .xlm .xlw .xjs .xjm .xjc .xjw .xja .xjt .odc .uxdc .ods')]
        title_dialog = 'Select file to write'
            
        self.ret = tkdialog.askopenfilename(accepting_file_types,
                                            self.iDir, title_dialog, multiple=False)

    def save_rfid(self):
        pass


class QuitorAgain(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        lbl = tk.Label(self, text='Done.',
                       height=5, font=("Migu 1M", 20))
        lbl.grid(row=0, column=0, columnspan=2)

        btn = tk.Button(master=self, text='Quit', width=15,
                        command=lambda: self.master.quit())
        btn.grid(row=1, column=0)
        btn = tk.Button(master=self, text='Again.', width=15,
                        command=lambda: self.master.back_to_start())
        btn.grid(row=1, column=1)


def main():
    root = FrameBase()
    root.mainloop()


if __name__ == "__main__":
    main()

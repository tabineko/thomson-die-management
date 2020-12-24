import tkinter as tk


class FrameBase(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("800x480")
        self.frame = StartPageFrame(self)
        self.frame.pack(expand=True, fill="both")
        #self.attributes("-fullscreen", True)

    def change(self, frame):
        # self.frame.destroy()  # delete currrent frame
        self.destroy()
        self.frame = frame(self)
        self.frame.pack(expand=True, fill="both") # make new frame

    def backToStart(self):
        self.destroy()
        self.frame = StartPageFrame(self)
        self.frame.pack(expand=True, fill="both")


class StartPageFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        # master.title('Home')

        btn = tk.Button(master=self, text='Read RFID', width=5,
                        command=self.master.change(RFIDConfirmFrame))
        btn.pack(anchor=tk.NW)


class RFIDConfirmFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        # master.title('RFID Confirmation')

        # RFID読み込み
        RFID = 'rfid'

        lbl = tk.Label(self, text='rfid: {}'.format(RFID),
                       height=5, font=("Migu 1M",20))
        lbl.pack()

        btn = tk.Button(master=self, text='Cancel', width=5,
                        command=self.master.backToStart)
        btn.pack(fill='x', padx=20, side='left')
        btn = tk.Button(master=self, text='Continue', width=5,
                        command=self.master.backToStart)
        btn.pack(fill='x', padx=20, side='left')


if __name__ == "__main__":
    root = FrameBase()
    root.mainloop()

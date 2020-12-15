import tkinter as tk
import rfidreader as rfid
import capturephoto as cp

rfid_number = 0
path = ''

# ｳｨﾝﾄﾞｳ作成
root = tk.Tk()
root.geometry("500x300")
'''
def im_botton():
    print("画像処理のプログラムを起動")
'''
def rfid_botton():
    print("RFIDリーダの取得")
    rfid.main()
    rfidreader = rfid.RfidReader()
    global rfid_number
    rfid_number = rfidreader.get_rfid()

def cam_botton():
    print('カメラの起動')
    cam = cp.CameraApp(device_num=1)
    global path
    cam.save_frame_camera_key('data/temp', str(rfid_number))
    cam.show_img()

def 

# ﾀｲﾄﾙ表示
root.title("tkinterでGUI作成")
'''
# ﾗﾍﾞﾙ作成
label = tk.Label(text="Hello")
label.pack()
'''
if __name__ == '__main__':
    '''
    button = tk.Button(text = "Image Processing", command=im_botton)
    button.place(x = 100, y = 100)
    '''
    # button = tk.Button(text = "--RFID--", command=rfid_botton)
    button = tk.Button(text = "--CAMERA--", command=cam_botton)
    button.place(x = 200, y = 100)
    


    root.mainloop()
import serial
import time


def select_port():
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.timeout = 0.1

    ports = serial.tools.list_ports.comports()

    devices = [info.device for info in ports]

    if len(devices) == 0:
        # シリアル通信できるデバイスが見つからなかった場合
        print("error: device not found")
        return None
    elif len(devices) == 1:
        print("only found %s" % devices[0])
        ser.port = devices[0]
    else:
        # ポートが複数見つかった場合それらを表示し選択させる
        for i in range(len(devices)):
            print("input %3d: open %s" % (i,devices[i]))
        print("input number of target port >> ",end="")
        num = int(input())
        ser.port = devices[num]
    try:
        ser.open()
        return ser
    except:
        print("error when opening serial")
        return None


def main():
    ser = select_port()
    
    if ser is None:
        return
    
    while ser.is_open:
        data = ser.read(256)
        if data != b'':
            print(data.decode(),end="")
        time.sleep(1)

    ser.close()
import sys
import serial
import time
import os


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


class RfidReader():
    def __init__(self):
        self.start_byte = 0x0A
        self.stop_byte = 0x0D
        self.cmd_read = 0x01
        self.addr_serial = 32
        self.port = '//./COM3'
        self.rfid = None

    def read_rfid(self, timeout=1):
        ser = serial.Serial(self.port, 2400, timeout=timeout)
        sys.stdout = Unbuffered(sys.stdout)

        while True:
            ser.write(('!RW' + chr(self.cmd_read) + chr(self.addr_serial)).encode())
            buf = ser.read(12).decode('UTF-8')
            if len(buf) != 0:
                if buf[0] == chr(self.start_byte) and buf[-1] == chr(self.stop_byte):
                    self.rfid = buf[1:]
                    break
            time.sleep(1)

        ser.close()
        return self.rfid

    def get_rfid(self):
        return self.rfid

    def search_img(self, photo_dir='../data/photo', extention='jpg'):
        base_path = os.path.join(photo_dir, str(self.rfid))
        return os.path.isfile('{}.{}'.format(base_path, extention))


def main():
    reader = RfidReader()
    rfid = reader.read_rfid()
    # rfid = reader.get_rfid()
    print(rfid)


if __name__ == '__main__':
    main()

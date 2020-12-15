import cv2
import os


class CameraApp():
    def __init__(self, device_num=0, format_mjpg=True, width_photo=1920, height_photo=1080, fps=30):
        self.device_num = device_num
        
        if format_mjpg is True:
            self.video_writer_fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        else:
            self.video_writer_fourcc = cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V')
        
        self.width_photo = width_photo
        self.height_photo = height_photo
        self.fps = fps



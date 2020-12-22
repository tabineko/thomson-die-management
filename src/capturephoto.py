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
        self.path_photo = None

    def save_frame_camera_key(self, dir_path, rfid, ext='jpg', delay=1, window_name='frame'):
        cap = cv2.VideoCapture(self.device_num)
        cap.set(cv2.CAP_PROP_FOURCC, self.video_writer_fourcc)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width_photo)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height_photo)
        cap.set(cv2.CAP_PROP_FPS, self.fps)

        os.makedirs(dir_path, exist_ok=True)
        base_path = os.path.join(dir_path, rfid)

        while True:
            ret, frame = cap.read()
            cv2.imshow(window_name, frame)
            key = cv2.waitKey(delay) & 0xFF
            if key == ord('c'):
                cv2.imwrite('{}.{}'.format(base_path, ext), frame)
                self.path = '{}.{}'.format(base_path, ext)
                break

            elif key == ord('q'):
                break

        cv2.destroyWindow(window_name)

    def show_img(self):
        img = cv2.imread(self.path_photo, 1)
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    cam = CameraApp(device_num=1)
    path = cam.save_frame_camera_key('data/photo', 'rfid')
    print(path)
    cam.show_img(path)
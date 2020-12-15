import cv2
import os

def save_frame_camera_key(device_num, dir_path, rfid, ext='jpg', delay=1, window_name='frame'):
    WIDTH = 1920
    HEIGHT = 1080
    FPS = 30
    cap = cv2.VideoCapture(device_num)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, rfid)

    while True:
        ret, frame = cap.read()
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('c'):
            cv2.imwrite('{}.{}'.format(base_path, ext), frame)
            return '{}.{}'.format(base_path, ext)
        elif key == ord('q'):
            break

    cv2.destroyWindow(window_name)


ret = save_frame_camera_key(1, 'data/temp', 'aaaaa')
print(ret)
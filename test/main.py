from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty
import os


DEVICE_ID = 0
WIDTH = 1920
HEIGHT = 1080
FPS = 30


class ImageButton(ButtonBehavior, Image):
    preview = ObjectProperty(None)

    def on_press(self):
        cv2.namedWindow("CV2 Image")
        cv2.imshow("CV2 Image", self.preview.frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class CameraPreview(Image):
    def __init__(self, **kwargs):
        super(CameraPreview, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.update, 1.0 / 30)

    def update(self, dt):
        ret, self.frame = self.capture.read()
        buf = cv2.flip(self.frame, 0).tostring()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr') 
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture


class MainScreen(Widget):
    pass


class MyCameraApp(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    # cap = cv2.VideoCapture(DEVICE_ID)
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    # # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    # cap.set(cv2.CAP_PROP_FPS, FPS)

    print(os.path.exists('./icons/capture.jpgs'))
    MyCameraApp().run()
# for invisibility
from objectDetection import *
import time
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture


class InvisiblityCloak(App):
    def build(self):
        # Layout of the App
        self.layout = BoxLayout(orientation='vertical')
        # Buttons
        self.saveButton = Button(text='Save Image',
                                 size=(200, 50), size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.saveButton.bind(on_press=self.save_image)
        self.invisbleButton = Button(text='Become Visible',
                                     size=(200, 50), size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.invisbleButton.bind(on_press=self.toggleVisibility)
        self.videoCapture = cv2.VideoCapture(0)
        # Image
        self.image = Image()
        # Adding Widgets to Layout
        self.layout.add_widget(self.image)
        self.layout.add_widget(self.saveButton)
        self.layout.add_widget(self.invisbleButton)
        self.visbile = True
        # Every 1/30th of a Second self.Image will be re-rendered
        Clock.schedule_interval(self.load_video, 1/30)
        return self.layout

    def on_stop(self):
        # releasing the VideoCapture on closing the app
        self.videoCapture.release()

    def load_video(self, *args):
        # using the function getFrame() form objectDetection module to get a frame
        success, self.frame = getFrame(self.videoCapture, self.visbile)
        if success:
            # convert the numpy array return by VideoCapture(0).read() function to
            # Kivy Image Texture
            buffer = cv2.flip(self.frame, 0).tobytes()
            image_texture = Texture.create(
                size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(
                buffer, colorfmt='bgr', bufferfmt='ubyte')
            # setting the texture of the Image Object as the obtained texture which created by converting
            # the 'self.frame' returned by VideoCapture(0).read()
            self.image.texture = image_texture

    def save_image(self, *args):
        cv2.imwrite(str(time.time())+".png", self.frame)

    def toggleVisibility(self, *args):
        if self.visbile == True:
            self.visbile = False
            self.invisbleButton.text = "Become Invisible"
        else:
            self.visbile = True
            self.invisbleButton.text = "Become Visible"


if __name__ == '__main__':
    InvisiblityCloak().run()

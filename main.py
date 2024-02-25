# Import necessary libraries
import os
import cv2
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from facerecognition import SimpleFacerec  # Assuming this is a custom face recognition module
from plyer import filechooser  # Plyer is a Python library for platform-independent access to features commonly found on mobile devices

# Define a Kivy widget for camera display
class KivyCamera(Image):
    """KivyCamera is a class for managing the camera and performing face recognition."""

    def __init__(self, capture, fps, sfr, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture  # OpenCV capture object
        self.sfr = sfr  # Face recognition object
        self.recognize = False  # Flag to control face recognition
        Clock.schedule_interval(self.update, 1.0 / fps)  # Schedule the update function at the specified frames per second

    def update(self, dt):
        ret, frame = self.capture.read()  # Read a frame from the camera
        if ret:
            if self.recognize:
                # Detect Faces using the SimpleFacerec object
                face_locations, face_names = self.sfr.detect_known_faces(frame)
                for face_loc, name in zip(face_locations, face_names):
                    y2, x2, y1, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]  # Extract face coordinates
                    if name == "Unknown":
                        # Draw rectangle and text for unknown faces
                        cv2.putText(frame, name, (x1, y1 + 25), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 200), 2)
                        cv2.rectangle(frame, (x1, y2), (x2, y1), (0, 0, 200), 3)
                    else:
                        # Draw rectangle and text for known faces
                        cv2.putText(frame, name, (x1, y1 + 25), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 128, 0), 2)
                        cv2.rectangle(frame, (x1, y2), (x2, y1), (0, 128, 0), 3)
            buf1 = cv2.flip(frame, 0)  # Flip the frame vertically
            buf = buf1.tostring()  # Convert the frame to a string buffer
            # Create a Kivy texture and update the widget with the camera frame
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture

# Define the main application class
class TestApp(App):
    """TestApp is the main application class."""

    def build(self):
        """Build the Kivy interface."""
        self.capture = cv2.VideoCapture(0)  # Initialize the OpenCV camera capture object
        self.sfr = SimpleFacerec()  # Initialize the face recognition object
        self.sfr.load_encoding_images("images/")  # Load pre-encoded images for recognition
        self.my_camera = KivyCamera(capture=self.capture, fps=30, sfr=self.sfr)  # Create the camera widget

        # Create buttons for controlling face recognition
        self.start_button = Button(text="Start Recognition", size_hint_y=None, height=50)
        self.start_button.bind(on_press=self.start_recognition)

        self.stop_button = Button(text="Stop Recognition", size_hint_y=None, height=50)
        self.stop_button.bind(on_press=self.stop_recognition)

        # Create a button for adding new images to the face recognition system
        self.add_image_button = Button(text="Add Image", size_hint_y=None, height=50)
        self.add_image_button.bind(on_press=self.add_image)

        # Create the layout and add widgets
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.my_camera)
        layout.add_widget(self.start_button)
        layout.add_widget(self.stop_button)
        layout.add_widget(self.add_image_button)

        return layout

    def start_recognition(self, instance):
        """Start face recognition."""
        self.my_camera.recognize = True

    def stop_recognition(self, instance):
        """Stop face recognition."""
        self.my_camera.recognize = False

    def add_image(self, instance):
        """Open a file chooser to select an image to add."""
        filters = [("Image Files", "*.png", "*.jpg" ,"*.jpeg")]
        file_paths = filechooser.open_file(title="Select an image", filters=filters)
        if file_paths:
            self.select_image(None, file_paths[0])

    def select_image(self, instance, value, *args):
        """Add the selected image to the face recognition system."""
        selected_path = value
        if os.path.isfile(selected_path):
            image_filename = os.path.basename(selected_path)
            script_dir = os.path.dirname(os.path.realpath(__file__))
            destination_dir = os.path.join(script_dir, "images")
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            destination_path = os.path.join(destination_dir, image_filename)
            with open(selected_path, 'rb') as source_file, open(destination_path, 'wb') as dest_file:
                dest_file.write(source_file.read())
            self.sfr.load_encoding_images(destination_dir)

    def on_stop(self):
        """Release the camera when the application stops."""
        self.capture.release()

# Run the Kivy application
if __name__ == '__main__':
    TestApp().run()

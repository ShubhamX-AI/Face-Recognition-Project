import cv2
import face_recognition
import glob
import numpy as np
import os

class SimpleFacerec:
    def __init__(self):
        # Initialize known face encodings and names
        self.known_face_encodings = []
        self.known_face_names = []
        # Initialize frame resizing factor for faster processing
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path and store their encodings and names.
        :param images_path: Path to the encoding images
        """
        # Get all image paths
        images_path = glob.glob(os.path.join(images_path, "*.*"))
        print(f"{len(images_path)} encoding images found.")

        for img_path in images_path:
            # Read image and convert color space from BGR to RGB
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Extract filename from path
            filename = os.path.splitext(os.path.basename(img_path))[0]
            # Compute face encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Store encoding and filename
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)

        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        """
        Detect known faces in the given frame.
        :param frame: Frame to detect faces in
        :return: Locations and names of detected faces
        """
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Convert color space from BGR to RGB
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect face locations and encodings in the frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Compare face with known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        # Adjust face locations according to frame resizing
        face_locations = (np.array(face_locations) / self.frame_resizing).astype(int)
        return face_locations, face_names

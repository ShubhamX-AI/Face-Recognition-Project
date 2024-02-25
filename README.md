# Face Recognition Application

## Overview

This project is a real-time face recognition application built using Python, OpenCV, Kivy, and a custom face recognition module. It allows users to detect and identify faces in real-time using a webcam. The application provides a user-friendly interface for starting and stopping face recognition, as well as adding new images for recognition.

## Key Features

- **Real-Time Recognition**: Instantly recognizes faces as they appear on the screen.
- **User-Friendly Interface**: Simple buttons control the start and stop of face recognition, enhancing usability.
- **Image Addition**: Easily expand the recognition database by adding new images through a file chooser.
- **Customization**: Utilizes Kivy to create a sleek and responsive user interface.

## How it Works

1. **Capture Frames**: The application captures video frames from the webcam using OpenCV.
2. **Face Recognition**: Our custom face recognition module identifies faces in the frames, distinguishing between known and unknown faces.
3. **User Interface**: Kivy provides the platform for creating the user interface, ensuring smooth interaction with the application.

## Usage

1. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the application:
    ```bash
    python main.py
    ```

3. Use the "Start Recognition" button to initiate face recognition.
4. Use the "Stop Recognition" button to stop face recognition.
5. Use the "Add Image" button to add new images for recognition.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or improvements, feel free to open an issue or create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

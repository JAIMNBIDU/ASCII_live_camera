# ASCII_live_camera
I think it self explanatory but for those who didn't get it its a real time camera feed that turns your live camera feed into ASCII.

Real-Time ASCII Camera (Python + OpenCV)

Turn your webcam feed into live ASCII art — in real time.
This project captures video from your camera, processes each frame, converts pixel brightness to ASCII characters, and renders the result dynamically.
It’s fast, clean, and entirely written in Python using OpenCV and NumPy.

 Overview
Every video frame is:
Captured from your webcam using OpenCV.
Downscaled to a smaller grid (based on desired resolution).
Converted to grayscale brightness values.
Mapped to ASCII characters according to pixel intensity.
Drawn as text on a blank image, optionally colored using original frame color.
Displayed live at 25–40 FPS depending on settings.
The result: a smooth, live “ASCII mirror” of yourself — like watching your webcam inside a typewriter.

 Features
✅ Real-time ASCII rendering from webcam feed
✅ Adjustable resolution, contrast, and FPS
✅ Option to enable/disable color mode
✅ Smooth live FPS counter
✅ Threaded camera capture for zero input lag
✅ Clean modular codebase (easy to extend)

 Tech Stack
Python 3.10+
OpenCV → video capture, rendering, display
NumPy → fast array manipulation
Threading → async camera input for performance

 Installation
Clone the repository:
git clone https://github.com/<your-username>/ascii-camera.git
cd ascii-camera

Install dependencies:
pip install opencv-python numpy
or 
python -m pip install opencv-python numpy

 Run It
python ascii_live_simple.py

 Configuration
Edit these variables in the code to customize behavior:

Variable        Description				                    Example
NUM_COLS	      Number of ASCII columns (resolution)	160
DARK_LIMIT	    Brightness threshold for blank space	25
USE_COLOR	      Enable/disable colored ASCII mode	    True (use "False" for black and white)
FONT_SCALE	    Size of each ASCII character		      0.35
FONT_THICKNESS	Boldness of text			                1

⚡ Performance Tips
Goal			            Adjustment
More FPS	          	Decrease NUM_COLS (e.g., 100)
Sharper Detail		    Increase NUM_COLS (e.g., 200)
Cleaner Blacks	    	Raise DARK_LIMIT (30–40)
Faster Rendering	    Set USE_COLOR = False


that's the end
try it out


🎥 Real-Time ASCII Camera

Turn your webcam feed into live ASCII art — directly in Python.

Converts every video frame into ASCII characters in real time using OpenCV and NumPy.
Optionally colorized, runs at 25–40 FPS, and fully customizable.

🧠 Overview

This project transforms your webcam feed into ASCII art dynamically.
Each frame is:

Captured from your webcam
Downscaled to a small grid
Converted to grayscale
Mapped to ASCII symbols by brightness
Drawn as text and displayed live

The result? A live ASCII mirror of your surroundings — fast, mesmerizing, and slightly retro.

✨ Features
🧩 Real-time webcam feed → ASCII conversion
🎨 Optional colored ASCII mode
⚙️ Adjustable resolution, brightness, and FPS
💨 Threaded capture for smooth, lag-free output

⚙️ Tech Stack
Component	Purpose
Python 3.10+	Core language
OpenCV	Video capture, drawing, and display
NumPy	Pixel-level math and mapping
Threading	Asynchronous camera input

🧩 Installation
git clone https://github.com/<your-username>/ascii-camera.git
cd ascii-camera
pip install -r requirements.txt

🚀 Run
python ascii_live_simple.py
Press Q to quit the window.

🔧 Configuration
Variable	Description	Default
NUM_COLS	ASCII resolution (more = sharper)	160
DARK_LIMIT	Brightness cutoff for blank pixels	25
USE_COLOR	Toggle color mode	True
FONT_SCALE	Character size	0.35
FONT_THICKNESS	Boldness of ASCII text	1

🖥️ Example Output
Monochrome ASCII:
@@@@@@@@@@@@@%%########**+=--::::........
@@@@@@@@@%%%%#####**++==--::::...........
@@@@@@%%%%####**++==--::::...............
@@@@%%%%###**++==--::::..................

Color Mode (live view):
Each ASCII symbol tinted by the pixel color of your webcam feed.

🧩 How It Works
Capture – Camera feed is read continuously on a background thread.
Resize – Image is scaled to a small grid where each pixel = 1 ASCII char.
Map – Brightness values mapped to characters in " .:-=+*#%@".
Draw – Each character drawn with OpenCV’s putText() (optionally colored).
Display – The ASCII-rendered frame is shown live with FPS overlay.

⚡ Performance Tips
Goal	Adjustment
🏎️ More FPS	Decrease NUM_COLS
🔍 Sharper Detail	Increase NUM_COLS
🌑 Cleaner Blacks	Raise DARK_LIMIT
⚪ Faster Rendering	Set USE_COLOR = False


 Side-by-side original + ASCII display
 Save ASCII video output (.mp4)
 Web streaming via Flask
 Emoji or Unicode art mode
 GPU / OpenGL accelerated renderer

📁 Project Structure
ascii-camera/
├── ascii_live_simple.py     # Main source code
├── requirements.txt         # Dependencies
└── README.md                # Documentation

🧑‍💻 Author
Aryan(JAIMNBIDu)
Built with Python, OpenCV, and too many caffeine molecules.

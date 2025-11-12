<div align="center">

# 🎥 Real-Time ASCII Camera  
**Turn your webcam feed into live ASCII art — in real time.**

Converts every frame from your webcam into ASCII characters using **Python**, **OpenCV**, and **NumPy**.  
Runs smoothly at 25–40 FPS with optional color rendering.

![screenshot](https://user-images.githubusercontent.com/00000000/placeholder-demo.gif)

</div>

---

## 🧭 Overview
Each frame from your camera is:

1. Captured from the webcam  
2. Downscaled to a coarse grid  
3. Converted to grayscale  
4. Mapped to ASCII symbols based on brightness  
5. Drawn as text and displayed live  

Result: a **real-time ASCII mirror** — fast, fluid, and strangely hypnotic.

---

## ✨ Features
- 🧩 Real-time webcam → ASCII conversion  
- 🎨 Optional **colorized** mode  
- ⚙️ Adjustable resolution, brightness & FPS  
- 💨 Threaded capture for lag-free performance  
- 🧱 Minimal, well-commented Python code  

---

## ⚙️ Tech Stack
| Tool | Purpose |
|------|----------|
| **Python 3.10+** | Core language |
| **OpenCV** | Video capture & rendering |
| **NumPy** | Matrix & pixel math |
| **Threading** | Async frame capture |

---

## 🧩 Installation
```bash
# Clone the repo
git clone https://github.com/<your-username>/ascii-camera.git
cd ascii-camera
pip install -r requirements.txt

# Run
python3 ascii_live_simple.py
Press Q to quit.
```
## 🔧 Configuration

| Variable | Meaning | Default |
|:----------|:---------|:--------|
| `NUM_COLS` | ASCII resolution (columns) | `160` |
| `DARK_LIMIT` | Brightness cutoff for blank cells | `25` |
| `USE_COLOR` | Enable colorized ASCII | `True` |
| `FONT_SCALE` | Character size | `0.35` |
| `FONT_THICKNESS` | Text boldness | `1` |

```
🧠 How It Works
Capture – threaded video input
Resize – compress frame → grid
Map – convert brightness → ASCII index
Draw – render characters with OpenCV
Display – show output with FPS overlay


📁 Project Structure
python
Copy code
ascii-camera/
├── ascii_live_simple.py     # main program
├── requirements.txt         # dependencies
└── README.md                # documentation


Author
Aryan (JAIMNBIDU)
Built with Python, OpenCV, too mauch caffeine and quite a lot of free time.  

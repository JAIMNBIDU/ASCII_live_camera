# ascii-cam

Live webcam feed rendered as detailed, colored ASCII directly in your terminal. No GUI window — just raw text.

92-level gradient instead of the usual lazy 10-char ramp, plus true 24-bit color per character, so it actually holds detail instead of looking like a fax.

## Requirements

```
pip install opencv-python numpy
```

## Run

```
python3 ascii_cam.py
```

## Controls

| Key | Action |
|-----|--------|
| `q` | Quit |
| `c` | Toggle color on/off |
| `[` | Decrease detail (smaller width) |
| `]` | Increase detail (larger width) |

No Enter needed — keys register instantly. Works on Linux, macOS, and Windows.

## Notes

- First launch can take a couple seconds — that's the camera negotiating resolution/format, not the script hanging.
- Color mode is heavier on the terminal at high width. Drop color or shrink width with `[` if it feels laggy.

---
JAIMNBIDU

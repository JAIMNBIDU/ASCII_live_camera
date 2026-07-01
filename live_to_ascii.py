#!/usr/bin/env python3
"""
ascii_cam.py — live webcam feed rendered as detailed color ASCII in the terminal.

Requires: opencv-python, numpy
    pip install opencv-python numpy

Run:
    python3 ascii_cam.py

Controls (Linux/macOS terminal, raw key read — no GUI window needed):
    q          -> quit
    c          -> toggle color on/off
    [ / ]      -> decrease / increase output width (detail level)
"""

import sys
import os
import shutil
import threading

import cv2
import numpy as np

IS_WINDOWS = sys.platform.startswith("win")

if IS_WINDOWS:
    import msvcrt
else:
    import select
    import termios
    import tty

ASCII_RAMP = (
    " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
)

state = {
    "color": True,
    "width": None,
    "quit": False,
}
state_lock = threading.Lock()


def get_terminal_size(default_cols=200):
    size = shutil.get_terminal_size(fallback=(default_cols, 50))
    return size.columns, size.lines


def key_listener():
    """Reads single keypresses from stdin, no Enter needed. Cross-platform."""
    if IS_WINDOWS:
        while True:
            with state_lock:
                if state["quit"]:
                    return
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                with state_lock:
                    if ch == 'q':
                        state["quit"] = True
                        return
                    elif ch == 'c':
                        state["color"] = not state["color"]
                    elif ch == '[':
                        state["width"] = max(20, (state["width"] or 100) - 10)
                    elif ch == ']':
                        state["width"] = min(400, (state["width"] or 100) + 10)
            else:
                threading.Event().wait(0.05)
        return

    # Unix/Linux/macOS: raw-mode stdin read
    fd = sys.stdin.fileno()
    try:
        old_settings = termios.tcgetattr(fd)
    except termios.error:
        return  # not a real tty (e.g. piped input) — skip listener

    try:
        tty.setcbreak(fd)
        while True:
            with state_lock:
                if state["quit"]:
                    return
            r, _, _ = select.select([fd], [], [], 0.1)
            if r:
                ch = sys.stdin.read(1)
                with state_lock:
                    if ch == 'q':
                        state["quit"] = True
                        return
                    elif ch == 'c':
                        state["color"] = not state["color"]
                    elif ch == '[':
                        state["width"] = max(20, (state["width"] or 100) - 10)
                    elif ch == ']':
                        state["width"] = min(400, (state["width"] or 100) + 10)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def frame_to_ascii(frame, out_width, color=True):
    h, w = frame.shape[:2]
    char_aspect = 0.55
    out_height = max(1, int((out_width / w) * h * char_aspect))

    small = cv2.resize(frame, (out_width, out_height), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

    ramp_len = len(ASCII_RAMP) - 1
    idx = (gray.astype(np.float32) / 255.0 * ramp_len).astype(np.uint8)

    out_lines = []

    if color:
        bgr = small
        for y in range(out_height):
            parts = []
            prev_color = None
            run_chars = []
            for x in range(out_width):
                b, g, r = bgr[y, x]
                cur_color = (r, g, b)
                ch = ASCII_RAMP[idx[y, x]]
                if cur_color != prev_color:
                    if run_chars:
                        parts.append("".join(run_chars))
                    parts.append(f"\x1b[38;2;{r};{g};{b}m")
                    run_chars = [ch]
                    prev_color = cur_color
                else:
                    run_chars.append(ch)
            if run_chars:
                parts.append("".join(run_chars))
            out_lines.append("".join(parts) + "\x1b[0m")
    else:
        for y in range(out_height):
            row = "".join(ASCII_RAMP[idx[y, x]] for x in range(out_width))
            out_lines.append(row)

    return "\n".join(out_lines)


def main():
    print("Opening camera... (first run / mode switch can take a couple seconds)")

    # Explicit V4L2 backend + MJPG fourcc: skips OpenCV's slower backend probing
    # and gets the camera into its fast native USB format instead of raw YUYV,
    # which is what causes the multi-second hang on many webcams.
    if sys.platform.startswith("linux"):
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    elif IS_WINDOWS:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Could not open webcam (index 0). Try a different index or check permissions.")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Warm-up read: first frame(s) after a mode switch are sometimes stale/black,
    # this also absorbs the negotiation delay before we clear the screen so the
    # visible "wait" happens next to a message instead of a blank terminal.
    cap.read()

    cols, _ = get_terminal_size()
    with state_lock:
        state["width"] = max(40, cols - 2)

    listener = threading.Thread(target=key_listener, daemon=True)
    listener.start()

    os.system("clear")
    print("\x1b[?25l", end="")  # hide cursor

    try:
        while True:
            with state_lock:
                if state["quit"]:
                    break
                color = state["color"]
                out_width = state["width"]

            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            frame = cv2.flip(frame, 1)
            ascii_frame = frame_to_ascii(frame, out_width, color=color)

            # Cursor home + clear from cursor to end of screen: removes
            # leftover artifact lines when frame size/width changes.
            sys.stdout.write("\x1b[H\x1b[J")
            sys.stdout.write(ascii_frame)
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        with state_lock:
            state["quit"] = True
        cap.release()
        print("\x1b[0m\x1b[?25h")  # reset color, show cursor
        os.system("clear")


if __name__ == "__main__":
    main()

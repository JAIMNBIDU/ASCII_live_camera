import cv2
import numpy as np
import time
import threading

# ---------- SETTINGS ----------
CAMERA_ID = 0
NUM_COLS = 160               # number of ASCII columns (increase for more detail)
DARK_LIMIT = 25              # darker than this = blank
ASCII_CHARS = list(" .:-=+*#%@")
USE_COLOR = True             # True = colored ASCII, False = white text
FONT_TYPE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.35
FONT_THICKNESS = 1


class CameraThread(threading.Thread):
    def __init__(self, camera_id=0):
        super().__init__(daemon=True)
        self.camera = cv2.VideoCapture(camera_id)
        if not self.camera.isOpened():
            raise RuntimeError("Cannot open camera")
        self.lock = threading.Lock()
        self.frame = None
        self.running = True

    def run(self):
        while self.running:
            ok, frame = self.camera.read()
            if not ok:
                continue
            with self.lock:
                self.frame = frame

    def get_frame(self):
        with self.lock:
            return None if self.frame is None else self.frame.copy()

    def stop(self):
        self.running = False
        self.camera.release()


def convert_frame_to_ascii(frame, cols):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape

    char_w, char_h = 8, 16
    rows = int(cols * (height / width) * (char_w / char_h))
    small_gray = cv2.resize(gray, (cols, rows), interpolation=cv2.INTER_AREA)

    num_chars = len(ASCII_CHARS)
    brightness_index = (small_gray / 255 * (num_chars - 1)).astype(np.int32)

    if USE_COLOR:
        small_color = cv2.resize(frame, (cols, rows), interpolation=cv2.INTER_AREA)

    output_height = rows * char_h
    output_width = cols * char_w
    output = np.zeros((output_height, output_width, 3), dtype=np.uint8)

    for row in range(rows):
        for col in range(cols):
            brightness = small_gray[row, col]
            if brightness < DARK_LIMIT:
                continue
            char = ASCII_CHARS[brightness_index[row, col]]
            color = (255, 255, 255)
            if USE_COLOR:
                b, g, r = small_color[row, col]
                color = (int(b), int(g), int(r))
            cv2.putText(
                output,
                char,
                (int(col * char_w), int((row + 1) * char_h - 2)),
                FONT_TYPE,
                FONT_SCALE,
                color,
                FONT_THICKNESS,
                cv2.LINE_AA
            )

    return output


def main():
    cam_thread = CameraThread(CAMERA_ID)
    cam_thread.start()
    time.sleep(0.1)

    prev_time = time.time()
    smooth_fps = 0.0

    cv2.namedWindow("ASCII Camera", cv2.WINDOW_NORMAL)

    try:
        while True:
            frame = cam_thread.get_frame()
            if frame is None:
                continue

            ascii_frame = convert_frame_to_ascii(frame, NUM_COLS)

            # FPS counter
            current_time = time.time()
            delta = current_time - prev_time
            prev_time = current_time
            if delta > 0:
                smooth_fps = 0.9 * smooth_fps + 0.1 * (1 / delta)
            cv2.putText(ascii_frame, f"{smooth_fps:.1f} FPS", (10, 25),
                        FONT_TYPE, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow("ASCII Camera", ascii_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cam_thread.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

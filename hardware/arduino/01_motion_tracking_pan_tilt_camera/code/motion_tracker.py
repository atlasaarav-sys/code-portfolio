"""
Motion-Tracking Pan-Tilt Camera
--------------------------------
Captures webcam frames, detects the largest moving object via background
subtraction, and sends proportional pan/tilt corrections to an Arduino
running pan_tilt_controller.ino so the camera rig follows the motion.

Setup:
    pip install opencv-python pyserial

Usage:
    python motion_tracker.py --port COM5          (Windows)
    python motion_tracker.py --port /dev/ttyACM0  (Linux/Mac)

Press 'q' to quit the preview window.
"""

import argparse
import time

import cv2
import serial


def find_largest_motion_blob(fg_mask, min_area=500):
    """Return (x, y, w, h) of the largest contour above min_area, or None."""
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    largest = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest) < min_area:
        return None

    return cv2.boundingRect(largest)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True, help="Serial port for the Arduino, e.g. COM5 or /dev/ttyACM0")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--camera", type=int, default=0, help="Webcam index")
    parser.add_argument("--min-area", type=int, default=500, help="Minimum contour area to count as motion")
    parser.add_argument("--gain", type=float, default=0.06, help="Proportional gain for angle correction")
    args = parser.parse_args()

    # --- Connect to Arduino ---
    print(f"Connecting to Arduino on {args.port}...")
    arduino = serial.Serial(args.port, args.baud, timeout=1)
    time.sleep(2)  # allow Arduino to reset after serial connect

    # --- Open webcam ---
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam. Try a different --camera index.")

    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    center_x, center_y = frame_w // 2, frame_h // 2

    bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=25, detectShadows=False)

    # Current servo angles (start centered)
    pan_angle = 90
    tilt_angle = 90
    send_pan_tilt(arduino, pan_angle, tilt_angle)

    print("Tracking started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # mirror for intuitive viewing

        fg_mask = bg_subtractor.apply(frame)
        fg_mask = cv2.medianBlur(fg_mask, 5)
        _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

        blob = find_largest_motion_blob(fg_mask, args.min_area)

        if blob is not None:
            x, y, w, h = blob
            target_x = x + w // 2
            target_y = y + h // 2

            # Error between target and frame center, in pixels
            error_x = target_x - center_x
            error_y = target_y - center_y

            # Proportional control: nudge angles toward the target.
            # Positive error_x (target right of center) should decrease pan angle
            # or increase it depending on servo orientation -- flip sign if it
            # tracks backwards on your rig.
            pan_angle -= error_x * args.gain
            tilt_angle += error_y * args.gain

            pan_angle = max(0, min(180, pan_angle))
            tilt_angle = max(30, min(150, tilt_angle))

            send_pan_tilt(arduino, int(pan_angle), int(tilt_angle))

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (target_x, target_y), 4, (0, 0, 255), -1)

        cv2.circle(frame, (center_x, center_y), 4, (255, 0, 0), -1)
        cv2.imshow("Motion Tracker", frame)
        cv2.imshow("Motion Mask", fg_mask)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()


def send_pan_tilt(arduino, pan, tilt):
    command = f"P{pan} T{tilt}\n"
    arduino.write(command.encode("utf-8"))


if __name__ == "__main__":
    main()

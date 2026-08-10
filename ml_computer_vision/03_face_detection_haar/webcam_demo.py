"""Live webcam face detection. Press 'q' to quit."""

import cv2

from face_detector import load_cascade, detect_faces, draw_detections


def main():
    cascade = load_cascade()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    print("Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detect_faces(frame, cascade)
        output = draw_detections(frame, faces)
        cv2.putText(output, f"Faces: {len(faces)}", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Face Detection", output)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

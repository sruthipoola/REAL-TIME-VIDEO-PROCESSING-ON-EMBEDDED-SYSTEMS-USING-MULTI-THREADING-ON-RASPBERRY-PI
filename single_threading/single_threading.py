import cv2
import time

def main():
    # Open webcam (0 = default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream")
        return

    prev_time = 0

    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if prev_time else 0
        prev_time = current_time

        # Put FPS text on video
        cv2.putText(frame, f"FPS: {fps:.2f}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show window
        cv2.imshow("Real-Time Video (Single Thread)", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
time.sleep(0.05)   # sleep for 50 ms

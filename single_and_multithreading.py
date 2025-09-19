import cv2
import time
import threading
import queue
import matplotlib.pyplot as plt


# ---------------- SINGLE THREAD ----------------
def single_thread_demo(source=0, duration=10, delay=0.05):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Error: cannot open video source:", source)
        return []

    start_time = time.perf_counter()
    fps_list = []

    while True:
        t0 = time.perf_counter()
        ret, frame = cap.read()
        if not ret:
            break

        # --- Simulated heavy processing ---
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        time.sleep(delay)  # artificial heavy step
        # ----------------------------------

        cv2.imshow("Single Thread", gray)

        elapsed = time.perf_counter() - t0
        fps = 1.0 / elapsed if elapsed > 0 else 0
        fps_list.append(fps)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if time.perf_counter() - start_time > duration:
            break

    cap.release()
    cv2.destroyAllWindows()
    return fps_list


# ---------------- MULTI THREAD ----------------
def capture_frames(cap, frame_queue, stop_event):
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        if not frame_queue.full():
            frame_queue.put(frame)


def multi_thread_demo(source=0, duration=10, delay=0.05):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Error: cannot open video source:", source)
        return []

    frame_queue = queue.Queue(maxsize=10)
    stop_event = threading.Event()
    capture_thread = threading.Thread(target=capture_frames, args=(cap, frame_queue, stop_event))
    capture_thread.start()

    start_time = time.perf_counter()
    fps_list = []

    while True:
        t0 = time.perf_counter()
        if not frame_queue.empty():
            frame = frame_queue.get()

            # --- Simulated heavy processing ---
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            time.sleep(delay)
            # ----------------------------------

            cv2.imshow("Multi Thread", gray)

            elapsed = time.perf_counter() - t0
            fps = 1.0 / elapsed if elapsed > 0 else 0
            fps_list.append(fps)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if time.perf_counter() - start_time > duration:
            break

    stop_event.set()
    capture_thread.join()
    cap.release()
    cv2.destroyAllWindows()
    return fps_list


# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("Running single-thread demo...")
    fps_single = single_thread_demo(0, duration=10)

    print("Running multi-thread demo...")
    fps_multi = multi_thread_demo(0, duration=10)

    # --- Plot results ---
    plt.figure(figsize=(10, 5))
    plt.plot(fps_single, label="Single Thread FPS")
    plt.plot(fps_multi, label="Multi Thread FPS")
    plt.xlabel("Frame #")
    plt.ylabel("FPS")
    plt.title("Single vs Multi Thread Video Processing")
    plt.legend()
    plt.show()
plt.savefig("result.png")

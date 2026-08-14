from detectors.pose_detector import PoseDetector
from detectors.fall_detector import FallDetector
from trackers.tracker import PersonTracker
from utils.geometry import body_angle
from utils.speed import SpeedTracker
import time
import pygame
import threading


def play_alarm():
    pygame.mixer.music.load("alarm/alarm.wav")
    pygame.mixer.music.play()


import cv2
from ultralytics import YOLO

# -----------------------------
# Load Models
# -----------------------------
model = YOLO("yolov8n-pose.pt")

pose_detector = PoseDetector()
fall_detector = FallDetector()
tracker = PersonTracker()

speed_tracker = SpeedTracker()

pygame.mixer.init()
alarm_playing = False

# -----------------------------
# Open Video
# -----------------------------
cap = cv2.VideoCapture("videos/fall_test.mp4")

if not cap.isOpened():
    print("Camera open nahi hua.")
    exit()

# -----------------------------
# Main Loop
# -----------------------------
while True:

    ret, frame = cap.read()

    if not ret or frame is None:
        print("Video Finished")
        break

    active_ids = set()

    # Tracking
    results = model.track(frame, persist=True, tracker="bytetrack.yaml", verbose=False)

    # Every Result
    for result in results:

        # Pose Keypoints
        keypoints = pose_detector.get_keypoints(result)

        if keypoints is not None:

            # Draw Pose
            frame = pose_detector.draw_keypoints(frame, keypoints)
            frame = pose_detector.draw_skeleton(frame, keypoints)

        # Draw Body Centers
        for person in keypoints:

            sx, sy, hx, hy = pose_detector.get_body_points(person)

            angle = body_angle(sx, sy, hx, hy)

            cv2.putText(
                frame,
                f"Angle: {angle:.1f}",
                (sx + 10, sy),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )

            # Shoulder Center
            cv2.circle(frame, (sx, sy), 6, (255, 0, 0), -1)

            # Hip Center
            cv2.circle(frame, (hx, hy), 6, (0, 0, 255), -1)

            # Body Line
            cv2.line(frame, (sx, sy), (hx, hy), (255, 255, 0), 3)

        # print(keypoints.shape)

        if result.boxes is None:
            continue

        # Every Person
        for box in result.boxes:

            cls = int(box.cls[0])

            if cls != 0:
                continue

            # Bounding Box
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            width = x2 - x1
            height = y2 - y1

            conf = float(box.conf[0])

            # Person ID
            if box.id is not None:
                person_id = int(box.id[0])
            else:
                person_id = -1

            # Center
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            # Match pose with current tracked person
            best_person = None
            best_distance = float("inf")

            if keypoints is not None:

                for person in keypoints:

                    px, py = pose_detector.get_pose_center(person)

                    distance = ((px - center_x) ** 2 + (py - center_y) ** 2) ** 0.5

                    if distance < best_distance:
                        best_distance = distance
                        best_person = person

            if best_person is not None:

                sx, sy, hx, hy = pose_detector.get_body_points(best_person)

                angle = body_angle(sx, sy, hx, hy)

                speed = speed_tracker.get_speed(person_id, hy)

                print(f"ID:{person_id}  Angle:{angle:.1f}  Speed:{speed:.1f}")

            else:

                angle = 0
                speed = 0

            print(f"ID:{person_id}  Angle:{angle:.1f}  Speed:{speed:.1f}")

            # Tracker Update
            tracker.update(person_id, (center_x, center_y))

            active_ids.add(person_id)

            history = tracker.get_history(person_id)

            # Fall Detection
            fall = fall_detector.check_fall(person_id, angle, speed)

            print("Fall Status:", fall)

    if person_id in fall_detector.start_time:

        seconds = time.time() - fall_detector.start_time[person_id]

        cv2.putText(
            frame,
            f"Ground: {seconds:.1f}s",
            (x1, y1 - 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )

        # Box Color
        if fall:
            box_color = (0, 0, 255)

            print("******** FALL DETECTED ********")

        if fall and not alarm_playing:

            alarm_playing = True

            threading.Thread(target=play_alarm, daemon=True).start()

        else:
            box_color = (0, 255, 0)
        # Rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)

        # Center Point
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

        # Label
        label = f"ID:{person_id} {conf:.2f}"

        cv2.putText(
            frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, box_color, 2
        )

        # Fall Alert
        if fall:
            cv2.putText(
                frame,
                "FALL DETECTED",
                (x1, y1 - 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3,
            )

        # History
        cv2.putText(
            frame,
            f"History: {len(history)}",
            (x1, y2 + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2,
        )

    # Remove Missing IDs
    tracker.clear_missing(active_ids)

    # Show Frame
    cv2.imshow("Fall Detection System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

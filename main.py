import cv2
import pyautogui
import time

from hand_tracker import HandTracker
import config


# ============================================================
# AI VIRTUAL MOUSE
# Phase 7.1 - Smooth Cursor + Stable Controls
# ============================================================


def main():

    print("=" * 55)
    print("AI VIRTUAL MOUSE")
    print("=" * 55)

    # --------------------------------------------------------
    # CAMERA
    # --------------------------------------------------------

    camera = cv2.VideoCapture(config.CAMERA_INDEX)

    if not camera.isOpened():
        print("ERROR: Could not open camera.")
        return

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        config.FRAME_WIDTH
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        config.FRAME_HEIGHT
    )

    print("Camera started successfully.")

    # --------------------------------------------------------
    # HAND TRACKER
    # --------------------------------------------------------

    hand_tracker = HandTracker(
        max_num_hands=config.MAX_NUM_HANDS,
        detection_confidence=config.DETECTION_CONFIDENCE,
        tracking_confidence=config.TRACKING_CONFIDENCE
    )

    print("MediaPipe hand tracking started.")

    # --------------------------------------------------------
    # SCREEN SIZE
    # --------------------------------------------------------

    screen_width, screen_height = pyautogui.size()

    print(
        f"Screen resolution: "
        f"{screen_width} x {screen_height}"
    )

    # --------------------------------------------------------
    # CURSOR VARIABLES
    # --------------------------------------------------------

    previous_x = screen_width // 2
    previous_y = screen_height // 2

    last_click_time = 0

    # --------------------------------------------------------
    # START MESSAGE
    # --------------------------------------------------------

    print()
    print("AI Virtual Mouse started.")
    print()
    print("CONTROLS:")
    print("Move INDEX finger  -> Move cursor")
    print("Thumb + INDEX      -> LEFT CLICK")
    print("INDEX + MIDDLE     -> RIGHT CLICK")
    print("Press ESC           -> Exit")
    print()

    # --------------------------------------------------------
    # MAIN LOOP
    # --------------------------------------------------------

    try:

        while True:

            # ------------------------------------------------
            # READ CAMERA
            # ------------------------------------------------

            success, frame = camera.read()

            if not success:

                print("Unable to read camera frame.")

                continue

            # Mirror camera
            frame = cv2.flip(frame, 1)

            # ------------------------------------------------
            # PROCESS HAND
            # ------------------------------------------------

            results = hand_tracker.process_frame(frame)

            # Draw landmarks
            frame = hand_tracker.draw_landmarks(
                frame,
                results
            )

            # ------------------------------------------------
            # GET LANDMARKS
            # ------------------------------------------------

            landmarks = hand_tracker.get_landmarks(results)

            # ------------------------------------------------
            # HAND DETECTED
            # ------------------------------------------------

            if landmarks:

                # MediaPipe landmarks
                #
                # 4  = Thumb tip
                # 8  = Index tip
                # 12 = Middle tip

                thumb = landmarks[4]
                index = landmarks[8]
                middle = landmarks[12]

                camera_height, camera_width, _ = frame.shape

                # ------------------------------------------------
                # INDEX FINGER POSITION
                # ------------------------------------------------

                index_x = int(
                    index.x * camera_width
                )

                index_y = int(
                    index.y * camera_height
                )

                # ------------------------------------------------
                # CAMERA -> SCREEN
                # ------------------------------------------------

                target_x = int(
                    index.x * screen_width
                )

                target_y = int(
                    index.y * screen_height
                )

                # Keep cursor inside screen
                target_x = max(
                    0,
                    min(screen_width - 1, target_x)
                )

                target_y = max(
                    0,
                    min(screen_height - 1, target_y)
                )

                # ------------------------------------------------
                # SMOOTH CURSOR
                # ------------------------------------------------

                smoothing = config.SMOOTHING

                current_x = (
                    previous_x
                    + (target_x - previous_x)
                    * smoothing
                )

                current_y = (
                    previous_y
                    + (target_y - previous_y)
                    * smoothing
                )

                current_x = int(current_x)
                current_y = int(current_y)

                # Move cursor
                pyautogui.moveTo(
                    current_x,
                    current_y,
                    duration=0
                )

                previous_x = current_x
                previous_y = current_y

                # ------------------------------------------------
                # DRAW INDEX POINT
                # ------------------------------------------------

                cv2.circle(
                    frame,
                    (index_x, index_y),
                    10,
                    (0, 255, 0),
                    -1
                )

                # ------------------------------------------------
                # THUMB POSITION
                # ------------------------------------------------

                thumb_x = int(
                    thumb.x * camera_width
                )

                thumb_y = int(
                    thumb.y * camera_height
                )

                # ------------------------------------------------
                # MIDDLE POSITION
                # ------------------------------------------------

                middle_x = int(
                    middle.x * camera_width
                )

                middle_y = int(
                    middle.y * camera_height
                )

                # ------------------------------------------------
                # THUMB + INDEX DISTANCE
                # ------------------------------------------------

                left_distance = (
                    (thumb_x - index_x) ** 2
                    +
                    (thumb_y - index_y) ** 2
                ) ** 0.5

                # ------------------------------------------------
                # INDEX + MIDDLE DISTANCE
                # ------------------------------------------------

                right_distance = (
                    (index_x - middle_x) ** 2
                    +
                    (index_y - middle_y) ** 2
                ) ** 0.5

                # ------------------------------------------------
                # CURRENT TIME
                # ------------------------------------------------

                current_time = time.time()

                # ------------------------------------------------
                # LEFT CLICK
                # ------------------------------------------------

                if (
                    left_distance
                    < config.LEFT_CLICK_THRESHOLD
                    and
                    current_time - last_click_time
                    > config.CLICK_COOLDOWN
                ):

                    pyautogui.click()

                    print("LEFT CLICK")

                    last_click_time = current_time

                    cv2.putText(
                        frame,
                        "LEFT CLICK",
                        (20, 125),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 255, 0),
                        2
                    )

                # ------------------------------------------------
                # RIGHT CLICK
                # ------------------------------------------------

                elif (
                    right_distance
                    < config.RIGHT_CLICK_THRESHOLD
                    and
                    current_time - last_click_time
                    > config.CLICK_COOLDOWN
                ):

                    pyautogui.rightClick()

                    print("RIGHT CLICK")

                    last_click_time = current_time

                    cv2.putText(
                        frame,
                        "RIGHT CLICK",
                        (20, 125),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 255, 255),
                        2
                    )

                # ------------------------------------------------
                # STATUS
                # ------------------------------------------------

                cv2.putText(
                    frame,
                    "HAND DETECTED",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    "INDEX = MOVE",
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    1
                )

                cv2.putText(
                    frame,
                    "THUMB + INDEX = LEFT CLICK",
                    (20, 95),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    1
                )

                cv2.putText(
                    frame,
                    "INDEX + MIDDLE = RIGHT CLICK",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    1
                )

            else:

                # ------------------------------------------------
                # NO HAND
                # ------------------------------------------------

                cv2.putText(
                    frame,
                    "NO HAND DETECTED",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            # ------------------------------------------------
            # DISPLAY WINDOW
            # ------------------------------------------------

            cv2.imshow(
                config.WINDOW_NAME,
                frame
            )

            # ------------------------------------------------
            # ESC
            # ------------------------------------------------

            key = cv2.waitKey(1) & 0xFF

            if key == 27:

                print()
                print("ESC pressed.")

                break

    except KeyboardInterrupt:

        print()
        print("Program interrupted.")

    except Exception as error:

        print()
        print("Application Error:")
        print(error)

    finally:

        # ----------------------------------------------------
        # CLEANUP
        # ----------------------------------------------------

        print("Stopping virtual mouse...")

        hand_tracker.close()

        camera.release()

        cv2.destroyAllWindows()

        print("Mouse control stopped.")
        print("Resources released successfully.")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
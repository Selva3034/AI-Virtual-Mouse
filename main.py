import cv2
import pyautogui
import time

from hand_tracker import HandTracker


# =========================================================
# SETTINGS
# =========================================================

CAMERA_INDEX = 0

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Cursor smoothing
SMOOTHING = 0.25

# Gesture thresholds
LEFT_CLICK_THRESHOLD = 35
RIGHT_CLICK_THRESHOLD = 35

# Click protection
CLICK_COOLDOWN = 0.5

# Double click
DOUBLE_CLICK_TIME = 0.45

# Drag
DRAG_HOLD_TIME = 0.7

# Scroll
SCROLL_THRESHOLD = 12
SCROLL_SPEED = 2


# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 55)
    print("AI VIRTUAL MOUSE")
    print("=" * 55)

    print("Starting camera...")

    # -----------------------------------------------------
    # CAMERA
    # -----------------------------------------------------

    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        print("ERROR: Could not open camera.")
        return

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        FRAME_WIDTH
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        FRAME_HEIGHT
    )

    print("Camera started successfully.")

    # -----------------------------------------------------
    # HAND TRACKER
    # -----------------------------------------------------

    hand_tracker = HandTracker(
        max_num_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.7
    )

    print("MediaPipe hand tracking started.")

    # -----------------------------------------------------
    # SCREEN
    # -----------------------------------------------------

    screen_width, screen_height = pyautogui.size()

    print(
        f"Screen resolution: "
        f"{screen_width} x {screen_height}"
    )

    # =====================================================
    # CURSOR VARIABLES
    # =====================================================

    previous_x = 0
    previous_y = 0

    # =====================================================
    # CLICK VARIABLES
    # =====================================================

    last_click_time = 0
    last_left_click_time = 0

    left_pinch_active = False
    right_pinch_active = False

    # =====================================================
    # DRAG VARIABLES
    # =====================================================

    pinch_start_time = None
    dragging = False

    # =====================================================
    # SCROLL VARIABLES
    # =====================================================

    previous_scroll_y = None
    scrolling = False

    # =====================================================
    # START
    # =====================================================

    print()
    print("AI Virtual Mouse started.")
    print()

    print("CONTROLS:")
    print("Move INDEX finger              -> Move cursor")
    print("Quick Thumb + INDEX            -> LEFT CLICK")
    print("Quick pinch twice              -> DOUBLE CLICK")
    print("Hold Thumb + INDEX             -> DRAG")
    print("Release Thumb + INDEX          -> DROP")
    print("INDEX + MIDDLE pinch            -> RIGHT CLICK")
    print("INDEX + MIDDLE extended        -> SCROLL")
    print("Press ESC                      -> Exit")
    print()

    # =====================================================
    # MAIN LOOP
    # =====================================================

    try:

        while True:

            # -------------------------------------------------
            # READ CAMERA
            # -------------------------------------------------

            success, frame = camera.read()

            if not success:

                print("Unable to read camera frame.")
                continue

            # Mirror camera
            frame = cv2.flip(frame, 1)

            # -------------------------------------------------
            # HAND DETECTION
            # -------------------------------------------------

            results = hand_tracker.process_frame(frame)

            frame = hand_tracker.draw_landmarks(
                frame,
                results
            )

            landmarks = hand_tracker.get_landmarks(
                results
            )

            # =================================================
            # HAND DETECTED
            # =================================================

            if landmarks:

                thumb = landmarks[4]
                index = landmarks[8]
                middle = landmarks[12]

                # Extra landmarks for finger-state detection
                index_mcp = landmarks[5]
                middle_mcp = landmarks[9]

                camera_height, camera_width, _ = frame.shape

                # =================================================
                # INDEX POSITION
                # =================================================

                index_x = int(
                    index.x * camera_width
                )

                index_y = int(
                    index.y * camera_height
                )

                # =================================================
                # SCREEN POSITION
                # =================================================

                target_x = int(
                    index.x * screen_width
                )

                target_y = int(
                    index.y * screen_height
                )

                # =================================================
                # CURSOR SMOOTHING
                # =================================================

                current_x = (
                    previous_x
                    + (target_x - previous_x)
                    * SMOOTHING
                )

                current_y = (
                    previous_y
                    + (target_y - previous_y)
                    * SMOOTHING
                )

                current_x = int(current_x)
                current_y = int(current_y)

                # -------------------------------------------------
                # MOVE CURSOR
                # -------------------------------------------------

                pyautogui.moveTo(
                    current_x,
                    current_y,
                    duration=0
                )

                previous_x = current_x
                previous_y = current_y

                # -------------------------------------------------
                # DRAW INDEX FINGERTIP
                # -------------------------------------------------

                cv2.circle(
                    frame,
                    (index_x, index_y),
                    10,
                    (0, 255, 0),
                    -1
                )

                # =================================================
                # THUMB POSITION
                # =================================================

                thumb_x = int(
                    thumb.x * camera_width
                )

                thumb_y = int(
                    thumb.y * camera_height
                )

                # =================================================
                # INDEX POSITION
                # =================================================

                index_point_x = int(
                    index.x * camera_width
                )

                index_point_y = int(
                    index.y * camera_height
                )

                # =================================================
                # MIDDLE POSITION
                # =================================================

                middle_x = int(
                    middle.x * camera_width
                )

                middle_y = int(
                    middle.y * camera_height
                )

                # =================================================
                # LEFT CLICK / DRAG DISTANCE
                # =================================================

                left_distance = (
                    (thumb_x - index_point_x) ** 2
                    +
                    (thumb_y - index_point_y) ** 2
                ) ** 0.5

                # =================================================
                # RIGHT CLICK DISTANCE
                # =================================================

                right_distance = (
                    (index_point_x - middle_x) ** 2
                    +
                    (index_point_y - middle_y) ** 2
                ) ** 0.5

                # =================================================
                # CURRENT TIME
                # =================================================

                current_time = time.time()

                # =================================================
                # FINGER EXTENSION DETECTION
                # =================================================

                index_extended = (
                    index.y < index_mcp.y
                )

                middle_extended = (
                    middle.y < middle_mcp.y
                )

                # =================================================
                # SCROLL MODE
                # =================================================

                scroll_gesture = (
                    index_extended
                    and middle_extended
                    and right_distance > RIGHT_CLICK_THRESHOLD
                    and not left_pinch_active
                    and not dragging
                )

                if scroll_gesture:

                    scrolling = True

                    # Start tracking scroll position
                    if previous_scroll_y is None:

                        previous_scroll_y = (
                            index_y + middle_y
                        ) / 2

                    current_scroll_y = (
                        index_y + middle_y
                    ) / 2

                    scroll_difference = (
                        current_scroll_y
                        - previous_scroll_y
                    )

                    # -------------------------------------------------
                    # SCROLL DOWN
                    # -------------------------------------------------

                    if scroll_difference > SCROLL_THRESHOLD:

                        pyautogui.scroll(
                            -SCROLL_SPEED
                        )

                        cv2.putText(
                            frame,
                            "SCROLL DOWN",
                            (20, 120),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 165, 255),
                            2
                        )

                    # -------------------------------------------------
                    # SCROLL UP
                    # -------------------------------------------------

                    elif scroll_difference < -SCROLL_THRESHOLD:

                        pyautogui.scroll(
                            SCROLL_SPEED
                        )

                        cv2.putText(
                            frame,
                            "SCROLL UP",
                            (20, 120),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 165, 255),
                            2
                        )

                    else:

                        cv2.putText(
                            frame,
                            "SCROLL MODE",
                            (20, 120),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 165, 255),
                            2
                        )

                    previous_scroll_y = current_scroll_y

                else:

                    # Reset scroll tracking
                    scrolling = False
                    previous_scroll_y = None

                # =================================================
                # LEFT PINCH / DRAG
                # =================================================

                if (
                    left_distance < LEFT_CLICK_THRESHOLD
                    and not scrolling
                ):

                    # -------------------------------------------------
                    # PINCH START
                    # -------------------------------------------------

                    if not left_pinch_active:

                        left_pinch_active = True

                        pinch_start_time = current_time

                    # -------------------------------------------------
                    # START DRAG
                    # -------------------------------------------------

                    if (
                        pinch_start_time is not None
                        and not dragging
                        and
                        current_time - pinch_start_time
                        >= DRAG_HOLD_TIME
                    ):

                        pyautogui.mouseDown()

                        dragging = True

                        print("DRAG STARTED")

                    # -------------------------------------------------
                    # DRAGGING
                    # -------------------------------------------------

                    if dragging:

                        cv2.putText(
                            frame,
                            "DRAGGING",
                            (20, 120),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 0, 0),
                            2
                        )

                    else:

                        cv2.putText(
                            frame,
                            "PINCH",
                            (20, 120),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 255, 255),
                            2
                        )

                # =================================================
                # LEFT PINCH RELEASE
                # =================================================

                else:

                    if dragging:

                        pyautogui.mouseUp()

                        dragging = False

                        pinch_start_time = None

                        print("DRAG ENDED")

                        cv2.putText(
                            frame,
                            "DROP",
                            (20, 120),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 0, 0),
                            2
                        )

                    elif left_pinch_active:

                        pinch_duration = 0

                        if pinch_start_time is not None:

                            pinch_duration = (
                                current_time
                                - pinch_start_time
                            )

                        # -------------------------------------------------
                        # SHORT PINCH = CLICK
                        # -------------------------------------------------

                        if pinch_duration < DRAG_HOLD_TIME:

                            # -------------------------------------------------
                            # DOUBLE CLICK
                            # -------------------------------------------------

                            if (
                                current_time
                                - last_left_click_time
                                <= DOUBLE_CLICK_TIME
                            ):

                                pyautogui.doubleClick()

                                print("DOUBLE CLICK")

                                cv2.putText(
                                    frame,
                                    "DOUBLE CLICK",
                                    (20, 120),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1,
                                    (255, 0, 255),
                                    2
                                )

                                last_left_click_time = 0

                            # -------------------------------------------------
                            # SINGLE CLICK
                            # -------------------------------------------------

                            else:

                                if (
                                    current_time
                                    - last_click_time
                                    > CLICK_COOLDOWN
                                ):

                                    pyautogui.click()

                                    print("LEFT CLICK")

                                    last_click_time = current_time

                                    last_left_click_time = (
                                        current_time
                                    )

                                    cv2.putText(
                                        frame,
                                        "LEFT CLICK",
                                        (20, 120),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        1,
                                        (0, 255, 0),
                                        2
                                    )

                    left_pinch_active = False

                    pinch_start_time = None

                # =================================================
                # RIGHT CLICK
                # =================================================

                if (
                    right_distance < RIGHT_CLICK_THRESHOLD
                    and not left_pinch_active
                    and not dragging
                    and not scrolling
                ):

                    if not right_pinch_active:

                        if (
                            current_time
                            - last_click_time
                            > CLICK_COOLDOWN
                        ):

                            pyautogui.rightClick()

                            print("RIGHT CLICK")

                            last_click_time = current_time

                            cv2.putText(
                                frame,
                                "RIGHT CLICK",
                                (20, 120),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0, 255, 255),
                                2
                            )

                        right_pinch_active = True

                else:

                    right_pinch_active = False

                # =================================================
                # STATUS
                # =================================================

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
                    "INDEX = CURSOR",
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    1
                )

                cv2.putText(
                    frame,
                    "PINCH = CLICK / HOLD = DRAG",
                    (20, 95),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    1
                )

            # =================================================
            # NO HAND DETECTED
            # =================================================

            else:

                cv2.putText(
                    frame,
                    "NO HAND DETECTED",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

                # -------------------------------------------------
                # SAFETY: RELEASE DRAG
                # -------------------------------------------------

                if dragging:

                    pyautogui.mouseUp()

                    dragging = False

                    print(
                        "DRAG CANCELLED - HAND LOST"
                    )

                # Reset everything
                left_pinch_active = False
                right_pinch_active = False
                pinch_start_time = None
                previous_scroll_y = None
                scrolling = False

            # =================================================
            # DISPLAY CAMERA
            # =================================================

            cv2.imshow(
                "AI Virtual Mouse",
                frame
            )

            # =================================================
            # ESC
            # =================================================

            key = cv2.waitKey(1) & 0xFF

            if key == 27:

                print()
                print("ESC pressed.")
                break

    # =========================================================
    # KEYBOARD INTERRUPT
    # =========================================================

    except KeyboardInterrupt:

        print()
        print("Program interrupted.")

    # =========================================================
    # ERROR HANDLING
    # =========================================================

    except Exception as error:

        print()
        print("Application Error:")
        print(error)

    # =========================================================
    # CLEANUP
    # =========================================================

    finally:

        # Safety release
        if dragging:

            try:
                pyautogui.mouseUp()
            except:
                pass

        print("Stopping virtual mouse...")

        hand_tracker.close()

        camera.release()

        cv2.destroyAllWindows()

        print("Resources released successfully.")


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":
    main()
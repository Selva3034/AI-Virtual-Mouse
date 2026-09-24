import cv2
import pyautogui
import time

from hand_tracker import HandTracker
import config
import control


# ============================================================
# CONFIGURATION
# ============================================================

CAMERA_INDEX = getattr(config, "CAMERA_INDEX", 0)

FRAME_WIDTH = getattr(config, "FRAME_WIDTH", 1280)
FRAME_HEIGHT = getattr(config, "FRAME_HEIGHT", 720)

DEFAULT_SMOOTHING = getattr(
    config,
    "SMOOTHING_FACTOR",
    0.5
)

DEFAULT_SCROLL_SPEED = getattr(
    config,
    "SCROLL_SPEED",
    3
)

DEFAULT_CONFIRM_FRAMES = getattr(
    config,
    "GESTURE_CONFIRM_FRAMES",
    3
)

CLICK_DISTANCE = getattr(
    config,
    "CLICK_DISTANCE",
    0.05
)

RIGHT_CLICK_DISTANCE = getattr(
    config,
    "RIGHT_CLICK_DISTANCE",
    0.05
)

DOUBLE_CLICK_TIME = getattr(
    config,
    "DOUBLE_CLICK_TIME",
    0.45
)

DRAG_HOLD_TIME = getattr(
    config,
    "DRAG_HOLD_TIME",
    0.7
)

CLICK_COOLDOWN = getattr(
    config,
    "CLICK_COOLDOWN",
    0.35
)

ACTION_COOLDOWN = getattr(
    config,
    "GESTURE_ACTION_COOLDOWN",
    0.35
)

SCROLL_CLICK_BLOCK_TIME = getattr(
    config,
    "SCROLL_CLICK_BLOCK_TIME",
    0.5
)

RIGHT_CLICK_BLOCK_TIME = getattr(
    config,
    "RIGHT_CLICK_BLOCK_TIME",
    0.5
)

PAUSE_HOLD_TIME = getattr(
    config,
    "PAUSE_HOLD_TIME",
    1.0
)

SCROLL_THRESHOLD = getattr(
    config,
    "SCROLL_THRESHOLD",
    0.02
)

WINDOW_NAME = getattr(
    config,
    "WINDOW_NAME",
    "AI Virtual Mouse"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def distance(point1, point2):

    if point1 is None or point2 is None:
        return 999

    dx = point1.x - point2.x
    dy = point1.y - point2.y

    return (dx * dx + dy * dy) ** 0.5


def confirm_gesture(
    current_gesture,
    last_gesture,
    gesture_count,
    required_frames
):

    if current_gesture == last_gesture:
        gesture_count += 1
    else:
        gesture_count = 1

    confirmed = gesture_count >= required_frames

    return current_gesture, gesture_count, confirmed


# ============================================================
# VISUALIZATION HELPERS
# ============================================================

def draw_hand_visualization(
    frame,
    landmarks,
    gesture
):

    """
    Draw enhanced hand visualization:

    - Hand bounding box
    - Fingertip markers
    - Fingertip labels
    - Current gesture badge
    """

    if not landmarks:
        return frame

    height, width, _ = frame.shape

    # --------------------------------------------------------
    # GET ALL HAND POINTS
    # --------------------------------------------------------

    points = []

    for landmark in landmarks:

        points.append(
            (
                int(landmark.x * width),
                int(landmark.y * height)
            )
        )

    # --------------------------------------------------------
    # HAND BOUNDING BOX
    # --------------------------------------------------------

    if points:

        x_values = [
            point[0]
            for point in points
        ]

        y_values = [
            point[1]
            for point in points
        ]

        x_min = max(
            0,
            min(x_values) - 15
        )

        x_max = min(
            width - 1,
            max(x_values) + 15
        )

        y_min = max(
            0,
            min(y_values) - 15
        )

        y_max = min(
            height - 1,
            max(y_values) + 15
        )

        cv2.rectangle(
            frame,
            (x_min, y_min),
            (x_max, y_max),
            (140, 80, 255),
            2
        )

    # --------------------------------------------------------
    # FINGERTIPS
    # --------------------------------------------------------

    fingertips = {
        4: "Thumb",
        8: "Index",
        12: "Middle",
        16: "Ring",
        20: "Pinky"
    }

    for landmark_id, label in fingertips.items():

        if landmark_id >= len(landmarks):
            continue

        landmark = landmarks[landmark_id]

        x = int(
            landmark.x * width
        )

        y = int(
            landmark.y * height
        )

        # Outer circle

        cv2.circle(
            frame,
            (x, y),
            9,
            (255, 255, 255),
            -1
        )

        # Inner border

        cv2.circle(
            frame,
            (x, y),
            9,
            (255, 0, 180),
            2
        )

        # Label

        cv2.putText(
            frame,
            label,
            (x + 10, y - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

    # --------------------------------------------------------
    # GESTURE BADGE COLOR
    # --------------------------------------------------------

    if gesture == "PAUSED":

        badge_color = (
            0,
            180,
            255
        )

    elif gesture in (
        "NO HAND",
        "Detecting..."
    ):

        badge_color = (
            150,
            150,
            150
        )

    elif gesture == "None":

        badge_color = (
            120,
            120,
            120
        )

    else:

        badge_color = (
            80,
            220,
            120
        )

    # --------------------------------------------------------
    # GESTURE BADGE
    # --------------------------------------------------------

    cv2.rectangle(
        frame,
        (
            width - 330,
            20
        ),
        (
            width - 20,
            68
        ),
        badge_color,
        -1
    )

    cv2.putText(
        frame,
        str(gesture),
        (
            width - 315,
            52
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

    return frame


def draw_status_panel(
    frame,
    camera_status,
    hand_status,
    cursor_status,
    fps,
    paused,
    smoothing,
    scroll_speed
):

    """
    Draw live system information on the camera preview.
    """

    panel_width = 245

    # --------------------------------------------------------
    # TRANSPARENT PANEL
    # --------------------------------------------------------

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (15, 160),
        (
            15 + panel_width,
            335
        ),
        (15, 15, 25),
        -1
    )

    frame[:] = cv2.addWeighted(
        overlay,
        0.78,
        frame,
        0.22,
        0
    )

    # --------------------------------------------------------
    # STATUS VALUES
    # --------------------------------------------------------

    rows = [
        (
            "CAMERA",
            camera_status
        ),
        (
            "HAND",
            hand_status
        ),
        (
            "CURSOR",
            cursor_status
        ),
        (
            "FPS",
            f"{fps:.1f}"
        ),
        (
            "SMOOTHING",
            f"{smoothing:.2f}"
        ),
        (
            "SCROLL",
            str(scroll_speed)
        )
    ]

    y = 188

    # --------------------------------------------------------
    # DRAW ROWS
    # --------------------------------------------------------

    for label, value in rows:

        cv2.putText(
            frame,
            label,
            (30, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (160, 160, 180),
            1,
            cv2.LINE_AA
        )

        cv2.putText(
            frame,
            str(value),
            (130, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

        y += 26

    # --------------------------------------------------------
    # PAUSE INDICATOR
    # --------------------------------------------------------

    if paused:

        cv2.rectangle(
            frame,
            (15, 350),
            (260, 400),
            (40, 40, 180),
            -1
        )

        cv2.putText(
            frame,
            "MOUSE PAUSED",
            (35, 383),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

    return frame


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # LOAD SETTINGS
    # --------------------------------------------------------

    settings = control.read_settings()

    smoothing = float(
        settings.get(
            "smoothing",
            DEFAULT_SMOOTHING
        )
    )

    scroll_speed = int(
        settings.get(
            "scroll_speed",
            DEFAULT_SCROLL_SPEED
        )
    )

    gesture_confirmation_frames = int(
        settings.get(
            "gesture_confirmation_frames",
            DEFAULT_CONFIRM_FRAMES
        )
    )

    # --------------------------------------------------------
    # SAFETY LIMITS
    # --------------------------------------------------------

    smoothing = max(
        0.05,
        min(
            1.0,
            smoothing
        )
    )

    scroll_speed = max(
        1,
        min(
            10,
            scroll_speed
        )
    )

    gesture_confirmation_frames = max(
        1,
        min(
            10,
            gesture_confirmation_frames
        )
    )

    # --------------------------------------------------------
    # START MESSAGE
    # --------------------------------------------------------

    print(
        "========================================"
    )

    print(
        "      AI VIRTUAL MOUSE"
    )

    print(
        "========================================"
    )

    print()

    print(
        "Loaded settings:"
    )

    print(
        f"Smoothing: {smoothing}"
    )

    print(
        f"Scroll Speed: {scroll_speed}"
    )

    print(
        "Gesture Confirmation Frames: "
        f"{gesture_confirmation_frames}"
    )

    print()

    # --------------------------------------------------------
    # CAMERA
    # --------------------------------------------------------

    cap = cv2.VideoCapture(
        CAMERA_INDEX,
        cv2.CAP_DSHOW
    )

    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        FRAME_WIDTH
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        FRAME_HEIGHT
    )

    if not cap.isOpened():

        print(
            "ERROR: Could not open camera."
        )

        control.write_status(
            camera="ERROR",
            hand="READY",
            cursor="READY",
            gesture="None",
            fps=0,
            paused=False
        )

        return

    # --------------------------------------------------------
    # HAND TRACKER
    # --------------------------------------------------------

    tracker = HandTracker(
        max_num_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.7
    )

    # --------------------------------------------------------
    # SCREEN
    # --------------------------------------------------------

    screen_width, screen_height = pyautogui.size()

    # --------------------------------------------------------
    # CURSOR VARIABLES
    # --------------------------------------------------------

    previous_x = 0
    previous_y = 0

    # --------------------------------------------------------
    # GESTURE VARIABLES
    # --------------------------------------------------------

    last_gesture = "None"

    gesture_count = 0

    # --------------------------------------------------------
    # CLICK VARIABLES
    # --------------------------------------------------------

    last_click_time = 0

    last_action_time = 0

    pinch_start_time = None

    pinch_was_active = False

    # --------------------------------------------------------
    # RIGHT CLICK VARIABLES
    # --------------------------------------------------------

    right_pinch_was_active = False

    # --------------------------------------------------------
    # DRAG VARIABLES
    # --------------------------------------------------------

    dragging = False

    drag_start_time = None

    # --------------------------------------------------------
    # PAUSE VARIABLES
    # --------------------------------------------------------

    paused = False

    fist_start_time = None

    fist_active = False

    # --------------------------------------------------------
    # SCROLL VARIABLES
    # --------------------------------------------------------

    previous_index_y = None

    # --------------------------------------------------------
    # FPS VARIABLES
    # --------------------------------------------------------

    previous_time = time.time()

    fps = 0

    # --------------------------------------------------------
    # WINDOW
    # --------------------------------------------------------

    cv2.namedWindow(
        WINDOW_NAME,
        cv2.WINDOW_NORMAL
    )

    cv2.resizeWindow(
        WINDOW_NAME,
        1000,
        700
    )

    print(
        "Virtual mouse started."
    )

    print(
        "Press ESC to exit."
    )

    print()

    # ========================================================
    # MAIN LOOP
    # ========================================================

    try:

        while True:

            # ------------------------------------------------
            # READ UI COMMAND
            # ------------------------------------------------

            command = control.read_command()

            if command == "pause":

                paused = True

                if dragging:

                    pyautogui.mouseUp()

                    dragging = False

                control.clear_command()

            elif command == "resume":

                paused = False

                control.clear_command()

            elif command == "stop":

                control.clear_command()

                break

            # ------------------------------------------------
            # CAMERA FRAME
            # ------------------------------------------------

            success, frame = cap.read()

            if not success:

                control.write_status(
                    camera="ERROR",
                    hand="ERROR",
                    cursor="ERROR",
                    gesture="None",
                    fps=fps,
                    paused=paused
                )

                continue

            # ------------------------------------------------
            # MIRROR CAMERA
            # ------------------------------------------------

            frame = cv2.flip(
                frame,
                1
            )

            # ------------------------------------------------
            # PROCESS HAND
            # ------------------------------------------------

            results = tracker.process_frame(
                frame
            )

            landmarks = tracker.get_landmarks(
                results
            )

            # ------------------------------------------------
            # DRAW MEDIAPIPE LANDMARKS
            # ------------------------------------------------

            tracker.draw_landmarks(
                frame,
                results
            )

            # ------------------------------------------------
            # DEFAULT STATUS
            # ------------------------------------------------

            camera_status = "ACTIVE"

            hand_status = (
                "DETECTED"
                if landmarks
                else "NOT DETECTED"
            )

            cursor_status = (
                "PAUSED"
                if paused
                else "ACTIVE"
            )

            current_gesture = "None"

            # =================================================
            # HAND DETECTED
            # =================================================

            if landmarks:

                # ---------------------------------------------
                # LANDMARKS
                # ---------------------------------------------

                thumb_tip = landmarks[4]

                index_tip = landmarks[8]

                middle_tip = landmarks[12]

                index_mcp = landmarks[5]

                middle_mcp = landmarks[9]

                # ---------------------------------------------
                # PINCH DISTANCES
                # ---------------------------------------------

                thumb_index_distance = distance(
                    thumb_tip,
                    index_tip
                )

                index_middle_distance = distance(
                    index_tip,
                    middle_tip
                )

                # ---------------------------------------------
                # FINGER STATE
                # ---------------------------------------------

                index_up = (
                    index_tip.y
                    < index_mcp.y
                )

                middle_up = (
                    middle_tip.y
                    < middle_mcp.y
                )

                # ---------------------------------------------
                # CLOSED FIST
                # ---------------------------------------------

                fingers_down = (
                    not index_up
                    and not middle_up
                )

                # =================================================
                # PAUSE / RESUME USING FIST
                # =================================================

                if fingers_down:

                    if fist_start_time is None:

                        fist_start_time = time.time()

                    if (
                        time.time()
                        - fist_start_time
                        >= PAUSE_HOLD_TIME
                    ):

                        if not fist_active:

                            paused = not paused

                            fist_active = True

                            if paused and dragging:

                                pyautogui.mouseUp()

                                dragging = False

                else:

                    fist_start_time = None

                    fist_active = False

                # =================================================
                # IF PAUSED
                # =================================================

                if paused:

                    current_gesture = "PAUSED"

                else:

                    # =================================================
                    # CURSOR MOVEMENT
                    # =================================================

                    if index_up:

                        target_x = int(
                            index_tip.x
                            * screen_width
                        )

                        target_y = int(
                            index_tip.y
                            * screen_height
                        )

                        # Smoothing

                        current_x = (
                            previous_x
                            + (
                                target_x
                                - previous_x
                            )
                            * smoothing
                        )

                        current_y = (
                            previous_y
                            + (
                                target_y
                                - previous_y
                            )
                            * smoothing
                        )

                        current_x = int(
                            current_x
                        )

                        current_y = int(
                            current_y
                        )

                        # Keep cursor inside screen

                        current_x = max(
                            0,
                            min(
                                screen_width - 1,
                                current_x
                            )
                        )

                        current_y = max(
                            0,
                            min(
                                screen_height - 1,
                                current_y
                            )
                        )

                        pyautogui.moveTo(
                            current_x,
                            current_y,
                            duration=0
                        )

                        previous_x = current_x

                        previous_y = current_y

                        current_gesture = "MOVE"

                    # =================================================
                    # LEFT CLICK / DRAG
                    # =================================================

                    pinch_active = (
                        thumb_index_distance
                        < CLICK_DISTANCE
                    )

                    if pinch_active:

                        if pinch_start_time is None:

                            pinch_start_time = time.time()

                        pinch_duration = (
                            time.time()
                            - pinch_start_time
                        )

                        # -----------------------------------------
                        # DRAG
                        # -----------------------------------------

                        if (
                            pinch_duration
                            >= DRAG_HOLD_TIME
                        ):

                            if not dragging:

                                pyautogui.mouseDown()

                                dragging = True

                            current_gesture = "DRAG"

                        else:

                            current_gesture = "LEFT CLICK"

                    else:

                        # -----------------------------------------
                        # RELEASE DRAG
                        # -----------------------------------------

                        if dragging:

                            pyautogui.mouseUp()

                            dragging = False

                        # -----------------------------------------
                        # QUICK PINCH CLICK
                        # -----------------------------------------

                        if pinch_was_active:

                            if pinch_start_time is not None:

                                pinch_duration = (
                                    time.time()
                                    - pinch_start_time
                                )

                                if (
                                    pinch_duration
                                    < DRAG_HOLD_TIME
                                ):

                                    now = time.time()

                                    if (
                                        now
                                        - last_click_time
                                        >= CLICK_COOLDOWN
                                    ):

                                        if (
                                            now
                                            - last_action_time
                                            >= ACTION_COOLDOWN
                                        ):

                                            # Double click

                                            if (
                                                now
                                                - last_click_time
                                                <= DOUBLE_CLICK_TIME
                                            ):

                                                pyautogui.doubleClick()

                                            else:

                                                pyautogui.click()

                                            last_click_time = now

                                            last_action_time = now

                            pinch_start_time = None

                    pinch_was_active = pinch_active

                    # =================================================
                    # RIGHT CLICK
                    # =================================================

                    right_pinch_active = (
                        index_middle_distance
                        < RIGHT_CLICK_DISTANCE
                    )

                    if right_pinch_active:

                        current_gesture = "RIGHT CLICK"

                        if not right_pinch_was_active:

                            now = time.time()

                            if (
                                now
                                - last_action_time
                                >= RIGHT_CLICK_BLOCK_TIME
                            ):

                                pyautogui.rightClick()

                                last_action_time = now

                    right_pinch_was_active = (
                        right_pinch_active
                    )

                    # =================================================
                    # SCROLL
                    # =================================================

                    if index_up and middle_up:

                        if previous_index_y is not None:

                            movement = (
                                previous_index_y
                                - index_tip.y
                            )

                            if (
                                abs(movement)
                                > SCROLL_THRESHOLD
                            ):

                                scroll_amount = int(
                                    movement
                                    * 100
                                    * scroll_speed
                                )

                                scroll_amount = max(
                                    -20,
                                    min(
                                        20,
                                        scroll_amount
                                    )
                                )

                                if scroll_amount != 0:

                                    pyautogui.scroll(
                                        scroll_amount
                                    )

                                    current_gesture = (
                                        "SCROLL"
                                    )

                        previous_index_y = (
                            index_tip.y
                        )

                    else:

                        previous_index_y = None

            else:

                # ------------------------------------------------
                # NO HAND
                # ------------------------------------------------

                if dragging:

                    pyautogui.mouseUp()

                    dragging = False

                pinch_start_time = None

                pinch_was_active = False

                right_pinch_was_active = False

                previous_index_y = None

                current_gesture = "NO HAND"

            # =================================================
            # GESTURE CONFIRMATION
            # =================================================

            (
                last_gesture,
                gesture_count,
                confirmed
            ) = confirm_gesture(
                current_gesture,
                last_gesture,
                gesture_count,
                gesture_confirmation_frames
            )

            if not confirmed:

                displayed_gesture = "Detecting..."

            else:

                displayed_gesture = current_gesture

            # =================================================
            # FPS
            # =================================================

            current_time = time.time()

            elapsed = (
                current_time
                - previous_time
            )

            if elapsed > 0:

                fps = (
                    1
                    / elapsed
                )

            previous_time = current_time

            # =================================================
            # STATUS TO UI
            # =================================================

            control.write_status(
                camera=camera_status,
                hand=hand_status,
                cursor=cursor_status,
                gesture=displayed_gesture,
                fps=round(fps, 1),
                paused=paused
            )

            # =================================================
            # ENHANCED CAMERA VISUALIZATION
            # =================================================

            draw_hand_visualization(
                frame,
                landmarks,
                displayed_gesture
            )

            draw_status_panel(
                frame,
                camera_status,
                hand_status,
                cursor_status,
                fps,
                paused,
                smoothing,
                scroll_speed
            )

            # ------------------------------------------------
            # HEADER
            # ------------------------------------------------

            cv2.putText(
                frame,
                "AI VIRTUAL MOUSE",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            cv2.putText(
                frame,
                "ESC = Exit",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (190, 190, 210),
                1,
                cv2.LINE_AA
            )

            # =================================================
            # SHOW FRAME
            # =================================================

            cv2.imshow(
                WINDOW_NAME,
                frame
            )

            # =================================================
            # KEYBOARD
            # =================================================

            key = cv2.waitKey(1) & 0xFF

            # ESC

            if key == 27:

                break

    except KeyboardInterrupt:

        print(
            "Stopped by user."
        )

    except Exception as error:

        print(
            f"Runtime error: {error}"
        )

        control.write_status(
            camera="ERROR",
            hand="ERROR",
            cursor="ERROR",
            gesture="ERROR",
            fps=0,
            paused=False
        )

    finally:

        # ------------------------------------------------
        # SAFETY CLEANUP
        # ------------------------------------------------

        if dragging:

            try:

                pyautogui.mouseUp()

            except Exception:

                pass

        try:

            tracker.close()

        except Exception:

            pass

        try:

            cap.release()

        except Exception:

            pass

        cv2.destroyAllWindows()

        control.clear_command()

        control.clear_status()

        print()

        print(
            "Virtual mouse stopped safely."
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
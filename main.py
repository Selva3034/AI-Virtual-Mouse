import cv2
import pyautogui
import time

from hand_tracker import HandTracker
import config
import control


# =========================================================
# SETTINGS FROM CONFIG.PY
# =========================================================

CAMERA_INDEX = config.CAMERA_INDEX

FRAME_WIDTH = config.FRAME_WIDTH
FRAME_HEIGHT = config.FRAME_HEIGHT

SMOOTHING = config.SMOOTHING

LEFT_CLICK_THRESHOLD = config.LEFT_CLICK_THRESHOLD
RIGHT_CLICK_THRESHOLD = config.RIGHT_CLICK_THRESHOLD

CLICK_COOLDOWN = config.CLICK_COOLDOWN

DOUBLE_CLICK_TIME = config.DOUBLE_CLICK_TIME

DRAG_HOLD_TIME = config.DRAG_HOLD_TIME

SCROLL_THRESHOLD = config.SCROLL_THRESHOLD
SCROLL_SPEED = config.SCROLL_SPEED

PAUSE_HOLD_TIME = config.PAUSE_HOLD_TIME

WINDOW_NAME = config.WINDOW_NAME


# =========================================================
# GESTURE STABILITY SETTINGS
# =========================================================

GESTURE_CONFIRM_FRAMES = getattr(
    config,
    "GESTURE_CONFIRM_FRAMES",
    3
)

GESTURE_ACTION_COOLDOWN = getattr(
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


# =========================================================
# GESTURE CONFIRMATION
# =========================================================

def confirm_gesture(
    gesture_name,
    detected,
    gesture_counts,
    required_frames
):

    if detected:

        gesture_counts[gesture_name] += 1

    else:

        gesture_counts[gesture_name] = 0

    return (
        gesture_counts[gesture_name]
        >= required_frames
    )


# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 55)

    print("AI VIRTUAL MOUSE")

    print("=" * 55)

    print("Starting camera...")

    # =====================================================
    # CAMERA
    # =====================================================

    camera = cv2.VideoCapture(
        CAMERA_INDEX,
        cv2.CAP_DSHOW
    )

    if not camera.isOpened():

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

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        FRAME_WIDTH
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        FRAME_HEIGHT
    )

    print(
        "Camera started successfully."
    )

    # =====================================================
    # HAND TRACKER
    # =====================================================

    hand_tracker = HandTracker(
        max_num_hands=config.MAX_NUM_HANDS,
        detection_confidence=config.DETECTION_CONFIDENCE,
        tracking_confidence=config.TRACKING_CONFIDENCE
    )

    print(
        "MediaPipe hand tracking started."
    )

    # =====================================================
    # SCREEN
    # =====================================================

    screen_width, screen_height = pyautogui.size()

    print(
        f"Screen resolution: "
        f"{screen_width} x {screen_height}"
    )

    # =====================================================
    # CURSOR
    # =====================================================

    previous_x = 0
    previous_y = 0

    # =====================================================
    # CLICK
    # =====================================================

    last_click_time = 0

    last_left_click_time = 0

    left_pinch_active = False

    right_pinch_active = False

    # =====================================================
    # DRAG
    # =====================================================

    pinch_start_time = None

    dragging = False

    # =====================================================
    # SCROLL
    # =====================================================

    previous_scroll_y = None

    scrolling = False

    # =====================================================
    # PAUSE
    # =====================================================

    paused = False

    fist_start_time = None

    pause_gesture_active = False

    # =====================================================
    # GESTURE STABILITY
    # =====================================================

    gesture_counts = {

        "left_click": 0,

        "right_click": 0,

        "scroll": 0

    }

    last_gesture_action_time = 0

    last_scroll_time = 0

    last_left_click_action_time = 0

    last_right_click_action_time = 0

    # =====================================================
    # FPS
    # =====================================================

    fps_start_time = time.time()

    fps_frame_count = 0

    current_fps = 0

    # =====================================================
    # CURRENT GESTURE
    # =====================================================

    current_gesture = "None"

    # =====================================================
    # START STATUS
    # =====================================================

    control.write_status(
        camera="ACTIVE",
        hand="READY",
        cursor="ACTIVE",
        gesture="None",
        fps=0,
        paused=False
    )

    # =====================================================
    # START MESSAGE
    # =====================================================

    print()

    print(
        "AI Virtual Mouse started."
    )

    print()

    print("CONTROLS:")

    print(
        "Move INDEX finger          -> Move cursor"
    )

    print(
        "Quick Thumb + INDEX        -> LEFT CLICK"
    )

    print(
        "Quick pinch twice          -> DOUBLE CLICK"
    )

    print(
        "Hold Thumb + INDEX         -> DRAG"
    )

    print(
        "Release Thumb + INDEX      -> DROP"
    )

    print(
        "INDEX + MIDDLE pinch       -> RIGHT CLICK"
    )

    print(
        "Two fingers extended       -> SCROLL"
    )

    print(
        "Closed fist for 1 sec      -> PAUSE / RESUME"
    )

    print(
        "Press ESC                  -> Exit"
    )

    print()

    # =====================================================
    # CAMERA WINDOW
    # =====================================================

    cv2.namedWindow(
        WINDOW_NAME,
        cv2.WINDOW_NORMAL
    )

    cv2.resizeWindow(
        WINDOW_NAME,
        1000,
        700
    )

    # =====================================================
    # MAIN LOOP
    # =====================================================

    try:

        while True:

            # =================================================
            # FPS
            # =================================================

            fps_frame_count += 1

            fps_elapsed = (
                time.time()
                - fps_start_time
            )

            if fps_elapsed >= 1.0:

                current_fps = (
                    fps_frame_count
                    / fps_elapsed
                )

                fps_frame_count = 0

                fps_start_time = time.time()

            # =================================================
            # UI CONTROL COMMAND
            # =================================================

            command = control.read_command()

            # =================================================
            # UI PAUSE
            # =================================================

            if command == "pause":

                if not paused:

                    paused = True

                    print(
                        "UI: VIRTUAL MOUSE PAUSED"
                    )

                    if dragging:

                        try:

                            pyautogui.mouseUp()

                        except Exception:

                            pass

                        dragging = False

                    left_pinch_active = False

                    right_pinch_active = False

                    pinch_start_time = None

                    previous_scroll_y = None

                    scrolling = False

                    gesture_counts[
                        "left_click"
                    ] = 0

                    gesture_counts[
                        "right_click"
                    ] = 0

                    gesture_counts[
                        "scroll"
                    ] = 0

                control.clear_command()

            # =================================================
            # UI RESUME
            # =================================================

            elif command == "resume":

                if paused:

                    paused = False

                    print(
                        "UI: VIRTUAL MOUSE RESUMED"
                    )

                    left_pinch_active = False

                    right_pinch_active = False

                    pinch_start_time = None

                    previous_scroll_y = None

                    scrolling = False

                    gesture_counts[
                        "left_click"
                    ] = 0

                    gesture_counts[
                        "right_click"
                    ] = 0

                    gesture_counts[
                        "scroll"
                    ] = 0

                control.clear_command()

            # =================================================
            # READ CAMERA
            # =================================================

            success, frame = camera.read()

            if not success:

                print(
                    "Unable to read camera frame."
                )

                control.write_status(
                    camera="ERROR",
                    hand="NOT DETECTED",
                    cursor="PAUSED" if paused else "ACTIVE",
                    gesture="Camera Error",
                    fps=current_fps,
                    paused=paused
                )

                continue

            # =================================================
            # MIRROR CAMERA
            # =================================================

            frame = cv2.flip(
                frame,
                1
            )

            # =================================================
            # HAND DETECTION
            # =================================================

            results = hand_tracker.process_frame(
                frame
            )

            frame = hand_tracker.draw_landmarks(
                frame,
                results
            )

            landmarks = hand_tracker.get_landmarks(
                results
            )

            # =================================================
            # DEFAULT STATUS
            # =================================================

            if landmarks:

                hand_status = "DETECTED"

            else:

                hand_status = "NOT DETECTED"

            # =================================================
            # DEFAULT GESTURE
            # =================================================

            if landmarks:

                current_gesture = "MOVE CURSOR"

            else:

                current_gesture = "None"

            # =================================================
            # HAND DETECTED
            # =================================================

            if landmarks:

                # -------------------------------------------------
                # LANDMARKS
                # -------------------------------------------------

                thumb = landmarks[4]

                index = landmarks[8]

                middle = landmarks[12]

                ring = landmarks[16]

                pinky = landmarks[20]

                index_mcp = landmarks[5]

                middle_mcp = landmarks[9]

                ring_mcp = landmarks[13]

                pinky_mcp = landmarks[17]

                camera_height, camera_width, _ = (
                    frame.shape
                )

                # =================================================
                # FINGER STATES
                # =================================================

                index_folded = (
                    index.y
                    > index_mcp.y
                )

                middle_folded = (
                    middle.y
                    > middle_mcp.y
                )

                ring_folded = (
                    ring.y
                    > ring_mcp.y
                )

                pinky_folded = (
                    pinky.y
                    > pinky_mcp.y
                )

                # =================================================
                # CLOSED FIST
                # =================================================

                fist_detected = (

                    index_folded

                    and middle_folded

                    and ring_folded

                    and pinky_folded

                )

                # =================================================
                # CURRENT TIME
                # =================================================

                current_time = time.time()

                # =================================================
                # FIST PAUSE / RESUME
                # =================================================

                if fist_detected:

                    current_gesture = "CLOSED FIST"

                    if fist_start_time is None:

                        fist_start_time = current_time

                    fist_duration = (
                        current_time
                        - fist_start_time
                    )

                    if (
                        fist_duration
                        >= PAUSE_HOLD_TIME
                        and not pause_gesture_active
                    ):

                        paused = not paused

                        pause_gesture_active = True

                        if paused and dragging:

                            try:

                                pyautogui.mouseUp()

                            except Exception:

                                pass

                            dragging = False

                        left_pinch_active = False

                        right_pinch_active = False

                        pinch_start_time = None

                        previous_scroll_y = None

                        scrolling = False

                        gesture_counts[
                            "left_click"
                        ] = 0

                        gesture_counts[
                            "right_click"
                        ] = 0

                        gesture_counts[
                            "scroll"
                        ] = 0

                        if paused:

                            print(
                                "VIRTUAL MOUSE PAUSED"
                            )

                        else:

                            print(
                                "VIRTUAL MOUSE RESUMED"
                            )

                else:

                    fist_start_time = None

                    pause_gesture_active = False

                # =================================================
                # PAUSED MODE
                # =================================================

                if paused:

                    current_gesture = "PAUSED"

                    overlay = frame.copy()

                    cv2.rectangle(
                        overlay,
                        (0, 0),
                        (
                            camera_width,
                            camera_height
                        ),
                        (0, 0, 0),
                        -1
                    )

                    frame = cv2.addWeighted(
                        overlay,
                        0.35,
                        frame,
                        0.65,
                        0
                    )

                    cv2.putText(
                        frame,
                        "PAUSED",
                        (
                            camera_width // 2 - 100,
                            100
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0, 255, 255),
                        3
                    )

                    cv2.putText(
                        frame,
                        "Use UI or hold CLOSED FIST to resume",
                        (
                            camera_width // 2 - 260,
                            145
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 255),
                        2
                    )

                # =================================================
                # ACTIVE MODE
                # =================================================

                else:

                    # =================================================
                    # INDEX POSITION
                    # =================================================

                    index_x = int(
                        index.x
                        * camera_width
                    )

                    index_y = int(
                        index.y
                        * camera_height
                    )

                    # =================================================
                    # SCREEN POSITION
                    # =================================================

                    target_x = int(
                        index.x
                        * screen_width
                    )

                    target_y = int(
                        index.y
                        * screen_height
                    )

                    # =================================================
                    # SMOOTH CURSOR
                    # =================================================

                    current_x = (

                        previous_x

                        +

                        (
                            target_x
                            - previous_x
                        )
                        * SMOOTHING

                    )

                    current_y = (

                        previous_y

                        +

                        (
                            target_y
                            - previous_y
                        )
                        * SMOOTHING

                    )

                    current_x = int(
                        current_x
                    )

                    current_y = int(
                        current_y
                    )

                    # =================================================
                    # MOVE CURSOR
                    # =================================================

                    pyautogui.moveTo(
                        current_x,
                        current_y,
                        duration=0
                    )

                    previous_x = current_x

                    previous_y = current_y

                    # =================================================
                    # DRAW INDEX
                    # =================================================

                    cv2.circle(
                        frame,
                        (
                            index_x,
                            index_y
                        ),
                        10,
                        (0, 255, 0),
                        -1
                    )

                    # =================================================
                    # THUMB POSITION
                    # =================================================

                    thumb_x = int(
                        thumb.x
                        * camera_width
                    )

                    thumb_y = int(
                        thumb.y
                        * camera_height
                    )

                    # =================================================
                    # MIDDLE POSITION
                    # =================================================

                    middle_x = int(
                        middle.x
                        * camera_width
                    )

                    middle_y = int(
                        middle.y
                        * camera_height
                    )

                    # =================================================
                    # LEFT DISTANCE
                    # =================================================

                    left_distance = (

                        (
                            thumb_x
                            - index_x
                        ) ** 2

                        +

                        (
                            thumb_y
                            - index_y
                        ) ** 2

                    ) ** 0.5

                    # =================================================
                    # RIGHT DISTANCE
                    # =================================================

                    right_distance = (

                        (
                            index_x
                            - middle_x
                        ) ** 2

                        +

                        (
                            index_y
                            - middle_y
                        ) ** 2

                    ) ** 0.5

                    # =================================================
                    # EXTENSION
                    # =================================================

                    index_extended = (
                        index.y
                        < index_mcp.y
                    )

                    middle_extended = (
                        middle.y
                        < middle_mcp.y
                    )

                    # =================================================
                    # SCROLL
                    # =================================================

                    scroll_detected = (

                        index_extended

                        and middle_extended

                        and right_distance
                        > RIGHT_CLICK_THRESHOLD

                        and not left_pinch_active

                        and not dragging

                    )

                    scroll_confirmed = (
                        confirm_gesture(
                            "scroll",
                            scroll_detected,
                            gesture_counts,
                            GESTURE_CONFIRM_FRAMES
                        )
                    )

                    if scroll_confirmed:

                        scrolling = True

                        gesture_counts[
                            "left_click"
                        ] = 0

                        gesture_counts[
                            "right_click"
                        ] = 0

                        if previous_scroll_y is None:

                            previous_scroll_y = (
                                index_y
                                + middle_y
                            ) / 2

                        current_scroll_y = (
                            index_y
                            + middle_y
                        ) / 2

                        scroll_difference = (
                            current_scroll_y
                            - previous_scroll_y
                        )

                        # Scroll down
                        if (
                            scroll_difference
                            > SCROLL_THRESHOLD
                        ):

                            current_gesture = (
                                "SCROLL DOWN"
                            )

                            if (
                                current_time
                                - last_gesture_action_time
                                >= GESTURE_ACTION_COOLDOWN
                            ):

                                pyautogui.scroll(
                                    -SCROLL_SPEED
                                )

                                last_gesture_action_time = (
                                    current_time
                                )

                                last_scroll_time = (
                                    current_time
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

                        # Scroll up
                        elif (
                            scroll_difference
                            < -SCROLL_THRESHOLD
                        ):

                            current_gesture = (
                                "SCROLL UP"
                            )

                            if (
                                current_time
                                - last_gesture_action_time
                                >= GESTURE_ACTION_COOLDOWN
                            ):

                                pyautogui.scroll(
                                    SCROLL_SPEED
                                )

                                last_gesture_action_time = (
                                    current_time
                                )

                                last_scroll_time = (
                                    current_time
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

                            current_gesture = (
                                "SCROLL MODE"
                            )

                            cv2.putText(
                                frame,
                                "SCROLL MODE",
                                (20, 120),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8,
                                (0, 165, 255),
                                2
                            )

                        previous_scroll_y = (
                            current_scroll_y
                        )

                    else:

                        scrolling = False

                        previous_scroll_y = None

                    # =================================================
                    # LEFT PINCH
                    # =================================================

                    left_pinch_detected = (

                        left_distance
                        < LEFT_CLICK_THRESHOLD

                        and not scrolling

                    )

                    left_pinch_confirmed = (
                        confirm_gesture(
                            "left_click",
                            left_pinch_detected,
                            gesture_counts,
                            GESTURE_CONFIRM_FRAMES
                        )
                    )

                    if left_pinch_confirmed:

                        gesture_counts[
                            "right_click"
                        ] = 0

                        if not left_pinch_active:

                            left_pinch_active = True

                            pinch_start_time = (
                                current_time
                            )

                        # =================================================
                        # DRAG START
                        # =================================================

                        if (
                            pinch_start_time
                            is not None

                            and not dragging

                            and (
                                current_time
                                - pinch_start_time
                                >= DRAG_HOLD_TIME
                            )
                        ):

                            pyautogui.mouseDown()

                            dragging = True

                            current_gesture = (
                                "DRAGGING"
                            )

                            print(
                                "DRAG STARTED"
                            )

                        # =================================================
                        # DRAGGING
                        # =================================================

                        if dragging:

                            current_gesture = (
                                "DRAGGING"
                            )

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

                            current_gesture = (
                                "PINCH"
                            )

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

                            current_gesture = (
                                "DROP"
                            )

                            print(
                                "DRAG ENDED"
                            )

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

                            if (
                                pinch_duration
                                < DRAG_HOLD_TIME
                            ):

                                scroll_blocked = (

                                    current_time
                                    - last_scroll_time
                                    < SCROLL_CLICK_BLOCK_TIME

                                )

                                action_allowed = (

                                    current_time
                                    - last_left_click_action_time
                                    >= GESTURE_ACTION_COOLDOWN

                                )

                                if (
                                    not scroll_blocked
                                    and action_allowed
                                ):

                                    # =================================
                                    # DOUBLE CLICK
                                    # =================================

                                    if (
                                        current_time
                                        - last_left_click_time
                                        <= DOUBLE_CLICK_TIME
                                    ):

                                        pyautogui.doubleClick()

                                        current_gesture = (
                                            "DOUBLE CLICK"
                                        )

                                        print(
                                            "DOUBLE CLICK"
                                        )

                                        last_left_click_time = 0

                                        last_left_click_action_time = (
                                            current_time
                                        )

                                        last_gesture_action_time = (
                                            current_time
                                        )

                                        cv2.putText(
                                            frame,
                                            "DOUBLE CLICK",
                                            (20, 120),
                                            cv2.FONT_HERSHEY_SIMPLEX,
                                            1,
                                            (255, 0, 255),
                                            2
                                        )

                                    # =================================
                                    # SINGLE CLICK
                                    # =================================

                                    else:

                                        if (
                                            current_time
                                            - last_click_time
                                            > CLICK_COOLDOWN
                                        ):

                                            pyautogui.click()

                                            current_gesture = (
                                                "LEFT CLICK"
                                            )

                                            print(
                                                "LEFT CLICK"
                                            )

                                            last_click_time = (
                                                current_time
                                            )

                                            last_left_click_time = (
                                                current_time
                                            )

                                            last_left_click_action_time = (
                                                current_time
                                            )

                                            last_gesture_action_time = (
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

                            gesture_counts[
                                "left_click"
                            ] = 0

                    # =================================================
                    # RIGHT CLICK
                    # =================================================

                    right_click_detected = (

                        right_distance
                        < RIGHT_CLICK_THRESHOLD

                        and not left_pinch_active

                        and not dragging

                        and not scrolling

                    )

                    right_click_confirmed = (
                        confirm_gesture(
                            "right_click",
                            right_click_detected,
                            gesture_counts,
                            GESTURE_CONFIRM_FRAMES
                        )
                    )

                    if right_click_confirmed:

                        gesture_counts[
                            "left_click"
                        ] = 0

                        if not right_pinch_active:

                            blocked_after_left = (

                                current_time
                                - last_left_click_action_time
                                < RIGHT_CLICK_BLOCK_TIME

                            )

                            action_allowed = (

                                current_time
                                - last_right_click_action_time
                                >= GESTURE_ACTION_COOLDOWN

                            )

                            if (
                                not blocked_after_left
                                and action_allowed
                            ):

                                pyautogui.rightClick()

                                current_gesture = (
                                    "RIGHT CLICK"
                                )

                                print(
                                    "RIGHT CLICK"
                                )

                                last_click_time = (
                                    current_time
                                )

                                last_right_click_action_time = (
                                    current_time
                                )

                                last_gesture_action_time = (
                                    current_time
                                )

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

                        gesture_counts[
                            "right_click"
                        ] = 0

                    # =================================================
                    # ACTIVE DISPLAY
                    # =================================================

                    cv2.putText(
                        frame,
                        "ACTIVE",
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
            # NO HAND
            # =================================================

            else:

                current_gesture = "None"

                cv2.putText(
                    frame,
                    "NO HAND DETECTED",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

                # Safety release
                if dragging:

                    try:

                        pyautogui.mouseUp()

                    except Exception:

                        pass

                    dragging = False

                    print(
                        "DRAG CANCELLED - HAND LOST"
                    )

                left_pinch_active = False

                right_pinch_active = False

                pinch_start_time = None

                previous_scroll_y = None

                scrolling = False

                fist_start_time = None

                pause_gesture_active = False

                gesture_counts[
                    "left_click"
                ] = 0

                gesture_counts[
                    "right_click"
                ] = 0

                gesture_counts[
                    "scroll"
                ] = 0

            # =================================================
            # SEND REAL-TIME STATUS TO UI
            # =================================================

            control.write_status(
                camera="ACTIVE",
                hand=hand_status,
                cursor=(
                    "PAUSED"
                    if paused
                    else "ACTIVE"
                ),
                gesture=(
                    "PAUSED"
                    if paused
                    else current_gesture
                ),
                fps=current_fps,
                paused=paused
            )

            # =================================================
            # DISPLAY CAMERA
            # =================================================

            cv2.imshow(
                WINDOW_NAME,
                frame
            )

            # =================================================
            # KEYBOARD
            # =================================================

            key = cv2.waitKey(1) & 0xFF

            # =================================================
            # ESC
            # =================================================

            if key == 27:

                print()

                print(
                    "ESC pressed."
                )

                break

    # =========================================================
    # KEYBOARD INTERRUPT
    # =========================================================

    except KeyboardInterrupt:

        print()

        print(
            "Program interrupted."
        )

    # =========================================================
    # ERROR HANDLING
    # =========================================================

    except Exception as error:

        print()

        print(
            "Application Error:"
        )

        print(error)

    # =========================================================
    # CLEANUP
    # =========================================================

    finally:

        # Clear runtime files
        control.clear_command()

        control.clear_status()

        # Safety release
        if dragging:

            try:

                pyautogui.mouseUp()

            except Exception:

                pass

        print(
            "Stopping virtual mouse..."
        )

        try:

            hand_tracker.close()

        except Exception:

            pass

        try:

            camera.release()

        except Exception:

            pass

        cv2.destroyAllWindows()

        print(
            "Resources released successfully."
        )


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    main()
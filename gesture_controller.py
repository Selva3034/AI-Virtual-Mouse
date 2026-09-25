import math
import time

import config


class GestureController:
    """
    Detect and manage hand gestures using MediaPipe landmarks.

    This class is responsible only for gesture recognition and
    gesture timing. Mouse actions are handled elsewhere.
    """

    def __init__(self, config_module=None):

        # Allow another config module to be supplied if required.
        self.config = config_module or config

        # ========================================================
        # CLICK STATE
        # ========================================================

        self.last_left_click_time = 0.0
        self.last_right_click_time = 0.0

        # ========================================================
        # DOUBLE CLICK STATE
        # ========================================================

        self.last_pinch_time = 0.0
        self.pinch_count = 0

        # ========================================================
        # DRAG STATE
        # ========================================================

        self.drag_start_time = None
        self.dragging = False

        # ========================================================
        # PAUSE STATE
        # ========================================================

        self.pause_start_time = None
        self.pause_triggered = False

        # ========================================================
        # GESTURE STATE
        # ========================================================

        self.current_gesture = "NONE"
        self.previous_gesture = "NONE"

        self.gesture_frame_count = 0

        # ========================================================
        # COOLDOWNS
        # ========================================================

        self.left_click_cooldown = getattr(
            self.config,
            "CLICK_COOLDOWN",
            0.5
        )

        self.right_click_cooldown = getattr(
            self.config,
            "RIGHT_CLICK_BLOCK_TIME",
            0.4
        )

        self.gesture_action_cooldown = getattr(
            self.config,
            "GESTURE_ACTION_COOLDOWN",
            0.35
        )

        self.double_click_time = getattr(
            self.config,
            "DOUBLE_CLICK_TIME",
            0.45
        )

        # ========================================================
        # THRESHOLDS
        # ========================================================

        self.pinch_threshold = 0.05

        self.scroll_threshold = getattr(
            self.config,
            "SCROLL_THRESHOLD",
            12
        )

        self.drag_hold_time = getattr(
            self.config,
            "DRAG_HOLD_TIME",
            0.7
        )

        self.pause_hold_time = getattr(
            self.config,
            "PAUSE_HOLD_TIME",
            1.0
        )

        self.confirmation_frames = getattr(
            self.config,
            "GESTURE_CONFIRM_FRAMES",
            3
        )

    # ============================================================
    # BASIC LANDMARK HELPERS
    # ============================================================

    @staticmethod
    def distance(point1, point2):
        """
        Calculate Euclidean distance between two MediaPipe
        landmarks.
        """

        if point1 is None or point2 is None:
            return float("inf")

        return math.sqrt(
            (point1.x - point2.x) ** 2
            + (point1.y - point2.y) ** 2
        )

    @staticmethod
    def is_finger_extended(landmarks, tip_id, pip_id):
        """
        Check whether a finger is extended.

        For index, middle, ring and pinky fingers,
        a smaller y-coordinate means the fingertip is higher.
        """

        if not landmarks:
            return False

        if (
            tip_id >= len(landmarks)
            or pip_id >= len(landmarks)
        ):
            return False

        return (
            landmarks[tip_id].y
            < landmarks[pip_id].y
        )

    # ============================================================
    # FINGER STATES
    # ============================================================

    def get_finger_states(self, landmarks):
        """
        Return the state of the four main fingers.

        Returns:
            {
                "index": True/False,
                "middle": True/False,
                "ring": True/False,
                "pinky": True/False
            }
        """

        if not landmarks or len(landmarks) < 21:
            return {
                "index": False,
                "middle": False,
                "ring": False,
                "pinky": False
            }

        return {
            "index": self.is_finger_extended(
                landmarks, 8, 6
            ),

            "middle": self.is_finger_extended(
                landmarks, 12, 10
            ),

            "ring": self.is_finger_extended(
                landmarks, 16, 14
            ),

            "pinky": self.is_finger_extended(
                landmarks, 20, 18
            )
        }

    # ============================================================
    # PINCH
    # ============================================================

    def is_pinch(self, landmarks):
        """Detect thumb + index finger pinch."""

        if not landmarks or len(landmarks) < 21:
            return False

        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        distance = self.distance(
            thumb_tip,
            index_tip
        )

        return distance < self.pinch_threshold

    # ============================================================
    # RIGHT CLICK
    # ============================================================

    def is_right_click_gesture(self, landmarks):
        """
        Right-click gesture:

        Index  -> extended
        Middle -> extended
        Ring   -> folded
        Pinky  -> folded
        """

        states = self.get_finger_states(landmarks)

        return (
            states["index"]
            and states["middle"]
            and not states["ring"]
            and not states["pinky"]
        )

    # ============================================================
    # TWO FINGER GESTURE
    # ============================================================

    def is_two_finger_gesture(self, landmarks):
        """
        Detect two-finger gesture.

        Index and middle are extended while ring and pinky
        remain folded.
        """

        states = self.get_finger_states(landmarks)

        return (
            states["index"]
            and states["middle"]
            and not states["ring"]
            and not states["pinky"]
        )

    # ============================================================
    # FIST
    # ============================================================

    def is_fist(self, landmarks):
        """Detect a closed fist."""

        states = self.get_finger_states(landmarks)

        return not (
            states["index"]
            or states["middle"]
            or states["ring"]
            or states["pinky"]
        )

    # ============================================================
    # OPEN HAND
    # ============================================================

    def is_open_hand(self, landmarks):
        """Detect an open hand."""

        states = self.get_finger_states(landmarks)

        return (
            states["index"]
            and states["middle"]
            and states["ring"]
            and states["pinky"]
        )

    # ============================================================
    # LEFT CLICK COOLDOWN
    # ============================================================

    def can_left_click(self):
        """Check whether another left click is allowed."""

        current_time = time.time()

        if (
            current_time - self.last_left_click_time
            >= self.left_click_cooldown
        ):
            self.last_left_click_time = current_time
            return True

        return False

    # ============================================================
    # RIGHT CLICK COOLDOWN
    # ============================================================

    def can_right_click(self):
        """Check whether another right click is allowed."""

        current_time = time.time()

        if (
            current_time - self.last_right_click_time
            >= self.right_click_cooldown
        ):
            self.last_right_click_time = current_time
            return True

        return False

    # ============================================================
    # GESTURE ACTION COOLDOWN
    # ============================================================

    def can_perform_action(self):
        """
        Check whether enough time has passed since the
        previous gesture action.
        """

        current_time = time.time()

        last_action = max(
            self.last_left_click_time,
            self.last_right_click_time
        )

        return (
            current_time - last_action
            >= self.gesture_action_cooldown
        )

    # ============================================================
    # DRAG
    # ============================================================

    def update_drag_state(self, landmarks):
        """
        Update drag state based on a thumb + index pinch.

        Returns:
            True  -> drag is active
            False -> drag is inactive
        """

        current_time = time.time()

        pinch = self.is_pinch(landmarks)

        if not pinch:

            self.drag_start_time = None
            self.dragging = False

            return False

        if self.drag_start_time is None:

            self.drag_start_time = current_time

            return False

        held_time = (
            current_time -
            self.drag_start_time
        )

        if held_time >= self.drag_hold_time:

            self.dragging = True

        return self.dragging

    # ============================================================
    # PAUSE / RESUME
    # ============================================================

    def update_pause_state(self, landmarks):
        """
        Detect a closed fist held for the configured duration.

        Returns:
            True only when the pause/resume action should trigger.
        """

        current_time = time.time()

        if not self.is_fist(landmarks):

            self.pause_start_time = None
            self.pause_triggered = False

            return False

        if self.pause_start_time is None:

            self.pause_start_time = current_time
            self.pause_triggered = False

            return False

        held_time = (
            current_time -
            self.pause_start_time
        )

        if (
            held_time >= self.pause_hold_time
            and not self.pause_triggered
        ):

            self.pause_triggered = True

            return True

        return False

    # ============================================================
    # DOUBLE CLICK
    # ============================================================

    def detect_double_click(self, landmarks):
        """
        Detect two quick pinch gestures.

        Returns:
            True when a double-click gesture is detected.
        """

        if not self.is_pinch(landmarks):
            return False

        current_time = time.time()

        # First pinch.
        if self.last_pinch_time == 0:

            self.last_pinch_time = current_time
            self.pinch_count = 1

            return False

        elapsed = (
            current_time -
            self.last_pinch_time
        )

        # Second pinch within allowed time.
        if elapsed <= self.double_click_time:

            self.pinch_count += 1
            self.last_pinch_time = current_time

            if self.pinch_count >= 2:

                self.pinch_count = 0
                self.last_pinch_time = 0

                return True

        else:

            # Start a new sequence.
            self.pinch_count = 1
            self.last_pinch_time = current_time

        return False

    # ============================================================
    # RAW GESTURE DETECTION
    # ============================================================

    def detect_gesture(self, landmarks):
        """
        Return the currently detected raw gesture.

        Possible values:

            MOVE
            LEFT_CLICK
            RIGHT_CLICK
            DOUBLE_CLICK
            DRAG
            SCROLL
            PAUSE
            NONE
        """

        if landmarks is None:
            return "NONE"

        if not landmarks or len(landmarks) < 21:
            return "NONE"

        # --------------------------------------------------------
        # FIST / PAUSE
        # --------------------------------------------------------

        if self.is_fist(landmarks):

            return "PAUSE"

        # --------------------------------------------------------
        # RIGHT CLICK
        # --------------------------------------------------------

        if self.is_right_click_gesture(landmarks):

            return "RIGHT_CLICK"

        # --------------------------------------------------------
        # DRAG
        # --------------------------------------------------------

        if self.update_drag_state(landmarks):

            return "DRAG"

        # --------------------------------------------------------
        # DOUBLE CLICK
        # --------------------------------------------------------

        if self.detect_double_click(landmarks):

            return "DOUBLE_CLICK"

        # --------------------------------------------------------
        # LEFT CLICK
        # --------------------------------------------------------

        if self.is_pinch(landmarks):

            return "LEFT_CLICK"

        # --------------------------------------------------------
        # TWO FINGER / SCROLL
        # --------------------------------------------------------

        if self.is_two_finger_gesture(landmarks):

            return "SCROLL"

        # --------------------------------------------------------
        # NORMAL MOVEMENT
        # --------------------------------------------------------

        states = self.get_finger_states(landmarks)

        if states["index"]:

            return "MOVE"

        return "NONE"

    # ============================================================
    # GESTURE CONFIRMATION
    # ============================================================

    def get_confirmed_gesture(self, landmarks):
        """
        Detect a gesture and require it to remain stable for
        the configured number of frames.

        Returns:
            Confirmed gesture name.
        """

        detected_gesture = self.detect_gesture(
            landmarks
        )

        if detected_gesture == self.current_gesture:

            self.gesture_frame_count += 1

        else:

            self.current_gesture = detected_gesture
            self.gesture_frame_count = 1

        if (
            self.gesture_frame_count
            >= self.confirmation_frames
        ):

            self.previous_gesture = (
                self.current_gesture
            )

            return self.current_gesture

        return self.previous_gesture

    # ============================================================
    # CURRENT GESTURE
    # ============================================================

    def get_current_gesture(self):
        """Return the currently tracked gesture."""

        return self.current_gesture

    # ============================================================
    # RESET
    # ============================================================

    def reset(self):
        """Reset all gesture state."""

        self.last_left_click_time = 0.0
        self.last_right_click_time = 0.0

        self.last_pinch_time = 0.0
        self.pinch_count = 0

        self.drag_start_time = None
        self.dragging = False

        self.pause_start_time = None
        self.pause_triggered = False

        self.current_gesture = "NONE"
        self.previous_gesture = "NONE"

        self.gesture_frame_count = 0
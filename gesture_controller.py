import math
import time


class GestureController:
    """Detect hand gestures using MediaPipe hand landmarks."""

    def __init__(self, config=None):
        self.config = config

        # Prevent repeated clicks while a gesture is held.
        self.last_left_click_time = 0
        self.last_right_click_time = 0

        self.left_click_cooldown = 0.6
        self.right_click_cooldown = 0.8

    @staticmethod
    def distance(point1, point2):
        """Calculate Euclidean distance between two landmarks."""

        return math.sqrt(
            (point1.x - point2.x) ** 2
            + (point1.y - point2.y) ** 2
        )

    @staticmethod
    def is_finger_extended(landmarks, tip_id, pip_id):
        """
        Check whether a finger is extended.

        For the index/middle/ring/pinky fingers,
        a smaller y-coordinate means the fingertip is higher.
        """

        return landmarks[tip_id].y < landmarks[pip_id].y

    def is_pinch(self, landmarks):
        """Detect thumb + index finger pinch."""

        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        distance = self.distance(thumb_tip, index_tip)

        return distance < 0.05

    def is_right_click_gesture(self, landmarks):
        """
        Right-click gesture:

        Index  -> extended
        Middle -> extended
        Ring   -> folded
        Pinky  -> folded
        """

        index_extended = self.is_finger_extended(
            landmarks, 8, 6
        )

        middle_extended = self.is_finger_extended(
            landmarks, 12, 10
        )

        ring_folded = not self.is_finger_extended(
            landmarks, 16, 14
        )

        pinky_folded = not self.is_finger_extended(
            landmarks, 20, 18
        )

        return (
            index_extended
            and middle_extended
            and ring_folded
            and pinky_folded
        )

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

    def detect_gesture(self, landmarks):
        """
        Return the currently detected gesture.

        Possible values:
        MOVE
        LEFT_CLICK
        RIGHT_CLICK
        NONE
        """

        if landmarks is None:
            return "NONE"

        # Right click gets priority over normal movement.
        if self.is_right_click_gesture(landmarks):
            return "RIGHT_CLICK"

        # Left click.
        if self.is_pinch(landmarks):
            return "LEFT_CLICK"

        # Otherwise normal cursor movement.
        return "MOVE"
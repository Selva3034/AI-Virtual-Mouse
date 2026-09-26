import cv2
import mediapipe as mp


class HandTracker:
    """
    Handle MediaPipe hand detection, landmark extraction,
    visualization and hand information.
    """

    def __init__(
        self,
        max_num_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.7
    ):
        # ========================================================
        # MEDIAPIPE SETUP
        # ========================================================

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.max_num_hands = max_num_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

        # ========================================================
        # FINGERTIPS
        # ========================================================

        self.fingertip_ids = {
            4: "Thumb",
            8: "Index",
            12: "Middle",
            16: "Ring",
            20: "Pinky"
        }

        self.closed = False

    # ============================================================
    # PROCESS FRAME
    # ============================================================

    def process_frame(self, frame):
        """
        Process a BGR OpenCV frame using MediaPipe.

        Returns:
            MediaPipe hand detection results.
        """

        if frame is None:
            return None

        if self.closed:
            return None

        try:
            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # Prevent MediaPipe from modifying the input image.
            rgb.flags.writeable = False

            results = self.hands.process(rgb)

            return results

        except Exception as error:
            print(
                f"Hand tracking error: {error}"
            )

            return None

    # ============================================================
    # HAND DETECTION
    # ============================================================

    def has_hand(self, results):
        """
        Return True when at least one hand is detected.
        """

        if results is None:
            return False

        if not hasattr(
            results,
            "multi_hand_landmarks"
        ):
            return False

        return bool(
            results.multi_hand_landmarks
        )

    # ============================================================
    # HAND COUNT
    # ============================================================

    def get_hand_count(self, results):
        """Return the number of detected hands."""

        if results is None:
            return 0

        if not hasattr(
            results,
            "multi_hand_landmarks"
        ):
            return 0

        if not results.multi_hand_landmarks:
            return 0

        return len(
            results.multi_hand_landmarks
        )

    # ============================================================
    # DRAW LANDMARKS
    # ============================================================

    def draw_landmarks(self, frame, results):
        """
        Draw MediaPipe landmarks and connections
        on the OpenCV frame.
        """

        if frame is None:
            return frame

        if not self.has_hand(results):
            return frame

        try:
            for hand_landmarks in (
                results.multi_hand_landmarks
            ):

                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        except Exception as error:
            print(
                f"Landmark drawing error: {error}"
            )

        return frame

    # ============================================================
    # GET LANDMARKS
    # ============================================================

    def get_landmarks(self, results):
        """
        Return landmarks from the first detected hand.

        Returns:
            List of 21 MediaPipe landmarks.
            Empty list when no hand is detected.
        """

        if not self.has_hand(results):
            return []

        return results.multi_hand_landmarks[0].landmark

    # ============================================================
    # GET LANDMARK
    # ============================================================

    def get_landmark(self, results, landmark_id):
        """
        Return one landmark using its MediaPipe ID.
        """

        landmarks = self.get_landmarks(
            results
        )

        if not landmarks:
            return None

        if (
            landmark_id < 0
            or landmark_id >= len(landmarks)
        ):
            return None

        return landmarks[landmark_id]

    # ============================================================
    # GET LANDMARK PIXEL POSITION
    # ============================================================

    def get_landmark_position(
        self,
        frame,
        results,
        landmark_id
    ):
        """
        Return a landmark's pixel coordinates.

        Returns:
            (x, y) or None
        """

        if frame is None:
            return None

        point = self.get_landmark(
            results,
            landmark_id
        )

        if point is None:
            return None

        height, width = frame.shape[:2]

        x = int(
            point.x * width
        )

        y = int(
            point.y * height
        )

        x = max(
            0,
            min(width - 1, x)
        )

        y = max(
            0,
            min(height - 1, y)
        )

        return x, y

    # ============================================================
    # GET FINGERTIP POSITIONS
    # ============================================================

    def get_fingertip_positions(
        self,
        frame,
        results
    ):
        """
        Return pixel positions of all fingertips.

        Returns:
            {
                "Thumb": (x, y),
                "Index": (x, y),
                ...
            }
        """

        positions = {}

        if frame is None:
            return positions

        for landmark_id, label in (
            self.fingertip_ids.items()
        ):

            position = self.get_landmark_position(
                frame,
                results,
                landmark_id
            )

            if position is not None:
                positions[label] = position

        return positions

    # ============================================================
    # DRAW FINGERTIP LABELS
    # ============================================================

    def draw_fingertip_labels(
        self,
        frame,
        results
    ):
        """Draw labels near each detected fingertip."""

        if frame is None:
            return frame

        landmarks = self.get_landmarks(
            results
        )

        if not landmarks:
            return frame

        height, width = frame.shape[:2]

        for landmark_id, label in (
            self.fingertip_ids.items()
        ):

            if landmark_id >= len(landmarks):
                continue

            point = landmarks[
                landmark_id
            ]

            x = int(
                point.x * width
            )

            y = int(
                point.y * height
            )

            cv2.putText(
                frame,
                label,
                (x + 5, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )

        return frame

    # ============================================================
    # DRAW FINGERTIP MARKERS
    # ============================================================

    def draw_fingertips(
        self,
        frame,
        results,
        radius=6
    ):
        """Draw circles on all detected fingertips."""

        if frame is None:
            return frame

        positions = self.get_fingertip_positions(
            frame,
            results
        )

        for position in positions.values():

            x, y = position

            cv2.circle(
                frame,
                (x, y),
                radius,
                (0, 255, 255),
                -1
            )

        return frame

    # ============================================================
    # HAND BOUNDING BOX
    # ============================================================

    def get_bounding_box(
        self,
        frame,
        results
    ):
        """
        Return the bounding box of the first detected hand.

        Returns:
            (x_min, y_min, x_max, y_max)
            or None when no hand exists.
        """

        if frame is None:
            return None

        landmarks = self.get_landmarks(
            results
        )

        if not landmarks:
            return None

        height, width = frame.shape[:2]

        x_values = [
            int(point.x * width)
            for point in landmarks
        ]

        y_values = [
            int(point.y * height)
            for point in landmarks
        ]

        x_min = max(
            0,
            min(x_values)
        )

        y_min = max(
            0,
            min(y_values)
        )

        x_max = min(
            width - 1,
            max(x_values)
        )

        y_max = min(
            height - 1,
            max(y_values)
        )

        return (
            x_min,
            y_min,
            x_max,
            y_max
        )

    # ============================================================
    # DRAW HAND BOUNDING BOX
    # ============================================================

    def draw_bounding_box(
        self,
        frame,
        results,
        padding=15
    ):
        """Draw a bounding box around the detected hand."""

        if frame is None:
            return frame

        box = self.get_bounding_box(
            frame,
            results
        )

        if box is None:
            return frame

        height, width = frame.shape[:2]

        x_min, y_min, x_max, y_max = box

        x_min = max(
            0,
            x_min - padding
        )

        y_min = max(
            0,
            y_min - padding
        )

        x_max = min(
            width - 1,
            x_max + padding
        )

        y_max = min(
            height - 1,
            y_max + padding
        )

        cv2.rectangle(
            frame,
            (x_min, y_min),
            (x_max, y_max),
            (0, 255, 255),
            2
        )

        return frame

    # ============================================================
    # HAND LABEL
    # ============================================================

    def get_hand_label(
        self,
        results
    ):
        """
        Return MediaPipe's detected hand label.

        Example:
            Left
            Right
        """

        if results is None:
            return "Unknown"

        if not hasattr(
            results,
            "multi_handedness"
        ):
            return "Unknown"

        if not results.multi_handedness:
            return "Unknown"

        try:
            classification = (
                results
                .multi_handedness[0]
                .classification[0]
            )

            return classification.label

        except Exception:
            return "Unknown"

    # ============================================================
    # HAND CONFIDENCE
    # ============================================================

    def get_hand_confidence(
        self,
        results
    ):
        """Return MediaPipe hand detection confidence."""

        if results is None:
            return 0.0

        if not hasattr(
            results,
            "multi_handedness"
        ):
            return 0.0

        if not results.multi_handedness:
            return 0.0

        try:
            score = (
                results
                .multi_handedness[0]
                .classification[0]
                .score
            )

            return round(
                float(score),
                3
            )

        except Exception:
            return 0.0

    # ============================================================
    # DRAW HAND INFORMATION
    # ============================================================

    def draw_hand_info(
        self,
        frame,
        results
    ):
        """
        Draw basic hand information on the frame.
        """

        if frame is None:
            return frame

        if not self.has_hand(results):
            return frame

        label = self.get_hand_label(
            results
        )

        confidence = self.get_hand_confidence(
            results
        )

        text = (
            f"{label} Hand  "
            f"{confidence * 100:.0f}%"
        )

        cv2.putText(
            frame,
            text,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        return frame

    # ============================================================
    # CLOSE
    # ============================================================

    def close(self):
        """Release MediaPipe resources."""

        if self.closed:
            return

        try:
            self.hands.close()

        except Exception as error:
            print(
                f"Hand tracker cleanup error: {error}"
            )

        finally:
            self.closed = True
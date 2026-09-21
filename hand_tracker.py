import cv2
import mediapipe as mp


class HandTracker:
    def __init__(
        self,
        max_num_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.7
    ):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

    def process_frame(self, frame):
        """Process a BGR OpenCV frame."""

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        return results

    def draw_landmarks(self, frame, results):
        """Draw detected hand landmarks."""

        if results is None:
            return frame

        if hasattr(results, "multi_hand_landmarks"):
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )

        return frame

    def get_landmarks(self, results):
        """Return the first detected hand landmarks."""

        if results is None:
            return []

        if not hasattr(results, "multi_hand_landmarks"):
            return []

        if not results.multi_hand_landmarks:
            return []

        hand = results.multi_hand_landmarks[0]

        return hand.landmark

    def get_landmark(self, results, landmark_id):
        """Return one landmark."""

        landmarks = self.get_landmarks(results)

        if not landmarks:
            return None

        if landmark_id < 0 or landmark_id >= len(landmarks):
            return None

        return landmarks[landmark_id]

    def draw_fingertip_labels(self, frame, results):
        """Draw fingertip labels."""

        landmarks = self.get_landmarks(results)

        if not landmarks:
            return frame

        h, w, _ = frame.shape

        fingertips = {
            4: "Thumb",
            8: "Index",
            12: "Middle",
            16: "Ring",
            20: "Pinky"
        }

        for landmark_id, label in fingertips.items():

            point = landmarks[landmark_id]

            x = int(point.x * w)
            y = int(point.y * h)

            cv2.putText(
                frame,
                label,
                (x + 5, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )

        return frame

    def close(self):
        self.hands.close()
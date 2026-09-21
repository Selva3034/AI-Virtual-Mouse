import cv2


class Camera:
    """Handle webcam initialization, frame capture and cleanup."""

    def __init__(self, camera_index=0, width=640, height=480):
        self.camera_index = camera_index

        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            raise RuntimeError(
                f"Unable to open camera with index {camera_index}."
            )

        # Set camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        print("Camera started successfully.")

    def read(self):
        """Capture and return one camera frame."""

        ret, frame = self.cap.read()

        return ret, frame

    def release(self):
        """Release the webcam."""

        if self.cap is not None:
            self.cap.release()

    def close_windows(self):
        """Close all OpenCV windows."""

        cv2.destroyAllWindows()
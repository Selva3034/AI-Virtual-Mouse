import cv2
import time


class Camera:
    """
    Handle webcam initialization, frame capture,
    camera information and cleanup.
    """

    def __init__(
        self,
        camera_index=0,
        width=640,
        height=480,
        fps=30
    ):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.target_fps = fps

        self.cap = None

        self.last_frame_time = None
        self.current_fps = 0.0

        self._open_camera()

    # ============================================================
    # CAMERA INITIALIZATION
    # ============================================================

    def _open_camera(self):
        """Open the webcam using a suitable backend."""

        # Try DirectShow first on Windows.
        self.cap = cv2.VideoCapture(
            self.camera_index,
            cv2.CAP_DSHOW
        )

        # Fallback to OpenCV default backend.
        if not self.cap.isOpened():
            self.cap.release()

            self.cap = cv2.VideoCapture(
                self.camera_index
            )

        # Final validation.
        if not self.cap.isOpened():
            self.cap = None

            raise RuntimeError(
                f"Unable to open camera with index "
                f"{self.camera_index}."
            )

        # ========================================================
        # CAMERA SETTINGS
        # ========================================================

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            self.width
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            self.height
        )

        self.cap.set(
            cv2.CAP_PROP_FPS,
            self.target_fps
        )

        # Read the actual resolution accepted by the camera.
        self.width = int(
            self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        self.height = int(
            self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        print(
            f"Camera started successfully "
            f"(Index: {self.camera_index}, "
            f"Resolution: {self.width}x{self.height})"
        )

    # ============================================================
    # READ FRAME
    # ============================================================

    def read(self):
        """
        Capture and return one camera frame.

        Returns:
            tuple:
                ret   -> True if frame was captured
                frame -> OpenCV frame or None
        """

        if self.cap is None:
            return False, None

        if not self.cap.isOpened():
            return False, None

        ret, frame = self.cap.read()

        if not ret or frame is None:
            return False, None

        self._update_fps()

        return True, frame

    # ============================================================
    # FPS CALCULATION
    # ============================================================

    def _update_fps(self):
        """Calculate approximate camera capture FPS."""

        current_time = time.perf_counter()

        if self.last_frame_time is not None:

            elapsed = (
                current_time -
                self.last_frame_time
            )

            if elapsed > 0:
                instant_fps = 1.0 / elapsed

                # Smooth FPS value.
                if self.current_fps == 0:
                    self.current_fps = instant_fps
                else:
                    self.current_fps = (
                        self.current_fps * 0.9
                        + instant_fps * 0.1
                    )

        self.last_frame_time = current_time

    # ============================================================
    # CAMERA STATUS
    # ============================================================

    def is_opened(self):
        """Return True when the camera is currently available."""

        return (
            self.cap is not None
            and self.cap.isOpened()
        )

    # ============================================================
    # CAMERA FPS
    # ============================================================

    def get_fps(self):
        """Return the calculated camera FPS."""

        return round(
            self.current_fps,
            1
        )

    # ============================================================
    # CAMERA RESOLUTION
    # ============================================================

    def get_resolution(self):
        """Return the current camera resolution."""

        return (
            self.width,
            self.height
        )

    # ============================================================
    # CAMERA INDEX
    # ============================================================

    def get_camera_index(self):
        """Return the active camera index."""

        return self.camera_index

    # ============================================================
    # RELEASE
    # ============================================================

    def release(self):
        """Safely release the webcam."""

        if self.cap is not None:

            if self.cap.isOpened():
                self.cap.release()

            self.cap = None

        self.current_fps = 0.0
        self.last_frame_time = None

        print("Camera released.")

    # ============================================================
    # CLOSE WINDOWS
    # ============================================================

    def close_windows(self):
        """Close all OpenCV windows."""

        cv2.destroyAllWindows()

    # ============================================================
    # FULL CLEANUP
    # ============================================================

    def close(self):
        """Release camera and close OpenCV windows."""

        self.release()
        self.close_windows()

        print("Camera cleanup completed.")

    # ============================================================
    # CONTEXT MANAGER
    # ============================================================

    def __enter__(self):
        """Allow usage with a 'with Camera()' statement."""

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):
        """Automatically clean up the camera."""

        self.close()
# ============================================================
# AI VIRTUAL MOUSE CONFIGURATION
# ============================================================
"""
Central configuration file for the AI Virtual Mouse.

Keep application-wide settings here so that individual
modules do not need to contain hard-coded values.
"""


# ============================================================
# CAMERA
# ============================================================

# Default webcam index.
CAMERA_INDEX = 0

# Camera resolution.
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Target camera FPS.
CAMERA_FPS = 30

# OpenCV camera backend.
# CAP_DSHOW is preferred on Windows.
USE_DIRECTSHOW = True


# ============================================================
# MEDIAPIPE
# ============================================================

# Maximum number of hands to detect.
MAX_NUM_HANDS = 1

# Minimum confidence required for initial hand detection.
DETECTION_CONFIDENCE = 0.7

# Minimum confidence required for hand tracking.
TRACKING_CONFIDENCE = 0.7


# ============================================================
# CURSOR
# ============================================================

# Cursor smoothing factor.
#
# Lower value  -> smoother/slower movement
# Higher value -> faster/more responsive movement
SMOOTHING = 0.25


# ============================================================
# CLICK
# ============================================================

# Distance threshold between thumb and index finger
# for left-click detection.
LEFT_CLICK_THRESHOLD = 35

# Distance threshold between thumb and middle/index
# fingers for right-click detection.
RIGHT_CLICK_THRESHOLD = 35

# Minimum time between click actions.
CLICK_COOLDOWN = 0.5


# ============================================================
# DOUBLE CLICK
# ============================================================

# Maximum time between two quick clicks to recognize
# a double click.
DOUBLE_CLICK_TIME = 0.45


# ============================================================
# DRAG
# ============================================================

# Time thumb + index finger must remain held together
# before drag mode is activated.
DRAG_HOLD_TIME = 0.7


# ============================================================
# SCROLL
# ============================================================

# Minimum finger movement required to trigger scrolling.
SCROLL_THRESHOLD = 12

# Scroll speed multiplier.
SCROLL_SPEED = 2


# ============================================================
# PAUSE / RESUME
# ============================================================

# Time a closed fist must be held before toggling
# pause/resume.
PAUSE_HOLD_TIME = 1.0


# ============================================================
# GESTURE STABILITY
# ============================================================

# Number of consecutive frames required before a gesture
# is considered stable.
GESTURE_CONFIRM_FRAMES = 3

# Minimum time between gesture actions.
GESTURE_ACTION_COOLDOWN = 0.35

# Prevent accidental click immediately after scrolling.
SCROLL_CLICK_BLOCK_TIME = 0.50

# Prevent accidental right-click immediately after left-click.
RIGHT_CLICK_BLOCK_TIME = 0.40


# ============================================================
# PERFORMANCE
# ============================================================

# Target display FPS for the application.
TARGET_FPS = 30

# Maximum FPS value used by the UI performance bar.
MAX_DISPLAY_FPS = 60


# ============================================================
# SAFETY
# ============================================================

# Emergency keyboard key used to stop the application.
EXIT_KEY = 27  # ESC

# Release mouse buttons automatically when the application
# stops, pauses, or loses hand tracking.
AUTO_RELEASE_MOUSE = True


# ============================================================
# WINDOW
# ============================================================

WINDOW_NAME = "AI Virtual Mouse"

# Default OpenCV window dimensions.
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# Allow the OpenCV window to be resized.
RESIZABLE_WINDOW = True


# ============================================================
# VISUALIZATION
# ============================================================

# Show hand landmarks.
SHOW_HAND_LANDMARKS = True

# Show fingertip labels.
SHOW_FINGERTIP_LABELS = True

# Show hand bounding box.
SHOW_HAND_BOUNDING_BOX = True

# Show gesture information on the camera frame.
SHOW_GESTURE_BADGE = True

# Show application status panel.
SHOW_STATUS_PANEL = True


# ============================================================
# UI
# ============================================================

# Dashboard update interval in milliseconds.
UI_UPDATE_INTERVAL = 300

# Main UI window size.
UI_WIDTH = 1250
UI_HEIGHT = 750

# Minimum UI window size.
UI_MIN_WIDTH = 1050
UI_MIN_HEIGHT = 650


# ============================================================
# DEBUG
# ============================================================

# Enable additional console information.
DEBUG_MODE = False

# Print camera information when initialized.
PRINT_CAMERA_INFO = True

# Print gesture changes to th
# =========================================================
# AI VIRTUAL MOUSE CONFIGURATION
# =========================================================


# =========================================================
# CAMERA
# =========================================================

CAMERA_INDEX = 0

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720


# =========================================================
# MEDIAPIPE
# =========================================================

MAX_NUM_HANDS = 1

DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.7


# =========================================================
# CURSOR
# =========================================================

SMOOTHING = 0.25


# =========================================================
# CLICK
# =========================================================

LEFT_CLICK_THRESHOLD = 35

RIGHT_CLICK_THRESHOLD = 35

CLICK_COOLDOWN = 0.5


# =========================================================
# DOUBLE CLICK
# =========================================================

DOUBLE_CLICK_TIME = 0.45


# =========================================================
# DRAG
# =========================================================

DRAG_HOLD_TIME = 0.7


# =========================================================
# SCROLL
# =========================================================

SCROLL_THRESHOLD = 12

SCROLL_SPEED = 2


# =========================================================
# PAUSE / RESUME
# =========================================================

PAUSE_HOLD_TIME = 1.0


# =========================================================
# APPLICATION
# =========================================================

WINDOW_NAME = "AI Virtual Mouse"

# =========================================================
# GESTURE STABILITY SETTINGS
# =========================================================

# Number of consecutive frames required
# before confirming a gesture
GESTURE_CONFIRM_FRAMES = 3

# Minimum time between gesture actions
GESTURE_ACTION_COOLDOWN = 0.35

# Prevent accidental click immediately after scrolling
SCROLL_CLICK_BLOCK_TIME = 0.50

# Prevent accidental right click immediately after left click
RIGHT_CLICK_BLOCK_TIME = 0.40
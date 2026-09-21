import pyautogui


class MouseController:
    """Control the Windows mouse using PyAutoGUI."""

    def __init__(self):
        # PyAutoGUI safety feature.
        pyautogui.PAUSE = 0.01

        self.screen_width, self.screen_height = (
            pyautogui.size()
        )

        self.is_dragging = False

    def move_cursor(self, x, y):
        """Move the mouse cursor to screen coordinates."""

        x = max(0, min(self.screen_width - 1, int(x)))
        y = max(0, min(self.screen_height - 1, int(y)))

        pyautogui.moveTo(x, y, duration=0.01)

    def left_click(self):
        """Perform a left mouse click."""

        pyautogui.click(button="left")
        print("LEFT CLICK")

    def right_click(self):
        """Perform a right mouse click."""

        pyautogui.click(button="right")
        print("RIGHT CLICK")

    def double_click(self):
        """Perform a double left click."""

        pyautogui.doubleClick(interval=0.15)
        print("DOUBLE CLICK")

    def start_drag(self):
        """Press and hold the left mouse button."""

        if not self.is_dragging:
            pyautogui.mouseDown(button="left")
            self.is_dragging = True
            print("DRAG STARTED")

    def stop_drag(self):
        """Release the left mouse button."""

        if self.is_dragging:
            pyautogui.mouseUp(button="left")
            self.is_dragging = False
            print("DRAG STOPPED")

    def scroll(self, amount):
        """Scroll vertically."""

        pyautogui.scroll(int(amount))

    def stop(self):
        """Safely release mouse buttons."""

        if self.is_dragging:
            pyautogui.mouseUp(button="left")
            self.is_dragging = False
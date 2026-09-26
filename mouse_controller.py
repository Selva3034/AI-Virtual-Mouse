import pyautogui


class MouseController:
    """
    Control the Windows mouse using PyAutoGUI.

    This class handles cursor movement, clicking, dragging,
    scrolling and safe mouse cleanup.
    """

    def __init__(self):
        # ========================================================
        # PYAUTOGUI SETTINGS
        # ========================================================

        # Small delay between PyAutoGUI actions.
        pyautogui.PAUSE = 0.01

        # Keep PyAutoGUI's emergency failsafe enabled.
        # Moving the physical mouse to the top-left corner
        # can trigger PyAutoGUI's emergency stop.
        pyautogui.FAILSAFE = True

        # ========================================================
        # SCREEN INFORMATION
        # ========================================================

        self.screen_width = 0
        self.screen_height = 0

        self.update_screen_size()

        # ========================================================
        # MOUSE STATE
        # ========================================================

        self.is_dragging = False

    # ============================================================
    # SCREEN SIZE
    # ============================================================

    def update_screen_size(self):
        """Refresh the current screen resolution."""

        try:
            self.screen_width, self.screen_height = (
                pyautogui.size()
            )

        except Exception as error:
            print(
                f"Unable to read screen size: {error}"
            )

            # Safe fallback.
            self.screen_width = 1920
            self.screen_height = 1080

    # ============================================================
    # COORDINATE VALIDATION
    # ============================================================

    def _clamp_coordinates(self, x, y):
        """
        Keep cursor coordinates inside the screen boundaries.
        """

        try:
            x = int(x)
            y = int(y)

        except (TypeError, ValueError):
            return 0, 0

        x = max(
            0,
            min(
                self.screen_width - 1,
                x
            )
        )

        y = max(
            0,
            min(
                self.screen_height - 1,
                y
            )
        )

        return x, y

    # ============================================================
    # MOVE CURSOR
    # ============================================================

    def move_cursor(self, x, y):
        """
        Move the mouse cursor to screen coordinates.
        """

        x, y = self._clamp_coordinates(
            x,
            y
        )

        try:
            pyautogui.moveTo(
                x,
                y,
                duration=0.01
            )

        except pyautogui.FailSafeException:
            print(
                "PyAutoGUI failsafe triggered."
            )

            self.stop()

        except Exception as error:
            print(
                f"Cursor movement error: {error}"
            )

    # ============================================================
    # LEFT CLICK
    # ============================================================

    def left_click(self):
        """Perform a left mouse click."""

        try:
            pyautogui.click(
                button="left"
            )

            print("LEFT CLICK")

        except pyautogui.FailSafeException:
            print(
                "PyAutoGUI failsafe triggered."
            )

            self.stop()

        except Exception as error:
            print(
                f"Left click error: {error}"
            )

    # ============================================================
    # RIGHT CLICK
    # ============================================================

    def right_click(self):
        """Perform a right mouse click."""

        try:
            pyautogui.click(
                button="right"
            )

            print("RIGHT CLICK")

        except pyautogui.FailSafeException:
            print(
                "PyAutoGUI failsafe triggered."
            )

            self.stop()

        except Exception as error:
            print(
                f"Right click error: {error}"
            )

    # ============================================================
    # DOUBLE CLICK
    # ============================================================

    def double_click(self):
        """Perform a double left click."""

        try:
            pyautogui.doubleClick(
                interval=0.15
            )

            print("DOUBLE CLICK")

        except pyautogui.FailSafeException:
            print(
                "PyAutoGUI failsafe triggered."
            )

            self.stop()

        except Exception as error:
            print(
                f"Double click error: {error}"
            )

    # ============================================================
    # START DRAG
    # ============================================================

    def start_drag(self):
        """Press and hold the left mouse button."""

        if self.is_dragging:
            return

        try:
            pyautogui.mouseDown(
                button="left"
            )

            self.is_dragging = True

            print("DRAG STARTED")

        except pyautogui.FailSafeException:
            print(
                "PyAutoGUI failsafe triggered."
            )

            self.stop()

        except Exception as error:
            print(
                f"Drag start error: {error}"
            )

    # ============================================================
    # STOP DRAG
    # ============================================================

    def stop_drag(self):
        """Release the left mouse button."""

        if not self.is_dragging:
            return

        try:
            pyautogui.mouseUp(
                button="left"
            )

            print("DRAG STOPPED")

        except Exception as error:
            print(
                f"Drag stop error: {error}"
            )

        finally:
            self.is_dragging = False

    # ============================================================
    # SCROLL
    # ============================================================

    def scroll(self, amount):
        """
        Scroll vertically.

        Positive amount  -> scroll up
        Negative amount  -> scroll down
        """

        try:
            amount = int(amount)

        except (TypeError, ValueError):
            return

        if amount == 0:
            return

        # Prevent an unexpectedly large scroll command.
        amount = max(
            -20,
            min(
                20,
                amount
            )
        )

        try:
            pyautogui.scroll(
                amount
            )

        except pyautogui.FailSafeException:
            print(
                "PyAutoGUI failsafe triggered."
            )

            self.stop()

        except Exception as error:
            print(
                f"Scroll error: {error}"
            )

    # ============================================================
    # DRAG STATUS
    # ============================================================

    def is_mouse_button_down(self):
        """
        Return True when the virtual mouse is currently
        holding the left mouse button.
        """

        return self.is_dragging

    # ============================================================
    # SAFE STOP
    # ============================================================

    def stop(self):
        """
        Safely release any mouse buttons currently held.
        """

        try:
            if self.is_dragging:

                pyautogui.mouseUp(
                    button="left"
                )

        except Exception as error:
            print(
                f"Mouse release error: {error}"
            )

        finally:
            self.is_dragging = False

    # ============================================================
    # RESET
    # ============================================================

    def reset(self):
        """
        Reset the mouse controller state.
        """

        self.stop()
        self.update_screen_size()

    # ============================================================
    # CLOSE
    # ============================================================

    def close(self):
        """Cleanly shut down the mouse controller."""

        self.stop()

        print(
            "Mouse controller closed."
        )
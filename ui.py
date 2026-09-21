import customtkinter as ctk


class VirtualMouseUI:

    def __init__(self):

        # -------------------------------------------------
        # APPEARANCE
        # -------------------------------------------------

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # -------------------------------------------------
        # WINDOW
        # -------------------------------------------------

        self.root = ctk.CTk()

        self.root.title("AI Virtual Mouse")

        self.root.geometry("700x600")

        self.root.resizable(False, False)

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        self.title_label = ctk.CTkLabel(
            self.root,
            text="AI Virtual Mouse",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        self.title_label.pack(
            pady=(30, 5)
        )

        # -------------------------------------------------
        # SUBTITLE
        # -------------------------------------------------

        self.subtitle_label = ctk.CTkLabel(
            self.root,
            text="Hand Gesture Based Computer Control",
            font=ctk.CTkFont(
                size=14
            )
        )

        self.subtitle_label.pack(
            pady=(0, 25)
        )

        # -------------------------------------------------
        # STATUS CARD
        # -------------------------------------------------

        self.status_frame = ctk.CTkFrame(
            self.root,
            corner_radius=15
        )

        self.status_frame.pack(
            padx=40,
            pady=10,
            fill="x"
        )

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="● SYSTEM READY",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        self.status_label.pack(
            pady=20
        )

        # -------------------------------------------------
        # GESTURES TITLE
        # -------------------------------------------------

        gesture_title = ctk.CTkLabel(
            self.root,
            text="Gesture Controls",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        gesture_title.pack(
            pady=(25, 10)
        )

        # -------------------------------------------------
        # GESTURE LIST
        # -------------------------------------------------

        gestures = [
            "Index Finger       → Move Cursor",
            "Thumb + Index      → Left Click",
            "Quick Pinch Twice   → Double Click",
            "Hold Pinch          → Drag & Drop",
            "Index + Middle      → Right Click",
            "Two Fingers         → Scroll",
            "Closed Fist         → Pause / Resume"
        ]

        for gesture in gestures:

            label = ctk.CTkLabel(
                self.root,
                text=gesture,
                font=ctk.CTkFont(
                    size=14
                ),
                anchor="w"
            )

            label.pack(
                padx=100,
                pady=3,
                anchor="w"
            )

        # -------------------------------------------------
        # BUTTON FRAME
        # -------------------------------------------------

        self.button_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )

        self.button_frame.pack(
            pady=30
        )

        # -------------------------------------------------
        # START BUTTON
        # -------------------------------------------------

        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="START",
            width=140,
            height=40,
            command=self.start
        )

        self.start_button.grid(
            row=0,
            column=0,
            padx=10
        )

        # -------------------------------------------------
        # PAUSE BUTTON
        # -------------------------------------------------

        self.pause_button = ctk.CTkButton(
            self.button_frame,
            text="PAUSE",
            width=140,
            height=40,
            command=self.pause
        )

        self.pause_button.grid(
            row=0,
            column=1,
            padx=10
        )

        # -------------------------------------------------
        # EXIT BUTTON
        # -------------------------------------------------

        self.exit_button = ctk.CTkButton(
            self.button_frame,
            text="EXIT",
            width=140,
            height=40,
            command=self.exit
        )

        self.exit_button.grid(
            row=0,
            column=2,
            padx=10
        )

    # =====================================================
    # START
    # =====================================================

    def start(self):

        self.status_label.configure(
            text="● SYSTEM ACTIVE"
        )

    # =====================================================
    # PAUSE
    # =====================================================

    def pause(self):

        self.status_label.configure(
            text="● SYSTEM PAUSED"
        )

    # =====================================================
    # EXIT
    # =====================================================

    def exit(self):

        self.root.destroy()

    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        self.root.mainloop()


# =========================================================
# TEST GUI
# =========================================================

if __name__ == "__main__":

    app = VirtualMouseUI()

    app.run()
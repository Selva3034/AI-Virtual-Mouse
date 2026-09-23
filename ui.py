import customtkinter as ctk
import subprocess
import sys
import os
import control


class VirtualMouseUI:
    def __init__(self):
        # -----------------------------
        # APP CONFIG
        # -----------------------------
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("AI Virtual Mouse")
        self.root.geometry("1100x700")
        self.root.minsize(950, 600)

        self.process = None
        self.running = False

        # -----------------------------
        # LOAD SETTINGS
        # -----------------------------
        self.settings = control.read_settings()

        # -----------------------------
        # COLORS
        # -----------------------------
        self.bg_color = "#10141A"
        self.sidebar_color = "#151A21"
        self.card_color = "#1B222B"
        self.border_color = "#2A333D"
        self.text_color = "#FFFFFF"
        self.secondary_text = "#9AA4AF"
        self.success_color = "#2ECC71"
        self.warning_color = "#F1C40F"
        self.danger_color = "#E74C3C"

        self.root.configure(fg_color=self.bg_color)

        # -----------------------------
        # MAIN LAYOUT
        # -----------------------------
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()

        self.show_dashboard()

        # Start status monitoring
        self.update_realtime_status()

        self.root.protocol("WM_DELETE_WINDOW", self.exit)

    # =========================================================
    # SIDEBAR
    # =========================================================

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self.root,
            width=230,
            corner_radius=0,
            fg_color=self.sidebar_color
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # Logo / title
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="AI VIRTUAL\nMOUSE",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            text_color=self.text_color
        )

        self.logo_label.pack(
            pady=(35, 10)
        )

        self.version_label = ctk.CTkLabel(
            self.sidebar,
            text="Hand Gesture Control",
            font=ctk.CTkFont(size=12),
            text_color=self.secondary_text
        )

        self.version_label.pack(
            pady=(0, 35)
        )

        # Navigation buttons
        self.dashboard_button = self.create_nav_button(
            "Dashboard",
            self.show_dashboard
        )

        self.gesture_button = self.create_nav_button(
            "Gesture Controls",
            self.show_gestures
        )

        self.settings_button = self.create_nav_button(
            "Settings",
            self.show_settings
        )

        # Bottom area
        self.sidebar_bottom = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        self.sidebar_bottom.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=25
        )

        self.start_button = ctk.CTkButton(
            self.sidebar_bottom,
            text="START",
            height=42,
            corner_radius=8,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.start
        )

        self.start_button.pack(
            fill="x",
            pady=(0, 10)
        )

        self.pause_button = ctk.CTkButton(
            self.sidebar_bottom,
            text="PAUSE",
            height=38,
            corner_radius=8,
            fg_color="#34495E",
            hover_color="#415A70",
            command=self.pause
        )

        self.pause_button.pack(
            fill="x",
            pady=(0, 10)
        )

        self.stop_button = ctk.CTkButton(
            self.sidebar_bottom,
            text="STOP",
            height=38,
            corner_radius=8,
            fg_color=self.danger_color,
            hover_color="#C0392B",
            command=self.stop
        )

        self.stop_button.pack(fill="x")

    def create_nav_button(self, text, command):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=42,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#222A33",
            anchor="w",
            font=ctk.CTkFont(size=14),
            command=command
        )

        button.pack(
            fill="x",
            padx=15,
            pady=4
        )

        return button

    # =========================================================
    # MAIN AREA
    # =========================================================

    def create_main_area(self):
        self.main_area = ctk.CTkFrame(
            self.root,
            fg_color=self.bg_color,
            corner_radius=0
        )

        self.main_area.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.main_area.grid_rowconfigure(
            1,
            weight=1
        )

        self.main_area.grid_columnconfigure(
            0,
            weight=1
        )

        # Header
        self.header = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=35,
            pady=(30, 10)
        )

        self.page_title = ctk.CTkLabel(
            self.header,
            text="Dashboard",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color=self.text_color
        )

        self.page_title.pack(
            anchor="w"
        )

        self.page_subtitle = ctk.CTkLabel(
            self.header,
            text="AI-powered hand gesture mouse control",
            font=ctk.CTkFont(size=13),
            text_color=self.secondary_text
        )

        self.page_subtitle.pack(
            anchor="w",
            pady=(3, 0)
        )

        # Content container
        self.content = ctk.CTkScrollableFrame(
            self.main_area,
            fg_color="transparent"
        )

        self.content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(10, 20)
        )

    # =========================================================
    # PAGE MANAGEMENT
    # =========================================================

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def update_page_header(self, title, subtitle):
        self.page_title.configure(text=title)
        self.page_subtitle.configure(text=subtitle)

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self):
        self.clear_content()

        self.update_page_header(
            "Dashboard",
            "AI-powered hand gesture mouse control"
        )

        # Status cards
        cards_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            pady=(10, 20)
        )

        for i in range(3):
            cards_frame.grid_columnconfigure(
                i,
                weight=1
            )

        self.camera_card = self.create_status_card(
            cards_frame,
            0,
            "Camera",
            "READY"
        )

        self.hand_card = self.create_status_card(
            cards_frame,
            1,
            "Hand Tracking",
            "READY"
        )

        self.cursor_card = self.create_status_card(
            cards_frame,
            2,
            "Cursor",
            "READY"
        )

        # Runtime information
        runtime_title = ctk.CTkLabel(
            self.content,
            text="Runtime Status",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        runtime_title.pack(
            anchor="w",
            pady=(10, 10)
        )

        runtime_card = ctk.CTkFrame(
            self.content,
            fg_color=self.card_color,
            corner_radius=12,
            border_width=1,
            border_color=self.border_color
        )

        runtime_card.pack(
            fill="x",
            pady=(0, 20)
        )

        runtime_card.grid_columnconfigure(
            1,
            weight=1
        )

        # Current gesture
        ctk.CTkLabel(
            runtime_card,
            text="Current Gesture",
            font=ctk.CTkFont(size=13),
            text_color=self.secondary_text
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=18,
            sticky="w"
        )

        self.gesture_value = ctk.CTkLabel(
            runtime_card,
            text="None",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        self.gesture_value.grid(
            row=0,
            column=1,
            padx=20,
            pady=18,
            sticky="e"
        )

        # FPS
        ctk.CTkLabel(
            runtime_card,
            text="FPS",
            font=ctk.CTkFont(size=13),
            text_color=self.secondary_text
        ).grid(
            row=1,
            column=0,
            padx=20,
            pady=18,
            sticky="w"
        )

        self.fps_value = ctk.CTkLabel(
            runtime_card,
            text="0",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        self.fps_value.grid(
            row=1,
            column=1,
            padx=20,
            pady=18,
            sticky="e"
        )

        # System status
        ctk.CTkLabel(
            runtime_card,
            text="System Status",
            font=ctk.CTkFont(size=13),
            text_color=self.secondary_text
        ).grid(
            row=2,
            column=0,
            padx=20,
            pady=18,
            sticky="w"
        )

        self.system_value = ctk.CTkLabel(
            runtime_card,
            text="READY",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        self.system_value.grid(
            row=2,
            column=1,
            padx=20,
            pady=18,
            sticky="e"
        )

        # Instructions
        info_title = ctk.CTkLabel(
            self.content,
            text="Quick Start",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        info_title.pack(
            anchor="w",
            pady=(5, 10)
        )

        info_card = ctk.CTkFrame(
            self.content,
            fg_color=self.card_color,
            corner_radius=12,
            border_width=1,
            border_color=self.border_color
        )

        info_card.pack(
            fill="x"
        )

        instructions = (
            "1. Click START to launch the virtual mouse.\n"
            "2. Place your hand in front of the camera.\n"
            "3. Use your index finger to control the cursor.\n"
            "4. Use the supported gestures for clicking and scrolling.\n"
            "5. Press ESC in the camera window to stop safely."
        )

        ctk.CTkLabel(
            info_card,
            text=instructions,
            justify="left",
            anchor="w",
            font=ctk.CTkFont(size=13),
            text_color=self.secondary_text
        ).pack(
            padx=20,
            pady=20,
            anchor="w"
        )

    def create_status_card(self, parent, column, title, value):
        card = ctk.CTkFrame(
            parent,
            fg_color=self.card_color,
            corner_radius=12,
            border_width=1,
            border_color=self.border_color
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=6
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=13),
            text_color=self.secondary_text
        ).pack(
            padx=18,
            pady=(18, 5),
            anchor="w"
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        value_label.pack(
            padx=18,
            pady=(0, 18),
            anchor="w"
        )

        return value_label

    # =========================================================
    # GESTURES PAGE
    # =========================================================

    def show_gestures(self):
        self.clear_content()

        self.update_page_header(
            "Gesture Controls",
            "Available hand gestures"
        )

        gestures = [
            ("Index Finger", "Move the mouse cursor"),
            ("Thumb + Index Pinch", "Left click"),
            ("Quick Pinch Twice", "Double click"),
            ("Hold Thumb + Index", "Drag"),
            ("Index + Middle Pinch", "Right click"),
            ("Two Fingers", "Scroll"),
            ("Closed Fist", "Pause / Resume")
        ]

        for gesture, action in gestures:
            card = ctk.CTkFrame(
                self.content,
                fg_color=self.card_color,
                corner_radius=10,
                border_width=1,
                border_color=self.border_color
            )

            card.pack(
                fill="x",
                pady=6
            )

            card.grid_columnconfigure(
                0,
                weight=1
            )

            ctk.CTkLabel(
                card,
                text=gesture,
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                )
            ).grid(
                row=0,
                column=0,
                padx=20,
                pady=16,
                sticky="w"
            )

            ctk.CTkLabel(
                card,
                text=action,
                font=ctk.CTkFont(size=13),
                text_color=self.secondary_text
            ).grid(
                row=0,
                column=1,
                padx=20,
                pady=16,
                sticky="e"
            )

    # =========================================================
    # SETTINGS PAGE
    # =========================================================

    def show_settings(self):
        self.clear_content()

        self.update_page_header(
            "Settings",
            "Configure virtual mouse behaviour"
        )

        # Refresh settings from file
        self.settings = control.read_settings()

        # ---------------------------------------------
        # SETTINGS CARD
        # ---------------------------------------------

        settings_card = ctk.CTkFrame(
            self.content,
            fg_color=self.card_color,
            corner_radius=12,
            border_width=1,
            border_color=self.border_color
        )

        settings_card.pack(
            fill="x",
            pady=(10, 20)
        )

        # ---------------------------------------------
        # SMOOTHING
        # ---------------------------------------------

        ctk.CTkLabel(
            settings_card,
            text="Cursor Smoothing",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        ctk.CTkLabel(
            settings_card,
            text="Controls how smoothly the cursor follows your finger.",
            font=ctk.CTkFont(size=12),
            text_color=self.secondary_text
        ).pack(
            anchor="w",
            padx=25
        )

        smoothing_frame = ctk.CTkFrame(
            settings_card,
            fg_color="transparent"
        )

        smoothing_frame.pack(
            fill="x",
            padx=25,
            pady=(15, 25)
        )

        smoothing_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.smoothing_slider = ctk.CTkSlider(
            smoothing_frame,
            from_=0.05,
            to=1.0,
            number_of_steps=95,
            command=self.update_smoothing_value
        )

        self.smoothing_slider.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 20)
        )

        self.smoothing_value = ctk.CTkLabel(
            smoothing_frame,
            text=f"{self.settings['smoothing']:.2f}",
            width=50,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.smoothing_value.grid(
            row=0,
            column=1
        )

        self.smoothing_slider.set(
            float(self.settings["smoothing"])
        )

        # ---------------------------------------------
        # SCROLL SPEED
        # ---------------------------------------------

        ctk.CTkLabel(
            settings_card,
            text="Scroll Speed",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        ctk.CTkLabel(
            settings_card,
            text="Controls how fast the mouse scrolls.",
            font=ctk.CTkFont(size=12),
            text_color=self.secondary_text
        ).pack(
            anchor="w",
            padx=25
        )

        scroll_frame = ctk.CTkFrame(
            settings_card,
            fg_color="transparent"
        )

        scroll_frame.pack(
            fill="x",
            padx=25,
            pady=(15, 25)
        )

        scroll_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.scroll_slider = ctk.CTkSlider(
            scroll_frame,
            from_=1,
            to=10,
            number_of_steps=9,
            command=self.update_scroll_value
        )

        self.scroll_slider.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 20)
        )

        self.scroll_value = ctk.CTkLabel(
            scroll_frame,
            text=str(self.settings["scroll_speed"]),
            width=50,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.scroll_value.grid(
            row=0,
            column=1
        )

        self.scroll_slider.set(
            int(self.settings["scroll_speed"])
        )

        # ---------------------------------------------
        # GESTURE CONFIRMATION
        # ---------------------------------------------

        ctk.CTkLabel(
            settings_card,
            text="Gesture Confirmation Frames",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        ctk.CTkLabel(
            settings_card,
            text="Higher values reduce accidental gesture detection.",
            font=ctk.CTkFont(size=12),
            text_color=self.secondary_text
        ).pack(
            anchor="w",
            padx=25
        )

        confirmation_frame = ctk.CTkFrame(
            settings_card,
            fg_color="transparent"
        )

        confirmation_frame.pack(
            fill="x",
            padx=25,
            pady=(15, 25)
        )

        confirmation_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.confirmation_slider = ctk.CTkSlider(
            confirmation_frame,
            from_=1,
            to=10,
            number_of_steps=9,
            command=self.update_confirmation_value
        )

        self.confirmation_slider.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 20)
        )

        self.confirmation_value = ctk.CTkLabel(
            confirmation_frame,
            text=str(
                self.settings[
                    "gesture_confirmation_frames"
                ]
            ),
            width=50,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.confirmation_value.grid(
            row=0,
            column=1
        )

        self.confirmation_slider.set(
            int(
                self.settings[
                    "gesture_confirmation_frames"
                ]
            )
        )

        # ---------------------------------------------
        # BUTTONS
        # ---------------------------------------------

        button_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        self.apply_button = ctk.CTkButton(
            button_frame,
            text="APPLY SETTINGS",
            height=42,
            corner_radius=8,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.apply_settings
        )

        self.apply_button.pack(
            side="left",
            padx=(0, 10)
        )

        self.reset_button = ctk.CTkButton(
            button_frame,
            text="RESET DEFAULTS",
            height=42,
            corner_radius=8,
            fg_color="#34495E",
            hover_color="#415A70",
            command=self.reset_settings
        )

        self.reset_button.pack(
            side="left"
        )

        # Status message
        self.settings_status = ctk.CTkLabel(
            self.content,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=self.success_color
        )

        self.settings_status.pack(
            anchor="w",
            pady=(0, 10)
        )

    # =========================================================
    # SETTINGS CALLBACKS
    # =========================================================

    def update_smoothing_value(self, value):
        self.smoothing_value.configure(
            text=f"{float(value):.2f}"
        )

    def update_scroll_value(self, value):
        self.scroll_value.configure(
            text=str(round(float(value)))
        )

    def update_confirmation_value(self, value):
        self.confirmation_value.configure(
            text=str(round(float(value)))
        )

    def apply_settings(self):
        smoothing = round(
            float(self.smoothing_slider.get()),
            2
        )

        scroll_speed = round(
            float(self.scroll_slider.get())
        )

        confirmation_frames = round(
            float(self.confirmation_slider.get())
        )

        new_settings = {
            "smoothing": smoothing,
            "scroll_speed": scroll_speed,
            "gesture_confirmation_frames": confirmation_frames
        }

        if control.write_settings(new_settings):
            self.settings = control.read_settings()

            self.settings_status.configure(
                text="Settings saved successfully.",
                text_color=self.success_color
            )
        else:
            self.settings_status.configure(
                text="Failed to save settings.",
                text_color=self.danger_color
            )

    def reset_settings(self):
        if control.reset_settings():
            self.settings = control.read_settings()

            self.smoothing_slider.set(
                self.settings["smoothing"]
            )

            self.scroll_slider.set(
                self.settings["scroll_speed"]
            )

            self.confirmation_slider.set(
                self.settings[
                    "gesture_confirmation_frames"
                ]
            )

            self.smoothing_value.configure(
                text=f"{self.settings['smoothing']:.2f}"
            )

            self.scroll_value.configure(
                text=str(
                    self.settings["scroll_speed"]
                )
            )

            self.confirmation_value.configure(
                text=str(
                    self.settings[
                        "gesture_confirmation_frames"
                    ]
                )
            )

            self.settings_status.configure(
                text="Settings reset to defaults.",
                text_color=self.success_color
            )

    # =========================================================
    # START ENGINE
    # =========================================================

    def start(self):
        if self.process is not None:
            if self.process.poll() is None:
                return

        control.clear_command()
        control.clear_status()

        project_directory = os.path.dirname(
            os.path.abspath(__file__)
        )

        main_file = os.path.join(
            project_directory,
            "main.py"
        )

        try:
            self.process = subprocess.Popen(
                [
                    sys.executable,
                    main_file
                ],
                cwd=project_directory
            )

            self.running = True

            self.start_button.configure(
                text="RUNNING",
                state="disabled"
            )

            self.pause_button.configure(
                text="PAUSE"
            )

        except Exception as error:
            print(f"Could not start main.py: {error}")

    # =========================================================
    # PAUSE / RESUME
    # =========================================================

    def pause(self):
        if not self.running:
            return

        status = control.read_status()

        if status.get("paused", False):
            control.write_command("resume")

            self.pause_button.configure(
                text="PAUSE"
            )
        else:
            control.write_command("pause")

            self.pause_button.configure(
                text="RESUME"
            )

    # =========================================================
    # STOP
    # =========================================================

    def stop(self):
        control.write_command("stop")

        if self.process is not None:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass

        self.process = None
        self.running = False

        control.clear_command()
        control.clear_status()

        self.start_button.configure(
            text="START",
            state="normal"
        )

        self.pause_button.configure(
            text="PAUSE"
        )

        # Reset dashboard display
        if hasattr(self, "camera_card"):
            self.camera_card.configure(text="READY")

        if hasattr(self, "hand_card"):
            self.hand_card.configure(text="READY")

        if hasattr(self, "cursor_card"):
            self.cursor_card.configure(text="READY")

        if hasattr(self, "gesture_value"):
            self.gesture_value.configure(text="None")

        if hasattr(self, "fps_value"):
            self.fps_value.configure(text="0")

        if hasattr(self, "system_value"):
            self.system_value.configure(text="READY")

    # =========================================================
    # REAL-TIME STATUS
    # =========================================================

    def update_realtime_status(self):
        status = control.read_status()

        camera = status.get(
            "camera",
            "READY"
        )

        hand = status.get(
            "hand",
            "READY"
        )

        cursor = status.get(
            "cursor",
            "READY"
        )

        gesture = status.get(
            "gesture",
            "None"
        )

        fps = status.get(
            "fps",
            0
        )

        paused = status.get(
            "paused",
            False
        )

        # Update dashboard if widgets exist
        if hasattr(self, "camera_card"):
            self.camera_card.configure(
                text=camera
            )

        if hasattr(self, "hand_card"):
            self.hand_card.configure(
                text=hand
            )

        if hasattr(self, "cursor_card"):
            self.cursor_card.configure(
                text=cursor
            )

        if hasattr(self, "gesture_value"):
            self.gesture_value.configure(
                text=gesture
            )

        if hasattr(self, "fps_value"):
            self.fps_value.configure(
                text=str(round(float(fps)))
            )

        if hasattr(self, "system_value"):
            if paused:
                self.system_value.configure(
                    text="PAUSED",
                    text_color=self.warning_color
                )

            elif self.running:
                self.system_value.configure(
                    text="RUNNING",
                    text_color=self.success_color
                )

            else:
                self.system_value.configure(
                    text="READY",
                    text_color=self.text_color
                )

        # Keep pause button synchronized
        if self.running:
            if paused:
                self.pause_button.configure(
                    text="RESUME"
                )
            else:
                self.pause_button.configure(
                    text="PAUSE"
                )

        # Check whether process has ended
        if self.process is not None:
            if self.process.poll() is not None:
                self.process = None
                self.running = False

                self.start_button.configure(
                    text="START",
                    state="normal"
                )

                self.pause_button.configure(
                    text="PAUSE"
                )

        self.root.after(
            200,
            self.update_realtime_status
        )

    # =========================================================
    # EXIT
    # =========================================================

    def exit(self):
        self.stop()

        try:
            self.root.destroy()
        except Exception:
            pass

    # =========================================================
    # RUN
    # =========================================================

    def run(self):
        self.root.mainloop()


# =============================================================
# APPLICATION START
# =============================================================

if __name__ == "__main__":
    app = VirtualMouseUI()
    app.run()
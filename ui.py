import customtkinter as ctk
import subprocess
import sys
import os

import control


class VirtualMouseUI:

    def __init__(self):

        # =====================================================
        # APPEARANCE
        # =====================================================

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # =====================================================
        # WINDOW
        # =====================================================

        self.root = ctk.CTk()

        self.root.title("AI Virtual Mouse")

        self.root.geometry("1100x700")

        self.root.minsize(950, 600)

        self.root.resizable(True, True)

        # =====================================================
        # ENGINE
        # =====================================================

        self.engine_process = None

        self.is_running = False

        self.is_paused = False

        # =====================================================
        # MAIN GRID
        # =====================================================

        self.root.grid_columnconfigure(
            0,
            weight=0
        )

        self.root.grid_columnconfigure(
            1,
            weight=1
        )

        self.root.grid_rowconfigure(
            0,
            weight=1
        )

        # =====================================================
        # SIDEBAR
        # =====================================================

        self.sidebar = ctk.CTkFrame(
            self.root,
            width=230,
            corner_radius=0
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # =====================================================
        # LOGO
        # =====================================================

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="AI VIRTUAL\nMOUSE",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        )

        self.logo_label.pack(
            pady=(35, 5)
        )

        self.logo_subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Hand Gesture Control",
            font=ctk.CTkFont(
                size=12
            ),
            text_color="gray"
        )

        self.logo_subtitle.pack(
            pady=(0, 35)
        )

        # =====================================================
        # MENU
        # =====================================================

        navigation_title = ctk.CTkLabel(
            self.sidebar,
            text="MENU",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color="gray"
        )

        navigation_title.pack(
            padx=25,
            anchor="w"
        )

        # Dashboard
        self.dashboard_button = ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            height=42,
            corner_radius=8,
            anchor="w",
            command=self.show_dashboard
        )

        self.dashboard_button.pack(
            padx=15,
            pady=(8, 5),
            fill="x"
        )

        # Gestures
        self.gestures_button = ctk.CTkButton(
            self.sidebar,
            text="Gesture Controls",
            height=42,
            corner_radius=8,
            anchor="w",
            fg_color="transparent",
            command=self.show_gestures
        )

        self.gestures_button.pack(
            padx=15,
            pady=5,
            fill="x"
        )

        # Settings
        self.settings_button = ctk.CTkButton(
            self.sidebar,
            text="Settings",
            height=42,
            corner_radius=8,
            anchor="w",
            fg_color="transparent",
            command=self.show_settings
        )

        self.settings_button.pack(
            padx=15,
            pady=5,
            fill="x"
        )

        # =====================================================
        # VERSION
        # =====================================================

        self.version_label = ctk.CTkLabel(
            self.sidebar,
            text="Version 1.0.0",
            font=ctk.CTkFont(
                size=11
            ),
            text_color="gray"
        )

        self.version_label.pack(
            side="bottom",
            pady=20
        )

        # =====================================================
        # MAIN FRAME
        # =====================================================

        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent",
            corner_radius=0
        )

        self.main_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=25,
            pady=20
        )

        self.main_frame.grid_rowconfigure(
            1,
            weight=1
        )

        self.main_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # =====================================================
        # HEADER
        # =====================================================

        self.header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        self.header_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Dashboard",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        self.title_label.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.header_status = ctk.CTkLabel(
            self.header_frame,
            text="● READY",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color="#3B82F6"
        )

        self.header_status.grid(
            row=0,
            column=1,
            sticky="e"
        )

        # =====================================================
        # CONTENT
        # =====================================================

        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.content_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.content_frame.grid_rowconfigure(
            0,
            weight=1
        )

        self.content_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # =====================================================
        # CREATE PAGES
        # =====================================================

        self.create_dashboard_page()

        self.create_gesture_page()

        self.create_settings_page()

        # =====================================================
        # CONTROL BUTTONS
        # =====================================================

        self.button_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.button_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(15, 0)
        )

        for column in range(3):

            self.button_frame.grid_columnconfigure(
                column,
                weight=1
            )

        # START
        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="START",
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.start
        )

        self.start_button.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        # PAUSE
        self.pause_button = ctk.CTkButton(
            self.button_frame,
            text="PAUSE",
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            state="disabled",
            command=self.pause
        )

        self.pause_button.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5
        )

        # STOP
        self.stop_button = ctk.CTkButton(
            self.button_frame,
            text="STOP",
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            fg_color="#B91C1C",
            hover_color="#991B1B",
            state="disabled",
            command=self.stop
        )

        self.stop_button.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=(5, 0)
        )

        # =====================================================
        # CLOSE EVENT
        # =====================================================

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.exit
        )

        # =====================================================
        # DEFAULT PAGE
        # =====================================================

        self.show_dashboard()

        # =====================================================
        # START STATUS MONITOR
        # =====================================================

        self.root.after(
            200,
            self.update_realtime_status
        )

    # =========================================================
    # DASHBOARD PAGE
    # =========================================================

    def create_dashboard_page(self):

        self.dashboard_page = ctk.CTkFrame(
            self.content_frame,
            corner_radius=15
        )

        self.dashboard_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.dashboard_page.grid_columnconfigure(
            0,
            weight=1
        )

        self.dashboard_page.grid_columnconfigure(
            1,
            weight=1
        )

        self.dashboard_page.grid_rowconfigure(
            1,
            weight=1
        )

        # =====================================================
        # STATUS CARDS
        # =====================================================

        self.status_container = ctk.CTkFrame(
            self.dashboard_page,
            fg_color="transparent"
        )

        self.status_container.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=15
        )

        for column in range(3):

            self.status_container.grid_columnconfigure(
                column,
                weight=1
            )

        self.camera_status = self.create_status_card(
            self.status_container,
            "Camera",
            "● READY",
            0
        )

        self.hand_status = self.create_status_card(
            self.status_container,
            "Hand Tracking",
            "● READY",
            1
        )

        self.cursor_status = self.create_status_card(
            self.status_container,
            "Cursor",
            "● READY",
            2
        )

        # =====================================================
        # SYSTEM PANEL
        # =====================================================

        self.system_panel = ctk.CTkFrame(
            self.dashboard_page,
            corner_radius=12
        )

        self.system_panel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(15, 8),
            pady=(0, 15)
        )

        self.system_title = ctk.CTkLabel(
            self.system_panel,
            text="System Status",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        self.system_title.pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        self.current_title = ctk.CTkLabel(
            self.system_panel,
            text="CURRENT GESTURE",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color="gray"
        )

        self.current_title.pack(
            anchor="w",
            padx=25
        )

        self.gesture_value = ctk.CTkLabel(
            self.system_panel,
            text="None",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        self.gesture_value.pack(
            anchor="w",
            padx=25,
            pady=(5, 25)
        )

        self.fps_title = ctk.CTkLabel(
            self.system_panel,
            text="FRAME RATE",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color="gray"
        )

        self.fps_title.pack(
            anchor="w",
            padx=25
        )

        self.fps_value = ctk.CTkLabel(
            self.system_panel,
            text="0 FPS",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        self.fps_value.pack(
            anchor="w",
            padx=25,
            pady=(5, 25)
        )

        self.system_label = ctk.CTkLabel(
            self.system_panel,
            text="● SYSTEM READY",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#3B82F6"
        )

        self.system_label.pack(
            anchor="w",
            padx=25
        )

        # =====================================================
        # INFO PANEL
        # =====================================================

        self.info_panel = ctk.CTkFrame(
            self.dashboard_page,
            corner_radius=12
        )

        self.info_panel.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(8, 15),
            pady=(0, 15)
        )

        self.info_title = ctk.CTkLabel(
            self.info_panel,
            text="Virtual Mouse",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        self.info_title.pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        self.info_text = ctk.CTkLabel(
            self.info_panel,
            text=(
                "Control your computer using\n"
                "real-time hand gestures.\n\n"
                "Move your index finger to\n"
                "control the cursor.\n\n"
                "Use the Gesture Controls page\n"
                "to view supported actions."
            ),
            font=ctk.CTkFont(
                size=14
            ),
            justify="left",
            anchor="w"
        )

        self.info_text.pack(
            anchor="w",
            padx=25
        )

    # =========================================================
    # GESTURE PAGE
    # =========================================================

    def create_gesture_page(self):

        self.gesture_page = ctk.CTkFrame(
            self.content_frame,
            corner_radius=15
        )

        self.gesture_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        title = ctk.CTkLabel(
            self.gesture_page,
            text="Supported Gestures",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(25, 20)
        )

        gestures = [

            ("INDEX FINGER", "Move Cursor"),

            ("THUMB + INDEX", "Left Click"),

            ("QUICK PINCH ×2", "Double Click"),

            ("HOLD THUMB + INDEX", "Drag & Drop"),

            ("INDEX + MIDDLE PINCH", "Right Click"),

            ("TWO FINGERS", "Scroll Up / Down"),

            ("CLOSED FIST", "Pause / Resume")

        ]

        for gesture, action in gestures:

            row = ctk.CTkFrame(
                self.gesture_page,
                corner_radius=8
            )

            row.pack(
                fill="x",
                padx=30,
                pady=5
            )

            row.grid_columnconfigure(
                0,
                weight=1
            )

            left = ctk.CTkLabel(
                row,
                text=gesture,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                ),
                anchor="w"
            )

            left.grid(
                row=0,
                column=0,
                sticky="w",
                padx=15,
                pady=12
            )

            right = ctk.CTkLabel(
                row,
                text=action,
                font=ctk.CTkFont(
                    size=14
                ),
                text_color="gray"
            )

            right.grid(
                row=0,
                column=1,
                sticky="e",
                padx=15
            )

    # =========================================================
    # SETTINGS PAGE
    # =========================================================

    def create_settings_page(self):

        self.settings_page = ctk.CTkFrame(
            self.content_frame,
            corner_radius=15
        )

        self.settings_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        title = ctk.CTkLabel(
            self.settings_page,
            text="Settings",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(25, 25)
        )

        # =====================================================
        # SMOOTHING
        # =====================================================

        smoothing_title = ctk.CTkLabel(
            self.settings_page,
            text="Cursor Smoothing",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        smoothing_title.pack(
            anchor="w",
            padx=30
        )

        self.smoothing_slider = ctk.CTkSlider(
            self.settings_page,
            from_=0.05,
            to=1.0
        )

        self.smoothing_slider.set(
            0.5
        )

        self.smoothing_slider.pack(
            fill="x",
            padx=30,
            pady=(10, 20)
        )

        # =====================================================
        # SCROLL SPEED
        # =====================================================

        scroll_title = ctk.CTkLabel(
            self.settings_page,
            text="Scroll Speed",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        scroll_title.pack(
            anchor="w",
            padx=30
        )

        self.scroll_slider = ctk.CTkSlider(
            self.settings_page,
            from_=1,
            to=10
        )

        self.scroll_slider.set(
            3
        )

        self.scroll_slider.pack(
            fill="x",
            padx=30,
            pady=(10, 20)
        )

        # =====================================================
        # CONFIRMATION FRAMES
        # =====================================================

        confirmation_title = ctk.CTkLabel(
            self.settings_page,
            text="Gesture Confirmation Frames",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        confirmation_title.pack(
            anchor="w",
            padx=30
        )

        self.confirmation_slider = ctk.CTkSlider(
            self.settings_page,
            from_=1,
            to=10,
            number_of_steps=9
        )

        self.confirmation_slider.set(
            3
        )

        self.confirmation_slider.pack(
            fill="x",
            padx=30,
            pady=(10, 20)
        )

        note = ctk.CTkLabel(
            self.settings_page,
            text=(
                "Settings will be connected to the\n"
                "virtual mouse engine in a later phase."
            ),
            font=ctk.CTkFont(
                size=12
            ),
            text_color="gray",
            justify="left"
        )

        note.pack(
            anchor="w",
            padx=30,
            pady=20
        )

    # =========================================================
    # STATUS CARD
    # =========================================================

    def create_status_card(
        self,
        parent,
        title,
        status,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            corner_radius=12
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color="gray"
        )

        title_label.pack(
            pady=(15, 2)
        )

        status_label = ctk.CTkLabel(
            card,
            text=status,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color="#3B82F6"
        )

        status_label.pack(
            pady=(0, 15)
        )

        return status_label

    # =========================================================
    # START
    # =========================================================

    def start(self):

        control.clear_command()

        control.clear_status()

        if (
            self.engine_process is not None
            and self.engine_process.poll() is None
        ):

            return

        try:

            project_directory = os.path.dirname(
                os.path.abspath(__file__)
            )

            main_file = os.path.join(
                project_directory,
                "main.py"
            )

            print(
                "Starting virtual mouse engine..."
            )

            self.engine_process = subprocess.Popen(
                [
                    sys.executable,
                    main_file
                ],
                cwd=project_directory
            )

            self.is_running = True

            self.is_paused = False

            # -------------------------------------------------
            # UI
            # -------------------------------------------------

            self.system_label.configure(
                text="● SYSTEM ACTIVE",
                text_color="#22C55E"
            )

            self.header_status.configure(
                text="● ACTIVE",
                text_color="#22C55E"
            )

            self.start_button.configure(
                state="disabled"
            )

            self.pause_button.configure(
                state="normal",
                text="PAUSE"
            )

            self.stop_button.configure(
                state="normal"
            )

            print(
                "Virtual mouse engine started."
            )

        except Exception as error:

            print(
                "Unable to start virtual mouse:"
            )

            print(error)

            self.is_running = False

    # =========================================================
    # PAUSE / RESUME
    # =========================================================

    def pause(self):

        if not self.is_running:

            return

        if not self.is_paused:

            control.write_command(
                "pause"
            )

            self.is_paused = True

            self.system_label.configure(
                text="● PAUSED",
                text_color="#F59E0B"
            )

            self.header_status.configure(
                text="● PAUSED",
                text_color="#F59E0B"
            )

            self.pause_button.configure(
                text="RESUME"
            )

            print(
                "UI: Pause command sent."
            )

        else:

            control.write_command(
                "resume"
            )

            self.is_paused = False

            self.system_label.configure(
                text="● SYSTEM ACTIVE",
                text_color="#22C55E"
            )

            self.header_status.configure(
                text="● ACTIVE",
                text_color="#22C55E"
            )

            self.pause_button.configure(
                text="PAUSE"
            )

            print(
                "UI: Resume command sent."
            )

    # =========================================================
    # STOP
    # =========================================================

    def stop(self):

        control.clear_command()

        if self.engine_process is not None:

            try:

                if self.engine_process.poll() is None:

                    self.engine_process.terminate()

                    self.engine_process.wait(
                        timeout=3
                    )

            except Exception:

                try:

                    self.engine_process.kill()

                except Exception:

                    pass

        self.engine_process = None

        self.is_running = False

        self.is_paused = False

        control.clear_status()

        # -----------------------------------------------------
        # RESET UI
        # -----------------------------------------------------

        self.system_label.configure(
            text="● SYSTEM READY",
            text_color="#3B82F6"
        )

        self.header_status.configure(
            text="● READY",
            text_color="#3B82F6"
        )

        self.camera_status.configure(
            text="● READY",
            text_color="#3B82F6"
        )

        self.hand_status.configure(
            text="● READY",
            text_color="#3B82F6"
        )

        self.cursor_status.configure(
            text="● READY",
            text_color="#3B82F6"
        )

        self.gesture_value.configure(
            text="None"
        )

        self.fps_value.configure(
            text="0 FPS"
        )

        self.start_button.configure(
            state="normal"
        )

        self.pause_button.configure(
            state="disabled",
            text="PAUSE"
        )

        self.stop_button.configure(
            state="disabled"
        )

        print(
            "Virtual mouse engine stopped."
        )

    # =========================================================
    # REAL-TIME STATUS
    # =========================================================

    def update_realtime_status(self):

        if self.is_running:

            # Check whether engine has exited
            if (
                self.engine_process is not None
                and self.engine_process.poll() is not None
            ):

                self.is_running = False

                self.engine_process = None

                self.start_button.configure(
                    state="normal"
                )

                self.pause_button.configure(
                    state="disabled",
                    text="PAUSE"
                )

                self.stop_button.configure(
                    state="disabled"
                )

                self.header_status.configure(
                    text="● READY",
                    text_color="#3B82F6"
                )

                self.system_label.configure(
                    text="● SYSTEM READY",
                    text_color="#3B82F6"
                )

            else:

                status = control.read_status()

                # ---------------------------------------------
                # CAMERA
                # ---------------------------------------------

                camera = status.get(
                    "camera",
                    "READY"
                )

                if camera == "ACTIVE":

                    self.camera_status.configure(
                        text="● ACTIVE",
                        text_color="#22C55E"
                    )

                else:

                    self.camera_status.configure(
                        text="● READY",
                        text_color="#3B82F6"
                    )

                # ---------------------------------------------
                # HAND
                # ---------------------------------------------

                hand = status.get(
                    "hand",
                    "READY"
                )

                if hand == "DETECTED":

                    self.hand_status.configure(
                        text="● DETECTED",
                        text_color="#22C55E"
                    )

                elif hand == "NOT DETECTED":

                    self.hand_status.configure(
                        text="● NOT DETECTED",
                        text_color="#F59E0B"
                    )

                else:

                    self.hand_status.configure(
                        text="● READY",
                        text_color="#3B82F6"
                    )

                # ---------------------------------------------
                # CURSOR
                # ---------------------------------------------

                cursor = status.get(
                    "cursor",
                    "READY"
                )

                if cursor == "ACTIVE":

                    self.cursor_status.configure(
                        text="● ACTIVE",
                        text_color="#22C55E"
                    )

                elif cursor == "PAUSED":

                    self.cursor_status.configure(
                        text="● PAUSED",
                        text_color="#F59E0B"
                    )

                else:

                    self.cursor_status.configure(
                        text="● READY",
                        text_color="#3B82F6"
                    )

                # ---------------------------------------------
                # GESTURE
                # ---------------------------------------------

                gesture = status.get(
                    "gesture",
                    "None"
                )

                self.gesture_value.configure(
                    text=gesture
                )

                # ---------------------------------------------
                # FPS
                # ---------------------------------------------

                fps = status.get(
                    "fps",
                    0
                )

                try:

                    fps = float(fps)

                except Exception:

                    fps = 0

                self.fps_value.configure(
                    text=f"{fps:.1f} FPS"
                )

        # =====================================================
        # CHECK AGAIN
        # =====================================================

        self.root.after(
            200,
            self.update_realtime_status
        )

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self):

        self.hide_pages()

        self.dashboard_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.title_label.configure(
            text="Dashboard"
        )

        self.dashboard_button.configure(
            fg_color="#1F6AA5"
        )

        self.gestures_button.configure(
            fg_color="transparent"
        )

        self.settings_button.configure(
            fg_color="transparent"
        )

    # =========================================================
    # GESTURES
    # =========================================================

    def show_gestures(self):

        self.hide_pages()

        self.gesture_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.title_label.configure(
            text="Gesture Controls"
        )

        self.dashboard_button.configure(
            fg_color="transparent"
        )

        self.gestures_button.configure(
            fg_color="#1F6AA5"
        )

        self.settings_button.configure(
            fg_color="transparent"
        )

    # =========================================================
    # SETTINGS
    # =========================================================

    def show_settings(self):

        self.hide_pages()

        self.settings_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.title_label.configure(
            text="Settings"
        )

        self.dashboard_button.configure(
            fg_color="transparent"
        )

        self.gestures_button.configure(
            fg_color="transparent"
        )

        self.settings_button.configure(
            fg_color="#1F6AA5"
        )

    # =========================================================
    # HIDE PAGES
    # =========================================================

    def hide_pages(self):

        self.dashboard_page.grid_forget()

        self.gesture_page.grid_forget()

        self.settings_page.grid_forget()

    # =========================================================
    # EXIT
    # =========================================================

    def exit(self):

        self.stop()

        self.root.destroy()

    # =========================================================
    # RUN
    # =========================================================

    def run(self):

        self.root.mainloop()


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    app = VirtualMouseUI()

    app.run()
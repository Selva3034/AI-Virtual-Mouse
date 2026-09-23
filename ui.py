import customtkinter as ctk
import subprocess
import sys
import os
import control


class VirtualMouseUI:
    def __init__(self):
        # =====================================================
        # APP CONFIG
        # =====================================================

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("AI Virtual Mouse")
        self.root.geometry("1180x760")
        self.root.minsize(1000, 650)

        self.process = None
        self.running = False

        self.settings = control.read_settings()

        # =====================================================
        # COLORS
        # =====================================================

        self.BG = "#0B0F14"
        self.SIDEBAR = "#10161D"
        self.CARD = "#151C24"
        self.CARD_HOVER = "#1C2631"
        self.BORDER = "#27323D"

        self.TEXT = "#F5F7FA"
        self.MUTED = "#8C98A6"

        self.BLUE = "#3B82F6"
        self.BLUE_HOVER = "#2563EB"

        self.GREEN = "#22C55E"
        self.YELLOW = "#F59E0B"
        self.RED = "#EF4444"

        self.root.configure(
            fg_color=self.BG
        )

        # =====================================================
        # GRID
        # =====================================================

        self.root.grid_columnconfigure(
            1,
            weight=1
        )

        self.root.grid_rowconfigure(
            0,
            weight=1
        )

        # =====================================================
        # CREATE UI
        # =====================================================

        self.create_sidebar()
        self.create_main_area()

        self.show_dashboard()

        self.update_realtime_status()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.exit
        )

    # =========================================================
    # SIDEBAR
    # =========================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self.root,
            width=245,
            corner_radius=0,
            fg_color=self.SIDEBAR
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # -----------------------------------------------------
        # BRAND
        # -----------------------------------------------------

        brand_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        brand_frame.pack(
            fill="x",
            padx=24,
            pady=(30, 35)
        )

        logo = ctk.CTkLabel(
            brand_frame,
            text="◉",
            font=ctk.CTkFont(
                size=34,
                weight="bold"
            ),
            text_color=self.BLUE
        )

        logo.pack(
            side="left",
            padx=(0, 10)
        )

        brand_text = ctk.CTkFrame(
            brand_frame,
            fg_color="transparent"
        )

        brand_text.pack(
            side="left"
        )

        ctk.CTkLabel(
            brand_text,
            text="AI VIRTUAL",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color=self.TEXT
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            brand_text,
            text="MOUSE",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color=self.BLUE
        ).pack(
            anchor="w"
        )

        # -----------------------------------------------------
        # NAVIGATION TITLE
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.sidebar,
            text="WORKSPACE",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=self.MUTED
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 8)
        )

        # -----------------------------------------------------
        # NAVIGATION
        # -----------------------------------------------------

        self.dashboard_button = self.create_nav_button(
            "▣   Dashboard",
            self.show_dashboard
        )

        self.gesture_button = self.create_nav_button(
            "✋   Gesture Controls",
            self.show_gestures
        )

        self.settings_button = self.create_nav_button(
            "⚙   Settings",
            self.show_settings
        )

        # -----------------------------------------------------
        # SYSTEM STATUS
        # -----------------------------------------------------

        self.sidebar_status = ctk.CTkFrame(
            self.sidebar,
            fg_color=self.CARD,
            corner_radius=12,
            border_width=1,
            border_color=self.BORDER
        )

        self.sidebar_status.pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=(10, 20)
        )

        status_top = ctk.CTkFrame(
            self.sidebar_status,
            fg_color="transparent"
        )

        status_top.pack(
            fill="x",
            padx=15,
            pady=(15, 5)
        )

        self.status_dot = ctk.CTkLabel(
            status_top,
            text="●",
            font=ctk.CTkFont(size=12),
            text_color=self.MUTED
        )

        self.status_dot.pack(
            side="left",
            padx=(0, 7)
        )

        ctk.CTkLabel(
            status_top,
            text="System",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.TEXT
        ).pack(
            side="left"
        )

        self.sidebar_system_text = ctk.CTkLabel(
            self.sidebar_status,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED
        )

        self.sidebar_system_text.pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )

        # -----------------------------------------------------
        # CONTROL BUTTONS
        # -----------------------------------------------------

        self.start_button = ctk.CTkButton(
            self.sidebar,
            text="▶  START",
            height=42,
            corner_radius=9,
            fg_color=self.BLUE,
            hover_color=self.BLUE_HOVER,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.start
        )

        self.start_button.pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=(0, 10)
        )

        self.pause_button = ctk.CTkButton(
            self.sidebar,
            text="Ⅱ  PAUSE",
            height=38,
            corner_radius=9,
            fg_color="#263341",
            hover_color="#344454",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=self.pause
        )

        self.pause_button.pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=(0, 8)
        )

        self.stop_button = ctk.CTkButton(
            self.sidebar,
            text="■  STOP",
            height=38,
            corner_radius=9,
            fg_color="#2A1A1D",
            hover_color="#4A2025",
            text_color="#FF7B84",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=self.stop
        )

        self.stop_button.pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=(0, 8)
        )

    # =========================================================
    # NAV BUTTON
    # =========================================================

    def create_nav_button(
        self,
        text,
        command
    ):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=44,
            corner_radius=8,
            fg_color="transparent",
            hover_color=self.CARD_HOVER,
            anchor="w",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=self.MUTED,
            command=command
        )

        button.pack(
            fill="x",
            padx=15,
            pady=3
        )

        return button

    # =========================================================
    # MAIN AREA
    # =========================================================

    def create_main_area(self):

        self.main_area = ctk.CTkFrame(
            self.root,
            fg_color=self.BG,
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

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        self.header = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=38,
            pady=(30, 10)
        )

        self.header.grid_columnconfigure(
            0,
            weight=1
        )

        header_left = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )

        header_left.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.page_title = ctk.CTkLabel(
            header_left,
            text="Dashboard",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=self.TEXT
        )

        self.page_title.pack(
            anchor="w"
        )

        self.page_subtitle = ctk.CTkLabel(
            header_left,
            text="Control your computer with natural hand gestures",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=self.MUTED
        )

        self.page_subtitle.pack(
            anchor="w",
            pady=(3, 0)
        )

        # Live indicator
        self.live_badge = ctk.CTkFrame(
            self.header,
            fg_color=self.CARD,
            corner_radius=20,
            border_width=1,
            border_color=self.BORDER
        )

        self.live_badge.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(20, 0)
        )

        self.live_dot = ctk.CTkLabel(
            self.live_badge,
            text="●",
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED
        )

        self.live_dot.pack(
            side="left",
            padx=(12, 5),
            pady=8
        )

        self.live_text = ctk.CTkLabel(
            self.live_badge,
            text="SYSTEM READY",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.MUTED
        )

        self.live_text.pack(
            side="left",
            padx=(0, 12),
            pady=8
        )

        # -----------------------------------------------------
        # CONTENT
        # -----------------------------------------------------

        self.content = ctk.CTkScrollableFrame(
            self.main_area,
            fg_color="transparent"
        )

        self.content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=28,
            pady=(5, 20)
        )

    # =========================================================
    # PAGE HELPERS
    # =========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def update_page_header(
        self,
        title,
        subtitle
    ):

        self.page_title.configure(
            text=title
        )

        self.page_subtitle.configure(
            text=subtitle
        )

    def set_active_nav(self, active_button):

        buttons = [
            self.dashboard_button,
            self.gesture_button,
            self.settings_button
        ]

        for button in buttons:

            if button == active_button:

                button.configure(
                    fg_color="#172B48",
                    text_color="#60A5FA"
                )

            else:

                button.configure(
                    fg_color="transparent",
                    text_color=self.MUTED
                )

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self):

        self.clear_content()

        self.set_active_nav(
            self.dashboard_button
        )

        self.update_page_header(
            "Dashboard",
            "Control your computer with natural hand gestures"
        )

        # -----------------------------------------------------
        # STATUS CARDS
        # -----------------------------------------------------

        cards_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            pady=(10, 15)
        )

        for i in range(4):

            cards_frame.grid_columnconfigure(
                i,
                weight=1
            )

        self.camera_card = self.create_dashboard_card(
            cards_frame,
            0,
            "CAMERA",
            "READY",
            "●"
        )

        self.hand_card = self.create_dashboard_card(
            cards_frame,
            1,
            "HAND TRACKING",
            "READY",
            "✋"
        )

        self.cursor_card = self.create_dashboard_card(
            cards_frame,
            2,
            "CURSOR",
            "READY",
            "↗"
        )

        self.fps_card = self.create_dashboard_card(
            cards_frame,
            3,
            "PERFORMANCE",
            "0 FPS",
            "◌"
        )

        # -----------------------------------------------------
        # CURRENT GESTURE
        # -----------------------------------------------------

        gesture_section = ctk.CTkFrame(
            self.content,
            fg_color=self.CARD,
            corner_radius=15,
            border_width=1,
            border_color=self.BORDER
        )

        gesture_section.pack(
            fill="x",
            pady=10
        )

        gesture_header = ctk.CTkFrame(
            gesture_section,
            fg_color="transparent"
        )

        gesture_header.pack(
            fill="x",
            padx=24,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            gesture_header,
            text="CURRENT GESTURE",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.MUTED
        ).pack(
            side="left"
        )

        self.gesture_live_label = ctk.CTkLabel(
            gesture_header,
            text="LIVE",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=self.GREEN
        )

        self.gesture_live_label.pack(
            side="right"
        )

        self.gesture_value = ctk.CTkLabel(
            gesture_section,
            text="None",
            font=ctk.CTkFont(
                size=38,
                weight="bold"
            ),
            text_color=self.TEXT
        )

        self.gesture_value.pack(
            pady=(8, 5)
        )

        self.gesture_hint = ctk.CTkLabel(
            gesture_section,
            text="Waiting for hand gesture...",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=self.MUTED
        )

        self.gesture_hint.pack(
            pady=(0, 22)
        )

        # -----------------------------------------------------
        # PERFORMANCE
        # -----------------------------------------------------

        performance_card = ctk.CTkFrame(
            self.content,
            fg_color=self.CARD,
            corner_radius=15,
            border_width=1,
            border_color=self.BORDER
        )

        performance_card.pack(
            fill="x",
            pady=10
        )

        performance_top = ctk.CTkFrame(
            performance_card,
            fg_color="transparent"
        )

        performance_top.pack(
            fill="x",
            padx=24,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            performance_top,
            text="SYSTEM PERFORMANCE",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.MUTED
        ).pack(
            side="left"
        )

        self.performance_fps = ctk.CTkLabel(
            performance_top,
            text="0 FPS",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.BLUE
        )

        self.performance_fps.pack(
            side="right"
        )

        self.fps_progress = ctk.CTkProgressBar(
            performance_card,
            height=8,
            corner_radius=5,
            progress_color=self.BLUE,
            fg_color="#222C36"
        )

        self.fps_progress.pack(
            fill="x",
            padx=24,
            pady=(0, 20)
        )

        self.fps_progress.set(0)

        # -----------------------------------------------------
        # QUICK START
        # -----------------------------------------------------

        quick_title = ctk.CTkLabel(
            self.content,
            text="Quick Start",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        quick_title.pack(
            anchor="w",
            pady=(20, 8)
        )

        quick_card = ctk.CTkFrame(
            self.content,
            fg_color=self.CARD,
            corner_radius=15,
            border_width=1,
            border_color=self.BORDER
        )

        quick_card.pack(
            fill="x"
        )

        steps = [
            ("01", "Start", "Launch the virtual mouse"),
            ("02", "Position", "Place your hand in front of the camera"),
            ("03", "Control", "Use gestures to control your cursor"),
            ("04", "Stop", "Press STOP when finished")
        ]

        for number, title, description in steps:

            row = ctk.CTkFrame(
                quick_card,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=20,
                pady=10
            )

            number_label = ctk.CTkLabel(
                row,
                text=number,
                width=38,
                height=38,
                corner_radius=19,
                fg_color="#172B48",
                text_color="#60A5FA",
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                )
            )

            number_label.pack(
                side="left",
                padx=(0, 14)
            )

            text_frame = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )

            text_frame.pack(
                side="left"
            )

            ctk.CTkLabel(
                text_frame,
                text=title,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=self.TEXT
            ).pack(
                anchor="w"
            )

            ctk.CTkLabel(
                text_frame,
                text=description,
                font=ctk.CTkFont(
                    size=11
                ),
                text_color=self.MUTED
            ).pack(
                anchor="w"
            )

    # =========================================================
    # DASHBOARD STATUS CARD
    # =========================================================

    def create_dashboard_card(
        self,
        parent,
        column,
        title,
        value,
        icon
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=13,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5
        )

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=15,
            pady=(15, 4)
        )

        ctk.CTkLabel(
            top,
            text=icon,
            font=ctk.CTkFont(
                size=18
            ),
            text_color=self.BLUE
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=self.MUTED
        ).pack(
            anchor="w",
            padx=15
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            ),
            text_color=self.TEXT
        )

        value_label.pack(
            anchor="w",
            padx=15,
            pady=(3, 15)
        )

        return value_label

    # =========================================================
    # GESTURE PAGE
    # =========================================================

    def show_gestures(self):

        self.clear_content()

        self.set_active_nav(
            self.gesture_button
        )

        self.update_page_header(
            "Gesture Controls",
            "Learn how to interact with your computer"
        )

        intro = ctk.CTkFrame(
            self.content,
            fg_color="#111D2B",
            corner_radius=15,
            border_width=1,
            border_color="#1F3B60"
        )

        intro.pack(
            fill="x",
            pady=(10, 20)
        )

        ctk.CTkLabel(
            intro,
            text="✋",
            font=ctk.CTkFont(
                size=38
            ),
            text_color=self.BLUE
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            intro,
            text="Control your computer naturally",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack()

        ctk.CTkLabel(
            intro,
            text="Use these hand gestures to control the virtual mouse.",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=self.MUTED
        ).pack(
            pady=(5, 20)
        )

        gestures = [
            ("☝", "Index Finger", "Move Cursor",
             "Move the cursor around the screen"),

            ("👌", "Thumb + Index", "Left Click",
             "Quick pinch to perform a left click"),

            ("◎", "Quick Pinch ×2", "Double Click",
             "Perform two quick pinches"),

            ("🤏", "Hold Pinch", "Drag",
             "Hold thumb and index together"),

            ("✌", "Index + Middle", "Right Click",
             "Pinch index and middle fingers"),

            ("↕", "Two Fingers", "Scroll",
             "Move two fingers vertically"),

            ("✊", "Closed Fist", "Pause / Resume",
             "Hold a closed fist to pause")
        ]

        for icon, gesture, action, description in gestures:

            card = ctk.CTkFrame(
                self.content,
                fg_color=self.CARD,
                corner_radius=13,
                border_width=1,
                border_color=self.BORDER
            )

            card.pack(
                fill="x",
                pady=5
            )

            icon_label = ctk.CTkLabel(
                card,
                text=icon,
                width=55,
                font=ctk.CTkFont(
                    size=26
                ),
                text_color=self.BLUE
            )

            icon_label.pack(
                side="left",
                padx=(15, 5),
                pady=15
            )

            text_frame = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            text_frame.pack(
                side="left",
                fill="x",
                expand=True,
                pady=12
            )

            ctk.CTkLabel(
                text_frame,
                text=gesture,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=self.TEXT
            ).pack(
                anchor="w"
            )

            ctk.CTkLabel(
                text_frame,
                text=description,
                font=ctk.CTkFont(
                    size=11
                ),
                text_color=self.MUTED
            ).pack(
                anchor="w",
                pady=(2, 0)
            )

            action_badge = ctk.CTkLabel(
                card,
                text=action,
                height=30,
                corner_radius=15,
                fg_color="#172B48",
                text_color="#60A5FA",
                font=ctk.CTkFont(
                    size=10,
                    weight="bold"
                )
            )

            action_badge.pack(
                side="right",
                padx=18
            )

    # =========================================================
    # SETTINGS
    # =========================================================

    def show_settings(self):

        self.clear_content()

        self.set_active_nav(
            self.settings_button
        )

        self.update_page_header(
            "Settings",
            "Customize virtual mouse behaviour"
        )

        self.settings = control.read_settings()

        # -----------------------------------------------------
        # SETTINGS CARD
        # -----------------------------------------------------

        settings_card = ctk.CTkFrame(
            self.content,
            fg_color=self.CARD,
            corner_radius=15,
            border_width=1,
            border_color=self.BORDER
        )

        settings_card.pack(
            fill="x",
            pady=(10, 20)
        )

        ctk.CTkLabel(
            settings_card,
            text="Mouse Behaviour",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 4)
        )

        ctk.CTkLabel(
            settings_card,
            text="Fine-tune how gestures control your mouse.",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=self.MUTED
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # -----------------------------------------------------
        # SMOOTHING
        # -----------------------------------------------------

        self.create_setting_slider(
            settings_card,
            "Cursor Smoothing",
            "Controls how smoothly the cursor follows your finger.",
            0.05,
            1.0,
            float(self.settings["smoothing"]),
            self.update_smoothing_value,
            "smoothing"
        )

        # -----------------------------------------------------
        # SCROLL
        # -----------------------------------------------------

        self.create_setting_slider(
            settings_card,
            "Scroll Speed",
            "Controls the speed of vertical scrolling.",
            1,
            10,
            int(self.settings["scroll_speed"]),
            self.update_scroll_value,
            "scroll"
        )

        # -----------------------------------------------------
        # CONFIRMATION
        # -----------------------------------------------------

        self.create_setting_slider(
            settings_card,
            "Gesture Confirmation",
            "Frames required before a gesture is confirmed.",
            1,
            10,
            int(
                self.settings[
                    "gesture_confirmation_frames"
                ]
            ),
            self.update_confirmation_value,
            "confirmation"
        )

        # -----------------------------------------------------
        # BUTTONS
        # -----------------------------------------------------

        buttons = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x"
        )

        self.apply_button = ctk.CTkButton(
            buttons,
            text="✓  APPLY SETTINGS",
            height=42,
            width=180,
            corner_radius=9,
            fg_color=self.BLUE,
            hover_color=self.BLUE_HOVER,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=self.apply_settings
        )

        self.apply_button.pack(
            side="left",
            padx=(0, 10)
        )

        self.reset_button = ctk.CTkButton(
            buttons,
            text="↻  RESET DEFAULTS",
            height=42,
            width=170,
            corner_radius=9,
            fg_color="#263341",
            hover_color="#344454",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=self.reset_settings
        )

        self.reset_button.pack(
            side="left"
        )

        self.settings_status = ctk.CTkLabel(
            self.content,
            text="",
            font=ctk.CTkFont(
                size=12
            )
        )

        self.settings_status.pack(
            anchor="w",
            pady=(12, 5)
        )

    # =========================================================
    # SETTING SLIDER
    # =========================================================

    def create_setting_slider(
        self,
        parent,
        title,
        description,
        minimum,
        maximum,
        value,
        callback,
        slider_type
    ):

        container = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        container.pack(
            fill="x",
            padx=25,
            pady=10
        )

        top = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        top.pack(
            fill="x"
        )

        ctk.CTkLabel(
            top,
            text=title,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        if slider_type == "smoothing":

            self.smoothing_value = ctk.CTkLabel(
                top,
                text=f"{value:.2f}",
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=self.BLUE
            )

        elif slider_type == "scroll":

            self.scroll_value = ctk.CTkLabel(
                top,
                text=str(value),
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=self.BLUE
            )

        else:

            self.confirmation_value = ctk.CTkLabel(
                top,
                text=str(value),
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=self.BLUE
            )

        if slider_type == "smoothing":
            self.smoothing_value.pack(
                side="right"
            )

        elif slider_type == "scroll":
            self.scroll_value.pack(
                side="right"
            )

        else:
            self.confirmation_value.pack(
                side="right"
            )

        ctk.CTkLabel(
            container,
            text=description,
            font=ctk.CTkFont(
                size=11
            ),
            text_color=self.MUTED
        ).pack(
            anchor="w",
            pady=(3, 8)
        )

        slider = ctk.CTkSlider(
            container,
            from_=minimum,
            to=maximum,
            number_of_steps=(
                95
                if slider_type == "smoothing"
                else int(maximum - minimum)
            ),
            command=callback,
            progress_color=self.BLUE,
            button_color=self.TEXT,
            button_hover_color="#D7E0EA"
        )

        slider.pack(
            fill="x",
            pady=(0, 10)
        )

        slider.set(value)

        if slider_type == "smoothing":
            self.smoothing_slider = slider

        elif slider_type == "scroll":
            self.scroll_slider = slider

        else:
            self.confirmation_slider = slider

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

    # =========================================================
    # APPLY SETTINGS
    # =========================================================

    def apply_settings(self):

        smoothing = round(
            float(
                self.smoothing_slider.get()
            ),
            2
        )

        scroll_speed = round(
            float(
                self.scroll_slider.get()
            )
        )

        confirmation_frames = round(
            float(
                self.confirmation_slider.get()
            )
        )

        new_settings = {
            "smoothing": smoothing,
            "scroll_speed": scroll_speed,
            "gesture_confirmation_frames": confirmation_frames
        }

        if control.write_settings(
            new_settings
        ):

            self.settings = (
                control.read_settings()
            )

            self.settings_status.configure(
                text="✓ Settings saved successfully.",
                text_color=self.GREEN
            )

        else:

            self.settings_status.configure(
                text="✕ Failed to save settings.",
                text_color=self.RED
            )

    # =========================================================
    # RESET SETTINGS
    # =========================================================

    def reset_settings(self):

        if control.reset_settings():

            self.settings = (
                control.read_settings()
            )

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
                text="✓ Settings restored to defaults.",
                text_color=self.GREEN
            )

    # =========================================================
    # START
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
                text="●  RUNNING",
                state="disabled"
            )

            self.live_text.configure(
                text="SYSTEM ACTIVE"
            )

            self.live_text.configure(
                text_color=self.GREEN
            )

            self.live_dot.configure(
                text_color=self.GREEN
            )

            self.status_dot.configure(
                text_color=self.GREEN
            )

            self.sidebar_system_text.configure(
                text="Virtual mouse is running",
                text_color=self.GREEN
            )

        except Exception as error:

            print(
                f"Could not start main.py: {error}"
            )

    # =========================================================
    # PAUSE / RESUME
    # =========================================================

    def pause(self):

        if not self.running:
            return

        status = control.read_status()

        if status.get(
            "paused",
            False
        ):

            control.write_command(
                "resume"
            )

            self.pause_button.configure(
                text="Ⅱ  PAUSE"
            )

        else:

            control.write_command(
                "pause"
            )

            self.pause_button.configure(
                text="▶  RESUME"
            )

    # =========================================================
    # STOP
    # =========================================================

    def stop(self):

        control.write_command(
            "stop"
        )

        if self.process is not None:

            try:

                self.process.terminate()
                self.process.wait(
                    timeout=2
                )

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
            text="▶  START",
            state="normal"
        )

        self.pause_button.configure(
            text="Ⅱ  PAUSE"
        )

        self.live_text.configure(
            text="SYSTEM READY",
            text_color=self.MUTED
        )

        self.live_dot.configure(
            text_color=self.MUTED
        )

        self.status_dot.configure(
            text_color=self.MUTED
        )

        self.sidebar_system_text.configure(
            text="Ready",
            text_color=self.MUTED
        )

        if hasattr(
            self,
            "camera_card"
        ):

            self.camera_card.configure(
                text="READY"
            )

        if hasattr(
            self,
            "hand_card"
        ):

            self.hand_card.configure(
                text="READY"
            )

        if hasattr(
            self,
            "cursor_card"
        ):

            self.cursor_card.configure(
                text="READY"
            )

        if hasattr(
            self,
            "fps_card"
        ):

            self.fps_card.configure(
                text="0 FPS"
            )

        if hasattr(
            self,
            "gesture_value"
        ):

            self.gesture_value.configure(
                text="None"
            )

        if hasattr(
            self,
            "performance_fps"
        ):

            self.performance_fps.configure(
                text="0 FPS"
            )

        if hasattr(
            self,
            "fps_progress"
        ):

            self.fps_progress.set(0)

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

        # -----------------------------------------------------
        # DASHBOARD CARDS
        # -----------------------------------------------------

        if hasattr(
            self,
            "camera_card"
        ):

            self.camera_card.configure(
                text=camera
            )

        if hasattr(
            self,
            "hand_card"
        ):

            self.hand_card.configure(
                text=hand
            )

        if hasattr(
            self,
            "cursor_card"
        ):

            self.cursor_card.configure(
                text=cursor
            )

        if hasattr(
            self,
            "fps_card"
        ):

            self.fps_card.configure(
                text=f"{round(float(fps))} FPS"
            )

        # -----------------------------------------------------
        # GESTURE
        # -----------------------------------------------------

        if hasattr(
            self,
            "gesture_value"
        ):

            self.gesture_value.configure(
                text=gesture
            )

        if hasattr(
            self,
            "gesture_hint"
        ):

            if gesture == "None":
                self.gesture_hint.configure(
                    text="Waiting for hand gesture..."
                )

            elif gesture == "NO HAND":
                self.gesture_hint.configure(
                    text="Place your hand in front of the camera"
                )

            elif gesture == "PAUSED":
                self.gesture_hint.configure(
                    text="Virtual mouse is paused"
                )

            else:
                self.gesture_hint.configure(
                    text="Gesture detected successfully"
                )

        # -----------------------------------------------------
        # FPS
        # -----------------------------------------------------

        if hasattr(
            self,
            "performance_fps"
        ):

            self.performance_fps.configure(
                text=f"{round(float(fps))} FPS"
            )

        if hasattr(
            self,
            "fps_progress"
        ):

            progress = min(
                max(
                    float(fps) / 60,
                    0
                ),
                1
            )

            self.fps_progress.set(
                progress
            )

        # -----------------------------------------------------
        # SYSTEM STATE
        # -----------------------------------------------------

        if paused:

            self.live_text.configure(
                text="SYSTEM PAUSED",
                text_color=self.YELLOW
            )

            self.live_dot.configure(
                text_color=self.YELLOW
            )

            self.status_dot.configure(
                text_color=self.YELLOW
            )

            self.sidebar_system_text.configure(
                text="Virtual mouse paused",
                text_color=self.YELLOW
            )

        elif self.running:

            self.live_text.configure(
                text="SYSTEM ACTIVE",
                text_color=self.GREEN
            )

            self.live_dot.configure(
                text_color=self.GREEN
            )

            self.status_dot.configure(
                text_color=self.GREEN
            )

            self.sidebar_system_text.configure(
                text="Virtual mouse is running",
                text_color=self.GREEN
            )

        else:

            self.live_text.configure(
                text="SYSTEM READY",
                text_color=self.MUTED
            )

            self.live_dot.configure(
                text_color=self.MUTED
            )

            self.status_dot.configure(
                text_color=self.MUTED
            )

        # -----------------------------------------------------
        # PROCESS CHECK
        # -----------------------------------------------------

        if self.process is not None:

            if self.process.poll() is not None:

                self.process = None
                self.running = False

                self.start_button.configure(
                    text="▶  START",
                    state="normal"
                )

                self.pause_button.configure(
                    text="Ⅱ  PAUSE"
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
# APPLICATION ENTRY POINT
# =============================================================

if __name__ == "__main__":

    app = VirtualMouseUI()
    app.run()
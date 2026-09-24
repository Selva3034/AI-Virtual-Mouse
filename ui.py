import customtkinter as ctk
import subprocess
import sys
import os
import time

import cv2
from PIL import Image

import control


# ============================================================
# APPEARANCE
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================
# COLORS
# ============================================================

BG = "#090B14"
SIDEBAR = "#101326"

CARD = "#171A2B"
CARD_2 = "#1D2136"

WHITE = "#FFFFFF"
MUTED = "#9299B2"

PURPLE = "#8B5CF6"
PURPLE_LIGHT = "#A78BFA"

BLUE = "#3B82F6"
CYAN = "#06B6D4"

PINK = "#EC4899"
MAGENTA = "#D946EF"

GREEN = "#22C55E"
YELLOW = "#F59E0B"
RED = "#EF4444"

BORDER = "#292E45"


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_DIRECTORY = os.path.dirname(
    os.path.abspath(__file__)
)

MAIN_FILE = os.path.join(
    PROJECT_DIRECTORY,
    "main.py"
)


# ============================================================
# MAIN APPLICATION
# ============================================================

class VirtualMouseUI(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("AI Virtual Mouse")
        self.geometry("1250x750")
        self.minsize(1050, 650)

        self.configure(
            fg_color=BG
        )

        self.process = None
        self.running = False
        self.paused = False

        self.preview_capture = None
        self.preview_running = False
        self.preview_image = None
        self.preview_width = 640
        self.preview_height = 360

        self.current_page = "Dashboard"

        self.setup_ui()
        self.show_dashboard()

        self.update_dashboard()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )


    # ========================================================
    # UI SETUP
    # ========================================================

    def setup_ui(self):

        self.grid_columnconfigure(
            0,
            weight=0
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.create_sidebar()

        self.create_main_area()


    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0,
            fg_color=SIDEBAR
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # ----------------------------------------------------
        # BRAND
        # ----------------------------------------------------

        brand_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        brand_frame.pack(
            padx=25,
            pady=(30, 20),
            fill="x"
        )

        logo = ctk.CTkLabel(
            brand_frame,
            text="◉",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            ),
            text_color=PURPLE_LIGHT
        )

        logo.pack(
            side="left"
        )

        brand_text = ctk.CTkLabel(
            brand_frame,
            text="Virtual\nMouse",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=WHITE,
            justify="left"
        )

        brand_text.pack(
            side="left",
            padx=10
        )

        # ----------------------------------------------------
        # NAVIGATION TITLE
        # ----------------------------------------------------

        nav_title = ctk.CTkLabel(
            self.sidebar,
            text="NAVIGATION",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=MUTED
        )

        nav_title.pack(
            padx=25,
            pady=(10, 10),
            anchor="w"
        )

        # ----------------------------------------------------
        # NAV BUTTONS
        # ----------------------------------------------------

        self.dashboard_button = self.create_nav_button(
            "⌂   Dashboard",
            self.show_dashboard
        )

        self.dashboard_button.pack(
            padx=15,
            pady=5,
            fill="x"
        )

        self.gesture_button = self.create_nav_button(
            "✋   Gesture Controls",
            self.show_gestures
        )

        self.gesture_button.pack(
            padx=15,
            pady=5,
            fill="x"
        )

        self.settings_button = self.create_nav_button(
            "⚙   Settings",
            self.show_settings
        )

        self.settings_button.pack(
            padx=15,
            pady=5,
            fill="x"
        )

        # ----------------------------------------------------
        # SPACER
        # ----------------------------------------------------

        spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        spacer.pack(
            expand=True,
            fill="both"
        )

        # ----------------------------------------------------
        # SYSTEM STATUS
        # ----------------------------------------------------

        status_card = ctk.CTkFrame(
            self.sidebar,
            fg_color=CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER
        )

        status_card.pack(
            padx=15,
            pady=10,
            fill="x"
        )

        status_title = ctk.CTkLabel(
            status_card,
            text="SYSTEM STATUS",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=MUTED
        )

        status_title.pack(
            padx=15,
            pady=(15, 5),
            anchor="w"
        )

        self.system_status_label = ctk.CTkLabel(
            status_card,
            text="●  Offline",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=RED
        )

        self.system_status_label.pack(
            padx=15,
            pady=(0, 15),
            anchor="w"
        )

        # ----------------------------------------------------
        # STOP BUTTON
        # ----------------------------------------------------

        self.stop_button = ctk.CTkButton(
            self.sidebar,
            text="■   STOP",
            height=45,
            corner_radius=12,
            fg_color=RED,
            hover_color="#DC2626",
            text_color=WHITE,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.stop
        )

        self.stop_button.pack(
            padx=15,
            pady=8,
            fill="x"
        )

        # ----------------------------------------------------
        # PAUSE BUTTON
        # ----------------------------------------------------

        self.pause_button = ctk.CTkButton(
            self.sidebar,
            text="Ⅱ   PAUSE",
            height=45,
            corner_radius=12,
            fg_color=YELLOW,
            hover_color="#D97706",
            text_color=WHITE,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.toggle_pause
        )

        self.pause_button.pack(
            padx=15,
            pady=8,
            fill="x"
        )

        # ----------------------------------------------------
        # START BUTTON
        # ----------------------------------------------------

        self.start_button = ctk.CTkButton(
            self.sidebar,
            text="▶   START MOUSE",
            height=50,
            corner_radius=14,
            fg_color=PURPLE,
            hover_color="#7C3AED",
            text_color=WHITE,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.start
        )

        self.start_button.pack(
            padx=15,
            pady=(8, 25),
            fill="x"
        )


    # ========================================================
    # NAV BUTTON
    # ========================================================

    def create_nav_button(
        self,
        text,
        command
    ):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=45,
            corner_radius=10,
            fg_color="transparent",
            hover_color=CARD_2,
            text_color=MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=command
        )

        return button


    # ========================================================
    # MAIN AREA
    # ========================================================

    def create_main_area(self):

        self.main_area = ctk.CTkFrame(
            self,
            fg_color=BG,
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

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        self.header = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent",
            height=80
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(25, 5)
        )

        self.header.grid_columnconfigure(
            0,
            weight=1
        )

        self.page_title = ctk.CTkLabel(
            self.header,
            text="Dashboard",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=WHITE
        )

        self.page_title.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.page_subtitle = ctk.CTkLabel(
            self.header,
            text="Control your computer using hand gestures",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=MUTED
        )

        self.page_subtitle.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(3, 0)
        )

        # ----------------------------------------------------
        # CONTENT FRAME
        # ----------------------------------------------------

        self.content = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        self.content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=10
        )


    # ========================================================
    # CLEAR CONTENT
    # ========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()


    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.current_page = "Dashboard"

        self.page_title.configure(
            text="Dashboard"
        )

        self.page_subtitle.configure(
            text="Control your computer using hand gestures"
        )

        self.clear_content()

        self.dashboard_button.configure(
            fg_color=CARD_2,
            text_color=WHITE
        )

        self.gesture_button.configure(
            fg_color="transparent",
            text_color=MUTED
        )

        self.settings_button.configure(
            fg_color="transparent",
            text_color=MUTED
        )

        # ----------------------------------------------------
        # STATUS CARDS
        # ----------------------------------------------------

        cards = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        cards.pack(
            fill="x",
            pady=(5, 20)
        )

        for i in range(4):
            cards.grid_columnconfigure(
                i,
                weight=1
            )

        self.camera_card = self.create_status_card(
            cards,
            0,
            "◉",
            "CAMERA",
            "READY",
            CYAN
        )

        self.hand_card = self.create_status_card(
            cards,
            1,
            "✋",
            "HAND TRACKING",
            "READY",
            PURPLE
        )

        self.cursor_card = self.create_status_card(
            cards,
            2,
            "➤",
            "CURSOR",
            "READY",
            PINK
        )

        self.fps_card = self.create_status_card(
            cards,
            3,
            "⚡",
            "PERFORMANCE",
            "0 FPS",
            GREEN
        )

        # ----------------------------------------------------
        # MIDDLE AREA
        # ----------------------------------------------------

        middle = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        middle.pack(
            fill="both",
            expand=True
        )

        middle.grid_columnconfigure(
            0,
            weight=2
        )

        middle.grid_columnconfigure(
            1,
            weight=1
        )

        middle.grid_rowconfigure(
            0,
            weight=1
        )

        # ----------------------------------------------------
        # CAMERA PREVIEW
        # ----------------------------------------------------

        camera_panel = ctk.CTkFrame(
            middle,
            fg_color=CARD,
            corner_radius=20,
            border_width=1,
            border_color=BORDER
        )

        camera_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        camera_header = ctk.CTkFrame(
            camera_panel,
            fg_color="transparent"
        )

        camera_header.pack(
            fill="x",
            padx=20,
            pady=(15, 5)
        )

        camera_title = ctk.CTkLabel(
            camera_header,
            text="LIVE CAMERA PREVIEW",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=MUTED
        )

        camera_title.pack(
            side="left"
        )

        self.preview_status = ctk.CTkLabel(
            camera_header,
            text="● IDLE",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=GREEN
        )

        self.preview_status.pack(
            side="right"
        )

        self.preview_label = ctk.CTkLabel(
            camera_panel,
            text="Opening camera preview...",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=MUTED,
            fg_color="#0D101C",
            corner_radius=12
        )

        self.preview_label.pack(
            padx=20,
            pady=(8, 10),
            fill="both",
            expand=True
        )

        self.preview_info = ctk.CTkLabel(
            camera_panel,
            text="Preview is available while the Virtual Mouse is stopped.",
            font=ctk.CTkFont(
                size=11
            ),
            text_color=MUTED
        )

        self.preview_info.pack(
            pady=(0, 15)
        )

        # ----------------------------------------------------
        # QUICK ACTIONS + GESTURE
        # ----------------------------------------------------

        action_panel = ctk.CTkFrame(
            middle,
            fg_color=CARD,
            corner_radius=20,
            border_width=1,
            border_color=BORDER
        )

        action_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        action_title = ctk.CTkLabel(
            action_panel,
            text="CURRENT GESTURE",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=MUTED
        )

        action_title.pack(
            pady=(22, 5)
        )

        self.gesture_value = ctk.CTkLabel(
            action_panel,
            text="None",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=PURPLE_LIGHT
        )

        self.gesture_value.pack(
            pady=(5, 3)
        )

        self.gesture_description = ctk.CTkLabel(
            action_panel,
            text="Waiting for hand gesture...",
            font=ctk.CTkFont(
                size=11
            ),
            text_color=MUTED
        )

        self.gesture_description.pack(
            pady=(0, 15)
        )

        perf_title = ctk.CTkLabel(
            action_panel,
            text="SYSTEM PERFORMANCE",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=MUTED
        )

        perf_title.pack(
            pady=(5, 8)
        )

        self.performance_bar = ctk.CTkProgressBar(
            action_panel,
            height=10,
            corner_radius=8,
            progress_color=CYAN
        )

        self.performance_bar.pack(
            padx=25,
            fill="x"
        )

        self.performance_bar.set(0)

        self.performance_text = ctk.CTkLabel(
            action_panel,
            text="0 FPS",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=CYAN
        )

        self.performance_text.pack(
            pady=(6, 15)
        )

        action_separator = ctk.CTkLabel(
            action_panel,
            text="QUICK ACTIONS",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=MUTED
        )

        action_separator.pack(
            pady=(5, 8)
        )

        self.quick_start = ctk.CTkButton(
            action_panel,
            text="▶  Start Mouse",
            height=43,
            corner_radius=12,
            fg_color=GREEN,
            hover_color="#16A34A",
            command=self.start
        )

        self.quick_start.pack(
            padx=25,
            pady=6,
            fill="x"
        )

        self.quick_pause = ctk.CTkButton(
            action_panel,
            text="Ⅱ  Pause",
            height=43,
            corner_radius=12,
            fg_color=YELLOW,
            hover_color="#D97706",
            command=self.toggle_pause
        )

        self.quick_pause.pack(
            padx=25,
            pady=6,
            fill="x"
        )

        self.quick_stop = ctk.CTkButton(
            action_panel,
            text="■  Stop",
            height=43,
            corner_radius=12,
            fg_color=RED,
            hover_color="#DC2626",
            command=self.stop
        )

        self.quick_stop.pack(
            padx=25,
            pady=6,
            fill="x"
        )

        self.preview_info_action = ctk.CTkLabel(
            action_panel,
            text="Camera preview pauses when the mouse engine starts.",
            font=ctk.CTkFont(
                size=10
            ),
            text_color=MUTED,
            wraplength=210
        )

        self.preview_info_action.pack(
            padx=20,
            pady=(12, 10)
        )

        self.start_preview()


    # ========================================================
    # CAMERA PREVIEW
    # ========================================================

    def start_preview(self):

        if self.running:
            return

        if self.preview_capture is not None:
            return

        try:
            self.preview_capture = cv2.VideoCapture(
                0,
                cv2.CAP_DSHOW
            )

            if not self.preview_capture.isOpened():
                self.preview_capture.release()
                self.preview_capture = None

                if hasattr(self, "preview_label"):
                    self.preview_label.configure(
                        text="Camera preview unavailable.\nCheck your webcam.",
                        image=None
                    )

                if hasattr(self, "preview_status"):
                    self.preview_status.configure(
                        text="● OFFLINE",
                        text_color=RED
                    )

                return

            self.preview_capture.set(
                cv2.CAP_PROP_FRAME_WIDTH,
                self.preview_width
            )

            self.preview_capture.set(
                cv2.CAP_PROP_FRAME_HEIGHT,
                self.preview_height
            )

            self.preview_running = True

            if hasattr(self, "preview_status"):
                self.preview_status.configure(
                    text="● LIVE",
                    text_color=GREEN
                )

            if hasattr(self, "preview_info"):
                self.preview_info.configure(
                    text="Camera preview active. Start Mouse to begin gesture control."
                )

            self.update_preview()

        except Exception as error:

            self.preview_capture = None
            self.preview_running = False

            if hasattr(self, "preview_status"):
                self.preview_status.configure(
                    text="● ERROR",
                    text_color=RED
                )

            if hasattr(self, "preview_label"):
                self.preview_label.configure(
                    text=f"Camera error: {error}",
                    image=None
                )


    def stop_preview(self):

        self.preview_running = False

        if self.preview_capture is not None:

            try:
                self.preview_capture.release()
            except Exception:
                pass

        self.preview_capture = None


    def update_preview(self):

        if not self.preview_running:
            return

        if self.running:
            self.stop_preview()
            return

        try:

            if self.preview_capture is None:
                return

            success, frame = self.preview_capture.read()

            if not success:
                if hasattr(self, "preview_status"):
                    self.preview_status.configure(
                        text="● NO SIGNAL",
                        text_color=RED
                    )

                self.after(
                    500,
                    self.update_preview
                )

                return

            frame = cv2.flip(
                frame,
                1
            )

            # Add a simple preview overlay.
            cv2.rectangle(
                frame,
                (10, 10),
                (190, 48),
                (10, 14, 28),
                -1
            )

            cv2.putText(
                frame,
                "CAMERA PREVIEW",
                (22, 36),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )

            frame_rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(
                frame_rgb
            )

            image.thumbnail(
                (self.preview_width, self.preview_height)
            )

            self.preview_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(image.width, image.height)
            )

            self.preview_label.configure(
                image=self.preview_image,
                text=""
            )

            if hasattr(self, "preview_status"):
                self.preview_status.configure(
                    text="● LIVE",
                    text_color=GREEN
                )

        except Exception:
            pass

        if self.preview_running:
            self.after(
                40,
                self.update_preview
            )


    # ========================================================
    # STATUS CARD
    # ========================================================

    def create_status_card(
        self,
        parent,
        column,
        icon,
        title,
        value,
        color
    ):

        card = ctk.CTkFrame(
            parent,
            height=115,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=6
        )

        card.grid_propagate(False)

        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            ),
            text_color=color
        )

        icon_label.pack(
            padx=18,
            pady=(15, 2),
            anchor="w"
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=MUTED
        )

        title_label.pack(
            padx=18,
            anchor="w"
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=WHITE
        )

        value_label.pack(
            padx=18,
            pady=(3, 0),
            anchor="w"
        )

        return value_label


    # ========================================================
    # GESTURES PAGE
    # ========================================================

    def show_gestures(self):

        self.stop_preview()
        self.current_page = "Gestures"

        self.page_title.configure(
            text="Gesture Controls"
        )

        self.page_subtitle.configure(
            text="Available hand gestures and their actions"
        )

        self.clear_content()

        self.dashboard_button.configure(
            fg_color="transparent",
            text_color=MUTED
        )

        self.gesture_button.configure(
            fg_color=CARD_2,
            text_color=WHITE
        )

        self.settings_button.configure(
            fg_color="transparent",
            text_color=MUTED
        )

        gestures = [
            (
                "☝",
                "Index Finger",
                "Move the cursor",
                BLUE
            ),
            (
                "👌",
                "Thumb + Index",
                "Left click",
                PURPLE
            ),
            (
                "✌",
                "Index + Middle",
                "Right click",
                CYAN
            ),
            (
                "✋",
                "Two Fingers",
                "Scroll",
                PINK
            ),
            (
                "✊",
                "Closed Fist",
                "Pause / Resume",
                YELLOW
            ),
            (
                "👌",
                "Quick Pinch ×2",
                "Double click",
                MAGENTA
            ),
        ]

        container = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        container.pack(
            fill="both",
            expand=True
        )

        for i in range(2):
            container.grid_columnconfigure(
                i,
                weight=1
            )

        for i in range(3):
            container.grid_rowconfigure(
                i,
                weight=1
            )

        for index, gesture in enumerate(gestures):

            icon, name, action, color = gesture

            row = index // 2
            column = index % 2

            card = ctk.CTkFrame(
                container,
                fg_color=CARD,
                corner_radius=20,
                border_width=1,
                border_color=BORDER
            )

            card.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=8,
                pady=8
            )

            icon_label = ctk.CTkLabel(
                card,
                text=icon,
                font=ctk.CTkFont(
                    size=38,
                    weight="bold"
                ),
                text_color=color
            )

            icon_label.pack(
                pady=(25, 5)
            )

            name_label = ctk.CTkLabel(
                card,
                text=name,
                font=ctk.CTkFont(
                    size=17,
                    weight="bold"
                ),
                text_color=WHITE
            )

            name_label.pack(
                pady=5
            )

            action_label = ctk.CTkLabel(
                card,
                text=action,
                font=ctk.CTkFont(
                    size=13
                ),
                text_color=MUTED
            )

            action_label.pack()


    # ========================================================
    # SETTINGS PAGE
    # ========================================================

    def show_settings(self):

        self.stop_preview()
        self.current_page = "Settings"

        self.page_title.configure(
            text="Settings"
        )

        self.page_subtitle.configure(
            text="Customize virtual mouse behaviour"
        )

        self.clear_content()

        self.dashboard_button.configure(
            fg_color="transparent",
            text_color=MUTED
        )

        self.gesture_button.configure(
            fg_color="transparent",
            text_color=MUTED
        )

        self.settings_button.configure(
            fg_color=CARD_2,
            text_color=WHITE
        )

        settings = control.read_settings()

        # ----------------------------------------------------
        # SETTINGS CARD
        # ----------------------------------------------------

        settings_card = ctk.CTkFrame(
            self.content,
            fg_color=CARD,
            corner_radius=20,
            border_width=1,
            border_color=BORDER
        )

        settings_card.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # ----------------------------------------------------
        # SMOOTHING
        # ----------------------------------------------------

        smoothing_title = ctk.CTkLabel(
            settings_card,
            text="Cursor Smoothing",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color=WHITE
        )

        smoothing_title.pack(
            padx=30,
            pady=(30, 5),
            anchor="w"
        )

        smoothing_description = ctk.CTkLabel(
            settings_card,
            text="Controls how smoothly the cursor follows your finger.",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=MUTED
        )

        smoothing_description.pack(
            padx=30,
            anchor="w"
        )

        self.smoothing_value = ctk.CTkLabel(
            settings_card,
            text=f"{settings['smoothing']:.2f}",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=PURPLE_LIGHT
        )

        self.smoothing_value.pack(
            padx=30,
            pady=(15, 0),
            anchor="w"
        )

        self.smoothing_slider = ctk.CTkSlider(
            settings_card,
            from_=0.1,
            to=1.0,
            number_of_steps=18,
            command=self.update_smoothing_value,
            progress_color=PURPLE
        )

        self.smoothing_slider.pack(
            padx=30,
            pady=(8, 20),
            fill="x"
        )

        self.smoothing_slider.set(
            settings["smoothing"]
        )

        # ----------------------------------------------------
        # SCROLL SPEED
        # ----------------------------------------------------

        scroll_title = ctk.CTkLabel(
            settings_card,
            text="Scroll Speed",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color=WHITE
        )

        scroll_title.pack(
            padx=30,
            pady=(15, 5),
            anchor="w"
        )

        scroll_description = ctk.CTkLabel(
            settings_card,
            text="Controls scrolling speed when using two fingers.",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=MUTED
        )

        scroll_description.pack(
            padx=30,
            anchor="w"
        )

        self.scroll_value = ctk.CTkLabel(
            settings_card,
            text=str(settings["scroll_speed"]),
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=CYAN
        )

        self.scroll_value.pack(
            padx=30,
            pady=(15, 0),
            anchor="w"
        )

        self.scroll_slider = ctk.CTkSlider(
            settings_card,
            from_=1,
            to=10,
            number_of_steps=9,
            command=self.update_scroll_value,
            progress_color=CYAN
        )

        self.scroll_slider.pack(
            padx=30,
            pady=(8, 20),
            fill="x"
        )

        self.scroll_slider.set(
            settings["scroll_speed"]
        )

        # ----------------------------------------------------
        # CONFIRMATION FRAMES
        # ----------------------------------------------------

        confirmation_title = ctk.CTkLabel(
            settings_card,
            text="Gesture Confirmation",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color=WHITE
        )

        confirmation_title.pack(
            padx=30,
            pady=(15, 5),
            anchor="w"
        )

        confirmation_description = ctk.CTkLabel(
            settings_card,
            text="Number of frames required before a gesture is confirmed.",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=MUTED
        )

        confirmation_description.pack(
            padx=30,
            anchor="w"
        )

        self.confirmation_value = ctk.CTkLabel(
            settings_card,
            text=str(
                settings["gesture_confirmation_frames"]
            ),
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=PINK
        )

        self.confirmation_value.pack(
            padx=30,
            pady=(15, 0),
            anchor="w"
        )

        self.confirmation_slider = ctk.CTkSlider(
            settings_card,
            from_=1,
            to=10,
            number_of_steps=9,
            command=self.update_confirmation_value,
            progress_color=PINK
        )

        self.confirmation_slider.pack(
            padx=30,
            pady=(8, 25),
            fill="x"
        )

        self.confirmation_slider.set(
            settings["gesture_confirmation_frames"]
        )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        buttons = ctk.CTkFrame(
            settings_card,
            fg_color="transparent"
        )

        buttons.pack(
            padx=30,
            pady=(10, 30),
            fill="x"
        )

        self.apply_button = ctk.CTkButton(
            buttons,
            text="✓  Apply Settings",
            height=45,
            corner_radius=12,
            fg_color=GREEN,
            hover_color="#16A34A",
            command=self.apply_settings
        )

        self.apply_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 8)
        )

        self.reset_button = ctk.CTkButton(
            buttons,
            text="↻  Reset",
            height=45,
            corner_radius=12,
            fg_color=RED,
            hover_color="#DC2626",
            command=self.reset_settings
        )

        self.reset_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(8, 0)
        )


    # ========================================================
    # SETTINGS SLIDER VALUES
    # ========================================================

    def update_smoothing_value(
        self,
        value
    ):

        self.smoothing_value.configure(
            text=f"{float(value):.2f}"
        )


    def update_scroll_value(
        self,
        value
    ):

        self.scroll_value.configure(
            text=str(
                int(round(float(value)))
            )
        )


    def update_confirmation_value(
        self,
        value
    ):

        self.confirmation_value.configure(
            text=str(
                int(round(float(value)))
            )
        )


    # ========================================================
    # APPLY SETTINGS
    # ========================================================

    def apply_settings(self):

        smoothing = round(
            float(
                self.smoothing_slider.get()
            ),
            2
        )

        scroll_speed = int(
            round(
                float(
                    self.scroll_slider.get()
                )
            )
        )

        confirmation_frames = int(
            round(
                float(
                    self.confirmation_slider.get()
                )
            )
        )

        control.write_settings({
            "smoothing": smoothing,
            "scroll_speed": scroll_speed,
            "gesture_confirmation_frames": confirmation_frames
        })

        self.show_message(
            "Settings applied successfully.",
            GREEN
        )


    # ========================================================
    # RESET SETTINGS
    # ========================================================

    def reset_settings(self):

        control.reset_settings()

        self.show_settings()

        self.show_message(
            "Settings reset to default.",
            YELLOW
        )


    # ========================================================
    # START
    # ========================================================

    def start(self):

        # Already running
        if self.process is not None:

            if self.process.poll() is None:

                self.running = True

                self.show_message(
                    "Virtual Mouse is already running.",
                    YELLOW
                )

                return

        # Clear old runtime files
        control.clear_command()
        control.clear_status()

        # ----------------------------------------------------
        # Check main.py
        # ----------------------------------------------------

        if not os.path.exists(MAIN_FILE):

            self.show_message(
                "main.py was not found.",
                RED
            )

            return

        # ----------------------------------------------------
        # Launch
        # ----------------------------------------------------

        # Release the dashboard preview camera before main.py opens it.
        self.stop_preview()

        try:

            self.process = subprocess.Popen(
                [
                    sys.executable,
                    MAIN_FILE
                ],
                cwd=PROJECT_DIRECTORY
            )

            self.running = True
            self.paused = False

            self.system_status_label.configure(
                text="●  Running",
                text_color=GREEN
            )

            self.start_button.configure(
                text="●   RUNNING",
                fg_color=GREEN,
                hover_color="#16A34A"
            )

            self.pause_button.configure(
                text="Ⅱ   PAUSE"
            )

            if hasattr(self, "preview_status"):
                self.preview_status.configure(
                    text="● MOUSE ACTIVE",
                    text_color=GREEN
                )

            if hasattr(self, "preview_label"):
                self.preview_label.configure(
                    text="Virtual Mouse is running.\n\nThe main camera window is active.",
                    image=None
                )

            if hasattr(self, "preview_info"):
                self.preview_info.configure(
                    text="Camera preview is paused while the mouse engine is active."
                )

            self.show_message(
                "Virtual Mouse started.",
                GREEN
            )

        except Exception as error:

            self.process = None
            self.running = False

            self.show_message(
                f"Start error: {error}",
                RED
            )


    # ========================================================
    # PAUSE / RESUME
    # ========================================================

    def toggle_pause(self):

        if not self.running:

            self.show_message(
                "Start the Virtual Mouse first.",
                YELLOW
            )

            return

        if self.paused:

            control.write_command(
                "resume"
            )

            self.paused = False

            self.pause_button.configure(
                text="Ⅱ   PAUSE",
                fg_color=YELLOW,
                hover_color="#D97706"
            )

            self.quick_pause.configure(
                text="Ⅱ  Pause",
                fg_color=YELLOW,
                hover_color="#D97706"
            )

            self.show_message(
                "Virtual Mouse resumed.",
                GREEN
            )

        else:

            control.write_command(
                "pause"
            )

            self.paused = True

            self.pause_button.configure(
                text="▶   RESUME",
                fg_color=GREEN,
                hover_color="#16A34A"
            )

            self.quick_pause.configure(
                text="▶  Resume",
                fg_color=GREEN,
                hover_color="#16A34A"
            )

            self.show_message(
                "Virtual Mouse paused.",
                YELLOW
            )


    # ========================================================
    # STOP
    # ========================================================

    def stop(self):

        # ----------------------------------------------------
        # Nothing running
        # ----------------------------------------------------

        if self.process is None:

            self.running = False
            self.paused = False

            control.clear_command()
            control.clear_status()

            self.reset_ui_state()

            self.show_message(
                "Virtual Mouse is already stopped.",
                YELLOW
            )

            return

        # ----------------------------------------------------
        # Tell main.py to stop
        # ----------------------------------------------------

        try:

            control.write_command(
                "stop"
            )

        except Exception:

            pass

        # ----------------------------------------------------
        # Wait for main.py to stop normally
        # ----------------------------------------------------

        process_stopped = False

        for _ in range(20):

            try:

                if self.process.poll() is not None:

                    process_stopped = True
                    break

            except Exception:

                process_stopped = True
                break

            self.update()

            time.sleep(0.1)

        # ----------------------------------------------------
        # Force terminate if still running
        # ----------------------------------------------------

        if not process_stopped:

            try:

                self.process.terminate()

            except Exception:

                pass

            try:

                self.process.wait(
                    timeout=2
                )

            except Exception:

                try:

                    self.process.kill()

                except Exception:

                    pass

        # ----------------------------------------------------
        # Reset process
        # ----------------------------------------------------

        self.process = None
        self.running = False
        self.paused = False

        # ----------------------------------------------------
        # Clear runtime files
        # ----------------------------------------------------

        control.clear_command()
        control.clear_status()

        # ----------------------------------------------------
        # Reset UI
        # ----------------------------------------------------

        self.reset_ui_state()

        if self.current_page == "Dashboard":
            self.start_preview()

        self.show_message(
            "Virtual Mouse stopped.",
            RED
        )


    # ========================================================
    # RESET UI STATE
    # ========================================================

    def reset_ui_state(self):

        self.system_status_label.configure(
            text="●  Offline",
            text_color=RED
        )

        self.start_button.configure(
            text="▶   START MOUSE",
            fg_color=PURPLE,
            hover_color="#7C3AED"
        )

        self.pause_button.configure(
            text="Ⅱ   PAUSE",
            fg_color=YELLOW,
            hover_color="#D97706"
        )

        if hasattr(
            self,
            "quick_start"
        ):

            self.quick_start.configure(
                text="▶  Start Mouse",
                fg_color=GREEN,
                hover_color="#16A34A"
            )

        if hasattr(
            self,
            "quick_pause"
        ):

            self.quick_pause.configure(
                text="Ⅱ  Pause",
                fg_color=YELLOW,
                hover_color="#D97706"
            )


    # ========================================================
    # MESSAGE
    # ========================================================

    def show_message(
        self,
        message,
        color
    ):

        # Small temporary notification
        notification = ctk.CTkLabel(
            self,
            text=message,
            fg_color=color,
            text_color=WHITE,
            corner_radius=10,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        notification.place(
            relx=0.5,
            rely=0.95,
            anchor="center"
        )

        self.after(
            2500,
            notification.destroy
        )


    # ========================================================
    # DASHBOARD UPDATE
    # ========================================================

    def update_dashboard(self):

        try:

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

            # ------------------------------------------------
            # Check actual process
            # ------------------------------------------------

            if self.process is not None:

                if self.process.poll() is not None:

                    self.process = None
                    self.running = False
                    self.paused = False

                    control.clear_command()

                    self.reset_ui_state()

                    if self.current_page == "Dashboard":
                        self.start_preview()

            # ------------------------------------------------
            # Dashboard widgets
            # ------------------------------------------------

            if hasattr(
                self,
                "camera_card"
            ):

                self.camera_card.configure(
                    text=str(camera)
                )

            if hasattr(
                self,
                "hand_card"
            ):

                self.hand_card.configure(
                    text=str(hand)
                )

            if hasattr(
                self,
                "cursor_card"
            ):

                self.cursor_card.configure(
                    text=str(cursor)
                )

            if hasattr(
                self,
                "fps_card"
            ):

                self.fps_card.configure(
                    text=f"{fps} FPS"
                )

            if hasattr(
                self,
                "gesture_value"
            ):

                self.gesture_value.configure(
                    text=str(gesture)
                )

            if hasattr(
                self,
                "gesture_description"
            ):

                if paused:

                    self.gesture_description.configure(
                        text="Virtual Mouse is paused.",
                        text_color=YELLOW
                    )

                elif gesture and gesture != "None":

                    self.gesture_description.configure(
                        text="Gesture detected.",
                        text_color=GREEN
                    )

                else:

                    self.gesture_description.configure(
                        text="Waiting for hand gesture...",
                        text_color=MUTED
                    )

            if hasattr(
                self,
                "performance_bar"
            ):

                fps_value = float(fps)

                performance = min(
                    fps_value / 60.0,
                    1.0
                )

                self.performance_bar.set(
                    performance
                )

            if hasattr(
                self,
                "performance_text"
            ):

                self.performance_text.configure(
                    text=f"{fps} FPS"
                )

            # ------------------------------------------------
            # Status
            # ------------------------------------------------

            if self.running:

                if self.paused:

                    self.system_status_label.configure(
                        text="●  Paused",
                        text_color=YELLOW
                    )

                else:

                    self.system_status_label.configure(
                        text="●  Running",
                        text_color=GREEN
                    )

        except Exception:

            pass

        self.after(
            300,
            self.update_dashboard
        )


    # ========================================================
    # WINDOW CLOSE
    # ========================================================

    def on_close(self):

        try:

            self.stop()

        except Exception:

            pass

        try:

            control.clear_command()
            control.clear_status()

        except Exception:

            pass

        self.destroy()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app = VirtualMouseUI()

    app.mainloop()
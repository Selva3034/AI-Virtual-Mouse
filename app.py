import customtkinter as ctk
import subprocess
import sys
import os


class VirtualMouseApp:

    def __init__(self):

        # =================================================
        # APPEARANCE
        # =================================================

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # =================================================
        # WINDOW
        # =================================================

        self.root = ctk.CTk()

        self.root.title("AI Virtual Mouse")

        self.root.geometry("720x650")

        self.root.resizable(False, False)

        # Virtual mouse process
        self.process = None

        # =================================================
        # TITLE
        # =================================================

        self.title_label = ctk.CTkLabel(
            self.root,
            text="AI Virtual Mouse",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        self.title_label.pack(
            pady=(25, 5)
        )

        # =================================================
        # SUBTITLE
        # =================================================

        self.subtitle_label = ctk.CTkLabel(
            self.root,
            text="Hand Gesture Based Computer Control",
            font=ctk.CTkFont(
                size=14
            )
        )

        self.subtitle_label.pack(
            pady=(0, 15)
        )

        # =================================================
        # STATUS CARD
        # =================================================

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
            pady=15
        )

        # =================================================
        # GESTURE TITLE
        # =================================================

        gesture_title = ctk.CTkLabel(
            self.root,
            text="Gesture Controls",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        gesture_title.pack(
            pady=(10, 8)
        )

        # =================================================
        # GESTURES
        # =================================================

        gestures = [
            "Index Finger       → Move Cursor",
            "Thumb + Index      → Left Click",
            "Quick Pinch Twice  → Double Click",
            "Hold Pinch         → Drag & Drop",
            "Index + Middle     → Right Click",
            "Two Fingers        → Scroll",
            "Closed Fist        → Pause / Resume"
        ]

        for gesture in gestures:

            label = ctk.CTkLabel(
                self.root,
                text=gesture,
                font=ctk.CTkFont(
                    size=13
                ),
                anchor="w"
            )

            label.pack(
                padx=110,
                pady=2,
                anchor="w"
            )

        # =================================================
        # BUTTON FRAME
        # =================================================

        button_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=20
        )

        # =================================================
        # START BUTTON
        # =================================================

        self.start_button = ctk.CTkButton(
            button_frame,
            text="START",
            width=150,
            height=42,
            command=self.start_mouse
        )

        self.start_button.grid(
            row=0,
            column=0,
            padx=8
        )

        # =================================================
        # STOP BUTTON
        # =================================================

        self.stop_button = ctk.CTkButton(
            button_frame,
            text="STOP",
            width=150,
            height=42,
            command=self.stop_mouse
        )

        self.stop_button.grid(
            row=0,
            column=1,
            padx=8
        )

        # =================================================
        # EXIT BUTTON
        # =================================================

        self.exit_button = ctk.CTkButton(
            button_frame,
            text="EXIT",
            width=150,
            height=42,
            command=self.exit_application
        )

        self.exit_button.grid(
            row=0,
            column=2,
            padx=8
        )

        # =================================================
        # FOOTER
        # =================================================

        footer = ctk.CTkLabel(
            self.root,
            text="ESC can be used inside the camera window to stop",
            font=ctk.CTkFont(
                size=11
            )
        )

        footer.pack(
            pady=(0, 10)
        )

        # =================================================
        # WINDOW CLOSE
        # =================================================

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.exit_application
        )

        # =================================================
        # CHECK PROCESS STATUS
        # =================================================

        self.check_process()

    # =====================================================
    # START VIRTUAL MOUSE
    # =====================================================

    def start_mouse(self):

        # -------------------------------------------------
        # CHECK IF ALREADY RUNNING
        # -------------------------------------------------

        if self.process is not None:

            if self.process.poll() is None:

                self.status_label.configure(
                    text="● SYSTEM ALREADY RUNNING"
                )

                return

        try:

            # -------------------------------------------------
            # PROJECT DIRECTORY
            # -------------------------------------------------

            project_folder = os.path.dirname(
                os.path.abspath(__file__)
            )

            # -------------------------------------------------
            # MAIN.PY
            # -------------------------------------------------

            main_file = os.path.join(
                project_folder,
                "main.py"
            )

            # -------------------------------------------------
            # CHECK MAIN.PY
            # -------------------------------------------------

            if not os.path.isfile(main_file):

                self.status_label.configure(
                    text="● main.py NOT FOUND"
                )

                print()
                print("ERROR: main.py was not found.")
                print(
                    f"Expected location: {main_file}"
                )

                return

            # -------------------------------------------------
            # TERMINAL INFORMATION
            # -------------------------------------------------

            print()
            print("=" * 60)
            print("STARTING AI VIRTUAL MOUSE")
            print("=" * 60)

            print(
                f"Python interpreter:"
            )

            print(
                sys.executable
            )

            print()

            print(
                f"Project folder:"
            )

            print(
                project_folder
            )

            print()

            print(
                f"Main file:"
            )

            print(
                main_file
            )

            print()
            print(
                "Launching main.py..."
            )
            print()

            # -------------------------------------------------
            # START MAIN.PY
            # -------------------------------------------------

            self.process = subprocess.Popen(
                [
                    sys.executable,
                    "-u",
                    main_file
                ],
                cwd=project_folder
            )

            # -------------------------------------------------
            # UPDATE GUI
            # -------------------------------------------------

            self.status_label.configure(
                text="● STARTING..."
            )

            self.start_button.configure(
                state="disabled"
            )

            # -------------------------------------------------
            # CHECK WHETHER PROCESS STARTED
            # -------------------------------------------------

            self.root.after(
                1000,
                self.check_start_result
            )

        except Exception as error:

            print()
            print("=" * 60)
            print("ERROR STARTING VIRTUAL MOUSE")
            print("=" * 60)

            print(error)

            self.status_label.configure(
                text="● START ERROR"
            )

            self.start_button.configure(
                state="normal"
            )

    # =====================================================
    # CHECK START RESULT
    # =====================================================

    def check_start_result(self):

        if self.process is None:

            self.status_label.configure(
                text="● SYSTEM READY"
            )

            return

        # -------------------------------------------------
        # PROCESS STILL RUNNING
        # -------------------------------------------------

        if self.process.poll() is None:

            self.status_label.configure(
                text="● SYSTEM ACTIVE"
            )

            print(
                "Virtual mouse process is running."
            )

        # -------------------------------------------------
        # PROCESS ALREADY EXITED
        # -------------------------------------------------

        else:

            exit_code = self.process.returncode

            print()
            print(
                "main.py stopped immediately."
            )

            print(
                f"Exit code: {exit_code}"
            )

            self.status_label.configure(
                text="● VIRTUAL MOUSE STOPPED"
            )

            self.process = None

            self.start_button.configure(
                state="normal"
            )

    # =====================================================
    # CHECK PROCESS CONTINUOUSLY
    # =====================================================

    def check_process(self):

        if self.process is not None:

            # Process finished
            if self.process.poll() is not None:

                exit_code = self.process.returncode

                print()
                print(
                    "Virtual mouse process ended."
                )

                print(
                    f"Exit code: {exit_code}"
                )

                self.process = None

                self.status_label.configure(
                    text="● SYSTEM STOPPED"
                )

                self.start_button.configure(
                    state="normal"
                )

        # Check again after 500 ms
        self.root.after(
            500,
            self.check_process
        )

    # =====================================================
    # STOP VIRTUAL MOUSE
    # =====================================================

    def stop_mouse(self):

        if self.process is None:

            self.status_label.configure(
                text="● SYSTEM READY"
            )

            self.start_button.configure(
                state="normal"
            )

            return

        try:

            # -------------------------------------------------
            # CHECK PROCESS
            # -------------------------------------------------

            if self.process.poll() is None:

                print()
                print(
                    "Stopping virtual mouse..."
                )

                # Ask process to terminate
                self.process.terminate()

                try:

                    self.process.wait(
                        timeout=3
                    )

                    print(
                        "Virtual mouse stopped."
                    )

                except subprocess.TimeoutExpired:

                    print(
                        "Process did not stop normally."
                    )

                    print(
                        "Force stopping..."
                    )

                    self.process.kill()

                    self.process.wait(
                        timeout=2
                    )

                    print(
                        "Virtual mouse force stopped."
                    )

            else:

                print(
                    "Virtual mouse process already stopped."
                )

        except Exception as error:

            print()
            print(
                "Error stopping virtual mouse:"
            )

            print(error)

        finally:

            self.process = None

            self.status_label.configure(
                text="● SYSTEM STOPPED"
            )

            self.start_button.configure(
                state="normal"
            )

    # =====================================================
    # EXIT APPLICATION
    # =====================================================

    def exit_application(self):

        print()
        print(
            "Closing AI Virtual Mouse..."
        )

        # Stop main.py first
        self.stop_mouse()

        # Close GUI
        self.root.destroy()

        print(
            "Application closed."
        )


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    app = VirtualMouseApp()

    app.root.mainloop()
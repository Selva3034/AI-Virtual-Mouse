import json
import os


# =========================================================
# FILE PATHS
# =========================================================

PROJECT_DIRECTORY = os.path.dirname(
    os.path.abspath(__file__)
)

CONTROL_FILE = os.path.join(
    PROJECT_DIRECTORY,
    "control.json"
)

STATUS_FILE = os.path.join(
    PROJECT_DIRECTORY,
    "status.json"
)

SETTINGS_FILE = os.path.join(
    PROJECT_DIRECTORY,
    "settings.json"
)


# =========================================================
# DEFAULT SETTINGS
# =========================================================

DEFAULT_SETTINGS = {

    "smoothing": 0.5,

    "scroll_speed": 3,

    "gesture_confirmation_frames": 3

}


# =========================================================
# COMMAND FUNCTIONS
# =========================================================

def write_command(command):

    data = {
        "command": command
    }

    try:

        with open(
            CONTROL_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    except Exception as error:

        print(
            f"Control write error: {error}"
        )


def read_command():

    if not os.path.exists(
        CONTROL_FILE
    ):

        return None

    try:

        with open(
            CONTROL_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

        return data.get(
            "command"
        )

    except Exception:

        return None


def clear_command():

    try:

        if os.path.exists(
            CONTROL_FILE
        ):

            os.remove(
                CONTROL_FILE
            )

    except Exception:

        pass


# =========================================================
# STATUS FUNCTIONS
# =========================================================

def write_status(
    camera="READY",
    hand="READY",
    cursor="READY",
    gesture="None",
    fps=0,
    paused=False
):

    data = {

        "camera": camera,

        "hand": hand,

        "cursor": cursor,

        "gesture": gesture,

        "fps": fps,

        "paused": paused

    }

    try:

        with open(
            STATUS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    except Exception:

        pass


def read_status():

    default_status = {

        "camera": "READY",

        "hand": "READY",

        "cursor": "READY",

        "gesture": "None",

        "fps": 0,

        "paused": False

    }

    if not os.path.exists(
        STATUS_FILE
    ):

        return default_status

    try:

        with open(
            STATUS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

        default_status.update(
            data
        )

        return default_status

    except Exception:

        return default_status


def clear_status():

    try:

        if os.path.exists(
            STATUS_FILE
        ):

            os.remove(
                STATUS_FILE
            )

    except Exception:

        pass


# =========================================================
# SETTINGS FUNCTIONS
# =========================================================

def write_settings(settings):

    try:

        current_settings = read_settings()

        current_settings.update(
            settings
        )

        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                current_settings,
                file,
                indent=4
            )

        return True

    except Exception as error:

        print(
            f"Settings write error: {error}"
        )

        return False


def read_settings():

    if not os.path.exists(
        SETTINGS_FILE
    ):

        return DEFAULT_SETTINGS.copy()

    try:

        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

        settings = DEFAULT_SETTINGS.copy()

        settings.update(
            data
        )

        return settings

    except Exception:

        return DEFAULT_SETTINGS.copy()


def reset_settings():

    try:

        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                DEFAULT_SETTINGS,
                file,
                indent=4
            )

        return True

    except Exception as error:

        print(
            f"Settings reset error: {error}"
        )

        return False


# =========================================================
# GET SINGLE SETTING
# =========================================================

def get_setting(
    key,
    default=None
):

    settings = read_settings()

    return settings.get(
        key,
        default
    )


# =========================================================
# SET SINGLE SETTING
# =========================================================

def set_setting(
    key,
    value
):

    return write_settings(
        {
            key: value
        }
    )


# =========================================================
# CLEAR SETTINGS
# =========================================================

def clear_settings():

    try:

        if os.path.exists(
            SETTINGS_FILE
        ):

            os.remove(
                SETTINGS_FILE
            )

    except Exception:

        pass
import json
import os


# =========================================================
# CONTROL FILE
# =========================================================

CONTROL_FILE = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    "control.json"
)


# =========================================================
# WRITE COMMAND
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
                file
            )

    except Exception as error:

        print(
            f"Control write error: {error}"
        )


# =========================================================
# READ COMMAND
# =========================================================

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


# =========================================================
# CLEAR COMMAND
# =========================================================

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
import json
from datetime import datetime


def json_to_console(data: str) -> None:

    print("----------------------------------------")
    print(json.dumps(data))
    print()


def message_to_console(message):
    print("<!------!>")
    print(datetime.now())
    print(
        "Message от {0} {1} (id = {2}) \n {3}".format(
            message.from_user.first_name,
            message.from_user.last_name,
            str(message.from_user.id),
            message.text,
        )
    )

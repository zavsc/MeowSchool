import datetime

from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback


# keyboard for select data
def diary_week(date_str: str):
    today_date = datetime.date.today()
    user_date = datetime.date(*map(int, date_str.split(".")[::-1]))
    keyboard = Keyboard(inline=True)

    # add days in one week
    for i in range(0, 3):
        date = (user_date - datetime.timedelta(days=user_date.weekday() - i)).strftime("%d.%m.%Y")
        if user_date.weekday() == i:
            color = KeyboardButtonColor.POSITIVE
        elif today_date.strftime("%d.%m.%Y") == date:
            color = KeyboardButtonColor.PRIMARY
        else:
            color = KeyboardButtonColor.SECONDARY
        keyboard.add(Callback(
            date, {"keyboard": "diary", "date": date}
        ), color)

    keyboard.row()

    for i in range(3, 6):
        date = (user_date - datetime.timedelta(days=user_date.weekday() - i)).strftime("%d.%m.%Y")
        if user_date.weekday() == i:
            color = KeyboardButtonColor.POSITIVE
        elif today_date.strftime("%d.%m.%Y") == date:
            color = KeyboardButtonColor.PRIMARY
        else:
            color = KeyboardButtonColor.SECONDARY
        keyboard.add(Callback(
            date, {"keyboard": "diary", "date": date}
        ), color)

    keyboard.row()

    # add week control
    keyboard.add(Callback(
        "Неделя -", {"keyboard": "diary", "date": (user_date - datetime.timedelta(weeks=1)).strftime("%d.%m.%Y")}
    ), KeyboardButtonColor.SECONDARY)
    keyboard.add(Callback(
        "Неделя +", {"keyboard": "diary", "date": (user_date + datetime.timedelta(weeks=1)).strftime("%d.%m.%Y")}
    ), KeyboardButtonColor.SECONDARY)

    return keyboard.get_json()


def menu():
    keyboard = (
        Keyboard()
        .add(Text("Дневник", payload={"keyboard": "menu", "menu": "diary"}), KeyboardButtonColor.SECONDARY)
        .add(Text("Оценки", payload={"keyboard": "menu", "menu": "marks"}), KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text("Настройки", payload={"keyboard": "menu", "menu": "settings"}), KeyboardButtonColor.SECONDARY)
    )
    return keyboard.get_json()


def empty():
    return Keyboard().get_json()


def auth():
    keyboard = (
        Keyboard(one_time=True)
        .add(Text("Авторизоваться", payload={"keyboard": "auth"}), KeyboardButtonColor.SECONDARY)
    )
    return keyboard.get_json()


def marks_stats(more: bool = False):
    keyboard = Keyboard(inline=True)
    if more:
        keyboard.add(Callback("Скрыть", {"keyboard": "marks", "more": False}), KeyboardButtonColor.SECONDARY)
    else:
        keyboard.add(Callback("Подробнее", {"keyboard": "marks", "more": True}), KeyboardButtonColor.SECONDARY)
    return keyboard.get_json()
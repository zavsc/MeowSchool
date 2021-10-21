from typing import List

from vkbottle.framework.abc_blueprint import ABCBlueprint

from . import admin, chat_message, private_message

bp_list: List[ABCBlueprint] = [
    private_message.bp,
    chat_message.bp,
    admin.bp,
]
from typing import Tuple

from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.dispenser import get_state_repr
from vkbottle.dispatch.rules.bot import ChatActionRule, CommandRule, PeerRule
from vkbottle.framework.bot import BotLabeler
from vkbottle.modules import logger
from vkbottle_types.objects import MessagesMessageActionStatus

from bot import db, keyboards
from bot.blueprints.other import AuthState, admin_log, tomorrow
from bot.error_handler import diary_date_error_handler, error_handler
from diary import DiaryApi

labeler = BotLabeler(auto_rules=[PeerRule(True)])

bp = Blueprint(name="PrivateMessage", labeler=labeler)


@bp.on.message(ChatActionRule(MessagesMessageActionStatus.CHAT_INVITE_USER.value))
@error_handler.catch
async def invite_message(message: Message):
    if message.action.member_id == bp.polling.group_id:  # type: ignore
        await message.answer(
            "Спасибо, что вы решили воспользоваться моим ботом. "
            "Напишите /начать (/start), что бы авторизовать беседу"
        )


@bp.on.message(CommandRule("помощь") | CommandRule("help"))
@error_handler.catch
async def help_command(message: Message):
    await message.answer(
        "Список всех команд:\n\n"
        "/помощь -- Собственно, этот список\n"
        "/начать -- Авторизовать беседу\n"
        "\nКоманды, повторяющие меню:\n"
        "/дневник -- Посмотреть дневник на завтра"
        "/дневник дд.мм.гггг -- Посмотреть дневник (домашнее задания, оценки)\n"
        "\nДля всех команд есть английские алиасы (help, start, diary)."
    )


@bp.on.message(CommandRule("начать") | CommandRule("start"))
@error_handler.catch
async def start_command(message: Message):
    if message.state_peer is None:  # if chat is not auth
        user_state_peer = await bp.state_dispenser.get(message.from_id)

        # check auth of user
        if user_state_peer is None or user_state_peer.state != get_state_repr(AuthState.AUTH):
            await message.answer(
                "Для начала, нужно авторизоваться в личных сообщениях бота: vk.me/schoolbot04, "
                "затем снова написать /начать (/start).",
                reply_to=message.id
            )

        else:
            await bp.state_dispenser.set(message.peer_id, AuthState.AUTH, api=user_state_peer.payload["api"])\

            db.add_chat(message.peer_id, message.from_id)

            await message.answer(
                "Беседа успешна авторизована! Напишите /помощь (/help) для получения списка всех команд.",
                reply_to=message.id
            )
            await admin_log("Новая беседа авторизована.")
            logger.info(f"Auth new chat: {message.peer_id}")
    else:
        await message.answer(
            "Беседа уже авторизована!\n"
            "Воспользуйтесь командой /помощь (/help) для получения списка команд.",
            reply_to=message.id
        )


@bp.on.message(CommandRule("дневник", args_count=1) | CommandRule("diary", args_count=1), state=AuthState.AUTH)
@diary_date_error_handler.catch
async def diary_command(message: Message, args: Tuple[str]):
    date = args[0]
    api: DiaryApi = message.state_peer.payload["api"]
    diary = await api.diary(date)
    await message.answer(
        message=diary.info(is_chat=True),
        keyboard=keyboards.diary_week(date),
        dont_parse_links=True
    )


@bp.on.message(CommandRule("дневник") | CommandRule("diary"), state=AuthState.AUTH)
@diary_date_error_handler.catch
async def diary_tomorrow_command(message: Message):
    return await diary_command(message, (tomorrow(),))  # type: ignore


@bp.on.message(text="/<command>")
async def undefined_command(message: Message, command: str):
    await message.answer(
        message=f"Команда \"/{command}\" не найдена. Возможно, был использован неправильный формат.\n"
                "Воспользуйтесь командой /помощь (/help) для получения списка команд.",
        reply_to=message.id
    )

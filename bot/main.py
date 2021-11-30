import sys

from vkbottle import LoopWrapper
from vkbottle.bot import Bot
from vkbottle_callback import MessageEventLabeler

from diary import DiaryApi
from . import db
from .blueprints import admin, admin_log, auth_users_and_chats, chat, message_event, other, private, scheduler
from .error_handler import vkbottle_error_handler

if len(sys.argv) < 2:
    raise ValueError("Token is undefined")
TOKEN = sys.argv[1]


async def _close_session():
    await admin_log("Система отключается.")
    scheduler.stop()
    await db.close()
    for peer_id, state_peer in bot.state_dispenser.dictionary.items():
        if peer_id < 2000000000:  # if user
            api: DiaryApi = state_peer.payload.get("api")
            if api:  # not None
                await api.close()


labeler = MessageEventLabeler()
loop_wrapper = LoopWrapper(
    on_startup=[
        db.start_up(),
        auth_users_and_chats(),
        scheduler.start()
    ],
    on_shutdown=[
        _close_session()
    ]
)

bot = Bot(TOKEN, labeler=labeler, loop_wrapper=loop_wrapper, error_handler=vkbottle_error_handler)

bps = [admin.bp, chat.bp, message_event.bp, other.bp, private.bp, scheduler.bp]

for bp in bps:
    bp.load(bot)

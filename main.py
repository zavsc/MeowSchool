import asyncio
import atexit

from bot import auth_users_and_chats, bot, create_tables
from bot.blueprints.other import admin_log
from diary import DiaryApi


@atexit.register
def close_session():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(admin_log("Система отключается."))
    for state_peer in bot.state_dispenser.dictionary.values():
        api: DiaryApi = state_peer.payload.get("api")
        if api:  # not None
            loop.run_until_complete(api.close())
    print("\nPlease, reboot me ^-^\n")


if __name__ == '__main__':
    create_tables()
    bot.loop.run_until_complete(auth_users_and_chats())
    bot.run_forever()

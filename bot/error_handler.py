from loguru import logger
from vkbottle import ErrorHandler, VKAPIError
from vkbottle.bot import Message

from diary.types import APIError

HANDLER = ErrorHandler(redirect_arguments=True)


@HANDLER.register_error_handler(APIError)
async def exc_handler_diary_api(e: APIError, m: Message):
    if not e.resp.ok:
        if e.resp.status is 401:
            logger.info(f"Re-auth {m.peer_id}")
            await m.answer("Проблемы с авторизацией. Необходимо переподключиться")  # todo
        logger.warning(f"Server error {e.resp.status}")
        await m.answer("Временные неполадки с сервером. Повторите попытку позже")

    if not e.json_success:
        logger.warning(f"Server error {e.resp.status} {await e.resp.json()}")
        await m.answer("Временные неполадки с сервером. Повторите попытку позже")


@HANDLER.register_error_handler(VKAPIError())
async def exc_handler_vk_api(e: VKAPIError, m: Message):
    logger.warning(f"VKApi error {e}")
    await m.answer("Временные неполадки с сервером. Повторите попытку позже")


@HANDLER.register_undefined_error_handler()
async def exc_handler(e: BaseException, m: Message):
    logger.warning(f"Undefined error {e}")
    await m.answer("Временные неполадки с сервером. Повторите попытку позже")
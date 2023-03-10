import os
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


BOT_API_TOKEN = os.getenv("BOT_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=BOT_API_TOKEN)
# using simple MemoryStorage for Dispatcher
dp = Dispatcher(bot, storage=MemoryStorage())

# Состояния для машины состояний бота
class BotStates(StatesGroup):
    STATE_1 = State()
    STATE_2 = State()
    STATE_3 = State()


@dp.message_handler(state="*",  commands=["start"])
async def handler_command_start(msg: types.Message):

    buttonOdin = InlineKeyboardButton(
        text="Odin", callback_data="odin")
    buttonDva = InlineKeyboardButton(
        text="Dva", callback_data="dva")

    kb_inline = InlineKeyboardMarkup().add(buttonOdin)
    kb_inline.add(buttonDva)
    await msg.answer("Выбери вариант", reply_markup=kb_inline)


@dp.callback_query_handler(state="*", text=["odin"])
async def handler_command_odin(call: types.CallbackQuery):
    """
    This handler will be called when user sends `/odin` command
    """
    state = dp.current_state(user=call.message.from_user.id)
    current_state = await state.get_state()
    await call.message.answer(f"handler odin before state: {current_state}")
    await state.set_state(BotStates.STATE_1)
    current_state = await state.get_state()
    await call.message.answer(f"handler odin after state: {current_state}")


@dp.callback_query_handler(state="*", text=['dva'])
async def handler_command_dva(call: types.CallbackQuery):

    state = dp.current_state(user=call.message.from_user.id)
    current_state = await state.get_state()
    await call.message.answer(f"handler dva before state: {current_state}")
    await state.set_state(BotStates.STATE_2)
    current_state = await state.get_state()
    buttonTri = InlineKeyboardButton(
        text="Tri", callback_data="tri")
    kb_inline = InlineKeyboardMarkup().add(buttonTri)
    await call.message.answer(f"handler dva after state: {current_state}", reply_markup=kb_inline)


@dp.callback_query_handler(state=BotStates.STATE_2, text=['tri'])
async def handler_command_tri(call: types.CallbackQuery):

    state = dp.current_state(user=call.message.from_user.id)
    current_state = await state.get_state()
    await call.message.answer(f"handler tri before state: {current_state}")
    await state.set_state(BotStates.STATE_3)
    current_state = await state.get_state()
    await call.message.answer(f"handler tri after state: {current_state}")


@dp.callback_query_handler(state="*", text=['tri'])
async def handler_command_tri_star(call: types.CallbackQuery):

    state = dp.current_state(user=call.message.from_user.id)
    current_state = await state.get_state()
    await call.message.answer(f"handler tri before state: {current_state}")
    await call.message.answer(f"Hello from Tri Star!")
    await state.set_state(BotStates.STATE_3)
    current_state = await state.get_state()
    await call.message.answer(f"handler tri after state: {current_state}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

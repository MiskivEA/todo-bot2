from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import default_state, State, StatesGroup
from database.crud import create_task, get_tasks_by_id, delete_task_by_id, done_task_by_id
from keyboards.task_keyboards import keyboard

router = Router()


class InputStateGroup(StatesGroup):
    idx = State()
    task_text = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """ /start """

    await message.answer('Вас приветствует TODO-bot!\nДля получения справки используйте команду /help',
                         reply_markup=keyboard)


@router.message(F.text == '/help')
async def cmd_help(message: Message):
    """ /help """
    await message.answer('<b>Доступные команды:</b>\n\n'
                         '/add [текст задачи] - добавление задачи\n'
                         '/done [индекс задачи] - отметить задачу выполненной\n'
                         '/list - показать все\n'
                         '/delete [индекс задачи] удалить по индексу\n'
                         '/cancel - выход из состояния воода данных(в режиме передачи данных)')


@router.callback_query(F.data == 'cancel_input_data', ~StateFilter(default_state))
async def cancel_input_data(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Состояние сброшено в дефолт,\nввод данных отменен')
    await state.clear()


@router.callback_query(F.data == 'cancel_input_data', StateFilter(default_state))
async def cancel_input_data(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Состояние сброшено в дефолт,\nввод данных отменен')
    await state.clear()


# #############################################################################
@router.callback_query(F.data == 'add_task', StateFilter(default_state))
async def add_cmd(callback: CallbackQuery, state: FSMContext):
    """ /add """
    await callback.message.answer('Введите текст вашей задачи')
    await callback.answer('Wait')
    await state.set_state(InputStateGroup.task_text)


@router.message(F.text, StateFilter(InputStateGroup.task_text))
async def input_task_text(message: Message, state: FSMContext):
    if isinstance(message.text, str):
        await message.answer(f'Задача:\n'
                             f'{message.text}\n'
                             f'Введите число')
        await state.set_state(InputStateGroup.idx)
    else:
        await message.answer('Некорректный ввод, проверьте ваще сообщение')


@router.message(F.text, StateFilter(InputStateGroup.idx))
async def input_id(message: Message, state: FSMContext):
    await message.answer(f'ПОлучено число {message.text}\n'
                         f'Данные приняты. Состояние сброшено')
    await state.clear()

# #######################################################################

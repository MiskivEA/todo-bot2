from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import default_state, State, StatesGroup
from database.crud import create_task, delete_task_by_id, done_task_by_id, get_tasks
from keyboards.task_keyboards import keyboard
from service.lexic import statuses
router = Router()


class InputStateGroup(StatesGroup):
    task_title = State()
    task_text = State()
    done_task = State()


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
    await callback.message.answer('Введите заголовок вашей задачи')
    await callback.answer('Wait ...')
    await state.set_state(InputStateGroup.task_title)


@router.message(F.text, StateFilter(InputStateGroup.task_title))
async def input_task_text(message: Message, state: FSMContext):
    await message.answer(f'<b>Заголовок:</b>\n\n'
                         f'{message.text}\n\n'
                         f'Введите описание')
    await state.update_data(title=message.text)
    await state.set_state(InputStateGroup.task_text)


@router.message(F.text, StateFilter(InputStateGroup.task_text))
async def input_id(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    task_title = data.get('title')
    task_description = data.get('description')
    await message.answer(f'<b>Задача добавлена\n\n</b>'
                         f'Title: {data.get("title")}\n'
                         f'Description: {data.get("description")}\n\n'
                         f'Данные приняты')

    create_task(task_title, task_description, message.from_user.id)
    await state.clear()


# #######################################################################

@router.callback_query(F.data == 'show_tasks')
async def show_tasks(callback: CallbackQuery):
    tasks = get_tasks(callback.from_user.id)
    msg = 'Ваши задачи:\n'
    for task in tasks:
        msg += f'{task.id} {task.title} Статус: {statuses[task.status]}\n'
    if msg.rstrip() != callback.message.text:
        await callback.message.edit_text(msg, reply_markup=keyboard)
    await callback.answer()


# ##########################################################################
@router.callback_query(F.data == 'done_task')
async def request_id_for_done(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введи ID задачи ждя завершения')
    await state.set_state(InputStateGroup.done_task)


@router.message(F.text, StateFilter(InputStateGroup.done_task))
async def done_task(message: Message, state: FSMContext):
    idx = message.text
    print(idx)
    done_task_by_id(idx, message.from_user.id)
    await message.answer(f'Задача {idx} завершена')
    await state.clear()




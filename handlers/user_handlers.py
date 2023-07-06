from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import default_state, State, StatesGroup
from database.crud import create_task, delete_task_by_id, done_task_by_id, get_tasks, get_task_by_id
from keyboards.task_keyboards import keyboard
from service.lexic import statuses

router = Router()


class InputStateGroup(StatesGroup):
    task_title = State()
    task_text = State()
    done_task = State()
    delete_task = State()
    open_task = State()


@router.message(Command(commands=['start', 'help']))
async def cmd_help(message: Message):
    """ /help """
    await message.answer('Вас приветствует TODO-bot!', reply_markup=keyboard)


@router.callback_query(F.data == 'cancel_input_data')
async def cancel_input_data(callback: CallbackQuery, state: FSMContext):
    """ Отмена ввода данных и сброс машины состояний """
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
async def input_title(message: Message, state: FSMContext):
    """ Переход в ожидание ввода заголовка задачи """
    await message.answer(f'<b>Заголовок:</b>\n\n'
                         f'{message.text}\n\n'
                         f'Введите описание')
    await state.update_data(title=message.text)
    await state.set_state(InputStateGroup.task_text)


@router.message(F.text, StateFilter(InputStateGroup.task_text))
async def input_description(message: Message, state: FSMContext):
    """ Переход в ожидание ввода описания задачи """
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
    """ Вывод всех задач """
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
    """ Переход в ожидание ввода ИД задачи """
    await callback.message.answer('Введи ИД задачи ждя завершения')
    await state.set_state(InputStateGroup.done_task)
    await callback.answer()


@router.message(F.text, StateFilter(InputStateGroup.done_task))
async def done_task(message: Message, state: FSMContext):
    """ Отметить задачу выполненной """
    idx = message.text
    done_task_by_id(idx, message.from_user.id)
    await message.answer(f'Задача {idx} завершена')
    await state.clear()


# #################################################################
@router.callback_query(F.data == 'delete_task')
async def request_id_for_done(callback: CallbackQuery, state: FSMContext):
    """ Переход в ожидание ввода ИД задачи """
    await callback.message.answer('Введи ИД задачи ждя завершения')
    await state.set_state(InputStateGroup.delete_task)


@router.message(F.text, StateFilter(InputStateGroup.delete_task))
async def done_task(message: Message, state: FSMContext):
    """ Удалить задачу """
    idx = message.text
    delete_task_by_id(idx, message.from_user.id)
    await message.answer(f'Задача {idx} удалена')
    await state.clear()


# ################################################

@router.callback_query(F.data == 'open_task')
async def request_id_for_done(callback: CallbackQuery, state: FSMContext):
    """ Переход в ожидание ввода ИД задачи """
    await callback.message.answer('Введи ИД задачи для открытия')
    await callback.answer()
    await state.set_state(InputStateGroup.open_task)


@router.message(F.text, StateFilter(InputStateGroup.open_task))
async def open_task(message: Message, state: FSMContext):
    """ Открыть задачу"""
    idx = message.text
    task = get_task_by_id(idx, message.from_user.id)
    await message.answer(f'Задача {task.id}\n\n'
                         f'{task.description}')
    await state.clear()

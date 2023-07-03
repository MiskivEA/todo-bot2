from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database.crud import create_task, get_tasks_by_id, delete_task_by_id, done_task_by_id
from database.models import Task, SchemaTask

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """ /start """
    await message.answer('Вас приветствует TODO-bot!\nДля получения справки используйте команду /help')


@router.message(F.text == '/help')
async def cmd_help(message: Message):
    """ /help """
    await message.answer('<b>Доступные команды:</b>\n\n'
                         '/add [текст задачи] - добавление задачи\n'
                         '/done [индекс задачи] - отметить задачу выполненной\n'
                         '/list - показать все\n'
                         '/delete [индекс задачи] удалить по индексу\n')


# ########################################## #
# ################ TASK #################### #
# ########################################## #


@router.message(F.text.startswith('/add '))
async def add_task(message: Message):
    """ /add -  Добавление задачи """
    task_text = message.text.split('/add')[-1]
    create_task(task_text, message.from_user.id)
    await message.answer('Задача добавлена')


@router.message(F.text.startswith('/done '))
async def done_task(message: Message):
    """ /done - Маркировка задачи как выполненная """
    task_id = message.text.split(' ')[-1]
    done_task_by_id(task_id, message.from_user.id)
    await message.answer('Задача отмечена выполненной')


@router.message(F.text == '/list')
async def list_tasks(message: Message):
    """ /list - Получение списка всех задач """
    tasks = get_tasks_by_id(message.from_user.id)
    for task in tasks:
        delete_button = InlineKeyboardButton(text='Удалить ❌', callback_data=f'delete_task {task.id}')
        done_button = InlineKeyboardButton(text='Выполнено', callback_data=f'done_task {task.id}')
        delete_task_kb = InlineKeyboardMarkup(inline_keyboard=[[delete_button, done_button]])
        await message.answer(f'ID: {task.id}\n'
                             f'TITLE: {task.title}\n'
                             f'DESCRIPTION: {task.description}\n'
                             f'STATUS: {task.status}',
                             reply_markup=delete_task_kb)


@router.callback_query(F.data.startswith('delete_task'))
async def delete_task_button_press(callback: CallbackQuery):
    """ Удаление задачи кнопкой """
    task_id = callback.data.split(' ')[-1]
    delete_task_by_id(task_id, callback.from_user.id)
    await callback.message.edit_text(f'Задача [{task_id}] удалена')


@router.callback_query(F.data.startswith('done_task'))
async def delete_task_button_press(callback: CallbackQuery):
    """ Удаление задачи кнопкой """
    task_id = callback.data.split(' ')[-1]
    done_task_by_id(task_id, callback.from_user.id)
    await callback.message.edit_text(f'{callback.message.text}\nЗадача [{task_id}] Выполнена')


@router.message(F.text.startswith('/delete '))
async def delete_task(message: Message):
    """ /delete - Удаление задачи командой"""
    task_id = message.text.split(' ')[-1]
    delete_task_by_id(task_id, message.from_user.id)
    await message.answer(f'Задача [{task_id}] удалена')


# ################ END #########################
@router.message(F.text == '/add')
async def incorrect_add(message: Message):
    """ Срабатывает, когда команда требует аргументов,
    но не получает их при вызове """
    await message.answer('<b> ERROR </b>\n'
                         'Эта команда требует данные для обработки')


@router.message()
async def i_dont_know(message: Message):
    """ Срабатывает в любой непонятной ситуации =)"""
    await message.answer('<b>Такой команды пока нет =(</b>')

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_add = InlineKeyboardButton(text='Добавить задачу', callback_data='add_task')
btn_done = InlineKeyboardButton(text='Отметить задачу выполненной', callback_data='done_task')
btn_list = InlineKeyboardButton(text='Показать все', callback_data='show_tasks')
btn_delete = InlineKeyboardButton(text='Удалить задачу', callback_data='delete_task')
btn_cancel = InlineKeyboardButton(text='Отменить ввод данных', callback_data='cancel_input_data')
btn_open = InlineKeyboardButton(text='Открыть задачу', callback_data='open_task')

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [btn_open],
    [btn_add, btn_list],
    [btn_done, btn_delete],
    [btn_cancel]
])

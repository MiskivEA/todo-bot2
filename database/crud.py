from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from database.database import engine
from database.models import Task


def create_task(task_title, task_description, telegram_id):
    """Создает задачу для текущего пользователя"""
    with Session(engine) as db:
        task = Task(
            telegram_id=telegram_id,
            title=task_title,
            description=task_description,
            status=False,
        )
        db.add(task)
        db.commit()


def get_tasks(telegram_id):
    """Возвращает все задачи текущего пользователя"""
    session = Session(engine)
    query = select(Task).where(Task.telegram_id == telegram_id)
    tasks = session.scalars(query)
    return tasks


def delete_task_by_id(task_id, telegram_id):
    """ Удаление задачи по индексу """
    session = Session(engine)
    query = delete(Task).where(Task.telegram_id == telegram_id, Task.id == task_id)
    session.execute(query)
    session.commit()


def done_task_by_id(task_id, telegram_id):
    """ Отметить статус задачи как "выполнено" """
    session = Session(engine)
    query = update(Task).where(Task.telegram_id == telegram_id, Task.id == task_id).values(status=True)
    session.execute(query)
    session.commit()


def get_task_by_id(task_id, telegram_id):
    """ Получение задачи по индексу """
    session = Session(engine)
    query = select(Task).where(Task.telegram_id == telegram_id, Task.id == task_id)
    task = session.execute(query).scalar()
    return task

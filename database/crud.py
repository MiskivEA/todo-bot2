from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from database.database import engine
from database.models import Task


def create_task(task_text, telegram_id):
    """Создает задачу для текущего пользователя"""
    with Session(engine) as db:
        task = Task(
            telegram_id=telegram_id,
            title=task_text[:10],
            description=task_text,
            status=False,
        )
        db.add(task)
        db.commit()


def get_tasks_by_id(telegram_id):
    """Возвращает все задачи текущего пользователя"""
    session = Session(engine)
    stmt = select(Task).where(Task.telegram_id == telegram_id)
    tasks = session.scalars(stmt)
    return tasks


def delete_task_by_id(task_id, telegram_id):
    session = Session(engine)
    stmt = delete(Task).where(Task.telegram_id == telegram_id, Task.id == task_id)
    session.execute(stmt)
    session.commit()


def done_task_by_id(task_id, telegram_id):
    session = Session(engine)
    stmt = update(Task).where(Task.telegram_id == telegram_id, Task.id == task_id).values(status=True)
    session.execute(stmt)
    session.commit()


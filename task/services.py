"""Services."""

from django.db.models import ProtectedError

from .forms import TaskForm
from .selectors import get_task_by_pk


def create_task(status_data, author_pk):
    form = TaskForm(data=status_data)
    if form.is_valid():
        form.set_author(author_pk)
        form.save()
    return form


def delete_task(pk):

    task = get_task_by_pk(pk)
    try:
        return task.delete()
    except ProtectedError:
        return None


def update_task(new_task_data, pk):
    task = get_task_by_pk(pk)
    form = TaskForm(instance=task,
                    data=new_task_data)
    if form.is_valid():
        form.save()
    return form

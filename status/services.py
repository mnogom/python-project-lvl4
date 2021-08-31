"""Services."""

from .forms import StatusForm
from .selectors import get_status_by_pk

def create_status(status_data):

    form = StatusForm(data=status_data)
    if form.is_valid():
        form.save()
    return form


def delete_status(pk):
    status = get_status_by_pk(pk)
    status.delete()


def update_status(new_status_data, pk):
    status = get_status_by_pk(pk)
    form = StatusForm(instance=status,
                      data=new_status_data)
    if form.is_valid():
        form.save()
    return form

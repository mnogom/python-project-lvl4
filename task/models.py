"""Models."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    # TODO: [fix]
    #  rename name from 'имя' to 'название'
    name = models.CharField(verbose_name=_('name'),
                            max_length=300,
                            blank=False,
                            null=False,
                            unique=True,
                            error_messages={
                                'unique': _('A task with that name already exists')})
    description = models.TextField(verbose_name=_('description'),
                                   blank=True,
                                   null=False)
    author = models.ForeignKey('user.User',
                               verbose_name=_('author'),
                               on_delete=models.PROTECT,
                               related_name='author')
    executor = models.ForeignKey('user.User',
                                 verbose_name=_('executor'),
                                 on_delete=models.PROTECT,
                                 related_name='executor')
    status = models.ForeignKey('status.Status',
                               verbose_name=_('status'),
                               on_delete=models.PROTECT,
                               related_name='status')
    labels = models.ManyToManyField('label.Label',
                                    verbose_name=_('labels'),
                                    through='TaskLabel',
                                    blank=True)
    created_at = models.DateField(verbose_name=_('created at'),
                                  auto_now_add=True,
                                  editable=False)


class TaskLabel(models.Model):
    task = models.ForeignKey('task.Task',
                             on_delete=models.CASCADE)
    label = models.ForeignKey('label.Label',
                              on_delete=models.PROTECT)

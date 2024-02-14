from django.db import models

from config import settings


class Module(models.Model):
    name = models.CharField(max_length=120, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL,
                              null=True, verbose_name='владелец')

    def __srt__(self):
        return f'{self.name}: "{self.description}"'

    class Meta:
        verbose_name = 'модуль'
        verbose_name_plural = 'модули'

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractModel
from server.apps.telegram_clean_prediction.services.enum import (
    ClientPrivileges,
)


class Client(AbstractModel):
    """Клиент."""

    tg_user_id = models.BigIntegerField(
        verbose_name=_('Id пользователя в telegram'),
        unique=True,
    )
    tg_user_username = models.CharField(
        verbose_name=_('Никнейм пользователя'),
        blank=True,
    )
    tg_user_first_name = models.CharField(
        verbose_name=_('Имя пользователя'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    tg_user_last_name = models.CharField(
        verbose_name=_('Фамилия пользователя'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    tg_user_is_premium = models.BooleanField(
        verbose_name=_('Наличие премиум-аккаунта'),
        blank=True,
        null=True,
    )
    tg_user_language_code = models.CharField(
        verbose_name=_('Язык пользователя'),
        blank=True,
    )
    privileges = models.CharField(
        verbose_name=_('Привилегии'),
        choices=ClientPrivileges.choices,
        default=ClientPrivileges.STANDARD,
    )

    class Meta(AbstractModel.Meta):
        verbose_name = _('Клиент')
        verbose_name_plural = _('Клиенты')

    def __str__(self):
        return 'Id: {id}. Username: {username}. Имя: {first_name}'.format(
            id=self.tg_user_id,
            username=self.tg_user_username,
            first_name=self.tg_user_first_name,
        )

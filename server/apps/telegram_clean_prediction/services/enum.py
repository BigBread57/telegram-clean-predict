from django.db import models
from django.utils.translation import gettext_lazy as _


class ClientPrivileges(models.TextChoices):
    """Привилегии клиента"""

    STANDARD = 'standard', _('Стандартные')
    PREMIUM = 'premium', _('Премиальные')
    MISSING = 'missing', _('Отсутствуют')


class ClientActivity(models.TextChoices):
    """Активность клиента"""

    INACTIVE = 'inactive', _('Не активный')
    ACTIVE = 'active', _('Активный')
    NARRATOR_SEARCH = 'narrator_search', _('Поиск рассказывающего')
    LISTENER_SEARCH = 'listener_search', _('Поиск слушающего')


class ComplaintStatus(models.TextChoices):
    """Статус жалобы."""

    UNDER_CONSIDERATION = 'under_consideration', _('На рассмотрении')
    ACCEPTED = 'accepted', _('Принята')
    REJECTED = 'rejected', _('Отклонена')
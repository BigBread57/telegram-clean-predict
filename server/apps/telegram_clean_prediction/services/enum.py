from django.db import models
from django.utils.translation import gettext_lazy as _


class DeckType(models.TextChoices):
    """Тип колоды."""

    RIDER_WAITE_TAROT = 'rider_waite_tarot', _('Таро Райдера — Уэйта')


class GroupType(models.TextChoices):
    """Тип группы."""

    MAJOR_ARCANA = 'major_arcana', _('Старшие арканы')
    MINOR_ARCANA = 'minor_arcana', _('Младшие арканы')


class SuitType(models.TextChoices):
    """Тип масти."""

    WANDS = 'wands', _('Жезлы')
    CUPS = 'cups', _('Кубки')
    SWORDS = 'swords', _('Мечи')
    PENTACLES = 'pentacles', _('Пентакли')


class ClientPrivileges(models.TextChoices):
    """Привилегии клиента"""

    STANDARD = 'standard', _('Стандартные')
    PREMIUM = 'premium', _('Премиальные')
    MISSING = 'missing', _('Отсутствуют')

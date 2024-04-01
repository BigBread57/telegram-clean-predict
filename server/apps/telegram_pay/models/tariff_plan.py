from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractModel


class TariffPlan(AbstractModel):
    """Тарифный план."""

    price_rub = models.DecimalField(
        verbose_name=_('Стоимость тарифного плана в рублях'),
        max_digits=6,
        decimal_places=2,
    )
    price_ton = models.DecimalField(
        verbose_name=_('Стоимость тарифного плана в TON'),
        max_digits=6,
        decimal_places=2,
    )
    price_usdt = models.DecimalField(
        verbose_name=_('Стоимость тарифного плана в USDT'),
        max_digits=6,
        decimal_places=2,
    )
    image = models.ImageField(
        verbose_name=_('Изображение тарифного плана'),
        blank=True,
        null=True,
    )
    key = models.CharField(
        verbose_name=_('Ключ тарифного плана'),
        max_length=settings.MAX_STRING_LENGTH,
        unique=True,
    )
    title = models.CharField(
        verbose_name=_('Название тарифного плана'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    text = models.TextField(
        verbose_name=_('Описание тарифного плана'),
        blank=True,
    )
    period = models.IntegerField(
        verbose_name=_('Период действия тарифного плана в днях'),
        null=True,
        blank=True,
    )
    number_of_actions = models.IntegerField(
        verbose_name=_('Количество доступных действий'),
        null=True,
        blank=True,
    )
    is_actual = models.BooleanField(
        verbose_name=_('Актуальный тарифный план или нет'),
        default=True,
    )

    class Meta(AbstractModel.Meta):
        verbose_name = _('Тарифный план')
        verbose_name_plural = _('Тарифный план')

    def __str__(self):
        return f'{self.title} - {self.key}'

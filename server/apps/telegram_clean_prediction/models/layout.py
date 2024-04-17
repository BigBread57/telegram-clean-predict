from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractModel
from server.apps.telegram_clean_prediction.services.enum import DeckType


class Layout(AbstractModel):
    """Расклад Карт."""

    client = models.ForeignKey(
        to='telegram_clean_prediction.Client',
        verbose_name=_('Клиент'),
        on_delete=models.CASCADE,
        related_name='layouts',
    )
    type_layout = models.CharField(
        verbose_name=_('Тип расклада'),
        choices=DeckType.choices,
        max_length=50,
    )
    question = models.TextField(
        verbose_name=_('Вопрос'),
        blank=True,
    )
    cards = models.ManyToManyField(
        to='telegram_clean_prediction.Card',
        verbose_name=_('Карты'),
        through='telegram_clean_prediction.LayoutCards',
        through_fields=('layout', 'card'),
        related_name='layouts',
    )
    is_accurate = models.BooleanField(
        verbose_name=_('Точный расклад'),
        null=True,
    )
    is_doubtful = models.BooleanField(
        verbose_name=_('Сомнительный расклад'),
        null=True,
    )
    is_like = models.BooleanField(
        verbose_name=_('Расклад нравится'),
        null=True,
    )
    is_not_like = models.BooleanField(
        verbose_name=_('Расклад не нравится'),
        null=True,
    )

    class Meta(AbstractModel.Meta):
        verbose_name = _('Расклад')
        verbose_name_plural = _('Расклады')

    def __str__(self):
        return f'{self.client}'

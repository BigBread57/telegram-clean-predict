import random

from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractModel
from server.apps.telegram_clean_prediction.services.enum import (
    DeckType,
    GroupType,
    SuitType,
)


class CombinationCards(AbstractModel):
    """Комбинации карт."""

    first_card = models.ForeignKey(
        to='telegram_clean_prediction.Card',
        on_delete=models.CASCADE,
        verbose_name=_('Первая карта'),
        related_name='combination_first_cards',
        db_index=True,
    )
    second_card = models.ForeignKey(
        to='telegram_clean_prediction.Card',
        on_delete=models.CASCADE,
        verbose_name=_('Вторая карта'),
        related_name='combination_second_cards',
        db_index=True,
    )
    description = models.JSONField(
        verbose_name=_('Описание'),
    )

    class Meta(AbstractModel.Meta):
        verbose_name = _('Комбинация карт')
        verbose_name_plural = _('Комбинации карт')

    def __str__(self):
        return f'{self.first_card} - {self.second_card}'

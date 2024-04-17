from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractModel


class LayoutCards(AbstractModel):
    """Карты, участвующие в раскладе."""

    layout = models.ForeignKey(
        to='telegram_clean_prediction.Layout',
        on_delete=models.CASCADE,
        verbose_name=_('Расклад'),
        related_name='layout_cards',
        db_index=True,
    )
    card = models.ForeignKey(
        to='telegram_clean_prediction.Card',
        on_delete=models.CASCADE,
        verbose_name=_('Карта'),
        related_name='layout_cards',
        db_index=True,
    )

    class Meta(AbstractModel.Meta):
        verbose_name = _('Карты, участвующие в раскладе')
        verbose_name_plural = _('Карты, участвующие в раскладе')

    def __str__(self):
        return f'{self.layout} - {self.card}'

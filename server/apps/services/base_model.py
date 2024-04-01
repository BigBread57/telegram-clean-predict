from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModel


class AbstractModel(RulesModel):
    """Базовая модель."""

    created_at = models.DateTimeField(
        verbose_name=_('Создан'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Изменен'),
        auto_now=True,
    )

    class Meta(object):
        abstract = True
        ordering = ['-id']


class AbstractContentTypeModel(models.Model):
    """Базовая модель, которая использует ContentType."""

    content_type = models.ForeignKey(
        to=ContentType,
        verbose_name=_('Тип содержимого'),
        on_delete=models.CASCADE,
        db_index=True,
    )
    object_id = models.PositiveIntegerField(_('Id объекта'))
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

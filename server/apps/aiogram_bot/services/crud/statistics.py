from typing import Dict

from django.db import models
from django.db.models.functions import Coalesce

from server.apps.telegram_clean_prediction.models import (
    Client,
    Dialog,
    Statistics,
)


async def get_statistics(client: Client) -> Dict[str, int]:
    """Статистика клиента."""
    statistics, _ = await Statistics.objects.aget_or_create(client=client)
    dialogs_statistics = [
        {
            'amount_narrating_client': client.amount_narrating_client,
            'amount_listening_client': client.amount_listening_client,
        }
        async for client in Client.objects.annotate(
            amount_narrating_client=Coalesce(
                models.Subquery(
                    Dialog.objects.filter(
                        narrating_client=models.OuterRef('id'),
                    ).values(
                        'id',
                    ).annotate(
                        count=models.Count('id'),
                    ).values(
                        'count',
                    ),
                ),
                models.Value(0),
            ),
            amount_listening_client=Coalesce(
                models.Subquery(
                    Dialog.objects.filter(
                        listening_client=models.OuterRef('id'),
                    ).values(
                        'id',
                    ).annotate(
                        count=models.Count('id'),
                    ).values(
                        'count',
                    ),
                ),
                models.Value(0),
            ),
        )
    ]

    return {
        'successfully_listened': statistics.successfully_listened,
        **dialogs_statistics[0],
    }

from typing import Optional

from server.apps.telegram_pay.models import TariffPlan


async def get_tariff_plan(
    tariff_plan_key: str
) -> TariffPlan:
    """Получение тарифного плана"""
    return await TariffPlan.objects.aget(key=tariff_plan_key, is_actual=True)

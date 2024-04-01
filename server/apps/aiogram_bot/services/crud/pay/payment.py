import decimal

from server.apps.telegram_pay.models import Payment, TariffPlan


async def update_or_create_payment(
    client_id: int,
    currency: str,
    status: str,
    amount: decimal.Decimal,
) -> TariffPlan:
    """Обновление или создание платежа."""
    payment, _ = await Payment.objects.aupdate_or_create(
        client_id=client_id,
        currency=currency,
        amount=amount,
        defaults={
            'status': status,
        },
    )
    return payment

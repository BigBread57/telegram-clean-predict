from django.contrib import admin

from server.apps.telegram_clean_prediction.models import Client
from server.apps.telegram_pay.models import (
    Payment,
    Subscription,
    TariffPlan,
    Wallet,
)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin[Payment]):
    """Платеж клиента."""

    list_display = (
        'id',
        'client',
        'status',
        'currency',
        'amount',
    )
    ordering = (
        'id',
        'client',
        'status',
        'currency',
        'amount',
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin[Subscription]):
    """Подписка клиента."""

    list_display = (
        'id',
        'client',
        'expired_at',
    )
    ordering = (
        'id',
        'client',
        'expired_at',
    )


@admin.register(TariffPlan)
class TariffPlanAdmin(admin.ModelAdmin[TariffPlan]):
    """Подписка клиента."""

    list_display = (
        'id',
        'price_rub',
        'price_ton',
        'price_usdt',
        'title',
        'key',
        'period',
    )
    ordering = (
        'id',
        'price_rub',
        'price_ton',
        'price_usdt',
        'title',
        'key',
        'period',
    )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin[Wallet]):
    """Кошелек."""

    list_display = (
        'id',
        'client',
        'amount_rub',
        'amount_ton',
        'amount_usdt',
    )
    ordering = (
        'id',
        'client',
        'amount_rub',
        'amount_ton',
        'amount_usdt',
    )

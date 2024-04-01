import decimal
import json

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.handlers import PreCheckoutQueryHandler
from aiogram.types import LabeledPrice
from django.conf import settings

from server.apps.aiogram_bot.bot import aiogram_bot
from server.apps.aiogram_bot.keyboards.bot_start import bot_start_keyboard
from server.apps.aiogram_bot.services.crud.client import get_client
from server.apps.aiogram_bot.services.crud.pay.payment import (
    update_or_create_payment,
)
from server.apps.aiogram_bot.services.crud.pay.tariff_plan import (
    get_tariff_plan,
)
from server.apps.aiogram_bot.services.state import state_clear
from server.apps.telegram_pay.models import TariffPlan
from server.apps.telegram_pay.services.enum import (
    PaymentCurrency,
    PaymentStatus,
)

router = Router()


@router.callback_query(F.data == 'replenishment_via_telegram')
async def replenishment_via_telegram(
    callback: types.CallbackQuery,
):
    """Оформление подписки."""
    await callback.message.edit_text(
        text=(
            'Выберите тариф'
        ),
        reply_markup=bot_start_keyboard.as_markup(resize_keyboard=True),
    )


@router.callback_query(F.data == 'replenishment_via_ykassa')
async def replenishment_via_ykassa(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    """Оформление подписки."""
    state_data = await state.get_data()
    await state_clear(state, state_data)
    if tariff_plan_key := state_data.get('tariff_plan_key'):
        tariff_plan = await get_tariff_plan(tariff_plan_key=tariff_plan_key)
        amount = tariff_plan.price_rub
        title = f'Оплата "{tariff_plan.title}" на сумму: {amount} руб.'

        await aiogram_bot.send_invoice(
            chat_id=callback.message.chat.id,
            title=title,
            description=' ',
            provider_token=settings.TELEGRAM_PROVIDER_TOKEN_YKASSA,
            currency='RUB',
            prices=[
                LabeledPrice(
                    label=title,
                    amount=int(amount * 100),
                ),
            ],
            start_parameter=str(tariff_plan.id),
            payload=json.dumps(
                {
                    'tariff_plan_key': tariff_plan.key,
                    'client_id': state_data['client_id'],
                },
            ),
        )
    else:
        amount = state_data['amount']
        title = f'Пополнение кошелька в боте на сумму: {amount} руб.'
        await aiogram_bot.send_invoice(
            chat_id=callback.message.chat.id,
            title=title,
            description=' ',
            provider_token=settings.TELEGRAM_PROVIDER_TOKEN_YKASSA,
            currency='RUB',
            prices=[
                LabeledPrice(
                    label=title,
                    amount=(amount * 100)
                ),
            ],
            start_parameter=str(state_data['amount']),
            payload=json.dumps(
                {
                    'amount': amount,
                    'client_id': state_data['client_id'],
                },
            ),
        )


@router.pre_checkout_query()
class MyHandler(PreCheckoutQueryHandler):
    async def handle(self):
        payload = json.loads(self.event.invoice_payload)
        tariff_plan = None

        if tariff_plan_key := payload.get('tariff_plan_key'):
            tariff_plan = await get_tariff_plan(tariff_plan_key=tariff_plan_key)

        if tariff_plan:
            if (tariff_plan.price_rub * 100) != self.event.total_amount:
                await update_or_create_payment(
                    client_id=payload['client_id'],
                    currency=PaymentCurrency.RUB,
                    status=PaymentStatus.ERROR,
                    amount=decimal.Decimal(self.event.total_amount/100),
                )

                await self.bot.answer_pre_checkout_query(
                    pre_checkout_query_id=self.event.id,
                    ok=False,
                    error_message='Суммы разные',
                    # self.vpn_admin_client.get_localize_settings_by_code(
                    #     user.id, self.SC_PAYMENT_ERROR_NOT_ACTUAL_PRICE_TARIFF
                    # ).value,
                )
            else:
                await update_or_create_payment(
                    client_id=payload['client_id'],
                    currency=PaymentCurrency.RUB,
                    status=PaymentStatus.NEW,
                    amount=tariff_plan.price_rub,
                )
                await self.bot.answer_pre_checkout_query(
                    pre_checkout_query_id=self.event.id,
                    ok=True,
                )

        elif amount := payload.get('amount'):
            await update_or_create_payment(
                client_id=payload['client_id'],
                currency=PaymentCurrency.RUB,
                status=PaymentStatus.NEW,
                amount=amount,
            )
            await self.bot.answer_pre_checkout_query(
                pre_checkout_query_id=self.event.id,
                ok=True,
            )
        else:
            await self.bot.answer_pre_checkout_query(
                pre_checkout_query_id=self.event.id,
                ok=False,
                error_message='Базовая ошибка',
            )


@router.message(F.successful_payment)
async def process_enter_keywords(
    message: types.Message,
):
    user = 1
    message.successful_payment
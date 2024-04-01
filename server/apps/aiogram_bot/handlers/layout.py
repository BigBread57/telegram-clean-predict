from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from server.apps.aiogram_bot.bot import aiogram_bot
from server.apps.aiogram_bot.keyboards.bot_start import bot_start_keyboard
from server.apps.aiogram_bot.keyboards.dialog import (
    dialog_keyboard,
    dialog_reply_keyboard,
    end_dialog_reply_keyboard,
)
from server.apps.aiogram_bot.keyboards.layout import LayoutCallback, \
    layout_keyboard

router = Router()


class FSMComplain(StatesGroup):
    """Класс конечных автоматов для жалобы на поведение пользователя."""

    enter_note = State()
    enter_messages = State()
# 1) Надо сформулировать и подумать о вопросе.
# 2) Подключить к энерегетике того кто задает вопрос и натсроиться с ним на ождну вибрацию.
# 3) Перемешивание карт.
# 4) Решение остановится остается за тарологом.
# 5) Таролог достает карту и кладет ее.
# 6) Случайно выпала карта из колоды и карты сами хоятт что то сообщить.


@router.message(F.text.lower() == 'расклад')
async def layout_section(
    message: types.Message,
):
    """Прервать процесс подачи жалобы."""
    await message.answer(
        text=(
            'Выбери расклад'
        ),
        reply_markup=layout_keyboard.as_markup(resize_keyboard=True),
    )



@router.callback_query(F.data.contains('layout_callback'))
async def cancellation_complaint_section(
    callback: types.CallbackQuery,
    callback_data: LayoutCallback,
    state: FSMContext,
):
    """Прервать процесс подачи жалобы."""
    await state.set_state(state=None)
    await state.update_data(note=None)
    await callback.message.edit_text(
        text=(
            'Подача жалобы отменена.'
        ),
        reply_markup=dialog_reply_keyboard.as_markup(resize_keyboard=True),
    )


@router.callback_query(F.data == 'send_message_for_review_section')
async def send_message_for_review_section(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    """Отправить сообщения с информацией о жалобах на проверку."""
    state_data = await state.get_data()
    client = state_data['client']
    dialog = await get_active_dialog(client=client)
    Complaint.objects.abulk_create(
        [
            Complaint(
                client=client,
                dialog=dialog,
                text=message,
                note=state_data['note'],
            )
            for message in state_data.get('messages', [])
        ]
    )

    await state.set_state(state=None)
    await state.update_data(note=None, messages=None)
    await callback.message.answer(
        text=(
            'Жалоба подана и будет рассмотрена в ближайшее время. '
            'Завершите диалог с пользователем во избежание лишних негативных '
            'эмоций.'
        ),
        reply_markup=end_dialog_reply_keyboard.as_markup(resize_keyboard=True),
    )


@router.message(F.text.lower() == 'Завершить диалог')
async def end_dialog_section(
    message: types.Message,
    state: FSMContext,
):
    """Завершить диалог."""
    # Завершаем диалог пользователя.
    state_data = await state.get_data()
    if await inactive_dialog(client=state_data['client']):
        await message.answer(
            text=(
                'Вы завершили диалог! Надеемся, что общение помогло вам!'
            ),
            reply_markup=bot_start_keyboard.as_markup(resize_keyboard=True),
        )
    else:
        await message.answer(
            text=(
                'У вас отсутствуют диалоги, или ранее активный диалог '
                'был завершен.\n'
                'Вы можете в любой момент начать поиск нового собеседника!'
            ),
            reply_markup=bot_start_keyboard.as_markup(resize_keyboard=True),
        )


@router.message(F.text.lower() == 'Пожаловаться на собеседника')
async def complain_about_interlocutor(
    message: types.Message,
    state: FSMContext,
):
    """Пожаловаться на собеседника"""
    await state.set_state(state=FSMComplain.enter_note)
    await message.answer(
        text=(
            'Опишите кратко возникшую ситуацию.'
        ),
        reply_markup=dialog_keyboard.as_markup(resize_keyboard=True),
    )


@router.message(FSMComplain.enter_note)
async def process_enter_note(
    message: types.Message,
    state: FSMContext,
):
    """Написать заметку на жалобу."""
    await state.update_data(note=message.text)
    await state.set_state(state=FSMComplain.enter_messages)
    await message.answer(
        text=(
            'Перешлите пожалуйста сообщения, которые не соответствуют '
            'нормальному поведению и нажмите на '
            '"Отправить сообщения на проверку"'
        ),
        reply_markup=dialog_keyboard.as_markup(resize_keyboard=True),
    )


@router.message(FSMComplain.enter_messages)
async def process_enter_messages(
    message: types.Message,
    state: FSMContext,
):
    """Переслать сообщения для жалобы."""
    state_data = await state.get_data()
    messages = state_data.get('messages', [])
    messages.append(message.text)


@router.message()
async def dialog_messages(
    message: types.Message,
    state: FSMContext,
):
    """Сообщения в диалоге."""
    state_data = await state.get_data()
    # client = state_data['client']

    # Если у нас есть информация о собеседнике, то просто пересылаем сообщение
    if interlocutor := state_data.get('interlocutor'):
        await aiogram_bot.send_message(
            chat_id=interlocutor,
            text=message.text,
        )
    # Если у нас нет информации о собеседнике, то ищем активный диалог
    # пользователя и получаем оттуда собеседника.
    # else:
    #     interlocutor = await get_interlocutor(client=client)
    #     if interlocutor:
    #         await state.update_data(interlocutor=interlocutor)
    #         await aiogram_bot.send_message(
    #             chat_id=interlocutor,
    #             text=message.text,
    #         )
    #     else:
    #         await state.clear()
    #         await message.answer(
    #             text=(
    #                 'У вас отсутствуют диалоги, или ранее активный диалог '
    #                 'был завершен.\n'
    #                 'Вы можете в любой момент начать поиск нового собеседника!'
    #             ),
    #             reply_markup=dialog_reply_keyboard.as_markup(resize_keyboard=True),
    #         )

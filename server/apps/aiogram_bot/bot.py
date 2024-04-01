from aiogram import Bot
from django.conf import settings
from googletrans import Translator

aiogram_bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

translator = Translator()

import asyncio
import sys
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# --- НАСТРОЙКИ ЯЗЫКА И ИНТЕРВАЛА ---
LANG = "ru"          # Поддерживаются: "ru" или "en"
CHECK_INTERVAL = 60  # Интервал проверки сайтов в секундах

# Список сайтов для мониторинга (пользователь меняет под себя)
SITES = [
    "https://google.com",
    "https://github.com"
]

# Глобальная переменная для автоматического перехвата ID
admin_id = None

# --- ЛОКАЛИЗАЦИЯ (Интерфейс) ---
MESSAGES = {
    "ru": {
        "ask_token": "🔑 Введите API Токен вашего Телеграм-бота (из @BotFather): ",
        "token_err": "❌ Ошибка: Вы ввели пустую строку. Перезапустите скрипт.",
        "start": "\n🚀 Бот успешно инициализирован! Напишите ему команду /start в Telegram, чтобы связать аккаунт.",
        "connected": "✅ Связь установлена! Ваш ID ({user_id}) сохранен. Начинаю асинхронный мониторинг сайтов...",
        "alarm": "⚠️ **ВНИМАНИЕ!** Сайт {url} вернул код ответа: {code}!",
        "critical": "🚨 **КРИТИЧЕСКАЯ ОШИБКА!** Сайт {url} полностью НЕДОСТУПЕН!\nОшибка: {error}"
    },
    "en": {
        "ask_token": "🔑 Enter your Telegram Bot API Token (from @BotFather): ",
        "token_err": "❌ Error: Token cannot be empty. Please restart the script.",
        "start": "\n🚀 Bot initialized successfully! Send /start command to it in Telegram to link your account.",
        "connected": "✅ Connection established! Your ID ({user_id}) is saved. Starting async website monitoring...",
        "alarm": "⚠️ **ALARM!** Website {url} returned status code: {code}!",
        "critical": "🚨 **CRITICAL!** Website {url} is completely UNREACHABLE!\nError: {error}"
    }
}

lang = LANG if LANG in MESSAGES else "en"

# --- ИНТЕРАКТИВНЫЙ ВВОД ТОКЕНА В КОНСОЛИ ---
TOKEN = input(MESSAGES[lang]["ask_token"]).strip()

if not TOKEN:
    print(MESSAGES[lang]["token_err"])
    sys.exit(1)

# Инициализируем aiogram динамически с введенным токеном
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Автоматически ловим ID пользователя при вводе команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global admin_id
    admin_id = message.from_user.id
    text = MESSAGES[lang]["connected"].format(user_id=admin_id)
    await message.answer(text)

# Фоновый цикл мониторинга сайтов
async def check_sites():
    print(MESSAGES[lang]["start"])
    async with httpx.AsyncClient(timeout=10.0) as client:
        while True:
            # Начинаем слать алерты только когда пользователь нажал /start и определился admin_id
            if admin_id is not None:
                for url in SITES:
                    try:
                        response = await client.get(url)
                        if response.status_code != 200:
                            text = MESSAGES[lang]["alarm"].format(url=url, code=response.status_code)
                            await bot.send_message(chat_id=admin_id, text=text, parse_mode="Markdown")
                    except Exception as e:
                        text = MESSAGES[lang]["critical"].format(url=url, error=str(e))
                        await bot.send_message(chat_id=admin_id, text=text, parse_mode="Markdown")
            await asyncio.sleep(CHECK_INTERVAL)

async def main():
    asyncio.create_task(check_sites())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

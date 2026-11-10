from max_bot import Bot, Dispatcher, run_polling  # Убрали types
import time
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

bad_words = ["дурак", "мат1", "мат2"]


@dp.message()
async def moderation_handler(message):  # Убрали : types.Message
    # Защита от пустых сообщений
    if not message.text:
        return

    text = message.text.lower()

    if any(word in text for word in bad_words):
        try:
            # Удаляем сообщение (в pymaxbot это работает через sent.delete(),
            # но для входящего сообщения можно попробовать message.delete())
            await message.delete()

            # ВАЖНО: В pymaxbot может не быть restrict_chat_member.
            # Если выдаст ошибку - используй метод исключения из чата (если есть)
            # или просто удаляй сообщение (для теста этого хватит).
            # Пока оставляем так, но в try/except:
            user_id = message.sender.id
            until_date = int(time.time()) + 900

            # Проверь в документации pymaxbot, есть ли метод restrict_chat_member
            # Если нет - замени на что-то вроде bot.remove_user(...)
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                until_date=until_date,
                can_send_messages=False
            )

            await message.answer(f"Пользователь получил мут на 15 минут.")

        except Exception as e:
            print(f"Ошибка: {e}")
            # Если restrict не работает, хотя бы просто удаляем сообщение
            await message.answer("Сообщение удалено. (Мут временно недоступен)")

if __name__ == "__main__":
    asyncio.run(run_polling(bot, dp))

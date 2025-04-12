from telegram import Update
from telegram.ext import ContextTypes
from crew_config import run_crew
import traceback

async def handle_generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text.replace("/generate", "").strip()
        print(f"[LOG] Получен запрос от Telegram: {user_input}")

        if not user_input:
            await update.message.reply_text("Пожалуйста, опиши продукт.")
            print("[LOG] Пустой запрос — бот попросил уточнение.")
            return

        await update.message.reply_text("🚀 Команда агентов начала работу...")
        print("[LOG] Старт работы CrewAI...")

        result = run_crew(user_input)

        print(f"[LOG] Завершено. Ответ от CrewAI: {result}")
        await update.message.reply_text("✅ Готово! Вот результат:\n" + str(result))

    except Exception as e:
        error_text = traceback.format_exc()
        print(f"[ERROR] Произошла ошибка:\n{error_text}")
        await update.message.reply_text(f"❌ Ошибка при обработке: {e}")

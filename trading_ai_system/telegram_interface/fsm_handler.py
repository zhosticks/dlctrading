from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
)
from crew_config import run_crew
import traceback

# Состояния
GOAL, PLATFORMS, INVESTMENT, HORIZON, RISK, AUTODEPLOY, INTERFACE, CONFIRM = range(8)

reply_keyboard = [['/cancel']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

async def start_collecting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎯 Какая цель приложения? (например: торговля по RSI и MACD)", reply_markup=markup)
    return GOAL

async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["goal"] = update.message.text
    await update.message.reply_text("📊 Какие торговые платформы нужно подключить?")
    return PLATFORMS

async def platforms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["platforms"] = update.message.text
    await update.message.reply_text("💰 Какую сумму готов вложить?")
    return INVESTMENT

async def investment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["investment"] = update.message.text
    await update.message.reply_text("⏳ На какой срок ожидается результат?")
    return HORIZON

async def horizon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["horizon"] = update.message.text
    await update.message.reply_text("⚠️ Какой уровень риска допустим?")
    return RISK

async def risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["risk"] = update.message.text
    await update.message.reply_text("🚀 Нужен ли автодеплой? (да/нет)")
    return AUTODEPLOY

async def autodeploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["autodeploy"] = update.message.text
    await update.message.reply_text("💬 Основной интерфейс (Telegram, Web, API)?")
    return INTERFACE

async def interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["interface"] = update.message.text

    summary = "\n".join([f"{k.capitalize()}: {v}" for k, v in context.user_data.items()])
    await update.message.reply_text(f"📝 Вот что я собрал:\n\n{summary}\n\nПодтвердить запуск генерации? Напиши /confirm или /cancel")
    return CONFIRM

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = "\n".join([f"{k}: {v}" for k, v in context.user_data.items()])
    await update.message.reply_text("🤖 Начинаю генерацию системы...")

    try:
        result = run_crew(user_input)
        if "уточни" in result.lower() or "не понимаю" in result.lower():
            await update.message.reply_text("📌 Один из агентов просит уточнение:\n" + result)
        else:
            await update.message.reply_text("✅ Готово! Вот результат:\n" + result)
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")
        traceback.print_exc()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Опрос отменён.")
    return ConversationHandler.END

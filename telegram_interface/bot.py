import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler
from telegram_interface.fsm_handler import (
    start_collecting, goal, platforms, investment, horizon, risk,
    autodeploy, interface, confirm, cancel,
    GOAL, PLATFORMS, INVESTMENT, HORIZON, RISK, AUTODEPLOY, INTERFACE, CONFIRM
)


if __name__ == "__main__":
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("generate", start_collecting)],
        states={
            GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, goal)],
            PLATFORMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, platforms)],
            INVESTMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, investment)],
            HORIZON: [MessageHandler(filters.TEXT & ~filters.COMMAND, horizon)],
            RISK: [MessageHandler(filters.TEXT & ~filters.COMMAND, risk)],
            AUTODEPLOY: [MessageHandler(filters.TEXT & ~filters.COMMAND, autodeploy)],
            INTERFACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, interface)],
            CONFIRM: [CommandHandler("confirm", confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("cancel", cancel))
    app.run_polling()

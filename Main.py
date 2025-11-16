import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Configuración de Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # El bot responderá con este mensaje cuando esté en Render
    await update.message.reply_text("🚀 ¡Tu bot está funcionando 24/7 desde **Render**!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Comandos disponibles:\n/start\n/help")

# --- Función Principal (Preparada para Webhook) ---
def main():
    # 1. Obtener Variables de Entorno (Secrets en Render)
    TOKEN = os.environ.get("BOT_TOKEN")
    PORT = int(os.environ.get("PORT", 8080))
    URL = os.environ.get("RENDER_EXTERNAL_URL") 

    if not TOKEN:
        logger.error("Error: La variable BOT_TOKEN no está definida.")
        return

    # 2. Inicializar la aplicación
    app = ApplicationBuilder().token(TOKEN).build()

    # 3. Añadir Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # 4. Configurar Webhook para Despliegue en Render
    if URL:
        logger.info(f"Iniciando en modo Webhook en el Puerto: {PORT}")
        WEBHOOK_PATH = TOKEN 
        
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=WEBHOOK_PATH,
            webhook_url=URL + "/" + WEBHOOK_PATH,
            secret_token=os.environ.get("WEBHOOK_SECRET", "mi_clave_secreta_default"), 
            drop_pending_updates=True, 
        )
    else:
        # Modo Polling de respaldo (si lo ejecutas localmente)
        logger.warning("RENDER_EXTERNAL_URL no está definida. Ejecutando en modo Polling.")
        app.run_polling()

if __name__ == "__main__":
    main()


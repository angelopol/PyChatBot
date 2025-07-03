# main.py

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from config import TELEGRAM_BOT_TOKEN
from data import MENU_TEXT, PROMOTIONS_TEXT, LOCATION_TEXT, FAQ_TEXT, HUMAN_CONTACT_TEXT
import json
from gemini import onlineResponse

# Configurar el registro (útil para depurar)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Funciones de Comandos ---

async def start(update: Update, context):
    """Maneja el comando /start y muestra el menú principal."""
    user = update.effective_user
    logger.info(f"Usuario {user.full_name} inició el bot.")

    keyboard = [
        [InlineKeyboardButton("🍦 Nuestro Menú", callback_data='menu')],
        [InlineKeyboardButton("🎉 Promociones y Ofertas", callback_data='promociones')],
        [InlineKeyboardButton("📍 ¿Dónde Estamos?", callback_data='ubicacion')],
        [InlineKeyboardButton("❓ Preguntas Frecuentes", callback_data='faq')],
        [InlineKeyboardButton("🗣️ Hablar con un Humano", callback_data='contacto_humano')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        f"¡Hola {user.mention_html()}! 👋 ¡Soy el bot de YogurtLandia, tu asistente para descubrir los sabores más refrescantes! ¿En qué puedo ayudarte hoy?"
    )

    if update.message:
        await update.message.reply_html(text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_html(text, reply_markup=reply_markup)
        await update.callback_query.answer()

async def send_menu(update: Update, context):
    """Envía el menú de helados de yogurt."""
    keyboard = [
        [InlineKeyboardButton("🔙 Volver al Inicio", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        MENU_TEXT, parse_mode='Markdown', reply_markup=reply_markup
    )
    await update.callback_query.answer() # Importante para que el botón deje de "girar"

async def send_promotions(update: Update, context):
    """Envía la información de promociones."""
    keyboard = [
        [InlineKeyboardButton("🔙 Volver al Inicio", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        PROMOTIONS_TEXT, parse_mode='Markdown', reply_markup=reply_markup
    )
    await update.callback_query.answer()

async def send_location(update: Update, context):
    """Envía la ubicación y horarios."""
    keyboard = [
        [InlineKeyboardButton("🔙 Volver al Inicio", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        LOCATION_TEXT, parse_mode='Markdown', reply_markup=reply_markup
    )
    # Opcional: Enviar una ubicación real de Google Maps (requiere latitud y longitud)
    # await update.callback_query.message.reply_location(latitude=10.2000, longitude=-68.0000)
    await update.callback_query.answer()

async def send_faq(update: Update, context):
    """Envía las preguntas frecuentes."""
    keyboard = [
        [InlineKeyboardButton("🔙 Volver al Inicio", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        FAQ_TEXT, parse_mode='Markdown', reply_markup=reply_markup
    )
    await update.callback_query.answer()

async def send_human_contact(update: Update, context):
    """Informa sobre cómo contactar a un humano."""
    keyboard = [
        [InlineKeyboardButton("🔙 Volver al Inicio", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        HUMAN_CONTACT_TEXT, parse_mode='Markdown', reply_markup=reply_markup
    )
    await update.callback_query.answer()

async def button(update: Update, context):
    """Maneja las pulsaciones de los botones Inline."""
    query = update.callback_query
    await query.answer() # Responde a la pulsación para que el usuario sepa que fue recibida

    if query.data == 'menu':
        await send_menu(update, context)
    elif query.data == 'promociones':
        await send_promotions(update, context)
    elif query.data == 'ubicacion':
        await send_location(update, context)
    elif query.data == 'faq':
        await send_faq(update, context)
    elif query.data == 'contacto_humano':
        await send_human_contact(update, context)
    elif query.data == 'start_over':
        await start(update, context) # Vuelve a ejecutar el comando start para mostrar el menú principal



async def unknown(update: Update, context):
    """Responde a mensajes personalizados usando Gemini y muestra el menú principal."""
    # Menú principal
    keyboard = [
        [InlineKeyboardButton("🍦 Nuestro Menú", callback_data='menu')],
        [InlineKeyboardButton("🎉 Promociones y Ofertas", callback_data='promociones')],
        [InlineKeyboardButton("📍 ¿Dónde Estamos?", callback_data='ubicacion')],
        [InlineKeyboardButton("❓ Preguntas Frecuentes", callback_data='faq')],
        [InlineKeyboardButton("🗣️ Hablar con un Humano", callback_data='contacto_humano')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Cargar datos del negocio
    try:
        with open("business.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}
    user_message = update.message.text if update.message else ""
    respuesta = onlineResponse(user_message, data)
    await update.message.reply_text(
        respuesta,
        reply_markup=reply_markup
    )

# --- Función Principal ---

def main():
    """Inicia el bot."""
    # Crea la aplicación y pásale el token de tu bot.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # --- Manejadores de Comandos ---
    application.add_handler(CommandHandler("start", start))

    # --- Manejador de Callbacks (para botones inline) ---
    application.add_handler(CallbackQueryHandler(button))

    # --- Manejador de Mensajes No Reconocidos ---
    # Asegúrate de que este manejador sea el último.
    application.add_handler(MessageHandler(filters.COMMAND, unknown)) # Para comandos que no existen
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown)) # Para texto que no es comando

    # Ejecuta el bot hasta que presiones Ctrl-C
    logger.info("Bot de YogurtLandia iniciando...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
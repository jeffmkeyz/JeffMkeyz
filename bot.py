import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, MenuButtonWebApp
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from flask import Flask, request, jsonify
import threading
import sqlite3

# ─── CONFIG ────────────────────────────────────────────────
BOT_TOKEN  = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "")   # URL de GitHub Pages
PORT       = int(os.environ.get("PORT", 5000))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

# ─── DATABASE ──────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id    INTEGER PRIMARY KEY,
            username   TEXT,
            first_name TEXT,
            is_pro     INTEGER DEFAULT 0,
            joined_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_or_create_user(user_id, username, first_name):
    conn = sqlite3.connect("users.db")
    cur  = conn.cursor()
    cur.execute("SELECT is_pro FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if not row:
        cur.execute(
            "INSERT INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
            (user_id, username, first_name)
        )
        conn.commit()
        is_pro = False
    else:
        is_pro = bool(row[0])
    conn.close()
    return is_pro

def set_pro(user_id: int, value: bool):
    conn = sqlite3.connect("users.db")
    conn.execute("UPDATE users SET is_pro = ? WHERE user_id = ?", (int(value), user_id))
    conn.commit()
    conn.close()

# ─── BOT HANDLERS ──────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user   = update.effective_user
    is_pro = get_or_create_user(user.id, user.username or "", user.first_name or "")

    plan_text = "⭐ *PRO ACTIVO*" if is_pro else "Plan Free — 5 herramientas disponibles"

    keyboard = [[
        InlineKeyboardButton(
            "🎛️ Abrir Artist Vault",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]]

    await update.message.reply_text(
        f"⚡ *ARTIST VAULT*\n"
        f"Herramientas de industria sin filtros.\n\n"
        f"{plan_text}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def setup_menu_button(app):
    """Configura el botón de menú persistente al iniciar el bot."""
    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="🎛️ Artist Vault",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    log.info("Menu button configurado correctamente.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde a cualquier mensaje con el botón directo."""
    user   = update.effective_user
    is_pro = get_or_create_user(user.id, user.username or "", user.first_name or "")

    keyboard = [[
        InlineKeyboardButton(
            "🎛️ Abrir Artist Vault",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]]
    await update.message.reply_text(
        "Toca el botón para abrir la plataforma 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ─── FLASK API (para el Mini App) ─────────────────────────
flask_app = Flask(__name__)

@flask_app.route("/check_plan")
def check_plan():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"is_pro": False})
    conn = sqlite3.connect("users.db")
    cur  = conn.cursor()
    cur.execute("SELECT is_pro FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return jsonify({"is_pro": bool(row[0]) if row else False})

@flask_app.route("/activate_pro", methods=["POST"])
def activate_pro():
    """
    Llamado desde tu sistema de pagos (Stripe, Stars, etc.)
    Body: { "user_id": 123456789 }
    """
    data    = request.get_json()
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"ok": False, "error": "user_id requerido"}), 400
    set_pro(user_id, True)
    return jsonify({"ok": True, "user_id": user_id, "is_pro": True})

@flask_app.route("/health")
def health():
    return jsonify({"status": "ok"})

def run_flask():
    flask_app.run(host="0.0.0.0", port=PORT)

# ─── MAIN ──────────────────────────────────────────────────
def main():
    init_db()

    # Flask en hilo separado
    threading.Thread(target=run_flask, daemon=True).start()
    log.info(f"Flask corriendo en puerto {PORT}")

    # Bot
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Menu button al iniciar
    app.post_init = setup_menu_button

    log.info("Bot iniciado.")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

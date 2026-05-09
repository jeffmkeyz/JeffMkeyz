import os
import json
import sqlite3
import logging
import threading
import requests
from flask import Flask, request, jsonify

# ─── CONFIG ────────────────────────────────────────────────
BOT_TOKEN  = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "")
PORT       = int(os.environ.get("PORT", 8080))
API        = f"https://api.telegram.org/bot{BOT_TOKEN}"

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
            (user_id, username or "", first_name or "")
        )
        conn.commit()
        is_pro = False
    else:
        is_pro = bool(row[0])
    conn.close()
    return is_pro

def set_pro(user_id, value):
    conn = sqlite3.connect("users.db")
    conn.execute("UPDATE users SET is_pro = ? WHERE user_id = ?", (int(value), user_id))
    conn.commit()
    conn.close()

# ─── TELEGRAM API HELPERS ──────────────────────────────────
def send_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    requests.post(f"{API}/sendMessage", json=payload)

def webapp_button():
    return {"inline_keyboard": [[{"text": "🎛️ Abrir Artist Vault", "web_app": {"url": WEBAPP_URL}}]]}

def set_menu_button():
    payload = {"menu_button": {"type": "web_app", "text": "🎛️ Artist Vault", "web_app": {"url": WEBAPP_URL}}}
    r = requests.post(f"{API}/setChatMenuButton", json=payload)
    log.info(f"Menu button: {r.json()}")

# ─── HANDLERS ──────────────────────────────────────────────
def handle_start(chat_id, user):
    is_pro = get_or_create_user(user.get("id"), user.get("username"), user.get("first_name"))
    plan = "⭐ *PRO ACTIVO*" if is_pro else "Plan Free — 5 herramientas disponibles"
    send_message(chat_id, f"⚡ *ARTIST VAULT*\nHerramientas de industria sin filtros.\n\n{plan}", reply_markup=webapp_button())

def handle_message(chat_id):
    send_message(chat_id, "Toca el botón para abrir la plataforma 👇", reply_markup=webapp_button())

# ─── POLLING LOOP ──────────────────────────────────────────
def poll():
    requests.post(f"{API}/deleteWebhook", json={"drop_pending_updates": True})
    offset = None
    log.info("Bot iniciado con polling.")
    while True:
        try:
            params = {"timeout": 30, "allowed_updates": ["message"]}
            if offset:
                params["offset"] = offset
            r = requests.get(f"{API}/getUpdates", params=params, timeout=35)
            for update in r.json().get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message")
                if not msg:
                    continue
                chat_id = msg["chat"]["id"]
                text    = msg.get("text", "")
                if text.startswith("/start"):
                    handle_start(chat_id, msg.get("from", {}))
                else:
                    handle_message(chat_id)
        except Exception as e:
            log.error(f"Polling error: {e}")

# ─── FLASK API ─────────────────────────────────────────────
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
    data    = request.get_json()
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"ok": False}), 400
    set_pro(user_id, True)
    return jsonify({"ok": True, "user_id": user_id, "is_pro": True})

@flask_app.route("/health")
def health():
    return jsonify({"status": "ok"})

# ─── MAIN ──────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    set_menu_button()
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=PORT), daemon=True).start()
    log.info(f"Flask corriendo en puerto {PORT}")
    poll()

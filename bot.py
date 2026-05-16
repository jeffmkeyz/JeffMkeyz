import os
import json
import sqlite3
import logging
import threading
import requests
from flask import Flask, request, jsonify
from youtube_commands import (
    handle_youtube_command,
    handle_youtube_callback,
    handle_youtube_state,
)


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
    return {"inline_keyboard": [[{"text": "🎛️ Abrir MusicCodexBox", "web_app": {"url": WEBAPP_URL}}]]}

def set_menu_button():
    payload = {"menu_button": {"type": "web_app", "text": "🎛️ MusicCodexBox", "web_app": {"url": WEBAPP_URL}}}
    r = requests.post(f"{API}/setChatMenuButton", json=payload)
    log.info(f"Menu button: {r.json()}")

# ─── HANDLERS ──────────────────────────────────────────────
def handle_start(chat_id, user):
    is_pro = get_or_create_user(user.get("id"), user.get("username"), user.get("first_name"))
    plan = "⭐ *PRO ACTIVO*" if is_pro else "Plan Free — 5 herramientas disponibles"
    send_message(chat_id, f"⚡ *MUSICCODEXBOX*\nHerramientas de industria sin filtros.\n\n{plan}", reply_markup=webapp_button())

def handle_message(chat_id):
    send_message(chat_id, "Toca el botón para abrir la plataforma 👇", reply_markup=webapp_button())

# ─── POLLING LOOP ──────────────────────────────────────────
def poll():
    requests.post(f"{API}/deleteWebhook", json={"drop_pending_updates": True})
    offset = None
    log.info("Bot iniciado con polling.")

    def send_msg(chat_id, text, markup=None):
        payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        if markup:
            payload["reply_markup"] = markup
        try:
            requests.post(f"{API}/sendMessage", json=payload)
        except Exception as e:
            log.error(f"send_msg error: {e}")

    while True:
        try:
            params = {"timeout": 30, "allowed_updates": ["message", "callback_query"]}
            if offset:
                params["offset"] = offset
            r = requests.get(f"{API}/getUpdates", params=params, timeout=35)
            for update in r.json().get("result", []):
                offset = update["update_id"] + 1

                # ── Callback queries (inline buttons) ──
                cb = update.get("callback_query")
                if cb:
                    cb_data = cb.get("data", "")
                    cb_chat = cb["message"]["chat"]["id"]
                    cb_user = cb["from"]["id"]
                    requests.post(f"{API}/answerCallbackQuery",
                        json={"callback_query_id": cb["id"]})
                    if cb_data.startswith("yt_"):
                        handle_youtube_callback(cb_chat, cb_user, cb_data, send_msg)
                    continue

                # ── Regular messages ──
                msg = update.get("message")
                if not msg:
                    continue
                chat_id = msg["chat"]["id"]
                user_id = msg["from"]["id"]
                text    = msg.get("text", "")

                if not text:
                    continue

                # /youtube module
                if text.lower().startswith("/youtube"):
                    handle_youtube_command(chat_id, user_id, text, send_msg,
                        lambda markup: json.dumps(markup))
                    continue

                # /start
                if text.startswith("/start"):
                    handle_start(chat_id, msg.get("from", {}))
                    continue

                # State machine (youtube multi-step)
                if handle_youtube_state(chat_id, user_id, text, send_msg):
                    continue

                # Default
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

# ─── TIKTOK OAUTH ───────────────────────────────────────────
TIKTOK_CLIENT_KEY    = os.environ.get("TIKTOK_CLIENT_KEY", "")
TIKTOK_CLIENT_SECRET = os.environ.get("TIKTOK_CLIENT_SECRET", "")
TIKTOK_REDIRECT_URI  = "https://jeffmkeyz.github.io/JeffMkeyz/tiktok-callback.html"

import urllib.parse, urllib.request, secrets, json as _json

def init_tiktok_db():
    conn = sqlite3.connect("users.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS tiktok_tokens (
        user_id INTEGER PRIMARY KEY, access_token TEXT,
        open_id TEXT, expires_at INTEGER,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit(); conn.close()

@flask_app.route("/tiktok/auth_url")
def tiktok_auth_url():
    user_id = request.args.get("user_id")
    if not user_id: return jsonify({"ok": False, "error": "user_id required"}), 400
    state = secrets.token_hex(16) + f"_{user_id}"
    params = {"client_key": TIKTOK_CLIENT_KEY, "response_type": "code",
              "scope": "user.info.stats,user.info.profile,video.list",
              "redirect_uri": TIKTOK_REDIRECT_URI, "state": state}
    url = "https://www.tiktok.com/v2/auth/authorize/?" + urllib.parse.urlencode(params)
    return jsonify({"ok": True, "url": url})

@flask_app.route("/tiktok/callback", methods=["POST"])
def tiktok_callback():
    data = request.get_json()
    code = data.get("code"); state = data.get("state")
    if not code: return jsonify({"ok": False, "error": "No code"}), 400
    try: user_id = int(state.split("_")[-1]) if state else 0
    except: user_id = 0
    payload = _json.dumps({"client_key": TIKTOK_CLIENT_KEY, "client_secret": TIKTOK_CLIENT_SECRET,
        "code": code, "grant_type": "authorization_code", "redirect_uri": TIKTOK_REDIRECT_URI}).encode()
    req = urllib.request.Request("https://open.tiktokapis.com/v2/oauth/token/",
        data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req) as res: token_data = _json.loads(res.read())
    except Exception as e: return jsonify({"ok": False, "error": str(e)}), 500
    if "access_token" not in token_data: return jsonify({"ok": False, "error": "Token failed"}), 400
    conn = sqlite3.connect("users.db")
    conn.execute("INSERT OR REPLACE INTO tiktok_tokens (user_id,access_token,open_id,expires_at) VALUES (?,?,?,?)",
        (user_id, token_data["access_token"], token_data.get("open_id",""), token_data.get("expires_in",86400)))
    conn.commit(); conn.close()
    return jsonify({"ok": True})

@flask_app.route("/tiktok/stats")
def tiktok_stats():
    user_id = request.args.get("user_id", type=int)
    if not user_id: return jsonify({"ok": False, "error": "user_id required"}), 400
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT access_token FROM tiktok_tokens WHERE user_id=?", (user_id,))
    row = cur.fetchone(); conn.close()
    if not row: return jsonify({"ok": False, "connected": False})
    req = urllib.request.Request(
        "https://open.tiktokapis.com/v2/user/info/?fields=display_name,follower_count,likes_count,video_count",
        headers={"Authorization": f"Bearer {row[0]}"})
    try:
        with urllib.request.urlopen(req) as res:
            data = _json.loads(res.read())
        return jsonify({"ok": True, "connected": True, "data": data.get("data",{}).get("user",{})})
    except Exception as e: return jsonify({"ok": False, "error": str(e)}), 500

@flask_app.route("/tiktok/webhook", methods=["POST"])
def tiktok_webhook():
    log.info(f"TikTok webhook: {request.get_json()}")
    return jsonify({"ok": True})

"""
youtube_commands.py — Módulo /youtube para MusicCodexBox
Stack: Python puro + requests (sin dependencias externas)
"""

import json
import sqlite3
from datetime import datetime

# ── GENRE DATABASE (Python) ────────────────────────────────────────────────
GENRE_DB = {
    "trap_latino": {
        "name": "Trap Latino", "bpm": [70, 145],
        "tags": ["trap latino", "trap en español", "rap latino", "urban latino",
                 "musica urbana", "trap 2025", "latin trap", "rap español",
                 "trap dominicano", "nuevo trap", "flow", "calle"],
        "moods": ["oscuro", "melancólico", "agresivo", "íntimo"],
        "hashtags": ["#TrapLatino", "#TrapEspañol", "#MusicaUrbana", "#UrbanLatino",
                     "#Flow", "#Trap2025", "#RapLatino", "#Calle"],
        "refs": ["Bad Bunny", "Anuel AA", "Bryant Myers", "Eladio Carrión"],
        "yt_category": "Music", "yt_lang": "es"
    },
    "reggaeton": {
        "name": "Reggaeton", "bpm": [85, 100],
        "tags": ["reggaeton", "perreo", "musica latina", "latin music",
                 "reggaeton 2025", "nuevo reggaeton", "urbano latino",
                 "reggaeton nuevo", "latin urban", "dembow"],
        "moods": ["fiesta", "sensual", "energético", "calle"],
        "hashtags": ["#Reggaeton", "#Perreo", "#MusicaLatina", "#UrbanLatino",
                     "#Reggaeton2025", "#LatinMusic", "#Dembow"],
        "refs": ["Bad Bunny", "J Balvin", "Daddy Yankee", "Ozuna"],
        "yt_category": "Music", "yt_lang": "es"
    },
    "dembow": {
        "name": "Dembow", "bpm": [115, 130],
        "tags": ["dembow", "dembow dominicano", "musica dominicana", "RD music",
                 "urban dominicano", "dembow 2025", "pachangeo", "saoco",
                 "musica rd", "flow dominicano", "tigueraje"],
        "moods": ["fiesta", "calle", "energético", "dominicano"],
        "hashtags": ["#Dembow", "#MusicaDominicana", "#RD", "#Saoco",
                     "#UrbanoDominicano", "#Pachangeo", "#Dembow2025"],
        "refs": ["El Alfa", "Rochy RD", "Bulin 47", "Chimbala"],
        "yt_category": "Music", "yt_lang": "es"
    },
    "afrobeat": {
        "name": "Afrobeat", "bpm": [90, 115],
        "tags": ["afrobeats", "afrobeat", "afropop", "african music",
                 "afrobeats 2025", "afrofusion", "afro music", "groove",
                 "naija music", "afroswing", "dancehall afro"],
        "moods": ["alegre", "sensual", "energético", "groove"],
        "hashtags": ["#Afrobeats", "#Afrobeat", "#AfroPop", "#AfroMusic",
                     "#Groove", "#Afrofusion", "#Afrobeats2025"],
        "refs": ["Burna Boy", "Wizkid", "Rema", "Davido"],
        "yt_category": "Music", "yt_lang": "en"
    },
    "bachata": {
        "name": "Bachata", "bpm": [110, 130],
        "tags": ["bachata", "bachata 2025", "nueva bachata", "bachata moderna",
                 "bachata romantica", "musica dominicana", "bachata urbana",
                 "latin music", "romantic latin", "bachata nueva"],
        "moods": ["romántico", "melancólico", "pasional", "íntimo"],
        "hashtags": ["#Bachata", "#BachataRomantica", "#NuevaBachata",
                     "#MusicaDominicana", "#Bachata2025", "#LatinMusic"],
        "refs": ["Romeo Santos", "Prince Royce", "Aventura"],
        "yt_category": "Music", "yt_lang": "es"
    },
    "r&b": {
        "name": "R&B", "bpm": [60, 95],
        "tags": ["rnb", "r&b", "soul music", "r&b 2025", "new rnb",
                 "contemporary r&b", "rnb español", "slow jam",
                 "r&b latino", "soul", "melodic rnb"],
        "moods": ["romántico", "sensual", "melancólico", "íntimo"],
        "hashtags": ["#RnB", "#Soul", "#SlowJam", "#RnB2025",
                     "#NewRnB", "#MelodicRnB", "#RnBLatino"],
        "refs": ["Frank Ocean", "The Weeknd", "SZA", "Brent Faiyaz"],
        "yt_category": "Music", "yt_lang": "es"
    },
    "pop_urbano": {
        "name": "Pop Urbano", "bpm": [80, 120],
        "tags": ["pop urbano", "pop latino", "latin pop", "musica pop latina",
                 "pop 2025", "latin urban", "pop en español",
                 "nuevo pop latino", "pop urbano 2025"],
        "moods": ["alegre", "energético", "romántico", "positivo"],
        "hashtags": ["#PopUrbano", "#PopLatino", "#LatinPop",
                     "#MusicaLatina", "#Pop2025", "#PopEnEspañol"],
        "refs": ["Maluma", "J Balvin", "Karol G", "Rauw Alejandro"],
        "yt_category": "Music", "yt_lang": "es"
    },
    "drill": {
        "name": "Drill", "bpm": [138, 145],
        "tags": ["drill", "uk drill", "drill music", "drill beat",
                 "drill 2025", "drill latino", "dark trap", "drill español"],
        "moods": ["agresivo", "oscuro", "callejero", "tenso"],
        "hashtags": ["#Drill", "#UKDrill", "#DrillMusic", "#DrillBeat",
                     "#Drill2025", "#DrillLatino"],
        "refs": ["Pop Smoke", "Central Cee", "Dave"],
        "yt_category": "Music", "yt_lang": "es"
    },
    "lofi": {
        "name": "Lo-Fi", "bpm": [60, 90],
        "tags": ["lofi", "lofi hip hop", "chill beats", "study music",
                 "lofi beats", "lofi music", "chill music", "relax music",
                 "lofi chill", "beats to study"],
        "moods": ["tranquilo", "nostálgico", "relajado", "concentrado"],
        "hashtags": ["#LoFi", "#LoFiHipHop", "#ChillBeats", "#StudyMusic",
                     "#LoFiBeats", "#ChillMusic"],
        "refs": ["Nujabes", "J Dilla", "Lofi Girl"],
        "yt_category": "Music", "yt_lang": "en"
    },
    "house": {
        "name": "House / Tech House", "bpm": [120, 135],
        "tags": ["house music", "tech house", "electronic music", "club music",
                 "house 2025", "underground house", "deep house", "4x4"],
        "moods": ["eufórico", "hipnótico", "libre", "nocturno"],
        "hashtags": ["#HouseMusic", "#TechHouse", "#ElectronicMusic",
                     "#ClubMusic", "#House2025", "#DeepHouse"],
        "refs": ["Fisher", "Chris Lake", "John Summit", "Fred Again"],
        "yt_category": "Music", "yt_lang": "en"
    },
}

# Default genre for unknown
DEFAULT_GENRE = GENRE_DB["trap_latino"]

# ── MARKET TIMES ──────────────────────────────────────────────────────────
MARKET_TIMES = {
    "tiktok": {
        "es": {"time": "21:00–22:30 Madrid", "label": "🇪🇸 España/Europa"},
        "la": {"time": "22:00–23:30 Madrid (su 21:00)", "label": "🌎 Latinoamérica"},
        "us": {"time": "02:00–04:00 Madrid (su 21:00 EST)", "label": "🇺🇸 USA Latino"},
        "sweet": {"time": "21:00–23:00 Madrid", "label": "⭐ Sweet Spot — Ambos"},
    },
    "reels": {
        "es": {"time": "20:00–22:00 Madrid", "label": "🇪🇸 España/Europa"},
        "la": {"time": "22:00–00:00 Madrid", "label": "🌎 Latinoamérica"},
        "us": {"time": "02:00–04:00 Madrid", "label": "🇺🇸 USA Latino"},
        "sweet": {"time": "21:00–23:00 Madrid", "label": "⭐ Sweet Spot"},
    },
}

# ── CONVERSATION STATE ─────────────────────────────────────────────────────
# user_id → {"step": str, "data": dict}
STATES = {}

def set_state(uid, step, data=None):
    STATES[uid] = {"step": step, "data": data or {}}

def get_state(uid):
    return STATES.get(uid, None)

def clear_state(uid):
    STATES.pop(uid, None)

# ── GENRE LOOKUP ───────────────────────────────────────────────────────────
def get_genre(genre_input):
    g = genre_input.lower().strip()
    mapping = {
        "trap": "trap_latino", "trap latino": "trap_latino",
        "reggaeton": "reggaeton", "dembow": "dembow",
        "afrobeat": "afrobeat", "afrobeats": "afrobeat",
        "bachata": "bachata", "r&b": "r&b", "rnb": "r&b",
        "pop": "pop_urbano", "pop urbano": "pop_urbano",
        "drill": "drill", "lofi": "lofi", "lo-fi": "lofi",
        "house": "house", "tech house": "house",
    }
    slug = mapping.get(g, None)
    if not slug:
        for key in GENRE_DB:
            if key in g or g in key:
                slug = key
                break
    return GENRE_DB.get(slug, DEFAULT_GENRE)

# ── WATCH HOURS DB ─────────────────────────────────────────────────────────
def get_watch_hours(user_id):
    try:
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("SELECT watch_hours FROM watch_hours WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else 0
    except:
        return 0

def save_watch_hours(user_id, hours):
    try:
        conn = sqlite3.connect("users.db")
        conn.execute("""CREATE TABLE IF NOT EXISTS watch_hours
            (user_id INTEGER PRIMARY KEY, watch_hours REAL, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)""")
        conn.execute("INSERT OR REPLACE INTO watch_hours (user_id, watch_hours) VALUES (?,?)", (user_id, hours))
        conn.commit()
        conn.close()
    except:
        pass

# ── METADATA GENERATOR ────────────────────────────────────────────────────
def generate_metadata(track_name, genre_input):
    g = get_genre(genre_input)
    gname = g["name"]
    tags = g["tags"]
    hashtags = g["hashtags"]
    refs = g["refs"]
    year = datetime.now().year

    # YouTube title — 3 variants
    titles = [
        f"{track_name} 🔥 | {gname} {year}",
        f"{track_name} | Official Audio",
        f"{track_name} (Official Video) — {gname}",
    ]

    # Description
    desc = f"""{track_name} — ya disponible en todas las plataformas.

🎵 Escucha en Spotify: [ENLACE]
🍎 Apple Music: [ENLACE]
📲 Seguir en Instagram: [ENLACE]
🎵 TikTok: [ENLACE]

━━━━━━━━━━━━━━━━━━━━━━━
📌 SOBRE EL TEMA
{track_name} es un tema de {gname} producido y escrito por Jeff Mkeyz.
Un sonido {', '.join(g['moods'][:2])}, con influencias de {', '.join(refs[:2])}.

━━━━━━━━━━━━━━━━━━━━━━━
🎬 MÁS CONTENIDO
→ BTS y proceso de grabación
→ Beats y producciones nuevas
→ Tips de industria musical
→ Making of de mis lanzamientos

Suscríbete para no perderte nada 🔔

━━━━━━━━━━━━━━━━━━━━━━━
#{track_name.replace(' ', '')} #{gname.replace(' ', '')} #MusicaLatina #NuevoTema #{year}

Tags: {', '.join(tags[:15])}"""

    # Tags string (500 chars max for YT)
    all_tags = tags + [track_name.lower(), "jeff mkeyz", "musica nueva", "nuevo tema",
                       gname.lower(), f"musica {year}", "lanzamiento"]
    tags_str = ", ".join(all_tags[:30])

    # TikTok captions
    tiktok_captions = [
        f"'{track_name}' ya fuera 🔥 {' '.join(hashtags[:4])} #NuevoTema",
        f"Este tema lo hice para los que... 👀 '{track_name}' {' '.join(hashtags[:3])}",
        f"¿Ya lo escuchaste? '{track_name}' 🎵 {' '.join(hashtags[:4])} #MusicaLatina",
    ]

    # Reels captions
    reels_captions = [
        f"🔥 NEW MUSIC · '{track_name}' ya disponible en todas las plataformas\nLink en bio 👆\n\n{' '.join(hashtags[:5])} #NuevoTema #MusicaLatina",
        f"'{track_name}' — {gname} · {year}\n\nEscúchalo completo, link en bio 🎵\n\n{' '.join(hashtags[:5])}",
    ]

    return {
        "track": track_name,
        "genre": gname,
        "titles": titles,
        "description": desc,
        "tags": tags_str,
        "tiktok_captions": tiktok_captions,
        "reels_captions": reels_captions,
        "hashtags": hashtags,
    }

def format_metadata_message(meta):
    t = meta
    msg = f"""🎬 *METADATA COMPLETA — {t['track']}*
_{t['genre']}_

━━━━━━━━━━━━━━━━━━━━━
📌 *TÍTULOS YOUTUBE* (elige uno)

`{t['titles'][0]}`

`{t['titles'][1]}`

`{t['titles'][2]}`

━━━━━━━━━━━━━━━━━━━━━
🏷️ *TAGS*
`{t['tags']}`

━━━━━━━━━━━━━━━━━━━━━
🎵 *CAPTIONS TIKTOK*

① `{t['tiktok_captions'][0]}`

② `{t['tiktok_captions'][1]}`

━━━━━━━━━━━━━━━━━━━━━
📸 *CAPTIONS REELS*

`{t['reels_captions'][0]}`

━━━━━━━━━━━━━━━━━━━━━
⏰ *HORARIOS ÓPTIMOS*
🇪🇸 TikTok/Reels: *21:00–22:30 Madrid*
🌎 LatAm llega: *22:00–23:30 Madrid*
⭐ Sweet spot: *21:00–23:00 Madrid*

📅 Release: *Viernes 00:00 UTC*

━━━━━━━━━━━━━━━━━━━━━
La descripción completa de YouTube la tienes con /youtube desc"""
    return msg

def format_description_message(meta):
    return f"""📝 *DESCRIPCIÓN YOUTUBE — {meta['track']}*

```
{meta['description']}
```

_Copia y personaliza los enlaces antes de publicar_"""

# ── CONTENT GENERATOR ─────────────────────────────────────────────────────
def generate_content_plan(track_name, genre_input):
    g = get_genre(genre_input)
    gname = g["name"]
    tags_base = g["tags"][:8]
    year = datetime.now().year

    videos = [
        {
            "num": 1,
            "type": "BTS / Proceso de grabación",
            "icon": "🎤",
            "title": f"Así grabé '{track_name}' | BTS Estudio | {gname}",
            "duration": "5–8 min",
            "desc": f"Video detrás de cámaras de la sesión de grabación de '{track_name}'. Muestra el proceso real: la cabina, los takes, el montaje del micrófono, los nervios y la magia del estudio.",
            "hook": f"'Así fue grabar {track_name}...' (primeros 3s en cabina)",
            "tags": f"{track_name.lower()}, bts estudio, behind the scenes, grabacion, {gname.lower()}, proceso musical, {', '.join(tags_base[:5])}",
            "watch_hours_potential": "Alto — los BTS retienen bien",
        },
        {
            "num": 2,
            "type": "Beat breakdown / Producción",
            "icon": "🎛️",
            "title": f"Hice este beat de {gname} en 1 hora | '{track_name}' production",
            "duration": "6–10 min",
            "desc": f"Proceso completo de producción del instrumental de '{track_name}' en FL Studio. Desde el loop base hasta el mixdown. Ideal para productores y fans del proceso creativo.",
            "hook": "Pantalla del DAW desde el segundo 1 — el beat empezando",
            "tags": f"fl studio tutorial, beat making, {gname.lower()} beat, produccion musical, como hacer un beat, {track_name.lower()}, {', '.join(tags_base[:4])}",
            "watch_hours_potential": "Muy alto — audiencia de productores retiene 70%+",
        },
        {
            "num": 3,
            "type": "Lyric video / Letra del tema",
            "icon": "📝",
            "title": f"{track_name} | Letra Completa | {gname} {year}",
            "duration": "Duración del tema + 30s",
            "desc": f"Letra completa de '{track_name}' con el audio oficial. Diseño minimal con la estética del single. Ideal para que los fans aprendan la letra y aumenta tiempo de visualización.",
            "hook": "Portada del single + primera línea de letra en los primeros 2s",
            "tags": f"{track_name.lower()} letra, {track_name.lower()} lyrics, {gname.lower()}, musica latina, {year}, {', '.join(tags_base[:5])}",
            "watch_hours_potential": "Muy alto — los lyric videos acumulan horas orgánicamente",
        },
        {
            "num": 4,
            "type": "Day in the life / Rutina del artista",
            "icon": "📅",
            "title": f"Un día en mi vida como artista independiente | Lanzando '{track_name}'",
            "duration": "8–12 min",
            "desc": f"Vlog del día de lanzamiento de '{track_name}'. Desde preparar el contenido por la mañana hasta ver los primeros streams en Spotify for Artists por la noche. Auténtico y sin filtros.",
            "hook": "'Hoy sale mi nuevo tema...' (cara a cámara, tono real)",
            "tags": f"artista independiente, day in the life, lanzamiento musical, {track_name.lower()}, musica independiente, spotify for artists, {', '.join(tags_base[:4])}",
            "watch_hours_potential": "Alto — el formato vlog retiene 50%+ si es auténtico",
        },
    ]

    return {
        "track": track_name,
        "genre": gname,
        "videos": videos,
    }

def format_content_message(plan):
    msg = f"""📺 *PLAN DE CONTENIDO — {plan['track']}*
_4 videos para acumular watch hours esta semana_

"""
    for v in plan['videos']:
        msg += f"""{v['icon']} *VIDEO {v['num']} — {v['type']}*
📌 Título: `{v['title']}`
⏱️ Duración: {v['duration']}
🎬 Hook: _{v['hook']}_
📈 Potencial: {v['watch_hours_potential']}

"""
    msg += """━━━━━━━━━━━━━━━━━━━━━
💡 *ESTRATEGIA*
Publica en este orden:
• Día del release → Lyric video
• +2 días → BTS grabación  
• +4 días → Beat breakdown
• +6 días → Day in the life

Los primeros 7 días de un tema son los más importantes para el algoritmo de YouTube.

Usa /youtube tags para los tags completos de cada video."""
    return msg

def format_video_tags(plan, video_num):
    if video_num < 1 or video_num > len(plan['videos']):
        return "Número de video inválido."
    v = plan['videos'][video_num - 1]
    return f"""🏷️ *TAGS — VIDEO {video_num}*
_{v['title']}_

`{v['tags']}`"""

# ── WATCH HOURS CALCULATOR ────────────────────────────────────────────────
def calculate_watch_hours(current_hours, videos_per_week=2, avg_duration_min=5, avg_views=50):
    """
    current_hours: horas actuales del canal
    videos_per_week: videos que publica
    avg_duration_min: duración promedio de videos
    avg_views: views promedio por video primera semana
    """
    target = 4000  # YPP requires 4000, not 3000 (common mistake, actual is 4000)
    # Wait, actually YPP requires 4,000 watch hours. But the user said 3,000.
    # Let me use what the user said (3,000) but note actual is 4,000
    target_user = 3000
    target_real = 4000

    remaining_user = max(0, target_user - current_hours)
    remaining_real = max(0, target_real - current_hours)

    # Hours per week from new uploads
    # avg_views * (avg_duration_min * 0.5 / 60) = hours per video (assume 50% retention)
    retention = 0.50
    hours_per_video = avg_views * (avg_duration_min * retention / 60)
    hours_per_week = videos_per_week * hours_per_video

    # Also organic accumulation from existing videos (estimated 10% of weekly new)
    organic = hours_per_week * 0.1
    total_weekly = hours_per_week + organic

    if total_weekly <= 0:
        weeks_user = weeks_real = 9999
    else:
        weeks_user = remaining_user / total_weekly
        weeks_real = remaining_real / total_weekly

    months_user = weeks_user / 4.33
    months_real = weeks_real / 4.33

    # Percentage progress
    pct_user = min(100, (current_hours / target_user) * 100)
    pct_real = min(100, (current_hours / target_real) * 100)

    bar_user = "█" * int(pct_user / 10) + "░" * (10 - int(pct_user / 10))
    bar_real = "█" * int(pct_real / 10) + "░" * (10 - int(pct_real / 10))

    msg = f"""⏱️ *WATCH HOURS CALCULATOR*

📊 *ESTADO ACTUAL*
Horas registradas: *{current_hours:,.0f}h*

━━━━━━━━━━━━━━━━━━━━━
🎯 *META 3,000h* (tu objetivo)
`{bar_user}` {pct_user:.1f}%
Faltan: *{remaining_user:,.0f}h*
Ritmo actual: ~{total_weekly:.1f}h/semana
⏳ Estimado: *{months_user:.1f} meses* ({weeks_user:.0f} semanas)

━━━━━━━━━━━━━━━━━━━━━
✅ *META REAL YPP — 4,000h*
`{bar_real}` {pct_real:.1f}%
Faltan: *{remaining_real:,.0f}h*
⏳ Estimado: *{months_real:.1f} meses* ({weeks_real:.0f} semanas)

⚠️ _YouTube requiere 4,000h reales para el YPP, no 3,000. Con 3,000h estás al {pct_real:.0f}% del camino._

━━━━━━━━━━━━━━━━━━━━━
💡 *CÓMO ACELERAR*

Con *{videos_per_week} videos/semana* de ~{avg_duration_min} min:
→ Lyric videos acumulan horas 24/7
→ BTS de 8–10 min = más horas por view
→ Shorts NO cuentan para el YPP

🚀 *Si subes 4 videos/semana:*
"""
    if total_weekly > 0:
        weeks_4v = remaining_real / (total_weekly * 2)
        msg += f"→ Llegarías en *{weeks_4v:.0f} semanas* ({weeks_4v/4.33:.1f} meses)\n"

    msg += f"""
📈 *Asumiendo:* {avg_views} views/video · 50% retención · {avg_duration_min}min duración

Actualiza tus horas reales con:
/youtube horas [número]"""

    return msg

# ── COMMAND HANDLERS ──────────────────────────────────────────────────────
def handle_youtube_command(chat_id, user_id, text, send_fn, reply_markup_fn):
    """
    Main router for /youtube commands.
    send_fn(chat_id, text, markup=None) — sends a message
    """
    text = text.strip()
    parts = text.split(None, 2)
    cmd = parts[1].lower() if len(parts) > 1 else ""

    # ── /youtube (menu) ──
    if not cmd:
        keyboard = {
            "inline_keyboard": [
                [{"text": "🎬 Generar Metadata", "callback_data": "yt_metadata"}],
                [{"text": "📺 Plan de Contenido", "callback_data": "yt_content"}],
                [{"text": "⏱️ Watch Hours", "callback_data": "yt_watchhours"}],
            ]
        }
        send_fn(chat_id,
            "🎬 *MÓDULO YOUTUBE*\n\nElige qué quieres generar:",
            markup=json.dumps(keyboard))
        return

    # ── /youtube metadata [track] [genre] ──
    if cmd == "metadata":
        if len(parts) < 4:
            set_state(user_id, "yt_meta_track")
            send_fn(chat_id, "🎬 *Generador de Metadata*\n\n¿Cuál es el nombre del tema?")
        else:
            track = parts[2]
            genre = parts[3] if len(parts) > 3 else "trap"
            meta = generate_metadata(track, genre)
            send_fn(chat_id, format_metadata_message(meta))
        return

    # ── /youtube desc ──
    if cmd == "desc":
        state = get_state(user_id)
        if state and "meta" in state.get("data", {}):
            send_fn(chat_id, format_description_message(state["data"]["meta"]))
        else:
            send_fn(chat_id, "Primero genera la metadata con /youtube metadata [tema] [género]")
        return

    # ── /youtube content [track] [genre] ──
    if cmd == "content":
        if len(parts) < 4:
            set_state(user_id, "yt_content_track")
            send_fn(chat_id, "📺 *Plan de Contenido*\n\n¿Cuál es el nombre del tema recién lanzado?")
        else:
            track = parts[2]
            genre = parts[3] if len(parts) > 3 else "trap"
            plan = generate_content_plan(track, genre)
            set_state(user_id, "yt_content_done", {"plan": plan})
            send_fn(chat_id, format_content_message(plan))
        return

    # ── /youtube tags [1-4] ──
    if cmd == "tags":
        state = get_state(user_id)
        if state and "plan" in state.get("data", {}):
            try:
                num = int(parts[2]) if len(parts) > 2 else 1
                send_fn(chat_id, format_video_tags(state["data"]["plan"], num))
            except:
                send_fn(chat_id, "Uso: /youtube tags 1 (para el video 1, hasta 4)")
        else:
            send_fn(chat_id, "Primero genera el plan con /youtube content [tema] [género]")
        return

    # ── /youtube horas [número] ──
    if cmd == "horas":
        if len(parts) < 3:
            current = get_watch_hours(user_id)
            send_fn(chat_id, calculate_watch_hours(current))
        else:
            try:
                hours = float(parts[2].replace(",", "."))
                save_watch_hours(user_id, hours)
                send_fn(chat_id, calculate_watch_hours(hours))
            except:
                send_fn(chat_id, "Formato: /youtube horas 150.5")
        return

    # ── /youtube watchhours ──
    if cmd == "watchhours":
        current = get_watch_hours(user_id)
        if current == 0:
            set_state(user_id, "yt_hours_input")
            send_fn(chat_id, "⏱️ *Watch Hours Calculator*\n\n¿Cuántas horas de visualización tienes actualmente en tu canal?\n\nEscribe el número (ej: 127.5)")
        else:
            send_fn(chat_id, calculate_watch_hours(current))
        return

    # ── Unknown ──
    send_fn(chat_id,
        "🎬 *Módulo YouTube*\n\n"
        "Comandos disponibles:\n"
        "/youtube metadata — Genera título, desc, tags y captions\n"
        "/youtube content — Plan de 4 videos de proceso\n"
        "/youtube horas [número] — Calcula watch hours\n"
        "/youtube desc — Descripción completa (tras metadata)\n"
        "/youtube tags [1-4] — Tags de cada video (tras content)")

# ── CALLBACK HANDLERS ─────────────────────────────────────────────────────
def handle_youtube_callback(chat_id, user_id, data, send_fn):
    if data == "yt_metadata":
        set_state(user_id, "yt_meta_track")
        send_fn(chat_id, "🎬 *Generar Metadata*\n\nEscribe: nombre del tema y género\n\nEjemplo:\n`No Te Pienso bachata`")
    elif data == "yt_content":
        set_state(user_id, "yt_content_track")
        send_fn(chat_id, "📺 *Plan de Contenido*\n\nEscribe: nombre del tema y género\n\nEjemplo:\n`Una y Media r&b`")
    elif data == "yt_watchhours":
        current = get_watch_hours(user_id)
        if current == 0:
            set_state(user_id, "yt_hours_input")
            send_fn(chat_id, "⏱️ ¿Cuántas horas de visualización tienes ahora?\n\nEscribe solo el número (ej: `127`)")
        else:
            send_fn(chat_id, calculate_watch_hours(current))

# ── MESSAGE STATE HANDLER ─────────────────────────────────────────────────
def handle_youtube_state(chat_id, user_id, text, send_fn):
    """Returns True if message was handled by youtube state machine."""
    state = get_state(user_id)
    if not state:
        return False

    step = state["step"]

    if step == "yt_meta_track":
        parts = text.strip().split(None, 1)
        if len(parts) < 1:
            send_fn(chat_id, "Escribe el nombre del tema y el género. Ej: `No Te Pienso bachata`")
            return True
        # Try to split track and genre
        words = text.strip().split()
        # Last word could be genre
        known_genres = ["trap", "reggaeton", "dembow", "afrobeat", "bachata",
                        "r&b", "rnb", "pop", "drill", "lofi", "house"]
        genre = "trap"
        track = text.strip()
        for g in known_genres:
            if text.lower().endswith(g):
                genre = g
                track = text[:-(len(g))].strip()
                break

        meta = generate_metadata(track, genre)
        set_state(user_id, "yt_meta_done", {"meta": meta})
        send_fn(chat_id, format_metadata_message(meta))
        return True

    if step == "yt_content_track":
        text = text.strip()
        known_genres = ["trap", "reggaeton", "dembow", "afrobeat", "bachata",
                        "r&b", "rnb", "pop", "drill", "lofi", "house"]
        genre = "trap"
        track = text
        for g in known_genres:
            if text.lower().endswith(g):
                genre = g
                track = text[:-(len(g))].strip()
                break

        plan = generate_content_plan(track, genre)
        set_state(user_id, "yt_content_done", {"plan": plan})
        send_fn(chat_id, format_content_message(plan))
        return True

    if step == "yt_hours_input":
        try:
            hours = float(text.strip().replace(",", "."))
            save_watch_hours(user_id, hours)
            clear_state(user_id)
            send_fn(chat_id, calculate_watch_hours(hours))
        except:
            send_fn(chat_id, "Escribe solo el número. Ej: `127` o `1250.5`")
        return True

    return False

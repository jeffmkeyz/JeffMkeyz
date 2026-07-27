🧩 MKEYZ OS — La unidad todopoderosa
Todo el ecosistema Mkeyz en un solo deploy: Hub del productor, Publisherz, Mkeyz Studio Bot (DAW en Telegram), 12 mini apps y las Artist Tools. En producción: https://mkeyzos.up.railway.app

Qué incluye
Pieza	Origen	Dónde vive ahora
Hub del productor (catálogo, releases, royalties, tareas, generador IA)	Mkeyz Sound Hub v2	/ (Mini App principal, fullscreen en móvil)
Publisherz — el maestro del algoritmo (con Cobalt downloader)	mkeyz-publisher.html intacto	/publisher
Mkeyz Studio Bot — DAW, análisis, pagos Stars, comunidad	Mkeyz Daw Bot (menús = solo herramientas nativas + lanzador del OS)	proceso bot.py (Telegram)
Mini apps del Studio (Beat Battle, BPM game, RPG, Views Tracker, Voice, Chords…)	Mkeyz Daw Bot	/game, /bpm, /game2, /views…
Artist Tools (bio, ISRC, pitch, planner…)	Artist Vault (depurado)	/tools/*.html
Seguridad (HMAC initData, Fernet, rate limit)	Multi-Perfil IA	backend/security.py
Sincronización multi-dispositivo: dentro de Telegram, el Hub se autentica solo con el initData firmado — misma cuenta = mismos datos en móvil, tablet y PC. En navegador normal se pega el HUB_TOKEN en Ajustes una vez.

Depurado en 2026-07: Frecuencias, Escala, VPS Simulator y Comparador quedaron fuera del OS (fuente original en 01-Mkeyz-Daw por si se recuperan). El bot dejó de listar herramientas HTML: es el arranque del OS + sus herramientas nativas de chat (DAW, analizador, calculadora, cotizador, comunidad, planes Stars).

Arquitectura
00-Mkeyz-OS/
├── backend/
│   ├── app.py          ← Flask unificado: API Hub (/api/v1) + frontend + Publisherz
│   ├── studio_api.py   ← Blueprint: API de juegos/battles/economía (rutas idénticas al server.py original)
│   ├── security.py     ← validate_tg_data (HMAC), Fernet, rate limiter
│   ├── bot.py          ← Mkeyz Studio Bot (intacto; DB por MKEYZ_DB_PATH)
│   └── youtube_commands.py ← módulo YouTube + genre DB (integración pendiente)
├── webapp/             ← Mini App del Hub (con vista lanzadora "Mkeyz OS")
│   ├── publisher/      ← Publisherz completo, sin tocar
│   └── tools/          ← Artist Tools
├── static/             ← las mini apps HTML del Studio
├── start.sh            ← gunicorn + bot (si hay BOT_TOKEN)
└── Procfile / runtime.txt / requirements.txt / .env.example
Un solo servicio Flask sirve TODO; el bot corre como proceso paralelo dentro del mismo contenedor (igual que hacía el Daw Bot original). Ambos comparten mkeyz.db; el Hub usa hub.db.

Arranque local
pip install -r requirements.txt      # el bot necesita además ffmpeg instalado
python backend/app.py                # → http://localhost:5000
# con bot:  BOT_TOKEN=xxx sh start.sh
Sin HUB_TOKEN la API queda abierta (solo aceptable en localhost). Sin BOT_TOKEN el bot no arranca, el resto funciona completo.

Deploy en Railway
Sube esta carpeta a un repo y conéctalo a Railway.
Volume en /data + variables de .env.example (mínimo HUB_TOKEN, DB_PATH=/data/hub.db, MKEYZ_DB_PATH=/data/mkeyz.db).
Para el bot: BOT_TOKEN, ADMIN_ID, GAME_URL=<URL pública del deploy>.
En @BotFather: /newapp → URL pública → la Mini App es el OS entero.
Autenticación de la API del Hub
Con HUB_TOKEN definido, /api/v1/* acepta cualquiera de las dos:

Authorization: Bearer <HUB_TOKEN> (como siempre, desde Ajustes), o
Authorization: <initData de Telegram> con firma HMAC válida (la Mini App dentro de Telegram entra sin pegar token).
Las rutas de juegos (/api/battles, /api/mkeyz, …) mantienen el comportamiento original del Studio (abiertas, mismo contrato que las mini apps). POST /api/tg/verify valida un initData y devuelve el tg_id real firmado.

Los 3 principios del OS
Depuración implacable — aquí solo entró lo mejor de cada repo.
Conservar la excelencia — Publisherz y el bot van byte a byte intactos.
Nivel Top — DAW y algoritmo operativos tal cual; la modularización de Publisherz (si algún día se hace) será después y con red de seguridad.

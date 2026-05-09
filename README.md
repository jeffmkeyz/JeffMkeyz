# 🎛️ Artist Vault Bot

Plataforma de herramientas para artistas. Mini App de Telegram con modelo Freemium.

## Estructura del repo

```
artist-vault-bot/
├── index.html        ← Mini App (sube a GitHub Pages)
├── bot.py            ← Bot de Telegram + API Flask
├── requirements.txt  ← Dependencias Python
├── Procfile          ← Para Railway
└── .env.example      ← Variables de entorno
```

---

## Setup paso a paso

### 1. GitHub Pages (Mini App)

1. Sube `index.html` a tu repo de GitHub
2. Ve a **Settings → Pages → Source: Deploy from branch → main → / (root)**
3. Tu URL será: `https://jeffmkeyz.github.io/NOMBRE-DEL-REPO/`

### 2. Variables en Railway

En el panel de Railway → Variables, agrega:

| Variable   | Valor                                    |
|------------|------------------------------------------|
| BOT_TOKEN  | Token de BotFather                       |
| WEBAPP_URL | URL de GitHub Pages (con https://)       |

### 3. BotFather

```
/setmenubutton → tu bot → pega WEBAPP_URL → texto: 🎛️ Artist Vault
```

### 4. index.html — actualizar URL del backend

En `index.html` busca esta línea y reemplaza con tu URL de Railway:

```javascript
const res = await fetch(`https://TU-BOT.railway.app/check_plan?user_id=${userId}`);
```

---

## API Endpoints

| Endpoint            | Método | Descripción                    |
|---------------------|--------|--------------------------------|
| `/check_plan`       | GET    | Verifica si user_id es Pro     |
| `/activate_pro`     | POST   | Activa Pro para un usuario     |
| `/health`           | GET    | Health check para Railway      |

### Activar Pro manualmente (pruebas)

```bash
curl -X POST https://TU-BOT.railway.app/activate_pro \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123456789}'
```

---

## Agregar herramientas reales

En `index.html`, busca el array `TOOLS` y reemplaza `url:"#"` con la URL real de cada herramienta:

```javascript
{ id:1, tier:"free", ..., url:"https://tu-herramienta.com" },
```

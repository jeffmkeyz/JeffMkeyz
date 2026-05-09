/**
 * ARTIST VAULT — GENRE DATABASE v1.0
 * ─────────────────────────────────────────────────────────────
 * Arquitectura escalable. Cada género tiene su propio bloque de
 * metadata. Para conectar APIs externas en el futuro, reemplaza
 * GenreDB.get(slug) con una llamada fetch() al endpoint y usa
 * este objeto como fallback local.
 *
 * ESTRUCTURA DE CADA GÉNERO:
 * {
 *   name        : string   — Nombre oficial del género
 *   slug        : string   — Identificador único (para API keys)
 *   parent      : string   — Género padre (null si es raíz)
 *   bpm         : [min,max]— Rango de BPM típico
 *   keys        : string[] — Tonalidades más usadas
 *   tags        : string[] — Smart tags para contenido
 *   moods       : string[] — Emociones y estados de ánimo
 *   aesthetic   : string[] — Estética visual / referencias
 *   seo         : string[] — Keywords SEO para plataformas
 *   platforms   : {}       — Mejores plataformas + peso (1-10)
 *   refs        : string[] — Artistas de referencia
 *   release     : {}       — Tips de lanzamiento específicos
 *   captions    : string[] — Estilos de caption recomendados
 *   visual      : string[] — Ideas de contenido visual
 *   collab      : string[] — Géneros compatibles para fusiones
 * }
 */

const GENRE_DB = {

  // ── URBANO LATINO ──────────────────────────────────────────

  reggaeton: {
    name: 'Reggaeton', slug: 'reggaeton', parent: null,
    bpm: [85, 100],
    keys: ['Am', 'Dm', 'Gm', 'Cm'],
    tags: ['perreo', 'calle', 'flow', 'ritmo', 'dembow', 'barrio', 'calor'],
    moods: ['fiesta', 'sensual', 'energético', 'calle', 'confianza'],
    aesthetic: ['neones', 'ciudad nocturna', 'colores vivos', 'lujo urbano', 'caribe'],
    seo: ['reggaeton 2025', 'nuevo reggaeton', 'perreo', 'reggaeton latino', 'urbano latino'],
    platforms: { TikTok: 10, Instagram: 9, YouTube: 8, Spotify: 9 },
    refs: ['Bad Bunny', 'J Balvin', 'Daddy Yankee', 'Ozuna', 'Anuel AA', 'Rauw Alejandro'],
    release: {
      bestDay: 'Viernes',
      bestTime: '00:00 EST',
      preLaunch: 'Teaser de 15s en TikTok 48h antes',
      tip: 'Las playlists de reggaeton en Spotify se actualizan los viernes. Pedir pitch con 7 días de anticipación.'
    },
    captions: ['🔥 calle pura', 'el ritmo no miente 🎵', 'dale que prende 🕺'],
    visual: ['video en rooftop nocturno', 'estética neón caribeña', 'outfits oversized coloridos'],
    collab: ['trap_latino', 'dembow', 'dancehall', 'pop_urbano']
  },

  trap_latino: {
    name: 'Trap Latino', slug: 'trap_latino', parent: 'reggaeton',
    bpm: [70, 145],
    keys: ['Am', 'Dm', 'Em', 'Bm'],
    tags: ['trap', 'calle', 'barrio', 'melancolía', 'drip', 'tigueraje', 'dinero'],
    moods: ['oscuro', 'melancólico', 'agresivo', 'íntimo', 'reflexivo', 'confiado'],
    aesthetic: ['oscuro', 'humo', 'luces rojas', 'money', 'grillz', 'tattoos'],
    seo: ['trap latino', 'trap español', 'drill latino', 'trap 2025', 'rap latino'],
    platforms: { TikTok: 9, Instagram: 8, YouTube: 9, SoundCloud: 7 },
    refs: ['Bad Bunny', 'Anuel AA', 'Bryant Myers', 'Jhay Cortez', 'Eladio Carrión', 'Mora'],
    release: {
      bestDay: 'Jueves o Viernes',
      bestTime: '23:00 local',
      preLaunch: 'Snippet de 30s con el hook más oscuro',
      tip: 'El trap latino funciona muy bien en playlists "late night". Tag: dark trap, melodic trap.'
    },
    captions: ['nadie te dijo que sería fácil 🖤', 'el barrio no olvida 🔫', 'flow sin filtros'],
    visual: ['sesión nocturna en coche', 'estudio oscuro con luces led', 'lifestyle minimalista negro'],
    collab: ['reggaeton', 'drill', 'pluggnb', 'rage', 'r&b']
  },

  dembow: {
    name: 'Dembow', slug: 'dembow', parent: 'reggaeton',
    bpm: [115, 130],
    keys: ['Am', 'Dm', 'Gm'],
    tags: ['dembow', 'RD', 'pachangeo', 'saoco', 'calle dominicana', 'tigueraje', 'flow RD'],
    moods: ['fiesta', 'calle', 'energético', 'dominicano', 'orgullo', 'flow'],
    aesthetic: ['colores caribeños', 'barrio dominicano', 'estética RD', 'tropical urbano'],
    seo: ['dembow dominicano', 'música dominicana', 'dembow 2025', 'urbano RD', 'música RD'],
    platforms: { TikTok: 10, Instagram: 9, YouTube: 8, Spotify: 7 },
    refs: ['El Alfa', 'Bulin 47', 'Rochy RD', 'Chimbala', 'Toxic Crow', 'Mozart La Para'],
    release: {
      bestDay: 'Viernes',
      bestTime: '08:00 EST',
      preLaunch: 'Clip de baile con el beat antes del lanzamiento',
      tip: 'El dembow domina TikTok con challenges de baile. Crea un paso específico para el tema.'
    },
    captions: ['puro saoco 🇩🇴', 'el flow no se compra 🔥', 'RD en la cima'],
    visual: ['barrio dominicano', 'challenge de baile', 'colores vivos tropicales'],
    collab: ['reggaeton', 'dancehall', 'afrobeat', 'trap_latino']
  },

  drill: {
    name: 'Drill', slug: 'drill', parent: null,
    bpm: [138, 145],
    keys: ['Am', 'Dm', 'Gm', 'Cm', 'Fm'],
    tags: ['drill', 'oscuro', 'agresivo', 'calle', 'trap', 'UK drill', 'Chicago'],
    moods: ['agresivo', 'oscuro', 'tenso', 'callejero', 'amenazante'],
    aesthetic: ['gris urbano', 'mascarillas', 'estética UK', 'dark', 'CCTV aesthetic'],
    seo: ['drill music', 'uk drill', 'drill latino', 'drill beat', 'drill 2025'],
    platforms: { YouTube: 10, TikTok: 8, SoundCloud: 9, Instagram: 7 },
    refs: ['Pop Smoke', 'Central Cee', 'Dave', 'Unknown T', 'Headie One', 'Fivio Foreign'],
    release: {
      bestDay: 'Viernes',
      bestTime: '00:00 UK time',
      preLaunch: 'Video lyric o visualizer oscuro',
      tip: 'El drill funciona muy bien en YouTube con visualizers. Los fans consumen álbumes y proyectos, no singles sueltos.'
    },
    captions: ['sin filtros 🔪', 'las calles hablan solas', 'drill puro 🩶'],
    visual: ['callejones oscuros', 'hoodie y mascarilla', 'blanco y negro urbano'],
    collab: ['trap_latino', 'jersey_drill', 'uk_garage', 'boom_bap']
  },

  jersey_club: {
    name: 'Jersey Club', slug: 'jersey_club', parent: null,
    bpm: [130, 160],
    keys: ['Am', 'Cm', 'Fm'],
    tags: ['jersey', 'club', 'baile', 'breaks', 'footwork', 'NJ', 'energético'],
    moods: ['eufórico', 'bailable', 'caótico', 'fiesta', 'movimiento'],
    aesthetic: ['club nocturno', 'luces estroboscópicas', 'underground', 'NYC vibe'],
    seo: ['jersey club', 'jersey club music', 'club music 2025', 'dance music', 'jersey bounce'],
    platforms: { TikTok: 10, Instagram: 8, YouTube: 7, SoundCloud: 8 },
    refs: ['DJ Smallz 732', 'Nadus', 'TT the Artist', 'Uniiqu3', 'DJ Sliink'],
    release: {
      bestDay: 'Jueves',
      bestTime: '18:00 EST',
      preLaunch: 'Video de baile con el beat antes del drop',
      tip: 'El Jersey Club se viraliza por challenges de baile en TikTok. El video de baile ES el marketing.'
    },
    captions: ['no para el club 🚨', 'si no bailas no lo entiendes 💃', 'Jersey en la sangre'],
    visual: ['challenge de baile', 'club con luces', 'video de baile callejero'],
    collab: ['dancehall', 'afrobeat', 'house', 'jersey_drill']
  },

  jersey_drill: {
    name: 'Jersey Drill', slug: 'jersey_drill', parent: 'drill',
    bpm: [138, 150],
    keys: ['Am', 'Dm', 'Gm'],
    tags: ['jersey drill', 'NJ', 'drill', 'club', 'fusión', 'energético', 'oscuro'],
    moods: ['agresivo', 'eufórico', 'callejero', 'energético'],
    aesthetic: ['urbano NJ', 'oscuro con energía', 'underground club'],
    seo: ['jersey drill', 'jersey drill music', 'drill club', 'nj drill'],
    platforms: { TikTok: 9, YouTube: 8, SoundCloud: 8 },
    refs: ['Sha Ek', 'Dusty Locane', 'Bizzy Banks'],
    release: { bestDay: 'Viernes', bestTime: '00:00', preLaunch: 'Clip oscuro 15s', tip: 'Fusiona el drill visual con la energía de baile del Jersey Club para diferenciarte.' },
    captions: ['ni drill ni club, los dos 🔪💃', 'NJ sin filtros'],
    visual: ['club oscuro', 'callejón nocturno NJ'],
    collab: ['drill', 'jersey_club', 'trap_latino']
  },

  afrobeat: {
    name: 'Afrobeat / Afrobeats', slug: 'afrobeat', parent: null,
    bpm: [90, 115],
    keys: ['Dm', 'Am', 'Gm', 'Cm', 'F'],
    tags: ['afro', 'groove', 'baile', 'África', 'percusión', 'vibra', 'caliente', 'positivo'],
    moods: ['alegre', 'sensual', 'energético', 'positivo', 'cultural', 'bailable'],
    aesthetic: ['colores africanos', 'naturaleza', 'telas coloridas', 'sunset', 'tropical'],
    seo: ['afrobeats 2025', 'afro music', 'afropop', 'música africana', 'afrofusion'],
    platforms: { TikTok: 10, Instagram: 9, YouTube: 8, Spotify: 9, Apple: 8 },
    refs: ['Burna Boy', 'Wizkid', 'Afroboiz', 'Rema', 'Tems', 'Davido', 'Ayra Starr'],
    release: {
      bestDay: 'Viernes',
      bestTime: '00:00 GMT',
      preLaunch: 'Video de baile con energía positiva',
      tip: 'Pitchear en playlists de Afrobeats en Spotify. El mercado UK y Nigeria son clave.'
    },
    captions: ['the groove never stops 🌍', 'afro energy only ✨', 'feel the rhythm 🥁'],
    visual: ['sunset en playa', 'colores vibrantes', 'danza afro', 'naturaleza + ciudad'],
    collab: ['dancehall', 'reggaeton', 'dembow', 'pop_urbano', 'r&b']
  },

  dancehall: {
    name: 'Dancehall', slug: 'dancehall', parent: null,
    bpm: [85, 110],
    keys: ['Am', 'Dm', 'Gm', 'Cm'],
    tags: ['dancehall', 'Jamaica', 'riddim', 'skank', 'vibra', 'caribe', 'baile'],
    moods: ['alegre', 'sensual', 'relajado', 'calle', 'vibra positiva'],
    aesthetic: ['Jamaica', 'colores caribeños', 'playa', 'rasta', 'tropical'],
    seo: ['dancehall music', 'dancehall 2025', 'reggae dancehall', 'caribbean music'],
    platforms: { YouTube: 9, Instagram: 8, TikTok: 8, Spotify: 7 },
    refs: ['Vybz Kartel', 'Popcaan', 'Skillibeng', 'Masicka', 'Alkaline', 'Sean Paul'],
    release: { bestDay: 'Viernes', bestTime: '09:00 EST', preLaunch: 'Clip de baile o riddim drop', tip: 'Las playlists de Caribbean Heat en Spotify son clave. Conectar con comunidad jamaicana en diaspora.' },
    captions: ['riddim cyaan done 🎶', 'jamaican vibes only 🇯🇲', 'feel di riddim'],
    visual: ['playa al atardecer', 'colores Jamaica', 'baile en la calle'],
    collab: ['afrobeat', 'reggaeton', 'dembow', 'uk_garage']
  },

  bachata: {
    name: 'Bachata', slug: 'bachata', parent: null,
    bpm: [110, 130],
    keys: ['Am', 'Dm', 'Em', 'Bm'],
    tags: ['bachata', 'romántico', 'guitarra', 'RD', 'amor', 'desamor', 'baile de pareja'],
    moods: ['romántico', 'melancólico', 'nostálgico', 'pasional', 'íntimo'],
    aesthetic: ['pareja bailando', 'puesta de sol', 'calles dominicanas', 'luces cálidas'],
    seo: ['bachata 2025', 'nueva bachata', 'bachata romántica', 'bachata moderna', 'bachata urbana'],
    platforms: { Spotify: 10, YouTube: 9, Instagram: 8, TikTok: 7 },
    refs: ['Romeo Santos', 'Prince Royce', 'Aventura', 'Juan Luis Guerra', 'Toby Love'],
    release: { bestDay: 'Viernes', bestTime: '00:00 EST', preLaunch: 'Video de pareja bailando o clip acústico', tip: 'Las playlists de bachata en Spotify tienen millones de seguidores. Fundamental pedir pitch. Los viernes a las 00:00 EST.' },
    captions: ['el amor no tiene idioma 🌹', 'bachata en el alma 🎸', 'siente la bachata'],
    visual: ['pareja en atardecer', 'guitarra acústica', 'luces cálidas y cine'],
    collab: ['reggaeton', 'pop_urbano', 'r&b', 'dembow']
  },

  corridos_tumbados: {
    name: 'Corridos Tumbados', slug: 'corridos_tumbados', parent: null,
    bpm: [75, 95],
    keys: ['Am', 'Dm', 'Em', 'Gm'],
    tags: ['corridos', 'mexicano', 'tumbados', 'narco estética', 'pistolas', 'sierreño', 'regional'],
    moods: ['orgulloso', 'nostálgico', 'macho', 'calle', 'regional', 'épico'],
    aesthetic: ['México', 'sombrero', 'botas', 'desierto', 'camionetas', 'rancho moderno'],
    seo: ['corridos tumbados 2025', 'corridos nuevos', 'regional mexicano', 'música mexicana', 'sierreño'],
    platforms: { YouTube: 10, Spotify: 9, TikTok: 8, Instagram: 7 },
    refs: ['Natanael Cano', 'Junior H', 'Peso Pluma', 'Fuerza Regida', 'Eslabón Armado'],
    release: { bestDay: 'Viernes', bestTime: '00:00 CST', preLaunch: 'Video en rancho o desierto', tip: 'El mercado mexicano y chicano en EE.UU. es masivo. YouTube es la plataforma principal. Los visualizers con estética narco-ranchera funcionan muy bien.' },
    captions: ['puro México 🇲🇽', 'corrido sin filtros 🤠', 'la sierra habla sola'],
    visual: ['rancho al atardecer', 'camioneta en carretera', 'estética norteña moderna'],
    collab: ['trap_latino', 'reggaeton', 'pop_urbano']
  },

  // ── ELECTRÓNICA ────────────────────────────────────────────

  house: {
    name: 'House / Tech House', slug: 'house', parent: null,
    bpm: [120, 135],
    keys: ['Am', 'Dm', 'Gm', 'Fm', 'Cm'],
    tags: ['house', 'club', '4x4', 'groove', 'underground', 'dancefloor', 'electronic'],
    moods: ['eufórico', 'hipnótico', 'libre', 'nocturno', 'elevado'],
    aesthetic: ['club oscuro', 'strobes', 'underground', 'Ibiza', 'minimal chic'],
    seo: ['tech house 2025', 'house music', 'electronic music', 'club music', 'house beat'],
    platforms: { Spotify: 9, SoundCloud: 10, YouTube: 7, Beatport: 10, Instagram: 8 },
    refs: ['Fisher', 'Chris Lake', 'John Summit', 'Fred Again..', 'Skrillex', 'Disclosure'],
    release: { bestDay: 'Viernes', bestTime: '00:00 GMT', preLaunch: 'Preview de 60s en SoundCloud', tip: 'Beatport y SoundCloud son esenciales para el mercado house. Enviar a DJs para que lo incluyan en sets.' },
    captions: ['the floor never lies 🎛️', 'underground always wins', '4x4 forever ♾️'],
    visual: ['club con luces', 'DJ set', 'multitud en festival', 'estética minimalista'],
    collab: ['edm', 'uk_garage', 'afrobeat', 'dancehall']
  },

  edm: {
    name: 'EDM', slug: 'edm', parent: null,
    bpm: [126, 145],
    keys: ['Am', 'Cm', 'Dm', 'Gm', 'F'],
    tags: ['festival', 'drop', 'build-up', 'EDM', 'electrónico', 'rave', 'anthem'],
    moods: ['eufórico', 'épico', 'energético', 'liberador', 'masivo'],
    aesthetic: ['festival', 'fuegos artificiales', 'multitudes', 'pantallas LED', 'colores neón'],
    seo: ['edm 2025', 'festival music', 'electronic dance music', 'rave music', 'edm drop'],
    platforms: { Spotify: 9, YouTube: 10, TikTok: 8, SoundCloud: 8, Beatport: 9 },
    refs: ['Martin Garrix', 'Tiësto', 'Afrojack', 'Hardwell', 'Alesso', 'Zedd'],
    release: { bestDay: 'Viernes', bestTime: '00:00 CET', preLaunch: 'Drop snippet de 15s', tip: 'Los vídeos de festival experience en YouTube son esenciales. Sincronizar con temporada de festivales (mayo-agosto).' },
    captions: ['the drop hits different 🔊', 'festival season always 🎡', 'no ceiling on this one'],
    visual: ['festival con pirotecnia', 'multitud levantando las manos', 'DJ en escenario grande'],
    collab: ['house', 'pop_urbano', 'hyperpop']
  },

  lofi: {
    name: 'Lo-Fi', slug: 'lofi', parent: null,
    bpm: [60, 90],
    keys: ['Dm', 'Am', 'Gm', 'Cm', 'Fm'],
    tags: ['lofi', 'chill', 'estudio', 'relajado', 'lluvia', 'café', 'nostálgico', 'beats'],
    moods: ['tranquilo', 'nostálgico', 'concentrado', 'melancólico', 'relajado'],
    aesthetic: ['animé chill', 'lluvia en ventana', 'café y libros', 'atardecer japonés', 'vintage'],
    seo: ['lofi beats', 'lofi hip hop', 'chill beats', 'study music', 'lofi 2025'],
    platforms: { YouTube: 10, Spotify: 9, SoundCloud: 8, Apple: 7 },
    refs: ['Nujabes', 'J Dilla', 'Lofi Girl', 'ChilledCow', 'Idealism', 'Philanthrope'],
    release: { bestDay: 'Domingo', bestTime: '10:00 local', preLaunch: 'Clip de video con estética animé chill', tip: 'Las playlists de "study beats" y "chill beats" en Spotify tienen audiencias masivas. El arte del single es crucial en este género.' },
    captions: ['just breathe 🌧️', 'beats for your thoughts ☕', 'slow down, it\'s okay 🍃'],
    visual: ['ventana con lluvia animada', 'café con libros', 'atardecer en japonés'],
    collab: ['boom_bap', 'r&b', 'experimental', 'pluggnb']
  },

  uk_garage: {
    name: 'UK Garage / UKG', slug: 'uk_garage', parent: null,
    bpm: [128, 140],
    keys: ['Am', 'Dm', 'Gm', 'Cm'],
    tags: ['UK garage', 'UKG', 'speed garage', '2-step', 'UK', 'club', 'shuffle'],
    moods: ['eufórico', 'nostálgico', 'bailable', 'underground UK'],
    aesthetic: ['UK club años 90-2000', 'puffer jackets', 'Londres nocturno'],
    seo: ['uk garage music', 'ukg 2025', '2-step', 'speed garage', 'uk club music'],
    platforms: { SoundCloud: 10, YouTube: 8, Spotify: 7, Instagram: 7 },
    refs: ['Craig David', 'MJ Cole', 'Artful Dodger', 'So Solid Crew', 'Burial'],
    release: { bestDay: 'Jueves', bestTime: '18:00 GMT', preLaunch: 'Preview en SoundCloud', tip: 'La comunidad UK Garage es nicho pero muy leal. SoundCloud y los DJs de radio UK son clave.' },
    captions: ['UKG never died 🇬🇧', 'two-step til morning', 'proper garage vibes'],
    visual: ['club UK nocturno', 'Londres años 2000', 'estética nostálgica UK'],
    collab: ['dancehall', 'house', 'drill', 'grime']
  },

  // ── HIP HOP / RAP ─────────────────────────────────────────

  boom_bap: {
    name: 'Boom Bap', slug: 'boom_bap', parent: null,
    bpm: [80, 100],
    keys: ['Am', 'Dm', 'Gm', 'Cm', 'Fm'],
    tags: ['boom bap', 'hip hop clásico', 'sample', 'NY', 'consciente', 'bars', 'flow'],
    moods: ['consciente', 'nostálgico', 'agresivo', 'poético', 'auténtico'],
    aesthetic: ['NY años 90', 'blanco y negro', 'graffiti', 'Timberlands', 'cassette'],
    seo: ['boom bap 2025', 'hip hop clásico', 'old school hip hop', 'boom bap beats', 'ny rap'],
    platforms: { YouTube: 10, SoundCloud: 9, Spotify: 8, Apple: 7 },
    refs: ['Nas', 'Jay-Z', 'Biggie', 'Rakim', 'Big L', 'Pete Rock', 'DJ Premier'],
    release: { bestDay: 'Viernes', bestTime: '00:00 EST', preLaunch: 'Cipher o freestyle video', tip: 'La comunidad boom bap valora la autenticidad sobre el marketing. Los ciphers en YouTube y los freestyles en radio hip hop son el canal más efectivo.' },
    captions: ['real hip hop never dies 🎤', 'bars por encima de todo', 'la cultura primero'],
    visual: ['rooftop NYC', 'estudio analógico', 'blanco y negro con graffiti'],
    collab: ['lofi', 'drill', 'r&b', 'experimental']
  },

  rage: {
    name: 'Rage / Plugg', slug: 'rage', parent: 'trap_latino',
    bpm: [60, 80],
    keys: ['Am', 'Dm', 'Gm', 'Bm'],
    tags: ['rage', 'slowed', 'dark', 'melodic', 'plugg', 'trap oscuro', 'experimental'],
    moods: ['oscuro', 'melancólico', 'agresivo suave', 'hipnótico', 'dreamy'],
    aesthetic: ['oscuro', 'niebla', 'colores apagados', 'minimal', 'lo-fi oscuro'],
    seo: ['rage beat', 'plugg music', 'rage trap', 'dark trap 2025', 'melodic rage'],
    platforms: { SoundCloud: 10, TikTok: 9, YouTube: 8, Spotify: 7 },
    refs: ['Summrs', 'Autumn!', 'Grizzy Hendrix', 'K$upreme', 'Yeat'],
    release: { bestDay: 'Jueves noche', bestTime: '22:00 EST', preLaunch: 'Snippet oscuro con aesthetic visual', tip: 'SoundCloud es la plataforma principal para rage/plugg. Los fans buscan activamente en SoundCloud antes que en Spotify.' },
    captions: ['no cap never 🌑', 'dark by design', 'the rage don\'t stop 🩶'],
    visual: ['estética oscura con niebla', 'colores desaturados', 'edición lenta y cinematográfica'],
    collab: ['trap_latino', 'pluggnb', 'drill', 'lofi']
  },

  pluggnb: {
    name: 'Pluggnb', slug: 'pluggnb', parent: null,
    bpm: [55, 75],
    keys: ['Am', 'Dm', 'Gm', 'Bm', 'Em'],
    tags: ['pluggnb', 'melodic', 'dark r&b', 'trap r&b', 'dreamy', 'emotional', 'oscuro'],
    moods: ['melancólico', 'romántico oscuro', 'dreamy', 'íntimo', 'emocional'],
    aesthetic: ['luces tenues', 'oscuro romántico', 'neón suave', 'aesthetic chill dark'],
    seo: ['pluggnb', 'plug r&b', 'dark rnb 2025', 'melodic trap r&b', 'emotional trap'],
    platforms: { SoundCloud: 10, Spotify: 8, TikTok: 9, YouTube: 7 },
    refs: ['Rio Da Yung OG', 'Babyface Ray', 'Bnyx', 'Clavish'],
    release: { bestDay: 'Miércoles o Jueves', bestTime: '20:00 EST', preLaunch: 'Clip oscuro de 15s en TikTok', tip: 'El género vive en SoundCloud y TikTok. Las colabs con productores de beats en esas plataformas son el mejor networking.' },
    captions: ['feelings on the beat 🖤', 'oscuro pero lo siento todo', 'plug in the dark'],
    visual: ['cuarto oscuro con luz suave', 'slow-motion cinematográfico', 'estética dreamy'],
    collab: ['rage', 'r&b', 'trap_latino', 'lofi']
  },

  detroit_type_beat: {
    name: 'Detroit Type Beat', slug: 'detroit_type_beat', parent: null,
    bpm: [68, 85],
    keys: ['Am', 'Dm', 'Gm', 'Cm'],
    tags: ['detroit', 'type beat', 'sample flip', 'melodic', 'gritty', 'midwest'],
    moods: ['gritty', 'melancólico', 'callejero', 'auténtico', 'frío'],
    aesthetic: ['Detroit industrial', 'invierno', 'gris urbano', 'midwest aesthetic'],
    seo: ['detroit type beat', 'detroit rap beat', 'midwest rap', 'detroit hip hop 2025'],
    platforms: { YouTube: 10, SoundCloud: 9, Spotify: 7 },
    refs: ['42 Dugg', 'Veeze', 'Babyface Ray', 'Icewear Vezzo', 'Sada Baby'],
    release: { bestDay: 'Viernes', bestTime: '00:00 EST', preLaunch: 'Freestyle o snippet', tip: 'YouTube es el principal canal para type beats. Optimizar el título con "type beat + artista" para búsqueda orgánica.' },
    captions: ['detroit on the map 🔩', 'midwest finest', 'gritty by default'],
    visual: ['Detroit urbano en invierno', 'fábrica abandonada', 'calles midwest'],
    collab: ['boom_bap', 'trap_latino', 'drill', 'rage']
  },

  // ── R&B / SOUL ─────────────────────────────────────────────

  r_and_b: {
    name: 'R&B', slug: 'r&b', parent: null,
    bpm: [60, 95],
    keys: ['Dm', 'Am', 'Gm', 'Cm', 'Fm', 'Bbm'],
    tags: ['r&b', 'soul', 'amor', 'sensual', 'vocal', 'groove', 'íntimo', 'melancolía'],
    moods: ['romántico', 'sensual', 'melancólico', 'íntimo', 'nostálgico', 'confiado'],
    aesthetic: ['luces cálidas', 'íntimo', 'lujoso', 'velas', 'noche urbana', 'minimal elegante'],
    seo: ['r&b 2025', 'new r&b', 'rnb music', 'soul music', 'contemporary r&b'],
    platforms: { Spotify: 10, Apple: 10, YouTube: 8, Instagram: 8, TikTok: 7 },
    refs: ['Frank Ocean', 'SZA', 'The Weeknd', 'Brent Faiyaz', 'Summer Walker', 'H.E.R.'],
    release: { bestDay: 'Viernes', bestTime: '00:00 EST', preLaunch: 'Clip íntimo o a capella', tip: 'Apple Music es muy importante en R&B. Los editoriales de Apple son críticos. El R&B en Spotify se coloca en playlists de "New Music Friday" y "RnB United".' },
    captions: ['feelings can\'t lie 💫', 'soul in every note 🎙️', 'late night vibrations'],
    visual: ['sesión íntima con velas', 'estudio con luces cálidas', 'película cinematográfica'],
    collab: ['trap_latino', 'pop_urbano', 'pluggnb', 'afrobeat', 'bachata']
  },

  // ── POP URBANO / MAINSTREAM ────────────────────────────────

  pop_urbano: {
    name: 'Pop Urbano', slug: 'pop_urbano', parent: null,
    bpm: [80, 120],
    keys: ['Am', 'Dm', 'Gm', 'Cm', 'F', 'C'],
    tags: ['pop', 'urbano', 'mainstream', 'viral', 'catchy', 'radio', 'gancho'],
    moods: ['alegre', 'energético', 'romántico', 'confiado', 'positivo'],
    aesthetic: ['colorido', 'moderno', 'lifestyle', 'lujo accesible', 'aspiracional'],
    seo: ['pop urbano 2025', 'latin pop', 'pop latino', 'música pop', 'pop urbano nuevo'],
    platforms: { Spotify: 10, TikTok: 10, Instagram: 9, YouTube: 9, Apple: 9 },
    refs: ['Maluma', 'J Balvin', 'Karol G', 'Shakira', 'Anitta', 'Becky G'],
    release: { bestDay: 'Viernes', bestTime: '00:00 EST', preLaunch: 'Teaser de 30s con el hook en TikTok', tip: 'El pop urbano necesita radio promotion. Pitch a playlists editoriales de Spotify y Apple con 4-6 semanas de anticipación.' },
    captions: ['new music out now 🎵', 'el tema del verano llegó ☀️', 'escúchalo ya'],
    visual: ['video producido', 'lifestyle aspiracional', 'colores vibrantes'],
    collab: ['reggaeton', 'afrobeat', 'r&b', 'bachata', 'edm']
  },

  // ── EXPERIMENTAL / NICHO ───────────────────────────────────

  hyperpop: {
    name: 'Hyperpop', slug: 'hyperpop', parent: null,
    bpm: [140, 180],
    keys: ['Am', 'Dm', 'Cm', 'Gm'],
    tags: ['hyperpop', 'glitch', 'distorsión', 'PC music', 'internet', 'Y2K', 'caótico'],
    moods: ['eufórico', 'caótico', 'irónico', 'digital', 'futurista', 'intenso'],
    aesthetic: ['Y2K', 'cyber', 'glitch art', 'pink y azul neón', 'internet aesthetic', 'anime 3D'],
    seo: ['hyperpop 2025', 'pc music', 'hyperpop artists', 'glitchpop', 'digital pop'],
    platforms: { TikTok: 10, SoundCloud: 9, Spotify: 7, YouTube: 8 },
    refs: ['100 gecs', 'Charli XCX', 'SOPHIE', 'A.G. Cook', 'Dorian Electra', 'Arca'],
    release: { bestDay: 'Cualquier día', bestTime: 'Cualquier hora (caos intencional)', preLaunch: 'Glitch teaser o arte digital extraño', tip: 'El hyperpop se viraliza por lo extraño y lo inesperado. TikTok y Discord son los canales principales. La comunidad es muy online.' },
    captions: ['🌸⚡💥 [no necesita explicación]', 'glitch in the system', 'too digital 4 u'],
    visual: ['glitch art', 'estética Y2K 3D', 'colores chillidos con distorsión'],
    collab: ['edm', 'experimental', 'jersey_club', 'rage']
  },

  experimental: {
    name: 'Experimental', slug: 'experimental', parent: null,
    bpm: [0, 999],
    keys: ['cualquier'],
    tags: ['experimental', 'avant-garde', 'sonido único', 'arte', 'sin límites', 'exploración'],
    moods: ['abstracto', 'reflexivo', 'perturbador', 'hipnótico', 'libre'],
    aesthetic: ['arte contemporáneo', 'abstracto', 'instalación', 'minimalismo extremo'],
    seo: ['experimental music', 'avant garde', 'alternative music', 'art music', 'unconventional'],
    platforms: { Bandcamp: 10, SoundCloud: 9, YouTube: 8, Spotify: 6 },
    refs: ['Arca', 'Bjork', 'Kendrick Lamar', 'Iglooghost', 'Huerco S.'],
    release: { bestDay: 'Sin patrón fijo', bestTime: 'Cuando esté listo', preLaunch: 'Instalación o experiencia visual', tip: 'Bandcamp es la plataforma más respetada para experimental. Los medios de arte y cultura (Pitchfork, The Wire) son los canales de PR.' },
    captions: ['art is the answer 🎨', 'sin reglas, sin límites', 'escucha diferente'],
    visual: ['instalación de arte', 'video experimental abstracto', 'visuales generativos'],
    collab: ['lofi', 'hyperpop', 'boom_bap', 'pluggnb']
  },

  // ── TABLA DE LOOKUP (slug -> objeto) ──────────────────────
};

// ─── API LAYER (preparado para futura integración) ───────────
/**
 * GenreDB — Interfaz principal de acceso a datos de géneros.
 * Cuando se integren APIs externas (Spotify Trends, TikTok API,
 * Chart Data), reemplazar los métodos con fetch() y usar
 * GENRE_DB como fallback local.
 */
const GenreDB = {

  // Retorna todos los géneros como array
  all() {
    return Object.values(GENRE_DB);
  },

  // Retorna género por slug
  get(slug) {
    return GENRE_DB[slug] || null;
  },

  // Retorna géneros principales (sin parent)
  roots() {
    return Object.values(GENRE_DB).filter(g => !g.parent);
  },

  // Retorna subgéneros de un género padre
  children(parentSlug) {
    return Object.values(GENRE_DB).filter(g => g.parent === parentSlug);
  },

  // Genera smart tags automáticos desde título
  analyzeTitle(title) {
    const low = title.toLowerCase();
    const keywordMap = {
      // Español urbano
      'calle': 'trap_latino', 'barrio': 'trap_latino', 'pistola': 'trap_latino',
      'perreo': 'reggaeton', 'mami': 'reggaeton', 'baby': 'reggaeton',
      'dembow': 'dembow', 'saoco': 'dembow', 'pachangeo': 'dembow',
      'amor': 'bachata', 'corazon': 'bachata', 'volverte': 'bachata',
      'corrido': 'corridos_tumbados', 'rancho': 'corridos_tumbados',
      'afro': 'afrobeat', 'groove': 'afrobeat', 'riddim': 'dancehall',
      // English
      'drill': 'drill', 'gang': 'drill', 'opps': 'drill',
      'rage': 'rage', 'plug': 'pluggnb', 'dark': 'trap_latino',
      'chill': 'lofi', 'rain': 'lofi', 'study': 'lofi',
      'club': 'jersey_club', 'bounce': 'jersey_club',
      'boom': 'boom_bap', 'bars': 'boom_bap', 'flow': 'boom_bap',
      'house': 'house', 'drop': 'edm', 'festival': 'edm',
      'glitch': 'hyperpop', 'hyper': 'hyperpop',
      'soul': 'r_and_b', 'feelings': 'r_and_b', 'vibe': 'r_and_b',
    };
    for (const [kw, slug] of Object.entries(keywordMap)) {
      if (low.includes(kw)) {
        const genre = GENRE_DB[slug];
        if (genre) return {
          slug,
          genre: genre.name,
          tags: genre.tags.slice(0, 5).join(', '),
          mood: genre.moods.slice(0, 3).join(', '),
        };
      }
    }
    return { slug: 'trap_latino', genre: 'Trap Latino', tags: 'calle, flow, barrio', mood: 'oscuro, melancólico' };
  },

  // Genera recomendaciones de lanzamiento para un género
  releaseGuide(slug) {
    const g = this.get(slug);
    if (!g) return null;
    return {
      bestPlatforms: Object.entries(g.platforms).sort((a,b)=>b[1]-a[1]).map(([p])=>p),
      bestDay: g.release.bestDay,
      bestTime: g.release.bestTime,
      preLaunch: g.release.preLaunch,
      tip: g.release.tip,
      refs: g.refs.slice(0, 3),
      seo: g.seo.slice(0, 5),
    };
  },

  // Genera ideas de contenido para un género y día de semana
  contentIdeas(slug, dayOffset) {
    const g = this.get(slug);
    if (!g) return null;
    return {
      visual: g.visual[dayOffset % g.visual.length],
      caption: g.captions[dayOffset % g.captions.length],
      tags: g.seo.slice(0, 3),
      platforms: Object.entries(g.platforms).sort((a,b)=>b[1]-a[1]).slice(0,2).map(([p])=>p),
    };
  },

  // Lista de todos los géneros para un selector UI
  forSelect() {
    return Object.values(GENRE_DB).map(g => ({
      slug: g.slug,
      name: g.name,
      parent: g.parent,
      bpm: g.bpm,
    })).sort((a,b) => a.name.localeCompare(b.name));
  },

  /* ── PLACEHOLDER PARA APIS FUTURAS ───────────────────────
   *
   * async getTrending(slug) {
   *   try {
   *     const res = await fetch(`https://api.artistvault.app/trends/${slug}`);
   *     return await res.json();
   *   } catch {
   *     return this.get(slug); // fallback local
   *   }
   * }
   *
   * async getSpotifyTags(slug) {
   *   // Conectar con Spotify API para trending tags del género
   * }
   *
   * async getTikTokHashtags(slug) {
   *   // Conectar con TikTok Research API para hashtags en tendencia
   * }
   *
   * async getChartData(slug, region) {
   *   // Conectar con Chart API (Billboard, iTunes) para posiciones
   * }
   * ────────────────────────────────────────────────────── */
};

// Exportar para uso en otros archivos
if (typeof module !== 'undefined') module.exports = { GENRE_DB, GenreDB };

# arcana_data.py

from typing import Dict, Any

# ============================================================
# NUMEN
# ============================================================

NUMEN: Dict[str, Dict[str, Any]] = {
    "IGNIS": {
        "id": "IGNIS",
        "name": "Ignis",
        "display_name": "Ignis (Fuego)",
        "color_hex": "#FF4500",
        "symbol": "TRIANGULO_LLAMA",
        "description": "Fuego, calor, combustión y purificación por llama.",
        "icon_url": "",        
        "tags": ["elemental", "ofensivo", "transformacion"],
    },
    "CRYOBORENS": {
        "id": "CRYOBORENS",
        "name": "Cryoborens",
        "display_name": "Cryoborens (Hielo)",
        "color_hex": "#00CED1",
        "symbol": "TRIANGULO_HIELO",
        "description": "Frío, cristalización, entumecimiento y detención.",
        "icon_url": "",         
        "tags": ["elemental", "control", "prision"],
    },
    "LIMINIS": {
        "id": "LIMINIS",
        "name": "Liminis",
        "display_name": "Liminis (Espacio)",
        "color_hex": "#D4AF37",
        "symbol": "CIRCULO_MUESCA",
        "description": "Espacio, distorsión, portales y tránsito.",
        "icon_url": "", 
        "tags": ["movimiento", "control", "posicion"],
    },
    "VITALIS": {
        "id": "VITALIS",
        "name": "Vitalis",
        "display_name": "Vitalis (Vida)",
        "color_hex": "#32CD32",
        "symbol": "CIRCULO_BROTE",
        "description": "Vida, crecimiento, regeneración y simbiosis.",
        "icon_url": "", 
        "tags": ["sanacion", "soporte"],
    },
    "IGNOTA": {
        "id": "IGNOTA",
        "name": "Ignota",
        "display_name": "Ignota (Secretos)",
        "color_hex": "#E44192",
        "symbol": "CIRCULO_VELOS",
        "description": "Secretos, velos, revelaciones y marcas ocultas.",
        "icon_url": "", 
        "tags": ["sigilo", "informacion", "control"],
    },
    "TELLURIS": {
        "id": "TELLURIS",
        "name": "Telluris",
        "display_name": "Telluris (Tierra)",
        "color_hex": "#813600",
        "symbol": "TRAPECIO_COLUMNA",
        "description": "Roca, suelo, estructura y estabilidad.",
        "icon_url": "", 
        "tags": ["defensa", "arquitectura", "elemental"],
    },
    "METALLUM": {
        "id": "METALLUM",
        "name": "Metallum",
        "display_name": "Metallum (Metal)",
        "color_hex": "#0047AB",
        "symbol": "PLACA_HEXAGONAL",
        "description": "Metal, forja, armaduras y armas.",
        "icon_url": "", 
        "tags": ["defensa", "ofensivo", "arma"],
    },
    "ASTRALIS": {
        "id": "ASTRALIS",
        "name": "Astralis",
        "display_name": "Astralis (Estrellas)",
        "color_hex": "#FCDA90",
        "symbol": "HALO_CRUZ",
        "description": "Luz estelar, orientación, presagios y guías.",
        "icon_url": "", 
        "tags": ["luz", "soporte", "adivinacion"],
    },
    "HIERATIA": {
        "id": "HIERATIA",
        "name": "Hieratia",
        "display_name": "Hieratia (Celestial)",
        "color_hex": "#6CA6FF",
        "symbol": "CIRCULO_NIMBUS",
        "description": "Esfera celestial, sacralidad, juramentos y protección.",
        "icon_url": "", 
        "tags": ["proteccion", "juramento", "sacro"],
    },
    "UMBRA": {
        "id": "UMBRA",
        "name": "Umbra",
        "display_name": "Umbra (Sombras)",
        "color_hex": "#2F2F2F",
        "symbol": "CRECIENTE_CHEVRON",
        "description": "Sombras, ocultación, perfiles, penumbra.",
        "icon_url": "", 
        "tags": ["sigilo", "debilitacion"],
    },
    "CHRONENS": {
        "id": "CHRONENS",
        "name": "Chronens",
        "display_name": "Chronens (Tiempo)",
        "color_hex": "#C0C0C0",
        "symbol": "CIRCULO_ROTO_AGUJA",
        "description": "Tiempo, ritmo, aceleración y suspensión.",
        "icon_url": "", 
        "tags": ["control", "tempo"],
    },
    "LIKA": {
        "id": "LIKA",
        "name": "Lika",
        "display_name": "Lika (Vínculos)",
        "color_hex": "#FFFFFF",
        "symbol": "DOBLE_OVALO_PUENTE",
        "description": "Lazos, pactos, contratos y redes.",
        "icon_url": "", 
        "tags": ["juramento", "control", "soporte"],
    },
    "MITAUNA": {
        "id": "MITAUNA",
        "name": "Mitauna",
        "display_name": "Miṭā'uṇā (Furia)",
        "color_hex": "#FF0000",
        "symbol": "ROMBO_IMPACTO",
        "description": "Fuerza bruta, choque, impacto y rabia.",
        "icon_url": "", 
        "tags": ["ofensivo", "fisico"],
    },
    "AHMAR": {
        "id": "AHMAR",
        "name": "Ahmar",
        "display_name": "Ahmar (Sangre)",
        "color_hex": "#B22222",
        "symbol": "GOTA_BARRA",
        "description": "Sangre, sacrificio, linaje y pactos vitales.",
        "icon_url": "", 
        "tags": ["coste", "vital", "sacrificio"],
    },
    "AETHERIS": {
        "id": "AETHERIS",
        "name": "Aetheris",
        "display_name": "Aetheris (Aire)",
        "color_hex": "#68D6B0",
        "symbol": "ONDAS_ASCENDENTES",
        "description": "Viento, corrientes, flotación y desplazamiento.",
        "icon_url": "", 
        "tags": ["movimiento", "control"],
    },
    "RAIZENS": {
        "id": "RAIZENS",
        "name": "Raizens",
        "display_name": "Raizens (Relámpago)",
        "color_hex": "#FFD700",
        "symbol": "CIRCULO_RAYO",
        "description": "Relámpagos, descarga súbita, impulso y sobrecarga.",
        "icon_url": "", 
        "tags": ["ofensivo", "impacto", "rapido"],
    },
    "AVAZAX": {
        "id": "AVAZAX",
        "name": "Avazax",
        "display_name": "Āvāzax (Sonido)",
        "color_hex": "#A47DFF",
        "symbol": "DIAFRAGMA_ONDAS",
        "description": "Sonido, vibración, resonancia y eco.",
        "icon_url": "", 
        "tags": ["control", "area", "sensorial"],
    },
    "MORTIS": {
        "id": "MORTIS",
        "name": "Mortis",
        "display_name": "Mortis (Muerte)",
        "color_hex": "#00FF80",
        "symbol": "CIRCULO_SEGMENTADO",
        "description": "Transición, final, reposo y quiebre.",
        "icon_url": "", 
        "tags": ["necro", "control", "transicion"],
    },
    "ONIRIANS": {
        "id": "ONIRIANS",
        "name": "Onirians",
        "display_name": "Onirians (Sueños)",
        "color_hex": "#5D67C0",
        "symbol": "CRECIENTE_ESPIRAL",
        "description": "Sueños, ilusión, desvío de la atención.",
        "icon_url": "", 
        "tags": ["ilusion", "control_mental"],
    },
    "NATURAE": {
        "id": "NATURAE",
        "name": "Naturae",
        "display_name": "Naturae (Naturaleza)",
        "color_hex": "#ACAF04",
        "symbol": "CIRCULO_RAMIFICACION",
        "description": "Ciclos naturales, flora, fauna y simbiosis.",
        "icon_url": "", 
        "tags": ["naturaleza", "soporte"],
    },
    "PSYKONENS": {
        "id": "PSYKONENS",
        "name": "Psykonens",
        "display_name": "Psykonens (Mente)",
        "color_hex": "#7801FF",
        "symbol": "OJO_ESPIRAL",
        "description": "Mente, emociones, dominación psíquica.",
        "icon_url": "", 
        "tags": ["control_mental", "comunicacion"],
    },
}

# ============================================================
# PRECEPTOS BASE (30)
# ============================================================

PRECEPTS: Dict[str, Dict[str, Any]] = {
    # ---------- Elementales ----------
    "ENCENDER": {
        "id": "ENCENDER",
        "verb": "Encender",
        "category": "Elemental",
        "preferred_numen_ids": ["IGNIS"],
        "description": "Inicia combustión o genera una pequeña llama.",
        "example_ordinances": ["Chispa Ígnea", "Llama Voraz", "Pira de Castigo"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "ENFRIAR": {
        "id": "ENFRIAR",
        "verb": "Enfriar",
        "category": "Elemental",
        "preferred_numen_ids": ["CRYOBORENS"],
        "description": "Reduce la temperatura, congela o entumece.",
        "example_ordinances": ["Toque Helado", "Crisálida Helada"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "MOVER": {
        "id": "MOVER",
        "verb": "Mover",
        "category": "Elemental",
        "preferred_numen_ids": ["LIMINIS"],
        "description": "Desplaza objetos, fuerzas o efectos en el espacio.",
        "example_ordinances": ["Empuje Espacial", "Puerta del Errante", "Soplo del Horizonte"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "ALTERAR_TIEMPO": {
        "id": "ALTERAR_TIEMPO",
        "verb": "Alterar",
        "category": "Elemental",
        "preferred_numen_ids": ["CHRONENS"],
        "description": "Distorsiona la percepción o el flujo del tiempo.",
        "example_ordinances": ["Distorsión Temporal", "Aguja del Tiempo"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "ILUMINAR": {
        "id": "ILUMINAR",
        "verb": "Iluminar",
        "category": "Elemental",
        "preferred_numen_ids": ["ASTRALIS", "HIERATIA"],
        "description": "Genera luz, guía o revela siluetas.",
        "example_ordinances": ["Luz Estelar", "Luz del Pastor"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "OSCURECER": {
        "id": "OSCURECER",
        "verb": "Oscurecer",
        "category": "Elemental",
        "preferred_numen_ids": ["UMBRA"],
        "description": "Apaga luces, espesa sombras, reduce visibilidad.",
        "example_ordinances": ["Velo de Sombras", "Manto de Sombras"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "ESCULPIR": {
        "id": "ESCULPIR",
        "verb": "Esculpir",
        "category": "Elemental",
        "preferred_numen_ids": ["TELLURIS", "METALLUM"],
        "description": "Da forma a piedra o metal en bruto.",
        "example_ordinances": ["Molde de Piedra", "Bastión Inquebrantable"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "ATRAVESAR": {
        "id": "ATRAVESAR",
        "verb": "Atravesar",
        "category": "Elemental",
        "preferred_numen_ids": ["LIMINIS"],
        "description": "Permite cruzar barreras, umbrales o distancias.",
        "example_ordinances": ["Salto Inmediato", "Puerta del Errante"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "INVOCAR": {
        "id": "INVOCAR",
        "verb": "Invocar",
        "category": "Elemental",
        "preferred_numen_ids": ["HIERATIA", "MORTIS"],
        "description": "Llama presencias, entidades o ecos numénicos.",
        "example_ordinances": ["Aparición Espectral", "Semilla del Nuevo Sol"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "APLASTAR": {
        "id": "APLASTAR",
        "verb": "Aplastar",
        "category": "Elemental",
        "preferred_numen_ids": ["MITAUNA"],
        "description": "Canaliza fuerza bruta en golpes demoledores.",
        "example_ordinances": ["Golpe Demoledor", "Garra de la Montaña"],
        "base_power": 1,
        "base_complexity": 1,
    },

    # ---------- Vitales ----------
    "CURAR": {
        "id": "CURAR",
        "verb": "Curar",
        "category": "Vital",
        "preferred_numen_ids": ["VITALIS"],
        "description": "Restaura tejido, estabiliza heridas o elimina toxinas.",
        "example_ordinances": ["Toque Sanador", "Pulso Regenerante", "Halo Sanador"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "VINCULAR": {
        "id": "VINCULAR",
        "verb": "Vincular",
        "category": "Vital",
        "preferred_numen_ids": ["LIKA"],
        "description": "Crea lazos entre seres, objetos o lugares.",
        "example_ordinances": ["Lazo Eterno", "Pacto Carmesí"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "PURIFICAR": {
        "id": "PURIFICAR",
        "verb": "Purificar",
        "category": "Vital",
        "preferred_numen_ids": ["IGNIS", "HIERATIA"],
        "description": "Quema o disuelve corrupción, enfermedades y maldiciones.",
        "example_ordinances": ["Llama Purgadora"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "EXTRAER": {
        "id": "EXTRAER",
        "verb": "Extraer",
        "category": "Vital",
        "preferred_numen_ids": ["AHMAR"],
        "description": "Obtiene sangre, esencia o recursos vitales de un objetivo.",
        "example_ordinances": ["Sangre Vinculada"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "REVIVIR": {
        "id": "REVIVIR",
        "verb": "Revivir",
        "category": "Vital",
        "preferred_numen_ids": ["VITALIS", "MORTIS"],
        "description": "Reconecta cuerpo y alma, devuelve o retiene la vida.",
        "example_ordinances": ["Susurro de los Muertos"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "ABSORBER": {
        "id": "ABSORBER",
        "verb": "Absorber",
        "category": "Vital",
        "preferred_numen_ids": ["IGNOTA", "VITALIS"],
        "description": "Drena energía, numen o vitalidad de una fuente.",
        "example_ordinances": ["Drenaje Vital"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "FORTALECER": {
        "id": "FORTALECER",
        "verb": "Fortalecer",
        "category": "Vital",
        "preferred_numen_ids": ["VITALIS", "AHMAR"],
        "description": "Mejora temporalmente la resistencia o la fuerza.",
        "example_ordinances": ["Potencia Carmesí"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "PROTEGER": {
        "id": "PROTEGER",
        "verb": "Proteger",
        "category": "Vital",
        "preferred_numen_ids": ["HIERATIA", "LIMINIS"],
        "description": "Erige defensas, redirige golpes o blinda el destino.",
        "example_ordinances": ["Escudo Celestial", "Luz del Pastor"],
        "base_power": 1,
        "base_complexity": 1,
    },

    # ---------- Cognitivas / Sensoriales ----------
    "REVELAR": {
        "id": "REVELAR",
        "verb": "Revelar",
        "category": "Cognitiva",
        "preferred_numen_ids": ["IGNOTA"],
        "description": "Hace visibles secretos, trampas u objetos ocultos.",
        "example_ordinances": ["Ojo Oculto", "Verdad Velada", "Faro del Misterio"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "PERCIBIR": {
        "id": "PERCIBIR",
        "verb": "Percibir",
        "category": "Cognitiva",
        "preferred_numen_ids": ["ASTRALIS", "PSYKONENS"],
        "description": "Amplifica sentidos físicos o psíquicos.",
        "example_ordinances": ["Vínculo Telepático"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "ILUSIONAR": {
        "id": "ILUSIONAR",
        "verb": "Ilusionar",
        "category": "Cognitiva",
        "preferred_numen_ids": ["ONIRIANS", "UMBRA"],
        "description": "Crea apariencias, escenas oníricas o falsos estímulos.",
        "example_ordinances": ["Sendero de Sueños"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "ALTERAR_MENTE": {
        "id": "ALTERAR_MENTE",
        "verb": "Alterar (Mente)",
        "category": "Cognitiva",
        "preferred_numen_ids": ["PSYKONENS"],
        "description": "Cambia emociones, recuerdos o voluntad.",
        "example_ordinances": ["Dominio Mental"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "ESCUCHAR": {
        "id": "ESCUCHAR",
        "verb": "Escuchar",
        "category": "Cognitiva",
        "preferred_numen_ids": ["AVAZAX"],
        "description": "Amplifica sonidos, ecos o resonancias.",
        "example_ordinances": ["Eco Resonante", "Tormenta Resonante"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "CALLAR": {
        "id": "CALLAR",
        "verb": "Callar",
        "category": "Cognitiva",
        "preferred_numen_ids": ["AVAZAX", "UMBRA"],
        "description": "Suprime sonido, voz o transmisión de información.",
        "example_ordinances": ["Silencio Atronador", "Niebla del Silencio"],
        "base_power": 1,
        "base_complexity": 1,
    },

    # ---------- Constructivas / Pragmáticas ----------
    "TEJER": {
        "id": "TEJER",
        "verb": "Tejer",
        "category": "Pragmática",
        "preferred_numen_ids": ["LIKA", "METALLUM"],
        "description": "Entreteje materia, vínculos o patrones.",
        "example_ordinances": ["Armadura de Hierro"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "FORJAR": {
        "id": "FORJAR",
        "verb": "Forjar",
        "category": "Pragmática",
        "preferred_numen_ids": ["METALLUM", "TELLURIS"],
        "description": "Da forma final y propósito a un objeto o efecto.",
        "example_ordinances": ["Martillo Arcano", "Forja Viva"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "MOLDEAR": {
        "id": "MOLDEAR",
        "verb": "Moldear",
        "category": "Pragmática",
        "preferred_numen_ids": ["TELLURIS", "VITALIS"],
        "description": "Reconfigura estructuras físicas u orgánicas.",
        "example_ordinances": ["Raíces Vivas", "Raíz del Alba"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "DESATAR": {
        "id": "DESATAR",
        "verb": "Desatar",
        "category": "Pragmática",
        "preferred_numen_ids": ["MITAUNA", "RAIZENS"],
        "description": "Libera energía contenida en una explosión o choque.",
        "example_ordinances": ["Tormenta Relampagueante", "Rayo del Juicio"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "SELLAR": {
        "id": "SELLAR",
        "verb": "Sellar",
        "category": "Pragmática",
        "preferred_numen_ids": ["CRYOBORENS", "LIMINIS"],
        "description": "Clausura, bloquea o fija algo en un estado.",
        "example_ordinances": ["Prisión de Hielo", "Círculo del Ocaso", "Crisálida Helada"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "MARCAR": {
        "id": "MARCAR",
        "verb": "Marcar",
        "category": "Pragmática",
        "preferred_numen_ids": ["IGNOTA", "LIKA"],
        "description": "Imprime un sello o condición que se activará después.",
        "example_ordinances": ["Sello de Juramento"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "CORTAR": {
        "id": "CORTAR",
        "verb": "Cortar",
        "category": "Pragmática",
        "preferred_numen": ["CRYOB", "IGNIS", "LIMINIS", "METALLUM", "RAIZENS"],
        "description": "Produce un tajo físico o energético capaz de seccionar materia o energía.",
        "base_power": 1,
        "base_complexity": 1,    
    },
}


# ============================================================
# MODOS DE PRECEPTO (para sugerencias mecánicas)
# ============================================================

# mode:
# - "damage"  → principal uso como daño
# - "heal"    → principal uso como curación / buff
# - "control" → control, estados, movimiento forzado
# - "utility" → info, creación, soporte sin números directos
# - "mixed"   → según INTENCIÓN: ofensivo = daño, defensivo = curación

DICE_BY_MODE = {
    "heal": 4,
    "mixed": 6,
    "damage": 10,
    "utility": 6,
}


def get_base_die_for_precept(precept_id: str, effect_type: str | None = None) -> int:
    """
    Devuelve el tamaño del dado base (4, 6, 10, etc.) según el modo del precepto.
    - mode='heal'   → d4
    - mode='mixed'  → d6
    - mode='damage' → d10
    - mode='utility' → d6 si acaba siendo ofensivo/curativo

    effect_type está por si en el futuro quieres diferenciar dentro de 'mixed'
    (p.ej. mixed+heal = d4), pero por ahora no lo usamos.
    """
    pre = PRECEPTS.get(precept_id, {})
    mode = pre.get("mode", "utility")

    # Si algún día quieres algo como:
    # if mode == "mixed" and effect_type == "heal": ...
    # lo tendrías aquí.

    return DICE_BY_MODE.get(mode, 6)



_PRECEPT_MODES = {
    # Elementales
    "ENCENDER": "mixed",
    "ENFRIAR": "mixed",
    "MOVER": "control",
    "ALTERAR_TIEMPO": "control",
    "ILUMINAR": "utility",
    "OSCURECER": "control",
    "ESCULPIR": "utility",
    "ATRAVESAR": "utility",
    "INVOCAR": "utility",
    "APLASTAR": "damage",

    # Vitales
    "CURAR": "heal",
    "VINCULAR": "control",
    "PURIFICAR": "mixed",
    "EXTRAER": "mixed",
    "REVIVIR": "heal",
    "ABSORBER": "mixed",
    "FORTALECER": "heal",
    "PROTEGER": "heal",

    # Cognitivas / sensoriales
    "REVELAR": "utility",
    "PERCIBIR": "utility",
    "ILUSIONAR": "control",
    "ALTERAR_MENTE": "control",
    "ESCUCHAR": "utility",
    "CALLAR": "control",

    # Constructivas / pragmáticas
    "TEJER": "utility",
    "FORJAR": "utility",
    "MOLDEAR": "mixed",
    "DESATAR": "damage",
    "SELLAR": "control",
    "MARCAR": "control",
    "CORTAR": "mixed",    
}

# Inyectamos el modo dentro de cada precepto para facilitar el acceso
for pid, mode in _PRECEPT_MODES.items():
    if pid in PRECEPTS:
        PRECEPTS[pid]["mode"] = mode
    else:
        # Por si falta alguno, no rompemos el import
        pass





# ============================================================
# MODIFICADORES / PARTÍCULAS
# ============================================================

MODIFIERS: Dict[str, Dict[str, Any]] = {
    # ---------- FORMA ----------
    "FORMA_LINEA": {
        "id": "FORMA_LINEA",
        "family": "FORMA",
        "name": "Línea",
        "description": "Convierte el efecto en un rayo o línea recta.",
        "base_cost": 2,
        "max_rank": 1,
        "tags": ["area", "rayo"],
    },
    "FORMA_CONO": {
        "id": "FORMA_CONO",
        "family": "FORMA",
        "name": "Cono",
        "description": "Extiende el efecto en abanico desde el regidor.",
        "base_cost": 2,
        "max_rank": 3,
        "tags": ["area"],
    },
    "FORMA_ESFERA": {
        "id": "FORMA_ESFERA",
        "family": "FORMA",
        "name": "Esfera",
        "description": "Área centrada en un punto.",
        "base_cost": 2,
        "max_rank": 3,
        "tags": ["area"],
    },
    "FORMA_MURO": {
        "id": "FORMA_MURO",
        "family": "FORMA",
        "name": "Muro",
        "description": "Superficie defensiva u ofensiva.",
        "base_cost": 2,
        "max_rank": 2,
        "tags": ["defensa", "control"],
    },
    "FORMA_AURA": {
        "id": "FORMA_AURA",
        "family": "FORMA",
        "name": "Aura",
        "description": "Área centrada en el regidor.",
        "base_cost": 2,
        "max_rank": 2,
        "tags": ["area", "self"],
    },

    # ---------- ALCANCE / DURACIÓN ----------
    "DURACION_INSTANTANEO": {
        "id": "DURACION_INSTANTANEO",
        "family": "ALCANCE_DURACION",
        "name": "Instantáneo",
        "description": "Efecto breve, un único destello o acción.",
        "base_cost": 0,
        "tags": ["rapido"],
    },
    "DURACION_PERSISTENTE": {
        "id": "DURACION_PERSISTENTE",
        "family": "ALCANCE_DURACION",
        "name": "Persistente",
        "description": "La ordenanza permanece activa más allá del instante inicial.",
        "base_cost": 1,
        "rank_cost": 1,      # cada rango extra aumenta complejidad
        "max_rank": 4,       # por ejemplo: 1=rondas, 2=minutos, 3=horas, 4=días+
        "tags": ["duracion"],
    },

    "ALCANCE_EXTENDIDO": {
        "id": "ALCANCE_EXTENDIDO",
        "family": "ALCANCE_DURACION",
        "name": "Extendido",
        "description": "Mayor alcance o radio efectivo. Cada rango aumenta el tamaño del área.",
        "base_cost": 1,
        "rank_cost": 1,      # +1 complejidad por rango adicional
        "max_rank": 3,       # puedes subirlo si quieres magias XXL
        "tags": ["rango"],
    },

    "ALCANCE_PROYECTADO": {
        "id": "ALCANCE_PROYECTADO",
        "family": "ALCANCE_DURACION",
        "name": "Proyectado",
        "description": "Ancla el efecto en un punto remoto o visible.",
        "base_cost": 2,
        "tags": ["rango", "control"],
    },

    # ---------- INTENCIÓN ----------
    "INTENCION_OFENSIVO": {
        "id": "INTENCION_OFENSIVO",
        "family": "INTENCION",
        "name": "Ofensivo",
        "description": "Daño, presión o control hostil.",
        "base_cost": 1,
        "tags": ["daño"],
    },
    "INTENCION_DEFENSIVO": {
        "id": "INTENCION_DEFENSIVO",
        "family": "INTENCION",
        "name": "Defensivo",
        "description": "Protección, escudo, mitigación o disipación.",
        "base_cost": 1,
        "tags": ["defensa"],
    },
    "INTENCION_CONDICIONAL": {
        "id": "INTENCION_CONDICIONAL",
        "family": "INTENCION",
        "name": "Condicional",
        "description": "Se dispara solo bajo ciertas circunstancias.",
        "base_cost": 1,
        "tags": ["condicional"],
    },

    # ---------- INTENSIDAD / EFICIENCIA ----------
    "INTENSIDAD_POTENCIADO": {
        "id": "INTENSIDAD_POTENCIADO",
        "family": "INTENSIDAD",
        "name": "Potenciado",
        "description": "Aumenta la magnitud del efecto.",
        "base_cost": 0,
        "rank_cost": 1,  # +1 coste por cada rango
        "max_rank": 3,
        "tags": ["fuerte"],
    },
    "INTENSIDAD_REDUCIDO": {
        "id": "INTENSIDAD_REDUCIDO",
        "family": "INTENSIDAD",
        "name": "Reducido",
        "description": "Minimiza el efecto para reducir riesgos o consumo.",
        "base_cost": 0,
        "cost_modifier_total": -1,  # reduce complejidad total en 1 (mínimo 1)
        "tags": ["sutil", "eficiente"],
    },
    "INTENSIDAD_MULTIPLICADO": {
        "id": "INTENSIDAD_MULTIPLICADO",
        "family": "INTENSIDAD",
        "name": "Multiplicado",
        "description": "Divide el efecto en varias instancias más débiles.",
        "base_cost": 0,
        "per_extra_instance_cost": 1,
        "tags": ["dividido"],
    },
    "INTENSIDAD_EFICIENCIA": {
        "id": "INTENSIDAD_EFICIENCIA",
        "family": "INTENSIDAD",
        "name": "Eficiencia",
        "description": "Optimiza el flujo: reduce coste total sacrificando potencia bruta.",
        "base_cost": 0,
        "cost_modifier_total": -1,
        "tags": ["eficiente"],
    },

    # ---------- CONDICIÓN / FILTROS ----------
    "COND_ALIADOS": {
        "id": "COND_ALIADOS",
        "family": "CONDICION",
        "name": "Solo aliados",
        "description": "El efecto solo afecta a aliados elegidos.",
        "base_cost": 1,
        "tags": ["filtro", "aliados"],
    },
    "COND_ENEMIGOS": {
        "id": "COND_ENEMIGOS",
        "family": "CONDICION",
        "name": "Solo enemigos",
        "description": "El efecto solo afecta a objetivos marcados como enemigos.",
        "base_cost": 1,
        "tags": ["filtro", "enemigos"],
    },
    "COND_DISPARADOR": {
        "id": "COND_DISPARADOR",
        "family": "CONDICION",
        "name": "Disparador",
        "description": "Se activa cuando se cumple una condición (palabra clave, gesto, evento).",
        "base_cost": 1,
        "tags": ["trampa", "preparado"],
    },
}

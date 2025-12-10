# arcana_data.py

from typing import Dict, List, Any

# ---------- Numen definitions ----------

NUMEN: Dict[str, Dict[str, Any]] = {
    "IGNIS": {
        "id": "IGNIS",
        "name": "Ignis",
        "display_name": "Ignis (Fuego)",
        "color_hex": "#FF4500",
        "symbol": "TRIANGULO_LLAMA",
        "description": "Numen del fuego, calor y combustión.",
        "tags": ["elemental", "ofensivo", "transformación"],
    },
    "LIMINIS": {
        "id": "LIMINIS",
        "name": "Liminis",
        "display_name": "Liminis (Espacio)",
        "color_hex": "#D4AF37",
        "symbol": "CIRCULO_MUESCA",
        "description": "Numen de espacio, desplazamiento y tránsito.",
        "tags": ["movimiento", "control"],
    },
    "VITALIS": {
        "id": "VITALIS",
        "name": "Vitalis",
        "display_name": "Vitalis (Vida)",
        "color_hex": "#32CD32",
        "symbol": "CIRCULO_BROTE",
        "description": "Numen de vida, crecimiento y restauración.",
        "tags": ["sanacion", "soporte"],
    },
    "IGNOTA": {
        "id": "IGNOTA",
        "name": "Ignota",
        "display_name": "Ignota (Secretos)",
        "color_hex": "#E44192",
        "symbol": "CIRCULO_VELOS",
        "description": "Numen de secretos, velos y revelaciones.",
        "tags": ["sigilo", "informacion"],
    },
    # ... añade el resto de Numen aquí ...
}

# ---------- Precepts (Preceptos base) ----------

PRECEPTS: Dict[str, Dict[str, Any]] = {
    "ENCENDER": {
        "id": "ENCENDER",
        "verb": "Encender",
        "category": "Elemental",
        "preferred_numen_ids": ["IGNIS"],
        "description": "Inicia combustión o genera una pequeña llama.",
        "example_ordinances": ["Chispa Ígnea", "Llama Voraz"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "MOVER": {
        "id": "MOVER",
        "verb": "Mover",
        "category": "Elemental",
        "preferred_numen_ids": ["LIMINIS"],
        "description": "Empuja o desplaza objetos o efectos.",
        "example_ordinances": ["Empuje Espacial", "Vórtice Espacial"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "CURAR": {
        "id": "CURAR",
        "verb": "Curar",
        "category": "Vital",
        "preferred_numen_ids": ["VITALIS"],
        "description": "Restaura tejido dañado o estabiliza heridas.",
        "example_ordinances": ["Toque Sanador", "Halo Sanador"],
        "base_power": 1,
        "base_complexity": 1,
    },
    "REVELAR": {
        "id": "REVELAR",
        "verb": "Revelar",
        "category": "Cognitiva",
        "preferred_numen_ids": ["IGNOTA"],
        "description": "Hace visibles cosas ocultas, veladas o invisibles.",
        "example_ordinances": ["Ojo Oculto", "Faro del Misterio"],
        "base_power": 1,
        "base_complexity": 1,
    },
    # ... añade el resto de los 30 preceptos ...
}

# ---------- Modifiers / Partículas ----------

# Families: FORMA, ALCANCE_DURACION, INTENCION, INTENSIDAD, CONDICION

MODIFIERS: Dict[str, Dict[str, Any]] = {
    # ---- Forma ----
    "FORMA_LINEA": {
        "id": "FORMA_LINEA",
        "family": "FORMA",
        "name": "Línea",
        "description": "Convierte el efecto en un rayo o línea recta.",
        "base_cost": 2,          # Forma mayor = 2
        "max_rank": 1,
        "tags": ["area", "rayo"],
    },
    "FORMA_CONO": {
        "id": "FORMA_CONO",
        "family": "FORMA",
        "name": "Cono",
        "description": "Extiende el efecto en abanico desde el regidor.",
        "base_cost": 2,
        "max_rank": 3,           # Cono I-III si quieres
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
        "description": "Superficie defensiva o de bloqueo.",
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

    # ---- Alcance / Duración ----
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
        "description": "Dura varios turnos/minutos.",
        "base_cost": 1,
        "extra_long_duration_cost": 1,  # si decides marcar duraciones largas
        "tags": ["concentracion"],
    },
    "ALCANCE_EXTENDIDO": {
        "id": "ALCANCE_EXTENDIDO",
        "family": "ALCANCE_DURACION",
        "name": "Extendido",
        "description": "Mayor alcance o radio.",
        "base_cost": 1,
        "tags": ["rango"],
    },
    "ALCANCE_PROYECTADO": {
        "id": "ALCANCE_PROYECTADO",
        "family": "ALCANCE_DURACION",
        "name": "Proyectado",
        "description": "Ancla el efecto a un punto remoto.",
        "base_cost": 2,
        "tags": ["rango", "control"],
    },

    # ---- Intención ----
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
        "description": "Protección, escudo o disipación.",
        "base_cost": 1,
        "tags": ["defensa"],
    },
    "INTENCION_CONDICIONAL": {
        "id": "INTENCION_CONDICIONAL",
        "family": "INTENCION",
        "name": "Condicional",
        "description": "Solo se activa bajo ciertas condiciones.",
        "base_cost": 1,
        "tags": ["condicional"],
    },

    # ---- Intensidad / Eficiencia ----
    "INTENSIDAD_POTENCIADO": {
        "id": "INTENSIDAD_POTENCIADO",
        "family": "INTENSIDAD",
        "name": "Potenciado",
        "description": "Aumenta la magnitud del efecto.",
        "base_cost": 0,
        "rank_cost": 1,      # +1 coste por cada grado
        "max_rank": 3,
        "tags": ["fuerte"],
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
        "description": "Reduce el coste total consumiendo un slot de intensidad.",
        "base_cost": 0,
        "cost_modifier_total": -1,   # se aplicará al final (mínimo 1)
        "tags": ["eficiente"],
    },

    # Aquí podrías añadir explícitos de CONDICION (trigger, filtro aliados/enemigos, etc.)
}

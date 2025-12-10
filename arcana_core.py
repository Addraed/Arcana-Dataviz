# arcana_core.py

from __future__ import annotations
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from arcana_data import NUMEN, PRECEPTS, MODIFIERS
import math
import json
import os

# --------- Data classes ----------

@dataclass
class ModifierSelection:
    """A chosen modifier with optional rank / extra instances."""
    modifier_id: str
    rank: int = 1                # for things like Potenciado I-III
    extra_instances: int = 0     # for Multiplicado (N-1)


@dataclass
class Ordinance:
    id: str
    canonical_key: str
    name: str
    precept_id: str
    numen_ids: List[str]
    modifiers: List[ModifierSelection]
    mechanical: Dict[str, Any]
    cost: Dict[str, Any]
    tier: int
    meta: Dict[str, Any]


# ---------- Canonical key ----------

def build_canonical_key(
    precept_id: str,
    numen_ids: List[str],
    modifiers: List[ModifierSelection],
) -> str:
    """
    Precept | NUMEN1+NUMEN2 | [MOD1:rank, MOD2:rank, ...]
    Sorted for stability.
    """
    sorted_numen = sorted(numen_ids)
    numen_part = "+".join(sorted_numen)

    # encode modifiers with rank and extra_instances
    modifier_parts = []
    for m in sorted(modifiers, key=lambda x: x.modifier_id):
        part = m.modifier_id
        if m.rank != 1:
            part += f":r{m.rank}"
        if m.extra_instances > 0:
            part += f":x{m.extra_instances}"
        modifier_parts.append(part)

    modifier_str = ",".join(modifier_parts)
    return f"{precept_id}|{numen_part}|[{modifier_str}]"


# ---------- Complexity & Tier ----------

def calculate_complexity(
    precept_id: str,
    numen_ids: List[str],
    modifiers: List[ModifierSelection],
    long_duration: bool = False,
) -> int:
    """
    Implementa tu modelo de coste:
    - Base (Precepto + Numen) = 1 punto
    - Cada modificador normal = +1
    - Formas mayores = +2
    - Persistente puede añadir +1 extra si long_duration = True
    - Potenciado: +1 por rango
    - Multiplicado: +1 por extra_instances
    - Eficiencia: -1 al total (mínimo 1)
    """
    if precept_id not in PRECEPTS:
        raise ValueError(f"Precepto desconocido: {precept_id}")

    base_cost = PRECEPTS[precept_id].get("base_complexity", 1)

    # Precepto + Numen = 1 → ya está representado como base_cost=1
    total = base_cost

    has_eficiencia = False

    for sel in modifiers:
        mod = MODIFIERS[sel.modifier_id]
        family = mod["family"]
        base_mod_cost = mod.get("base_cost", 1)

        # Forma mayor = +2, pero ya hemos puesto base_cost=2 en los datos
        total += base_mod_cost

        # Casos especiales según familia / id
        if sel.modifier_id == "DURACION_PERSISTENTE" and long_duration:
            total += mod.get("extra_long_duration_cost", 1)

        if sel.modifier_id == "INTENSIDAD_POTENCIADO":
            # +1 por cada rango (I/II/III)
            rank = max(1, sel.rank)
            total += mod.get("rank_cost", 1) * rank

        if sel.modifier_id == "INTENSIDAD_MULTIPLICADO":
            # +1 por cada instancia extra
            total += mod.get("per_extra_instance_cost", 1) * sel.extra_instances

        if sel.modifier_id == "INTENSIDAD_EFICIENCIA":
            has_eficiencia = True

    if has_eficiencia:
        total += MODIFIERS["INTENSIDAD_EFICIENCIA"].get("cost_modifier_total", -1)

    # mínimo 1
    if total < 1:
        total = 1

    return total


def derive_tier(complexity: int) -> int:
    """
    Mapea complejidad a Tier sugerido.
    Puedes ajustar los rangos a tu gusto.
    """
    if complexity <= 2:
        return 1  # Aprendiz
    elif complexity <= 5:
        return 2  # Adeptus
    elif complexity <= 8:
        return 3  # Maestro
    else:
        return 4  # Archirregidor


# ============================================================
# EXTRACCIÓN DE INFO DE MODIFICADORES
# ============================================================

def get_intent_from_modifiers(modifiers: list[ModifierSelection]) -> str:
    """
    Devuelve 'OFFENSIVE', 'DEFENSIVE', 'CONDITIONAL' o 'NEUTRAL'
    según los modificadores de INTENCION presentes.
    """
    ids = {m.modifier_id for m in modifiers}
    if "INTENCION_OFENSIVO" in ids:
        return "OFFENSIVE"
    if "INTENCION_DEFENSIVO" in ids:
        return "DEFENSIVE"
    if "INTENCION_CONDICIONAL" in ids:
        return "CONDITIONAL"
    return "NEUTRAL"


def extract_modifier_info(modifiers: list[ModifierSelection]) -> dict:
    """
    Analiza los modificadores y devuelve info agregada útil para las sugerencias:
    - forma (linea, cono, esfera, muro, aura, None)
    - has_persistente
    - extendido_rank
    - has_proyectado
    - potenciado_rank
    - multiplicado_instances (>=1)
    """
    info = {
        "shape": None,              # 'LINE', 'CONE', 'SPHERE', 'WALL', 'AURA'
        "has_persistente": False,
        "extendido_rank": 0,        # 0 = normal, 1+ = más tamaño/alcance
        "has_proyectado": False,
        "potenciado_rank": 0,
        "has_reducido": False,
        "multiplicado_instances": 1,
    }

    # Formas: cogemos la primera que aparezca
    for sel in modifiers:
        mid = sel.modifier_id

        # Formas (cogemos la primera que aparezca)
        if mid == "FORMA_LINEA" and info["shape"] is None:
            info["shape"] = "LINE"
        elif mid == "FORMA_CONO" and info["shape"] is None:
            info["shape"] = "CONE"
        elif mid == "FORMA_ESFERA" and info["shape"] is None:
            info["shape"] = "SPHERE"
        elif mid == "FORMA_MURO" and info["shape"] is None:
            info["shape"] = "WALL"
        elif mid == "FORMA_AURA" and info["shape"] is None:
            info["shape"] = "AURA"

        # Duración / alcance
        if mid == "DURACION_PERSISTENTE":
            info["has_persistente"] = True
        if mid == "ALCANCE_EXTENDIDO":
            # Si no tocas el slider, rank vendrá como 1 por defecto
            rank = sel.rank if sel.rank and sel.rank > 0 else 1
            info["extendido_rank"] = max(info["extendido_rank"], rank)
        if mid == "ALCANCE_PROYECTADO":
            info["has_proyectado"] = True

        # Intensidad
        if mid == "INTENSIDAD_POTENCIADO":
            info["potenciado_rank"] = max(info["potenciado_rank"], sel.rank)
        if mid == "INTENSIDAD_REDUCIDO":
            info["has_reducido"] = True
        if mid == "INTENSIDAD_MULTIPLICADO":
            # SOLO instancias, nunca rango
            info["multiplicado_instances"] = 1 + max(0, sel.extra_instances)

    return info


def get_effect_type(precept_id: str, intent: str) -> str:
    """
    Devuelve 'damage', 'heal', 'control' o 'utility' en base al modo del precepto
    y, solo si es 'mixed', usa la INTENCIÓN para decidir.
    """
    pre = PRECEPTS.get(precept_id, {})
    mode = pre.get("mode", "utility")

    # Caso especial: preceptos mixtos
    if mode == "mixed":
        if intent == "OFFENSIVE":
            return "damage"
        if intent == "DEFENSIVE":
            return "heal"
        # Condicional / neutro → se comporta como control / soporte
        return "control"

    # Si el modo es uno de los estándar, lo respetamos tal cual
    if mode in ("damage", "heal", "control", "utility"):
        return mode

    # Fallback por si algún precepto no tiene modo bien definido
    if intent == "OFFENSIVE":
        return "damage"
    if intent == "DEFENSIVE":
        return "heal"
    return "utility"



# ============================================================
# SUGERENCIAS MECÁNICAS (GLUTINANTES)
# ============================================================

def suggest_mechanics(
    precept_id: str,
    numen_ids: list[str],
    modifiers: list[ModifierSelection],
    complexity: int,
    long_duration: bool = False,
) -> dict:
    """
    Devuelve un dict con sugerencias mecánicas glutinantes:
    - type: 'damage', 'heal', 'control' o 'utility'
    - summary: texto breve
    - details: dict con info estructurada (dados, área, etc.)
    """
    tier = derive_tier(complexity)
    intent = get_intent_from_modifiers(modifiers)
    mod_info = extract_modifier_info(modifiers)
    effect_type = get_effect_type(precept_id, intent)

    if effect_type in ("damage", "heal"):
        return suggest_damage_or_heal(
            precept_id=precept_id,
            numen_ids=numen_ids,
            tier=tier,
            effect_type=effect_type,   # 🔁 aquí pasamos damage/heal
            intent=intent,             # sigue siendo útil p.ej. para texto
            mod_info=mod_info,
            long_duration=long_duration,
        )
    elif effect_type == "control":
        return suggest_control_effect(
            precept_id=precept_id,
            numen_ids=numen_ids,
            tier=tier,
            intent=intent,
            mod_info=mod_info,
            long_duration=long_duration,
        )
    else:
        return suggest_utility_effect(
            precept_id=precept_id,
            numen_ids=numen_ids,
            tier=tier,
            intent=intent,
            mod_info=mod_info,
            long_duration=long_duration,
        )



def _suggest_area_description(
    shape: str | None,
    tier: int,
    extendido_rank: int,
) -> dict:
    """
    Devuelve una descripción de área según forma, tier
    y rango de ALCANCE_EXTENDIDO.
    - El tier marca la escala base.
    - Cada rango de Extendido aumenta el tamaño (no la potencia).
    """
    if shape is None:
        # Sin forma → objetivo único
        if extendido_rank > 0:
            desc = "Objetivo único a alcance medio (~18 m)."
        else:
            desc = "Objetivo único a alcance corto (~6 m)."
        return {
            "shape": "TARGET",
            "description": desc,
        }

    # Escala base por tier (3, 6, 9, 12…)
    radius_base = 3 + (tier - 1) * 3

    # Cada rango de Extendido crece el área
    if extendido_rank > 0:
        radius_base += 3 * extendido_rank

    if shape == "LINE":
        length = radius_base * 2
        return {
            "shape": "LINE",
            "length_m": length,
            "width_m": 1.5,
            "description": f"Línea de ~{length} m de largo, 1 casilla de ancho.",
        }
    if shape == "CONE":
        return {
            "shape": "CONE",
            "radius_m": radius_base,
            "description": f"Cono de ~{radius_base} m de alcance desde el regidor.",
        }
    if shape == "SPHERE":
        return {
            "shape": "SPHERE",
            "radius_m": radius_base,
            "description": f"Esfera de ~{radius_base} m de radio.",
        }
    if shape == "AURA":
        aura_r = max(3, radius_base - 3)
        return {
            "shape": "AURA",
            "radius_m": aura_r,
            "description": f"Aura alrededor del regidor de ~{aura_r} m.",
        }
    if shape == "WALL":
        length = radius_base * 2
        return {
            "shape": "WALL",
            "length_m": length,
            "height_m": 3,
            "description": f"Muro de hasta ~{length} m de largo y 3 m de alto.",
        }

    return {
        "shape": "UNKNOWN",
        "description": "Forma inusual; define el área narrativamente.",
    }




def suggest_damage_or_heal(
    precept_id: str,
    numen_ids: list[str],
    tier: int,
    effect_type: str,   # 'damage' o 'heal', viene del modo del precepto
    intent: str,
    mod_info: dict,
    long_duration: bool,
) -> dict:
    """
    Sugiere daño o curación en dados, área y duración.
    - effect_type viene del modo del precepto ('damage' o 'heal')
    - intent aún nos sirve para matices (ofensivo/defensivo/condicional)
    """

    # 1) UP base
    up = 1

    # 2) Potenciado → más potencia
    up += mod_info["potenciado_rank"]

    # 3) Reducido → atenúa
    if mod_info.get("has_reducido", False):
        up = max(0, up - 1)

    # 4) Tier → escala ligera
    total_dice = max(1, up + (tier - 1))

    # 5) Multiplicado → SOLO instancias, no rango
    instances = max(1, mod_info.get("multiplicado_instances", 1))
    dice_per_instance = max(1, total_dice // instances)

    # 6) Persistente → repartir por rondas (DoT/HoT)
    per_round = None
    rounds = None
    duration_text = "Instantáneo"

    if mod_info.get("has_persistente", False) or long_duration:
        rounds = 1 + max(0, mod_info.get("potenciado_rank", 0))
        rounds = min(rounds, 4)
        per_round = max(1, math.ceil(dice_per_instance / rounds))
        duration_text = f"Persistente ~{rounds} rondas"

    # Área
    area = _suggest_area_description(
        shape=mod_info.get("shape"),
        tier=tier,
        extendido_rank=mod_info.get("extendido_rank", 0),
    )

    element_name = NUMEN[numen_ids[0]]["name"] if numen_ids else "Genérico"

    # Aquí ya no miramos la intención para decidir el tipo,
    # usamos effect_type (viene del modo del precepto).
    eff_kind = "daño" if effect_type == "damage" else "curación"

    if per_round is not None and rounds is not None:
        summary = (
            f"{eff_kind.title()}: {per_round}d6 por ronda"
            f" durante ~{rounds} rondas ({element_name}), "
            f"{instances} instancia(s), área: {area['description']}"
        )
    else:
        summary = (
            f"{eff_kind.title()}: {dice_per_instance}d6"
            f" ({element_name}), {instances} instancia(s), "
            f"área: {area['description']}"
        )

    return {
        "type": effect_type,  # 'damage' o 'heal' directo
        "summary": summary,
        "details": {
            "tier": tier,
            "total_dice_d6": total_dice,
            "dice_per_instance_d6": dice_per_instance,
            "instances": instances,
            "persistent": per_round is not None and rounds is not None,
            "dice_per_round_d6": per_round,
            "rounds": rounds,
            "element": element_name,
            "area": area,
            "duration": duration_text,
            "intent": intent,
        },
    }




def suggest_control_effect(
    precept_id: str,
    numen_ids: list[str],
    tier: int,
    intent: str,
    mod_info: dict,
    long_duration: bool,
) -> dict:
    """
    Sugiere un efecto de control basado en tier e intensidad.
    """
    pre = PRECEPTS.get(precept_id, {})
    category = pre.get("category", "Control")
    pot = mod_info["potenciado_rank"]

    # Severidad: 1–4
    has_reducido = mod_info["has_reducido"]

    severity = tier
    if pot >= 2:
        severity += 1
    if has_reducido:
        severity -= 1

    severity = min(4, max(1, severity))


    # Área
    area = _suggest_area_description(
        shape=mod_info["shape"],
        tier=tier,
        extendido_rank=mod_info["extendido_rank"],
    )



    # Duración en rondas
    rounds = severity
    if long_duration or mod_info["has_persistente"]:
        rounds += 1
    rounds = min(rounds, 6)

    # Tipo de control aproximado
    control_kind = "general"
    if category == "Cognitiva":
        control_kind = "mental/sensorial"
    elif category == "Elemental":
        control_kind = "de movimiento/entorno"
    elif category == "Vital":
        control_kind = "de estado físico/vital"
    elif category == "Constructiva":
        control_kind = "de bloqueo/estructura"

    # DC sugerida
    dc = 10 + tier  # luego le sumas bonificador del regidor en mesa

    summary = (
        f"Efecto de control {control_kind} de severidad {severity} "
        f"durante ~{rounds} rondas. Salvación sugerida DC {dc} + HOP."
    )

    return {
        "type": "control",
        "summary": summary,
        "details": {
            "tier": tier,
            "severity": severity,
            "rounds": rounds,
            "control_kind": control_kind,
            "suggested_dc_base": dc,
            "persistent": mod_info["has_persistente"] or long_duration,
        },
    }


def suggest_utility_effect(
    precept_id: str,
    numen_ids: list[str],
    tier: int,
    intent: str,
    mod_info: dict,
    long_duration: bool,
) -> dict:
    """
    Sugiere un efecto utilitario / exploración / soporte sin números concretos.
    """
    pre = PRECEPTS.get(precept_id, {})
    category = pre.get("category", "Utility")
    element_name = NUMEN[numen_ids[0]]["name"] if numen_ids else "Genérico"
    area = _suggest_area_description(
        shape=mod_info["shape"],
        tier=tier,
        extendido_rank=mod_info["extendido_rank"],
    )



    # Duración narrativa
    if mod_info["has_persistente"] or long_duration:
        dur = "varios minutos"
    else:
        dur = "instantáneo o unos segundos"

    summary = (
        f"Efecto utilitario de categoría {category.lower()} ligado a {element_name}, "
        f"área: {area['description']}, duración {dur}."
    )

    return {
        "type": "utility",
        "summary": summary,
        "details": {
            "tier": tier,
            "category": category,
            "element": element_name,
            "area": area,
            "duration_narrative": dur,
        },
    }


# ---------- Simple JSON "DB" helpers ----------

DB_PATH = "ordinances_db.json"


def load_ordinances() -> Dict[str, Ordinance]:
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    ordinances: Dict[str, Ordinance] = {}
    for oid, data in raw.items():
        modifiers = [
            ModifierSelection(**m) for m in data["modifiers"]
        ]
        ordinances[oid] = Ordinance(
            id=data["id"],
            canonical_key=data["canonical_key"],
            name=data["name"],
            precept_id=data["precept_id"],
            numen_ids=data["numen_ids"],
            modifiers=modifiers,
            mechanical=data["mechanical"],
            cost=data["cost"],
            tier=data["tier"],
            meta=data["meta"],
        )
    return ordinances


def save_ordinances(ordinances: Dict[str, Ordinance]) -> None:
    raw: Dict[str, Any] = {}
    for oid, ord_obj in ordinances.items():
        raw[oid] = asdict(ord_obj)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)


def find_by_canonical_key(
    ordinances: Dict[str, Ordinance],
    canonical_key: str,
) -> Ordinance | None:
    for ord_obj in ordinances.values():
        if ord_obj.canonical_key == canonical_key:
            return ord_obj
    return None


def next_ordinance_id(ordinances: Dict[str, Ordinance]) -> str:
    # simple incremental id
    if not ordinances:
        return "ORD_000001"
    nums = [
        int(o.id.split("_")[-1])
        for o in ordinances.values()
        if o.id.startswith("ORD_")
    ]
    n = max(nums) + 1 if nums else 1
    return f"ORD_{n:06d}"

# arcana_core.py

from __future__ import annotations
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from arcana_data import NUMEN, PRECEPTS, MODIFIERS, get_base_die_for_precept
from datetime import datetime, timezone
from huggingface_hub import HfApi
from pathlib import Path
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
        "persistente_rank": 0,      # 0 = no persistente, 1+ = duración más larga
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
            # si no has definido rank en el selector, asumimos 1
            rank = sel.rank if getattr(sel, "rank", None) else 1
            info["persistente_rank"] = max(info["persistente_rank"], rank)
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

def _suggest_duration_profile(
    effect_type: str,           # 'damage', 'heal', 'control', 'utility'
    tier: int,                  # 1–4
    persistente_rank: int,      # 0–3
    potenciado_rank: int,       # 0–3
    long_duration: bool,        # flag del UI
) -> dict:
    """
    Devuelve un perfil de duración:
    - kind: 'INSTANT', 'ROUNDS', 'MINUTES', 'HOURS', 'DAYS', 'WEEKS', 'MONTHS_YEARS'
    - text: texto narrativo
    - rounds: nº de rondas si aplica
    - upkeep: 'bajo', 'medio', 'alto', 'muy alto'
    """

    # Sin persistencia ni intención de larga duración → instantáneo
    if persistente_rank <= 0 and not long_duration:
        return {
            "kind": "INSTANT",
            "text": "Instantáneo o unos segundos.",
            "rounds": None,
            "upkeep": "bajo",
        }

    # “Potencia de duración”: cuánto se está forzando a durar
    duration_power = tier + persistente_rank + potenciado_rank
    if long_duration:
        duration_power += 1  # botón explícito de querer algo más largo

    # Daño/curación vs utilidad/control
    is_heavy = effect_type in ("damage", "heal")

    # Mapeo para daño/curación (más caro y más difícil mantener en el tiempo)
    if is_heavy:
        if duration_power <= 2:
            # combate / pocos turnos
            rounds = 2 + duration_power  # 2–4 aprox.
            return {
                "kind": "ROUNDS",
                "text": f"Persistente durante ~{rounds} rondas.",
                "rounds": rounds,
                "upkeep": "medio",
            }
        elif duration_power <= 4:
            return {
                "kind": "MINUTES",
                "text": "Activa durante varios minutos.",
                "rounds": None,
                "upkeep": "alto",
            }
        elif duration_power <= 6:
            return {
                "kind": "HOURS",
                "text": "Activa durante varias horas. Requiere concentración intensa.",
                "rounds": None,
                "upkeep": "muy alto",
            }
        elif duration_power <= 8:
            return {
                "kind": "DAYS",
                "text": "Se mantiene un día entero a gran coste numénico.",
                "rounds": None,
                "upkeep": "extremo",
            }
        else:
            return {
                "kind": "WEEKS",
                "text": "Sostener este efecto semanas roza el límite de lo posible; suele requerir anclaje o ritual estable.",
                "rounds": None,
                "upkeep": "extremo",
            }

    # Mapeo para utility/control (más fácil mantener en el tiempo)
    else:
        if duration_power <= 2:
            return {
                "kind": "MINUTES",
                "text": "Activa durante algunos minutos.",
                "rounds": None,
                "upkeep": "bajo",
            }
        elif duration_power <= 4:
            return {
                "kind": "HOURS",
                "text": "Activa durante varias horas. Coste numénico basal moderado.",
                "rounds": None,
                "upkeep": "medio",
            }
        elif duration_power <= 6:
            return {
                "kind": "DAYS",
                "text": "Efecto sostenido durante uno o varios días.",
                "rounds": None,
                "upkeep": "medio-alto",
            }
        elif duration_power <= 8:
            return {
                "kind": "WEEKS",
                "text": "Efecto anclado durante semanas, habitual en rituales de alto nivel.",
                "rounds": None,
                "upkeep": "alto",
            }
        else:
            return {
                "kind": "MONTHS_YEARS",
                "text": "Efecto cuasi-permanente (meses o años). Se debe repetir para ser permanente.",
                "rounds": None,
                "upkeep": "muy alto",
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

    # 4) Selección del dado según modo del precepto + tier
    dice_base = get_base_die_for_precept(precept_id, effect_type)

    total_dice = max(1, up + (tier - 1))

    # 5) Instancias (por Multiplicado)
    instances = max(1, mod_info.get("multiplicado_instances", 1))
    dice_per_instance = max(1, total_dice // instances)


    # 6) Persistente → repartir por rondas (DoT/HoT)
    duration_profile = _suggest_duration_profile(
        effect_type=effect_type,
        tier=tier,
        persistente_rank=mod_info.get("persistente_rank", 0),
        potenciado_rank=mod_info.get("potenciado_rank", 0),
        long_duration=long_duration,
    )

    per_round = None
    rounds = duration_profile.get("rounds")
    duration_text = duration_profile["text"]

    # Solo tiene sentido hablar de “por ronda” si la duración es de rondas
    if duration_profile["kind"] == "ROUNDS" and rounds:
        per_round = max(1, math.ceil(dice_per_instance / rounds))

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
            f"{eff_kind.title()} sugerida: {per_round}d{dice_base} por ronda"
            f" durante ~{rounds} rondas ({element_name}), "
            f"{instances} instancia(s), área: {area['description']}"
        )
    else:
        summary = (
            f"{eff_kind.title()} sugerida: {dice_per_instance}d{dice_base}"
            f" ({element_name}), {instances} instancia(s), "
            f"{area['description']} — {duration_text}"
        )


    return {
        "type": effect_type,  # 'damage' o 'heal' directo
        "summary": summary,
        "details": {
            "tier": tier,
            "total_dice": total_dice,
            "dice_per_instance": dice_per_instance,
            "instances": instances,
            "persistent": per_round is not None and rounds is not None,
            "dice_per_round": per_round,
            "rounds": rounds,
            "element": element_name,
            "area": area,
            "duration": duration_text,
            "intent": intent,
            "duration_kind": duration_profile["kind"],
            "upkeep": duration_profile["upkeep"],
            "duration_narrative": duration_text,

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
    duration_profile = _suggest_duration_profile(
        effect_type="control",
        tier=tier,
        persistente_rank=mod_info.get("persistente_rank", 0),
        potenciado_rank=mod_info.get("potenciado_rank", 0),
        long_duration=long_duration,
    )



    # Tipo de control aproximado
    control_kind = "general"
    if category == "Cognitiva":
        control_kind = "mental/sensorial"
    elif category == "Elemental":
        control_kind = "de movimiento/entorno"
    elif category == "Vital":
        control_kind = "de estado físico/vital"
    elif category == "Pragmática":
        control_kind = "de bloqueo/estructura"

    # DC sugerida
    dc = 10 + tier  # luego le sumas bonificador del regidor en mesa

    rounds = duration_profile.get("rounds")
    summary = (
        f"Efecto de control {control_kind} de severidad {severity}. "
        f"{duration_profile['text']} Salvación sugerida DC {dc} + HOP."
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
            "duration_kind": duration_profile["kind"],
            "duration_narrative": duration_profile["text"],
            "upkeep": duration_profile["upkeep"],
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
    duration_profile = _suggest_duration_profile(
        effect_type="utility",
        tier=tier,
        persistente_rank=mod_info.get("persistente_rank", 0),
        potenciado_rank=mod_info.get("potenciado_rank", 0),
        long_duration=long_duration,
    )

    area = _suggest_area_description(
        shape=mod_info.get("shape"),
        tier=tier,
        extendido_rank=mod_info.get("extendido_rank", 0),
    )

    element_name = NUMEN[numen_ids[0]]["name"] if numen_ids else "Genérico"

    summary = (
        f"Efecto utilitario de tipo {category.lower()} ligado a {element_name}, "
        f"área: {area['description']}. {duration_profile['text']}"
    )

    return {
        "type": "utility",
        "summary": summary,
        "details": {
            "tier": tier,
            "category": category,
            "element": element_name,
            "area": area,
            "duration_kind": duration_profile["kind"],
            "duration_narrative": duration_profile["text"],
            "upkeep": duration_profile["upkeep"],
        },
    }



# ---------- Simple JSON "DB" helpers ----------

DB_PATH = os.environ.get( "ARCANA_DB_PATH", "ordinances_db.json")
BACKUP_DIR = Path(os.environ.get("ARCANA_BACKUP_DIR", "grimoire_h"))

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN_ARCANA")  # Tu Personal Access Token de GitHub
GITHUB_REPO = "Addraed/Arcana-Dataviz"  # Tu repo de GitHub
GITHUB_BRANCH = "main"  # o "master" según tu repo

# Ensure backup directory exists
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


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

def save_ordinances(
    ordinances: Dict[str, Ordinance], 
    make_backup: bool = False,
    commit_to_repo: bool = True
) -> None:
    """
    Save ordinances locally and optionally commit to GitHub repo.
    """
    print(f"🔍 save_ordinances called with {len(ordinances)} ordinances")
    
    raw: Dict[str, Any] = {oid: asdict(ord_obj) for oid, ord_obj in ordinances.items()}
    
    # Write main DB locally (ephemeral)
    print(f"💾 Saving to local DB_PATH: {DB_PATH}")
    try:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=2)
        print(f"✓ Local save successful")
    except Exception as e:
        print(f"✗ Local save failed: {e}")
    
    # Write timestamped backup (optional)
    if make_backup:
        try:
            backup_path = _write_backup_snapshot(raw)
            print(f"✓ Backup created: {backup_path}")
        except Exception as e:
            print(f"⚠️  Backup failed: {e}")
    
    # Commit to GitHub repo
    if commit_to_repo:
        print(f"🚀 Attempting to commit to GitHub repo...")
        
        if not GITHUB_TOKEN:
            print("✗ GITHUB_TOKEN not found - skipping repo commit")
            return
        
        try:
            _commit_to_github_repo(raw)
            print("✓ Commit to GitHub successful!")
        except Exception as e:
            print(f"✗ Commit to GitHub failed: {e}")
            import traceback
            traceback.print_exc()


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

def _write_backup_snapshot(raw: Dict[str, Any]) -> Path:
    """Create timestamped backup"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    backup_path = BACKUP_DIR / f"ordinances_db_{ts}.json"
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)
    return backup_path

def _commit_to_github_repo(raw: Dict[str, Any]) -> None:
    """Commit current ordinances to GitHub repository using GitHub API"""
    
    file_path = "ordinances_db.json"
    
    # Convert to JSON
    json_content = json.dumps(raw, ensure_ascii=False, indent=2)
    
    # Encode to base64 (GitHub API requirement)
    content_base64 = base64.b64encode(json_content.encode('utf-8')).decode('utf-8')
    
    # GitHub API endpoint
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get current file SHA (needed to update existing file)
    print(f"   Checking if file exists...")
    response = requests.get(url, headers=headers)
    
    sha = None
    if response.status_code == 200:
        sha = response.json()["sha"]
        print(f"   File exists, SHA: {sha[:7]}...")
    else:
        print(f"   File doesn't exist, will create new")
    
    # Prepare commit data
    commit_message = f"💾 Auto-save ordinances from HF Space [{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}]"
    
    data = {
        "message": commit_message,
        "content": content_base64,
        "branch": GITHUB_BRANCH
    }
    
    if sha:
        data["sha"] = sha  # Required to update existing file
    
    # Commit to GitHub
    print(f"   Committing to GitHub...")
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"   ✓ Successfully committed to GitHub!")
        result = response.json()
        print(f"   Commit URL: {result['commit']['html_url']}")
    else:
        print(f"   ✗ GitHub API error: {response.status_code}")
        print(f"   Response: {response.text}")
        raise Exception(f"GitHub commit failed: {response.status_code} - {response.text}")

def export_ordinances_json_bytes(ordinances: Dict[str, Ordinance]) -> bytes:
    """Export ordinances as JSON bytes"""
    raw: Dict[str, Any] = {oid: asdict(ord_obj) for oid, ord_obj in ordinances.items()}
    return json.dumps(raw, ensure_ascii=False, indent=2).encode("utf-8")

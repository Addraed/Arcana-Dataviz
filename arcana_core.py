# arcana_core.py

from __future__ import annotations
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from arcana_data import NUMEN, PRECEPTS, MODIFIERS
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

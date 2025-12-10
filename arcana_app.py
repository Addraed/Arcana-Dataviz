# arcana_app.py

import streamlit as st
from typing import List
from arcana_data import PRECEPTS, NUMEN, MODIFIERS
from arcana_core import (
    ModifierSelection,
    Ordinance,
    build_canonical_key,
    calculate_complexity,
    derive_tier,
    load_ordinances,
    save_ordinances,
    find_by_canonical_key,
    next_ordinance_id,
)

st.set_page_config(page_title="A.R.C.A.N.A. Constructor", layout="wide")

# Load DB
ORDINANCES = load_ordinances()

st.title("A.R.C.A.N.A. — Constructor de Ordenanzas")

# --- 1) Select Precept ---

st.sidebar.header("1. Precepto (Raíz)")
precept_options = list(PRECEPTS.keys())
precept_labels = [f"{pid} – {PRECEPTS[pid]['verb']}" for pid in precept_options]
precept_choice = st.sidebar.selectbox(
    "Elige un Precepto base:",
    options=precept_options,
    format_func=lambda pid: f"{PRECEPTS[pid]['verb']} ({pid})",
)

precept = PRECEPTS[precept_choice]
st.subheader(f"Precepto seleccionado: {precept['verb']}")
st.markdown(precept["description"])

with st.expander("Detalles del Precepto"):
    st.json(precept, expanded=False)

# --- 2) Select Numen ---

st.sidebar.header("2. Numen (color/afinidad)")
numen_ids = list(NUMEN.keys())

numen_multi_choice = st.sidebar.multiselect(
    "Selecciona uno o más Numen:",
    options=numen_ids,
    format_func=lambda nid: NUMEN[nid]["display_name"],
    default=precept.get("preferred_numen_ids", [])[:1],  # default: preferente
)

if not numen_multi_choice:
    st.warning("Selecciona al menos un Numen para continuar.")
    st.stop()

st.write("### Numen seleccionados")
cols = st.columns(len(numen_multi_choice))
for col, nid in zip(cols, numen_multi_choice):
    n = NUMEN[nid]
    with col:
        st.markdown(
            f"<div style='padding:0.5rem;border-radius:8px;border:1px solid #444;"
            f"background:{n['color_hex']}22;'>"
            f"<strong>{n['display_name']}</strong><br>"
            f"<small>{', '.join(n['tags'])}</small>"
            f"</div>",
            unsafe_allow_html=True,
        )

# --- 3) Select Modifiers ---

st.sidebar.header("3. Partículas / Modificadores")

# Group modifiers by family for nicer UI
families = ["FORMA", "ALCANCE_DURACION", "INTENCION", "INTENSIDAD"]
selected_modifiers: List[ModifierSelection] = []

for fam in families:
    fam_mods = {mid: m for mid, m in MODIFIERS.items() if m["family"] == fam}
    if not fam_mods:
        continue

    st.sidebar.markdown(f"**{fam.replace('_', ' ').title()}**")

    chosen_ids = st.sidebar.multiselect(
        f"Modificadores ({fam.lower()}):",
        options=list(fam_mods.keys()),
        format_func=lambda mid: MODIFIERS[mid]["name"],
        key=f"ms_{fam}",
    )

    for mid in chosen_ids:
        mod = MODIFIERS[mid]
        # Controls for rank / extra instances if relevant
        rank = 1
        extra = 0
        if mid == "INTENSIDAD_POTENCIADO":
            rank = st.sidebar.slider(
                "Rango de Potenciado",
                min_value=1,
                max_value=mod.get("max_rank", 3),
                value=1,
                key=f"rank_{mid}",
            )
        if mid == "INTENSIDAD_MULTIPLICADO":
            extra = st.sidebar.number_input(
                "Instancias adicionales (Multiplicado)",
                min_value=0,
                max_value=10,
                value=0,
                step=1,
                key=f"extra_{mid}",
            )

        selected_modifiers.append(
            ModifierSelection(
                modifier_id=mid,
                rank=rank,
                extra_instances=extra,
            )
        )

long_duration = any(
    sel.modifier_id == "DURACION_PERSISTENTE" for sel in selected_modifiers
) and st.sidebar.checkbox(
    "¿Duración larga (encarece Persistente)?",
    value=False,
)

# --- 4) Compute canonical key / complexity / tier ---

canonical_key = build_canonical_key(
    precept_id=precept_choice,
    numen_ids=numen_multi_choice,
    modifiers=selected_modifiers,
)

complexity = calculate_complexity(
    precept_id=precept_choice,
    numen_ids=numen_multi_choice,
    modifiers=selected_modifiers,
    long_duration=long_duration,
)
tier = derive_tier(complexity)

st.markdown("---")
st.header("Sintaxis y Coste de la Ordenanza")

st.code(
    f"{precept['verb']} + "
    f\"{', '.join(NUMEN[nid]['name'] for nid in numen_multi_choice)}\" + "
    f\"[{', '.join(MODIFIERS[m.modifier_id]['name'] for m in selected_modifiers)}]\",
    language="text",
)

st.write(f"**Clave canónica:** `{canonical_key}`")
st.write(f"**Complejidad total:** {complexity}")
st.write(f"**Tier sugerido:** {tier} (1=Aprendiz, 2=Adeptus, 3=Maestro, 4=Archirregidor)")

# --- 5) DB lookup: does this ordinance already exist? ---

existing = find_by_canonical_key(ORDINANCES, canonical_key)

if existing:
    st.success("Esta combinación ya existe en el grimorio.")
    st.subheader(existing.name)
    st.write("### Efecto mecánico")
    st.json(existing.mechanical)
    st.write("### Coste")
    st.json(existing.cost)
    st.write("### Metadatos")
    st.json(existing.meta)
else:
    st.info("Esta combinación aún no está registrada. Puedes guardarla como nueva Ordenanza.")

    with st.form("new_ordinance_form"):
        name = st.text_input("Nombre de la Ordenanza", value="")
        effect_narrative = st.text_area(
            "Efecto narrativo",
            value="Describe cómo se manifiesta esta Ordenanza.",
        )
        mechanical_notes = st.text_area(
            "Efecto mecánico (stats, daño, área, etc.)",
            value="Ej: 3d6 fuego en cono de 6m, Persistente 3 turnos.",
        )
        created_by = st.text_input("Creado por", value="Manu")
        source = st.text_input("Fuente (campaña/sesión)", value="")

        submitted = st.form_submit_button("Guardar Ordenanza")

        if submitted:
            if not name.strip():
                st.error("La Ordenanza necesita un nombre.")
            else:
                oid = next_ordinance_id(ORDINANCES)
                ord_obj = Ordinance(
                    id=oid,
                    canonical_key=canonical_key,
                    name=name.strip(),
                    precept_id=precept_choice,
                    numen_ids=numen_multi_choice,
                    modifiers=selected_modifiers,
                    mechanical={
                        "narrative": effect_narrative,
                        "notes": mechanical_notes,
                    },
                    cost={
                        "complexity_points": complexity,
                        "tier": tier,
                    },
                    tier=tier,
                    meta={
                        "created_by": created_by,
                        "source": source,
                    },
                )
                ORDINANCES[oid] = ord_obj
                save_ordinances(ORDINANCES)
                st.success(f"Ordenanza '{name}' guardada con id {oid}. Recarga para verla en el grimorio.")

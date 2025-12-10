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
    suggest_mechanics,   
)


st.set_page_config(page_title="A.R.C.A.N.A. Constructor", layout="wide")

# Load DB
ORDINANCES = load_ordinances()

st.title("A.R.C.A.N.A. — Sistema de Ordenanzas")

# -------------------------------------------------------------------
# MODE SWITCH
# -------------------------------------------------------------------
st.sidebar.markdown("## Modo")
mode = st.sidebar.radio(
    "Selecciona modo de trabajo",
    [
        "Constructor de Ordenanzas",
        "Explorador de Preceptos",
        "Explorador de Numen",
        "Explorador de Modificadores",
        "Grimorio de Ordenanzas",
    ],
)

# ===================================================================
# MODO: EXPLORADOR DE PRECEPTOS
# ===================================================================
if mode == "Explorador de Preceptos":
    st.header("Explorador de Preceptos (Raíces)")

    # Categorías dinámicas
    categories = sorted(
        {p.get("category", "Sin categoría") for p in PRECEPTS.values()}
    )
    categories.insert(0, "Todos")

    col_filters = st.columns([2, 2, 3])
    with col_filters[0]:
        category_filter = st.selectbox(
            "Filtrar por categoría:",
            options=categories,
            index=0,
        )
    with col_filters[1]:
        search_text = st.text_input(
            "Buscar por nombre/verbo:",
            value="",
            placeholder="Ej: Encender, Curar...",
        )

    # Filtro
    filtered_ids = []
    for pid, p in PRECEPTS.items():
        if category_filter != "Todos" and p.get("category") != category_filter:
            continue
        if search_text:
            t = search_text.lower()
            if t not in p["verb"].lower() and t not in p.get(
                "description", ""
            ).lower():
                continue
        filtered_ids.append(pid)

    if not filtered_ids:
        st.info("No se han encontrado preceptos con esos filtros.")
    else:
        st.write(f"Se han encontrado **{len(filtered_ids)}** preceptos.")
        for pid in sorted(filtered_ids):
            p = PRECEPTS[pid]
            with st.expander(f"{p['verb']} ({pid}) — {p.get('category', '')}"):
                st.markdown(f"**Verbo:** `{p['verb']}`")
                st.markdown(f"**ID:** `{pid}`")
                st.markdown(f"**Categoría:** `{p.get('category', '—')}`")

                pref_numen = p.get("preferred_numen_ids", [])
                if pref_numen:
                    st.markdown("**Numen preferente:**")
                    cols_numen = st.columns(len(pref_numen))
                    for c, nid in zip(cols_numen, pref_numen):
                        if nid in NUMEN:
                            n = NUMEN[nid]
                            with c:
                                st.markdown(
                                    f"<div style='padding:0.4rem;border-radius:6px;"
                                    f"border:1px solid #444;background:{n['color_hex']}22;'>"
                                    f"<strong>{n['display_name']}</strong><br>"
                                    f"<small>{', '.join(n['tags'])}</small>"
                                    f"</div>",
                                    unsafe_allow_html=True,
                                )
                        else:
                            c.write(f"- {nid} (definir en NUMEN)")

                st.markdown("**Descripción:**")
                st.write(p.get("description", "_Sin descripción_"))

                ex = p.get("example_ordinances", [])
                if ex:
                    st.markdown("**Ejemplos de Ordenanzas:**")
                    for e in ex:
                        st.markdown(f"- {e}")


    st.stop()

# ===================================================================
# MODO: EXPLORADOR DE NUMEN
# ===================================================================
if mode == "Explorador de Numen":
    st.header("Explorador de Numen")

    # Tags dinámicos
    all_tags = sorted(
        {tag for n in NUMEN.values() for tag in n.get("tags", [])}
    )
    all_tags.insert(0, "Todos")

    col_filters = st.columns([2, 2, 3])
    with col_filters[0]:
        tag_filter = st.selectbox(
            "Filtrar por tag:",
            options=all_tags,
            index=0,
        )
    with col_filters[1]:
        search_text = st.text_input(
            "Buscar por nombre:",
            value="",
            placeholder="Ej: Ignis, Umbra...",
        )

    filtered_ids = []
    for nid, n in NUMEN.items():
        if tag_filter != "Todos" and tag_filter not in n.get("tags", []):
            continue
        if search_text:
            t = search_text.lower()
            if t not in n["name"].lower() and t not in n["display_name"].lower():
                continue
        filtered_ids.append(nid)

    if not filtered_ids:
        st.info("No se han encontrado Numen con esos filtros.")
    else:
        st.write(f"Se han encontrado **{len(filtered_ids)}** Numen.")
        cols = st.columns(3)
        for i, nid in enumerate(sorted(filtered_ids)):
            n = NUMEN[nid]
            col = cols[i % 3]
            with col:
                st.markdown(
                    f"<div style='margin-bottom:0.8rem;padding:0.6rem;border-radius:10px;"
                    f"border:1px solid #444;background:{n['color_hex']}33;'>"
                    f"<strong>{n['display_name']}</strong><br>"
                    f"<small>{', '.join(n.get('tags', []))}</small><br>"
                    f"<span style='font-size: 0.8rem;'>{n.get('short_description', n.get('description', '')[:90] + '...')}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )


    st.stop()

# ===================================================================
# MODO: EXPLORADOR DE MODIFICADORES
# ===================================================================
if mode == "Explorador de Modificadores":
    st.header("Explorador de Modificadores / Partículas")

    families = sorted({m["family"] for m in MODIFIERS.values()})
    families.insert(0, "Todas")

    col_filters = st.columns([2, 2, 3])
    with col_filters[0]:
        fam_filter = st.selectbox(
            "Filtrar por familia:",
            options=families,
            index=0,
        )
    with col_filters[1]:
        search_text = st.text_input(
            "Buscar por nombre:",
            value="",
            placeholder="Ej: Cono, Persistente...",
        )

    filtered_ids = []
    for mid, m in MODIFIERS.items():
        if fam_filter != "Todas" and m["family"] != fam_filter:
            continue
        if search_text:
            t = search_text.lower()
            if t not in m["name"].lower() and t not in m.get(
                "description", ""
            ).lower():
                continue
        filtered_ids.append(mid)

    if not filtered_ids:
        st.info("No se han encontrado modificadores con esos filtros.")
    else:
        st.write(f"Se han encontrado **{len(filtered_ids)}** modificadores.")
        for mid in sorted(filtered_ids):
                    m = MODIFIERS[mid]
                    with st.expander(f"{m['name']}"):
                        st.markdown(f"**Familia:** {m['family']}")
                        st.markdown("**Descripción:**")
                        st.write(m.get("description", "_Sin descripción_"))

                        # Costes como texto, no JSON crudo
                        st.markdown("**Costes (modelo actual):**")
                        base_cost = m.get("base_cost")
                        rank_cost = m.get("rank_cost")
                        extra_long = m.get("extra_long_duration_cost")
                        per_instance = m.get("per_extra_instance_cost")

                        lines = []
                        if base_cost is not None:
                            lines.append(f"- Coste base: {base_cost}")
                        if rank_cost is not None:
                            lines.append(f"- Coste por rango: {rank_cost}")
                        if extra_long is not None:
                            lines.append(f"- Coste extra por duración larga: {extra_long}")
                        if per_instance is not None:
                            lines.append(f"- Coste por instancia adicional: {per_instance}")
                        if not lines:
                            lines.append("- Sin costes específicos definidos.")

                        st.markdown("\n".join(lines))

                        st.markdown("**Tags:** " + (", ".join(m.get("tags", [])) or "—"))


    st.stop()

# ===================================================================
# MODO: GRIMORIO DE ORDENANZAS
# ===================================================================
if mode == "Grimorio de Ordenanzas":
    st.header("Grimorio de Ordenanzas")

    if not ORDINANCES:
        st.info("Aún no hay Ordenanzas registradas. Usa el Constructor para crear algunas.")
        st.stop()

    # Filtros: Numen, Precepto, Tier, texto
    all_numen_ids = sorted({nid for o in ORDINANCES.values() for nid in o.numen_ids})
    all_precepts = sorted({o.precept_id for o in ORDINANCES.values()})
    all_tiers = sorted({o.tier for o in ORDINANCES.values()})

    col_filters = st.columns(4)
    with col_filters[0]:
        numen_filter = st.multiselect(
            "Filtrar por Numen:",
            options=all_numen_ids,
            format_func=lambda nid: NUMEN.get(nid, {}).get("display_name", nid),
        )
    with col_filters[1]:
        precept_filter = st.multiselect(
            "Filtrar por Precepto:",
            options=all_precepts,
            format_func=lambda pid: PRECEPTS.get(pid, {}).get("verb", pid),
        )
    with col_filters[2]:
        tier_filter = st.multiselect(
            "Filtrar por Tier:",
            options=all_tiers,
            default=all_tiers,
        )
    with col_filters[3]:
        search_text = st.text_input(
            "Buscar por nombre:",
            value="",
            placeholder="Ej: Llama Voraz...",
        )

    # Aplicar filtros
    filtered = []
    for o in ORDINANCES.values():
        if numen_filter and not any(n in o.numen_ids for n in numen_filter):
            continue
        if precept_filter and o.precept_id not in precept_filter:
            continue
        if tier_filter and o.tier not in tier_filter:
            continue
        if search_text:
            t = search_text.lower()
            if t not in o.name.lower():
                continue
        filtered.append(o)

    st.write(f"Se han encontrado **{len(filtered)}** Ordenanzas.")

    # Ordenar por tier y nombre
    filtered.sort(key=lambda x: (x.tier, x.name.lower()))

    for o in filtered:
        precept_name = PRECEPTS.get(o.precept_id, {}).get("verb", o.precept_id)
        numen_names = [
            NUMEN.get(nid, {}).get("name", nid) for nid in o.numen_ids
        ]
        with st.expander(
            f"{o.name} (Tier {o.tier}) — {precept_name} + {', '.join(numen_names)}"
        ):
            st.markdown(f"**ID:** `{o.id}`")
            st.markdown(f"**Clave canónica:** `{o.canonical_key}`")
            st.markdown(f"**Precepto:** `{precept_name}`")
            st.markdown(
                "**Numen:** "
                + ", ".join(
                    NUMEN.get(nid, {}).get("display_name", nid)
                    for nid in o.numen_ids
                )
            )

            # Mostrar modificadores
            if o.modifiers:
                st.markdown("**Modificadores:**")
                for sel in o.modifiers:
                    m = MODIFIERS.get(sel.modifier_id, {})
                    line = f"- {m.get('name', sel.modifier_id)}"
                    if sel.rank != 1:
                        line += f" (rango {sel.rank})"
                    if sel.extra_instances > 0:
                        line += f" · +{sel.extra_instances} instancias"
                    st.markdown(line)
            else:
                st.markdown("**Modificadores:** ninguno.")

            st.markdown("**Descripción:**")
            mech = o.mechanical or {}
            st.write(mech.get("narrative", ""))
            if "notes" in mech:
                st.markdown(f"**Efecto mecánico:** {mech['notes']}")


    st.stop()

# ===================================================================
# MODO: CONSTRUCTOR DE ORDENANZAS
# ===================================================================

# --- 1) Select Precept ---
st.sidebar.header("1. Precepto (Raíz)")
precept_options = sorted(
    PRECEPTS.keys(),
    key=lambda pid: PRECEPTS[pid]["verb"].lower()
)

precept_choice = st.sidebar.selectbox(
    "Elige un Precepto base:",
    options=precept_options,
    format_func=lambda pid: PRECEPTS[pid]["verb"],  # Solo el verbo, sin ID feo
)

precept = PRECEPTS[precept_choice]

st.header("Constructor de Ordenanzas")
st.subheader(f"Precepto seleccionado: **{precept['verb']}**")

# Descripción legible
st.markdown(precept.get("description", "_Sin descripción definida._"))

# Numen preferentes como texto
preferred = precept.get("preferred_numen_ids", [])
if preferred:
    names = [
        NUMEN[nid]["display_name"]
        for nid in preferred
        if nid in NUMEN
    ]
    st.markdown(f"**Numen preferentes:** {', '.join(names)}")
else:
    st.markdown("**Numen preferentes:** —")



# --- 2) Select Numen ---
st.sidebar.header("2. Numen (color/afinidad)")
numen_ids = list(NUMEN.keys())

numen_multi_choice = st.sidebar.multiselect(
    "Selecciona uno o más Numen:",
    options=numen_ids,
    format_func=lambda nid: NUMEN[nid]["display_name"],
    default=precept.get("preferred_numen_ids", [])[:1],
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
            f"<small>{', '.join(n.get('tags', []))}</small><br>"
            f"<span style='font-size: 0.8rem;'>{n.get('short_description', n.get('description', '')[:80] + '...')}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

# --- 3) Select Modifiers ---
st.sidebar.header("3. Partículas / Modificadores")

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
        rank = 1
        extra = 0

        if mid == "INTENSIDAD_POTENCIADO":
            rank = st.sidebar.slider(
                "Nivel de Potenciado",
                min_value=1,
                max_value=mod.get("max_rank", 3),
                value=1,
                key=f"rank_{mid}",
            )
        elif mid == "ALCANCE_EXTENDIDO":
            rank = st.sidebar.slider(
                "Rango de Alcance Extendido",
                min_value=1,
                max_value=mod.get("max_rank", 3),
                value=1,
                key=f"rank_{mid}",
            )
        elif mid == "DURACION_PERSISTENTE":
            rank = st.sidebar.slider(
                "Rango de Persistencia",
                min_value=1,
                max_value=mod.get("max_rank", 3),
                value=1,
                key=f"rank_{mid}",
            )
        elif mid == "INTENSIDAD_MULTIPLICADO":
            extra = st.sidebar.number_input(
                "Instancias adicionales (Multiplicado)",
                min_value=0,
                max_value=10,
                value=0,
                step=1,
                key=f"extra_{mid}",
            )
            # rank puede quedarse en 1 tranquilamente

        # Para el resto de modificadores sin rango, rank=1 por defecto
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

# --- 4) Compute canonical key / complexity / tier / Sugerencia mecánica automática ---

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

# Sugerencia mecánica automática (glutinante)
mechanics_suggestion = suggest_mechanics(
    precept_id=precept_choice,
    numen_ids=numen_multi_choice,
    modifiers=selected_modifiers,
    complexity=complexity,
    long_duration=long_duration,
)


st.markdown("---")
st.header("Sintaxis y Coste de la Ordenanza")

precept_part = precept["verb"]
numen_part = ", ".join(NUMEN[nid]["name"] for nid in numen_multi_choice)
mods_part = ", ".join(
    MODIFIERS[m.modifier_id]["name"] for m in selected_modifiers
) or "—"

syntax_str = f"{precept_part} + {numen_part} + [{mods_part}]"
st.code(syntax_str, language="text")

st.write(f"**Clave canónica:** `{canonical_key}`")
st.write(f"**Complejidad total:** {complexity}")
st.write(f"**Tier sugerido:** {tier} (1=Aprendiz, 2=Adeptus, 3=Maestro, 4=Archirregidor)")

st.subheader("Sugerencia mecánica automática")
st.write(mechanics_suggestion.get("summary", ""))



# --- 5) DB lookup / save ---

existing = find_by_canonical_key(ORDINANCES, canonical_key)

if existing:
    st.success("Esta combinación ya existe en el grimorio.")
    st.subheader(existing.name)

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
            value=mechanics_suggestion.get("summary", "Ej: 3d6 fuego en cono de 6m, Persistente 3 turnos."),
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
                st.success(
                    f"Ordenanza '{name}' guardada con id {oid}. "
                    "Revisa el Grimorio para consultarla."
                )





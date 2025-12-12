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
    export_ordinances_json_bytes
)


st.set_page_config(page_title="A.R.C.A.N.A. Constructor", layout="wide")

# Load DB
ORDINANCES = load_ordinances()

# ---------------------------------------------------------
# ESTILOS GLOBALES PARA TARJETAS DE NUMEN (HOVER REACTIVO)
# ---------------------------------------------------------

# ---------------------------------------------------------
# ESTILOS GLOBALES
# ---------------------------------------------------------

def inject_global_css():
    css = """
    <style>
    .numen-card {
        position: relative;
        padding: 0.5rem;
        border-radius: 10px;
        border: 1px solid #444;
        background: rgba(10, 10, 10, 0.4);
        transition:
            transform 0.18s ease-out,
            box-shadow 0.18s ease-out,
            filter 0.18s ease-out,
            border-color 0.18s ease-out;
        cursor: pointer;
        overflow: hidden;
        min-height: 5rem;
    }
    .numen-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 14px rgba(0,0,0,0.7);
    }
    .numen-card-name {
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.1rem;
        display: block;
    }

    .numen-card-tags {
        font-size: 0.75rem;
        opacity: 0.8;
        display: block;
        margin-bottom: 0.2rem;
    }

    .numen-card-desc {
        font-size: 0.75rem;
        opacity: 0.9;
        display: block;
    }

    /* Emblema pequeño a la derecha */
    .numen-card-emblem {
        position: relative;
        width: 46px;
        height: 46px;
        margin-right: 6px;
        flex-shrink: 0;
        transform: translateZ(10px);
        transition: transform 0.25s ease, filter 0.25s ease;
    }

    /* Imagen */
    .numen-card-emblem img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        filter: drop-shadow(0 0 4px rgba(0,0,0,0.65));
    }    

    
    /* CARTAS ANIMADAS DE ORDENANZA (details + summary) */
    details.ordinance-card {
        margin-bottom: 0.9rem;
        border-radius: 12px;
        border: 2px solid #444;
        background: rgba(5, 5, 5, 0.6);
        position: relative;
        overflow: hidden;
        transition:
            transform 0.18s ease-out,
            box-shadow 0.18s ease-out,
            border-color 0.18s ease-out;
    }

    details.ordinance-card summary {
        list-style: none;
        cursor: pointer;
        padding: 0.7rem 0.9rem;
        outline: none;
    }

    details.ordinance-card summary::-webkit-details-marker {
        display: none;
    }

    .ordinance-header-title {
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.1rem;
    }

    .ordinance-header-sub {
        font-size: 0.8rem;
        opacity: 0.85;
    }

    .ordinance-header-tag {
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.3rem;
        display: inline-block;
        padding: 0.1rem 0.4rem;
        border-radius: 999px;
        background: rgba(0, 0, 0, 0.4);
    }

    .ordinance-details {
        padding: 0 0.9rem 0.7rem 0.9rem;
        border-top: 1px solid rgba(255,255,255,0.06);
        font-size: 0.85rem;
    }

    /* Texturas animadas / vibración (ordenanzas) */
    details.ordinance-card::before {
        content: "";
        position: absolute;
        inset: -40%;
        background: conic-gradient(
            from 0deg,
            rgba(255,255,255,0.0),
            rgba(255,255,255,0.25),
            rgba(255,255,255,0.0),
            rgba(255,255,255,0.25),
            rgba(255,255,255,0.0)
        );
        opacity: 0.12;
        mix-blend-mode: screen;
        animation: spin-glow 18s linear infinite;
        pointer-events: none;
    }

    details.ordinance-card:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 0 20px rgba(0,0,0,0.8);
        animation: tilt-shake 0.35s ease-in-out;
    }

    @keyframes spin-glow {
        to {
            transform: rotate(360deg);
        }
    }

    @keyframes tilt-shake {
        0% { transform: translateY(-3px) rotate(0deg); }
        25% { transform: translateY(-3px) rotate(-0.7deg); }
        50% { transform: translateY(-3px) rotate(0.4deg); }
        75% { transform: translateY(-3px) rotate(-0.4deg); }
        100% { transform: translateY(-3px) rotate(0deg); }
    }

    /* Bordes según tipo de ordenanza */
    .ordinance-border-damage {
        border-color: #ff4b4b;
    }
    .ordinance-border-heal {
        border-color: #4caf50;
    }
    .ordinance-border-control {
        border-color: #ffc857;
    }
    .ordinance-border-utility {
        border-color: #7e57c2;
    }

    .ordinance-border-damage .ordinance-header-tag {
        color: #ffb3b3;
        border: 1px solid #ff4b4b;
    }
    .ordinance-border-heal .ordinance-header-tag {
        color: #b6ffb6;
        border: 1px solid #4caf50;
    }
    .ordinance-border-control .ordinance-header-tag {
        color: #ffe9a8;
        border: 1px solid #ffc857;
    }
    .ordinance-border-utility .ordinance-header-tag {
        color: #e1d0ff;
        border: 1px solid #7e57c2;
    }

    /* CARTAS COMPLETAS DE PRECEPTO (details+summary) */
    details.precept-card {
        margin-bottom: 0.7rem;
        border-radius: 10px;
        border: 2px solid #444;
        background: rgba(10, 10, 10, 0.65);
        position: relative;
        overflow: hidden;
        transition:
            transform 0.18s ease-out,
            box-shadow 0.18s ease-out,
            border-color 0.18s ease-out;
    }
    details.precept-card summary {
        list-style: none;
        cursor: pointer;
        padding: 0.6rem 0.8rem;
        outline: none;
    }
    details.precept-card summary::-webkit-details-marker {
        display: none;
    }
    .precept-header-title {
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.1rem;
    }
    .precept-header-sub {
        font-size: 0.8rem;
        opacity: 0.85;
    }
    .precept-header-tag {
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.3rem;
        display: inline-block;
        padding: 0.1rem 0.4rem;
        border-radius: 999px;
        background: rgba(0, 0, 0, 0.4);
    }
    .precept-details {
        padding: 0 0.8rem 0.6rem 0.8rem;
        border-top: 1px solid rgba(255,255,255,0.06);
        font-size: 0.85rem;
    }
    details.precept-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 16px rgba(0,0,0,0.8);
    }

    /* PRECEPTOS mini (constructor) */
    .precept-card {
        margin-top: 0.4rem;
        margin-bottom: 0.2rem;
        padding: 0.5rem 0.7rem;
        border-radius: 8px;
        border: 1px solid #444;
        background: rgba(10, 10, 10, 0.5);
        transition:
            transform 0.16s ease-out,
            box-shadow 0.16s ease-out,
            border-color 0.16s ease-out,
            background 0.16s ease-out;
        cursor: pointer;
    }
    .precept-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 14px rgba(0,0,0,0.7);
    }
    .precept-card-title {
        font-weight: 600;
        font-size: 0.95rem;
    }
    .precept-card-sub {
        font-size: 0.8rem;
        opacity: 0.85;
    }

    /* =============================
       CARTAS COMPLETAS DE NUMEN
       + 3D HOVER CON ICONO PNG
       ============================= */
    details.numen-card-full {
        margin-bottom: 0.7rem;
        border-radius: 10px;
        border: 2px solid #444;
        background: rgba(8, 8, 12, 0.7);
        position: relative;
        overflow: hidden;
        transition:
            transform 0.18s ease-out,
            box-shadow 0.18s ease-out,
            border-color 0.18s ease-out;
        perspective: 1000px; /* para efecto 3D interno */
    }
    details.numen-card-full summary {
        list-style: none;
        cursor: pointer;
        padding: 0.6rem 0.8rem;
        outline: none;
    }
    details.numen-card-full summary::-webkit-details-marker {
        display: none;
    }

    /* Contenedor 3D interno: icono + texto */
    .numen-3d-inner {
        display: flex;
        gap: 0.75rem;
        align-items: center;
        transform-style: preserve-3d;
        transition:
            transform 0.25s ease-out,
            filter 0.25s ease-out;
    }


    /* Bloque cabecera (nombre + tags) */
    .numen-header-block {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .numen-header-title {
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.1rem;
    }
    .numen-header-sub {
        font-size: 0.8rem;
        opacity: 0.85;
        margin-bottom: 0.15rem;
    }
    .numen-header-tags {
        font-size: 0.75rem;
        opacity: 0.9;
    }

    .numen-details {
        padding: 0 0.8rem 0.6rem 0.8rem;
        border-top: 1px solid rgba(255,255,255,0.06);
        font-size: 0.85rem;
    }

    /* Marco general hover (además de los efectos específicos por tipo) */
    details.numen-card-full:hover {
        transform: rotateX(8deg) rotateY(-7deg) translateY(-4px);
        box-shadow: 0 18px 30px rgba(0,0,0,0.75);
        overflow: visible
    }
    /* Al hacer hover sobre la carta, la badge crece y flota más */
    details.numen-card-full:hover .numen-emblem {
        transform: translateZ(26px) scale(1.5) translateY(-2px);
        box-shadow:
            0 0 0 1px rgba(255,255,255,0.25),
            0 14px 22px rgba(0,0,0,0.8);
        overflow: visible
    }

    details.numen-card-full:hover::before {
        opacity: 0 !important;
        animation: none !important;
    }


    /* “Emblema” del Numen: fondo + PNG */
    .numen-emblem {
        position: relative;
        width: 56px;      /* antes 56 */
        height: 56px;     /* antes 56 */
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        overflow: visible;      /* necesario para que sobresalga */
        flex-shrink: 0;
        transform: translateZ(22px);
    }


    .numen-emblem::before {
        content: "";
        position: absolute;
        inset: -10%;
        background: conic-gradient(
            from 0deg,
            rgba(255,255,255,0.0),
            rgba(255,255,255,0.25),
            rgba(255,255,255,0.0),
            rgba(255,255,255,0.25),
            rgba(255,255,255,0.0)
        );
        opacity: 0.18;
        mix-blend-mode: screen;
        animation: spin-glow 14s linear infinite;
        pointer-events: none;
    }

    .numen-emblem img {
        position: absolute;
        width: 56px;   /* tamaño real del PNG */
        height: 56px;
        object-fit: contain;
        filter:
            drop-shadow(0 0 3px rgba(0,0,0,0.7))
            drop-shadow(0 0 6px rgba(0,0,0,0.5));
    }
    

    /* reutilizamos textura animada en preceptos + numen */
    details.precept-card::before,
    details.numen-card-full::before {
        content: "";
        position: absolute;
        inset: -40%;
        background: conic-gradient(
            from 0deg,
            rgba(255,255,255,0.0),
            rgba(255,255,255,0.2),
            rgba(255,255,255,0.0),
            rgba(255,255,255,0.2),
            rgba(255,255,255,0.0)
        );
        opacity: 0.12;
        mix-blend-mode: screen;
        animation: spin-glow 20s linear infinite;
        pointer-events: none;
    }


    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def inject_numen_effects_css():
    css = """
    <style>
    /* ===========================
       ANIMACIONES BASE
       =========================== */

    @keyframes numen-fire-flicker {
        0%   { transform: translateY(-2px) scale(1.00); opacity: 0.8; }
        30%  { transform: translateY(-3px) scale(1.02); opacity: 1.0; }
        60%  { transform: translateY(-1px) scale(0.99); opacity: 0.9; }
        100% { transform: translateY(-2px) scale(1.01); opacity: 1.0; }
    }

    @keyframes numen-ice-shards {
        0%   { transform: translateX(0) skewX(0deg); opacity: 0.7; }
        50%  { transform: translateX(2px) skewX(-1.5deg); opacity: 1.0; }
        100% { transform: translateX(-1px) skewX(1.5deg); opacity: 0.85; }
    }

    @keyframes numen-space-warp {
        0%   { transform: scale(1.00); opacity: 0.7; }
        50%  { transform: scale(1.04); opacity: 1.0; }
        100% { transform: scale(1.00); opacity: 0.7; }
    }

    @keyframes numen-vital-pulse {
        0%   { transform: scale(0.98); opacity: 0.5; }
        50%  { transform: scale(1.05); opacity: 0.95; }
        100% { transform: scale(0.98); opacity: 0.5; }
    }

    @keyframes numen-shadow-breathe {
        0%   { opacity: 0.15; }
        50%  { opacity: 0.45; }
        100% { opacity: 0.15; }
    }

    @keyframes numen-default-glow {
        0%   { opacity: 0.1; }
        50%  { opacity: 0.35; }
        100% { opacity: 0.1; }
    }

    @keyframes numen-weave {
        0%   { background-position: 0 0, 0 0; }
        100% { background-position: 20px 20px, -20px -20px; }
    }

    @keyframes numen-rage-quake {
        0%   { transform: translate(0, -2px); }
        20%  { transform: translate(1px, -3px); }
        40%  { transform: translate(-2px, -1px); }
        60%  { transform: translate(2px, -4px); }
        80%  { transform: translate(-1px, -3px); }
        100% { transform: translate(0, -2px); }
    }

    @keyframes rock-quake-tilt {
        0% { transform: translate(0px, -2px) rotate(0deg); }
        15% { transform: translate(1px, -3px) rotate(-0.4deg); }
        30% { transform: translate(-2px, -1px) rotate(0.3deg); }
        45% { transform: translate(2px, -4px) rotate(-0.5deg); }
        60% { transform: translate(-1px, -3px) rotate(0.2deg); }
        80% { transform: translate(1px, -2px) rotate(-0.3deg); }
        100% { transform: translate(0px, -2px) rotate(0deg); }
    }
    

    @keyframes numen-drip {
        0%   { background-position: 0 0; }
        100% { background-position: 0 20px; }
    }

    @keyframes numen-wave-h {
        0%   { background-position: 0 0; }
        100% { background-position: 40px 0; }
    }

    @keyframes numen-wave-sine {
        0% { background-position: 0px 0px;
            transform: translateY(0px);
            opacity: 0.55;}
        20% {  background-position: 22px -4px;
            transform: translateY(-2px);
            opacity: 0.80; }
        40% {   background-position: 44px 0px;
            transform: translateY(0px);
            opacity: 0.90;  }
        60% {  background-position: 22px 4px;
            transform: translateY(2px);
            opacity: 0.75;  }
        80% { background-position: 0px 0px;
            transform: translateY(0px);
            opacity: 0.60;  }
        100% {  background-position: 0px 0px;
            transform: translateY(0px);
            opacity: 0.55;  }
    }

    
    @keyframes numen-zap {
        0%   { opacity: 0.1; }
        25%  { opacity: 0.4; }
        50%  { opacity: 0.1; }
        75%  { opacity: 0.5; }
        100% { opacity: 0.1; }
    }

    @keyframes numen-spiral {
        0%   { transform: rotate(0deg) scale(0.9); opacity: 0.2; }
        50%  { transform: rotate(180deg) scale(1.05); opacity: 0.6; }
        100% { transform: rotate(360deg) scale(0.9); opacity: 0.2; }
    }

    /* --------- BASE POR DEFECTO PARA CUALQUIER NUMEN --------- */
    details.numen-card-full:hover {
        transform: rotateX(8deg) rotateY(-7deg) translateY(-4px);
        box-shadow: 0 18px 30px rgba(0,0,0,0.75);
    }

    details.numen-card-full::after {
        content: "";
        position: absolute;
        inset: -20%;
        opacity: 0;
        pointer-events: none;
        mix-blend-mode: screen;
        transition: opacity 0.25s ease-out;
    }

    details.numen-card-full:hover::after {
        opacity: 1;
        animation: numen-default-glow 3s linear infinite;
        background:
          radial-gradient(circle at 10% 0%, rgba(255,255,255,0.08), transparent 55%),
          radial-gradient(circle at 90% 100%, rgba(255,255,255,0.05), transparent 60%);
        max-width: 500px;     /* ajusta el ancho a lo que prefieras */
        margin-left: auto;
        margin-right: auto;       
    }

    /* =====================================================
       NUMEN ESPECÍFICOS
       ===================================================== */

    /* IGNIS — chispas / vibración de fuego */
    details.numen-card-full.numen-ignis:hover {
        border-color: #FF4500;
        box-shadow: 0 0 22px #FF4500aa;
    }
    details.numen-card-full.numen-ignis:hover::after {
        animation: numen-fire-flicker 0.9s infinite alternate;
        background:
          radial-gradient(circle at 20% 80%, rgba(255, 200, 150, 0.0) 0, rgba(255, 200, 150, 0.7) 4px, transparent 10px),
          radial-gradient(circle at 65% 50%, rgba(255, 120, 0, 0.0) 0, rgba(255, 120, 0, 0.9) 3px, transparent 9px),          
          radial-gradient(circle at 55% 30%, rgba(255, 120, 0, 0.0) 0, rgba(255, 200, 150, 0.9) 3px, transparent 9px),
          radial-gradient(circle at 85% 20%, rgba(255, 120, 0, 0.0) 0, rgba(255, 120, 0, 0.9) 3px, transparent 9px),
          radial-gradient(circle at 45% 55%, rgba(255, 120, 0, 0.0) 0, rgba(255, 120, 0, 0.9) 3px, transparent 9px),                    
          radial-gradient(circle at 75% 85%, rgba(255, 80, 0, 0.0) 0, rgba(255, 80, 0, 0.8) 3px, transparent 10px);
    }

    /* CRYBORENS — shards de hielo */
    details.numen-card-full.numen-cryoborens:hover {
        border-color: #00CED1;
        box-shadow: 0 0 20px #00CED1aa;
    }
    details.numen-card-full.numen-cryoborens:hover::after {
        animation: numen-ice-shards 1.4s infinite ease-in-out;
        background:
          repeating-linear-gradient(
            -35deg,
            rgba(200, 255, 255, 0.12),
            rgba(200, 255, 255, 0.12) 4px,
            transparent 4px,
            transparent 10px
          );
    }

    /* LIMINIS — warp espacial */
    details.numen-card-full.numen-liminis:hover {
        border-color: #D4AF37;
        box-shadow: 0 0 20px #D4AF37aa;
    }
    details.numen-card-full.numen-liminis:hover::after {
        animation: numen-space-warp 2.4s infinite ease-in-out;
        background:
          radial-gradient(circle at 50% 50%, rgba(212, 175, 55, 0.28), transparent 55%),
          radial-gradient(circle at 50% 50%, rgba(212, 175, 55, 0.18), transparent 75%);
    }

    /* VITALIS — pulso de vida */
    details.numen-card-full.numen-vitalis:hover {
        border-color: #32CD32;
        box-shadow: 0 0 22px #32CD32aa;
    }
    details.numen-card-full.numen-vitalis:hover::after {
        animation: numen-vital-pulse 1.3s infinite ease-in-out;
        background:
          radial-gradient(circle at 50% 50%, rgba(50, 205, 50, 0.35), transparent 60%),
          radial-gradient(circle at 20% 20%, rgba(120, 255, 120, 0.25), transparent 55%);
    }

    /* IGNOTA — velos móviles */
    details.numen-card-full.numen-ignota:hover {
        border-color: #E44192;
        box-shadow: 0 0 20px #E44192aa;
    }
    details.numen-card-full.numen-ignota:hover::after {
        animation: numen-weave 4s linear infinite;
        background:
          repeating-linear-gradient(
            15deg,
            rgba(228, 65, 146, 0.12),
            rgba(228, 65, 146, 0.12) 10px,
            transparent 10px,
            transparent 20px
          ),
          repeating-linear-gradient(
            -25deg,
            rgba(90, 10, 60, 0.25),
            rgba(90, 10, 60, 0.25) 8px,
            transparent 8px,
            transparent 18px
          );
    }

    /* TELLURIS — estratos de roca */
    details.numen-card-full.numen-telluris:hover {
        border-color: #813600;
        box-shadow: 0 0 18px #813600aa;
    }
    details.numen-card-full.numen-telluris:hover::after {
        animation: rock-quake-tilt 2.2s infinite ease-in-out;
        background:
          repeating-linear-gradient(
            90deg,
            rgba(90, 40, 10, 0.35),
            rgba(90, 40, 10, 0.35) 5px,
            rgba(40, 15, 5, 0.2) 5px,
            rgba(40, 15, 5, 0.2) 12px
          );
    }

    /* METALLUM — reflejos metálicos */
    details.numen-card-full.numen-metallum:hover {
        border-color: #0047AB;
        box-shadow: 0 0 22px #0047ABaa;
    }
    details.numen-card-full.numen-metallum:hover::after {
        animation: numen-wave-h 2.8s linear infinite;
        background:
          linear-gradient(
            120deg,
            rgba(200, 220, 255, 0.0) 0%,
            rgba(200, 220, 255, 0.4) 35%,
            rgba(200, 220, 255, 0.0) 70%
          );
        background-size: 200% 100%;
    }

    /* ASTRALIS — destellos estelares */
    details.numen-card-full.numen-astralis:hover {
        border-color: #FCDA90;
        box-shadow: 0 0 22px #FCDA90aa;
    }
    details.numen-card-full.numen-astralis:hover::after {
        animation: numen-default-glow 2.5s ease-in-out infinite;
        background:
          radial-gradient(circle at 10% 20%, rgba(255,255,220,0.6), transparent 55%),
          radial-gradient(circle at 75% 80%, rgba(255,255,180,0.5), transparent 55%),
          radial-gradient(circle at 50% 50%, rgba(255,255,255,0.35), transparent 60%);
    }

    /* HIERATIA — halo sagrado */
    details.numen-card-full.numen-hieratia:hover {
        border-color: #6CA6FF;
        box-shadow: 0 0 22px #6CA6FFaa;
    }
    details.numen-card-full.numen-hieratia:hover::after {
        animation: numen-vital-pulse 2.0s infinite ease-in-out;
        background:
          radial-gradient(circle at 50% 50%, rgba(108,166,255,0.5), transparent 65%),
          radial-gradient(circle at 50% 50%, rgba(180,210,255,0.4), transparent 80%);
    }

    /* UMBRA — respiración de sombras */
    details.numen-card-full.numen-umbra:hover {
        border-color: #2F2F2F;
        box-shadow: 0 0 24px #000000dd;
    }
    details.numen-card-full.numen-umbra:hover::after {
        animation: numen-shadow-breathe 2.8s infinite ease-in-out;
        background:
          radial-gradient(circle at 50% 20%, rgba(31, 31, 31, 0.8), transparent 80%),
          radial-gradient(circle at 10% 90%, rgba(31, 31, 31, 0.6), transparent 65%),
          radial-gradient(circle at 90% 80%, rgba(31, 31, 31, 0.6), transparent 65%);
    }

    /* CHRONENS — tics de reloj */
    details.numen-card-full.numen-chronens:hover {
        border-color: #C0C0C0;
        box-shadow: 0 0 20px #C0C0C0aa;
    }
    details.numen-card-full.numen-chronens:hover::after {
        animation: numen-spiral 6s linear infinite;
        background:
          conic-gradient(
            from 0deg,
            rgba(192,192,192,0.0) 0deg,
            rgba(192,192,192,0.4) 20deg,
            rgba(192,192,192,0.0) 40deg,
            rgba(192,192,192,0.4) 60deg,
            rgba(192,192,192,0.0) 80deg
          );
    }

    /* LIKA — entramado de lazos */
    details.numen-card-full.numen-lika:hover {
        border-color: #FFFFFF;
        box-shadow: 0 0 20px #FFFFFFaa;
    }
    details.numen-card-full.numen-lika:hover::after {
        animation: numen-weave 3.2s linear infinite;
        background:
          repeating-linear-gradient(
            45deg,
            rgba(255,255,255,0.15),
            rgba(255,255,255,0.15) 6px,
            transparent 6px,
            transparent 14px
          ),
          repeating-linear-gradient(
            -45deg,
            rgba(200,200,255,0.1),
            rgba(200,200,255,0.1) 6px,
            transparent 6px,
            transparent 14px
          );
    }

    /* MITAUNA — sacudida de furia */
    details.numen-card-full.numen-mitauna:hover {
        border-color: #FF0000;
        box-shadow: 0 0 24px #FF0000aa;
    }
    details.numen-card-full.numen-mitauna:hover::after {
        animation: numen-rage-quake 0.5s infinite;
        background:
          radial-gradient(circle at 50% 50%, rgba(255,0,0,0.35), transparent 70%);
    }

    /* AHMAR — goteo de sangre */
    details.numen-card-full.numen-ahmar:hover {
        border-color: #B22222;
        box-shadow: 0 0 22px #B22222aa;
    }
    details.numen-card-full.numen-ahmar:hover::after {
        animation: numen-drip 1.8s linear infinite;
        background:
          repeating-linear-gradient(
            180deg,
            rgba(178,34,34,0.4),
            rgba(178,34,34,0.4) 8px,
            transparent 8px,
            transparent 16px
          );
        background-size: 100% 40px;
    }

    /* AETHERIS — ondas de aire */
    details.numen-card-full.numen-aetheris:hover {
        border-color: #68D6B0;
        box-shadow: 0 0 22px #68D6B0aa;
    }
    details.numen-card-full.numen-aetheris:hover::after {
        animation: numen-wave-sine 2.5s linear infinite;
        background:
          repeating-linear-gradient(
            0deg,
            rgba(104,214,176,0.25),
            rgba(104,214,176,0.25) 4px,
            transparent 4px,
            transparent 10px
          );
        background-size: 60px 100%;
    }

    /* RAIZENS — rayos */
    details.numen-card-full.numen-raizens:hover {
        border-color: #FFD700;
        box-shadow: 0 0 24px #FFD700cc;
    }
    details.numen-card-full.numen-raizens:hover::after {
        animation: numen-zap 1.1s linear infinite;
        background:
          repeating-linear-gradient(
            -60deg,
            rgba(255,215,0,0.9),
            rgba(255,215,0,0.9) 2px,
            transparent 2px,
            transparent 10px
          );
    }

    /* AVAZAX — ondas de sonido */
    details.numen-card-full.numen-avazax:hover {
        border-color: #A47DFF;
        box-shadow: 0 0 22px #A47DFFaa;
    }
    details.numen-card-full.numen-avazax:hover::after {
        animation: numen-shadow-breathe 0.8s infinite ease-in-out;
        background:
          radial-gradient(circle at 50% 20%, rgba(164,125,255,0.35), transparent 55%),
          radial-gradient(circle at 10% 90%, rgba(255, 28, 243, 0.61), transparent 55%),
          radial-gradient(circle at 90% 80%, rgba(164,125,255,0.25), transparent 55%);
        background-size: 140% 100%;
    }

    /* MORTIS — neblina venenosa */
    details.numen-card-full.numen-mortis:hover {
        border-color: #00FF80;
        box-shadow: 0 0 24px #00FF80bb;
    }
    details.numen-card-full.numen-mortis:hover::after {
        animation: numen-shadow-breathe 3.5s infinite ease-in-out;
        background:
          radial-gradient(circle at 30% 30%, rgba(0,255,128,0.45), transparent 60%),
          radial-gradient(circle at 70% 70%, rgba(0,180,90,0.35), transparent 70%);
    }

    /* ONIRIANS — ondas oníricas */
    details.numen-card-full.numen-onirians:hover {
        border-color: #5D67C0;
        box-shadow: 0 0 22px #5D67C0aa;
    }
    details.numen-card-full.numen-onirians:hover::after {
        animation: numen-space-warp 3.0s ease-in-out infinite;
        background:
          repeating-radial-gradient(
            circle at 50% 50%,
            rgba(93,103,192,0.3),
            rgba(93,103,192,0.3) 10px,
            transparent 10px,
            transparent 20px
          );
    }

    /* NATURAE — brotes verdes */
    details.numen-card-full.numen-naturae:hover {
        border-color: #ACAF04;
        box-shadow: 0 0 22px #ACAF04aa;
    }
    details.numen-card-full.numen-naturae:hover::after {
        animation: numen-vital-pulse 2.6s infinite ease-in-out;
        background:
          radial-gradient(circle at 20% 80%, rgba(172,175,4,0.45), transparent 60%),
          radial-gradient(circle at 70% 20%, rgba(190,220,70,0.4), transparent 65%);
    }

    /* PSYKONENS — espiral mental */
    details.numen-card-full.numen-psykonens:hover {
        border-color: #7801FF;
        box-shadow: 0 0 24px #7801FFaa;
    }
    details.numen-card-full.numen-psykonens:hover::after {
        animation: numen-space-warp 3.0s ease-in-out infinite;
        background:
          conic-gradient(
            from 0deg,
            rgba(120,1,255,0.0) 0deg,
            rgba(120,1,255,0.5) 60deg,
            rgba(120,1,255,0.0) 120deg,
            rgba(120,1,255,0.5) 180deg,
            rgba(120,1,255,0.0) 240deg,
            rgba(120,1,255,0.5) 300deg,
            rgba(120,1,255,0.0) 360deg
          );
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)





# Colores por categoría de Precepto
PRECEPT_CATEGORY_COLORS = {
    "Elemental": "#ff6b3b",
    "Vital": "#4caf50",
    "Cognitiva": "#a47dff",
    "Pragmática": "#ffc857",
    "Sin categoría": "#666666",
}

def get_precept_color(precept_dict: dict) -> str:
    cat = precept_dict.get("category", "Sin categoría")
    return PRECEPT_CATEGORY_COLORS.get(cat, "#555555")

def render_precept_card(precept_id: str):
    p = PRECEPTS.get(precept_id)
    if not p:
        st.write(f"(Precepto {precept_id} no definido)")
        return

    color = get_precept_color(p)
    cat = p.get("category", "Sin categoría")
    desc = p.get("description", "_Sin descripción_")
    examples = p.get("example_ordinances", [])
    pref_numen = p.get("preferred_numen_ids", [])

    if pref_numen:
        numen_names = [
            NUMEN[nid]["display_name"]
            for nid in pref_numen
            if nid in NUMEN
        ]
        numen_line = ", ".join(numen_names)
    else:
        numen_line = "—"

    examples_html = ""
    if examples:
        items = "".join(f"<li>{e}</li>" for e in examples)
        examples_html = f"<ul>{items}</ul>"

    html = f"""
    <details class="precept-card" style="border-color:{color};background:{color}22;">
      <summary>
        <div class="precept-header-title">{p['verb']}</div>
        <div class="precept-header-sub">{cat}</div>
        <span class="precept-header-tag">Precepto</span>
      </summary>
      <div class="precept-details">
        <p><strong>Descripción:</strong><br>{desc}</p>
        <p><strong>Numen preferentes:</strong> {numen_line}</p>
        {"<p><strong>Ejemplos de ordenanzas:</strong></p>" + examples_html if examples_html else ""}
      </div>
    </details>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_numen_card(nid: str, compact: bool = False):
    """Tarjeta simplificada de Numen con emblema PNG a la derecha (clase original: numen-card)."""
    if nid not in NUMEN:
        st.write(f"(Numen {nid} no definido)")
        return

    n = NUMEN[nid]

    name = n["display_name"]
    tags = ", ".join(n.get("tags", [])) or "—"
    desc_full = n.get("description", "")
    short_desc = (
        n.get("short_description")
        or (desc_full[:70] + "..." if len(desc_full) > 70 else desc_full)
    )

    icon_url = n.get("icon_url", "")

    bg_color = n["color_hex"] + "22"
    border_color = n["color_hex"]
    height = "4.6rem" if compact else "5.6rem"

    slug = f"numen-{nid.lower()}"

    # Emblema (solo si icon_url existe)
    emblem_html = ""
    if icon_url:
        emblem_html = (
            "<div class='numen-emblem-mini'>"
                "<img src='" + icon_url + "' alt='" + name + " emblem'>"
            "</div>"
        )

    html = (
        "<div class='numen-card " + slug + "' "
            "style='background:" + bg_color + "; border-color:" + border_color +
            "; min-height:" + height + "; display:flex; justify-content:space-between; align-items:center;'>"

            "<div class='numen-card-text'>"
                "<span class='numen-card-name'>" + name + "</span>"
                "<span class='numen-card-tags'>" + tags + "</span>"
                "<span class='numen-card-desc'>" + short_desc + "</span>"
            "</div>"

            + emblem_html +

        "</div>"
    )

    st.markdown(html, unsafe_allow_html=True)



def render_numen_full_card(nid: str):
    n = NUMEN.get(nid)
    if not n:
        st.write(f"(Numen {nid} no definido)")
        return

    color = n.get("color_hex", "#FFFFFF")
    bg = color + "22"
    name = n["display_name"]
    base_name = n["name"]
    tags = ", ".join(n.get("tags", [])) or "—"
    desc = n.get("description", "_Sin descripción_")

    slug = f"numen-{nid.lower()}"  # ej. numen-ignis

    icon_url = n.get("icon_url") or ""
    if icon_url:
        emblem_html = (
            '<div class="numen-emblem">'
            '<img src="' + icon_url + '" alt="' + name + ' icon" />'
            '</div>'
        )
    else:
        emblem_html = ""

    html = (
        '<details class="numen-card-full ' + slug + '" '
        'style="border-color:' + color + ';background:' + bg + ';">'
        '<summary>'
        '<div class="numen-3d-inner">'
        + emblem_html +
        '<div class="numen-header-block">'
        '<div class="numen-header-title">' + name + '</div>'
        '<div class="numen-header-sub">' + base_name + '</div>'
        '<div class="numen-header-tags">' + tags + '</div>'
        '</div>'
        '</div>'
        '</summary>'
        '<div class="numen-details">'
        '<p><strong>Descripción:</strong><br>' + desc + '</p>'
        '</div>'
        '</details>'
    )

    st.markdown(html, unsafe_allow_html=True)





def render_animated_ordinance_card(o, effect_type: str, mechanics_summary: str):
    if o.numen_ids:
        primary = NUMEN.get(o.numen_ids[0], {})
        bg_color = primary.get("color_hex", "#FFFFFF") + "22"
        numen_label = ", ".join(
            NUMEN.get(nid, {}).get("display_name", nid) for nid in o.numen_ids
        )
    else:
        bg_color = "rgba(80,80,80,0.3)"
        numen_label = "Sin Numen"

    precept_name = PRECEPTS.get(o.precept_id, {}).get("verb", o.precept_id)

    border_class = {
        "damage": "ordinance-border-damage",
        "heal": "ordinance-border-heal",
        "control": "ordinance-border-control",
        "utility": "ordinance-border-utility",
    }.get(effect_type, "ordinance-border-utility")

    effect_label = {
        "damage": "Daño",
        "heal": "Curación",
        "control": "Control",
        "utility": "Utilidad",
    }.get(effect_type, "Utilidad")

    # Modificadores en texto
    if o.modifiers:
        mods_lines = []
        for sel in o.modifiers:
            m = MODIFIERS.get(sel.modifier_id, {})
            name = m.get("name", sel.modifier_id)
            extra = []
            if sel.rank != 1:
                extra.append(f"rango {sel.rank}")
            if sel.extra_instances > 0:
                extra.append(f"+{sel.extra_instances} instancias")
            extra_str = f" ({', '.join(extra)})" if extra else ""
            mods_lines.append(f"• {name}{extra_str}")
        mods_text = "<br>".join(mods_lines)
    else:
        mods_text = "• Ningún modificador aplicado."

    mech_saved = o.mechanical or {}
    narrative = mech_saved.get("narrative", "")
    notes = mech_saved.get("notes", "")

    html = f"""
    <details class="ordinance-card {border_class}" style="background:{bg_color};">
      <summary>
        <div class="ordinance-header-title">{o.name}</div>
        <div class="ordinance-header-sub">
            Precepto: {precept_name} · Numen: {numen_label} · Tier {o.tier}
        </div>
        <div class="ordinance-header-tag">{effect_label}</div>
      </summary>
      <div class="ordinance-details">
        <p><strong>Sugerencia mecánica (actual):</strong><br>{mechanics_summary}</p>
        <p><strong>Efecto narrativo guardado:</strong><br>{narrative or '<em>Sin texto narrativo guardado.</em>'}</p>
        {"<p><em>Notas:</em> " + notes + "</p>" if notes else ""}
        <p><strong>Modificadores:</strong><br>{mods_text}</p>
        <p><strong>Coste:</strong><br>
           Complejidad: {o.cost.get('complexity_points', '—')} · Tier: {o.cost.get('tier', o.tier)}
        </p>
      </div>
    </details>
    """
    st.markdown(html, unsafe_allow_html=True)



inject_global_css()
inject_numen_effects_css()






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

            ordered_pids = sorted(
                filtered_ids,
                key=lambda pid: PRECEPTS[pid]["verb"].lower()
            )

            for pid in ordered_pids:
                render_precept_card(pid)


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

            ordered_ids = sorted(
                filtered_ids,
                key=lambda nid: NUMEN[nid]["display_name"].lower()
            )

            # Si quieres en columnas, mantenemos 2–3 columnas; o una sola columna si las prefieres grandes
            cols = st.columns(3)
            for i, nid in enumerate(ordered_ids):
                col = cols[i % 3]
                with col:
                    render_numen_full_card(nid)




    st.stop()

# ===================================================================
# MODO: EXPLORADOR DE MODIFICADORES
# ===================================================================
if mode == "Explorador de Modificadores":
    st.header("Explorador de Modificadores")

    # Familias dinámicas
    families = sorted({m["family"] for m in MODIFIERS.values()})
    families.insert(0, "Todas")

    col_filters = st.columns([2, 3])
    with col_filters[0]:
        fam_filter = st.selectbox(
            "Filtrar por familia:",
            options=families,
            index=0,
        )
    with col_filters[1]:
        search_text = st.text_input(
            "Buscar por nombre o descripción:",
            value="",
            placeholder="Ej: Cono, Persistente, Ofensivo...",
        ).lower().strip()

    # Qué familias mostramos
    if fam_filter == "Todas":
        fams_to_show = sorted({m["family"] for m in MODIFIERS.values()})
    else:
        fams_to_show = [fam_filter]

    total_mods = 0

    for fam in fams_to_show:
        # Todos los mods de esa familia
        fam_mods = [
            (mid, m)
            for mid, m in MODIFIERS.items()
            if m["family"] == fam
        ]

        # Filtro por texto
        if search_text:
            fam_mods = [
                (mid, m)
                for mid, m in fam_mods
                if search_text in m["name"].lower()
                or search_text in m.get("description", "").lower()
            ]

        if not fam_mods:
            continue

        total_mods += len(fam_mods)
        st.markdown(f"### Familia: {fam}")

        # Ordenar por nombre
        fam_mods_sorted = sorted(fam_mods, key=lambda x: x[1]["name"].lower())
        options = [mid for mid, _ in fam_mods_sorted]

        # 🔄 Nuevo selector: selectbox en vez de select_slider
        selected_mid = st.selectbox(
            "Elige un modificador de esta familia:",
            options=options,
            format_func=lambda mid: MODIFIERS[mid]["name"],
            key=f"selector_{fam}",
        )

        sel_mod = MODIFIERS[selected_mid]

        # Card visual (usa la CSS de .modifier-card que ya tienes)
        st.markdown(
            f"""
            <div class="modifier-card">
                <div class="modifier-card-title">{sel_mod['name']}</div>
                <div class="modifier-card-sub">Familia: {sel_mod['family']}</div>
                <div style="font-size:0.85rem;margin-top:0.2rem;">
                    {sel_mod.get("description", "_Sin descripción_")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Costes legibles
        cost_parts = []
        base_cost = sel_mod.get("base_cost")
        if base_cost is not None:
            cost_parts.append(f"- Coste base: **{base_cost}**")

        rank_cost = sel_mod.get("rank_cost")
        if rank_cost is not None:
            cost_parts.append(f"- Coste por rango: **+{rank_cost}**")

        extra_long = sel_mod.get("extra_long_duration_cost")
        if extra_long is not None:
            cost_parts.append(f"- Extra por duración larga: **+{extra_long}**")

        per_inst = sel_mod.get("per_extra_instance_cost")
        if per_inst is not None:
            cost_parts.append(f"- Coste por instancia adicional: **+{per_inst}**")

        mod_total = sel_mod.get("cost_modifier_total")
        if mod_total is not None:
            cost_parts.append(f"- Modificador total al coste: **{mod_total:+}**")

        st.markdown("**Coste (modelo actual):**")
        if cost_parts:
            st.markdown("\n".join(cost_parts))
        else:
            st.markdown("- Sin costes específicos definidos.")

        st.markdown("**Tags:** " + (", ".join(sel_mod.get("tags", [])) or "—"))
        st.markdown("---")

    if total_mods == 0:
        st.info("No se han encontrado modificadores con esos filtros.")
    else:
        st.caption(f"Mostrando {total_mods} modificadores en total.")

    st.stop()



# ===================================================================
# MODO: GRIMORIO DE ORDENANZAS
# ===================================================================
if mode == "Grimorio de Ordenanzas":
    st.header("Grimorio de Ordenanzas")

    if not ORDINANCES:
        st.info("Aún no hay Ordenanzas registradas. Usa el Constructor para crear algunas.")
        st.stop()

    # Filtros: Tipo, Numen, Precepto, Tier, texto
    all_numen_ids = sorted({nid for o in ORDINANCES.values() for nid in o.numen_ids})
    all_precepts = sorted({o.precept_id for o in ORDINANCES.values()})
    all_tiers = sorted({o.tier for o in ORDINANCES.values()})

    EFFECT_FILTER_LABELS = {
        "Todas 🟦": None,
        "🟥 Daño": "damage",
        "🟩 Curación": "heal",
        "🟨 Control": "control",
        "🟪 Utilidad": "utility",
    }

    col_filters = st.columns(5)
    with col_filters[0]:
        effect_label = st.selectbox(
            "Tipo de ordenanza:",
            options=list(EFFECT_FILTER_LABELS.keys()),
            index=0,
        )
        effect_filter = EFFECT_FILTER_LABELS[effect_label]

    with col_filters[1]:
        numen_filter = st.multiselect(
            "Filtrar por Numen:",
            options=all_numen_ids,
            format_func=lambda nid: NUMEN.get(nid, {}).get("display_name", nid),
        )
    with col_filters[2]:
        precept_filter = st.multiselect(
            "Filtrar por Precepto:",
            options=all_precepts,
            format_func=lambda pid: PRECEPTS.get(pid, {}).get("verb", pid),
        )
    with col_filters[3]:
        tier_filter = st.multiselect(
            "Filtrar por Tier:",
            options=all_tiers,
            default=all_tiers,
        )
    with col_filters[4]:
        search_text = st.text_input(
            "Buscar por nombre:",
            value="",
            placeholder="Ej: Llama Voraz...",
        ).lower()


    # Aplicar filtros + tipo de ordenanza
    filtered = []
    for o in ORDINANCES.values():
        if numen_filter and not any(n in o.numen_ids for n in numen_filter):
            continue
        if precept_filter and o.precept_id not in precept_filter:
            continue
        if tier_filter and o.tier not in tier_filter:
            continue
        if search_text and search_text not in o.name.lower():
            continue

        # Tipo de ordenanza a partir de la sugerencia mecánica
        long_duration_flag = any(
            sel.modifier_id == "DURACION_PERSISTENTE" for sel in o.modifiers
        )
        complexity_o = calculate_complexity(
            precept_id=o.precept_id,
            numen_ids=o.numen_ids,
            modifiers=o.modifiers,
            long_duration=long_duration_flag,
        )
        mech = suggest_mechanics(
            precept_id=o.precept_id,
            numen_ids=o.numen_ids,
            modifiers=o.modifiers,
            complexity=complexity_o,
            long_duration=long_duration_flag,
        )
        effect_type = mech.get("type", "utility")

        if effect_filter and effect_type != effect_filter:
            continue

        filtered.append((o, effect_type, mech))

    st.write(f"Se han encontrado **{len(filtered)}** Ordenanzas.")

    # Ordenar por tier y nombre
    filtered.sort(key=lambda tup: (tup[0].tier, tup[0].name.lower()))

    for o, effect_type, mech in filtered:
        summary = mech.get("summary", "")
        render_animated_ordinance_card(o, effect_type, summary)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Exportar")
    
    st.sidebar.download_button(
        label="⬇️ Descargar grimorio (JSON)",
        data=export_ordinances_json_bytes(ORDINANCES),
        file_name="arcana_ordinances_export.json",
        mime="application/json",
    )





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
p_color = get_precept_color(precept)

st.header("Constructor de Ordenanzas")
st.markdown(
    f"""
    <div class="precept-card" style="border-color:{p_color};background:{p_color}22;">
        <div class="precept-card-title">Precepto seleccionado: {precept['verb']}</div>
        <div class="precept-card-sub">{precept.get('category', 'Sin categoría')}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(precept.get("description", "_Sin descripción definida._"))





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
    with col:
        render_numen_card(nid, compact=True)


# --- 3) Select Modifiers ---
st.sidebar.header("3. Modificadores")

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
# --- Condicionales adicionales si la intención es Condicional ---
has_conditional_intent = any(
    sel.modifier_id == "INTENCION_CONDICIONAL" for sel in selected_modifiers
)

if has_conditional_intent:
    cond_mods = {
        mid: m
        for mid, m in MODIFIERS.items()
        if m.get("family") == "CONDICION"
    }

    if cond_mods:
        st.sidebar.markdown("**Condiciones de activación**")
        chosen_conds = st.sidebar.multiselect(
            "Selecciona una o más condiciones:",
            options=list(cond_mods.keys()),
            format_func=lambda mid: cond_mods[mid]["name"],
            key="ms_CONDICION",
        )

        for mid in chosen_conds:
            # Evita duplicar si en el futuro las condiciones se seleccionan por otro lado
            if any(sel.modifier_id == mid for sel in selected_modifiers):
                continue

            selected_modifiers.append(
                ModifierSelection(
                    modifier_id=mid,
                    rank=1,
                    extra_instances=0,
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





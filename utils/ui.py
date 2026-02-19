"""
utils/ui.py
Componentes visuales reutilizables para Surtidora Departamental PoC
"""

import streamlit as st

SD_COLORS = {
    "primary":   "#2BBAB4",   # turquesa/teal SD
    "accent":    "#229E99",   # turquesa oscuro
    "light":     "#B2EDED",   # turquesa claro
    "warning":   "#F4A261",   # naranja
    "danger":    "#E63946",   # rojo
    "success":   "#2DC653",   # verde éxito
    "neutral":   "#F8F9FA",
    "dark":      "#2D2D2D",   # gris oscuro (logo SD)
    "muted":     "#6C757D",
}

def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .main {{ background-color: #F2F5F5; }}

    /* Header de página */
    .page-header {{
        background: linear-gradient(135deg, {SD_COLORS["dark"]} 0%, {SD_COLORS["primary"]} 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
    }}
    .page-header h1 {{ color: white; font-size: 1.8rem; font-weight: 700; margin: 0; }}
    .page-header p  {{ color: rgba(255,255,255,0.85); margin: 0.25rem 0 0; font-size: 0.95rem; }}

    /* KPI Cards */
    .kpi-card {{
        background: white;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        border-left: 4px solid {SD_COLORS["primary"]};
        box-shadow: 0 1px 8px rgba(0,0,0,0.06);
    }}
    .kpi-label  {{ font-size: 0.78rem; color: {SD_COLORS["muted"]}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }}
    .kpi-value  {{ font-size: 1.9rem; font-weight: 700; color: {SD_COLORS["dark"]}; line-height: 1.1; }}
    .kpi-delta  {{ font-size: 0.82rem; color: {SD_COLORS["muted"]}; margin-top: 0.2rem; }}
    .kpi-danger {{ border-left-color: {SD_COLORS["danger"]}; }}
    .kpi-warn   {{ border-left-color: {SD_COLORS["warning"]}; }}
    .kpi-success{{ border-left-color: {SD_COLORS["success"]}; }}

    /* Alerta Cards */
    .alerta-critica {{
        background: white;
        border: 1.5px solid {SD_COLORS["danger"]};
        border-left: 6px solid {SD_COLORS["danger"]};
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 12px rgba(230,57,70,0.10);
    }}
    .alerta-warning {{
        background: white;
        border: 1.5px solid {SD_COLORS["warning"]};
        border-left: 6px solid {SD_COLORS["warning"]};
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 12px rgba(244,162,97,0.10);
    }}
    .alerta-info {{
        background: white;
        border: 1.5px solid {SD_COLORS["primary"]};
        border-left: 6px solid {SD_COLORS["primary"]};
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 12px rgba(43,186,180,0.10);
    }}

    .alerta-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.6rem;
    }}
    .badge-red   {{ background: #FEE2E2; color: {SD_COLORS["danger"]}; }}
    .badge-orange{{ background: #FEF3C7; color: #92400E; }}
    .badge-green {{ background: #D1FAE5; color: #065F46; }}

    .alerta-titulo {{ font-size: 1.05rem; font-weight: 700; color: {SD_COLORS["dark"]}; margin-bottom: 0.4rem; }}
    .alerta-desc   {{ font-size: 0.88rem; color: #4B5563; line-height: 1.5; }}
    .alerta-impacto{{
        background: #F9FAFB;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-top: 0.75rem;
        font-size: 0.85rem;
        color: {SD_COLORS["dark"]};
    }}
    .impacto-num {{ font-size: 1.3rem; font-weight: 700; }}

    /* Tabla de datos */
    .data-table {{
        font-size: 0.85rem;
        width: 100%;
        border-collapse: collapse;
    }}
    .data-table th {{
        background: {SD_COLORS["dark"]};
        color: white;
        padding: 0.6rem 0.9rem;
        text-align: left;
        font-weight: 600;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    .data-table td {{
        padding: 0.55rem 0.9rem;
        border-bottom: 1px solid #E5E7EB;
        color: #374151;
    }}
    .data-table tr:hover td {{ background: #F9FAFB; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {SD_COLORS["dark"]};
    }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    [data-testid="stSidebar"] .stSelectbox label {{ color: rgba(255,255,255,0.7) !important; font-size: 0.8rem; }}

    /* Botones */
    .stButton > button {{
        background: {SD_COLORS["primary"]};
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
        transition: all 0.2s;
    }}
    .stButton > button:hover {{
        background: {SD_COLORS["accent"]};
        transform: translateY(-1px);
    }}

    /* Chat input */
    .stChatInput input {{
        border-radius: 12px !important;
        border: 1.5px solid {SD_COLORS["primary"]} !important;
    }}

    /* Divider */
    hr {{ border-color: #E5E7EB; margin: 1.5rem 0; }}

    /* Métricas nativas de streamlit — override */
    [data-testid="metric-container"] {{
        background: white;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    }}
    </style>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="page-header">
        <h1>{title}</h1>
        {"<p>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)


def kpi_card(label: str, value: str, delta: str = "", tipo: str = ""):
    tipo_class = {"danger": "kpi-danger", "warn": "kpi-warn", "success": "kpi-success"}.get(tipo, "")
    st.markdown(f"""
    <div class="kpi-card {tipo_class}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {"<div class='kpi-delta'>" + delta + "</div>" if delta else ""}
    </div>
    """, unsafe_allow_html=True)


def alerta_card(tipo: str, badge: str, titulo: str, desc: str, impacto_label: str, impacto_valor: str, badge_class: str = "badge-red"):
    clase = {"critica": "alerta-critica", "warning": "alerta-warning", "info": "alerta-info"}.get(tipo, "alerta-info")
    st.markdown(f"""
    <div class="{clase}">
        <span class="alerta-badge {badge_class}">{badge}</span>
        <div class="alerta-titulo">{titulo}</div>
        <div class="alerta-desc">{desc}</div>
        <div class="alerta-impacto">
            {impacto_label}: <span class="impacto-num">{impacto_valor}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def fmt_mxn(valor: float, decimales: int = 0) -> str:
    if valor >= 1_000_000:
        return f"${valor/1_000_000:.1f}M MXN"
    elif valor >= 1_000:
        return f"${valor/1_000:.0f}K MXN"
    else:
        return f"${valor:,.{decimales}f} MXN"

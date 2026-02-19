"""
app.py — Surtidora Departamental BI + IA PoC
Home: Resumen Ejecutivo
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils.data_loader import load_all, get_kpis
from utils.ui import inject_css, page_header, kpi_card, fmt_mxn

st.set_page_config(
    page_title="SD | BI + IA",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏪 Surtidora Departamental")
    st.markdown("---")
    st.markdown("**PoC — BI + Inteligencia Artificial**")
    st.caption("Inteligencia real para tus datos")
    st.markdown("---")
    st.markdown("**Navegación**")
    st.markdown("Usa el menú de páginas ↑")
    st.markdown("---")
    st.caption("Período: Ene 2023 – Dic 2024")
    st.caption("v1.0 | Datos sintéticos")

# ── Header ─────────────────────────────────────────────────────────────
page_header(
    "Resumen Ejecutivo — Surtidora Departamental",
    "Vista consolidada del negocio · 2023 – 2024"
)

ventas, clientes, productos, inventario, compras, rent_cli, abc_skus, perdidas = load_all()
kpis = get_kpis()

# ── KPIs Fila 1 ────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Venta Total 2 años", fmt_mxn(kpis["venta_total"]), "Todas las tiendas y canales")
with c2:
    kpi_card("Margen Bruto", f"{kpis['margen_pct']:.1f}%", fmt_mxn(kpis["margen_total"]), tipo="success")
with c3:
    kpi_card("Venta Perdida (quiebres)", fmt_mxn(kpis["venta_perdida"]), "Producto no disponible en demanda alta", tipo="danger")
with c4:
    kpi_card("Margen Perdido", fmt_mxn(kpis["margen_perdido"]), "Impacto directo en rentabilidad", tipo="danger")

st.markdown("<br>", unsafe_allow_html=True)

# ── KPIs Fila 2 ────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Puntos de Venta", str(len(clientes)), f"{len(rent_cli[rent_cli['segmento']=='A'])} Segmento A")
with c2:
    kpi_card("SKUs en Catálogo", str(len(productos)), f"{kpis['skus_a']} SKUs clase A (80% del margen)")
with c3:
    n_canales = clientes["canal"].nunique()
    kpi_card("Canales de Venta", str(n_canales), "Tienda Física · E-commerce · Crédito SD")
with c4:
    kpi_card("Unidades Vendidas", f"{kpis['unidades_vendidas']:,}", "En el período 2023-2024")

st.markdown("---")

# ── Gráficas ──────────────────────────────────────────────────────────
left, right = st.columns([3, 2])

with left:
    st.markdown("#### 📈 Venta Mensual por Canal")
    ventas = ventas.copy()
    ventas.loc[:, "mes"] = ventas["fecha"].dt.to_period("M").astype(str)

    canal_map = {
        "Tienda Física": "Tienda Física",
        "E-commerce":    "E-commerce",
        "Marketplace":   "Marketplace",
        "Crédito SD":    "Crédito SD",
        "Kuesky Pay":    "Financiamiento",
        "Aplazo":        "Financiamiento",
        "Mayoreo":       "Mayoreo",
    }
    v2 = ventas.merge(clientes[["cliente_id","canal"]], on="cliente_id")
    v2.loc[:, "canal_grupo"] = v2["canal"].map(canal_map).fillna("Otro")

    venta_mes = v2.groupby(["mes","canal_grupo"])["monto_total_mxn"].sum().reset_index()
    fig = px.bar(
        venta_mes, x="mes", y="monto_total_mxn", color="canal_grupo",
        color_discrete_sequence=["#2BBAB4","#229E99","#F4A261","#E63946","#B2EDED","#6C757D"],
        labels={"monto_total_mxn": "Venta MXN", "mes": "", "canal_grupo": "Canal"},
    )
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis=dict(tickangle=45, tickfont=dict(size=10)),
        margin=dict(l=0, r=0, t=30, b=0),
        height=320,
        yaxis=dict(tickformat=",.0f"),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#F3F4F6")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("#### 🍩 Margen por Canal")
    margen_canal = v2.groupby("canal_grupo").agg(
        margen=("margen_bruto_mxn","sum"),
        venta=("monto_total_mxn","sum"),
    ).reset_index()
    margen_canal.loc[:, "margen_pct"] = (margen_canal["margen"] / margen_canal["venta"] * 100).round(1)
    margen_canal = margen_canal.sort_values("margen", ascending=False)

    fig2 = px.pie(
        margen_canal, values="margen", names="canal_grupo",
        color_discrete_sequence=["#2BBAB4","#229E99","#40C9C3","#74D8D4","#A3E6E3","#B2EDED"],
        hole=0.55,
    )
    fig2.update_traces(textposition="outside", textinfo="percent+label")
    fig2.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20),
        height=320,
        paper_bgcolor="white",
    )
    fig2.add_annotation(
        text=f"{fmt_mxn(kpis['margen_total'])}<br><span style='font-size:11px'>Margen Total</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=13, color="#2D2D2D"),
        align="center",
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Tabla: Top 10 puntos de venta ──────────────────────────────────────
st.markdown("---")
st.markdown("#### 🏆 Top 10 Puntos de Venta — Volumen vs Margen Real")
st.caption("⚠️ Las tiendas de mayor volumen no siempre son las más rentables")

top10 = rent_cli.head(10)[["nombre","canal","segmento","venta_total_mxn","margen_total_mxn","margen_pct_real","descuento_promedio","ticket_promedio"]].copy()
top10.loc[:, "venta_total_mxn"] = top10["venta_total_mxn"].apply(lambda x: f"${x/1e6:.1f}M")
top10.loc[:, "margen_total_mxn"] = top10["margen_total_mxn"].apply(lambda x: f"${x/1e6:.1f}M")
top10.loc[:, "margen_pct_real"]  = top10["margen_pct_real"].apply(lambda x: f"{x:.1f}%")
top10.loc[:, "descuento_promedio"]= top10["descuento_promedio"].apply(lambda x: f"{x:.1f}%")
top10.loc[:, "ticket_promedio"]   = top10["ticket_promedio"].apply(lambda x: f"${x:,.0f}")
top10.columns = ["Punto de Venta","Canal","Seg.","Venta Total","Margen $","Margen %","Desc. Prom.","Ticket Prom."]

st.dataframe(top10, use_container_width=True, height=380)

# ── Footer insight ─────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    n_skus_a = kpis["skus_a"]
    n_skus_t = kpis["skus_total"]
    st.info(f"📦 **Regla 80/20 validada:** Solo {n_skus_a} de {n_skus_t} SKUs generan el 80% del margen. El resto inmoviliza capital sin retorno proporcional.")
with col2:
    pct = kpis["venta_perdida"] / (kpis["venta_total"] + kpis["venta_perdida"]) * 100
    st.error(f"💸 **Oportunidad oculta:** Se perdieron {fmt_mxn(kpis['venta_perdida'])} en ventas por quiebres de stock en temporadas clave — el {pct:.1f}% del potencial real del negocio.")

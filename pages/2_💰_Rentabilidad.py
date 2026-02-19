"""
pages/2_💰_Rentabilidad.py
Análisis profundo de rentabilidad por punto de venta, canal y categoría
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import load_all
from utils.ui import inject_css, page_header, fmt_mxn

st.set_page_config(page_title="Rentabilidad | SD", page_icon="💰", layout="wide")
inject_css()

with st.sidebar:
    st.markdown("### 🏪 Surtidora Departamental")
    st.markdown("---")
    st.markdown("**Filtros**")

ventas, clientes, productos, inventario, compras, rent_cli, abc_skus, perdidas = load_all()

page_header("💰 Rentabilidad por Canal y Categoría", "El dato que nadie había calculado: margen real después de descuentos y comisiones")

# ─ Filtros ─────────────────────────────────────────────────────────────
with st.sidebar:
    canales_disponibles = ["Todos"] + sorted(rent_cli["canal"].dropna().unique().tolist())
    filtro_canal = st.selectbox("Canal", canales_disponibles)
    segmentos    = st.multiselect("Segmento", ["A","B","C"], default=["A","B","C"])
    regiones_disp = ["Todas"] + sorted(clientes["region"].unique().tolist())
    filtro_region = st.selectbox("Región", regiones_disp)

# Aplicar filtros
df = rent_cli.merge(clientes[["cliente_id","ejecutivo","region"]], on="cliente_id", how="left")
if filtro_canal != "Todos":
    df = df[df["canal"] == filtro_canal]
if segmentos:
    df = df[df["segmento"].isin(segmentos)]
if filtro_region != "Todas":
    df = df[df["region"] == filtro_region]

# ─ KPIs filtrados ──────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Puntos de venta en vista",  f"{len(df)}")
c2.metric("Venta total",               fmt_mxn(df["venta_total_mxn"].sum()))
c3.metric("Margen promedio",            f"{df['margen_pct_real'].mean():.1f}%")
c4.metric("Descuento promedio",         f"{df['descuento_promedio'].mean():.1f}%")

st.markdown("---")

# ─ Gráfica Principal: Margen por Canal ─────────────────────────────────
left, right = st.columns([3, 2])

with left:
    st.markdown("#### Margen Real por Canal")
    st.caption("El margen de lista vs. el margen neto después de descuentos y comisiones de financiamiento")

    margen_canal = df.groupby("canal").agg(
        venta=("venta_total_mxn","sum"),
        margen_pct=("margen_pct_real","mean"),
        descuento=("descuento_promedio","mean"),
        n_clientes=("cliente_id","nunique"),
    ).reset_index().sort_values("margen_pct", ascending=True)

    margen_canal["margen_lista"] = 40.0
    margen_canal["erosion"] = margen_canal["margen_lista"] - margen_canal["margen_pct"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Margen Real", x=margen_canal["canal"], y=margen_canal["margen_pct"],
        marker_color="#2BBAB4", text=margen_canal["margen_pct"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name="Erosión por Descuentos", x=margen_canal["canal"], y=margen_canal["erosion"],
        marker_color="#FCA5A5", text=margen_canal["erosion"].apply(lambda x: f"-{x:.1f}%"),
        textposition="outside",
    ))
    fig.update_layout(
        barmode="stack", height=350, paper_bgcolor="white", plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis=dict(tickangle=25),
        yaxis=dict(title="Margen %", showgrid=True, gridcolor="#F3F4F6"),
        margin=dict(l=0, r=0, t=30, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("#### Rentabilidad vs. Descuento")
    st.caption("Cada punto es un punto de venta. Los más rentables están arriba a la izquierda.")

    fig2 = px.scatter(
        df, x="descuento_promedio", y="margen_pct_real",
        size="venta_total_mxn", color="segmento",
        hover_name="nombre",
        color_discrete_map={"A": "#2BBAB4", "B": "#229E99", "C": "#B2EDED"},
        labels={"descuento_promedio": "Descuento Prom. %", "margen_pct_real": "Margen %", "segmento": "Segmento"},
    )
    fig2.update_layout(
        height=350, paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#F3F4F6"),
        yaxis=dict(showgrid=True, gridcolor="#F3F4F6"),
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig2, use_container_width=True)

# ─ Tabla detallada ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown("#### Detalle por Punto de Venta")

tabla = df[["nombre","canal","segmento","ejecutivo","venta_total_mxn","margen_total_mxn","margen_pct_real","descuento_promedio","ticket_promedio","pedidos","skus_distintos"]].copy()
tabla["venta_total_mxn"]   = tabla["venta_total_mxn"].apply(lambda x: f"${x/1e6:.2f}M")
tabla["margen_total_mxn"]  = tabla["margen_total_mxn"].apply(lambda x: f"${x/1e6:.2f}M")
tabla["margen_pct_real"]   = tabla["margen_pct_real"].apply(lambda x: f"{x:.1f}%")
tabla["descuento_promedio"]= tabla["descuento_promedio"].apply(lambda x: f"{x:.1f}%")
tabla["ticket_promedio"]   = tabla["ticket_promedio"].apply(lambda x: f"${x:,.0f}")
tabla.columns = ["Punto de Venta","Canal","Seg","Responsable","Venta","Margen $","Margen %","Desc%","Ticket","Pedidos","SKUs"]

st.dataframe(tabla.reset_index(drop=True), use_container_width=True, height=420)

# ─ Rentabilidad por Región ─────────────────────────────────────────────
st.markdown("---")
st.markdown("#### 📍 Rentabilidad por Región")

rent_region = df.groupby("region").agg(
    venta=("venta_total_mxn","sum"),
    margen=("margen_total_mxn","sum"),
    margen_pct=("margen_pct_real","mean"),
    n_puntos=("cliente_id","nunique"),
    desc_prom=("descuento_promedio","mean"),
).reset_index().sort_values("margen", ascending=False)
rent_region["margen_pct"] = rent_region["margen_pct"].round(1)

fig3 = px.bar(
    rent_region, x="region", y="margen",
    color="margen_pct",
    color_continuous_scale=["#FEE2E2","#FCA5A5","#2BBAB4","#229E99"],
    text=rent_region["margen"].apply(lambda x: fmt_mxn(x)),
    labels={"region":"Región","margen":"Margen Total MXN","margen_pct":"Margen %"},
)
fig3.update_traces(textposition="outside")
fig3.update_layout(
    height=320, paper_bgcolor="white", plot_bgcolor="white",
    coloraxis_showscale=True,
    yaxis=dict(tickformat=",.0f", showgrid=True, gridcolor="#F3F4F6"),
    margin=dict(l=0, r=0, t=20, b=0),
)
st.plotly_chart(fig3, use_container_width=True)

st.info("💡 **Insight IA:** Los canales con mayor volumen no siempre tienen mayor margen. Marketplace y financiamiento terceros (Kuesky, Aplazo) erosionan el margen por comisiones y descuentos agresivos. Considera vincular promociones a la rentabilidad real por canal.")

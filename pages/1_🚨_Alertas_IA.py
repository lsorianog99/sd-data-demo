"""
pages/1_🚨_Alertas_IA.py
El centerpiece de la PoC: 3 alertas inteligentes generadas por la IA
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import load_all, get_alertas
from utils.ui import inject_css, page_header, fmt_mxn

st.set_page_config(page_title="Alertas IA | SD", page_icon="🚨", layout="wide")
inject_css()

with st.sidebar:
    st.markdown("### 🏪 Surtidora Departamental")
    st.markdown("---")
    st.caption("Alertas generadas automáticamente\npor modelos de IA sobre datos reales.")
    st.markdown("---")
    st.caption("Actualizado: hace 2 horas")

page_header(
    "🚨 Centro de Alertas — Inteligencia Artificial",
    "La IA analizó 65,765 transacciones y detectó 3 situaciones críticas que requieren acción hoy"
)

alertas = get_alertas()
ventas, clientes, productos, inventario, compras, rent_cli, abc_skus, perdidas = load_all()

# ══════════════════════════════════════════════
# ALERTA 1 — QUIEBRE DE STOCK INMINENTE
# ══════════════════════════════════════════════
st.markdown("---")

col_badge, col_empty = st.columns([1, 5])
with col_badge:
    st.markdown('<span style="background:#FEE2E2;color:#E63946;padding:6px 16px;border-radius:20px;font-weight:700;font-size:0.8rem;letter-spacing:0.05em">🔴 CRÍTICO</span>', unsafe_allow_html=True)

st.markdown("### Alerta 1 — Riesgo de Quiebre de Stock en Productos de Alta Demanda")

left, right = st.columns([3, 2])

with left:
    riesgo = alertas["quiebre"]

    if len(riesgo) > 0:
        for _, row in riesgo.iterrows():
            prod = productos[productos["sku"] == row["sku"]]
            nombre = prod["nombre"].values[0] if len(prod) > 0 else row["sku"]
            dias   = row["dias_inventario"]
            venta_r= row.get("venta_en_riesgo", 0)

            color = "#E63946" if dias < 7 else "#F4A261"
            icon  = "🔴" if dias < 7 else "🟠"

            st.markdown(f"""
            <div style="background:white;border-left:5px solid {color};border-radius:10px;
                        padding:1rem 1.2rem;margin-bottom:0.75rem;box-shadow:0 1px 6px rgba(0,0,0,0.07)">
                <div style="font-weight:700;font-size:0.95rem;color:#1F2937">{icon} {nombre}</div>
                <div style="font-size:0.85rem;color:#6B7280;margin-top:0.25rem">
                    Stock actual: <b>{row['stock_cajas']:.0f} unidades</b> · 
                    Demanda semanal: <b>{row['demanda_semana']:.0f} uds</b> · 
                    <span style="color:{color};font-weight:700">⏳ {dias:.0f} días de inventario</span>
                </div>
                <div style="margin-top:0.6rem;background:#FEF2F2;border-radius:6px;padding:0.5rem 0.8rem;font-size:0.83rem">
                    💸 Venta en riesgo si no se actúa: <b style="color:{color}">{fmt_mxn(venta_r)}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No se detectaron SKUs en riesgo inminente")

    # Recomendación IA
    st.markdown("""
    <div style="background:#F0FDF4;border:1.5px solid #86EFAC;border-radius:10px;padding:1rem 1.2rem;margin-top:0.5rem">
        <div style="font-weight:700;color:#166534;font-size:0.9rem">🤖 Recomendación IA</div>
        <div style="font-size:0.85rem;color:#14532D;margin-top:0.4rem;line-height:1.5">
            Generar órdenes de reabastecimiento urgente con Samsung y Apple esta semana.
            Temporada de alta demanda activa (Buen Fin + Navidad, factor estacional +180% vs. mes base).
            Priorizar <b>iPhones</b> y <b>TVs Samsung</b> dado historial de quiebres en períodos similares.
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    # Gráfica: inventario vs demanda por SKU en riesgo
    st.markdown("**Días de inventario restantes**")

    ult_semana = inventario["semana"].max()
    inv_rec = inventario[inventario["semana"] == ult_semana].merge(
        productos[["sku","nombre"]], on="sku"
    )
    inv_rec = inv_rec[inv_rec["dias_inventario"] < 60].sort_values("dias_inventario").copy()

    inv_rec.loc[:, "color"] = inv_rec["dias_inventario"].apply(
        lambda x: "#E63946" if x < 7 else ("#F4A261" if x < 14 else "#2BBAB4")
    )
    inv_rec.loc[:, "nombre_corto"] = inv_rec["nombre"].str[:30]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=inv_rec["dias_inventario"],
        y=inv_rec["nombre_corto"],
        orientation="h",
        marker_color=inv_rec["color"].tolist(),
        text=inv_rec["dias_inventario"].apply(lambda x: f"{x:.0f} días"),
        textposition="outside",
    ))
    fig.add_vline(x=14, line_dash="dash", line_color="#F4A261", annotation_text="⚠️ 14 días", annotation_position="top right")
    fig.add_vline(x=7,  line_dash="dash", line_color="#E63946", annotation_text="🔴 7 días",  annotation_position="top right")
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        height=300, margin=dict(l=0, r=60, t=10, b=0),
        xaxis=dict(title="Días", showgrid=True, gridcolor="#F3F4F6"),
        yaxis=dict(showgrid=False, tickfont=dict(size=9)),
    )
    st.plotly_chart(fig, use_container_width=True)

    if st.button("📋 Generar Órdenes de Compra Sugeridas", type="primary"):
        st.success("✅ Se generaron 3 OCs para revisión del área de compras")
        oc_preview = pd.DataFrame({
            "SKU":       ["SKU001", "SKU011", "SKU046"],
            "Producto":  ["iPhone 15 128GB", "Smart TV Samsung 55\" 4K", "Barbie Dreamhouse"],
            "Proveedor": ["Apple México", "Samsung Electronics MX", "Mattel de México"],
            "Unidades":  [150, 80, 200],
            "Monto":     ["$2,280,000", "$616,000", "$400,000"],
        })
        st.dataframe(oc_preview, use_container_width=True)

# ══════════════════════════════════════════════
# ALERTA 2 — MARGEN EROSIONADO
# ══════════════════════════════════════════════
st.markdown("---")

col_badge2, _ = st.columns([1, 5])
with col_badge2:
    st.markdown('<span style="background:#FEF3C7;color:#92400E;padding:6px 16px;border-radius:20px;font-weight:700;font-size:0.8rem;letter-spacing:0.05em">🟡 ATENCIÓN</span>', unsafe_allow_html=True)

st.markdown("### Alerta 2 — Margen Erosionado: Los Canales de Mayor Volumen Son los Menos Rentables")

left2, right2 = st.columns([2, 3])

with left2:
    m = alertas["margen"]
    peor  = m["peor"]
    mejor = m["mejor"]
    impacto = m["impacto"]
    gap     = m["gap"]

    peor_canal  = peor["canal"].values[0]
    mejor_canal = mejor["canal"].values[0]
    peor_marg   = peor["margen_pct"].values[0]
    mejor_marg  = mejor["margen_pct"].values[0]
    peor_desc   = peor["descuento"].values[0]
    mejor_desc  = mejor["descuento"].values[0]

    st.markdown(f"""
    <div style="background:white;border-radius:12px;padding:1.2rem;box-shadow:0 1px 8px rgba(0,0,0,0.07);margin-bottom:1rem">
        <div style="font-size:0.78rem;color:#9CA3AF;text-transform:uppercase;font-weight:600">Canal con menor margen</div>
        <div style="font-size:1.1rem;font-weight:700;color:#1F2937;margin:0.3rem 0">{peor_canal}</div>
        <div style="display:flex;gap:1.5rem;margin-top:0.5rem">
            <div>
                <div style="font-size:0.75rem;color:#9CA3AF">Margen real</div>
                <div style="font-size:1.6rem;font-weight:700;color:#E63946">{peor_marg:.1f}%</div>
            </div>
            <div>
                <div style="font-size:0.75rem;color:#9CA3AF">Desc. promedio</div>
                <div style="font-size:1.6rem;font-weight:700;color:#F4A261">{peor_desc:.1f}%</div>
            </div>
        </div>
    </div>
    <div style="background:white;border-radius:12px;padding:1.2rem;box-shadow:0 1px 8px rgba(0,0,0,0.07);margin-bottom:1rem">
        <div style="font-size:0.78rem;color:#9CA3AF;text-transform:uppercase;font-weight:600">Canal más rentable</div>
        <div style="font-size:1.1rem;font-weight:700;color:#1F2937;margin:0.3rem 0">{mejor_canal}</div>
        <div style="display:flex;gap:1.5rem;margin-top:0.5rem">
            <div>
                <div style="font-size:0.75rem;color:#9CA3AF">Margen real</div>
                <div style="font-size:1.6rem;font-weight:700;color:#2BBAB4">{mejor_marg:.1f}%</div>
            </div>
            <div>
                <div style="font-size:0.75rem;color:#9CA3AF">Desc. promedio</div>
                <div style="font-size:1.6rem;font-weight:700;color:#2BBAB4">{mejor_desc:.1f}%</div>
            </div>
        </div>
    </div>
    <div style="background:#FFF7ED;border:1.5px solid #FDBA74;border-radius:10px;padding:1rem">
        <div style="font-weight:700;color:#92400E;font-size:0.9rem">💰 Impacto estimado de optimizar descuentos</div>
        <div style="font-size:1.5rem;font-weight:700;color:#92400E;margin-top:0.3rem">{fmt_mxn(impacto)}</div>
        <div style="font-size:0.8rem;color:#78350F;margin-top:0.2rem">de margen adicional anual sin perder clientes</div>
    </div>
    """, unsafe_allow_html=True)

with right2:
    st.markdown("**Volumen vs. Margen por Punto de Venta** — el cuadrante ideal es arriba a la derecha")

    scatter_data = rent_cli.copy()
    canal_map2 = {
        "Tienda Física": "Tienda Física",
        "E-commerce":    "E-commerce",
        "Marketplace":   "Marketplace",
        "Crédito SD":    "Crédito SD",
        "Kuesky Pay":    "Financiamiento",
        "Aplazo":        "Financiamiento",
        "Mayoreo":       "Mayoreo",
    }
    scatter_data["canal_g"] = scatter_data["canal"].map(canal_map2).fillna("Otro")

    fig3 = px.scatter(
        scatter_data,
        x="venta_total_mxn", y="margen_pct_real",
        size="margen_total_mxn", color="canal_g",
        hover_name="nombre",
        hover_data={"venta_total_mxn": ":,.0f", "margen_pct_real": ":.1f", "canal_g": True},
        labels={"venta_total_mxn": "Venta Total MXN", "margen_pct_real": "Margen %", "canal_g": "Canal"},
        color_discrete_sequence=["#2BBAB4","#229E99","#F4A261","#E63946","#74D8D4","#6C757D"],
    )
    venta_med  = scatter_data["venta_total_mxn"].median()
    margen_med = scatter_data["margen_pct_real"].median()
    fig3.add_vline(x=venta_med,  line_dash="dot", line_color="#D1D5DB")
    fig3.add_hline(y=margen_med, line_dash="dot", line_color="#D1D5DB")

    fig3.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        height=340, margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=10)),
        xaxis=dict(tickformat=",.0f", showgrid=True, gridcolor="#F3F4F6"),
        yaxis=dict(showgrid=True, gridcolor="#F3F4F6"),
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    <div style="background:#F0FDF4;border:1.5px solid #86EFAC;border-radius:10px;padding:0.8rem 1rem;font-size:0.83rem">
        🤖 <b>IA detectó:</b> Marketplace y canales de financiamiento generan alto volumen pero con márgenes significativamente menores.
        Estrategia sugerida: ajustar precios en marketplace y optimizar comisiones de financiamiento.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# ALERTA 3 — CAÍDA DE VENTAS POR CANAL
# ══════════════════════════════════════════════
st.markdown("---")

col_badge3, _ = st.columns([1, 5])
with col_badge3:
    st.markdown('<span style="background:#EDE9FE;color:#4C1D95;padding:6px 16px;border-radius:20px;font-weight:700;font-size:0.8rem;letter-spacing:0.05em">🟣 ALERTA</span>', unsafe_allow_html=True)

st.markdown("### Alerta 3 — Sucursales con Caída de Actividad (Riesgo de Bajo Rendimiento)")

left3, right3 = st.columns([3, 2])

with left3:
    churn = alertas["churn"]
    churn_valor = alertas["churn_valor"]

    st.markdown(f"""
    <div style="background:#FFF7ED;border:1.5px solid #FDBA74;border-radius:10px;padding:1rem 1.2rem;margin-bottom:1rem">
        <div style="font-size:0.85rem;color:#92400E">
            La IA identificó <b>{len(churn)} puntos de venta</b> con caída significativa en actividad.
            Este patrón precede una reducción permanente de ventas en el <b>70% de los casos</b>.
        </div>
        <div style="font-size:1.3rem;font-weight:700;color:#92400E;margin-top:0.5rem">
            Venta anual en riesgo: {fmt_mxn(churn_valor)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if len(churn) > 0:
        for _, row in churn.iterrows():
            dias = row["dias_sin_compra"]
            seg  = row.get("segmento", "C")
            canal= row.get("canal", "")
            color= "#E63946" if dias > 25 else "#F4A261"

            st.markdown(f"""
            <div style="background:white;border-left:4px solid {color};border-radius:8px;
                        padding:0.8rem 1rem;margin-bottom:0.5rem;
                        box-shadow:0 1px 4px rgba(0,0,0,0.06)">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                        <div style="font-weight:600;font-size:0.9rem;color:#1F2937">{row['nombre']}</div>
                        <div style="font-size:0.78rem;color:#9CA3AF">{canal} · Segmento {seg}</div>
                    </div>
                    <div style="text-align:right">
                        <div style="font-size:1.3rem;font-weight:700;color:{color}">{dias} días</div>
                        <div style="font-size:0.75rem;color:#9CA3AF">sin actividad</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#F0FDF4;border:1.5px solid #86EFAC;border-radius:10px;padding:0.8rem 1rem;margin-top:0.5rem;font-size:0.83rem">
        🤖 <b>Acción sugerida:</b> Activar plan de reactivación: revisión de surtido en sucursales afectadas +
        campaña de promociones localizadas + evaluación de inventario por categoría.
    </div>
    """, unsafe_allow_html=True)

    if st.button("📧 Activar Plan de Reactivación para estas Sucursales"):
        st.success("✅ Gerentes regionales notificados. Plan de reactivación generado con análisis de categorías top por sucursal.")

with right3:
    st.markdown("**Días sin actividad por punto de venta en riesgo**")

    if len(churn) > 0:
        churn_plot = churn.copy()
        churn_plot["nombre_corto"] = churn_plot["nombre"].str[:28]
        churn_plot["color"] = churn_plot["dias_sin_compra"].apply(
            lambda x: "#E63946" if x > 25 else "#F4A261"
        )

        fig4 = go.Figure(go.Bar(
            x=churn_plot["dias_sin_compra"],
            y=churn_plot["nombre_corto"],
            orientation="h",
            marker_color=churn_plot["color"].tolist(),
            text=churn_plot["dias_sin_compra"].apply(lambda x: f"{x} días"),
            textposition="outside",
        ))
        fig4.add_vline(x=18, line_dash="dash", line_color="#F4A261", annotation_text="⚠️ Umbral alerta")
        fig4.update_layout(
            paper_bgcolor="white", plot_bgcolor="white",
            height=max(250, len(churn_plot) * 45),
            margin=dict(l=0, r=60, t=10, b=0),
            xaxis=dict(title="Días sin actividad", showgrid=True, gridcolor="#F3F4F6"),
            yaxis=dict(showgrid=False, tickfont=dict(size=9)),
        )
        st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════
# RESUMEN DE IMPACTO TOTAL
# ══════════════════════════════════════════════
st.markdown("---")
st.markdown("### 💰 Impacto Total de las 3 Alertas")

total_impacto = alertas["perdidas_hist"]["venta_perdida_mxn"].sum() + alertas["margen"]["impacto"] + alertas["churn_valor"]

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("🔴 Quiebres de stock", fmt_mxn(alertas["perdidas_hist"]["venta_perdida_mxn"].sum()), "Venta recuperable")
with c2:
    st.metric("🟡 Margen erosionado", fmt_mxn(alertas["margen"]["impacto"]), "Optimización de descuentos")
with c3:
    st.metric("🟣 Sucursales en riesgo", fmt_mxn(alertas["churn_valor"]), "Venta anual en riesgo")
with c4:
    st.metric("💎 Impacto total estimado", fmt_mxn(total_impacto), "Oportunidad identificada por IA", delta_color="off")

st.markdown(f"""
<div style="background:linear-gradient(135deg,#2D2D2D,#2BBAB4);border-radius:14px;padding:1.5rem 2rem;margin-top:1rem;color:white;text-align:center">
    <div style="font-size:0.9rem;opacity:0.85;margin-bottom:0.3rem">Con decisiones basadas en datos, Surtidora Departamental puede recuperar o proteger</div>
    <div style="font-size:2.5rem;font-weight:800">{fmt_mxn(total_impacto)}</div>
    <div style="font-size:0.88rem;opacity:0.75;margin-top:0.3rem">en los próximos 12 meses — sin abrir una sola sucursal nueva</div>
</div>
""", unsafe_allow_html=True)

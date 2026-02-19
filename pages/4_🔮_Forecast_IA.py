"""
pages/4_🔮_Forecast_IA.py
Predicción de demanda con IA — Próximas 8 semanas por SKU
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import load_all, get_forecast_data
from utils.ui import inject_css, page_header, fmt_mxn

st.set_page_config(page_title="Forecast IA | SD", page_icon="🔮", layout="wide")
inject_css()

ventas, clientes, productos, inventario, compras, rent_cli, abc_skus, perdidas = load_all()

with st.sidebar:
    st.markdown("### 🏪 Surtidora Departamental")
    st.markdown("---")
    skus_disponibles = {
        "SKU001": "iPhone 15 128GB",
        "SKU003": "Samsung Galaxy S24 128GB",
        "SKU011": "Smart TV Samsung 55\" 4K",
        "SKU020": "Tenis Nike Air Max 90",
        "SKU037": "Carolina Herrera Good Girl 80ml",
        "SKU046": "Barbie Dreamhouse",
    }
    sku_sel = st.selectbox(
        "SKU a analizar",
        list(skus_disponibles.keys()),
        format_func=lambda x: skus_disponibles[x],
    )
    st.markdown("---")
    st.caption("Modelo: Media móvil ponderada con factor de estacionalidad")
    st.caption("Horizonte: 8 semanas")
    st.caption("Intervalo de confianza: 85%")

page_header(
    "🔮 Forecast de Demanda — IA Predictiva",
    "De reaccionar a los quiebres a anticiparlos con 8 semanas de anticipación"
)

forecast_df = get_forecast_data()

# ─ KPIs del SKU seleccionado ───────────────────────────────────────────
prod_sel = productos[productos["sku"] == sku_sel].iloc[0]
ventas_sku = ventas[ventas["sku"] == sku_sel]
inv_sku = inventario[inventario["sku"] == sku_sel]

forecast_sku = forecast_df[forecast_df["sku"] == sku_sel]
real_sku     = forecast_sku[forecast_sku["tipo"] == "real"]
pred_sku     = forecast_sku[forecast_sku["tipo"] == "forecast"]

demanda_pred_total = pred_sku["cajas"].sum() if len(pred_sku) > 0 else 0
stock_actual = inv_sku[inv_sku["semana"] == inv_sku["semana"].max()]["stock_cajas"].values
stock_actual = stock_actual[0] if len(stock_actual) > 0 else 0
deficit = max(0, demanda_pred_total - stock_actual)

st.markdown(f"**Analizando:** {prod_sel['nombre']} · {prod_sel['marca']} · {prod_sel['categoria']}")
st.markdown("")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Precio Lista",       f"${prod_sel['precio_lista_mxn']:,.0f} MXN")
c2.metric("Demanda Proyectada", f"{demanda_pred_total:,.0f} uds", "Próximas 8 semanas")
c3.metric("Stock Actual",       f"{stock_actual:,.0f} uds", "Último snapshot")
c4.metric(
    "Déficit Estimado",
    f"{deficit:,.0f} uds" if deficit > 0 else "✅ Sin déficit",
    f"{fmt_mxn(deficit * prod_sel['precio_lista_mxn'])} en riesgo" if deficit > 0 else "Inventario suficiente",
    delta_color="inverse" if deficit > 0 else "normal",
)

st.markdown("---")

# ─ Gráfica principal de forecast ──────────────────────────────────────
st.markdown("#### 📈 Demanda Real vs. Forecast — Continuidad de Serie")

fig = go.Figure()

if len(real_sku) > 0:
    fig.add_trace(go.Scatter(
        x=real_sku["semana"], y=real_sku["cajas"],
        name="Demanda Real", mode="lines+markers",
        line=dict(color="#2D2D2D", width=2),
        marker=dict(size=5, color="#2D2D2D"),
    ))

if len(pred_sku) > 0:
    factor_ci = 0.15
    fig.add_trace(go.Scatter(
        x=pd.concat([pred_sku["semana"], pred_sku["semana"].iloc[::-1]]),
        y=pd.concat([pred_sku["cajas"] * (1 + factor_ci), pred_sku["cajas"].iloc[::-1] * (1 - factor_ci)]),
        fill="toself", fillcolor="rgba(43,186,180,0.12)",
        line=dict(color="rgba(43,186,180,0)"),
        name="Intervalo 85%", showlegend=True,
    ))
    fig.add_trace(go.Scatter(
        x=pred_sku["semana"], y=pred_sku["cajas"],
        name="Forecast IA", mode="lines+markers",
        line=dict(color="#2BBAB4", width=2.5, dash="dash"),
        marker=dict(size=7, color="#2BBAB4", symbol="diamond"),
    ))

if stock_actual > 0:
    fig.add_hline(
        y=stock_actual, line_dash="dot", line_color="#E63946",
        annotation_text=f"Stock actual: {stock_actual:.0f} uds",
        annotation_position="top left",
    )

if len(real_sku) > 0:
    corte = real_sku["semana"].max()
    corte_str = str(corte)
    fig.add_shape(
        type="line", x0=corte_str, x1=corte_str, y0=0, y1=1,
        yref="paper", line=dict(dash="dash", color="#9CA3AF"),
    )
    fig.add_annotation(
        x=corte_str, y=1, yref="paper",
        text="↓ Forecast", showarrow=False,
        xanchor="left", yanchor="bottom",
        font=dict(size=11, color="#9CA3AF"),
    )

fig.update_layout(
    height=380, paper_bgcolor="white", plot_bgcolor="white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    xaxis=dict(showgrid=False, title=""),
    yaxis=dict(showgrid=True, gridcolor="#F3F4F6", title="Unidades"),
    margin=dict(l=0, r=0, t=30, b=0),
    hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True)

# ─ Tabla de forecast por semana ───────────────────────────────────────
left2, right2 = st.columns([2, 3])

with left2:
    st.markdown("#### 📅 Forecast Semanal — Próximas 8 Semanas")

    if len(pred_sku) > 0:
        tabla_fc = pred_sku.copy()
        tabla_fc["semana_str"]      = tabla_fc["semana"].dt.strftime("%d %b %Y")
        tabla_fc["cajas_fmt"]       = tabla_fc["cajas"].apply(lambda x: f"{x:.0f}")
        tabla_fc["venta_est_mxn"]   = (tabla_fc["cajas"] * prod_sel["precio_lista_mxn"] * 0.90).apply(lambda x: f"${x:,.0f}")
        tabla_fc["margen_est_mxn"]  = (tabla_fc["cajas"] * (prod_sel["precio_lista_mxn"] - prod_sel["costo_mxn"]) * 0.90).apply(lambda x: f"${x:,.0f}")
        tabla_fc["accion"] = tabla_fc["cajas"].apply(
            lambda x: "🟢 Normal" if x < stock_actual * 0.2 else "🟠 Preparar OC" if x < stock_actual * 0.5 else "🔴 Reabastecer"
        )

        st.dataframe(
            tabla_fc[["semana_str","cajas_fmt","venta_est_mxn","margen_est_mxn","accion"]].rename(columns={
                "semana_str": "Semana", "cajas_fmt": "Uds est.", 
                "venta_est_mxn": "Venta est.", "margen_est_mxn": "Margen est.", "accion": "Acción"
            }),
            use_container_width=True, height=320,
        )

with right2:
    st.markdown("#### 📊 Estacionalidad Histórica por Mes")
    st.caption("Patrones de demanda que el modelo usa para proyectar")

    ventas_sku = ventas_sku.copy()
    ventas_sku.loc[:, "mes_num"] = ventas_sku["fecha"].dt.month
    ventas_sku.loc[:, "mes_nom"] = ventas_sku["fecha"].dt.strftime("%b")
    est_mes = ventas_sku.groupby(["mes_num","mes_nom"])["cantidad_cajas"].sum().reset_index()
    est_mes = est_mes.sort_values("mes_num")
    promedio = est_mes["cantidad_cajas"].mean()
    est_mes["vs_promedio"] = ((est_mes["cantidad_cajas"] - promedio) / promedio * 100).round(1)
    est_mes["color"] = est_mes["vs_promedio"].apply(lambda x: "#2BBAB4" if x >= 0 else "#E63946")

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=est_mes["mes_nom"], y=est_mes["cantidad_cajas"],
        marker_color=est_mes["color"].tolist(),
        text=est_mes["vs_promedio"].apply(lambda x: f"{'+'if x>=0 else''}{x:.0f}%"),
        textposition="outside",
    ))
    fig3.add_hline(y=promedio, line_dash="dash", line_color="#9CA3AF", annotation_text="Promedio")
    fig3.update_layout(
        height=320, paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#F3F4F6", title="Unidades"),
        margin=dict(l=0, r=0, t=30, b=0),
    )
    st.plotly_chart(fig3, use_container_width=True)

# ─ Recomendación de OC ─────────────────────────────────────────────────
st.markdown("---")
st.markdown("#### 🤖 Recomendación de Reabastecimiento — Generada por IA")

lt_estimado = compras[compras["sku"] == sku_sel]["lead_time_dias"].mean() if len(compras[compras["sku"] == sku_sel]) > 0 else 15
semanas_lt  = int(np.ceil(lt_estimado / 7))
demanda_lt  = pred_sku.head(semanas_lt)["cajas"].sum() if len(pred_sku) >= semanas_lt else demanda_pred_total / 2
cantidad_oc = max(0, demanda_lt * 1.2 - stock_actual)
monto_oc    = cantidad_oc * prod_sel["costo_mxn"]

# Obtener proveedor
proveedor_map = {
    "Apple": "Apple México Distribución", "Samsung": "Samsung Electronics MX",
    "Nike": "Nike de México", "Mattel": "Mattel de México",
    "Carolina Herrera": "Puig México",
}
proveedor_nombre = proveedor_map.get(prod_sel["marca"], "Proveedor autorizado")

col_rec, col_accion = st.columns([3, 1])
with col_rec:
    if cantidad_oc > 0:
        st.markdown(f"""
        <div style="background:#F0FDF4;border:1.5px solid #86EFAC;border-radius:12px;padding:1.2rem 1.5rem">
            <div style="font-weight:700;color:#166534;font-size:1rem;margin-bottom:0.5rem">
                📋 Orden de Compra Sugerida — {prod_sel['nombre']}
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;font-size:0.88rem">
                <div>
                    <div style="color:#6B7280">Cantidad sugerida</div>
                    <div style="font-weight:700;font-size:1.2rem;color:#2D2D2D">{cantidad_oc:.0f} unidades</div>
                </div>
                <div>
                    <div style="color:#6B7280">Monto de compra</div>
                    <div style="font-weight:700;font-size:1.2rem;color:#2D2D2D">{fmt_mxn(monto_oc)}</div>
                </div>
                <div>
                    <div style="color:#6B7280">Lead time estimado</div>
                    <div style="font-weight:700;font-size:1.2rem;color:#2D2D2D">{lt_estimado:.0f} días</div>
                </div>
            </div>
            <div style="margin-top:0.8rem;font-size:0.82rem;color:#166534">
                ✅ Emitir OC antes del <b>{(pd.Timestamp.now() + pd.Timedelta(days=3)).strftime('%d %b %Y')}</b> 
                para garantizar disponibilidad durante la temporada de demanda proyectada.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success(f"✅ Stock actual suficiente para cubrir la demanda proyectada de las próximas 8 semanas con {stock_actual:.0f} unidades.")

with col_accion:
    st.markdown("<br>", unsafe_allow_html=True)
    if cantidad_oc > 0:
        if st.button("📤 Generar OC", type="primary", use_container_width=True):
            st.success("✅ OC generada y enviada para aprobación")
    st.markdown(f"**Proveedor:** {proveedor_nombre}")
    st.markdown(f"**Condición:** 30 días")

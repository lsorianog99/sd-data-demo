"""
utils/data_loader.py
Carga y procesamiento central de datos para Surtidora Departamental PoC
"""

import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


@st.cache_data
def load_all():
    ventas       = pd.read_csv(DATA_DIR / "ventas.csv", parse_dates=["fecha"])
    clientes     = pd.read_csv(DATA_DIR / "clientes.csv", parse_dates=["fecha_alta"])
    productos    = pd.read_csv(DATA_DIR / "productos.csv")
    inventario   = pd.read_csv(DATA_DIR / "inventario.csv", parse_dates=["semana"])
    compras      = pd.read_csv(DATA_DIR / "pedidos_compra.csv", parse_dates=["fecha_pedido"])
    rent_cli     = pd.read_csv(DATA_DIR / "rentabilidad_clientes.csv")
    abc_skus     = pd.read_csv(DATA_DIR / "analisis_abc_skus.csv")
    perdidas     = pd.read_csv(DATA_DIR / "ventas_perdidas.csv")
    return ventas, clientes, productos, inventario, compras, rent_cli, abc_skus, perdidas


@st.cache_data
def get_kpis():
    ventas, clientes, productos, inventario, compras, rent_cli, abc_skus, perdidas = load_all()

    venta_total       = ventas["monto_total_mxn"].sum()
    margen_total      = ventas["margen_bruto_mxn"].sum()
    margen_pct        = margen_total / venta_total * 100
    venta_perdida     = perdidas["venta_perdida_mxn"].sum()
    margen_perdido    = perdidas["margen_perdido_mxn"].sum()
    n_quiebres        = perdidas.shape[0]
    clientes_churn    = _detectar_churn(ventas)
    skus_a            = abc_skus[abc_skus["clasificacion_abc"] == "A"].shape[0]
    skus_total        = abc_skus.shape[0]
    unidades_vendidas = ventas["cantidad_cajas"].sum()

    return {
        "venta_total":     venta_total,
        "margen_total":    margen_total,
        "margen_pct":      margen_pct,
        "venta_perdida":   venta_perdida,
        "margen_perdido":  margen_perdido,
        "n_quiebres":      n_quiebres,
        "clientes_churn":  clientes_churn,
        "skus_a":          skus_a,
        "skus_total":      skus_total,
        "unidades_vendidas": unidades_vendidas,
    }


def _detectar_churn(ventas: pd.DataFrame, dias_umbral: int = 18) -> list:
    """Sucursales/canales que llevan más de N días sin vender (señal de caída)"""
    ultimo_global = ventas["fecha"].max()
    ultima_compra = ventas.groupby("cliente_id")["fecha"].max()
    dias_sin_comprar = (ultimo_global - ultima_compra).dt.days
    en_riesgo = dias_sin_comprar[dias_sin_comprar >= dias_umbral].sort_values(ascending=False)
    return en_riesgo.reset_index().rename(columns={"fecha": "dias_sin_compra"}).head(10)


@st.cache_data
def get_forecast_data():
    """Genera forecast simple por SKU usando media móvil ponderada"""
    ventas, *_ = load_all()
    ventas = ventas.copy()
    ventas.loc[:, "semana"] = ventas["fecha"].dt.to_period("W").apply(lambda r: r.start_time)

    # Calcular demanda semanal por SKU
    dem = ventas.groupby(["semana", "sku"])["cantidad_cajas"].sum().reset_index()

    # Forecast para SKUs estrella retail
    skus_forecast = ["SKU001", "SKU003", "SKU011", "SKU020", "SKU037", "SKU046"]
    resultados = []

    for sku in skus_forecast:
        serie = dem[dem["sku"] == sku].set_index("semana")["cantidad_cajas"].sort_index()
        if len(serie) < 4:
            continue
        # Media móvil ponderada (más peso a semanas recientes)
        ultimas = serie.tail(8).values
        pesos   = np.linspace(1, 2, len(ultimas))
        pesos  /= pesos.sum()
        pred    = (ultimas * pesos).sum()

        # Proyectar 8 semanas
        ultima_semana = serie.index.max()
        for i in range(1, 9):
            semana_fut = ultima_semana + pd.Timedelta(weeks=i)
            resultados.append({
                "sku":     sku,
                "semana":  semana_fut,
                "tipo":    "forecast",
                "cajas":   max(0, pred * np.random.normal(1.0, 0.08)),
            })

        # Histórico para mostrar continuidad
        for semana, cajas in serie.tail(12).items():
            resultados.append({"sku": sku, "semana": semana, "tipo": "real", "cajas": cajas})

    return pd.DataFrame(resultados)


@st.cache_data
def get_alertas():
    """Las 3 alertas IA — el centerpiece de la PoC"""
    ventas, clientes, productos, inventario, _, rent_cli, _, perdidas = load_all()

    # ── ALERTA 1: Riesgo de quiebre inminente ──────────────────────────
    ult_semana = inventario["semana"].max()
    inv_reciente = inventario[inventario["semana"] == ult_semana].copy()
    inv_reciente = inv_reciente.merge(productos[["sku","nombre","marca","precio_lista_mxn","temporalidad"]], on="sku")

    # SKUs con menos de 14 días de inventario y alta demanda
    riesgo_quiebre = inv_reciente[
        (inv_reciente["dias_inventario"] < 14) &
        (inv_reciente["dias_inventario"] > 0) &
        (inv_reciente["demanda_semana"] > 0)
    ].sort_values("dias_inventario").head(3)

    riesgo_quiebre = riesgo_quiebre.copy()
    riesgo_quiebre.loc[:, "venta_en_riesgo"] = (
        riesgo_quiebre["demanda_semana"] * 2 * riesgo_quiebre["precio_lista_mxn"] * 0.90
    ).round(0)

    # ── ALERTA 2: Margen erosionado por descuentos ──────────────────────
    margen_canal = rent_cli.groupby("canal").agg(
        margen_pct=("margen_pct_real", "mean"),
        venta=("venta_total_mxn", "sum"),
        descuento=("descuento_promedio", "mean"),
    ).reset_index()

    peor_margen  = margen_canal.sort_values("margen_pct").head(2)
    mejor_margen = margen_canal.sort_values("margen_pct", ascending=False).head(1)

    gap_margen = mejor_margen["margen_pct"].values[0] - peor_margen["margen_pct"].values[0]
    venta_canal_bajo = peor_margen["venta"].sum()
    impacto_margen = venta_canal_bajo * (gap_margen / 100)

    # ── ALERTA 3: Sucursales/canales en riesgo de churn ─────────────────
    churn_df = _detectar_churn(ventas, dias_umbral=15)
    churn_df = churn_df.merge(clientes[["cliente_id","nombre","canal","segmento"]], on="cliente_id")
    churn_seg_a = churn_df[churn_df["segmento"].isin(["A","B"])].head(3)

    # Valor histórico
    ventas_churn = ventas[ventas["cliente_id"].isin(churn_seg_a["cliente_id"])].groupby("cliente_id")["monto_total_mxn"].sum()
    venta_en_riesgo_churn = ventas_churn.sum() * 0.12

    return {
        "quiebre":        riesgo_quiebre,
        "margen":         {"peor": peor_margen, "mejor": mejor_margen, "impacto": impacto_margen, "gap": gap_margen},
        "churn":          churn_seg_a,
        "churn_valor":    venta_en_riesgo_churn,
        "perdidas_hist":  perdidas,
    }

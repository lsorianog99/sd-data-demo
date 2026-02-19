"""
pages/5_🤖_Chat_IA.py
Asistente de IA entrenado con los datos de Surtidora Departamental
"""

import streamlit as st
import pandas as pd
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import load_all, get_kpis, get_alertas
from utils.ui import inject_css, page_header, fmt_mxn

st.set_page_config(page_title="Chat IA | SD", page_icon="🤖", layout="wide")
inject_css()

page_header(
    "🤖 Asistente IA — Pregunta sobre tu Negocio",
    "IA entrenada con los datos de Surtidora Departamental. Haz preguntas en lenguaje natural."
)

# ── Carga de datos para contexto ────────────────────────────────────────
ventas, clientes, productos, inventario, compras, rent_cli, abc_skus, perdidas = load_all()
kpis    = get_kpis()
alertas = get_alertas()

# ── Construir contexto de negocio ──────────────────────────────────────
def build_context() -> str:
    top10 = rent_cli.head(10)[["nombre","canal","segmento","venta_total_mxn","margen_pct_real","descuento_promedio"]].copy()
    top10.loc[:, "venta_total_mxn"] = top10["venta_total_mxn"].round(0)
    top10.loc[:, "margen_pct_real"] = top10["margen_pct_real"].round(1)
    top10.loc[:, "descuento_promedio"] = top10["descuento_promedio"].round(1)

    margen_canal = rent_cli.copy()
    margen_canal_agg = margen_canal.groupby("canal").agg(
        venta=("venta_total_mxn","sum"),
        margen_pct=("margen_pct_real","mean"),
    ).round(1).reset_index()

    abc_res = abc_skus.groupby("clasificacion_abc").agg(
        n_skus=("sku","count"),
        margen_sum=("margen_total_mxn","sum"),
    ).reset_index()

    churn = alertas["churn"]
    quiebre = alertas["quiebre"]

    ctx = f"""
Eres el asistente de inteligencia de negocios de SURTIDORA DEPARTAMENTAL, una tienda departamental mexicana
con presencia en Jalisco, Guanajuato, y otras regiones de México. Vende tecnología, línea blanca, calzado,
ropa, perfumes, colchones, juguetes, bicicletas y más. Opera con tiendas físicas, e-commerce, marketplace
y financiamiento propio (Crédito Surtidora, Kuesky Pay, Aplazo).

=== DATOS CLAVE DE SURTIDORA DEPARTAMENTAL ===

RESUMEN EJECUTIVO (2023-2024):
- Venta total: {fmt_mxn(kpis['venta_total'])}
- Margen bruto total: {fmt_mxn(kpis['margen_total'])} ({kpis['margen_pct']:.1f}%)
- Venta perdida por quiebres de stock: {fmt_mxn(kpis['venta_perdida'])}
- Margen perdido: {fmt_mxn(kpis['margen_perdido'])}
- Puntos de venta: {len(clientes)}
- SKUs en catálogo: {len(productos)}
- Categorías: Smartphones, Laptops, TVs, Línea Blanca, Calzado, Ropa, Perfumes, Colchones, Juguetes, Bicicletas, Belleza, Accesorios Tech, Hogar
- Marcas principales: Apple, Samsung, Nike, Puma, LOB, Andrea, Lee, Mattel, Hasbro, LG, Whirlpool, Restonic

CATEGORÍAS Y MARCAS:
{productos.groupby("categoria")["marca"].apply(lambda x: ", ".join(x.unique())).to_string()}

TOP 10 PUNTOS DE VENTA POR VOLUMEN:
{top10.to_string(index=False)}

MARGEN REAL POR CANAL:
{margen_canal_agg.to_string(index=False)}

ANÁLISIS ABC DE SKUs:
{abc_res.to_string(index=False)}
- Clase A: {kpis['skus_a']} SKUs → 80% del margen
- Clase C: {kpis['skus_total'] - kpis['skus_a']} SKUs → ~5% del margen

SUCURSALES CON CAÍDA DE ACTIVIDAD:
{churn[['nombre','canal','dias_sin_compra','segmento']].to_string(index=False) if len(churn) > 0 else 'Ninguna detectada'}

QUIEBRES DE STOCK DETECTADOS:
{quiebre[['sku','stock_cajas','dias_inventario','venta_en_riesgo']].to_string(index=False) if len(quiebre) > 0 else 'Sin quiebres inminentes'}

EPISODIOS HISTÓRICOS DE QUIEBRE:
{perdidas[['nombre','temporada','dias_sin_stock','venta_perdida_mxn','margen_perdido_mxn']].to_string(index=False)}

INSIGHT CLAVE:
Los canales digitales (Marketplace, E-commerce) generan alto volumen pero menor margen por descuentos y comisiones.
Crédito Surtidora es el canal con mejor margen neto dado que no hay comisiones de terceros.
Los quiebres de stock ocurren en temporadas clave: Buen Fin, Navidad, Hot Sale, Día de las Madres.

INSTRUCCIONES:
- Responde siempre con datos específicos de Surtidora Departamental
- Sé directo y ejecutivo — hablas con la dirección general
- Ofrece recomendaciones accionables con números concretos
- Usa montos en MXN
- Responde en español
"""
    return ctx

SYSTEM_CONTEXT = build_context()

# ── Preguntas sugeridas ─────────────────────────────────────────────────
PREGUNTAS_SUGERIDAS = [
    "¿Cuál es la sucursal más rentable?",
    "¿Qué categorías debería priorizar en inventario?",
    "¿Cuánto perdimos por quiebres de stock?",
    "¿Qué sucursales están perdiendo ventas?",
    "¿Dónde está la mayor oportunidad de mejora de margen?",
    "¿Qué canal debería priorizar para crecer?",
    "¿Cómo se comparan las ventas de e-commerce vs tienda física?",
    "Dame un resumen ejecutivo del negocio",
    "¿Qué pasa con las ventas en temporada de Buen Fin?",
    "¿Qué productos son los más vendidos?",
]

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"""¡Hola! Soy el asistente de inteligencia de negocios de **Surtidora Departamental**.

Tengo acceso completo a los datos de ventas 2023-2024:
- **{len(ventas):,}** transacciones analizadas
- **{len(clientes)}** puntos de venta en **{clientes['canal'].nunique()} canales**
- **{len(productos)}** SKUs de **{productos['marca'].nunique()} marcas**

Algunos hallazgos que ya detecté y puedes explorar:

🔴 **{fmt_mxn(kpis['venta_perdida'])}** en ventas perdidas por quiebres en Buen Fin, Navidad y temporadas clave

🟡 Los canales **Marketplace** y **financiamiento terceros** tienen márgenes significativamente menores que **Tienda Física** y **Crédito SD**

🟣 **{len(alertas['churn'])} sucursales** muestran caída significativa en actividad

¿Qué quieres analizar?"""
    })

# ── API Key ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏪 Surtidora Departamental")
    st.markdown("---")
    st.markdown("**Configuración del Chat**")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "") or st.secrets.get("ANTHROPIC_API_KEY", "")

    if not api_key:
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            placeholder="sk-ant-...",
            help="Requerida para el chat con IA real. Obtén una en console.anthropic.com",
        )
    else:
        st.success("✅ API Key cargada desde .env")

    st.markdown("---")
    st.markdown("**Preguntas sugeridas:**")
    for preg in PREGUNTAS_SUGERIDAS[:6]:
        if st.button(preg, use_container_width=True, key=f"sug_{preg[:20]}"):
            st.session_state.pending_question = preg
    st.markdown("---")
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.messages = []
        st.rerun()

# ── Mostrar historial ──────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🏪" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# ── Input ──────────────────────────────────────────────────────────────
pregunta = st.chat_input("Pregunta sobre el negocio de Surtidora Departamental...")

if "pending_question" in st.session_state:
    pregunta = st.session_state.pending_question
    del st.session_state.pending_question


# ═════════════════════════════════════════════════════════════════════════
# MOTOR DE RESPUESTAS DEMO — Multi-tema con fallback inteligente
# ═════════════════════════════════════════════════════════════════════════

def _demo_response(pregunta: str, kpis, rent_cli, abc_skus, perdidas, alertas) -> str:
    p = pregunta.lower()

    TOPICS = {
        "rentabilidad":   ["rentable", "rentabilidad", "margen", "mejor sucursal",
                           "ganancia", "utilidad", "profit"],
        "inventario":     ["quiebre", "perdid", "stock", "inventario",
                           "faltante", "desabasto", "abastec"],
        "churn":          ["churn", "sin vender", "perdiendo", "caída",
                           "abandono", "inactiv", "baja actividad"],
        "abc":            ["sku", "producto", "abc", "priorizar",
                           "catálogo", "catalogo", "clase", "más vendid"],
        "resumen":        ["resumen", "general", "negocio", "panorama", "dashboard"],
        "estacionalidad": ["estacional", "temporad", "buen fin", "navidad",
                           "hot sale", "día de las madres", "patrón", "ciclo"],
        "canales":        ["canal", "e-commerce", "tienda física", "marketplace",
                           "crédito", "kuesky", "aplazo", "financiamiento"],
        "regiones":       ["región", "region", "jalisco", "guanajuato", "sucursal",
                           "zona", "geográf"],
        "oportunidad":    ["oportunidad", "mejora", "crecer", "crecimiento",
                           "optimizar", "estrategia", "acción",
                           "recomendación", "recomendacion"],
    }

    matched = []
    for topic, keywords in TOPICS.items():
        if any(w in p for w in keywords):
            matched.append(topic)

    if len(matched) > 1 and "resumen" in matched:
        matched.remove("resumen")

    def _resp_rentabilidad():
        top = rent_cli.sort_values("margen_total_mxn", ascending=False).head(5)
        bottom = rent_cli.sort_values("margen_pct_real").head(3)
        r = "### 💰 Análisis de Rentabilidad\n\n"
        r += "**Top 5 puntos de venta por margen total:**\n\n"
        for _, row in top.iterrows():
            r += (f"- **{row['nombre']}** · {row['canal']} · "
                  f"Margen: {row['margen_pct_real']:.1f}% · "
                  f"{fmt_mxn(row['margen_total_mxn'])}\n")
        r += "\n**Puntos de venta con margen más débil (alerta):**\n\n"
        for _, row in bottom.iterrows():
            r += (f"- ⚠️ **{row['nombre']}** · {row['canal']} · "
                  f"Margen: {row['margen_pct_real']:.1f}% · "
                  f"Desc: {row['descuento_promedio']:.1f}%\n")
        mc = rent_cli.groupby("canal")["margen_pct_real"].mean().sort_values()
        gap = mc.iloc[-1] - mc.iloc[0]
        r += (f"\n💡 **Insight:** El canal **{mc.index[-1]}** supera a "
              f"**{mc.index[0]}** por **{gap:.1f} pts** de margen. "
              f"Marketplace y financiamiento terceros erosionan margen por comisiones.")
        return r

    def _resp_inventario():
        total = perdidas["venta_perdida_mxn"].sum()
        total_m = perdidas["margen_perdido_mxn"].sum()
        r = "### 📦 Quiebres de Stock\n\n"
        r += (f"**Impacto total:** {fmt_mxn(total)} venta perdida · "
              f"{fmt_mxn(total_m)} margen perdido\n\n")
        for _, row in perdidas.iterrows():
            r += (f"- **{row['nombre']}** · Temporada {row['temporada']} · "
                  f"{row['dias_sin_stock']} días sin stock · "
                  f"Perdido: {fmt_mxn(row['venta_perdida_mxn'])}\n")
        r += ("\n⚠️ Los quiebres ocurren en las temporadas de mayor demanda "
              "(Buen Fin +180%, Navidad +220%), amplificando el impacto.")
        r += (f"\n\n🎯 **Acción:** Asegurar inventario 4-6 semanas antes de cada "
              f"temporada para los productos afectados.")
        return r

    def _resp_churn():
        churn = alertas["churn"]
        churn_valor = alertas["churn_valor"]
        r = "### 🟣 Sucursales con Caída de Actividad\n\n"
        r += (f"**{len(churn)} puntos de venta** con actividad reducida · "
              f"Venta en riesgo: **{fmt_mxn(churn_valor)}**\n\n")
        for _, row in churn.iterrows():
            seg = row.get("segmento", "—")
            canal = row.get("canal", "")
            r += (f"- **{row['nombre']}** · {canal} · Seg. {seg} · "
                  f"**{row['dias_sin_compra']} días** sin actividad\n")
        r += ("\n🎯 **Acción inmediata:** Revisión de surtido, evaluación de "
              "competencia local y campaña de reactivación por sucursal.")
        return r

    def _resp_abc():
        sa = abc_skus[abc_skus["clasificacion_abc"] == "A"]
        sb = abc_skus[abc_skus["clasificacion_abc"] == "B"]
        sc = abc_skus[abc_skus["clasificacion_abc"] == "C"]
        r = f"### 📊 Análisis ABC ({len(abc_skus)} SKUs)\n\n"
        r += f"🟢 **Clase A ({len(sa)}):** 80% del margen — disponibilidad permanente\n"
        r += f"🟡 **Clase B ({len(sb)}):** 15% del margen — stock mínimo calculado\n"
        r += f"🔴 **Clase C ({len(sc)}):** 5% del margen — evaluar descontinuación\n\n"
        r += "**Top 5 SKUs Clase A:**\n\n"
        for _, row in sa.head(5).iterrows():
            r += (f"- **{row['nombre']}** · "
                  f"Margen: {fmt_mxn(row['margen_total_mxn'])} · "
                  f"Venta: {fmt_mxn(row['venta_total_mxn'])}\n")
        r += f"\n💡 Los {len(sc)} SKUs C consumen espacio de almacén sin retorno proporcional."
        return r

    def _resp_resumen():
        return f"""### 📈 Resumen Ejecutivo — Surtidora Departamental 2023-2024

**Venta:** {fmt_mxn(kpis['venta_total'])} · **Margen:** {kpis['margen_pct']:.1f}% · **Margen $:** {fmt_mxn(kpis['margen_total'])}

**3 hallazgos críticos:**

🔴 **{fmt_mxn(kpis['venta_perdida'])} en venta perdida** por quiebres en temporadas clave (Buen Fin, Navidad, Hot Sale). Margen perdido: {fmt_mxn(kpis['margen_perdido'])}.

🟡 **Paradoja Digital:** Mayor volumen en marketplace = menor margen por comisiones y descuentos. Crédito SD y Tienda Física tienen el mejor margen neto.

🟣 **{len(alertas['churn'])} sucursales** con señal de baja actividad — {fmt_mxn(alertas['churn_valor'])} en venta anual en riesgo.

**Oportunidad total sin abrir nuevas sucursales:** {fmt_mxn(kpis['venta_perdida'] + kpis['margen_perdido'] + alertas['churn_valor'])}"""

    def _resp_estacionalidad():
        por_temp = perdidas.groupby("temporada")["venta_perdida_mxn"].sum()
        impacto_total = por_temp.sum()

        r = "### 🌡️ Estacionalidad y Temporadas Clave\n\n"
        r += ("El retail departamental tiene **5 temporadas críticas** de demanda:\n\n")

        r += "**1. 🛒 Buen Fin (3a semana noviembre)**\n"
        r += ("Pico de +180% en smartphones, TVs y laptops. Los quiebres aquí "
              "significan perder la venta más importante del año.\n\n")

        r += "**2. 🎄 Navidad (diciembre)**\n"
        r += ("Juguetes (+300%), perfumes (+220%) y electrónica (+200%). "
              "Inventario debe estar preparado desde octubre.\n\n")

        r += "**3. 💐 Día de las Madres (1-10 mayo)**\n"
        r += ("Perfumes, belleza y accesorios disparan +280%. "
              "Es la 2a temporada más importante en estas categorías.\n\n")

        r += "**4. 🔥 Hot Sale (mayo-junio)**\n"
        r += ("Línea blanca y colchones +160%. Los consumidores esperan "
              "descuentos agresivos — asegurar stock es clave.\n\n")

        r += "**5. 📚 Regreso a Clases (agosto-septiembre)**\n"
        r += ("Laptops y tablets +100%. Oportunidad de captar nuevos "
              "clientes jóvenes.\n\n")

        r += f"**🎯 Impacto de quiebres en temporadas:** {fmt_mxn(impacto_total)} perdidos\n"
        r += ("Preparar inventario 4-6 semanas antes de cada temporada "
              f"podría recuperar **~{fmt_mxn(impacto_total * 0.6)}** anuales.")
        return r

    def _resp_canales():
        mc = rent_cli.groupby("canal").agg(
            venta=("venta_total_mxn", "sum"),
            margen_pct=("margen_pct_real", "mean"),
            descuento=("descuento_promedio", "mean"),
            n=("cliente_id", "nunique"),
        ).sort_values("margen_pct", ascending=False).reset_index()

        r = "### 📊 Comparativa por Canal\n\n"
        r += "| Canal | Venta | Margen % | Desc. % | Puntos |\n"
        r += "|-------|-------|----------|---------|--------|\n"
        for _, row in mc.iterrows():
            r += (f"| {row['canal']} | {fmt_mxn(row['venta'])} | "
                  f"{row['margen_pct']:.1f}% | {row['descuento']:.1f}% | "
                  f"{row['n']} |\n")
        mejor = mc.iloc[0]
        peor = mc.iloc[-1]
        gap = mejor["margen_pct"] - peor["margen_pct"]
        r += f"\n🏆 **Más rentable:** {mejor['canal']} ({mejor['margen_pct']:.1f}%)\n"
        r += f"⚠️ **Menos rentable:** {peor['canal']} ({peor['margen_pct']:.1f}%)\n"
        r += (f"\n💡 La diferencia de **{gap:.1f} pts** se explica por comisiones de "
              f"marketplace, descuentos en e-commerce y costos de financiamiento. "
              f"Fortalecer Crédito SD propio maximiza rentabilidad.")
        return r

    def _resp_regiones():
        reg = rent_cli.merge(
            clientes[["cliente_id", "region"]], on="cliente_id"
        ).groupby("region").agg(
            venta=("venta_total_mxn", "sum"),
            margen=("margen_total_mxn", "sum"),
            margen_pct=("margen_pct_real", "mean"),
            n=("cliente_id", "nunique"),
        ).sort_values("margen", ascending=False).reset_index()

        r = "### 📍 Rendimiento por Región\n\n"
        r += "| Región | Venta | Margen $ | Margen % | Sucursales |\n"
        r += "|--------|-------|----------|----------|------------|\n"
        for _, row in reg.iterrows():
            r += (f"| {row['region']} | {fmt_mxn(row['venta'])} | "
                  f"{fmt_mxn(row['margen'])} | {row['margen_pct']:.1f}% | "
                  f"{row['n']} |\n")
        mejor = reg.iloc[0]
        r += f"\n🏆 **Mayor generación de margen:** {mejor['region']} — {fmt_mxn(mejor['margen'])}\n"
        r += ("\n💡 **Insight:** Las regiones con más sucursales no siempre "
              "generan mayor margen. Evaluar densidad competitiva y surtido por región.")
        return r

    def _resp_oportunidad():
        total_op = kpis["venta_perdida"] + alertas["margen"]["impacto"] + alertas["churn_valor"]
        r = "### 🎯 Mapa de Oportunidades — Priorizado por Impacto\n\n"
        r += f"**Oportunidad total identificada: {fmt_mxn(total_op)}**\n\n"
        r += f"**1. Eliminar quiebres de stock** → {fmt_mxn(kpis['venta_perdida'])}\n"
        r += f"   - Forecast estacional + buffer en temporadas clave\n"
        r += f"   - Implementación: 4-6 semanas\n\n"
        r += f"**2. Optimizar canal mix** → {fmt_mxn(alertas['margen']['impacto'])}\n"
        r += f"   - Fortalecer Crédito SD vs marketplace\n"
        r += f"   - Ajustar descuentos por canal\n\n"
        r += f"**3. Reactivar sucursales en riesgo** → {fmt_mxn(alertas['churn_valor'])}\n"
        r += f"   - Plan de reactivación con {len(alertas['churn'])} sucursales identificadas\n"
        r += f"   - Acción: inmediata (2 semanas)\n\n"
        r += ("📌 **Estas oportunidades no requieren abrir nuevas sucursales** — "
              "son mejoras operativas con la infraestructura actual.")
        return r

    GEN = {
        "rentabilidad":   _resp_rentabilidad,
        "inventario":     _resp_inventario,
        "churn":          _resp_churn,
        "abc":            _resp_abc,
        "resumen":        _resp_resumen,
        "estacionalidad": _resp_estacionalidad,
        "canales":        _resp_canales,
        "regiones":       _resp_regiones,
        "oportunidad":    _resp_oportunidad,
    }

    if not matched:
        mc = rent_cli.groupby("canal")["margen_pct_real"].mean()
        gap = mc.max() - mc.min()
        return f"""Analicé tu pregunta: *"{pregunta}"*

Con base en los datos de Surtidora Departamental (2023-2024):

📈 **Ventas:** {fmt_mxn(kpis['venta_total'])} · Margen: {kpis['margen_pct']:.1f}%
📦 **Quiebres:** {fmt_mxn(kpis['venta_perdida'])} en venta perdida
💰 **Canales:** {rent_cli['canal'].nunique()} canales con hasta {gap:.1f} pts de diferencia en margen
🟣 **Sucursales:** {len(alertas['churn'])} con señales de baja actividad

Puedo profundizar en:
- 💰 **Rentabilidad** — márgenes por sucursal, canal o categoría
- 📦 **Inventario** — quiebres, temporadas, forecast
- 🌡️ **Estacionalidad** — Buen Fin, Navidad, Hot Sale, Día de las Madres
- 📊 **Canales** — e-commerce vs tienda física vs crédito SD
- 📍 **Regiones** — rendimiento por zona geográfica
- 🎯 **Oportunidades** — mapa de impacto priorizado

¿Sobre cuál quieres profundizar?"""

    parts = [GEN[t]() for t in matched[:3] if t in GEN]
    response = "\n\n---\n\n".join(parts)

    if len(matched) > 3:
        extras = ", ".join(f"**{t}**" for t in matched[3:])
        response += f"\n\n---\n\n💡 También detecté interés en: {extras}. Pregúntame para profundizar."

    return response


if pregunta:
    st.session_state.messages.append({"role": "user", "content": pregunta})
    with st.chat_message("user", avatar="👤"):
        st.markdown(pregunta)

    with st.chat_message("assistant", avatar="🏪"):
        if not api_key:
            respuesta = _demo_response(pregunta, kpis, rent_cli, abc_skus, perdidas, alertas)
            st.markdown(respuesta)
        else:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)

                messages_api = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                    if m["role"] in ["user", "assistant"]
                ]

                with st.spinner("Analizando datos..."):
                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1000,
                        system=SYSTEM_CONTEXT,
                        messages=messages_api,
                    )
                    respuesta = response.content[0].text
                st.markdown(respuesta)

            except ImportError:
                st.error("Instala anthropic: `pip install anthropic`")
                respuesta = "Error: librería anthropic no instalada."
            except Exception as e:
                respuesta = _demo_response(pregunta, kpis, rent_cli, abc_skus, perdidas, alertas)
                st.markdown(respuesta)
                st.caption(f"ℹ️ Modo demo (sin API): {str(e)[:80]}")

        st.session_state.messages.append({"role": "assistant", "content": respuesta})
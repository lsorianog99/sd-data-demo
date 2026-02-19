# 🌿 Alceda BI + IA — Proof of Concept

## Plataforma de Inteligencia de Negocios con IA para Distribuidoras de Alimentos

---

## Índice

1. [Visión General](#visión-general)
2. [Dashboard Ejecutivo — Vista General](#1-dashboard-ejecutivo)
3. [Alertas IA — Centro de Monitoreo Inteligente](#2-alertas-ia)
4. [Rentabilidad por Cliente y Canal](#3-rentabilidad)
5. [Inventario — Quiebres y Análisis ABC](#4-inventario)
6. [Forecast IA — Predicción de Demanda](#5-forecast-ia)
7. [Chat IA — Asistente de Negocio en Lenguaje Natural](#6-chat-ia)
8. [Datos Utilizados en la PoC](#datos-utilizados)
9. [Arquitectura Técnica](#arquitectura-técnica)
10. [Próximos Pasos](#próximos-pasos)

---

## Visión General

**Alceda BI + IA** es una plataforma de inteligencia de negocios diseñada específicamente para **distribuidoras de alimentos en México**. Integra análisis automatizado, detección de alertas con IA, predicción de demanda y un asistente conversacional — todo alimentado con los datos reales de la operación.

### ¿Qué problema resuelve?

Las distribuidoras de alimentos operan con márgenes ajustados (35-40%) y enfrentan tres problemas recurrentes que impactan directamente la utilidad:

| Problema | Impacto detectado en Alceda |
|----------|----------------------------|
| Quiebres de stock en temporada alta | **$10.8M MXN** en venta perdida |
| Erosión de margen por descuentos no controlados | **$26.7M MXN** en margen regalado |
| Clientes abandonando sin que nadie lo detecte | **$1.8M MXN** en venta anual en riesgo |
| **Total identificado** | **$39.3M MXN en oportunidades** |

> **Esta plataforma detecta estos problemas automáticamente y recomienda acciones concretas antes de que se conviertan en pérdidas.**

### Cifras clave del negocio analizado

| Indicador | Valor |
|-----------|-------|
| Venta total (2023-2024) | $2,137.9M MXN |
| Margen bruto | 35.9% ($766.8M MXN) |
| Clientes activos | 80 |
| SKUs en catálogo | 58 (8 marcas propias) |
| Canales de distribución | 12 |
| Registros de transacciones | 57,351 |

---

## 1. Dashboard Ejecutivo

### ¿Qué es?

El Dashboard Ejecutivo es la **vista de arranque** de la plataforma. Ofrece un panorama completo del negocio en una sola pantalla: KPIs principales, distribución de venta por canal, y un ranking de los 10 clientes más importantes con su margen real.

### ¿Qué muestra?

- **KPIs de cabecera:** Venta total, margen bruto (% y $), venta perdida por quiebres, SKUs Clase A
- **Distribución por canal:** Gráfica de pastel con los 12 canales y su participación porcentual (Retail Conveniencia: 22.2%, QSR: 19.6%, Retail Super: 17.8%, etc.)
- **Top 10 Clientes:** Tabla con nombre, canal, segmento, venta total, margen real post-descuento, descuento promedio y ticket promedio
- **Insights automáticos:** Alertas al pie sobre la regla 80/20 (37 de 58 SKUs generan el 80% del margen) y la oportunidad oculta ($10.8M MXN perdidos por quiebres)

### ¿Por qué es valioso?

Antes, obtener esta vista requería que alguien cruzara manualmente ventas, descuentos, inventario y clientes en Excel. Aquí **se genera automáticamente en tiempo real** y revela un insight crítico desde la primera pantalla: **los clientes de mayor volumen no siempre son los más rentables** — OXXO Región Norte genera $213.6M en venta pero solo 35.6% de margen, mientras que cuentas más pequeñas en canales como Dark Kitchen superan el 39%.

---

## 2. Alertas IA

### ¿Qué es?

El Centro de Alertas es el **sistema de detección temprana** de la plataforma. Funciona como un radar que monitorea continuamente los datos y dispara alertas cuando detecta situaciones que requieren acción inmediata.

### ¿Qué detecta?

La plataforma genera **tres tipos de alertas** automáticamente:

#### 🔴 Alertas de Quiebre de Stock Inminente
- Detecta SKUs cuyo inventario actual no cubre la demanda proyectada
- Calcula **días de inventario restantes** y la **venta en riesgo** si no se reabastece
- Prioriza por impacto económico para que el equipo de compras actúe primero donde más importa

#### 🟡 Alertas de Desviación de Margen
- Compara el margen real de cada canal vs. el margen de lista
- Identifica qué canales están **erosionando margen** por exceso de descuentos
- Cuantifica el impacto: cuántos pesos de margen se están dejando en la mesa

#### 🟣 Alertas de Clientes en Riesgo (Churn)
- Detecta clientes que llevan **18+ días sin comprar** — señal temprana de abandono
- Muestra nombre, canal, segmento y días de inactividad
- Calcula el **valor anual en riesgo** si el cliente se pierde

### ¿Por qué es valioso?

Sin este sistema, estas alertas las detecta un ejecutivo de forma reactiva — cuando ya perdió la venta o el cliente. Con Alceda BI + IA, el equipo comercial recibe **señales tempranas automatizadas** que les permiten actuar antes de que el problema se materialice.

---

## 3. Rentabilidad por Cliente y Canal

### ¿Qué es?

Este módulo responde la pregunta más importante que ningún ERP o Excel contesta bien: **¿cuál es mi margen real después de descuentos, por cliente y por canal?**

### ¿Qué muestra?

- **KPIs de cabecera:** Clientes en vista, venta total, margen promedio (38.1%), descuento promedio (2.7%)
- **Margen Real por Canal:** Gráfica de barras apiladas que muestra el margen de lista vs. la erosión por descuentos en cada uno de los 12 canales
- **Rentabilidad vs. Descuento:** Scatter plot donde cada punto es un cliente, posicionado por su margen y descuento — revela visualmente quién está dando demasiado descuento
- **Filtros interactivos:** Canal, segmento (A/B/C), ejecutivo — para analizar cualquier corte del negocio

### ¿Qué insights genera?

| Canal | Margen Real | Descuento Prom. | Observación |
|-------|------------|-----------------|-------------|
| Dark Kitchen | 39.1% | 0.9% | Mayor rentabilidad del portafolio |
| Catering | 38.8% | 1.2% | Alto margen, bajo volumen |
| Food Service | 38.7% | 1.5% | Oportunidad de crecimiento rentable |
| Retail Conveniencia | 35.6% | 6.0% | Mayor volumen, menor margen |
| QSR | 35.0% | 6.0% | Segundo en volumen, menor margen |

**Hallazgo clave — La Paradoja de Rentabilidad:**
Los canales que generan más volumen (Retail, QSR) son los que tienen menor margen, debido a descuentos comerciales de hasta 6%. Esto significa que **crecer en volumen en los canales actuales sin renegociar condiciones comerciales erosiona la utilidad del negocio.**

### ¿Por qué es valioso?

Permite a la dirección comercial tomar decisiones fundamentadas:
- Renegociar condiciones comerciales con datos concretos
- Priorizar crecimiento en canales de alto margen
- Identificar ejecutivos que ceden descuento excesivo vs. los que protegen rentabilidad

---

## 4. Inventario — Quiebres y Análisis ABC

### ¿Qué es?

El módulo de Inventario combina **análisis de quiebres históricos** con la **clasificación ABC** del catálogo para responder: ¿cuánto dinero perdimos por no tener producto?, y ¿en qué SKUs debemos enfocarnos?

### ¿Qué muestra?

#### Análisis de Quiebres
- **Venta perdida total:** $10.8M MXN por episodios de desabasto
- **Margen perdido total:** $4.3M MXN
- **Detalle por SKU:** Nombre del producto, temporada afectada, días sin stock, y el monto de venta/margen perdido
- **Análisis por temporada:** Verano (44% del impacto), Navideña (31%), Regular (25%)

#### Clasificación ABC
- **Clase A (37 SKUs):** 80% del margen — deben tener disponibilidad 100%
- **Clase B (8-10 SKUs):** 15% del margen — stock mínimo calculado
- **Clase C (11-13 SKUs):** 5.8% del margen — evaluar descontinuación o compra bajo pedido

### ¿Por qué es valioso?

Revela un patrón crítico: **los quiebres de stock ocurren precisamente en temporada alta**, cuando la demanda es 60-180% mayor que el promedio. Esto amplifica el impacto de cada día sin producto. El análisis ABC además permite concentrar el 100% de la atención de compras en los 37 SKUs que realmente mueven el negocio.

---

## 5. Forecast IA — Predicción de Demanda

### ¿Qué es?

El módulo de Forecast utiliza **modelos de series de tiempo** para proyectar la demanda de cada SKU a 8 semanas vista. Esto permite al equipo de compras anticiparse al mercado en lugar de reaccionar a los quiebres.

### ¿Qué muestra?

- **Gráfica de demanda:** Histórico de ventas en cajas (línea sólida) + proyección a futuro (línea punteada) con banda de confianza
- **Línea de corte:** Separación visual entre datos reales y forecast
- **Tabla semanal:** Demanda estimada semana por semana para los próximos 2 meses
- **Selector de SKU:** Permite analizar el forecast de cualquiera de los 58 SKUs del catálogo

### ¿Cómo funciona?

1. Toma el histórico de ventas semanales de cada SKU (2023-2024)
2. Aplica un modelo de suavizado exponencial (Holt-Winters) que captura tendencia y estacionalidad
3. Genera dos pronósticos: el escenario base y un ajuste estacional que amplifica o reduce la demanda según la temporada
4. El resultado se presenta con bandas de confianza para que compras tenga un rango de escenarios

### ¿Por qué es valioso?

Hoy, el equipo de compras decide cuánto pedir basándose en **intuición y el último pedido**. Con el Forecast IA, tienen una proyección cuantitativa que:
- **Anticipa picos de demanda** 4-8 semanas antes de que ocurran
- **Reduce quiebres** al elevar puntos de reorden antes de temporadas altas
- **Reduce sobreinventario** al bajar pedidos antes de temporadas bajas
- **Potencial de recuperación:** Hasta $5.4M MXN anuales si se reducen quiebres en 50%

---

## 6. Chat IA — Asistente de Negocio en Lenguaje Natural

### ¿Qué es?

El Chat IA es un **asistente conversacional** entrenado con todos los datos del negocio de Alceda. Permite hacer preguntas en español, en lenguaje natural, y obtener respuestas con datos reales, insights y recomendaciones accionables.

### ¿Qué puede responder?

| Tipo de pregunta | Ejemplo |
|------------------|---------|
| Rentabilidad | *"¿Cuál es mi cliente más rentable?"* |
| Inventario | *"¿Cuánto dinero perdí por quiebres?"* |
| Churn | *"¿Qué clientes están en riesgo de irse?"* |
| Canales | *"¿Qué canal debería priorizar para crecer?"* |
| ABC | *"¿Qué SKUs debo priorizar en inventario?"* |
| Estacionalidad | *"¿Qué variables externas nos ayudarían a predecir demanda?"* |
| Ejecutivos | *"¿Cómo se comparan los ejecutivos de cuenta?"* |
| Oportunidades | *"¿Dónde está la mayor oportunidad de mejora?"* |
| Resumen | *"Dame un resumen ejecutivo del negocio"* |

### Características clave

- **Multi-tema:** Entiende preguntas que combinan dos o tres temas (ej: *"Quiero ver rentabilidad e inventario"*) y combina las respuestas
- **Datos reales:** Cada respuesta incluye cifras concretas de Alceda, no texto genérico
- **9 categorías de análisis:** Cada una con insights específicos y recomendaciones accionables
- **Fallback inteligente:** Si la pregunta no coincide con ningún tema, muestra un resumen del negocio y sugiere áreas de análisis disponibles
- **Integración con Claude (Anthropic):** Cuando se configura una API key, las respuestas son generadas por un modelo de lenguaje avanzado con acceso a todo el contexto del negocio

### ¿Por qué es valioso?

Democratiza el acceso a los datos. El CEO, los socios, o cualquier ejecutivo puede **obtener insights complejos sin necesidad de abrir un Excel ni esperar a que alguien prepare un reporte**. Reduce la dependencia de analistas para preguntas operativas y permite tomar decisiones informadas en tiempo real.

---

## Datos Utilizados en la PoC

La PoC fue construida con **datos sintéticos realistas** que simulan la operación de una distribuidora de alimentos en México. La estructura de datos es la siguiente:

| Dataset | Descripción | Registros |
|---------|-------------|-----------|
| **Ventas** | Transacciones semanales por cliente × SKU (Ene 2023 – Dic 2024) | 57,351 |
| **Clientes** | Base de clientes con canal, segmento, ejecutivo, ubicación | 80 |
| **Productos** | Catálogo de SKUs con marca, categoría, precio, temporalidad | 58 |
| **Inventario** | Niveles de stock semanales por SKU con punto de reorden | Semanal |
| **Compras** | Órdenes de reabastecimiento con proveedor y costo | Semanal |
| **Rentabilidad** | Margen real por cliente post-descuentos (calculado) | 80 |
| **ABC** | Clasificación de SKUs por contribución al margen | 58 |
| **Pérdidas** | Episodios históricos de quiebre con impacto cuantificado | 6 |

### Marcas propias simuladas
La Prateria, Multichef, Sushida, Cremaní, Koctelazo, Avella, Sayulita, Ambiderm

### Canales de distribución
Retail Conveniencia, QSR, Retail Super, Retail Mayorista, Mayorista, Hotelero, Restaurante, Institucional, Dark Kitchen, Retail Descuento, Retail Regional, Catering

> **Nota:** Para la implementación real, estos datasets se conectarían directamente al ERP/WMS de Alceda mediante integración automatizada. La estructura ya está preparada para recibir datos reales con mínima adaptación.

---

## Arquitectura Técnica

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (Streamlit)               │
│  ┌──────┐ ┌────────┐ ┌─────────┐ ┌────────┐ ┌────┐│
│  │Dash. │ │Alertas │ │Rentab.  │ │Invent. │ │... ││
│  │Ejec. │ │  IA    │ │Canal/Cli│ │ABC/Quie│ │    ││
│  └──────┘ └────────┘ └─────────┘ └────────┘ └────┘│
├─────────────────────────────────────────────────────┤
│              Motor de Datos (Pandas)                 │
│  ┌──────────────────────────────────────────────┐   │
│  │  Load → Clean → Transform → Cache (st.cache) │   │
│  └──────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│               Módulos de IA                          │
│  ┌────────────┐ ┌──────────────┐ ┌──────────────┐  │
│  │ Forecast   │ │ Detección de │ │ Chat IA      │  │
│  │ (Holt-W.)  │ │ Alertas      │ │ (Claude API) │  │
│  └────────────┘ └──────────────┘ └──────────────┘  │
├─────────────────────────────────────────────────────┤
│           Fuentes de Datos                           │
│  ┌────────┐ ┌───────┐ ┌──────────┐ ┌────────────┐  │
│  │ Ventas │ │Client.│ │Productos │ │Inventario  │  │
│  │ (CSV)  │ │ (CSV) │ │  (CSV)   │ │   (CSV)    │  │
│  └────────┘ └───────┘ └──────────┘ └────────────┘  │
└─────────────────────────────────────────────────────┘
```

### Tecnologías utilizadas

| Componente | Tecnología |
|------------|-----------|
| Frontend | Streamlit (Python) |
| Visualización | Plotly + CSS personalizado |
| Motor de datos | Pandas con caching |
| Forecast | Holt-Winters / Suavizado exponencial |
| Chat IA | Anthropic Claude API |
| Deployment PoC | Streamlit Cloud / ngrok |

---

## Próximos Pasos

### Fase 1 — Integración de Datos Reales (2-4 semanas)
- Conectar directamente al ERP/WMS de Alceda
- Sustituir CSVs por consultas en tiempo real
- Validar cálculos con datos de producción

### Fase 2 — Mejoras de Modelo (4-6 semanas)
- Integrar variables externas al Forecast (calendario de eventos, clima, promos de clientes)
- Refinar modelo de detección de churn con datos históricos de cancelación
- Implementar alertas por correo electrónico y WhatsApp

### Fase 3 — Escalamiento (6-8 semanas)
- Dashboard de acceso multi-usuario con roles (CEO, Comercial, Compras)
- Integración con herramientas de comunicación del equipo
- APIs para alimentar sistemas de reabastecimiento automático

---

> **Esta PoC fue desarrollada para demostrar el potencial de una plataforma de BI + IA adaptada a las necesidades específicas de Alceda. Todas las cifras, cálculos y recomendaciones se generan automáticamente a partir de los datos del negocio.**

---

*Alceda BI + IA · v1.0 · Febrero 2025*

# 🏪 Surtidora Departamental BI + IA — Proof of Concept

> **Inteligencia real para tus datos** — Demo interactiva de Business Intelligence + Inteligencia Artificial para Surtidora Departamental

---

## 📋 ¿Qué incluye esta PoC?

| Página | Descripción |
|--------|-------------|
| 🏠 **Home** | Resumen ejecutivo con KPIs globales 2023-2024 |
| 🚨 **Alertas IA** | 3 alertas críticas generadas automáticamente por IA (el "wow" de la demo) |
| 💰 **Rentabilidad** | Análisis de margen real por canal, categoría y región |
| 📦 **Inventario** | Quiebres históricos, análisis ABC, ventas perdidas cuantificadas |
| 🔮 **Forecast IA** | Predicción de demanda por SKU para las próximas 8 semanas |
| 🤖 **Chat IA** | Asistente conversacional entrenado con datos de SD |

---

## ⚡ Instalación Rápida (Mac)

### Prerequisitos
- Python 3.10+ instalado ([python.org](https://www.python.org))
- Terminal (iTerm, Warp, o la nativa de Mac)

### Pasos

```bash
# 1. Navegar a la carpeta del proyecto
cd sd-data-poc

# 2. Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar API Key de Anthropic (para el Chat IA)
cp .env.example .env
# Editar .env y pegar tu API Key:
# ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxx

# 5. Lanzar la aplicación
streamlit run app.py
```

La app abrirá automáticamente en: **http://localhost:8501**

---

## 📁 Estructura del Proyecto

```
sd-data-poc/
├── app.py                          # Home - Resumen Ejecutivo
├── requirements.txt                # Dependencias Python
├── .env                            # Variables de entorno (API Key)
├── README.md                       # Este archivo
│
├── pages/
│   ├── 1_🚨_Alertas_IA.py         # Alertas inteligentes (centerpiece)
│   ├── 2_💰_Rentabilidad.py        # Análisis de rentabilidad
│   ├── 3_📦_Inventario.py          # Inventario y quiebres
│   ├── 4_🔮_Forecast_IA.py         # Predicción de demanda
│   └── 5_🤖_Chat_IA.py             # Asistente conversacional
│
├── utils/
│   ├── data_loader.py              # Carga y procesamiento de datos
│   └── ui.py                       # Componentes visuales y CSS
│
└── data/
    ├── generate_data.py            # Script para regenerar datos sintéticos
    ├── ventas.csv                  # ~65,000 transacciones (2023-2024)
    ├── clientes.csv                # 69 puntos de venta por canal y región
    ├── productos.csv               # 67 SKUs del catálogo SD
    ├── inventario.csv              # Snapshots semanales de stock
    ├── pedidos_compra.csv          # Órdenes de compra a proveedores
    ├── rentabilidad_clientes.csv   # KPIs de rentabilidad por punto de venta
    ├── analisis_abc_skus.csv       # Clasificación ABC del catálogo
    └── ventas_perdidas.csv         # Quiebres y ventas no realizadas
```

---

## 📊 Los Números de la Historia

```
Venta Total 2023-2024:       $3,630,333,382 MXN
Margen Bruto Total:          $1,197,288,852 MXN  (33.0%)
─────────────────────────────────────────────────
💀 Venta Perdida (quiebres):   $38,582,460 MXN
💀 Margen Perdido:              $11,035,755 MXN

Temporadas de quiebre:      Buen Fin, Navidad, Hot Sale, Día de las Madres
SKUs Clase A:                34 SKUs → 80% del margen
```

### El "Momento Wow" para la Dirección

> *Los canales digitales (Marketplace, E-commerce) generan alto volumen pero el MENOR margen.
> Crédito Surtidora, un canal propio, genera el MEJOR margen neto.
> Nadie en SD lo había cuantificado — hasta hoy.*

---

## 🔄 Regenerar Datos Sintéticos

```bash
cd data
python generate_data.py
```

---

## 🚀 Roadmap — Próximas Fases

- [ ] Conectar a ERP/POS real de SD
- [ ] Integrar datos de e-commerce en tiempo real
- [ ] Modelo de forecast con Prophet (mayor precisión)
- [ ] Alertas automáticas por WhatsApp / Email
- [ ] Dashboard móvil para gerentes de tienda
- [ ] Integración con sistema de compras (OCs reales)

---

*PoC desarrollada para Surtidora Departamental — Transformación Digital con IA*

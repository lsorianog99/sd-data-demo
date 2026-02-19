"""
Generador de Datos Sintéticos — Surtidora Departamental PoC
BI + IA: Inteligencia real para tus datos
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────
# PARÁMETROS GLOBALES
# ─────────────────────────────────────────────
START_DATE = datetime(2023, 1, 1)
END_DATE   = datetime(2024, 12, 31)
DATES      = pd.date_range(START_DATE, END_DATE, freq="D")

print("🚀 Iniciando generación de datos sintéticos Surtidora Departamental...")

# ─────────────────────────────────────────────
# 1. SUCURSALES / PUNTOS DE VENTA (equiv. a "clientes")
# ─────────────────────────────────────────────
print("\n📋 Generando sucursales y canales de venta...")

clientes_data = [
    # Tiendas Físicas — Jalisco (sede principal)
    ("SUC001", "SD Guadalajara Centro",       "Tienda Física",  "Jalisco",     "Carlos Herrera",  "A", 18000000),
    ("SUC002", "SD Tlaquepaque",               "Tienda Física",  "Jalisco",     "Carlos Herrera",  "A", 14000000),
    ("SUC003", "SD Zapopan Plaza del Sol",     "Tienda Física",  "Jalisco",     "Laura Mendoza",   "A", 16000000),
    ("SUC004", "SD Tonalá",                    "Tienda Física",  "Jalisco",     "Laura Mendoza",   "A", 12000000),
    ("SUC005", "SD Puerto Vallarta",           "Tienda Física",  "Jalisco",     "Carlos Herrera",  "B",  8500000),
    ("SUC006", "SD Lagos de Moreno",           "Tienda Física",  "Jalisco",     "Laura Mendoza",   "B",  6000000),
    ("SUC007", "SD Tepatitlán",                "Tienda Física",  "Jalisco",     "Carlos Herrera",  "B",  5500000),
    ("SUC008", "SD Chapala",                   "Tienda Física",  "Jalisco",     "Laura Mendoza",   "C",  3200000),

    # Tiendas Físicas — Otras regiones
    ("SUC009", "SD León Gto",                  "Tienda Física",  "Guanajuato",  "Roberto Díaz",    "A", 13000000),
    ("SUC010", "SD Aguascalientes Centro",     "Tienda Física",  "Aguascalientes","Roberto Díaz",  "A", 11000000),
    ("SUC011", "SD San Luis Potosí",           "Tienda Física",  "SLP",         "Roberto Díaz",    "B",  7500000),
    ("SUC012", "SD Colima",                    "Tienda Física",  "Colima",      "Laura Mendoza",   "B",  5000000),
    ("SUC013", "SD Morelia",                   "Tienda Física",  "Michoacán",   "Roberto Díaz",    "B",  6800000),
    ("SUC014", "SD Tepic",                     "Tienda Física",  "Nayarit",     "Carlos Herrera",  "C",  3800000),
    ("SUC015", "SD Zacatecas",                 "Tienda Física",  "Zacatecas",   "Roberto Díaz",    "C",  3500000),
    ("SUC016", "SD Querétaro",                 "Tienda Física",  "Querétaro",   "Roberto Díaz",    "B",  9000000),

    # E-commerce
    ("ECO001", "SD E-commerce Web",            "E-commerce",     "Nacional",    "Ana Torres",      "A", 25000000),
    ("ECO002", "SD App Móvil",                 "E-commerce",     "Nacional",    "Ana Torres",      "B",  8000000),

    # Marketplace
    ("MKP001", "SD en Mercado Libre",          "Marketplace",    "Nacional",    "Ana Torres",      "B",  6500000),
    ("MKP002", "SD en Amazon MX",              "Marketplace",    "Nacional",    "Ana Torres",      "C",  3000000),

    # Canal Crédito Surtidora (ventas a crédito propio — alto volumen)
    ("CRD001", "Crédito SD Jalisco",           "Crédito SD",     "Jalisco",     "Diana Ruiz",      "A", 20000000),
    ("CRD002", "Crédito SD Bajío",             "Crédito SD",     "Guanajuato",  "Diana Ruiz",      "A", 12000000),
    ("CRD003", "Crédito SD Occidente",         "Crédito SD",     "Colima",      "Diana Ruiz",      "B",  7000000),

    # Financiamiento terceros
    ("FIN001", "Ventas Kuesky Pay",            "Kuesky Pay",     "Nacional",    "Ana Torres",      "B",  4500000),
    ("FIN002", "Ventas Aplazo",                "Aplazo",         "Nacional",    "Ana Torres",      "C",  2800000),

    # Ventas Mayoreo / Corporativas
    ("MAY001", "Corporativo Hoteles GDL",      "Mayoreo",        "Jalisco",     "Carlos Herrera",  "B",  5000000),
    ("MAY002", "Gobierno del Estado Jalisco",  "Mayoreo",        "Jalisco",     "Diana Ruiz",      "C",  3500000),
    ("MAY003", "Uniformes Empresariales SA",   "Mayoreo",        "Nacional",    "Roberto Díaz",    "C",  2500000),

    # Sucursales más pequeñas y canales menores
    *[
        (f"SUC{16+i:03d}", f"SD Sucursal Regional {16+i}",
         random.choice(["Tienda Física", "Tienda Física", "Tienda Física"]),
         random.choice(["Jalisco", "Guanajuato", "Michoacán", "Colima", "Nayarit", "SLP", "Aguascalientes", "Querétaro"]),
         random.choice(["Carlos Herrera", "Laura Mendoza", "Roberto Díaz", "Diana Ruiz"]),
         "C",
         random.randint(1500000, 4500000))
        for i in range(1, 42)
    ]
]

clientes = pd.DataFrame(clientes_data, columns=[
    "cliente_id", "nombre", "canal", "region",
    "ejecutivo", "segmento", "venta_anual_potencial_mxn"
])

clientes["credito_dias"] = clientes["canal"].map({
    "Tienda Física": 0, "E-commerce": 0, "Marketplace": 0,
    "Crédito SD": 90, "Kuesky Pay": 0, "Aplazo": 0,
    "Mayoreo": 30,
}).fillna(0).astype(int)

clientes["fecha_alta"] = [
    START_DATE - timedelta(days=random.randint(180, 1800)) if i < 50
    else START_DATE + timedelta(days=random.randint(0, 400))
    for i in range(len(clientes))
]

clientes.to_csv(f"{OUTPUT_DIR}/clientes.csv", index=False)
print(f"  ✅ {len(clientes)} puntos de venta generados")


# ─────────────────────────────────────────────
# 2. PRODUCTOS (catálogo retail SD)
# ─────────────────────────────────────────────
print("\n📦 Generando catálogo de productos...")

productos_data = [
    # SKU, Nombre, Marca, Categoría, Precio_lista, Costo, Peso_kg, Uds/caja, Rotación, Temporalidad

    # SMARTPHONES
    ("SKU001", "iPhone 15 128GB",                 "Apple",      "Smartphones",    18999, 15200,  0.3,  1, "alta",   "buen_fin_navidad"),
    ("SKU002", "iPhone 15 Pro Max 256GB",         "Apple",      "Smartphones",    28999, 23200,  0.3,  1, "media",  "buen_fin_navidad"),
    ("SKU003", "Samsung Galaxy S24 128GB",        "Samsung",    "Smartphones",    16499, 12375,  0.3,  1, "alta",   "buen_fin_navidad"),
    ("SKU004", "Samsung Galaxy A15 64GB",         "Samsung",    "Smartphones",     4299,  2580,  0.3,  1, "alta",   "todo_año"),
    ("SKU005", "Xiaomi Redmi Note 13 128GB",      "Xiaomi",     "Smartphones",     4999,  2750,  0.3,  1, "alta",   "todo_año"),
    ("SKU006", "Motorola Moto G54 128GB",         "Motorola",   "Smartphones",     5499,  3300,  0.3,  1, "alta",   "todo_año"),

    # LAPTOPS Y TABLETS
    ("SKU007", "Laptop HP 15 Core i5 8GB/512SSD", "HP",         "Laptops",        14999, 11250,  2.5,  1, "alta",   "regreso_clases"),
    ("SKU008", "Laptop Lenovo IdeaPad 15 Ryzen5", "Lenovo",     "Laptops",        12999,  9100,  2.5,  1, "alta",   "regreso_clases"),
    ("SKU009", "MacBook Air M2 256GB",            "Apple",      "Laptops",        24999, 20000,  1.5,  1, "media",  "buen_fin_navidad"),
    ("SKU010", "Tablet Samsung Galaxy Tab A9",    "Samsung",    "Laptops",         4999,  3250,  0.5,  1, "media",  "regreso_clases"),

    # TVs
    ("SKU011", 'Smart TV Samsung 55" 4K',         "Samsung",    "TVs",            10999,  7700,  15.0, 1, "alta",   "buen_fin_navidad"),
    ("SKU012", 'Smart TV LG 50" 4K',              "LG",         "TVs",             8999,  5850,  14.0, 1, "alta",   "buen_fin_navidad"),
    ("SKU013", 'Smart TV Hisense 65" 4K',         "Hisense",    "TVs",            12999,  8450,  20.0, 1, "media",  "buen_fin_navidad"),
    ("SKU014", 'Smart TV TCL 43" FHD',            "TCL",        "TVs",             5499,  3300,  10.0, 1, "alta",   "todo_año"),

    # LÍNEA BLANCA
    ("SKU015", "Refrigerador Samsung 14ft",       "Samsung",    "Línea Blanca",   14999, 10500,  60.0, 1, "media",  "hot_sale"),
    ("SKU016", "Lavadora LG 20kg Inverter",       "LG",         "Línea Blanca",   13499,  9450,  45.0, 1, "media",  "hot_sale"),
    ("SKU017", "Estufa Whirlpool 6 Quemadores",   "Whirlpool",  "Línea Blanca",    8999,  5850,  50.0, 1, "media",  "todo_año"),
    ("SKU018", "Microondas LG 1.4ft Inverter",    "LG",         "Línea Blanca",    4499,  2700,   8.0, 1, "alta",   "todo_año"),
    ("SKU019", "Aire Acondicionado Samsung 1Ton", "Samsung",    "Línea Blanca",    9999,  6500,  35.0, 1, "media",  "verano"),

    # CALZADO HOMBRE
    ("SKU020", "Tenis Nike Air Max 90",           "Nike",       "Calzado",         2899,  1450,   1.0, 1, "alta",   "todo_año"),
    ("SKU021", "Tenis Puma RS-X",                 "Puma",       "Calzado",         2499,  1250,   1.0, 1, "alta",   "todo_año"),
    ("SKU022", "Zapato LOB Casual Hombre",        "LOB",        "Calzado",         1899,  1045,   0.8, 1, "alta",   "todo_año"),
    ("SKU023", "Bota Andrea Hombre",              "Andrea",     "Calzado",         1599,   800,   1.2, 1, "media",  "invierno"),
    ("SKU024", "Tenis Adidas Superstar",          "Adidas",     "Calzado",         2199,  1100,   1.0, 1, "alta",   "todo_año"),

    # CALZADO MUJER
    ("SKU025", "Tenis Nike Revolution 7 Mujer",   "Nike",       "Calzado",         1999,  1000,   0.8, 1, "alta",   "todo_año"),
    ("SKU026", "Sandalia Andrea Mujer",            "Andrea",     "Calzado",          999,   500,   0.5, 1, "alta",   "verano"),
    ("SKU027", "Bota LOB Mujer Chelsea",           "LOB",        "Calzado",         2299,  1150,   1.0, 1, "media",  "invierno"),
    ("SKU028", "Zapato Flexi Mujer Confort",       "Flexi",      "Calzado",         1299,   650,   0.7, 1, "alta",   "todo_año"),

    # ROPA HOMBRE
    ("SKU029", "Jeans Lee Hombre Slim Fit",        "Lee",        "Ropa",            1099,   550,   0.6, 1, "alta",   "todo_año"),
    ("SKU030", "Playera Polo Hombre",              "Levi's",     "Ropa",             799,   360,   0.3, 1, "alta",   "todo_año"),
    ("SKU031", "Chamarra Aéropostale Hombre",      "Aéropostale","Ropa",            1899,   950,   0.8, 1, "media",  "invierno"),
    ("SKU032", "Camisa Formal Hombre",             "LOB",        "Ropa",             999,   500,   0.3, 1, "media",  "todo_año"),

    # ROPA MUJER
    ("SKU033", "Jeans Lee Mujer Skinny",           "Lee",        "Ropa",             999,   500,   0.5, 1, "alta",   "todo_año"),
    ("SKU034", "Blusa Casual Mujer",               "Levi's",     "Ropa",             699,   315,   0.2, 1, "alta",   "todo_año"),
    ("SKU035", "Vestido Andrea Mujer",             "Andrea",     "Ropa",            1499,   750,   0.4, 1, "media",  "verano"),
    ("SKU036", "Chamarra Mujer Acolchada",         "Aéropostale","Ropa",            2199,  1100,   0.9, 1, "media",  "invierno"),

    # PERFUMES / FRAGANCIAS
    ("SKU037", "Carolina Herrera Good Girl 80ml",  "Carolina Herrera", "Perfumes",   3499,  1750,  0.3, 1, "alta",   "dia_madres_navidad"),
    ("SKU038", "Hugo Boss Bottled 100ml",          "Hugo Boss",  "Perfumes",         2499,  1250,  0.3, 1, "alta",   "navidad"),
    ("SKU039", "Versace Eros 100ml",               "Versace",    "Perfumes",         2799,  1400,  0.3, 1, "alta",   "navidad"),
    ("SKU040", "Dolce & Gabbana Light Blue 100ml", "D&G",        "Perfumes",         2299,  1150,  0.3, 1, "media",  "dia_madres_navidad"),
    ("SKU041", "Perfume Zara Mujer 90ml",          "Zara",       "Perfumes",          699,   280,  0.3, 1, "alta",   "todo_año"),

    # COLCHONES
    ("SKU042", "Colchón Restonic Matrimonial",     "Restonic",   "Colchones",        8999,  4950,  25.0, 1, "media", "hot_sale"),
    ("SKU043", "Colchón Wendy Matrimonial",        "Wendy",      "Colchones",        6999,  3850,  23.0, 1, "media", "hot_sale"),
    ("SKU044", "Colchón Spring Air Individual",    "Spring Air", "Colchones",        4999,  2750,  18.0, 1, "media", "todo_año"),
    ("SKU045", "Base + Colchón Restonic Queen",    "Restonic",   "Colchones",       14999,  8250,  35.0, 1, "baja",  "buen_fin_navidad"),

    # JUGUETES
    ("SKU046", "Barbie Dreamhouse",                "Mattel",     "Juguetes",         3999,  2000,   5.0, 1, "alta",  "navidad"),
    ("SKU047", "Hot Wheels Pista Épica",           "Mattel",     "Juguetes",         1299,   650,   2.5, 1, "alta",  "navidad"),
    ("SKU048", "Monopoly Clásico",                 "Hasbro",     "Juguetes",          599,   300,   1.5, 1, "alta",  "navidad"),
    ("SKU049", "LEGO City Set Bomberos",           "LEGO",       "Juguetes",         1499,   750,   1.0, 1, "alta",  "navidad"),
    ("SKU050", "Nerf Elite 2.0",                   "Hasbro",     "Juguetes",          899,   450,   1.2, 1, "alta",  "navidad"),

    # BICICLETAS
    ("SKU051", "Bicicleta Mountain Bike R29",      "Benotto",    "Bicicletas",       5999,  3000,  14.0, 1, "media", "verano"),
    ("SKU052", "Bicicleta Urbana R26 Mujer",       "Mercurio",   "Bicicletas",       3999,  2000,  12.0, 1, "media", "verano"),
    ("SKU053", "Bicicleta Infantil R16",           "Benotto",    "Bicicletas",       2499,  1250,   8.0, 1, "alta",  "navidad"),

    # CUIDADO PERSONAL / BELLEZA
    ("SKU054", "Plancha Cabello Conair",           "Conair",     "Belleza",          1299,   650,   0.5, 1, "alta",  "dia_madres_navidad"),
    ("SKU055", "Secadora Cabello Revlon",          "Revlon",     "Belleza",           999,   500,   0.8, 1, "alta",  "dia_madres_navidad"),
    ("SKU056", "Rasuradora Philips OneBlade",      "Philips",    "Belleza",          1199,   600,   0.3, 1, "alta",  "todo_año"),
    ("SKU057", "Kit Skin Care 5 Pasos",            "Neutrogena", "Belleza",           899,   450,   0.5, 1, "media", "todo_año"),

    # ACCESORIOS TECH
    ("SKU058", "Audífonos Sony WH-1000XM5",       "Sony",       "Accesorios Tech",  6999,  4550,   0.3, 1, "media", "buen_fin_navidad"),
    ("SKU059", "Apple AirPods Pro 2",              "Apple",      "Accesorios Tech",  5499,  3850,   0.1, 1, "alta",  "buen_fin_navidad"),
    ("SKU060", "Smart Watch Xiaomi Band 8",        "Xiaomi",     "Accesorios Tech",  1299,   650,   0.1, 1, "alta",  "todo_año"),
    ("SKU061", "Bocina JBL Flip 6",                "JBL",        "Accesorios Tech",  2499,  1500,   0.5, 1, "alta",  "todo_año"),
    ("SKU062", "Power Bank 20000mAh",              "Xiaomi",     "Accesorios Tech",   699,   350,   0.4, 1, "alta",  "todo_año"),

    # HOGAR
    ("SKU063", "Licuadora Oster 10 Vel",           "Oster",      "Hogar",            1499,   750,   3.0, 1, "alta",  "dia_madres_navidad"),
    ("SKU064", "Cafetera Nespresso Vertuo",        "Nespresso",  "Hogar",            3499,  2100,   4.0, 1, "media", "buen_fin_navidad"),
    ("SKU065", "Aspiradora Robot iRobot",          "iRobot",     "Hogar",            7999,  4800,   4.0, 1, "baja",  "buen_fin_navidad"),
    ("SKU066", "Freidora de Aire 5.5L",            "Oster",      "Hogar",            2499,  1250,   5.0, 1, "alta",  "hot_sale"),
    ("SKU067", "Sartén Set 5pz Antiadherente",     "T-Fal",      "Hogar",            1999,  1000,   3.0, 1, "media", "todo_año"),
]

productos = pd.DataFrame(productos_data, columns=[
    "sku", "nombre", "marca", "categoria",
    "precio_lista_mxn", "costo_mxn", "peso_kg",
    "unidades_por_caja", "rotacion_esperada", "temporalidad"
])
productos["margen_bruto_pct"] = ((productos["precio_lista_mxn"] - productos["costo_mxn"]) / productos["precio_lista_mxn"] * 100).round(1)

productos.to_csv(f"{OUTPUT_DIR}/productos.csv", index=False)
print(f"  ✅ {len(productos)} SKUs generados")


# ─────────────────────────────────────────────
# HELPER: Factor de estacionalidad retail
# ─────────────────────────────────────────────
def estacionalidad_factor(fecha, temporalidad):
    mes = fecha.month
    dia = fecha.day

    base = 1.0

    # Buen Fin (tercera semana de noviembre)
    es_buen_fin = (mes == 11 and 13 <= dia <= 20)
    # Hot Sale (última semana mayo — primera junio)
    es_hot_sale = (mes == 5 and dia >= 25) or (mes == 6 and dia <= 5)
    # Día de las Madres (1-10 mayo)
    es_dia_madres = (mes == 5 and dia <= 10)

    if temporalidad == "todo_año":
        if mes in [11, 12]: base *= 1.3
        elif mes in [5]: base *= 1.15
        elif mes in [1, 2]: base *= 0.8

    elif temporalidad == "buen_fin_navidad":
        if es_buen_fin: base *= 2.8
        elif mes == 12: base *= 2.2
        elif mes == 11: base *= 1.5
        elif mes in [1, 2, 3]: base *= 0.5
        else: base *= 0.8

    elif temporalidad == "navidad":
        if mes == 12: base *= 3.0
        elif mes == 11: base *= 1.8
        elif mes in [10]: base *= 1.3
        elif mes in [1, 2, 3, 4]: base *= 0.4
        else: base *= 0.7

    elif temporalidad == "hot_sale":
        if es_hot_sale: base *= 2.5
        elif mes in [5, 6]: base *= 1.6
        elif mes == 11: base *= 1.4  # Buen Fin también
        elif mes in [1, 2]: base *= 0.6
        else: base *= 0.9

    elif temporalidad == "dia_madres_navidad":
        if es_dia_madres: base *= 2.8
        elif mes == 5: base *= 1.8
        elif mes == 12: base *= 2.2
        elif mes == 11: base *= 1.5
        elif mes == 2 and dia >= 10: base *= 1.5  # San Valentín
        elif mes in [1, 3]: base *= 0.6
        else: base *= 0.8

    elif temporalidad == "regreso_clases":
        if mes in [8, 9]: base *= 2.0
        elif mes in [1]: base *= 1.6  # regreso enero
        elif mes == 11: base *= 1.3
        elif mes in [4, 5, 6]: base *= 0.6
        else: base *= 0.9

    elif temporalidad == "verano":
        if mes in [5, 6, 7, 8]: base *= 1.8
        elif mes in [11, 12, 1]: base *= 0.5
        else: base *= 0.9

    elif temporalidad == "invierno":
        if mes in [10, 11, 12, 1]: base *= 1.8
        elif mes in [5, 6, 7]: base *= 0.3
        else: base *= 0.7

    return base


def canal_categoria_affinity(canal, categoria):
    """Qué tan probable es que un canal venda una categoría"""
    affinities = {
        "Tienda Física":  {"Calzado": 1.8, "Ropa": 1.8, "Colchones": 2.0, "Línea Blanca": 1.6,
                           "Perfumes": 1.5, "Bicicletas": 1.5, "Juguetes": 1.4, "Hogar": 1.5,
                           "Belleza": 1.5, "Smartphones": 1.2, "TVs": 1.3, "Laptops": 1.0},
        "E-commerce":     {"Smartphones": 2.0, "Laptops": 1.8, "TVs": 1.6, "Accesorios Tech": 2.0,
                           "Perfumes": 1.6, "Belleza": 1.5, "Ropa": 1.3, "Calzado": 1.2,
                           "Hogar": 1.4, "Juguetes": 1.3, "Colchones": 0.8},
        "Marketplace":    {"Smartphones": 1.8, "Accesorios Tech": 2.0, "Laptops": 1.5,
                           "Belleza": 1.3, "Hogar": 1.2, "Calzado": 0.7, "Ropa": 0.6},
        "Crédito SD":     {"Línea Blanca": 2.2, "Colchones": 2.0, "TVs": 1.8, "Smartphones": 1.5,
                           "Laptops": 1.5, "Bicicletas": 1.4, "Calzado": 1.3, "Ropa": 1.2},
        "Kuesky Pay":     {"Smartphones": 1.8, "TVs": 1.5, "Calzado": 1.3, "Ropa": 1.3,
                           "Perfumes": 1.2, "Belleza": 1.2},
        "Aplazo":         {"Smartphones": 1.6, "Laptops": 1.4, "Calzado": 1.3, "Ropa": 1.2},
        "Mayoreo":        {"Ropa": 1.8, "Calzado": 1.5, "Línea Blanca": 1.3, "Hogar": 1.4},
    }
    canal_aff = affinities.get(canal, {})
    return canal_aff.get(categoria, 1.0)


# ─────────────────────────────────────────────
# 3. VENTAS — el corazón de la PoC
# ─────────────────────────────────────────────
print("\n💰 Generando ventas (esto toma un momento)...")

SKUS_ESTRELLA = ["SKU001", "SKU003", "SKU011", "SKU020", "SKU029", "SKU037",
                 "SKU046", "SKU015", "SKU042", "SKU054", "SKU059", "SKU066"]

QUIEBRES_PROGRAMADOS = {
    "SKU001": [(datetime(2023, 11, 15), datetime(2023, 12, 2)),    # iPhone en Buen Fin / inicio Navidad
               (datetime(2024, 11, 14), datetime(2024, 11, 22))],
    "SKU046": [(datetime(2023, 12, 5), datetime(2023, 12, 20)),    # Barbie en Navidad
               (datetime(2024, 12, 8), datetime(2024, 12, 22))],
    "SKU011": [(datetime(2024, 11, 12), datetime(2024, 11, 25))],  # TV Samsung Buen Fin
    "SKU037": [(datetime(2023, 5, 1), datetime(2023, 5, 10))],     # Perfume Día de las Madres
    "SKU015": [(datetime(2024, 5, 27), datetime(2024, 6, 8))],     # Refrigerador Hot Sale
}

def esta_en_quiebre(sku, fecha):
    for inicio, fin in QUIEBRES_PROGRAMADOS.get(sku, []):
        if inicio <= fecha <= fin:
            return True
    return False

ventas_rows = []
freq_compra = {"A": 2, "B": 5, "C": 12}

cliente_sku_catalogo = {}

for _, cliente in clientes.iterrows():
    n_skus = {"A": random.randint(25, 50), "B": random.randint(12, 25), "C": random.randint(5, 15)}[cliente["segmento"]]

    pesos = []
    for _, prod in productos.iterrows():
        aff = canal_categoria_affinity(cliente["canal"], prod["categoria"])
        pesos.append(aff)
    pesos = np.array(pesos)
    pesos = pesos / pesos.sum()

    skus_cliente = np.random.choice(productos["sku"].values, size=min(n_skus, len(productos)), replace=False, p=pesos)
    cliente_sku_catalogo[cliente["cliente_id"]] = skus_cliente

    es_churn = cliente["segmento"] == "B" and random.random() < 0.12
    fecha_churn = datetime(2024, random.randint(8, 11), random.randint(1, 28)) if es_churn else None

    fecha_actual = max(START_DATE, cliente["fecha_alta"])
    if isinstance(fecha_actual, pd.Timestamp):
        fecha_actual = fecha_actual.to_pydatetime()

    while fecha_actual <= END_DATE:
        if fecha_churn and fecha_actual >= fecha_churn:
            break

        dias_siguiente = int(np.random.normal(freq_compra[cliente["segmento"]], freq_compra[cliente["segmento"]] * 0.4))
        dias_siguiente = max(1, dias_siguiente)

        n_skus_pedido = max(1, int(np.random.normal(len(skus_cliente) * 0.3, len(skus_cliente) * 0.15)))
        skus_pedido = random.sample(list(skus_cliente), min(n_skus_pedido, len(skus_cliente)))

        metodo_pago = random.choices(
            ["Contado", "Crédito SD", "Tarjeta Crédito", "Kuesky Pay", "Aplazo", "Transferencia"],
            weights=[0.25, 0.30, 0.20, 0.10, 0.08, 0.07]
        )[0]

        for sku in skus_pedido:
            if esta_en_quiebre(sku, fecha_actual):
                continue

            prod = productos[productos["sku"] == sku].iloc[0]
            factor_est = estacionalidad_factor(fecha_actual, prod["temporalidad"])

            vol_base = {"A": random.randint(3, 25), "B": random.randint(1, 10), "C": random.randint(1, 4)}[cliente["segmento"]]
            cantidad_uds = max(1, int(vol_base * factor_est * np.random.normal(1.0, 0.25)))

            # Descuentos: e-commerce y marketplace dan más descuento
            desc_max = {
                "Tienda Física": 0.08, "E-commerce": 0.15, "Marketplace": 0.18,
                "Crédito SD": 0.05, "Kuesky Pay": 0.10, "Aplazo": 0.12,
                "Mayoreo": 0.20,
            }.get(cliente["canal"], 0.08)
            descuento_pct = round(random.uniform(0, desc_max), 3)

            precio_neto = round(prod["precio_lista_mxn"] * (1 - descuento_pct), 2)
            monto_total = round(precio_neto * cantidad_uds, 2)
            costo_total = round(prod["costo_mxn"] * cantidad_uds, 2)
            margen_mxn  = round(monto_total - costo_total, 2)

            ventas_rows.append({
                "fecha":           fecha_actual.strftime("%Y-%m-%d"),
                "cliente_id":      cliente["cliente_id"],
                "sku":             sku,
                "canal_pedido":    cliente["canal"],
                "region":          cliente["region"],
                "ejecutivo":       cliente["ejecutivo"],
                "cantidad_cajas":  cantidad_uds,
                "precio_lista":    prod["precio_lista_mxn"],
                "descuento_pct":   round(descuento_pct * 100, 1),
                "precio_neto":     precio_neto,
                "monto_total_mxn": monto_total,
                "costo_total_mxn": costo_total,
                "margen_bruto_mxn":margen_mxn,
                "margen_pct":      round((margen_mxn / monto_total * 100) if monto_total > 0 else 0, 1),
                "metodo_pago":     metodo_pago,
            })

        fecha_actual += timedelta(days=dias_siguiente)

ventas = pd.DataFrame(ventas_rows)
ventas["fecha"] = pd.to_datetime(ventas["fecha"])
ventas = ventas.sort_values("fecha").reset_index(drop=True)
ventas["venta_id"] = [f"VTA{i+1:06d}" for i in range(len(ventas))]
ventas.to_csv(f"{OUTPUT_DIR}/ventas.csv", index=False)
print(f"  ✅ {len(ventas):,} registros de ventas generados")
print(f"     Período: {ventas['fecha'].min().date()} → {ventas['fecha'].max().date()}")
print(f"     Venta total: ${ventas['monto_total_mxn'].sum():,.0f} MXN")
print(f"     Margen total: ${ventas['margen_bruto_mxn'].sum():,.0f} MXN")


# ─────────────────────────────────────────────
# 4. INVENTARIO (snapshots semanales)
# ─────────────────────────────────────────────
print("\n📦 Generando inventario semanal...")

semanas = pd.date_range(START_DATE, END_DATE, freq="W-MON")
inventario_rows = []

demanda_semanal = ventas.copy()
demanda_semanal["semana"] = pd.to_datetime(demanda_semanal["fecha"]).dt.to_period("W").apply(lambda r: r.start_time)
demanda_sku_semana = demanda_semanal.groupby(["semana", "sku"])["cantidad_cajas"].sum().reset_index()

for _, prod in productos.iterrows():
    sku = prod["sku"]
    stock_actual = random.randint(50, 300)

    for semana in semanas:
        dem = demanda_sku_semana[(demanda_sku_semana["semana"] == semana) & (demanda_sku_semana["sku"] == sku)]
        demanda = dem["cantidad_cajas"].sum() if len(dem) > 0 else 0

        punto_reorden = demanda * 3 if demanda > 0 else 20
        reabasto = 0
        if stock_actual < punto_reorden:
            reabasto = int(demanda * random.uniform(4, 8))
            stock_actual += reabasto

        quiebre = esta_en_quiebre(sku, semana.to_pydatetime()) and prod["rotacion_esperada"] in ["alta", "media"]
        if quiebre:
            stock_actual = random.randint(0, 3)

        stock_post = max(0, stock_actual - demanda)
        dias_inv = round(stock_post / (demanda / 7 + 0.001), 1) if demanda > 0 else 999.0
        dias_inv = min(dias_inv, 365)

        merma = max(0, int(stock_post * random.uniform(0, 0.008)))

        inventario_rows.append({
            "semana":           semana.strftime("%Y-%m-%d"),
            "sku":              sku,
            "stock_cajas":      int(stock_post),
            "demanda_semana":   int(demanda),
            "reabasto_cajas":   int(reabasto),
            "dias_inventario":  dias_inv,
            "quiebre_stock":    1 if (stock_post == 0 and demanda > 0) or quiebre else 0,
            "merma_cajas":      merma,
            "punto_reorden":    int(punto_reorden),
        })

        stock_actual = stock_post - merma

inventario = pd.DataFrame(inventario_rows)
n_quiebres = inventario["quiebre_stock"].sum()
inventario.to_csv(f"{OUTPUT_DIR}/inventario.csv", index=False)
print(f"  ✅ {len(inventario):,} registros de inventario generados")
print(f"     Quiebres de stock detectados: {n_quiebres} semana-SKU")


# ─────────────────────────────────────────────
# 5. PEDIDOS DE COMPRA A PROVEEDORES
# ─────────────────────────────────────────────
print("\n🛒 Generando pedidos de compra...")

proveedores_por_marca = {
    "Apple":      "PROV001 - Apple México Distribución",
    "Samsung":    "PROV002 - Samsung Electronics MX",
    "LG":         "PROV003 - LG Electronics México",
    "Nike":       "PROV004 - Nike de México",
    "Puma":       "PROV005 - Puma Sports MX",
    "LOB":        "PROV006 - LOB Footwear México",
    "Andrea":     "PROV007 - Andrea Distribución",
    "Lee":        "PROV008 - VF Corporation MX",
    "Levi's":     "PROV008 - VF Corporation MX",
    "Mattel":     "PROV009 - Mattel de México",
    "Hasbro":     "PROV010 - Hasbro México",
    "Whirlpool":  "PROV011 - Whirlpool México",
    "Restonic":   "PROV012 - Restonic de México",
    "Conair":     "PROV013 - Conair México",
    "HP":         "PROV014 - HP Inc México",
    "Lenovo":     "PROV015 - Lenovo México",
    "Sony":       "PROV016 - Sony México",
    "JBL":        "PROV017 - Harman International",
    "Xiaomi":     "PROV018 - Xiaomi Technology MX",
    "Motorola":   "PROV019 - Motorola Mobility MX",
    "Hisense":    "PROV020 - Hisense México",
    "TCL":        "PROV021 - TCL Electronics MX",
    "Adidas":     "PROV022 - Adidas México",
    "Flexi":      "PROV023 - Calzado Flexi",
    "Benotto":    "PROV024 - Bicicletas Benotto",
    "Mercurio":   "PROV025 - Bicicletas Mercurio",
    "Carolina Herrera": "PROV026 - Puig México",
    "Hugo Boss":  "PROV026 - Puig México",
    "Versace":    "PROV027 - Grupo Coty MX",
    "D&G":        "PROV028 - Dolce & Gabbana MX",
    "Zara":       "PROV029 - Inditex Fragancias",
    "Oster":      "PROV030 - Newell Brands MX",
    "T-Fal":      "PROV031 - Groupe SEB MX",
    "Nespresso":  "PROV032 - Nestlé Nespresso MX",
    "iRobot":     "PROV033 - iRobot Distribución",
    "Wendy":      "PROV034 - Colchones Wendy",
    "Spring Air": "PROV035 - Spring Air México",
    "LEGO":       "PROV036 - LEGO México",
    "Aéropostale":"PROV037 - Aéropostale MX",
    "Revlon":     "PROV038 - Revlon MX",
    "Philips":    "PROV039 - Philips México",
    "Neutrogena": "PROV040 - Johnson & Johnson MX",
}

lead_times = {
    "Apple": (5, 10), "Samsung": (7, 14), "LG": (7, 14),
    "Nike": (14, 28), "Puma": (14, 28), "LOB": (7, 14),
    "Andrea": (7, 12), "Lee": (14, 21), "Mattel": (10, 20),
    "Hasbro": (10, 20), "Whirlpool": (7, 14), "Restonic": (5, 10),
}

compras_rows = []
for row in inventario_rows:
    if row["reabasto_cajas"] > 0:
        prod = productos[productos["sku"] == row["sku"]]
        if len(prod) == 0:
            continue
        prod = prod.iloc[0]
        proveedor = proveedores_por_marca.get(prod["marca"], "PROV099 - Proveedor Genérico")
        lt_min, lt_max = lead_times.get(prod["marca"], (10, 20))
        lead_time = random.randint(lt_min, lt_max)
        fecha_pedido = datetime.strptime(row["semana"], "%Y-%m-%d") - timedelta(days=lead_time)

        factor_costo = np.random.normal(1.0, 0.03)
        costo_real = round(prod["costo_mxn"] * factor_costo, 2)

        compras_rows.append({
            "oc_id":            f"OC{len(compras_rows)+1:05d}",
            "fecha_pedido":     fecha_pedido.strftime("%Y-%m-%d"),
            "fecha_recepcion_esperada": row["semana"],
            "proveedor":        proveedor,
            "sku":              row["sku"],
            "marca":            prod["marca"],
            "cantidad_cajas":   row["reabasto_cajas"],
            "costo_unitario":   costo_real,
            "monto_total_mxn":  round(costo_real * row["reabasto_cajas"], 2),
            "lead_time_dias":   lead_time,
            "condicion_pago":   random.choice(["30 días", "45 días", "60 días", "Contado"]),
            "recibido":         1 if datetime.strptime(row["semana"], "%Y-%m-%d") <= END_DATE else 0,
        })

compras = pd.DataFrame(compras_rows)
compras.to_csv(f"{OUTPUT_DIR}/pedidos_compra.csv", index=False)
print(f"  ✅ {len(compras):,} órdenes de compra generadas")


# ─────────────────────────────────────────────
# 6. VENTAS PERDIDAS
# ─────────────────────────────────────────────
print("\n💸 Calculando ventas perdidas por quiebre de stock...")

perdidas_rows = []
for sku, periodos in QUIEBRES_PROGRAMADOS.items():
    prod = productos[productos["sku"] == sku].iloc[0]
    for inicio, fin in periodos:
        dias_quiebre = (fin - inicio).days
        ventas_sku = ventas[ventas["sku"] == sku]
        demanda_diaria_prom = ventas_sku["cantidad_cajas"].sum() / max(1, len(ventas_sku["fecha"].dt.date.unique()))

        factor = estacionalidad_factor(inicio, prod["temporalidad"])

        uds_perdidas = int(demanda_diaria_prom * dias_quiebre * factor * 1.3)
        venta_perdida = round(uds_perdidas * prod["precio_lista_mxn"] * 0.90, 2)
        margen_perdido = round(uds_perdidas * (prod["precio_lista_mxn"] - prod["costo_mxn"]) * 0.90, 2)

        temporada_lbl = "Buen Fin" if inicio.month == 11 else "Navidad" if inicio.month == 12 else "Día de las Madres" if inicio.month == 5 and inicio.day <= 10 else "Hot Sale" if inicio.month in [5,6] else "Regular"

        perdidas_rows.append({
            "sku":              sku,
            "nombre":           prod["nombre"],
            "marca":            prod["marca"],
            "quiebre_inicio":   inicio.strftime("%Y-%m-%d"),
            "quiebre_fin":      fin.strftime("%Y-%m-%d"),
            "dias_sin_stock":   dias_quiebre,
            "cajas_perdidas_estimadas": uds_perdidas,
            "venta_perdida_mxn":venta_perdida,
            "margen_perdido_mxn":margen_perdido,
            "temporada":        temporada_lbl,
        })

perdidas = pd.DataFrame(perdidas_rows)
perdidas.to_csv(f"{OUTPUT_DIR}/ventas_perdidas.csv", index=False)

total_venta_perdida = perdidas["venta_perdida_mxn"].sum()
total_margen_perdido = perdidas["margen_perdido_mxn"].sum()

print(f"  ✅ {len(perdidas)} episodios de quiebre documentados")
print(f"     💀 Venta perdida total estimada: ${total_venta_perdida:,.0f} MXN")
print(f"     💀 Margen perdido total:         ${total_margen_perdido:,.0f} MXN")


# ─────────────────────────────────────────────
# 7. RESUMEN EJECUTIVO
# ─────────────────────────────────────────────
print("\n📊 Calculando KPIs ejecutivos...")

rent_cliente = ventas.merge(clientes[["cliente_id","nombre","canal","segmento"]], on="cliente_id")
rent_cliente_agg = rent_cliente.groupby(["cliente_id","nombre","canal","segmento"]).agg(
    venta_total_mxn=("monto_total_mxn", "sum"),
    margen_total_mxn=("margen_bruto_mxn", "sum"),
    pedidos=("venta_id", "nunique"),
    skus_distintos=("sku", "nunique"),
    descuento_promedio=("descuento_pct", "mean"),
).reset_index()
rent_cliente_agg["margen_pct_real"] = (rent_cliente_agg["margen_total_mxn"] / rent_cliente_agg["venta_total_mxn"] * 100).round(1)
rent_cliente_agg["ticket_promedio"] = (rent_cliente_agg["venta_total_mxn"] / rent_cliente_agg["pedidos"]).round(0)
rent_cliente_agg = rent_cliente_agg.sort_values("venta_total_mxn", ascending=False)
rent_cliente_agg.to_csv(f"{OUTPUT_DIR}/rentabilidad_clientes.csv", index=False)

# ABC de SKUs
abc_sku = ventas.groupby("sku").agg(
    venta_total_mxn=("monto_total_mxn", "sum"),
    margen_total_mxn=("margen_bruto_mxn", "sum"),
    cajas_vendidas=("cantidad_cajas", "sum"),
).reset_index()
abc_sku = abc_sku.sort_values("margen_total_mxn", ascending=False)
abc_sku["margen_acumulado_pct"] = (abc_sku["margen_total_mxn"].cumsum() / abc_sku["margen_total_mxn"].sum() * 100).round(1)
abc_sku["clasificacion_abc"] = abc_sku["margen_acumulado_pct"].apply(
    lambda x: "A" if x <= 80 else ("B" if x <= 95 else "C")
)
abc_sku = abc_sku.merge(productos[["sku","nombre","marca","categoria"]], on="sku")
abc_sku.to_csv(f"{OUTPUT_DIR}/analisis_abc_skus.csv", index=False)

# ─────────────────────────────────────────────
# RESUMEN FINAL
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("🎯 RESUMEN DE DATOS — SURTIDORA DEPARTAMENTAL POC")
print("="*60)
print(f"\n  Sucursales/Canales: {len(clientes):>8,}")
print(f"  SKUs en catálogo:  {len(productos):>8,}")
print(f"  Registros ventas:  {len(ventas):>8,}")
print(f"  Registros inv.:    {len(inventario):>8,}")
print(f"  Órdenes de compra: {len(compras):>8,}")
print(f"\n  📈 Venta total 2023-2024:   ${ventas['monto_total_mxn'].sum():>15,.0f} MXN")
print(f"  📈 Margen total:             ${ventas['margen_bruto_mxn'].sum():>15,.0f} MXN")
print(f"  💀 Venta perdida estimada:  ${total_venta_perdida:>15,.0f} MXN")
print(f"  💀 Margen perdido:          ${total_margen_perdido:>15,.0f} MXN")

pct_perdido = total_venta_perdida / (ventas['monto_total_mxn'].sum() + total_venta_perdida) * 100
print(f"\n  ⚠️  Se perdió aprox. el {pct_perdido:.1f}% de la venta potencial")
print(f"      por quiebres de stock en productos clave.")

skus_a = abc_sku[abc_sku["clasificacion_abc"] == "A"]
skus_c = abc_sku[abc_sku["clasificacion_abc"] == "C"]
print(f"\n  📦 Análisis ABC:")
print(f"    SKUs clase A: {len(skus_a)} ({len(skus_a)/len(abc_sku)*100:.0f}% de SKUs → 80% del margen)")
print(f"    SKUs clase C: {len(skus_c)} ({len(skus_c)/len(abc_sku)*100:.0f}% de SKUs → 5% del margen)")

print(f"\n✅ Todos los archivos guardados en: {OUTPUT_DIR}/")
print("="*60)

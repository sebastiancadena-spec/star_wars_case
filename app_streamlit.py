# ============================ PAQUETES ============================
import os

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ============================ VARIABLES ============================
NAVY  = '#1B2A4A'
GOLD  = '#C9A84C'
GRAY  = '#8C9BAA'
LGRAY = '#E8ECF1'
WHITE = '#FFFFFF'
RED   = '#C0392B'
BG    = '#F4F6F9'

DATA_DIR = 'data/raw'

st.set_page_config(
    page_title = 'Inteligencia Estrategica — Consejo Jedi',
    page_icon  = ':rocket:',
    layout     = 'wide',
)

# ============================ ESTILOS ============================
# CSS para emular el look minimalista del dashboard (navy + gold + sombras)
st.markdown(f'''
<style>
  .stApp {{ background-color: {BG}; }}
  .block-container {{ padding-top: 0; padding-left: 2rem; padding-right: 2rem; max-width: 1200px; }}
  header[data-testid="stHeader"] {{ background: transparent; }}

  .header-block {{
      background: {NAVY};
      padding: 36px 40px 30px;
      border-bottom: 4px solid {GOLD};
      margin: 0 -2rem 0 -2rem;
  }}
  .header-eyebrow {{
      font-size: 9px; font-weight: bold; letter-spacing: 2px;
      color: {GOLD}; margin-bottom: 12px;
  }}
  .header-title {{
      font-size: 30px; font-weight: bold; color: {WHITE};
      line-height: 1.3; margin-bottom: 10px;
  }}
  .header-sub {{
      font-size: 12px; color: {GRAY}; line-height: 1.6;
  }}

  .section-card {{
      background: {WHITE};
      margin: 28px 0;
      padding: 36px 40px;
      border-left: 4px solid {GOLD};
      box-shadow: 0 1px 6px rgba(0,0,0,0.06);
  }}
  .section-eyebrow {{
      font-size: 9px; font-weight: bold; letter-spacing: 2px;
      margin-bottom: 10px;
  }}
  .section-title {{
      font-size: 20px; font-weight: bold; color: {NAVY};
      line-height: 1.35; margin-bottom: 8px;
  }}
  .section-insight {{
      font-size: 12px; color: {GRAY}; margin-bottom: 20px;
  }}
  .gold-divider {{
      height: 1.5px; background: {GOLD}; margin-bottom: 24px;
  }}
  .reco-box {{
      background: {LGRAY}; padding: 14px 18px; font-size: 12px;
      color: {NAVY}; line-height: 1.6; border-radius: 2px;
      margin-top: 18px;
  }}

  .kpi-card {{
      padding: 18px 20px; border-radius: 2px; height: 100%;
  }}
  .kpi-value {{ font-size: 26px; font-weight: bold; margin-bottom: 6px; }}
  .kpi-label {{ font-size: 10px; line-height: 1.4; }}

  .footer-block {{
      background: {NAVY}; color: {GRAY}; text-align: center;
      padding: 20px; font-size: 10px; margin: 30px -2rem 0 -2rem;
      border-top: 2px solid {GOLD};
  }}
</style>
''', unsafe_allow_html = True)


# ============================ FUNCIONES DE DATOS ============================

@st.cache_data
def cargar_parquets():
    """
    Carga todos los parquets disponibles en data/raw como dict de DataFrames.

    Retorna:
        dict: nombre_archivo (sin extension) -> DataFrame.
    """
    try:
        archivos = [f for f in os.listdir(DATA_DIR) if f.endswith('.parquet')]
        return {f.replace('.parquet', ''): pd.read_parquet(os.path.join(DATA_DIR, f))
                for f in archivos}
    except Exception as e:
        print(f'Error cargando parquets...\n{e}')
        return {}


# ============================ FUNCIONES DE CHARTS ============================

def chart_q1():
    """
    Genera chart Q1: costo por pasajero por nave (barras horizontales).
    """
    naves     = ['Halcon Milenario', 'Executor', 'Transporte Rebelde', 'Tantive IV']
    costo_pax = [16_667, 30_088, 33_333, 116_667]
    colores   = [GOLD] + [NAVY] * 3

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x = costo_pax,
        y = naves,
        orientation = 'h',
        marker_color = colores,
        text = [f'{v:,.0f} creditos por pasajero' for v in costo_pax],
        textposition = 'outside',
        hovertemplate = '<b>%{y}</b><br>Costo por pasajero: %{x:,.0f} creditos<extra></extra>',
    ))
    fig.update_layout(
        paper_bgcolor = WHITE, plot_bgcolor = WHITE,
        font = dict(family = 'Arial', size = 12, color = '#2C2C2C'),
        height = 320,
        margin = dict(l = 180, r = 220, t = 20, b = 40),
        xaxis = dict(showgrid = True, gridcolor = LGRAY, linecolor = LGRAY,
                     tickformat = ',', title = 'Creditos por pasajero (menor es mejor)',
                     title_font = dict(size = 11, color = GRAY)),
        yaxis = dict(showgrid = False, autorange = 'reversed',
                     tickfont = dict(size = 12, color = '#2C2C2C')),
        showlegend = False,
    )
    return fig


def chart_q2():
    """
    Genera chart Q2: tasa de pilotos por planeta de origen.
    """
    planetas = ['Fest', 'Lothal', 'Tatooine', 'Ryloth', 'Naboo', 'Alderaan', 'Kamino', 'Corellia']
    tasa     = [100, 100, 50, 50, 50, 50, 50, 20]
    colores  = [GOLD if t >= 50 else NAVY for t in tasa]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x = planetas, y = tasa,
        marker_color = colores,
        text = [f'{v}%' for v in tasa],
        textposition = 'outside',
        hovertemplate = '<b>%{x}</b><br>Tasa de pilotos: %{y}%<extra></extra>',
    ))
    fig.add_hline(
        y = 18.8, line_dash = 'dot', line_color = RED, line_width = 2,
        annotation_text = 'Promedio galactico: 18.8%',
        annotation_position = 'top right',
        annotation_font = dict(size = 10, color = RED),
    )
    fig.update_layout(
        paper_bgcolor = WHITE, plot_bgcolor = WHITE,
        font = dict(family = 'Arial', size = 12, color = '#2C2C2C'),
        height = 360,
        margin = dict(l = 50, r = 50, t = 20, b = 60),
        xaxis = dict(showgrid = False, linecolor = LGRAY),
        yaxis = dict(showgrid = True, gridcolor = LGRAY, range = [0, 120],
                     title = '% de personajes que son pilotos',
                     title_font = dict(size = 11, color = GRAY)),
        showlegend = False,
    )
    return fig


def chart_q3():
    """
    Genera chart Q3: puntaje estrategico por clase de nave.
    """
    clases  = ['Destructor Estelar', 'Carguero Ligero', 'Corbeta', 'Transporte Medio']
    scores  = [0.573, 0.500, 0.445, 0.300]
    detalle = ['38,000 pasajeros · 1,143 M cr.', '6 pasajeros · 100,000 cr.',
               '30 pasajeros · 3.5 M cr.', '90 pasajeros · 3 M cr.']
    colores = [GOLD, NAVY, LGRAY, LGRAY]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x = scores, y = clases,
        orientation = 'h',
        marker_color = colores,
        text = [f'{s:.2f} — {d}' for s, d in zip(scores, detalle)],
        textposition = 'outside',
        hovertemplate = '<b>%{y}</b><br>Puntaje estrategico: %{x:.2f}<extra></extra>',
    ))
    fig.update_layout(
        paper_bgcolor = WHITE, plot_bgcolor = WHITE,
        font = dict(family = 'Arial', size = 12, color = '#2C2C2C'),
        height = 300,
        margin = dict(l = 190, r = 380, t = 20, b = 40),
        xaxis = dict(showgrid = True, gridcolor = LGRAY, range = [0, 0.85],
                     title = 'Puntaje estrategico (0 = peor, 1 = mejor)',
                     title_font = dict(size = 11, color = GRAY)),
        yaxis = dict(showgrid = False, autorange = 'reversed'),
        showlegend = False,
    )
    return fig


def chart_q4():
    """
    Genera chart Q4: Executor vs resto de la flota en capacidad.
    """
    naves = ['Executor', 'Las otras 59 naves']
    cap   = [38_000, 126]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x = naves, y = cap,
        marker_color = [RED, LGRAY],
        text = ['38,000 pasajeros<br>(99.7% de la flota)',
                '126 pasajeros<br>(0.3% de la flota)'],
        textposition = 'outside',
        hovertemplate = '<b>%{x}</b><br>Capacidad: %{y:,} pasajeros<extra></extra>',
    ))
    fig.update_layout(
        paper_bgcolor = WHITE, plot_bgcolor = WHITE,
        font = dict(family = 'Arial', size = 12, color = '#2C2C2C'),
        height = 360,
        margin = dict(l = 60, r = 60, t = 20, b = 50),
        xaxis = dict(showgrid = False, linecolor = LGRAY),
        yaxis = dict(showgrid = True, gridcolor = LGRAY, range = [0, 44000],
                     title = 'Capacidad de pasajeros',
                     title_font = dict(size = 11, color = GRAY),
                     tickformat = ','),
        showlegend = False,
    )
    return fig


# ============================ COMPONENTES UI ============================

def kpi_card(valor: str, etiqueta: str, bg = LGRAY, col_val = NAVY, col_label = GRAY):
    """
    Renderiza una tarjeta KPI con los colores del dashboard.
    """
    st.markdown(f'''
    <div class="kpi-card" style="background:{bg};">
        <div class="kpi-value" style="color:{col_val};">{valor}</div>
        <div class="kpi-label" style="color:{col_label};">{etiqueta}</div>
    </div>
    ''', unsafe_allow_html = True)


def render_seccion(etiqueta, col_etiqueta, titular, insight, kpis, fig, recomendacion):
    """
    Renderiza una seccion completa del dashboard (etiqueta, titular, KPIs, chart, reco).

    Parametros:
        etiqueta (str): Label tipo 'P1 | EFICIENCIA DE FLOTA'.
        col_etiqueta (str): Color hex del label.
        titular (str): Conclusion principal en negritas.
        insight (str): Frase corta de contexto.
        kpis (list): Lista de tuplas (valor, etiqueta, bg, col_val, col_label).
        fig (Figure): Figura plotly para mostrar.
        recomendacion (str): Texto de recomendacion final.
    """
    # Apertura de la tarjeta
    st.markdown(f'''
    <div class="section-card">
        <div class="section-eyebrow" style="color:{col_etiqueta};">{etiqueta}</div>
        <div class="section-title">{titular}</div>
        <div class="section-insight">{insight}</div>
        <div class="gold-divider"></div>
    </div>
    ''', unsafe_allow_html = True)

    # KPIs en columnas
    cols = st.columns(len(kpis))
    for col, args in zip(cols, kpis):
        with col:
            kpi_card(*args)

    # Chart
    st.plotly_chart(fig, use_container_width = True, config = {'displayModeBar': False})

    # Recomendacion
    st.markdown(f'''
    <div class="reco-box">
        <strong>Recomendacion:</strong> {recomendacion}
    </div>
    ''', unsafe_allow_html = True)


# ============================ HEADER ============================

st.markdown(f'''
<div class="header-block">
    <div class="header-eyebrow">CONSEJO JEDI — REPORTE CONFIDENCIAL &nbsp;|&nbsp; MAYO 2026 &nbsp;|&nbsp; SEBASTIAN CADENA</div>
    <div class="header-title">Inteligencia Estrategica de la Galaxia:<br>Logistica y Operaciones</div>
    <div class="header-sub">
        Mision: transformar datos imperiales interceptados en decisiones estrategicas sobre flota, talento e inversion.<br>
        Fuente de datos: People, Starships y Planets (Star Wars API — SWAPI) &nbsp;|&nbsp;
        Herramientas: Python &middot; Plotly &middot; Streamlit
    </div>
</div>
''', unsafe_allow_html = True)


# ============================ SECCION 1 — EFICIENCIA DE FLOTA ============================

render_seccion(
    etiqueta = 'P1 | EFICIENCIA DE FLOTA',
    col_etiqueta = GOLD,
    titular = 'El Halcon Milenario es la nave mas eficiente:<br>costo por pasajero 7 veces menor que cualquier otra.',
    insight = 'Nota: solo 4 naves tienen datos completos de costo y pasajeros en el dataset. La muestra es pequena pero suficiente para orientar la decision.',
    kpis = [
        ('4', 'Naves con datos completos de costo y capacidad', LGRAY, NAVY, GRAY),
        ('16,667 cr.', 'Costo por pasajero del Halcon Milenario (el mas bajo)', GOLD, WHITE, WHITE),
        ('38,000', 'Pasajeros del Executor — mayor capacidad absoluta', LGRAY, NAVY, GRAY),
        ('30,088 cr.', 'Costo por pasajero del Executor (2a opcion)', LGRAY, NAVY, GRAY),
    ],
    fig = chart_q1(),
    recomendacion = (
        'Para misiones con presupuesto limitado, el Halcon Milenario es la mejor opcion: '
        'el costo mas bajo por pasajero de toda la flota. Para evacuacion masiva, el Executor '
        'es insustituible — tiene 38,000 plazas — pero su precio equivale al 99.97% del '
        'presupuesto total de la flota. No se puede depender de una sola nave de ese costo.'
    ),
)

# ============================ SECCION 2 — TALENTO ============================

render_seccion(
    etiqueta = 'P2 | ANALISIS DE TALENTO',
    col_etiqueta = GOLD,
    titular = 'Tatooine, Ryloth y Naboo producen el doble de pilotos<br>que el promedio galactico.',
    insight = (
        'Como se identificaron los pilotos: se cruzaron los nombres de personajes con '
        'la lista de pilotos registrados en cada nave. Fest y Lothal muestran 100% pero '
        'solo tienen 2 personajes cada uno — muestra muy pequena, dato orientativo.'
    ),
    kpis = [
        ('96', 'Total de personajes analizados en el universo', LGRAY, NAVY, GRAY),
        ('18', 'Pilotos certificados identificados en la flota', GOLD, WHITE, WHITE),
        ('18.8%', 'Tasa galactica: 1 de cada 5 personajes es piloto', LGRAY, NAVY, GRAY),
        ('50%', 'Tasa en Tatooine, Ryloth y Naboo — el doble del promedio', LGRAY, NAVY, GRAY),
    ],
    fig = chart_q2(),
    recomendacion = (
        'Concentrar el reclutamiento en Tatooine, Ryloth y Naboo: '
        'tasa de pilotos del 50% vs 18.8% del promedio galactico. '
        'No se encontro brecha significativa por genero (masculino 20.6% vs femenino 16.7%), '
        'por lo que el reclutamiento debe ser inclusivo y enfocado en el planeta de origen.'
    ),
)

# ============================ SECCION 3 — INVERSION ESTRATEGICA ============================

render_seccion(
    etiqueta = 'P3 | INVERSION ESTRATEGICA',
    col_etiqueta = GOLD,
    titular = 'El Destructor Estelar maximiza la presencia galactica.<br>El Carguero Ligero maximiza la eficiencia del presupuesto.',
    insight = (
        'Como se calculo el puntaje: cada metrica (pasajeros, costo, velocidad) se normalizo de 0 a 1 '
        'y se combino con pesos. Velocidad subluminica = que tan rapido puede moverse la nave dentro de un sistema. '
        'Solo 4 clases tienen datos completos — la recomendacion es orientativa.'
    ),
    kpis = [
        ('0.57', 'Puntaje estrategico del Destructor Estelar (el mas alto)', GOLD, WHITE, WHITE),
        ('0.50', 'Puntaje del Carguero Ligero — el mas eficiente en costo', LGRAY, NAVY, GRAY),
        ('50/30/20', 'Pesos: pasajeros + costo + velocidad', LGRAY, NAVY, GRAY),
        ('4', 'Clases de naves evaluadas con datos completos', LGRAY, NAVY, GRAY),
    ],
    fig = chart_q3(),
    recomendacion = (
        'No concentrar el 100% del presupuesto en una sola clase. '
        'Portafolio recomendado: 1 Destructor Estelar para operaciones de gran escala '
        '+ flota de Cargueros Ligeros para presencia distribuida y misiones encubiertas.'
    ),
)

# ============================ SECCION 4 — HALLAZGO CRITICO ============================

render_seccion(
    etiqueta = 'P4 | HALLAZGO CRITICO',
    col_etiqueta = RED,
    titular = (
        'La flota completa solo puede transportar el 0.003% de la poblacion galactica.<br>'
        'Una sola nave concentra el 99.7% de esa capacidad.'
    ),
    insight = (
        'Como se encontro este hallazgo: se sumo la capacidad de pasajeros de todas las naves '
        'y se comparo con la poblacion total de los planetas en el dataset. '
        'Se aplico el Principio de Pareto para mostrar la concentracion: pocas naves controlan casi todo el recurso.'
    ),
    kpis = [
        ('1.14 Billones', 'Habitantes en los planetas conocidos de la galaxia', RED, WHITE, WHITE),
        ('38,126', 'Pasajeros que caben en toda la flota junta', LGRAY, NAVY, GRAY),
        ('29.9 M', 'Viajes para evacuar toda la galaxia', NAVY, GOLD, GOLD),
        ('99.7%', 'De la capacidad esta en 1 sola nave: el Executor', RED, WHITE, WHITE),
    ],
    fig = chart_q4(),
    recomendacion = (
        'El Consejo Jedi debe proteger al Executor como activo numero 1 de la flota: '
        'su perdida equivale a perder casi toda la capacidad de evacuacion. '
        'Se requiere un plan urgente de diversificacion de flota para eliminar este punto critico de falla.'
    ),
)


# ============================ EXPLORADOR DE DATOS ============================

st.markdown(f'''
<div class="section-card">
    <div class="section-eyebrow" style="color:{NAVY};">EXTRA | EXPLORADOR DE DATOS</div>
    <div class="section-title">Explora cualquiera de los 15 datasets parquet del universo Star Wars.</div>
    <div class="section-insight">Selecciona una tabla para ver su contenido. Datos cargados en vivo desde data/raw.</div>
    <div class="gold-divider"></div>
</div>
''', unsafe_allow_html = True)

datos = cargar_parquets()

if datos:
    tabla_sel = st.selectbox(
        'Selecciona un dataset:',
        sorted(datos.keys()),
        index = sorted(datos.keys()).index('starships') if 'starships' in datos else 0,
    )
    df = datos[tabla_sel]
    c1, c2, c3 = st.columns(3)
    c1.metric('Filas', f'{len(df):,}')
    c2.metric('Columnas', f'{len(df.columns):,}')
    c3.metric('Tamano (KB)', f'{df.memory_usage(deep=True).sum()/1024:,.1f}')
    st.dataframe(df, use_container_width = True, height = 360)
else:
    st.warning('No se encontraron archivos parquet en data/raw/')


# ============================ FOOTER ============================

st.markdown('''
<div class="footer-block">
    Preparado por Sebastian Cadena &nbsp;|&nbsp; Proceso de Seleccion — BI Analyst &nbsp;|&nbsp; Mayo 2026
</div>
''', unsafe_allow_html = True)

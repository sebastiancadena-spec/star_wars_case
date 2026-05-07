# ============================ PAQUETES ============================
import os
import plotly.graph_objects as go

# ============================ VARIABLES ============================
OUT       = r'c:\Users\sebastian.cadena_kav\Downloads\star_wars_bi_case\output'
OUT_HTML  = f'{OUT}/dashboard_star_wars_bi.html'

NAVY  = '#1B2A4A'
GOLD  = '#C9A84C'
GRAY  = '#8C9BAA'
LGRAY = '#E8ECF1'
WHITE = '#FFFFFF'
RED   = '#C0392B'

# ============================ DATOS ============================

# Q1 — 4 naves con datos completos
q1_naves     = ['Halcon Milenario', 'Executor', 'Transporte Rebelde', 'Tantive IV']
q1_costo_pax = [16_667, 30_088, 33_333, 116_667]   # creditos por pasajero

# Q2 — tasa de pilotos por planeta (min 2 personajes)
q2_planetas  = ['Fest', 'Lothal', 'Tatooine', 'Ryloth', 'Naboo', 'Alderaan', 'Kamino', 'Corellia']
q2_tasa      = [100, 100, 50, 50, 50, 50, 50, 20]

# Q3 — puntaje estrategico por clase (0-1)
q3_clases    = ['Destructor Estelar', 'Carguero Ligero', 'Corbeta', 'Transporte Medio']
q3_scores    = [0.573, 0.500, 0.445, 0.300]
q3_detalle   = ['38,000 pasajeros · 1,143 M cr.', '6 pasajeros · 100,000 cr.',
                '30 pasajeros · 3.5 M cr.', '90 pasajeros · 3 M cr.']

# Q4 — capacidad concentrada
q4_naves  = ['Executor', 'Las otras 59 naves']
q4_cap    = [38_000, 126]

# ============================ FUNCIONES DE CHARTS ============================

def chart_q1() -> str:
    """
    Genera chart Q1: costo por pasajero por nave (barras horizontales).
    La nave con menor costo es la mas eficiente para misiones de bajo presupuesto.

    Retorna:
        str: HTML del chart Plotly.
    """
    colores = [GOLD] + [NAVY] * 3
    anotaciones = [
        'MEJOR VALOR',
        '',
        '',
        'COSTO MAS ALTO',
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=q1_costo_pax,
        y=q1_naves,
        orientation='h',
        marker_color=colores,
        text=[f'{v:,.0f} creditos por pasajero' for v in q1_costo_pax],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Costo por pasajero: %{x:,.0f} creditos<extra></extra>',
    ))

    fig.update_layout(
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(family='Arial', size=12, color='#2C2C2C'),
        height=320,
        margin=dict(l=180, r=220, t=20, b=40),
        xaxis=dict(
            showgrid=True, gridcolor=LGRAY,
            linecolor=LGRAY, tickformat=',',
            title='Creditos por pasajero (menor es mejor)',
            title_font=dict(size=11, color=GRAY),
        ),
        yaxis=dict(
            showgrid=False, autorange='reversed',
            tickfont=dict(size=12, color='#2C2C2C'),
        ),
        showlegend=False,
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)


def chart_q2() -> str:
    """
    Genera chart Q2: tasa de pilotos por planeta de origen (barras verticales).
    Planetas con mayor tasa son los mejores candidatos para reclutamiento.

    Retorna:
        str: HTML del chart Plotly.
    """
    colores = [GOLD if t >= 50 else NAVY for t in q2_tasa]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=q2_planetas,
        y=q2_tasa,
        marker_color=colores,
        text=[f'{v}%' for v in q2_tasa],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Tasa de pilotos: %{y}%<extra></extra>',
    ))

    # Linea de promedio galactico
    fig.add_hline(
        y=18.8, line_dash='dot', line_color=RED, line_width=2,
        annotation_text='Promedio galactico: 18.8%',
        annotation_position='top right',
        annotation_font=dict(size=10, color=RED),
    )

    fig.update_layout(
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(family='Arial', size=12, color='#2C2C2C'),
        height=360,
        margin=dict(l=50, r=50, t=20, b=60),
        xaxis=dict(showgrid=False, linecolor=LGRAY),
        yaxis=dict(
            showgrid=True, gridcolor=LGRAY,
            range=[0, 120],
            title='% de personajes que son pilotos',
            title_font=dict(size=11, color=GRAY),
        ),
        showlegend=False,
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)


def chart_q3() -> str:
    """
    Genera chart Q3: puntaje estrategico por clase de nave.
    Mayor puntaje = mejor balance entre capacidad, costo y velocidad.

    Retorna:
        str: HTML del chart Plotly.
    """
    colores = [GOLD, NAVY, LGRAY, LGRAY]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=q3_scores,
        y=q3_clases,
        orientation='h',
        marker_color=colores,
        text=[f'{s:.2f} — {d}' for s, d in zip(q3_scores, q3_detalle)],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Puntaje estrategico: %{x:.2f}<extra></extra>',
    ))

    fig.update_layout(
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(family='Arial', size=12, color='#2C2C2C'),
        height=300,
        margin=dict(l=190, r=380, t=20, b=40),
        xaxis=dict(
            showgrid=True, gridcolor=LGRAY, range=[0, 0.85],
            title='Puntaje estrategico (0 = peor, 1 = mejor)',
            title_font=dict(size=11, color=GRAY),
        ),
        yaxis=dict(showgrid=False, autorange='reversed'),
        showlegend=False,
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)


def chart_q4() -> str:
    """
    Genera chart Q4: Executor vs resto de la flota en capacidad de pasajeros.
    Muestra la concentracion extrema de capacidad en una sola nave.

    Retorna:
        str: HTML del chart Plotly.
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=q4_naves,
        y=q4_cap,
        marker_color=[RED, LGRAY],
        text=['38,000 pasajeros<br>(99.7% de la flota)', '126 pasajeros<br>(0.3% de la flota)'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Capacidad: %{y:,} pasajeros<extra></extra>',
    ))

    fig.update_layout(
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(family='Arial', size=12, color='#2C2C2C'),
        height=360,
        margin=dict(l=60, r=60, t=20, b=50),
        xaxis=dict(showgrid=False, linecolor=LGRAY),
        yaxis=dict(
            showgrid=True, gridcolor=LGRAY,
            range=[0, 44000],
            title='Capacidad de pasajeros',
            title_font=dict(size=11, color=GRAY),
            tickformat=',',
        ),
        showlegend=False,
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)


# ============================ BLOQUES HTML ============================

def kpi(valor: str, etiqueta: str, bg=LGRAY, col_val=NAVY, col_label=GRAY) -> str:
    """
    Genera HTML de una tarjeta KPI.

    Parametros:
        valor (str): Numero o dato principal.
        etiqueta (str): Descripcion en texto pequeno.
        bg, col_val, col_label: Colores de fondo, valor y etiqueta.

    Retorna:
        str: HTML de la tarjeta.
    """
    return f'''<div style="
        background:{bg}; padding:20px 22px; flex:1; min-width:180px;
        border-radius:2px; margin:0 6px 0 0;">
      <div style="font-size:28px; font-weight:bold; color:{col_val}; margin-bottom:6px;">{valor}</div>
      <div style="font-size:10px; color:{col_label}; line-height:1.4;">{etiqueta}</div>
    </div>'''


def seccion(etiqueta: str, col_etiqueta: str, titular: str,
            kpis: str, insight: str, chart_html: str,
            recomendacion: str) -> str:
    """
    Genera HTML de una seccion completa del dashboard.

    Parametros:
        etiqueta (str): Label de la seccion (ej. 'P1 | EFICIENCIA DE FLOTA').
        col_etiqueta (str): Color del label.
        titular (str): Mensaje clave (la conclusion, estilo McKinsey).
        kpis (str): HTML de los KPIs.
        insight (str): Frase corta de interpretacion debajo del titular.
        chart_html (str): HTML del grafico Plotly.
        recomendacion (str): Accion recomendada.

    Retorna:
        str: HTML completo de la seccion.
    """
    return f'''
  <div style="background:{WHITE}; margin:28px 48px; padding:36px 40px;
              border-left:4px solid {GOLD}; box-shadow:0 1px 6px rgba(0,0,0,0.06);">

    <!-- Etiqueta -->
    <div style="font-size:9px; font-weight:bold; letter-spacing:2px;
                color:{col_etiqueta}; margin-bottom:10px;">{etiqueta}</div>

    <!-- Titular: la conclusion va primero -->
    <div style="font-size:20px; font-weight:bold; color:{NAVY};
                line-height:1.35; margin-bottom:8px;">{titular}</div>

    <!-- Frase de apoyo -->
    <div style="font-size:12px; color:{GRAY}; margin-bottom:20px;">{insight}</div>

    <!-- Separador dorado -->
    <div style="height:1.5px; background:{GOLD}; margin-bottom:24px;"></div>

    <!-- KPIs -->
    <div style="display:flex; gap:0; margin-bottom:28px; flex-wrap:wrap;">
      {kpis}
    </div>

    <!-- Chart -->
    <div style="margin-bottom:24px;">
      {chart_html}
    </div>

    <!-- Recomendacion -->
    <div style="background:{LGRAY}; padding:12px 16px; font-size:11px;
                color:{NAVY}; line-height:1.6; border-radius:2px;">
      <strong>Recomendacion:</strong> {recomendacion}
    </div>

  </div>'''


# ============================ MAIN ============================

def main():
    """
    Genera el dashboard HTML minimalista del caso Star Wars BI.
    """
    # Generar charts
    c1 = chart_q1()
    c2 = chart_q2()
    c3 = chart_q3()
    c4 = chart_q4()

    # Secciones
    s1 = seccion(
        etiqueta='P1 | EFICIENCIA DE FLOTA',
        col_etiqueta=GOLD,
        titular='El Halcon Milenario es la nave mas eficiente:<br>costo por pasajero 7 veces menor que cualquier otra.',
        kpis=(
            kpi('4', 'Naves con datos completos de costo y capacidad de pasajeros') +
            kpi('16,667 cr.', 'Costo por pasajero del Halcon Milenario (el mas bajo)', GOLD, WHITE, WHITE) +
            kpi('38,000', 'Pasajeros del Executor — la nave con mayor capacidad absoluta') +
            kpi('30,088 cr.', 'Costo por pasajero del Executor (2a opcion en eficiencia)')
        ),
        insight='Nota: solo 4 naves tienen datos completos de costo y pasajeros en el dataset. La muestra es pequena pero suficiente para orientar la decision.',
        chart_html=c1,
        recomendacion=(
            'Para misiones con presupuesto limitado, el Halcon Milenario es la mejor opcion: '
            'el costo mas bajo por pasajero de toda la flota. Para evacuacion masiva, el Executor '
            'es insustituible — tiene 38,000 plazas — pero su precio equivale al 99.97% del '
            'presupuesto total de la flota. No se puede depender de una sola nave de ese costo.'
        )
    )

    s2 = seccion(
        etiqueta='P2 | ANALISIS DE TALENTO',
        col_etiqueta=GOLD,
        titular='Tatooine, Ryloth y Naboo producen el doble de pilotos<br>que el promedio galactico.',
        kpis=(
            kpi('96', 'Total de personajes analizados en el universo Star Wars') +
            kpi('18', 'Pilotos certificados identificados en la flota', GOLD, WHITE, WHITE) +
            kpi('18.8%', 'Tasa de pilotos a nivel galactico: 1 de cada 5 personajes') +
            kpi('50%', 'Tasa de pilotos en Tatooine, Ryloth y Naboo — el doble del promedio')
        ),
        insight=(
            'Como se identificaron los pilotos: se cruzaron los nombres de personajes con '
            'la lista de pilotos registrados en cada nave de la flota. '
            'Fest y Lothal muestran 100% pero solo tienen 2 personajes cada uno — muestra muy pequeña, dato orientativo.'
        ),
        chart_html=c2,
        recomendacion=(
            'Concentrar el reclutamiento en Tatooine, Ryloth y Naboo: '
            'tasa de pilotos del 50% vs 18.8% del promedio galactico. '
            'No se encontro brecha significativa por genero (masculino 20.6% vs femenino 16.7%), '
            'por lo que el reclutamiento debe ser inclusivo y enfocado en el planeta de origen.'
        )
    )

    s3 = seccion(
        etiqueta='P3 | INVERSION ESTRATEGICA',
        col_etiqueta=GOLD,
        titular='El Destructor Estelar maximiza la presencia galactica.<br>El Carguero Ligero maximiza la eficiencia del presupuesto.',
        kpis=(
            kpi('0.57', 'Puntaje estrategico del Destructor Estelar (el mas alto)', GOLD, WHITE, WHITE) +
            kpi('0.50', 'Puntaje del Carguero Ligero — el mas eficiente en costo') +
            kpi('50%+30%+20%', 'Formula: capacidad de pasajeros + menor costo + velocidad') +
            kpi('4', 'Clases de naves evaluadas con datos completos')
        ),
        insight=(
            'Como se calculo el puntaje: cada metrica (pasajeros, costo, velocidad) se normalizo de 0 a 1 '
            'y se combino con pesos. Velocidad subluminica = que tan rapido puede moverse la nave dentro de un sistema planetario. '
            'Nota: solo 4 clases tienen datos completos — la recomendacion es orientativa.'
        ),
        chart_html=c3,
        recomendacion=(
            'No concentrar el 100% del presupuesto en una sola clase. '
            'Portafolio recomendado: 1 Destructor Estelar para operaciones de gran escala '
            '+ flota de Cargueros Ligeros para presencia distribuida y misiones encubiertas.'
        )
    )

    s4 = seccion(
        etiqueta='P4 | HALLAZGO CRITICO',
        col_etiqueta=RED,
        titular='La flota completa solo puede transportar el 0.003% de la poblacion galactica.<br>Una sola nave concentra el 99.7% de esa capacidad.',
        kpis=(
            kpi('1.14 Billones', 'Habitantes en los planetas conocidos de la galaxia', RED, WHITE, WHITE) +
            kpi('38,126', 'Pasajeros que caben en toda la flota junta (todas las naves)') +
            kpi('29.9 M', 'Viajes que se necesitarian para evacuar toda la galaxia', NAVY, GOLD, GOLD) +
            kpi('99.7%', 'De la capacidad total esta en 1 sola nave: el Executor', RED, WHITE, WHITE)
        ),
        insight=(
            'Como se encontro este hallazgo: se sumo la capacidad de pasajeros de todas las naves '
            'y se comparo con la poblacion total de los planetas en el dataset. '
            'Se aplico el Principio de Pareto para mostrar la concentracion: pocas naves controlan casi todo el recurso.'
        ),
        chart_html=c4,
        recomendacion=(
            'El Consejo Jedi debe proteger al Executor como activo numero 1 de la flota: '
            'su perdida equivale a perder casi toda la capacidad de evacuacion. '
            'Se requiere un plan urgente de diversificacion de flota para eliminar este punto critico de falla.'
        )
    )

    # Pagina HTML completa
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Inteligencia Estrategica — Consejo Jedi | KAVAK</title>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: Arial, sans-serif; background: #F4F6F9; }}
  </style>
</head>
<body>

  <!-- HEADER -->
  <div style="background:{NAVY}; padding:36px 48px 30px; border-bottom:4px solid {GOLD};">
    <div style="font-size:9px; font-weight:bold; letter-spacing:2px; color:{GOLD}; margin-bottom:12px;">
      CONSEJO JEDI — REPORTE CONFIDENCIAL &nbsp;|&nbsp; MAYO 2026 &nbsp;|&nbsp; SEBASTIAN CADENA
    </div>
    <div style="font-size:30px; font-weight:bold; color:{WHITE}; line-height:1.3; margin-bottom:10px;">
      Inteligencia Estrategica de la Galaxia:<br>Logistica y Operaciones
    </div>
    <div style="font-size:12px; color:{GRAY}; line-height:1.6;">
      Mision: transformar datos imperiales interceptados en decisiones estrategicas sobre flota, talento e inversion.<br>
      Fuente de datos: People, Starships y Planets (Star Wars API — SWAPI) &nbsp;|&nbsp;
      Herramientas: Python en VS Code → Google Sheets → Looker Studio
    </div>
  </div>

  {s1}
  {s2}
  {s3}
  {s4}

  <!-- FOOTER -->
  <div style="background:{NAVY}; color:{GRAY}; text-align:center; padding:20px;
              font-size:10px; margin-top:12px; border-top:2px solid {GOLD};">
    Preparado por Sebastian Cadena &nbsp;|&nbsp; Proceso de Seleccion KAVAK — BI Analyst &nbsp;|&nbsp; Mayo 2026
  </div>

</body>
</html>'''

    os.makedirs(OUT, exist_ok=True)
    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Dashboard guardado: {OUT_HTML}')


if __name__ == '__main__':
    main()

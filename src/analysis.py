# ============================ PAQUETES ============================
import duckdb
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import warnings

warnings.filterwarnings('ignore')

# ============================ VARIABLES ============================
RAW = r'c:\Users\sebastian.cadena_kav\Downloads\star_wars_bi_case\data\raw'
OUT_CSV = r'c:\Users\sebastian.cadena_kav\Downloads\star_wars_bi_case\data\processed'
OUT_CHARTS = r'c:\Users\sebastian.cadena_kav\Downloads\star_wars_bi_case\output\charts'

# Paleta McKinsey minimalista
NAVY   = '#1B2A4A'
GOLD   = '#C9A84C'
GRAY   = '#8C9BAA'
LGRAY  = '#D6DCE4'
WHITE  = '#FFFFFF'
RED    = '#C0392B'

PALETTE = [NAVY, GOLD, GRAY, '#2E86AB', '#A23B72', '#F18F01']

TEMPLATE = dict(
    layout = go.Layout(
        font        = dict(family='Arial', color='#2C2C2C', size=12),
        paper_bgcolor = WHITE,
        plot_bgcolor  = WHITE,
        title_font    = dict(size=16, color=NAVY, family='Arial'),
        xaxis         = dict(showgrid=False, linecolor=LGRAY, tickfont=dict(size=11)),
        yaxis         = dict(showgrid=True,  gridcolor=LGRAY, linecolor=LGRAY, tickfont=dict(size=11)),
        legend        = dict(bgcolor='rgba(0,0,0,0)', borderwidth=0),
        margin        = dict(l=60, r=40, t=70, b=60),
    )
)

# ============================ FUNCIONES ============================

def cargar_datos():
    """
    Carga los parquets relevantes con DuckDB.

    Retorna:
        tuple: (characters, starships, planets) como DataFrames.
    """
    con = duckdb.connect()

    characters = con.execute(f"SELECT * FROM read_parquet('{RAW}/characters.parquet')").df()
    starships  = con.execute(f"SELECT * FROM read_parquet('{RAW}/starships.parquet')").df()
    planets    = con.execute(f"SELECT * FROM read_parquet('{RAW}/planets.parquet')").df()

    print(f'characters: {characters.shape} | starships: {starships.shape} | planets: {planets.shape}')
    return characters, starships, planets


def limpiar_starships(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia columnas numéricas clave de starships.

    Parámetros:
        df (pd.DataFrame): DataFrame raw de starships.

    Retorna:
        pd.DataFrame: DataFrame limpio con columnas numéricas.
    """
    cols_num = ['cost_in_credits', 'passengers', 'crew', 'cargo_capacity',
                'length', 'max_atmosphering_speed', 'hyperdrive_rating', 'MGLT']

    df = df.copy()
    for col in cols_num:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.strip(), errors='coerce')

    # Deduplicar por nombre
    df = df.drop_duplicates(subset=['name'])

    # Eliminar filas sin costo o sin capacidad de pasajeros
    df = df.dropna(subset=['cost_in_credits', 'passengers'])
    df = df[df['cost_in_credits'] > 0]
    df = df[df['passengers'] > 0]

    return df


def limpiar_planets(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia columnas numéricas clave de planets.

    Parámetros:
        df (pd.DataFrame): DataFrame raw de planets.

    Retorna:
        pd.DataFrame: DataFrame limpio con población numérica.
    """
    df = df.copy()
    df['population'] = pd.to_numeric(df['population'].astype(str).str.replace(',', '').str.strip(), errors='coerce')
    return df


def limpiar_characters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia columnas de characters y normaliza texto.

    Parámetros:
        df (pd.DataFrame): DataFrame raw de characters.

    Retorna:
        pd.DataFrame: DataFrame limpio.
    """
    df = df.copy()
    df['height'] = pd.to_numeric(df['height'], errors='coerce')
    if 'mass' in df.columns:
        df['mass'] = pd.to_numeric(df['mass'].astype(str).str.replace(',', ''), errors='coerce')
    if 'weight' in df.columns:
        df['weight'] = pd.to_numeric(df['weight'].astype(str).str.replace(',', ''), errors='coerce')

    # Normalizar campos de texto
    for col in ['gender', 'species', 'homeworld']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
            df[col] = df[col].replace({'None': 'Unknown', 'Nan': 'Unknown', '': 'Unknown'})

    return df


def guardar_chart(fig, nombre: str):
    """
    Guarda un chart Plotly como HTML y PNG.

    Parámetros:
        fig: Figura Plotly.
        nombre (str): Nombre base del archivo.
    """
    os.makedirs(OUT_CHARTS, exist_ok=True)
    html_str = fig.to_html()
    with open(f'{OUT_CHARTS}/{nombre}.html', 'w', encoding='utf-8') as f:
        f.write(html_str)
    try:
        fig.write_image(f'{OUT_CHARTS}/{nombre}.png', width=900, height=520, scale=2)
    except Exception as e:
        print(f'PNG no guardado (requiere kaleido): {e}')


def guardar_csv(df: pd.DataFrame, nombre: str):
    """
    Guarda un DataFrame como CSV en la carpeta processed.

    Parámetros:
        df (pd.DataFrame): Datos a guardar.
        nombre (str): Nombre del archivo.
    """
    os.makedirs(OUT_CSV, exist_ok=True)
    path = f'{OUT_CSV}/{nombre}.csv'
    df.to_csv(path, index=False, encoding='utf-8')
    print(f'  Guardado: {path}')


# ============================ Q1: EFICIENCIA DE FLOTA ============================

def q1_eficiencia_flota(starships_raw: pd.DataFrame):
    """
    Responde Q1: Top 3 naves más eficientes por costo vs capacidad de pasajeros.

    Parámetros:
        starships_raw (pd.DataFrame): Starships sin limpiar.

    Retorna:
        pd.DataFrame: Top naves con índice de eficiencia.
    """
    print('\n--- Q1: Eficiencia de Flota ---')
    df = limpiar_starships(starships_raw)

    # Eficiencia = pasajeros por crédito (cuántos pasajeros por unidad de costo)
    df['efficiency_score'] = df['passengers'] / df['cost_in_credits']
    df['cost_per_passenger'] = df['cost_in_credits'] / df['passengers']

    # Agregar clase de nave
    cols = ['name', 'starship_class', 'cost_in_credits', 'passengers', 'crew',
            'efficiency_score', 'cost_per_passenger', 'length', 'hyperdrive_rating']
    df_out = df[cols].sort_values('efficiency_score', ascending=False).reset_index(drop=True)

    top3 = df_out.head(3)
    print(top3[['name', 'starship_class', 'passengers', 'cost_in_credits', 'efficiency_score']])

    # --- Chart: Scatter costo vs pasajeros (burbujas = eficiencia) ---
    df_plot = df_out.head(20).copy()
    df_plot['es_top3'] = df_plot.index < 3
    df_plot['label'] = df_plot.apply(
        lambda r: r['name'] if r['es_top3'] else '', axis=1
    )
    df_plot['cost_M'] = df_plot['cost_in_credits'] / 1_000_000

    fig = go.Figure()

    # Resto de naves
    otros = df_plot[~df_plot['es_top3']]
    fig.add_trace(go.Scatter(
        x=otros['cost_M'], y=otros['passengers'],
        mode='markers',
        marker=dict(size=8, color=GRAY, opacity=0.5),
        name='Otras naves',
        text=otros['name'], hovertemplate='%{text}<br>Costo: %{x:.1f}M cr<br>Pasajeros: %{y:,}<extra></extra>'
    ))

    # Top 3
    top = df_plot[df_plot['es_top3']]
    fig.add_trace(go.Scatter(
        x=top['cost_M'], y=top['passengers'],
        mode='markers+text',
        marker=dict(size=14, color=GOLD, symbol='star'),
        text=top['name'],
        textposition='top center',
        name='Top 3',
        hovertemplate='%{text}<br>Costo: %{x:.1f}M cr<br>Pasajeros: %{y:,}<extra></extra>'
    ))

    fig.update_layout(
        TEMPLATE['layout'],
        title='Eficiencia de Flota: Costo vs. Capacidad de Pasajeros',
        xaxis_title='Costo (Millones de Creditos)',
        yaxis_title='Capacidad de Pasajeros',
        annotations=[dict(
            text='Estrella = Top 3 naves mas eficientes (mayor cantidad de pasajeros por credito)',
            xref='paper', yref='paper', x=0, y=-0.15,
            showarrow=False, font=dict(size=10, color=GRAY)
        )]
    )

    guardar_chart(fig, 'q1_fleet_efficiency')

    # Chart 2: Bar chart top 10 eficiencia
    top10 = df_out.head(10).copy()
    top10['color'] = top10.index.map(lambda i: GOLD if i < 3 else NAVY)

    fig2 = go.Figure(go.Bar(
        x=top10['efficiency_score'],
        y=top10['name'],
        orientation='h',
        marker_color=top10['color'],
        text=top10['efficiency_score'].apply(lambda x: f'{x:.4f}'),
        textposition='outside',
        hovertemplate='%{y}<br>Efficiency Score: %{x:.5f}<extra></extra>'
    ))
    fig2.update_layout(
        TEMPLATE['layout'],
        title='Top 10 Naves por Indice de Eficiencia (Pasajeros por Credito)',
        xaxis_title='Pasajeros por Credito',
        yaxis=dict(autorange='reversed', showgrid=False),
        height=480
    )
    guardar_chart(fig2, 'q1_top10_efficiency_bar')

    guardar_csv(df_out, 'q1_fleet_efficiency')
    return df_out


# ============================ Q2: ANÁLISIS DE TALENTO ============================

def q2_analisis_talento(characters_raw: pd.DataFrame, starships_raw: pd.DataFrame, planets_raw: pd.DataFrame):
    """
    Responde Q2: distribución de especies/género por planeta y correlación con pilotos.

    Parámetros:
        characters_raw, starships_raw, planets_raw (pd.DataFrame): DataFrames raw.

    Retorna:
        tuple: (df_talent, df_pilot_homeworld)
    """
    print('\n--- Q2: Análisis de Talento ---')
    chars = limpiar_characters(characters_raw)

    # Extraer pilotos desde starships (columna pilots es lista de nombres)
    def parsear_lista(val):
        """Parsea columnas que contienen listas en string."""
        if pd.isna(val) or val in ('', '[]', 'None'):
            return []
        try:
            result = json.loads(val.replace("'", '"'))
            return result if isinstance(result, list) else []
        except Exception:
            # Intentar split por coma si no es JSON válido
            return [x.strip() for x in str(val).strip("[]").split(',') if x.strip()]

    # Pilotos únicos en toda la flota
    all_pilots = set()
    starships_raw_copy = starships_raw.copy()
    starships_raw_copy['pilots_list'] = starships_raw_copy['pilots'].apply(parsear_lista)
    for pilots in starships_raw_copy['pilots_list']:
        all_pilots.update([p.strip() for p in pilots])

    # Marcar si el personaje es piloto
    chars['is_pilot'] = chars['name'].isin(all_pilots)

    print(f'  Total pilotos identificados: {chars["is_pilot"].sum()} de {len(chars)} personajes')

    # --- Distribución por especie ---
    species_dist = (
        chars.groupby('species')
        .agg(total=('name', 'count'), pilots=('is_pilot', 'sum'))
        .reset_index()
        .sort_values('total', ascending=False)
    )
    species_dist['pilot_rate'] = (species_dist['pilots'] / species_dist['total'] * 100).round(1)

    # Top 10 especies
    top_species = species_dist.head(10)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top_species['species'], y=top_species['total'],
        name='Total Personajes',
        marker_color=NAVY,
        text=top_species['total'], textposition='outside'
    ))
    fig.add_trace(go.Bar(
        x=top_species['species'], y=top_species['pilots'],
        name='Pilotos',
        marker_color=GOLD,
        text=top_species['pilots'], textposition='outside'
    ))
    fig.update_layout(
        TEMPLATE['layout'],
        title='Distribucion de Talento: Personajes vs Pilotos por Especie',
        xaxis_title='Especie', yaxis_title='Cantidad',
        barmode='group',
        xaxis_tickangle=-30
    )
    guardar_chart(fig, 'q2_species_talent')

    # --- Tasa de pilotos por homeworld ---
    homeworld_pilot = (
        chars.groupby('homeworld')
        .agg(total=('name', 'count'), pilots=('is_pilot', 'sum'))
        .reset_index()
    )
    homeworld_pilot['pilot_rate'] = (homeworld_pilot['pilots'] / homeworld_pilot['total'] * 100).round(1)
    homeworld_pilot = homeworld_pilot[homeworld_pilot['total'] >= 2].sort_values('pilot_rate', ascending=False)

    top_hw = homeworld_pilot.head(12)

    fig2 = go.Figure(go.Bar(
        x=top_hw['homeworld'],
        y=top_hw['pilot_rate'],
        marker_color=[GOLD if r >= 50 else NAVY for r in top_hw['pilot_rate']],
        text=top_hw['pilot_rate'].apply(lambda x: f'{x:.0f}%'),
        textposition='outside',
        hovertemplate='%{x}<br>Tasa de Pilotos: %{y:.1f}%<br><extra></extra>'
    ))
    fig2.update_layout(
        TEMPLATE['layout'],
        title='Tasa de Exito como Piloto por Planeta de Origen (min. 2 personajes)',
        xaxis_title='Planeta de Origen', yaxis_title='% Pilotos',
        xaxis_tickangle=-30,
        shapes=[dict(type='line', x0=-0.5, x1=len(top_hw)-0.5, y0=50, y1=50,
                     line=dict(color=RED, width=1.5, dash='dot'))],
        annotations=[dict(text='Umbral 50%', x=len(top_hw)-1, y=52,
                         font=dict(color=RED, size=10), showarrow=False)]
    )
    guardar_chart(fig2, 'q2_pilot_rate_by_planet')

    # --- Género ---
    gender_pilot = (
        chars.groupby('gender')
        .agg(total=('name', 'count'), pilots=('is_pilot', 'sum'))
        .reset_index()
    )
    gender_pilot['pilot_rate'] = (gender_pilot['pilots'] / gender_pilot['total'] * 100).round(1)

    fig3 = go.Figure(go.Bar(
        x=gender_pilot['gender'],
        y=gender_pilot['pilot_rate'],
        marker_color=PALETTE[:len(gender_pilot)],
        text=gender_pilot['pilot_rate'].apply(lambda x: f'{x:.0f}%'),
        textposition='outside'
    ))
    fig3.update_layout(
        TEMPLATE['layout'],
        title='Tasa de Pilotos por Genero',
        xaxis_title='Genero', yaxis_title='% Pilotos'
    )
    guardar_chart(fig3, 'q2_pilot_rate_gender')

    guardar_csv(species_dist, 'q2_species_distribution')
    guardar_csv(homeworld_pilot, 'q2_pilot_homeworld')
    guardar_csv(gender_pilot, 'q2_pilot_gender')

    return species_dist, homeworld_pilot, gender_pilot, chars


# ============================ Q3: INVERSIÓN ESTRATÉGICA ============================

def q3_inversion_estrategica(starships_raw: pd.DataFrame):
    """
    Responde Q3: qué clase de nave (starship_class) maximiza presencia en la galaxia.

    Parámetros:
        starships_raw (pd.DataFrame): Starships sin limpiar.

    Retorna:
        pd.DataFrame: Análisis por clase de nave.
    """
    print('\n--- Q3: Inversión Estratégica ---')
    df = limpiar_starships(starships_raw)

    # Métricas por clase
    class_analysis = (
        df.groupby('starship_class')
        .agg(
            count         = ('name', 'count'),
            avg_cost      = ('cost_in_credits', 'mean'),
            avg_passengers= ('passengers', 'mean'),
            avg_crew      = ('crew', 'mean'),
            total_capacity= ('passengers', 'sum'),
            avg_hyperdrive= ('hyperdrive_rating', 'mean'),
            avg_MGLT      = ('MGLT', 'mean')
        )
        .reset_index()
    )

    # Score compuesto: más pasajeros, menos costo, mejor hyperdrive
    # Normalizar 0-1 para scoring
    def norm(series):
        """Normaliza una serie entre 0 y 1."""
        rng = series.max() - series.min()
        return (series - series.min()) / rng if rng > 0 else series * 0

    class_analysis['score_capacity'] = norm(class_analysis['avg_passengers'])
    class_analysis['score_cost']     = 1 - norm(class_analysis['avg_cost'])     # menor costo = mejor
    class_analysis['score_speed']    = norm(class_analysis['avg_MGLT'].fillna(0))

    # Peso: 50% capacidad, 30% costo, 20% velocidad
    class_analysis['strategic_score'] = (
        class_analysis['score_capacity'] * 0.50 +
        class_analysis['score_cost']     * 0.30 +
        class_analysis['score_speed']    * 0.20
    ).round(3)

    class_analysis = class_analysis.sort_values('strategic_score', ascending=False).reset_index(drop=True)
    print(class_analysis[['starship_class', 'count', 'avg_cost', 'avg_passengers', 'strategic_score']].head(8))

    top5 = class_analysis.head(5)

    # Chart: Bubble chart — costo vs capacidad, tamaño = strategic score
    fig = go.Figure(go.Scatter(
        x=class_analysis['avg_cost'] / 1_000_000,
        y=class_analysis['avg_passengers'],
        mode='markers+text',
        text=class_analysis['starship_class'],
        textposition='top center',
        marker=dict(
            size=class_analysis['strategic_score'] * 60 + 10,
            color=class_analysis['strategic_score'],
            colorscale=[[0, LGRAY], [0.5, NAVY], [1, GOLD]],
            showscale=True,
            colorbar=dict(title='Strategic Score', thickness=12)
        ),
        hovertemplate='%{text}<br>Costo Promedio: %{x:.1f}M cr<br>Pasajeros Promedio: %{y:,}<extra></extra>'
    ))
    fig.update_layout(
        TEMPLATE['layout'],
        title='Inversion Estrategica por Clase de Nave<br><sub>Tamano de burbuja = Puntaje Estrategico (50% capacidad + 30% costo + 20% velocidad)</sub>',
        xaxis_title='Costo Promedio (Millones de Creditos)',
        yaxis_title='Capacidad Promedio de Pasajeros',
        height=540
    )
    guardar_chart(fig, 'q3_strategic_investment')

    # Chart 2: Bar horizontal - strategic score por clase
    fig2 = go.Figure(go.Bar(
        x=class_analysis['strategic_score'],
        y=class_analysis['starship_class'],
        orientation='h',
        marker_color=[GOLD if i < 3 else NAVY for i in range(len(class_analysis))],
        text=class_analysis['strategic_score'].apply(lambda x: f'{x:.2f}'),
        textposition='outside'
    ))
    fig2.update_layout(
        TEMPLATE['layout'],
        title='Puntaje Estrategico por Clase de Nave',
        xaxis_title='Puntaje Estrategico (0-1)',
        yaxis=dict(autorange='reversed', showgrid=False),
        height=max(400, len(class_analysis) * 35)
    )
    guardar_chart(fig2, 'q3_class_score_bar')

    guardar_csv(class_analysis, 'q3_strategic_investment')
    return class_analysis


# ============================ Q4: ANOMALÍA LIBRE ============================

def q4_anomalia_libre(starships_raw: pd.DataFrame, characters_raw: pd.DataFrame, planets_raw: pd.DataFrame):
    """
    Responde Q4: hallazgo/anomalía libre en los datos.
    Hallazgo: concentración extrema de poder militar - pocas naves concentran
    casi toda la capacidad de transporte pero son inaccesibles por costo.

    Parámetros:
        starships_raw, characters_raw, planets_raw (pd.DataFrame): DataFrames raw.
    """
    print('\n--- Q4: Anomalía Libre ---')
    df = limpiar_starships(starships_raw)
    planets = limpiar_planets(planets_raw)

    # ANOMALÍA: Concentración de capacidad de pasajeros (Pareto de la flota)
    df_sorted = df.sort_values('passengers', ascending=False).reset_index(drop=True)
    df_sorted['cumulative_pct'] = (df_sorted['passengers'].cumsum() / df_sorted['passengers'].sum() * 100).round(1)
    df_sorted['ship_pct'] = ((df_sorted.index + 1) / len(df_sorted) * 100).round(1)

    # Pareto curve
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sorted['ship_pct'],
        y=df_sorted['cumulative_pct'],
        mode='lines',
        line=dict(color=NAVY, width=2.5),
        name='Capacidad Acumulada',
        fill='tozeroy', fillcolor='rgba(27,42,74,0.1)'
    ))
    # Línea de igualdad perfecta
    fig.add_trace(go.Scatter(
        x=[0, 100], y=[0, 100],
        mode='lines',
        line=dict(color=LGRAY, width=1.5, dash='dash'),
        name='Distribucion Perfecta'
    ))
    # Marcar punto 80/20
    idx_80 = df_sorted[df_sorted['cumulative_pct'] >= 80].index[0]
    pct_ships_80 = df_sorted.loc[idx_80, 'ship_pct']
    fig.add_annotation(
        x=pct_ships_80, y=80,
        text=f'{pct_ships_80:.0f}% de las naves transportan<br>el 80% de todos los pasajeros',
        showarrow=True, arrowhead=2, arrowcolor=RED,
        font=dict(color=RED, size=11), bgcolor='white'
    )
    fig.add_trace(go.Scatter(
        x=[pct_ships_80], y=[80],
        mode='markers', marker=dict(color=GOLD, size=10, symbol='circle'),
        showlegend=False
    ))
    fig.update_layout(
        TEMPLATE['layout'],
        title='[ALERTA] Concentracion de Capacidad: El Riesgo Oculto de la Flota',
        xaxis_title='% de Naves (ordenadas por capacidad)',
        yaxis_title='% Acumulado de Capacidad Total de Pasajeros',
        xaxis=dict(range=[0, 100], dtick=20),
        yaxis=dict(range=[0, 105], dtick=20)
    )
    guardar_chart(fig, 'q4_capacity_concentration')

    # ANOMALÍA 2: Costo de las naves de mayor capacidad vs población a evacuar
    total_pop = planets['population'].sum()
    total_cap = df['passengers'].sum()
    top1_cap = df_sorted.iloc[0]['passengers']
    top1_name = df_sorted.iloc[0]['name']
    top1_cost = df_sorted.iloc[0]['cost_in_credits']

    print(f'  Población total galaxia: {total_pop:,.0f}')
    print(f'  Capacidad total flota: {total_cap:,.0f}')
    print(f'  Nave con mayor capacidad: {top1_name} ({top1_cap:,.0f} pasajeros, costo: {top1_cost:,.0f} cr)')
    print(f'  Viajes necesarios para evacuar: {total_pop / total_cap:,.0f}')

    # Summary stats para CSV
    summary = pd.DataFrame({
        'metrica': ['Poblacion Total de la Galaxia', 'Capacidad Total de la Flota', 'Viajes Necesarios para Evacuar',
                    'Nave con Mayor Capacidad', 'Naves que Cubren el 80% de Capacidad', '% de Naves para 80% Capacidad'],
        'valor': [f'{total_pop:,.0f}', f'{total_cap:,.0f}',
                  f'{total_pop / total_cap:,.1f}',
                  f'{top1_name} ({top1_cap:,.0f} pax)',
                  str(idx_80 + 1),
                  f'{pct_ships_80:.1f}%']
    })

    # Gini-like barras: top 5 naves por capacidad
    top5 = df_sorted.head(5)[['name', 'passengers', 'cost_in_credits']].copy()
    rest_cap = df_sorted.iloc[5:]['passengers'].sum()
    rest_row = pd.DataFrame([{'name': 'Resto de Naves', 'passengers': rest_cap, 'cost_in_credits': 0}])
    top5_plot = pd.concat([top5, rest_row], ignore_index=True)
    top5_plot['color'] = [GOLD if i < 5 else LGRAY for i in range(len(top5_plot))]

    fig2 = go.Figure(go.Bar(
        x=top5_plot['name'],
        y=top5_plot['passengers'],
        marker_color=top5_plot['color'],
        text=top5_plot['passengers'].apply(lambda x: f'{x:,.0f}'),
        textposition='outside'
    ))
    fig2.update_layout(
        TEMPLATE['layout'],
        title='Las 5 Naves que Concentran el Poder de Evacuacion de la Galaxia',
        xaxis_title='Nave', yaxis_title='Capacidad de Pasajeros',
        xaxis_tickangle=-15
    )
    guardar_chart(fig2, 'q4_top5_capacity_dominance')

    guardar_csv(df_sorted[['name', 'starship_class', 'passengers', 'cost_in_credits', 'cumulative_pct', 'ship_pct']], 'q4_capacity_concentration')
    guardar_csv(summary, 'q4_evacuation_summary')

    return df_sorted, summary


# ============================ MAIN ============================

def main():
    """
    Ejecuta el análisis completo del caso Star Wars BI.
    """
    print('=' * 60)
    print('STAR WARS BI CASE — Análisis Completo')
    print('=' * 60)

    # Cargar datos
    chars_raw, ships_raw, planets_raw = cargar_datos()

    # Preview columnas
    print('\nColumnas starships:', list(ships_raw.columns))
    print('Columnas characters:', list(chars_raw.columns))
    print('Columnas planets:', list(planets_raw.columns))

    # Ejecutar análisis
    q1_eficiencia_flota(ships_raw)
    q2_analisis_talento(chars_raw, ships_raw, planets_raw)
    q3_inversion_estrategica(ships_raw)
    q4_anomalia_libre(ships_raw, chars_raw, planets_raw)

    print('\n' + '=' * 60)
    print('Análisis completado. Archivos en:')
    print(f'  CSVs:   {OUT_CSV}')
    print(f'  Charts: {OUT_CHARTS}')
    print('=' * 60)


if __name__ == '__main__':
    main()

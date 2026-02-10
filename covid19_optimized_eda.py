# ==============================================================================
# ANÁLISIS EXPLORATORIO DE DATOS COVID-19 - VERSIÓN OPTIMIZADA
# Genera solo las 4 visualizaciones esenciales para presentación ejecutiva
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import requests
import warnings
import os
from datetime import datetime

warnings.filterwarnings('ignore')

print("🚀 INICIANDO ANÁLISIS EXPLORATORIO OPTIMIZADO COVID-19")
print("=" * 80)

# Crear directorios si no existen
os.makedirs('data', exist_ok=True)
os.makedirs('images', exist_ok=True)

# ==============================================================================
# 1. OBTENCIÓN Y PROCESAMIENTO DE DATOS
# ==============================================================================

def get_covid_data(endpoint):
    """Obtener datos de la API COVID-19"""
    try:
        url = f"https://disease.sh/v3/covid-19/{endpoint}"
        print(f"📡 Obteniendo datos de: {endpoint}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def process_us_data(historical_data):
    """Procesar datos históricos de EE.UU."""
    if not historical_data or 'timeline' not in historical_data:
        return pd.DataFrame()
    
    timeline = historical_data['timeline']
    dates = list(timeline['cases'].keys())
    
    df = pd.DataFrame({
        'date': pd.to_datetime(dates),
        'cases': list(timeline['cases'].values()),
        'deaths': list(timeline['deaths'].values()),
        'recovered': list(timeline['recovered'].values())
    })
    
    # Calcular casos y muertes diarias
    df['daily_cases'] = df['cases'].diff().fillna(0)
    df['daily_deaths'] = df['deaths'].diff().fillna(0)
    df['fatality_rate'] = (df['deaths'] / df['cases'] * 100).fillna(0)
    
    return df

def process_states_data(states_data):
    """Procesar datos por estados"""
    if not states_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(states_data)
    df['fatality_rate'] = (df['deaths'] / df['cases'] * 100).fillna(0)
    df['cases_per_million'] = (df['cases'] / df['population'] * 1000000).fillna(0)
    
    return df

# ==============================================================================
# 2. OBTENER DATOS
# ==============================================================================

print("📊 FASE 1: OBTENCIÓN DE DATOS")

# Obtener datos históricos de EE.UU.
us_historical = get_covid_data("historical/USA?lastdays=all")
df_us = process_us_data(us_historical)

# Obtener datos actuales por estados
states_current = get_covid_data("states")
df_states = process_states_data(states_current)

if not df_us.empty:
    df_us.to_csv('data/us_historical_clean.csv', index=False)
    print("💾 Datos históricos EE.UU. guardados")

if not df_states.empty:
    df_states.to_csv('data/states_clean.csv', index=False)
    print("💾 Datos por estados guardados")

print(f"✅ Datos procesados: {len(df_us)} registros temporales, {len(df_states)} estados")

# ==============================================================================
# 3. VISUALIZACIÓN 1: EVOLUCIÓN TEMPORAL
# ==============================================================================

print("📈 GENERANDO: Evolución Temporal")

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('📈 EVOLUCIÓN TEMPORAL COVID-19 EN ESTADOS UNIDOS', fontsize=16, fontweight='bold')

# Casos acumulados
ax1.plot(df_us['date'], df_us['cases'], color='#1f77b4', linewidth=2)
ax1.set_title('Casos Acumulados', fontweight='bold')
ax1.set_ylabel('Casos Totales')
ax1.ticklabel_format(style='plain', axis='y')
ax1.grid(True, alpha=0.3)

# Muertes acumuladas
ax2.plot(df_us['date'], df_us['deaths'], color='#d62728', linewidth=2)
ax2.set_title('Muertes Acumuladas', fontweight='bold')
ax2.set_ylabel('Muertes Totales')
ax2.ticklabel_format(style='plain', axis='y')
ax2.grid(True, alpha=0.3)

# Casos diarios (promedio móvil 7 días)
df_us['daily_cases_ma7'] = df_us['daily_cases'].rolling(window=7).mean()
ax3.plot(df_us['date'], df_us['daily_cases_ma7'], color='#ff7f0e', linewidth=2)
ax3.set_title('Casos Diarios (Promedio 7 días)', fontweight='bold')
ax3.set_ylabel('Casos Diarios')
ax3.set_xlabel('Fecha')
ax3.grid(True, alpha=0.3)

# Tasa de letalidad
ax4.plot(df_us['date'], df_us['fatality_rate'], color='#9467bd', linewidth=2)
ax4.set_title('Tasa de Letalidad (%)', fontweight='bold')
ax4.set_ylabel('Letalidad (%)')
ax4.set_xlabel('Fecha')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('images/temporal_evolution.png', dpi=300, bbox_inches='tight')
plt.close()

# ==============================================================================
# 4. VISUALIZACIÓN 2: MAPA DE CORRELACIONES
# ==============================================================================

print("🔗 GENERANDO: Mapa de Correlaciones")

# Preparar datos numéricos para correlación
numeric_cols = ['cases', 'deaths', 'recovered', 'active', 'casesPerOneMillion', 
                'deathsPerOneMillion', 'tests', 'testsPerOneMillion']

# Filtrar columnas que existen
available_cols = [col for col in numeric_cols if col in df_states.columns]
correlation_data = df_states[available_cols].corr()

plt.figure(figsize=(12, 10))
mask = np.triu(correlation_data)
sns.heatmap(correlation_data, mask=mask, annot=True, cmap='RdYlBu_r', center=0,
            square=True, fmt='.2f', cbar_kws={"shrink": .8})
plt.title('🔗 MAPA DE CORRELACIONES - VARIABLES COVID-19', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('images/correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# ==============================================================================
# 5. VISUALIZACIÓN 3: RANKINGS DE ESTADOS
# ==============================================================================

print("🏆 GENERANDO: Rankings de Estados")

# Top 10 estados por diferentes métricas
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('🏆 RANKINGS DE ESTADOS - MÉTRICAS COVID-19', fontsize=16, fontweight='bold')

# Top 10 casos totales
top_cases = df_states.nlargest(10, 'cases')
ax1.barh(top_cases['state'], top_cases['cases'], color='#1f77b4')
ax1.set_title('Top 10 Estados - Casos Totales', fontweight='bold')
ax1.set_xlabel('Casos')

# Top 10 muertes totales
top_deaths = df_states.nlargest(10, 'deaths')
ax2.barh(top_deaths['state'], top_deaths['deaths'], color='#d62728')
ax2.set_title('Top 10 Estados - Muertes Totales', fontweight='bold')
ax2.set_xlabel('Muertes')

# Top 10 casos por millón
if 'casesPerOneMillion' in df_states.columns:
    top_cases_pm = df_states.nlargest(10, 'casesPerOneMillion')
    ax3.barh(top_cases_pm['state'], top_cases_pm['casesPerOneMillion'], color='#ff7f0e')
    ax3.set_title('Top 10 Estados - Casos por Millón', fontweight='bold')
    ax3.set_xlabel('Casos por Millón')

# Top 10 tasa de letalidad
df_states_filtered = df_states[df_states['cases'] > 10000]  # Filtrar estados con pocos casos
top_fatality = df_states_filtered.nlargest(10, 'fatality_rate')
ax4.barh(top_fatality['state'], top_fatality['fatality_rate'], color='#9467bd')
ax4.set_title('Top 10 Estados - Tasa de Letalidad (%)', fontweight='bold')
ax4.set_xlabel('Letalidad (%)')

plt.tight_layout()
plt.savefig('images/states_rankings.png', dpi=300, bbox_inches='tight')
plt.close()

# ==============================================================================
# 6. VISUALIZACIÓN 4: DASHBOARD INTERACTIVO
# ==============================================================================

print("📱 GENERANDO: Dashboard Interactivo")

# Dashboard con múltiples gráficos interactivos
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Evolución Temporal de Casos', 'Distribución por Estados', 
                   'Correlación Casos vs Muertes', 'Ranking Top 15 Estados'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}]]
)

# 1. Evolución temporal
fig.add_trace(
    go.Scatter(x=df_us['date'], y=df_us['cases'], 
              name='Casos Acumulados', line=dict(color='blue', width=2)),
    row=1, col=1
)

# 2. Top 15 estados por casos
top15_states = df_states.nlargest(15, 'cases')
fig.add_trace(
    go.Bar(x=top15_states['cases'], y=top15_states['state'], 
           name='Casos por Estado', orientation='h', marker_color='lightblue'),
    row=1, col=2
)

# 3. Scatter casos vs muertes
fig.add_trace(
    go.Scatter(x=df_states['cases'], y=df_states['deaths'],
              mode='markers', name='Estados', 
              text=df_states['state'], textposition='top center',
              marker=dict(size=8, color='red', opacity=0.7)),
    row=2, col=1
)

# 4. Ranking casos por millón (si existe)
if 'casesPerOneMillion' in df_states.columns:
    top15_per_million = df_states.nlargest(15, 'casesPerOneMillion')
    fig.add_trace(
        go.Bar(x=top15_per_million['casesPerOneMillion'], y=top15_per_million['state'],
               name='Casos por Millón', orientation='h', marker_color='orange'),
        row=2, col=2
    )

# Actualizar layout
fig.update_layout(
    title_text="📊 DASHBOARD INTERACTIVO COVID-19 - ESTADOS UNIDOS",
    title_x=0.5,
    title_font_size=20,
    height=800,
    showlegend=True
)

# Guardar como HTML
fig.write_html('images/interactive_dashboard.html')

# ==============================================================================
# 7. REPORTE FINAL
# ==============================================================================

print("\n📋 REPORTE FINAL DE ANÁLISIS")
print("=" * 80)

visualizations = [
    "temporal_evolution.png",
    "correlation_heatmap.png", 
    "states_rankings.png",
    "interactive_dashboard.html"
]

datasets = [
    "us_historical_clean.csv",
    "states_clean.csv"
]

print(f"📊 Visualizaciones generadas ({len(visualizations)}):")
for viz in visualizations:
    print(f"   ✅ {viz}")

print(f"💾 Datasets generados ({len(datasets)}):")
for dataset in datasets:
    print(f"   ✅ {dataset}")

if not df_us.empty and not df_states.empty:
    total_cases = df_us['cases'].iloc[-1]
    total_deaths = df_us['deaths'].iloc[-1]
    final_fatality_rate = df_us['fatality_rate'].iloc[-1]
    
    print(f"📈 ESTADÍSTICAS FINALES:")
    print(f"   • Casos totales EE.UU.: {total_cases:,}")
    print(f"   • Muertes totales EE.UU.: {total_deaths:,}")
    print(f"   • Tasa de letalidad final: {final_fatality_rate:.2f}%")
    print(f"   • Estados analizados: {len(df_states)}")
    print(f"   • Estado más afectado: {df_states.loc[df_states['cases'].idxmax(), 'state']}")
    print(f"   • Período analizado: {df_us['date'].min().strftime('%Y-%m-%d')} a {df_us['date'].max().strftime('%Y-%m-%d')}")

print("\n🎉 ANÁLISIS EXPLORATORIO OPTIMIZADO COMPLETADO!")
print("📊 Solo las 4 visualizaciones esenciales generadas para presentación ejecutiva")
print("🎯 Proyecto optimizado listo para GitHub")

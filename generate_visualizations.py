# ==============================================================================
# SCRIPT DE GENERACIÓN DE VISUALIZACIONES COVID-19 EDA
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import warnings
from datetime import datetime
import os

warnings.filterwarnings('ignore')

# Crear directorios si no existen
os.makedirs('data', exist_ok=True)
os.makedirs('images', exist_ok=True)

print("🚀 Iniciando generación de visualizaciones COVID-19...")

# ==============================================================================
# 1. OBTENER DATOS DE LA API
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

# Obtener datos
print("\n📊 Obteniendo datos de COVID-19...")
us_historical = get_covid_data("historical/USA?lastdays=all")
states_current = get_covid_data("states")

# ==============================================================================
# 2. PROCESAR DATOS
# ==============================================================================

def process_us_data(historical_data):
    """Procesar datos históricos de EE.UU."""
    if not historical_data or 'timeline' not in historical_data:
        return pd.DataFrame()
    
    timeline = historical_data['timeline']
    dates = list(timeline['cases'].keys())
    cases = list(timeline['cases'].values())
    deaths = list(timeline['deaths'].values())
    
    df = pd.DataFrame({
        'date': pd.to_datetime(dates),
        'cases': cases,
        'deaths': deaths
    })
    
    # Calcular casos y muertes nuevas
    df['new_cases'] = df['cases'].diff().fillna(0)
    df['new_deaths'] = df['deaths'].diff().fillna(0)
    
    # Promedios móviles
    df['cases_7day_avg'] = df['new_cases'].rolling(window=7, center=True).mean()
    df['deaths_7day_avg'] = df['new_deaths'].rolling(window=7, center=True).mean()
    
    # Tasa de letalidad
    df['fatality_rate'] = (df['deaths'] / df['cases'] * 100).fillna(0)
    
    return df

def process_states_data(states_data):
    """Procesar datos por estados"""
    if not states_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(states_data)
    
    # Calcular métricas per cápita
    df['cases_per_100k'] = (df['cases'] / df['population'] * 100000).fillna(0)
    df['deaths_per_100k'] = (df['deaths'] / df['population'] * 100000).fillna(0)
    df['fatality_rate'] = (df['deaths'] / df['cases'] * 100).fillna(0)
    
    return df

# Procesar datos
print("🔄 Procesando datos...")
df_us = process_us_data(us_historical)
df_states = process_states_data(states_current)

# Guardar datos procesados
if not df_us.empty:
    df_us.to_csv('data/us_historical_clean.csv', index=False)
    print("💾 Datos históricos EE.UU. guardados")

if not df_states.empty:
    df_states.to_csv('data/states_clean.csv', index=False)
    print("💾 Datos por estados guardados")

# ==============================================================================
# 3. GENERAR VISUALIZACIONES
# ==============================================================================

print("\n📊 Generando visualizaciones...")

# Configurar estilo
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)

# Gráfico 1: Evolución temporal de casos
if not df_us.empty and len(df_us) > 0:
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('📊 COVID-19 Estados Unidos: Evolución Temporal', fontsize=20, fontweight='bold')
    
    # Casos acumulados
    ax1.plot(df_us['date'], df_us['cases'], color='blue', linewidth=2)
    ax1.set_title('🦠 Casos Acumulados', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Casos Totales')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    
    # Muertes acumuladas
    ax2.plot(df_us['date'], df_us['deaths'], color='red', linewidth=2)
    ax2.set_title('☠️ Muertes Acumuladas', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Muertes Totales')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.0f}K'))
    
    # Casos diarios
    ax3.bar(df_us['date'], df_us['new_cases'], alpha=0.6, color='blue', label='Casos Diarios')
    if 'cases_7day_avg' in df_us.columns:
        ax3.plot(df_us['date'], df_us['cases_7day_avg'], color='red', linewidth=3, label='Promedio 7 días')
    ax3.set_title('📈 Casos Diarios y Promedio Móvil', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Casos Nuevos por Día')
    ax3.tick_params(axis='x', rotation=45)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Muertes diarias
    ax4.bar(df_us['date'], df_us['new_deaths'], alpha=0.6, color='red', label='Muertes Diarias')
    if 'deaths_7day_avg' in df_us.columns:
        ax4.plot(df_us['date'], df_us['deaths_7day_avg'], color='darkred', linewidth=3, label='Promedio 7 días')
    ax4.set_title('📈 Muertes Diarias y Promedio Móvil', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Muertes Nuevas por Día')
    ax4.tick_params(axis='x', rotation=45)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('images/temporal_evolution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Gráfico de evolución temporal guardado")

# Gráfico 2: Tasa de letalidad
if not df_us.empty and len(df_us) > 100:  # Asegurar suficientes datos
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Filtrar datos para evitar valores muy tempranos
    df_filtered = df_us[df_us['cases'] > 1000].copy()
    
    if not df_filtered.empty:
        ax.plot(df_filtered['date'], df_filtered['fatality_rate'], linewidth=3, color='darkred', alpha=0.8)
        ax.fill_between(df_filtered['date'], df_filtered['fatality_rate'], alpha=0.3, color='red')
        
        ax.set_title('💀 Evolución de la Tasa de Letalidad COVID-19 (EE.UU.)', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Tasa de Letalidad (%)')
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('images/fatality_rate_evolution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Gráfico de tasa de letalidad guardado")

# Gráfico 3: Rankings de estados
if not df_states.empty and len(df_states) > 0:
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('🏆 Rankings de Estados COVID-19', fontsize=18, fontweight='bold')
    
    # Top 15 por casos totales
    top15_cases = df_states.nlargest(15, 'cases')
    bars1 = ax1.barh(range(len(top15_cases)), top15_cases['cases'], color='skyblue', alpha=0.8)
    ax1.set_yticks(range(len(top15_cases)))
    ax1.set_yticklabels(top15_cases['state'])
    ax1.set_title('📊 Top 15 - Casos Totales', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Casos Totales')
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    ax1.grid(axis='x', alpha=0.3)
    
    # Top 15 por casos per cápita
    top15_per_capita = df_states.nlargest(15, 'cases_per_100k')
    ax2.barh(range(len(top15_per_capita)), top15_per_capita['cases_per_100k'], color='orange', alpha=0.8)
    ax2.set_yticks(range(len(top15_per_capita)))
    ax2.set_yticklabels(top15_per_capita['state'])
    ax2.set_title('📊 Top 15 - Casos por 100k Habitantes', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Casos por 100k Habitantes')
    ax2.grid(axis='x', alpha=0.3)
    
    # Top 15 por muertes
    top15_deaths = df_states.nlargest(15, 'deaths')
    ax3.barh(range(len(top15_deaths)), top15_deaths['deaths'], color='red', alpha=0.8)
    ax3.set_yticks(range(len(top15_deaths)))
    ax3.set_yticklabels(top15_deaths['state'])
    ax3.set_title('💀 Top 15 - Muertes Totales', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Muertes Totales')
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.0f}K'))
    ax3.grid(axis='x', alpha=0.3)
    
    # Top 15 por tasa de letalidad
    top15_fatality = df_states.nlargest(15, 'fatality_rate')
    ax4.barh(range(len(top15_fatality)), top15_fatality['fatality_rate'], color='darkred', alpha=0.8)
    ax4.set_yticks(range(len(top15_fatality)))
    ax4.set_yticklabels(top15_fatality['state'])
    ax4.set_title('📈 Top 15 - Tasa de Letalidad', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Tasa de Letalidad (%)')
    ax4.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('images/states_rankings.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Gráfico de rankings de estados guardado")

# Gráfico 4: Mapa de correlaciones
if not df_states.empty:
    # Seleccionar variables numéricas para correlación
    numeric_columns = ['cases', 'deaths', 'population', 'cases_per_100k', 'deaths_per_100k', 'fatality_rate']
    available_columns = [col for col in numeric_columns if col in df_states.columns]
    
    if len(available_columns) > 2:
        plt.figure(figsize=(12, 10))
        
        correlation_matrix = df_states[available_columns].corr()
        mask = np.triu(np.ones_like(correlation_matrix), k=1)
        
        sns.heatmap(correlation_matrix, 
                   mask=mask,
                   annot=True, 
                   cmap='RdBu_r', 
                   center=0,
                   square=True, 
                   linewidths=0.5,
                   cbar_kws={"shrink": .8},
                   fmt='.3f',
                   annot_kws={'fontsize': 10})
        
        plt.title('🔥 Mapa de Calor: Correlaciones entre Variables COVID-19', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Variables')
        plt.ylabel('Variables')
        plt.tight_layout()
        plt.savefig('images/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Mapa de correlaciones guardado")

# ==============================================================================
# 4. GENERAR GRÁFICO INTERACTIVO CON PLOTLY
# ==============================================================================

if not df_us.empty:
    try:
        # Crear gráfico interactivo
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('📈 Casos Diarios', '☠️ Muertes Diarias', '📊 Casos Acumulados', '💀 Tasa de Letalidad'),
            specs=[[{'secondary_y': False}, {'secondary_y': False}],
                   [{'secondary_y': False}, {'secondary_y': False}]]
        )
        
        # Casos diarios
        fig.add_trace(
            go.Scatter(x=df_us['date'], y=df_us['new_cases'],
                      mode='lines', name='Casos Diarios', line=dict(color='blue', width=1)),
            row=1, col=1
        )
        
        # Muertes diarias
        fig.add_trace(
            go.Scatter(x=df_us['date'], y=df_us['new_deaths'],
                      mode='lines', name='Muertes Diarias', line=dict(color='red', width=1)),
            row=1, col=2
        )
        
        # Casos acumulados
        fig.add_trace(
            go.Scatter(x=df_us['date'], y=df_us['cases'],
                      mode='lines', name='Casos Totales', line=dict(color='green', width=2)),
            row=2, col=1
        )
        
        # Tasa de letalidad
        fig.add_trace(
            go.Scatter(x=df_us['date'], y=df_us['fatality_rate'],
                      mode='lines', name='Tasa de Letalidad', line=dict(color='purple', width=2)),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="🦠 COVID-19 Estados Unidos: Dashboard Interactivo",
            title_font_size=20,
            height=800,
            showlegend=True
        )
        
        # Guardar como HTML
        fig.write_html('images/interactive_dashboard.html')
        print("✅ Dashboard interactivo guardado como HTML")
        
    except Exception as e:
        print(f"⚠️ No se pudo generar el gráfico interactivo: {e}")

# ==============================================================================
# 5. RESUMEN FINAL
# ==============================================================================

print(f"\n🎉 ¡GENERACIÓN DE VISUALIZACIONES COMPLETADA!")
print("=" * 60)

# Listar archivos generados
image_files = []
data_files = []

if os.path.exists('images'):
    image_files = [f for f in os.listdir('images') if f.endswith(('.png', '.html'))]

if os.path.exists('data'):
    data_files = [f for f in os.listdir('data') if f.endswith('.csv')]

print(f"📊 Visualizaciones generadas ({len(image_files)}):")
for img in sorted(image_files):
    print(f"   ✅ {img}")

print(f"\n💾 Archivos de datos generados ({len(data_files)}):")
for data in sorted(data_files):
    print(f"   ✅ {data}")

# Estadísticas finales
if not df_us.empty:
    print(f"\n📈 ESTADÍSTICAS FINALES:")
    print(f"   • Casos totales EE.UU.: {df_us['cases'].max():,}")
    print(f"   • Muertes totales EE.UU.: {df_us['deaths'].max():,}")
    print(f"   • Tasa de letalidad final: {df_us['fatality_rate'].iloc[-1]:.2f}%")
    
if not df_states.empty:
    print(f"   • Estados analizados: {len(df_states)}")
    print(f"   • Estado más afectado: {df_states.loc[df_states['cases'].idxmax(), 'state']}")

print("\n🎯 Todas las visualizaciones están listas para presentación!")
print("📂 Revisa las carpetas images/ y data/ para ver los resultados")

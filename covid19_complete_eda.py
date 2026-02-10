# ==============================================================================
# ANÁLISIS EXPLORATORIO DE DATOS COVID-19 - SCRIPT COMPLETO
# Genera TODAS las visualizaciones y análisis del proyecto EDA
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

print("🚀 INICIANDO ANÁLISIS EXPLORATORIO COMPLETO COVID-19")
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
    cases = list(timeline['cases'].values())
    deaths = list(timeline['deaths'].values())
    
    df = pd.DataFrame({
        'date': pd.to_datetime(dates),
        'cases': cases,
        'deaths': deaths
    })
    
    # Calcular métricas derivadas
    df['new_cases'] = df['cases'].diff().fillna(0)
    df['new_deaths'] = df['deaths'].diff().fillna(0)
    df['cases_7day_avg'] = df['new_cases'].rolling(window=7, center=True).mean()
    df['deaths_7day_avg'] = df['new_deaths'].rolling(window=7, center=True).mean()
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
    
    # Limpiar valores infinitos
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=['cases_per_100k', 'deaths_per_100k', 'fatality_rate'])
    
    return df

# Obtener y procesar datos
print("\n📊 FASE 1: OBTENCIÓN DE DATOS")
us_historical = get_covid_data("historical/USA?lastdays=all")
states_current = get_covid_data("states")

df_us = process_us_data(us_historical)
df_states = process_states_data(states_current)

# Guardar datos limpios
if not df_us.empty:
    df_us.to_csv('data/us_historical_clean.csv', index=False)
    print("💾 Datos históricos EE.UU. guardados")

if not df_states.empty:
    df_states.to_csv('data/states_clean.csv', index=False)
    print("💾 Datos por estados guardados")

print(f"✅ Datos procesados: {len(df_us)} registros temporales, {len(df_states)} estados")

# ==============================================================================
# 2. ANÁLISIS UNIVARIADO - DISTRIBUCIONES Y ESTADÍSTICAS
# ==============================================================================

print("\n📊 FASE 2: ANÁLISIS UNIVARIADO")

# Configurar estilo general
plt.style.use('default')
sns.set_palette("husl")

if not df_states.empty:
    # Figura 1: Histogramas con estadísticas descriptivas
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('📊 Análisis Univariado - Distribuciones de Variables Clave', fontsize=20, fontweight='bold')

    # Histograma 1: Casos per cápita
    ax1.hist(df_states['cases_per_100k'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.axvline(df_states['cases_per_100k'].mean(), color='red', linestyle='--', linewidth=2, 
                label=f'Media: {df_states["cases_per_100k"].mean():.0f}')
    ax1.axvline(df_states['cases_per_100k'].median(), color='orange', linestyle='--', linewidth=2, 
                label=f'Mediana: {df_states["cases_per_100k"].median():.0f}')
    ax1.set_title('📈 Distribución: Casos por 100k Habitantes', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Casos por 100k Habitantes')
    ax1.set_ylabel('Frecuencia (Estados)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Histograma 2: Muertes per cápita
    ax2.hist(df_states['deaths_per_100k'], bins=20, alpha=0.7, color='lightcoral', edgecolor='black')
    ax2.axvline(df_states['deaths_per_100k'].mean(), color='red', linestyle='--', linewidth=2,
                label=f'Media: {df_states["deaths_per_100k"].mean():.0f}')
    ax2.axvline(df_states['deaths_per_100k'].median(), color='orange', linestyle='--', linewidth=2,
                label=f'Mediana: {df_states["deaths_per_100k"].median():.0f}')
    ax2.set_title('💀 Distribución: Muertes por 100k Habitantes', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Muertes por 100k Habitantes')
    ax2.set_ylabel('Frecuencia (Estados)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Histograma 3: Tasa de letalidad
    ax3.hist(df_states['fatality_rate'], bins=20, alpha=0.7, color='gold', edgecolor='black')
    ax3.axvline(df_states['fatality_rate'].mean(), color='red', linestyle='--', linewidth=2,
                label=f'Media: {df_states["fatality_rate"].mean():.2f}%')
    ax3.axvline(df_states['fatality_rate'].median(), color='orange', linestyle='--', linewidth=2,
                label=f'Mediana: {df_states["fatality_rate"].median():.2f}%')
    ax3.set_title('📊 Distribución: Tasa de Letalidad', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Tasa de Letalidad (%)')
    ax3.set_ylabel('Frecuencia (Estados)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Histograma 4: Casos diarios recientes
    if not df_us.empty:
        recent_data = df_us.tail(90)
        ax4.hist(recent_data['new_cases'], bins=25, alpha=0.7, color='lightgreen', edgecolor='black')
        ax4.axvline(recent_data['new_cases'].mean(), color='red', linestyle='--', linewidth=2,
                    label=f'Media: {recent_data["new_cases"].mean():.0f}')
        ax4.axvline(recent_data['new_cases'].median(), color='orange', linestyle='--', linewidth=2,
                    label=f'Mediana: {recent_data["new_cases"].median():.0f}')
        ax4.set_title('🦠 Distribución: Casos Diarios (Últimos 90 días)', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Casos Nuevos por Día')
        ax4.set_ylabel('Frecuencia (Días)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('images/univariate_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Histogramas de distribuciones guardados")

# ==============================================================================
# 3. DETECCIÓN DE OUTLIERS - BOXPLOTS Y ANÁLISIS IQR/Z-SCORE
# ==============================================================================

print("\n🔍 FASE 3: DETECCIÓN DE OUTLIERS")

if not df_states.empty:
    # Figura 2: Boxplots para outliers
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('📦 Detección de Outliers - Análisis con Boxplots', fontsize=20, fontweight='bold')

    # Función para detectar outliers con IQR
    def detect_outliers_iqr(data):
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = data[(data < lower_bound) | (data > upper_bound)]
        return len(outliers)

    # Boxplots con información de outliers
    variables = [
        ('cases_per_100k', 'skyblue', '📈 Casos por 100k'),
        ('deaths_per_100k', 'lightcoral', '💀 Muertes por 100k'),
        ('fatality_rate', 'gold', '📊 Tasa de Letalidad'),
        ('cases', 'lightgreen', '🦠 Casos Totales')
    ]

    for i, (var, color, title) in enumerate(variables):
        ax = [ax1, ax2, ax3, ax4][i]
        if var in df_states.columns:
            data = df_states[var] if var != 'cases' else df_states[var]/1e6
            ax.boxplot(data, patch_artist=True, boxprops=dict(facecolor=color, alpha=0.7))
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.set_ylabel('Millones' if var == 'cases' else ('Por 100k' if 'per_100k' in var else '%'))
            ax.grid(True, alpha=0.3)
            
            outliers_count = detect_outliers_iqr(df_states[var])
            ax.text(0.02, 0.98, f'Outliers: {outliers_count}', transform=ax.transAxes,
                    fontsize=12, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('images/outlier_detection_boxplots.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Boxplots de outliers guardados")

# ==============================================================================
# 4. ANÁLISIS BIVARIADO - SCATTER PLOTS Y CORRELACIONES
# ==============================================================================

print("\n🔗 FASE 4: ANÁLISIS BIVARIADO")

if not df_states.empty:
    # Figura 3: Scatter plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('🔍 Análisis Bivariado - Relaciones entre Variables', fontsize=20, fontweight='bold')

    # Scatter plot 1: Población vs Casos
    scatter1 = ax1.scatter(df_states['population']/1e6, df_states['cases']/1e6,
                          c=df_states['fatality_rate'], cmap='Reds', s=100, alpha=0.7)
    ax1.set_xlabel('Población (Millones)')
    ax1.set_ylabel('Casos Totales (Millones)')
    ax1.set_title('👥 Población vs Casos (Color: Tasa Letalidad)', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    plt.colorbar(scatter1, ax=ax1, label='Tasa Letalidad (%)')
    corr1 = df_states['population'].corr(df_states['cases'])
    ax1.text(0.05, 0.95, f'r = {corr1:.3f}', transform=ax1.transAxes, fontsize=12,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Scatter plot 2: Casos vs Muertes per cápita
    scatter2 = ax2.scatter(df_states['cases_per_100k'], df_states['deaths_per_100k'],
                          c=df_states['population']/1e6, cmap='viridis', s=100, alpha=0.7)
    ax2.set_xlabel('Casos por 100k')
    ax2.set_ylabel('Muertes por 100k')
    ax2.set_title('📊 Casos vs Muertes per cápita (Color: Población)', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    plt.colorbar(scatter2, ax=ax2, label='Población (M)')
    corr2 = df_states['cases_per_100k'].corr(df_states['deaths_per_100k'])
    ax2.text(0.05, 0.95, f'r = {corr2:.3f}', transform=ax2.transAxes, fontsize=12,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Scatter plot 3: Casos vs Letalidad
    scatter3 = ax3.scatter(df_states['cases']/1e6, df_states['fatality_rate'],
                          c=df_states['population']/1e6, cmap='plasma', s=100, alpha=0.7)
    ax3.set_xlabel('Casos (Millones)')
    ax3.set_ylabel('Tasa Letalidad (%)')
    ax3.set_title('📈 Casos vs Letalidad', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    plt.colorbar(scatter3, ax=ax3, label='Población (M)')
    corr3 = df_states['cases'].corr(df_states['fatality_rate'])
    ax3.text(0.05, 0.95, f'r = {corr3:.3f}', transform=ax3.transAxes, fontsize=12,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Scatter plot 4: Población vs Casos per cápita
    scatter4 = ax4.scatter(df_states['population']/1e6, df_states['cases_per_100k'],
                          c=df_states['fatality_rate'], cmap='coolwarm', s=100, alpha=0.7)
    ax4.set_xlabel('Población (Millones)')
    ax4.set_ylabel('Casos por 100k')
    ax4.set_title('🏙️ Población vs Casos per cápita', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    plt.colorbar(scatter4, ax=ax4, label='Tasa Letalidad (%)')
    corr4 = df_states['population'].corr(df_states['cases_per_100k'])
    ax4.text(0.05, 0.95, f'r = {corr4:.3f}', transform=ax4.transAxes, fontsize=12,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig('images/bivariate_scatter_plots.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Scatter plots guardados")

    # Mapa de correlaciones
    correlation_vars = ['cases', 'deaths', 'population', 'cases_per_100k', 'deaths_per_100k', 'fatality_rate']
    available_vars = [var for var in correlation_vars if var in df_states.columns]
    
    if len(available_vars) > 2:
        plt.figure(figsize=(12, 10))
        correlation_matrix = df_states[available_vars].corr()
        mask = np.triu(np.ones_like(correlation_matrix), k=1)
        
        sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='RdBu_r', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8}, fmt='.3f')
        
        plt.title('🔥 Mapa de Correlaciones - Variables COVID-19', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('images/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Mapa de correlaciones guardado")

# ==============================================================================
# 5. ANÁLISIS TEMPORAL - EVOLUCIÓN DE LA PANDEMIA
# ==============================================================================

print("\n📈 FASE 5: ANÁLISIS TEMPORAL")

if not df_us.empty:
    # Evolución temporal completa
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('📊 COVID-19 EE.UU.: Evolución Temporal Completa', fontsize=20, fontweight='bold')

    # Casos acumulados
    ax1.plot(df_us['date'], df_us['cases'], color='blue', linewidth=2.5)
    ax1.set_title('🦠 Casos Acumulados', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Casos Totales')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    ax1.grid(True, alpha=0.3)

    # Muertes acumuladas
    ax2.plot(df_us['date'], df_us['deaths'], color='red', linewidth=2.5)
    ax2.set_title('☠️ Muertes Acumuladas', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Muertes Totales')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.0f}K'))
    ax2.grid(True, alpha=0.3)

    # Casos diarios
    ax3.bar(df_us['date'], df_us['new_cases'], alpha=0.6, color='blue', label='Casos Diarios')
    ax3.plot(df_us['date'], df_us['cases_7day_avg'], color='red', linewidth=3, label='Promedio 7d')
    ax3.set_title('📈 Casos Diarios y Promedio Móvil', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Casos Nuevos/Día')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Muertes diarias
    ax4.bar(df_us['date'], df_us['new_deaths'], alpha=0.6, color='red', label='Muertes Diarias')
    ax4.plot(df_us['date'], df_us['deaths_7day_avg'], color='darkred', linewidth=3, label='Promedio 7d')
    ax4.set_title('📈 Muertes Diarias y Promedio Móvil', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Muertes Nuevas/Día')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # Formatear fechas en todos los ejes x
    for ax in [ax1, ax2, ax3, ax4]:
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig('images/temporal_evolution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Evolución temporal guardada")

    # Evolución de tasa de letalidad
    df_filtered = df_us[df_us['cases'] > 1000].copy()
    if not df_filtered.empty:
        plt.figure(figsize=(16, 8))
        plt.plot(df_filtered['date'], df_filtered['fatality_rate'], linewidth=3, color='darkred')
        plt.fill_between(df_filtered['date'], df_filtered['fatality_rate'], alpha=0.3, color='red')
        plt.title('💀 Evolución de la Tasa de Letalidad COVID-19', fontsize=16, fontweight='bold')
        plt.xlabel('Fecha')
        plt.ylabel('Tasa de Letalidad (%)')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('images/fatality_rate_evolution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Evolución de letalidad guardada")

# ==============================================================================
# 6. RANKINGS Y COMPARACIONES ENTRE ESTADOS
# ==============================================================================

print("\n🏆 FASE 6: RANKINGS DE ESTADOS")

if not df_states.empty:
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('🏆 Rankings de Estados COVID-19', fontsize=18, fontweight='bold')

    # Top 15 casos totales
    top15_cases = df_states.nlargest(15, 'cases')
    ax1.barh(range(len(top15_cases)), top15_cases['cases'], color='skyblue', alpha=0.8)
    ax1.set_yticks(range(len(top15_cases)))
    ax1.set_yticklabels(top15_cases['state'])
    ax1.set_title('📊 Top 15 - Casos Totales', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Casos Totales')
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))

    # Top 15 casos per cápita
    top15_per_capita = df_states.nlargest(15, 'cases_per_100k')
    ax2.barh(range(len(top15_per_capita)), top15_per_capita['cases_per_100k'], color='orange', alpha=0.8)
    ax2.set_yticks(range(len(top15_per_capita)))
    ax2.set_yticklabels(top15_per_capita['state'])
    ax2.set_title('📊 Top 15 - Casos por 100k', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Casos por 100k')

    # Top 15 muertes
    top15_deaths = df_states.nlargest(15, 'deaths')
    ax3.barh(range(len(top15_deaths)), top15_deaths['deaths'], color='red', alpha=0.8)
    ax3.set_yticks(range(len(top15_deaths)))
    ax3.set_yticklabels(top15_deaths['state'])
    ax3.set_title('💀 Top 15 - Muertes', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Muertes Totales')
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.0f}K'))

    # Top 15 tasa de letalidad
    top15_fatality = df_states.nlargest(15, 'fatality_rate')
    ax4.barh(range(len(top15_fatality)), top15_fatality['fatality_rate'], color='darkred', alpha=0.8)
    ax4.set_yticks(range(len(top15_fatality)))
    ax4.set_yticklabels(top15_fatality['state'])
    ax4.set_title('📈 Top 15 - Tasa Letalidad', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Tasa Letalidad (%)')

    plt.tight_layout()
    plt.savefig('images/states_rankings.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Rankings de estados guardados")

# ==============================================================================
# 7. DASHBOARD INTERACTIVO
# ==============================================================================

print("\n📱 FASE 7: DASHBOARD INTERACTIVO")

if not df_us.empty:
    try:
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('📈 Casos Diarios', '☠️ Muertes Diarias', '📊 Casos Acumulados', '💀 Tasa Letalidad')
        )

        # Agregar trazas
        fig.add_trace(go.Scatter(x=df_us['date'], y=df_us['new_cases'], mode='lines',
                                name='Casos Diarios', line=dict(color='blue')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df_us['date'], y=df_us['new_deaths'], mode='lines',
                                name='Muertes Diarias', line=dict(color='red')), row=1, col=2)
        fig.add_trace(go.Scatter(x=df_us['date'], y=df_us['cases'], mode='lines',
                                name='Casos Totales', line=dict(color='green')), row=2, col=1)
        fig.add_trace(go.Scatter(x=df_us['date'], y=df_us['fatality_rate'], mode='lines',
                                name='Tasa Letalidad', line=dict(color='purple')), row=2, col=2)

        fig.update_layout(title_text="🦠 COVID-19 EE.UU.: Dashboard Interactivo",
                         title_font_size=20, height=800, showlegend=True)

        fig.write_html('images/interactive_dashboard.html')
        print("✅ Dashboard interactivo guardado")
    except Exception as e:
        print(f"⚠️ Error creando dashboard interactivo: {e}")

# ==============================================================================
# 8. REPORTE FINAL
# ==============================================================================

print("\n📋 REPORTE FINAL DE ANÁLISIS")
print("=" * 80)

# Listar archivos generados
image_files = [f for f in os.listdir('images') if f.endswith(('.png', '.html'))]
data_files = [f for f in os.listdir('data') if f.endswith('.csv')]

print(f"📊 Visualizaciones generadas ({len(image_files)}):")
for img in sorted(image_files):
    print(f"   ✅ {img}")

print(f"\n💾 Datasets generados ({len(data_files)}):")
for data in sorted(data_files):
    print(f"   ✅ {data}")

# Estadísticas finales
if not df_us.empty and not df_states.empty:
    print(f"\n📈 ESTADÍSTICAS FINALES:")
    print(f"   • Casos totales EE.UU.: {df_us['cases'].max():,}")
    print(f"   • Muertes totales EE.UU.: {df_us['deaths'].max():,}")
    print(f"   • Tasa de letalidad final: {df_us['fatality_rate'].iloc[-1]:.2f}%")
    print(f"   • Estados analizados: {len(df_states)}")
    print(f"   • Estado más afectado: {df_states.loc[df_states['cases'].idxmax(), 'state']}")
    print(f"   • Período analizado: {df_us['date'].min().date()} a {df_us['date'].max().date()}")

print(f"\n🎉 ANÁLISIS EXPLORATORIO COMPLETADO EXITOSAMENTE!")
print("📊 Todas las visualizaciones siguiendo metodología EDA generadas")
print("🎯 Proyecto listo para presentación ejecutiva")

# ==============================================================================
# SCRIPT COMPLEMENTARIO - ANÁLISIS UNIVARIADO Y DETECCIÓN DE OUTLIERS
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("🔍 Generando análisis univariado y detección de outliers...")

# Cargar datos
df_us = pd.read_csv('data/us_historical_clean.csv')
df_states = pd.read_csv('data/states_clean.csv')

# Convertir fecha a datetime
df_us['date'] = pd.to_datetime(df_us['date'])

# Limpiar valores infinitos y NaN
df_states = df_states.replace([np.inf, -np.inf], np.nan)
df_states = df_states.dropna(subset=['cases_per_100k', 'deaths_per_100k', 'fatality_rate'])

print(f"📊 Datos cargados: {len(df_us)} registros temporales, {len(df_states)} estados")

# ==============================================================================
# 1. ANÁLISIS UNIVARIADO - HISTOGRAMAS Y ESTADÍSTICAS DESCRIPTIVAS
# ==============================================================================

# Configurar estilo
plt.style.use('default')
sns.set_palette("husl")

# Figura 1: Histogramas de distribuciones clave
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
fig.suptitle('📊 Análisis Univariado - Distribuciones de Variables Clave', fontsize=20, fontweight='bold')

# Histograma 1: Casos per cápita por estado
ax1.hist(df_states['cases_per_100k'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
ax1.axvline(df_states['cases_per_100k'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {df_states["cases_per_100k"].mean():.0f}')
ax1.axvline(df_states['cases_per_100k'].median(), color='orange', linestyle='--', linewidth=2, label=f'Mediana: {df_states["cases_per_100k"].median():.0f}')
ax1.set_title('📈 Distribución: Casos por 100k Habitantes', fontsize=14, fontweight='bold')
ax1.set_xlabel('Casos por 100k Habitantes')
ax1.set_ylabel('Frecuencia (Estados)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Histograma 2: Muertes per cápita por estado
ax2.hist(df_states['deaths_per_100k'], bins=20, alpha=0.7, color='lightcoral', edgecolor='black')
ax2.axvline(df_states['deaths_per_100k'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {df_states["deaths_per_100k"].mean():.0f}')
ax2.axvline(df_states['deaths_per_100k'].median(), color='orange', linestyle='--', linewidth=2, label=f'Mediana: {df_states["deaths_per_100k"].median():.0f}')
ax2.set_title('💀 Distribución: Muertes por 100k Habitantes', fontsize=14, fontweight='bold')
ax2.set_xlabel('Muertes por 100k Habitantes')
ax2.set_ylabel('Frecuencia (Estados)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Histograma 3: Tasa de letalidad por estado
ax3.hist(df_states['fatality_rate'], bins=20, alpha=0.7, color='gold', edgecolor='black')
ax3.axvline(df_states['fatality_rate'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {df_states["fatality_rate"].mean():.2f}%')
ax3.axvline(df_states['fatality_rate'].median(), color='orange', linestyle='--', linewidth=2, label=f'Mediana: {df_states["fatality_rate"].median():.2f}%')
ax3.set_title('📊 Distribución: Tasa de Letalidad', fontsize=14, fontweight='bold')
ax3.set_xlabel('Tasa de Letalidad (%)')
ax3.set_ylabel('Frecuencia (Estados)')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Histograma 4: Casos diarios nuevos (últimos 90 días)
recent_data = df_us.tail(90)  # Últimos 90 días
ax4.hist(recent_data['new_cases'], bins=25, alpha=0.7, color='lightgreen', edgecolor='black')
ax4.axvline(recent_data['new_cases'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {recent_data["new_cases"].mean():.0f}')
ax4.axvline(recent_data['new_cases'].median(), color='orange', linestyle='--', linewidth=2, label=f'Mediana: {recent_data["new_cases"].median():.0f}')
ax4.set_title('🦠 Distribución: Casos Diarios Nuevos (Últimos 90 días)', fontsize=14, fontweight='bold')
ax4.set_xlabel('Casos Nuevos por Día')
ax4.set_ylabel('Frecuencia (Días)')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('images/univariate_distributions.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Histogramas de distribuciones guardados")

# ==============================================================================
# 2. DETECCIÓN DE OUTLIERS - BOXPLOTS Y MÉTODOS IQR/Z-SCORE
# ==============================================================================

# Figura 2: Boxplots para detectar outliers
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
fig.suptitle('📦 Detección de Outliers - Análisis con Boxplots', fontsize=20, fontweight='bold')

# Boxplot 1: Casos per cápita
box1 = ax1.boxplot(df_states['cases_per_100k'], patch_artist=True, boxprops=dict(facecolor='skyblue', alpha=0.7))
ax1.set_title('📈 Boxplot: Casos por 100k Habitantes', fontsize=14, fontweight='bold')
ax1.set_ylabel('Casos por 100k Habitantes')
ax1.grid(True, alpha=0.3)

# Identificar outliers con IQR
Q1_cases = df_states['cases_per_100k'].quantile(0.25)
Q3_cases = df_states['cases_per_100k'].quantile(0.75)
IQR_cases = Q3_cases - Q1_cases
lower_bound_cases = Q1_cases - 1.5 * IQR_cases
upper_bound_cases = Q3_cases + 1.5 * IQR_cases
outliers_cases = df_states[(df_states['cases_per_100k'] < lower_bound_cases) | 
                          (df_states['cases_per_100k'] > upper_bound_cases)]

ax1.text(0.02, 0.98, f'Outliers detectados: {len(outliers_cases)}', transform=ax1.transAxes, 
         fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Boxplot 2: Muertes per cápita
box2 = ax2.boxplot(df_states['deaths_per_100k'], patch_artist=True, boxprops=dict(facecolor='lightcoral', alpha=0.7))
ax2.set_title('💀 Boxplot: Muertes por 100k Habitantes', fontsize=14, fontweight='bold')
ax2.set_ylabel('Muertes por 100k Habitantes')
ax2.grid(True, alpha=0.3)

# Boxplot 3: Tasa de letalidad
box3 = ax3.boxplot(df_states['fatality_rate'], patch_artist=True, boxprops=dict(facecolor='gold', alpha=0.7))
ax3.set_title('📊 Boxplot: Tasa de Letalidad', fontsize=14, fontweight='bold')
ax3.set_ylabel('Tasa de Letalidad (%)')
ax3.grid(True, alpha=0.3)

# Boxplot 4: Casos diarios (últimos 90 días)
box4 = ax4.boxplot(recent_data['new_cases'], patch_artist=True, boxprops=dict(facecolor='lightgreen', alpha=0.7))
ax4.set_title('🦠 Boxplot: Casos Diarios Nuevos (Últimos 90 días)', fontsize=14, fontweight='bold')
ax4.set_ylabel('Casos Nuevos por Día')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('images/outlier_detection_boxplots.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Boxplots para detección de outliers guardados")

# ==============================================================================
# 3. ANÁLISIS BIVARIADO - SCATTER PLOTS ESPECÍFICOS
# ==============================================================================

# Figura 3: Scatter plots para relaciones bivariadas
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
fig.suptitle('🔍 Análisis Bivariado - Relaciones entre Variables', fontsize=20, fontweight='bold')

# Scatter plot 1: Población vs Casos Totales
scatter1 = ax1.scatter(df_states['population']/1e6, df_states['cases']/1e6, 
                      c=df_states['fatality_rate'], cmap='Reds', s=100, alpha=0.7)
ax1.set_xlabel('Población (Millones)')
ax1.set_ylabel('Casos Totales (Millones)')
ax1.set_title('👥 Población vs Casos Totales (Color: Tasa Letalidad)', fontweight='bold')
ax1.grid(True, alpha=0.3)
plt.colorbar(scatter1, ax=ax1, label='Tasa Letalidad (%)')

# Calcular y mostrar correlación
corr1 = df_states['population'].corr(df_states['cases'])
ax1.text(0.05, 0.95, f'Correlación: {corr1:.3f}', transform=ax1.transAxes, 
         fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Scatter plot 2: Casos per cápita vs Muertes per cápita
scatter2 = ax2.scatter(df_states['cases_per_100k'], df_states['deaths_per_100k'], 
                      c=df_states['population']/1e6, cmap='viridis', s=100, alpha=0.7)
ax2.set_xlabel('Casos por 100k Habitantes')
ax2.set_ylabel('Muertes por 100k Habitantes')
ax2.set_title('📊 Casos vs Muertes per cápita (Color: Población)', fontweight='bold')
ax2.grid(True, alpha=0.3)
plt.colorbar(scatter2, ax=ax2, label='Población (Millones)')

corr2 = df_states['cases_per_100k'].corr(df_states['deaths_per_100k'])
ax2.text(0.05, 0.95, f'Correlación: {corr2:.3f}', transform=ax2.transAxes, 
         fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Scatter plot 3: Casos vs Tasa de Letalidad
scatter3 = ax3.scatter(df_states['cases']/1e6, df_states['fatality_rate'], 
                      c=df_states['population']/1e6, cmap='plasma', s=100, alpha=0.7)
ax3.set_xlabel('Casos Totales (Millones)')
ax3.set_ylabel('Tasa de Letalidad (%)')
ax3.set_title('📈 Casos Totales vs Tasa de Letalidad', fontweight='bold')
ax3.grid(True, alpha=0.3)
plt.colorbar(scatter3, ax=ax3, label='Población (Millones)')

corr3 = df_states['cases'].corr(df_states['fatality_rate'])
ax3.text(0.05, 0.95, f'Correlación: {corr3:.3f}', transform=ax3.transAxes, 
         fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Scatter plot 4: Densidad poblacional vs Casos per cápita
df_states['population_density'] = df_states['population'] / 1000  # Aproximación simple
scatter4 = ax4.scatter(df_states['population_density'], df_states['cases_per_100k'], 
                      c=df_states['fatality_rate'], cmap='coolwarm', s=100, alpha=0.7)
ax4.set_xlabel('Densidad Poblacional (aprox)')
ax4.set_ylabel('Casos por 100k Habitantes')
ax4.set_title('🏙️ Densidad Poblacional vs Casos per cápita', fontweight='bold')
ax4.grid(True, alpha=0.3)
plt.colorbar(scatter4, ax=ax4, label='Tasa Letalidad (%)')

plt.tight_layout()
plt.savefig('images/bivariate_scatter_plots.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Scatter plots bivariados guardados")

# ==============================================================================
# 4. REPORTE DETALLADO DE OUTLIERS
# ==============================================================================

print("\n🔍 REPORTE DETALLADO DE OUTLIERS")
print("=" * 60)

# Función para detectar outliers con IQR
def detect_outliers_iqr(data, column_name):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    return outliers, lower_bound, upper_bound

# Función para detectar outliers con Z-score
def detect_outliers_zscore(data, threshold=2):
    z_scores = np.abs(stats.zscore(data.dropna()))
    outliers_idx = z_scores > threshold
    return data[outliers_idx]

# Analizar casos per cápita
outliers_cases_iqr, lower_cases, upper_cases = detect_outliers_iqr(df_states['cases_per_100k'], 'cases_per_100k')
outliers_cases_zscore = detect_outliers_zscore(df_states['cases_per_100k'])

print(f"\n📈 CASOS PER CÁPITA:")
print(f"   • Media: {df_states['cases_per_100k'].mean():.1f}")
print(f"   • Mediana: {df_states['cases_per_100k'].median():.1f}")
print(f"   • Diferencia Media-Mediana: {abs(df_states['cases_per_100k'].mean() - df_states['cases_per_100k'].median()):.1f}")
print(f"   • Outliers (IQR): {len(outliers_cases_iqr)} estados")
print(f"   • Outliers (Z-score > 2): {len(outliers_cases_zscore)} estados")

if len(outliers_cases_iqr) > 0:
    outlier_states = df_states[df_states['cases_per_100k'].isin(outliers_cases_iqr)]['state'].tolist()
    print(f"   • Estados outliers: {', '.join(outlier_states[:5])}")

# Analizar muertes per cápita
outliers_deaths_iqr, _, _ = detect_outliers_iqr(df_states['deaths_per_100k'], 'deaths_per_100k')
outliers_deaths_zscore = detect_outliers_zscore(df_states['deaths_per_100k'])

print(f"\n💀 MUERTES PER CÁPITA:")
print(f"   • Media: {df_states['deaths_per_100k'].mean():.1f}")
print(f"   • Mediana: {df_states['deaths_per_100k'].median():.1f}")
print(f"   • Diferencia Media-Mediana: {abs(df_states['deaths_per_100k'].mean() - df_states['deaths_per_100k'].median()):.1f}")
print(f"   • Outliers (IQR): {len(outliers_deaths_iqr)} estados")
print(f"   • Outliers (Z-score > 2): {len(outliers_deaths_zscore)} estados")

# Análisis de asimetría
def analyze_skewness(data, name):
    skew = stats.skew(data.dropna())
    if abs(skew) < 0.5:
        skew_desc = "aproximadamente simétrica"
    elif skew > 0.5:
        skew_desc = "asimétrica hacia la derecha"
    else:
        skew_desc = "asimétrica hacia la izquierda"
    
    print(f"   • Asimetría: {skew:.3f} ({skew_desc})")

print(f"\n📊 ANÁLISIS DE ASIMETRÍA:")
analyze_skewness(df_states['cases_per_100k'], "Casos per cápita")
analyze_skewness(df_states['deaths_per_100k'], "Muertes per cápita")
analyze_skewness(df_states['fatality_rate'], "Tasa de letalidad")

print(f"\n🎉 ANÁLISIS COMPLEMENTARIO COMPLETADO!")
print(f"✅ 3 nuevas visualizaciones generadas:")
print(f"   • univariate_distributions.png")
print(f"   • outlier_detection_boxplots.png")  
print(f"   • bivariate_scatter_plots.png")
print(f"\n📊 El proyecto ahora incluye TODOS los elementos de la guía EDA!")

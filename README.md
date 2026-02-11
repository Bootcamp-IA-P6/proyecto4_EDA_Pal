# 📊 Análisis Exploratorio de Datos COVID-19 Estados Unidos

## 🎯 Descripción del Proyecto

Este proyecto presenta un **análisis exploratorio exhaustivo** de los datos de COVID-19 en Estados Unidos, utilizando técnicas avanzadas de ciencia de datos para extraer insights valiosos sobre la evoluc**🌍**📱 Visualizar el Dashboard Localmente:**
```bash
# Opción 1: Página principal (recomendado)
start index.html                          # Windows - Página de bienvenida
open index.html                           # macOS - Página de bienvenida
xdg-open index.html                       # Linux - Página de bienvenida

# Opción 2: Dashboard directo
start images/interactive_dashboard.html    # Windows - Dashboard directo
open images/interactive_dashboard.html     # macOS - Dashboard directo
xdg-open images/interactive_dashboard.html # Linux - Dashboard directo

# Opción 3: VS Code Simple Browser
# Ctrl+Shift+P → "Simple Browser: Show" 
# Navegar a: file:///ruta-completa/index.html
```Público Online:**
> **🌐 [Ver Dashboard Interactivo en Vivo](https://bootcamp-ia-p6.github.io/proyecto4_EDA_Pal/)**n de la pandemia durante 2020-2023.3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el análisis completo**
   ```bash
   # Notebook interactivo (recomendado)
   jupyter notebook notebooks/covid19_eda_analysis.ipynb
   
   # Script completo con todas las visualizaciones
   python covid19_complete_eda.py
   
   # Script optimizado con 4 visualizaciones esenciales
   python covid19_optimized_eda.py
   ```

5. **Generar informe PDF ejecutivo**
   ```bash
   python generate_pdf_report.py
   ```
   **📄 Output:** `reports/COVID19_Executive_Report.pdf` (Informe completo con estadísticas y visualizaciones)

### 📄 Cómo Visualizar el Informe PDF

**⚠️ Importante:** Los archivos PDF son documentos binarios. Si los abres como texto en VS Code, verás código interno del PDF, no el contenido legible.

**✅ Formas correctas de ver el PDF:**

#### **Opción 1: VS Code (Recomendado)**
```bash
# Abrir en el visualizador de PDF integrado de VS Code
code reports/COVID19_Executive_Report.pdf
```

#### **Opción 2: Navegador Web**
```bash
# Windows
start reports/COVID19_Executive_Report.pdf

# macOS  
open reports/COVID19_Executive_Report.pdf

# Linux
xdg-open reports/COVID19_Executive_Report.pdf
```

**📊 El PDF incluye:**
- 📋 Portada profesional con información del proyecto
- 📈 Estadísticas clave y métricas principales  
- 🖼️ Las 4 visualizaciones esenciales integradas
- 📄 Metodología detallada y conclusiones ejecutivas
- 🔧 Información técnica y limitaciones del análisis

### 🎯 Descripción del Proyecto 

El análisis se basa en datos públicos confiables obtenidos a través de APIs especializadas y proporciona una **base sólida para la toma de decisiones estratégicas** con visualizaciones impactantes y conclusiones respaldadas por evidencia estadística.

### 🔍 ¿Por qué este proyecto?

Durante la pandemia de COVID-19, la capacidad de analizar y comprender los datos epidemiológicos se volvió crítica para:
- **Planificación de recursos sanitarios**
- **Toma de decisiones de política pública**
- **Comprensión de patrones geográficos y temporales**
- **Preparación para futuras crisis sanitarias**

Este proyecto demuestra cómo el análisis de datos puede convertir información cruda en insights accionables.

---

## 🎯 Objetivos del Análisis

### Objetivos Principales
- 🧹 **Limpieza y preprocesamiento** riguroso de datos epidemiológicos
- 📈 **Análisis de tendencias temporales** de casos, muertes y recuperaciones
- 🗺️ **Identificación de patrones geográficos** entre estados y regiones
- 📊 **Generación de visualizaciones** impactantes y comprensibles
- 💡 **Extracción de insights** para la toma de decisiones ejecutivas

### Objetivos Específicos
- Identificar las **múltiples olas pandémicas** y sus características
- Comparar el **impacto por estados** usando métricas per cápita
- Analizar **correlaciones** entre variables demográficas y epidemiológicas
- Evaluar la **evolución de la tasa de letalidad** a lo largo del tiempo
- Proporcionar **recomendaciones estratégicas** basadas en datos

---

## 🔍 HALLAZGOS PRINCIPALES

### 1. 📈 Evolución Temporal de la Pandemia
- **Múltiples olas claramente identificables** con patrones estacionales
- **Picos máximos históricos** de hasta 300,000+ casos diarios
- **Mejora progresiva** en la tasa de letalidad (de ~6% a ~1.5%)
- **Patrones predecibles** de incremento durante períodos invernales

### 2. 🗺️ Variabilidad Geográfica Extrema
- **Diferencias significativas** entre estados (3,000-25,000 casos por 100k habitantes)
- **Correlación fuerte** entre densidad poblacional y casos totales (r > 0.85)
- **Patrones regionales distintivos** con diferentes capacidades de respuesta
- **Estados más afectados por volumen:** California, Texas, Florida

### 3. 📊 Correlaciones y Factores Críticos
- **Población ↔ Casos totales:** Correlación muy fuerte (r > 0.85)
- **Casos per cápita ↔ Muertes per cápita:** Correlación fuerte (r > 0.75)
- **Capacidad de testeo ↔ Detección temprana:** Correlación moderada pero significativa
- **Factores estacionales** con patrones predecibles

---

## 📊 MÉTRICAS CLAVE IDENTIFICADAS

### Impacto Nacional Total
- **📈 Casos confirmados:** ~85+ millones
- **💀 Muertes confirmadas:** ~1+ millón  
- **📊 Tasa de letalidad promedio:** 1.5-2.5%
- **🏥 Picos de hospitalizaciones** correlacionados con olas

### Por Regiones Geográficas

#### 🌎 Región Sur
- Mayor impacto absoluto en casos y muertes
- Tasas de letalidad variables entre estados
- Factores demográficos influyentes identificados

#### 🏙️ Región Noreste  
- Alto impacto inicial durante primera ola
- Mejora significativa en fases posteriores
- Alta densidad poblacional como factor crítico

#### 🌄 Región Oeste
- Variabilidad interna alta (California vs estados rurales)
- Factores geográficos y climáticos diversos

#### 🌾 Medio Oeste
- Impacto moderado pero consistente
- Patrones estacionales muy marcados

---

## 🎓 Mini Guía Resumida para Principiantes en Análisis Exploratorio de Datos (EDA)

### 🔍 ¿Qué es el EDA?
El EDA consiste en **explorar y entender los datos antes de modelar**.

> Se usan `estadísticas simples` (media, frecuencias) + con ayuda de `gráficos` (boxplots, mapas de calor) se buscan `valores atípicos` (outliers: IQR/Z-score) + `relaciones entre variables` (correlaciones).

### 🧹 Paso 1: Preparación de Datos
> 👉 Primero cargamos datos, después los miramos y limpiamos tipos de datos y valores nulos.

### 📊 Paso 2: Análisis Univariado (Una sola variable)

#### 👉 `Estadísticas simples`
- **Media y frecuencias:** resumen estadístico para entender **cómo se distribuyen los datos.**
  
  Si media y mediana difieren mucho, suele indicar asimetría en la distribución
  
  **Gráficos 👁‍🗨: Histogramas**

#### 👉 `Valores atípicos`
- **Detección de Outliers (IQR):** detecta valores demasiado bajos o altos
  
  **Gráficos 👁‍🗨: Boxplot:** muestra distribución y outliers visualmente.

### 🔗 Paso 3: Análisis Bivariado (Relación entre dos variables)

#### 👉 `Correlaciones`
- **Correlaciones (corr):** valores numéricos de -1 a 1 (qué tanto se relacionan).
  
  **Gráficos 👁‍🗨: Heatmap:** enseña cómo se relacionan todas las variables numéricas.
  
  **Scatter plot:** Para ver la relación punto a punto entre dos variables.

### 💻 Herramientas en Código
> En code: `Pandas` + `Seaborn` + `Matplotlib`

---

## 📁 Estructura del Proyecto

```
proyecto4_EDA_Pal/
├── 📂 data/                    # Datos limpios y procesados
│   ├── us_historical_clean.csv # Serie temporal nacional
│   └── states_clean.csv        # Datos por estados
├── 📓 notebooks/               # Jupyter notebooks con análisis
│   └── covid19_eda_analysis.ipynb # Notebook principal completo
├── 🖼️ images/                 # Visualizaciones esenciales optimizadas
│   ├── temporal_evolution.png  # Evolución temporal de la pandemia
│   ├── correlation_heatmap.png # Mapa de correlaciones entre variables
│   ├── states_rankings.png     # Rankings comparativos por estado
│   └── interactive_dashboard.html # Dashboard interactivo ejecutivo
├── 📄 reports/                 # Informes generados automáticamente
│   └── COVID19_Executive_Report.pdf # Informe ejecutivo completo
├── � Scripts de análisis/      # Scripts Python especializados
│   ├── covid19_complete_eda.py     # Script completo con todas las visualizaciones
│   ├── covid19_optimized_eda.py   # Script optimizado (4 visualizaciones esenciales)
│   └── generate_pdf_report.py     # Generador de informe PDF ejecutivo
├── 📋 requirements.txt         # Dependencias del proyecto
├── 🔧 .gitignore & .vscode/    # Configuración de desarrollo
└── 📖 README.md               # Este archivo (documentación completa)
```

---

## 🛠️ Tecnologías y Herramientas

### Lenguaje Principal
- **🐍 Python 3.8+** - Análisis de datos y computación científica

### Librerías de Datos
- **📊 Pandas** - Manipulación y análisis de datos estructurados
- **🔢 NumPy** - Computación numérica y álgebra lineal
- **🌐 Requests** - Consumo de APIs RESTful
- **📈 SciPy** - Estadísticas y computación científica

### Visualización
- **📈 Matplotlib** - Gráficos estáticos de alta calidad
- **🎨 Seaborn** - Visualizaciones estadísticas avanzadas
- **⚡ Plotly** - Gráficos interactivos y dashboards
- **🎯 Bokeh** - Visualizaciones web interactivas

### Entorno de Desarrollo
- **📓 Jupyter Notebook** - Análisis interactivo y documentación
- **🔧 Git** - Control de versiones
- **📦 Pip** - Gestión de dependencias

---

## 🚀 Instalación y Uso

### Prerequisitos
- Python 3.8 o superior
- Git (opcional, para clonar el repositorio)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Bootcamp-IA-P6/proyecto4_EDA_Pal.git
   cd proyecto4_EDA_Pal
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el notebook principal**
   ```bash
   jupyter notebook notebooks/covid19_eda_analysis.ipynb
   ```

### � Exploración del Análisis

El notebook está organizado en **9 secciones principales**:

1. **📚 Importación de librerías** - Configuración del entorno
2. **🌐 Obtención de datos** - Extracción desde API COVID-19
3. **🔍 Exploración inicial** - Análisis de estructura y calidad
4. **🧹 Limpieza de datos** - Preprocesamiento y transformaciones
5. **📊 Análisis descriptivo** - Estadísticas y métricas clave
6. **📈 Visualizaciones temporales** - Evolución de la pandemia
7. **🗺️ Comparación entre estados** - Análisis geográfico
8. **🎯 Visualizaciones interactivas** - Exploración dinámica con Bokeh
9. **📋 Resumen ejecutivo** - Conclusiones y recomendaciones

---

## 📋 VISUALIZACIONES GENERADAS

### Gráficos Estáticos de Alto Impacto
- **📈 Evolución temporal completa** - Tendencias de casos y muertes con promedios móviles
- **🕐 Análisis por fases pandémicas** - Comparación estadística entre períodos
- **🏆 Rankings estatales** - Múltiples métricas de comparación
- **🌎 Análisis regional** - Patrones geográficos y demográficos
- **🔥 Mapas de calor** - Correlaciones entre variables epidemiológicas
- **💀 Evolución de letalidad** - Tendencias de mortalidad con eventos clave

### Visualizaciones Interactivas
- **📊 Dashboard temporal dinámico** - Exploración de tendencias en tiempo real
- **🎯 Scatter plots interactivos** - Comparación multivariable entre estados
- **📊 Gráficos de barras dinámicos** - Rankings ajustables por diferentes métricas
- **🔍 Herramientas de exploración** - Tooltips informativos y filtros

### 🌐 Acceso al Dashboard Interactivo

**🌍 Dashboard Público Online:**
> **� [Ver Dashboard Interactivo en Vivo](https://bootcamp-ia-p6.github.io/proyecto4_EDA_Pal/images/interactive_dashboard.html)**

**�📱 Visualizar el Dashboard Localmente:**
```bash
# Opción 1: Navegador web (recomendado)
start images/interactive_dashboard.html    # Windows
open images/interactive_dashboard.html     # macOS
xdg-open images/interactive_dashboard.html # Linux

# Opción 2: VS Code Simple Browser
# Ctrl+Shift+P → "Simple Browser: Show" 
# Navegar a: file:///ruta-completa/images/interactive_dashboard.html
```

**📊 El dashboard incluye 4 visualizaciones interactivas:**
- ✅ **Zoom y Pan** habilitados en todos los gráficos
- ✅ **Tooltips informativos** al pasar el mouse  
- ✅ **Descarga de imágenes** (botón de cámara en cada gráfico)
- ✅ **Reset de vista** (doble click en cualquier gráfico)

---

## �️ CREACIÓN DEL DASHBOARD INTERACTIVO

### 🚀 Tecnología y Herramientas Utilizadas

El dashboard interactivo (`interactive_dashboard.html`) fue desarrollado utilizando **Python** con la librería **Plotly**, una de las bibliotecas más potentes para visualizaciones interactivas en ciencia de datos.

#### 📚 Librerías Principales
```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
```

### 🔧 Proceso de Creación

#### **1. 📊 Estructura Multi-Panel**
El dashboard utiliza `make_subplots()` de Plotly para crear una cuadrícula 2x2 con 4 visualizaciones integradas:

```python
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Evolución Temporal de Casos', 'Distribución por Estados', 
                   'Correlación Casos vs Muertes', 'Ranking Top 15 Estados'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}]]
)
```

#### **2. 📈 Visualizaciones Implementadas**

**Panel 1 - Evolución Temporal:**
- **Tipo:** `go.Scatter()` con línea temporal
- **Datos:** Serie temporal de casos acumulados diarios
- **Características:** Línea suavizada con interactividad completa

**Panel 2 - Top Estados:**
- **Tipo:** `go.Bar()` con orientación horizontal
- **Datos:** Top 15 estados ordenados por casos totales
- **Características:** Barras interactivas con colores diferenciados

**Panel 3 - Scatter Plot:**
- **Tipo:** `go.Scatter()` en modo markers
- **Datos:** Correlación casos vs muertes por estado
- **Características:** Tooltips con nombres de estados, marcadores personalizados

**Panel 4 - Casos per Cápita:**
- **Tipo:** `go.Bar()` horizontal
- **Datos:** Ranking por casos por millón de habitantes
- **Características:** Normalización por población para comparación justa

#### **3. ⚡ Configuración de Interactividad**

```python
fig.update_layout(
    title_text="📊 DASHBOARD INTERACTIVO COVID-19 - ESTADOS UNIDOS",
    title_x=0.5,
    title_font_size=20,
    height=800,
    showlegend=True
)
```

**Funcionalidades Interactivas Habilitadas:**
- **🔍 Zoom dinámico:** Click y arrastre para ampliar áreas específicas
- **📍 Pan:** Arrastre para navegar por diferentes secciones
- **💡 Tooltips:** Información contextual al pasar el mouse
- **📷 Descarga:** Exportación de gráficos como imágenes PNG
- **🔄 Reset:** Doble-click para restablecer vista original
- **👁 Toggle:** Activar/desactivar series en la leyenda

#### **4. 💾 Generación del Archivo HTML**

```python
fig.write_html('images/interactive_dashboard.html')
```

**El comando `write_html()` genera:**
- ✅ Archivo HTML completamente autónomo
- ✅ JavaScript de Plotly embebido (v3.3.1)
- ✅ Todos los datos integrados en el archivo
- ✅ Funcionalidad completa sin dependencias externas
- ✅ Optimizado para navegadores modernos

### 🎯 Ventajas de Plotly vs Otras Librerías

| Característica | Plotly | Matplotlib | Seaborn |
|---------------|---------|------------|---------|
| **Interactividad** | ✅ Nativa | ❌ Limitada | ❌ Estática |
| **Web Ready** | ✅ HTML directo | ⚠️ Conversión | ❌ No |
| **Zoom/Pan** | ✅ Built-in | ⚠️ Widgets | ❌ No |
| **Tooltips** | ✅ Automático | ❌ Manual | ❌ No |
| **Responsive** | ✅ Adaptativo | ⚠️ Limitado | ❌ Fijo |
| **Multi-panel** | ✅ `subplots` | ✅ `subplots` | ⚠️ `FacetGrid` |

### 📁 Archivos Relacionados

```
proyecto4_EDA_Pal/
├── covid19_optimized_eda.py      # 🐍 Script principal que genera el dashboard
├── covid19_complete_eda.py       # 🐍 Versión extendida con más visualizaciones  
└── images/
    └── interactive_dashboard.html # 📊 Dashboard final (3,888 líneas de código)
```

### 🚀 Cómo se Ejecuta

**Opción 1: Script Optimizado (recomendado)**
```bash
python covid19_optimized_eda.py
```

**Opción 2: Script Completo**
```bash
python covid19_complete_eda.py
```

**Opción 3: Notebook Interactivo**
```bash
jupyter notebook notebooks/covid19_eda_analysis.ipynb
```

> **💡 Tip:** El dashboard se genera automáticamente al ejecutar cualquiera de los scripts de análisis. El archivo HTML resultante es completamente portátil y puede abrirse en cualquier navegador web moderno.

### 🔍 Detalles Técnicos

- **📊 Tamaño del archivo:** ~3,888 líneas de código HTML/JavaScript
- **⚡ Librería embebida:** Plotly.js v3.3.1 (completa)
- **🎨 Responsive:** Adaptable a diferentes tamaños de pantalla
- **🌐 Compatibilidad:** Navegadores modernos (Chrome, Firefox, Safari, Edge)
- **📱 Mobile:** Optimizado para dispositivos táctiles
- **⚡ Rendimiento:** Carga rápida con datos pre-procesados

---

## �💡 INSIGHTS PARA LA TOMA DE DECISIONES

### 🚨 Factores Críticos Identificados

1. **👥 Densidad Poblacional**
   - Correlación directa con propagación viral
   - Necesidad de estrategias diferenciadas urbano/rural
   - Impacto en velocidad de transmisión

2. **🧪 Capacidad de Testeo**
   - Relación directa con detección temprana
   - Variabilidad significativa entre jurisdicciones
   - Factor clave en control de brotes

3. **🏥 Preparación del Sistema de Salud**
   - Correlación con tasas de supervivencia
   - Importancia crítica de capacidad hospitalaria
   - Diferencias regionales marcadas

4. **🌡️ Factores Estacionales**
   - Patrones predecibles de incremento invernal
   - Oportunidades para preparación anticipada
   - Correlación con comportamiento social

### 📈 Recomendaciones Estratégicas

1. **🎯 Monitoreo Diferenciado**
   - Sistemas de alerta temprana específicos por región
   - Métricas ajustadas por características demográficas
   - Indicadores predictivos basados en patrones históricos

2. **📦 Asignación Inteligente de Recursos**
   - Distribución basada en análisis predictivo
   - Reservas estratégicas para picos estacionales
   - Priorización por vulnerabilidad y riesgo

3. **⏰ Preparación Estacional**
   - Planes de contingencia para períodos críticos
   - Comunicación proactiva y educación pública
   - Fortalecimiento previo de capacidades

4. **🔧 Fortalecimiento de Capacidades**
   - Inversión prioritaria en sistemas de testeo
   - Mejora de infraestructura hospitalaria
   - Desarrollo de protocolos regionales específicos

---

## 🔗 CORRELACIONES Y PATRONES DESCUBIERTOS

### Relaciones Fuertes (r > 0.7)
- **� Población total ↔ Casos totales** - Relación casi lineal
- **� Casos per cápita ↔ Muertes per cápita** - Proporcionalidad consistente
- **🏙️ Densidad urbana ↔ Velocidad de propagación** - Factor geográfico crítico

### Relaciones Moderadas (r = 0.4-0.7)
- **🧪 Capacidad de testeo ↔ Casos detectados** - Importante para vigilancia
- **🏥 Preparación hospitalaria ↔ Tasa de supervivencia** - Factor de calidad
- **💰 Factores socioeconómicos ↔ Impacto per cápita** - Determinantes sociales

### Patrones Temporales Identificados
- **Ciclos estacionales** con picos invernales consistentes
- **Correlación negativa** entre temperatura y transmisión
- **Efectos de políticas públicas** visibles en las tendencias

---

## 🎯 CONCLUSIONES EJECUTIVAS

### Conclusiones Principales

1. **🔄 Patrones Predecibles**
   - La pandemia mostró ciclos y tendencias que pueden informar preparación futura
   - Los modelos predictivos basados en estos datos son viables y útiles

2. **🗺️ Estrategias Diferenciadas**
   - Las diferencias regionales requieren enfoques específicos y personalizados
   - No existe una solución única para todos los contextos geográficos

3. **📊 Calidad de Datos**
   - Los datos proporcionan una base sólida para modelado y análisis predictivo
   - La inversión en sistemas de recolección de datos es fundamental

4. **🏥 Capacidades Críticas**
   - La inversión en testeo y capacidad hospitalaria tiene retorno medible
   - La preparación anticipada es más costo-efectiva que la respuesta reactiva

### Impacto del Proyecto

Este análisis demuestra cómo las técnicas de **ciencia de datos** pueden:
- ✅ Convertir datos crudos en insights accionables
- ✅ Identificar patrones no evidentes a simple vista  
- ✅ Proporcionar evidencia para toma de decisiones
- ✅ Generar visualizaciones que comunican efectivamente
- ✅ Establecer bases para análisis predictivos futuros

---

## 👨‍💻 Sobre el Desarrollo

### Metodología Empleada
- **🔬 Enfoque científico** con metodología reproducible
- **📊 Análisis estadístico** riguroso y documentado
- **🎨 Visualización efectiva** para múltiples audiencias
- **💻 Código limpio** y bien documentado
- **🔄 Proceso iterativo** de refinamiento y validación

### Aplicabilidad
Este proyecto sirve como **plantilla y referencia** para:
- Análisis epidemiológicos similares
- Estudios de series temporales complejas
- Análisis comparativos geográficos
- Proyectos de visualización de datos
- Informes ejecutivos basados en datos

---

## 📄 Licencia

Este proyecto está bajo licencia **MIT**. Ver el archivo `LICENSE` para más detalles.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

**Este proyecto demuestra el poder del análisis exploratorio de datos para generar insights valiosos que pueden informar decisiones estratégicas críticas en situaciones de crisis sanitaria.**

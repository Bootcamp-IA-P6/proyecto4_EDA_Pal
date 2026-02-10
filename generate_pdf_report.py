# ==============================================================================
# GENERADOR DE INFORME PDF - ANÁLISIS COVID-19
# Genera un informe ejecutivo profesional en PDF con todas las visualizaciones
# ==============================================================================

import pandas as pd
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from datetime import datetime
import os
import warnings

warnings.filterwarnings('ignore')

def create_covid_report():
    """Generar informe PDF completo del análisis COVID-19"""
    
    print("📄 GENERANDO INFORME PDF EJECUTIVO...")
    
    # Crear directorio de reportes si no existe
    os.makedirs('reports', exist_ok=True)
    
    # Configurar el documento PDF
    doc = SimpleDocTemplate(
        "reports/COVID19_Executive_Report.pdf",
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Obtener estilos predefinidos
    styles = getSampleStyleSheet()
    
    # Crear estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=12,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=10,
        textColor=colors.darkred,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    # Lista de elementos del documento
    story = []
    
    # ==============================================================================
    # PORTADA
    # ==============================================================================
    
    # Título principal
    story.append(Spacer(1, 50))
    story.append(Paragraph("📊 ANÁLISIS EXPLORATORIO DE DATOS", title_style))
    story.append(Paragraph("COVID-19 ESTADOS UNIDOS", title_style))
    story.append(Spacer(1, 30))
    
    # Subtítulo
    story.append(Paragraph("Informe Ejecutivo Completo", heading_style))
    story.append(Spacer(1, 20))
    
    # Información del proyecto
    project_info = f"""
    <b>Fecha del Análisis:</b> {datetime.now().strftime('%d de %B, %Y')}<br/>
    <b>Período de Datos:</b> Enero 2020 - Marzo 2023<br/>
    <b>Fuente de Datos:</b> Disease.sh API (Johns Hopkins University)<br/>
    <b>Metodología:</b> Análisis Exploratorio de Datos (EDA)<br/>
    <b>Herramientas:</b> Python, Pandas, Matplotlib, Seaborn, Plotly
    """
    story.append(Paragraph(project_info, body_style))
    story.append(Spacer(1, 40))
    
    # Resumen ejecutivo
    story.append(Paragraph("RESUMEN EJECUTIVO", heading_style))
    
    executive_summary = """
    Este informe presenta un análisis exhaustivo de los datos de COVID-19 en Estados Unidos,
    basado en información oficial de la Universidad Johns Hopkins. El análisis abarca desde
    los primeros casos reportados en enero de 2020 hasta marzo de 2023, proporcionando
    insights valiosos sobre la evolución de la pandemia, patrones geográficos y tendencias
    estadísticas clave que pueden informar la toma de decisiones estratégicas.
    """
    story.append(Paragraph(executive_summary, body_style))
    
    story.append(PageBreak())
    
    # ==============================================================================
    # METODOLOGÍA Y OBJETIVOS
    # ==============================================================================
    
    story.append(Paragraph("1. OBJETIVOS DEL ANÁLISIS", heading_style))
    
    objectives = """
    <b>Objetivo Principal:</b> Extraer insights valiosos de los datos de COVID-19 en Estados Unidos
    mediante técnicas de análisis exploratorio de datos.<br/><br/>
    
    <b>Objetivos Específicos:</b><br/>
    • Analizar la evolución temporal de casos, muertes y recuperaciones<br/>
    • Identificar patrones geográficos y diferencias entre estados<br/>
    • Calcular métricas clave como tasas de letalidad y casos per cápita<br/>
    • Generar visualizaciones impactantes para comunicar hallazgos<br/>
    • Proporcionar conclusiones basadas en evidencia para la toma de decisiones
    """
    story.append(Paragraph(objectives, body_style))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("2. METODOLOGÍA", heading_style))
    
    methodology = """
    <b>Fase 1: Extracción de Datos</b><br/>
    • Consumo de API pública Disease.sh (datos de Johns Hopkins)<br/>
    • Obtención de series temporales nacionales y datos por estados<br/><br/>
    
    <b>Fase 2: Limpieza y Preprocesamiento</b><br/>
    • Validación de integridad de datos<br/>
    • Cálculo de métricas derivadas (casos diarios, tasas de letalidad)<br/>
    • Tratamiento de valores faltantes y outliers<br/><br/>
    
    <b>Fase 3: Análisis Exploratorio</b><br/>
    • Análisis univariado: estadísticas descriptivas<br/>
    • Análisis bivariado: correlaciones entre variables<br/>
    • Análisis temporal: tendencias y estacionalidad<br/>
    • Análisis geográfico: comparaciones entre estados<br/><br/>
    
    <b>Fase 4: Visualización y Reporting</b><br/>
    • Generación de gráficos estáticos e interactivos<br/>
    • Creación de dashboard ejecutivo<br/>
    • Documentación de hallazgos y conclusiones
    """
    story.append(Paragraph(methodology, body_style))
    
    story.append(PageBreak())
    
    # ==============================================================================
    # CARGAR Y MOSTRAR ESTADÍSTICAS
    # ==============================================================================
    
    story.append(Paragraph("3. ESTADÍSTICAS CLAVE", heading_style))
    
    # Cargar datos para estadísticas
    try:
        df_us = pd.read_csv('data/us_historical_clean.csv')
        df_states = pd.read_csv('data/states_clean.csv')
        
        # Estadísticas principales
        total_cases = df_us['cases'].iloc[-1]
        total_deaths = df_us['deaths'].iloc[-1]
        total_recovered = df_us['recovered'].iloc[-1] if 'recovered' in df_us.columns else 0
        final_fatality_rate = (total_deaths / total_cases * 100)
        
        # Estado más afectado
        most_affected_state = df_states.loc[df_states['cases'].idxmax(), 'state']
        most_affected_cases = df_states['cases'].max()
        
        # Período de análisis
        start_date = pd.to_datetime(df_us['date'].iloc[0]).strftime('%d/%m/%Y')
        end_date = pd.to_datetime(df_us['date'].iloc[-1]).strftime('%d/%m/%Y')
        
        stats_text = f"""
        <b>RESUMEN ESTADÍSTICO NACIONAL</b><br/><br/>
        
        • <b>Casos Totales:</b> {total_cases:,} casos confirmados<br/>
        • <b>Muertes Totales:</b> {total_deaths:,} fallecimientos<br/>
        • <b>Casos Recuperados:</b> {total_recovered:,} recuperaciones<br/>
        • <b>Tasa de Letalidad:</b> {final_fatality_rate:.2f}%<br/>
        • <b>Estados Analizados:</b> {len(df_states)} estados y territorios<br/>
        • <b>Período de Análisis:</b> {start_date} al {end_date}<br/><br/>
        
        <b>ESTADO MÁS AFECTADO</b><br/>
        • <b>Estado:</b> {most_affected_state}<br/>
        • <b>Casos Totales:</b> {most_affected_cases:,}<br/>
        """
        
        story.append(Paragraph(stats_text, body_style))
        
    except Exception as e:
        story.append(Paragraph(f"Error al cargar estadísticas: {str(e)}", body_style))
    
    story.append(PageBreak())
    
    # ==============================================================================
    # VISUALIZACIONES
    # ==============================================================================
    
    story.append(Paragraph("4. ANÁLISIS VISUAL", heading_style))
    
    # Función para agregar imagen si existe
    def add_image_if_exists(image_path, title, description):
        if os.path.exists(image_path):
            story.append(Paragraph(title, subheading_style))
            story.append(Paragraph(description, body_style))
            story.append(Spacer(1, 10))
            
            # Agregar imagen (ajustada al ancho de página)
            img = Image(image_path, width=6*inch, height=4.5*inch)
            story.append(img)
            story.append(Spacer(1, 20))
            story.append(PageBreak())
        else:
            story.append(Paragraph(f"⚠️ Imagen no encontrada: {image_path}", body_style))
    
    # 4.1 Evolución Temporal
    add_image_if_exists(
        'images/temporal_evolution.png',
        '4.1 Evolución Temporal de la Pandemia',
        """Esta visualización muestra la evolución de casos acumulados, muertes, casos diarios
        y tasa de letalidad a lo largo del tiempo. Se pueden identificar claramente las diferentes
        olas de la pandemia y cómo la tasa de letalidad ha evolucionado."""
    )
    
    # 4.2 Mapa de Correlaciones
    add_image_if_exists(
        'images/correlation_heatmap.png',
        '4.2 Matriz de Correlaciones',
        """El mapa de calor muestra las correlaciones entre diferentes variables del dataset.
        Las correlaciones fuertes (cercanas a 1 o -1) indican relaciones lineales significativas
        entre variables, mientras que valores cercanos a 0 indican poca relación lineal."""
    )
    
    # 4.3 Rankings de Estados
    add_image_if_exists(
        'images/states_rankings.png',
        '4.3 Rankings Comparativos por Estado',
        """Esta visualización presenta los top 10 estados en diferentes métricas: casos totales,
        muertes totales, casos por millón de habitantes y tasa de letalidad. Permite identificar
        los estados más afectados desde diferentes perspectivas analíticas."""
    )
    
    # ==============================================================================
    # CONCLUSIONES Y RECOMENDACIONES
    # ==============================================================================
    
    story.append(Paragraph("5. CONCLUSIONES Y HALLAZGOS CLAVE", heading_style))
    
    conclusions = """
    <b>HALLAZGOS PRINCIPALES:</b><br/><br/>
    
    <b>1. Evolución Temporal:</b><br/>
    • La pandemia mostró múltiples olas con picos diferenciados<br/>
    • La tasa de letalidad ha disminuido progresivamente desde los primeros meses<br/>
    • Los casos diarios mostraron alta variabilidad estacional<br/><br/>
    
    <b>2. Distribución Geográfica:</b><br/>
    • Existe una gran heterogeneidad en el impacto entre estados<br/>
    • Los estados más poblados tienden a tener más casos absolutos<br/>
    • Sin embargo, los casos per cápita muestran patrones diferentes<br/><br/>
    
    <b>3. Correlaciones Identificadas:</b><br/>
    • Fuerte correlación positiva entre casos y muertes (esperado)<br/>
    • Correlaciones significativas entre población y casos totales<br/>
    • Las métricas per cápita proporcionan mejor comparabilidad<br/><br/>
    
    <b>IMPLICACIONES ESTRATÉGICAS:</b><br/><br/>
    
    • Los datos sugieren la necesidad de enfoques diferenciados por región<br/>
    • La mejora en la tasa de letalidad indica progreso en el tratamiento<br/>
    • La alta variabilidad requiere monitoreo continuo y capacidad de respuesta adaptativa<br/>
    • Las correlaciones identificadas pueden informar modelos predictivos futuros
    """
    story.append(Paragraph(conclusions, body_style))
    
    story.append(PageBreak())
    
    # ==============================================================================
    # INFORMACIÓN TÉCNICA
    # ==============================================================================
    
    story.append(Paragraph("6. INFORMACIÓN TÉCNICA", heading_style))
    
    technical_info = """
    <b>FUENTES DE DATOS:</b><br/>
    • Disease.sh API (https://disease.sh/)<br/>
    • Datos originales: Johns Hopkins University CSSE<br/>
    • Actualización: Datos históricos desde enero 2020<br/><br/>
    
    <b>HERRAMIENTAS Y TECNOLOGÍAS:</b><br/>
    • Python 3.8+ como lenguaje principal<br/>
    • Pandas y NumPy para manipulación de datos<br/>
    • Matplotlib y Seaborn para visualización estática<br/>
    • Plotly para visualizaciones interactivas<br/>
    • ReportLab para generación de este informe PDF<br/><br/>
    
    <b>LIMITACIONES DEL ANÁLISIS:</b><br/>
    • Los datos dependen de la precisión del reporte por jurisdicción<br/>
    • Posibles subregistros en períodos de alta demanda del sistema sanitario<br/>
    • Criterios de reporte pueden haber variado entre estados y períodos<br/>
    • El análisis es descriptivo, no incluye modelado predictivo<br/><br/>
    
    <b>REPRODUCIBILIDAD:</b><br/>
    • Todo el código está disponible en el repositorio del proyecto<br/>
    • Los datos se obtienen mediante API pública y se archivan localmente<br/>
    • La metodología está completamente documentada<br/>
    • El entorno de desarrollo está especificado en requirements.txt
    """
    story.append(Paragraph(technical_info, body_style))
    
    # ==============================================================================
    # PIE DE PÁGINA
    # ==============================================================================
    
    story.append(Spacer(1, 40))
    
    footer_text = f"""
    <b>Informe generado automáticamente el {datetime.now().strftime('%d de %B de %Y a las %H:%M')}</b><br/>
    Proyecto: COVID-19 Exploratory Data Analysis<br/>
    Repositorio: https://github.com/Pal-cloud/proyecto4_EDA_Pal<br/>
    Metodología EDA siguiendo mejores prácticas de ciencia de datos
    """
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    
    story.append(Paragraph(footer_text, footer_style))
    
    # ==============================================================================
    # GENERAR PDF
    # ==============================================================================
    
    try:
        doc.build(story)
        print("✅ Informe PDF generado exitosamente: reports/COVID19_Executive_Report.pdf")
        return True
    except Exception as e:
        print(f"❌ Error al generar PDF: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 GENERADOR DE INFORME PDF COVID-19")
    print("=" * 50)
    
    success = create_covid_report()
    
    if success:
        print("\n🎉 INFORME PDF COMPLETADO!")
        print("📄 Archivo: reports/COVID19_Executive_Report.pdf")
        print("📊 Incluye: estadísticas, visualizaciones y análisis completo")
        print("💼 Listo para presentación ejecutiva")
    else:
        print("\n❌ Error en la generación del informe")
        print("Revisa los archivos de datos y visualizaciones")

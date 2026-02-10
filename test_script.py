import pandas as pd
import matplotlib.pyplot as plt
import requests
import os

print("🚀 Iniciando script de prueba...")

# Crear directorios
os.makedirs('data', exist_ok=True)
os.makedirs('images', exist_ok=True)

print("📁 Directorios creados")

# Probar matplotlib
plt.figure(figsize=(10, 6))
plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.title('📊 Gráfico de Prueba - COVID-19 EDA')
plt.xlabel('Tiempo')
plt.ylabel('Valores')
plt.grid(True, alpha=0.3)
plt.savefig('images/test_plot.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Gráfico de prueba generado")

# Crear datos de ejemplo
data = {
    'date': pd.date_range('2020-01-01', periods=100),
    'cases': [i*100 + (i**1.5)*50 for i in range(100)],
    'deaths': [i*2 + (i**1.2)*10 for i in range(100)]
}

df = pd.DataFrame(data)
df.to_csv('data/sample_data.csv', index=False)
print("✅ Datos de ejemplo guardados")

print("🎉 Script de prueba completado!")

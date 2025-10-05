"""
Análise de Quartis - Boston Housing Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def analyze_quartiles():
    print("="*60)
    print("ANÁLISE DE QUARTIS - BOSTON HOUSING")
    print("="*60)
    
    # Carregar e tratar dados
    df = pd.read_csv('HousingData.csv')
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    print(f"Variáveis analisadas: {df.shape[1]}")
    
    # Análise dos quartis principais
    print(f"\nESTATÍSTICAS DOS QUARTIS:")
    print("-" * 50)
    
    main_vars = ['MEDV', 'RM', 'LSTAT', 'CRIM', 'PTRATIO', 'NOX']
    quartil_data = []
    
    for col in main_vars:
        q1, q2, q3 = df[col].quantile([0.25, 0.5, 0.75])
        iqr = q3 - q1
        outliers = df[(df[col] < q1-1.5*iqr) | (df[col] > q3+1.5*iqr)][col].count()
        quartil_data.append((col, q1, q2, q3, iqr, outliers))
        print(f"{col:8s}: Q1={q1:7.2f} | Q2={q2:7.2f} | Q3={q3:7.2f} | IQR={iqr:6.2f} | Outliers={outliers:3d}")
    
    # Boxplots
    print(f"\n📊 GERANDO BOXPLOTS...")
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for i, col in enumerate(main_vars):
        axes[i].boxplot(df[col], patch_artist=True, 
                       boxprops=dict(facecolor='lightblue', alpha=0.7),
                       medianprops=dict(color='red', linewidth=2))
        axes[i].set_title(f'{col}', fontweight='bold')
        axes[i].grid(True, alpha=0.3)
    
    plt.suptitle('Análise de Quartis - Boston Housing', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    # Resumo
    print(f"\nRESUMO:")
    print("-" * 30)
    
    # Ordenar por IQR e outliers
    quartil_data.sort(key=lambda x: x[4], reverse=True)  # Por IQR
    print(f"Maior dispersão (IQR):")
    for i, (col, _, _, _, iqr, _) in enumerate(quartil_data[:3], 1):
        print(f"  {i}. {col}: {iqr:.2f}")
    
    quartil_data.sort(key=lambda x: x[5], reverse=True)  # Por outliers
    print(f"\nMais outliers:")
    for i, (col, _, _, _, _, outliers) in enumerate(quartil_data[:3], 1):
        pct = (outliers / len(df)) * 100
        print(f"  {i}. {col}: {outliers} ({pct:.1f}%)")
    
    print("=" * 60)

if __name__ == "__main__":
    analyze_quartiles()
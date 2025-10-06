"""
Análise de Correlação - Matriz Básica
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

def analyze_correlations():
    print("="*50)
    print("ANÁLISE DE CORRELAÇÃO - MATRIZ BÁSICA")
    print("="*50)
    
    # Carregar e tratar dados
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'HousingData.csv')
    df = pd.read_csv(csv_path)
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Matriz de correlação
    correlation_matrix = df.corr()
    
    # Correlações com MEDV (variável target)
    medv_corr = correlation_matrix['MEDV'].sort_values(key=abs, ascending=False)
    
    print("\nCORRELAÇÕES COM MEDV (preço):")
    print("-" * 30)
    for var, corr in medv_corr.items():
        if var != 'MEDV':
            print(f"  {var:10s}: {corr:6.3f}")
    
    # Top correlações gerais
    print(f"\nTOP 5 CORRELAÇÕES MAIS FORTES:")
    print("-" * 30)
    
    # Encontrar pares com maior correlação
    correlations = []
    for i in range(len(df.columns)):
        for j in range(i+1, len(df.columns)):
            var1, var2 = df.columns[i], df.columns[j]
            corr = correlation_matrix.loc[var1, var2]
            correlations.append((var1, var2, abs(corr), corr))
    
    # Ordenar por correlação absoluta
    correlations.sort(key=lambda x: x[2], reverse=True)
    
    for var1, var2, abs_corr, corr in correlations[:5]:
        print(f"  {var1} ↔ {var2}: {corr:6.3f}")
    
    # Visualização - Matriz completa
    print(f"\n📊 GERANDO HEATMAP...")
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', 
                cmap='RdBu_r', center=0, cbar_kws={"shrink": .8},
                square=True, linewidths=0.5)
    plt.title('Matriz de Correlação Completa - Boston Housing', pad=20)
    plt.tight_layout()
    plt.show()
    
    # Resumo
    strong_corr = len([1 for _, _, abs_c, _ in correlations if abs_c >= 0.7])
    moderate_corr = len([1 for _, _, abs_c, _ in correlations if 0.3 <= abs_c < 0.7])
    
    print(f"\nRESUMO:")
    print(f"  ✓ Correlações fortes (|r| ≥ 0.7): {strong_corr}")
    print(f"  ✓ Correlações moderadas (0.3 ≤ |r| < 0.7): {moderate_corr}")
    print(f"  ✓ Melhor preditor de MEDV: {medv_corr.index[1]} (r={medv_corr.iloc[1]:.3f})")
    
    print("="*50)
    print("ANÁLISE CONCLUÍDA!")
    print("="*50)

if __name__ == "__main__":
    analyze_correlations()
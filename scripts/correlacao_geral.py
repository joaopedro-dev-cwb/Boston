"""
Análise de Correlação Geral
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

def analyze_general_correlations():
    print("="*50)
    print("CORRELAÇÕES GERAIS")
    print("="*50)
    
    # Carregar dados
    df = pd.read_csv('HousingData.csv')
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Correlações fortes (|r| >= 0.5)
    correlations = []
    for i, var1 in enumerate(df.columns):
        for j, var2 in enumerate(df.columns[i+1:], i+1):
            corr, p_val = pearsonr(df[var1], df[var2])
            if abs(corr) >= 0.5:
                correlations.append((var1, var2, corr, p_val))
    
    correlations.sort(key=lambda x: abs(x[2]), reverse=True)
    
    print(f"\nTop 8 correlações fortes:")
    for var1, var2, corr, p_val in correlations[:8]:
        print(f"  {var1} ↔ {var2}: {corr:6.3f}")
    
    # Heatmap - Matriz completa
    corr_matrix = df.corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', 
                cmap='RdBu_r', center=0, cbar_kws={"shrink": .8},
                square=True, linewidths=0.5)
    plt.title('Matriz de Correlação Completa - Boston Housing', pad=20)
    plt.tight_layout()
    plt.show()
    
    # Resumo
    strong_count = len(correlations)
    significant_count = len([c for c in correlations if c[3] < 0.05])
    
    print(f"\n✓ Correlações fortes: {strong_count}")
    print(f"✓ Significativas: {significant_count}")
    
    return correlations
    strongest_positive = results_df[results_df['Correlação'] > 0].iloc[0]
    strongest_negative = results_df[results_df['Correlação'] < 0].iloc[0]
    
    print(f"Correlação positiva mais forte:")
    print(f"  {strongest_positive['Variável 1']} ↔ {strongest_positive['Variável 2']}")
    print(f"  r = {strongest_positive['Correlação']:.4f}, p = {strongest_positive['P-valor']:.4f}")
    
    print(f"\nCorrelação negativa mais forte:")
    print(f"  {strongest_negative['Variável 1']} ↔ {strongest_negative['Variável 2']}")
    print(f"  r = {strongest_negative['Correlação']:.4f}, p = {strongest_negative['P-valor']:.4f}")
    
    # Correlações não significativas
    non_significant = results_df[results_df['P-valor'] >= 0.05]
    print(f"\nCorrelações NÃO significativas (p ≥ 0.05): {len(non_significant)}")
    if len(non_significant) > 0:
        print("  Exemplos:")
        for _, row in non_significant.head(3).iterrows():
            print(f"    {row['Variável 1']} ↔ {row['Variável 2']}: r={row['Correlação']:.3f}, p={row['P-valor']:.3f}")
    
    return correlation_df, pvalue_df, results_df

if __name__ == "__main__":
    analyze_general_correlations()
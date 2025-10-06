"""
Hipótese: Relação entre Status Socioeconômico (LSTAT) e Valor dos Imóveis (MEDV)
H0: Não há correlação entre LSTAT e MEDV
H1: Há correlação negativa entre LSTAT e MEDV (melhor status = maior preço)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import os
import warnings
warnings.filterwarnings('ignore')

def test_lstat_medv_hypothesis():
    print("="*60)
    print("HIPÓTESE: STATUS SOCIOECONÔMICO vs VALOR DOS IMÓVEIS")
    print("="*60)
    
    # Carregar dados
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', '..', 'HousingData.csv')
    df = pd.read_csv(csv_path)
    
    # Tratar valores ausentes
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    print("H0: Não há correlação entre LSTAT e MEDV")
    print("H1: Há correlação negativa entre LSTAT e MEDV")
    print("    (Melhor status socioeconômico = Maior preço dos imóveis)")
    
    # Teste de correlação
    correlation, p_value = pearsonr(df['LSTAT'], df['MEDV'])
    
    print(f"\nRESULTADOS:")
    print(f"  Correlação (r): {correlation:.4f}")
    print(f"  P-valor: {p_value:.6f}")
    
    # Interpretação da força da correlação
    if abs(correlation) >= 0.7:
        strength = "forte"
    elif abs(correlation) >= 0.3:
        strength = "moderada"
    else:
        strength = "fraca"
    
    print(f"  Força: {strength}")
    print(f"  Direção: {'positiva' if correlation > 0 else 'negativa'}")
    
    # Decisão estatística
    alpha = 0.05
    if p_value < alpha:
        print(f"\n✓ DECISÃO: Rejeitamos H0 (p < {alpha})")
        print("✓ CONCLUSÃO: Há correlação significativa")
        if correlation < -0.7:
            print("✓ RESULTADO: LSTAT é o MELHOR PREDITOR de MEDV!")
    else:
        print(f"\n✗ DECISÃO: Não rejeitamos H0 (p ≥ {alpha})")
        print("✗ CONCLUSÃO: Não há evidência de correlação")
    
    # Categorias por status socioeconômico
    print(f"\nCATEGORIAS:")
    bins = [0, 10, 20, 50]
    labels = ['Alto (<10%)', 'Médio (10-20%)', 'Baixo (>20%)']
    df['Status'] = pd.cut(df['LSTAT'], bins=bins, labels=labels)
    
    for cat in df['Status'].cat.categories:
        subset = df[df['Status'] == cat]
        if len(subset) > 0:
            print(f"  {cat}: ${subset['MEDV'].mean():.1f}k (n={len(subset)})")
    
    # Visualização
    plt.figure(figsize=(10, 6))
    plt.scatter(df['LSTAT'], df['MEDV'], alpha=0.6, s=30, color='blue')
    z = np.polyfit(df['LSTAT'], df['MEDV'], 1)
    p = np.poly1d(z)
    plt.plot(df['LSTAT'], p(df['LSTAT']), "r--", alpha=0.8, linewidth=2)
    plt.xlabel('LSTAT - % Status Socioeconômico Baixo')
    plt.ylabel('MEDV - Valor dos Imóveis ($1000s)')
    plt.title(f'Relação LSTAT vs MEDV\\nr = {correlation:.4f}, p = {p_value:.4f}')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    print("="*60)

if __name__ == "__main__":
    test_lstat_medv_hypothesis()
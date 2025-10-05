"""
Hipótese: Relação entre Número de Quartos (RM) e Valor dos Imóveis (MEDV)
H0: Não há correlação entre RM e MEDV
H1: Há correlação positiva entre RM e MEDV
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import os
import warnings
warnings.filterwarnings('ignore')

def test_rm_medv_hypothesis():
    print("="*60)
    print("HIPÓTESE: QUARTOS vs VALOR DOS IMÓVEIS")
    print("="*60)
    
    # Carregar dados
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', '..', 'HousingData.csv')
    df = pd.read_csv(csv_path)
    
    # Tratar valores ausentes
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    print("H0: Não há correlação entre RM e MEDV")
    print("H1: Há correlação positiva entre RM e MEDV")
    
    # Teste de correlação
    correlation, p_value = pearsonr(df['RM'], df['MEDV'])
    
    print(f"\nRESULTADOS:")
    print(f"  Correlação (r): {correlation:.4f}")
    print(f"  P-valor: {p_value:.6f}")
    
    # Interpretação
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
        print("✓ CONCLUSÃO: Há correlação significativa entre RM e MEDV")
    else:
        print(f"\n✗ DECISÃO: Não rejeitamos H0 (p ≥ {alpha})")
        print("✗ CONCLUSÃO: Não há evidência de correlação significativa")
    
    # Análise rápida por categorias
    print(f"\nCATEGORIAS:")
    bins = [0, 5.5, 6.5, 10]
    labels = ['≤5.5', '5.5-6.5', '>6.5']
    df['RM_cat'] = pd.cut(df['RM'], bins=bins, labels=labels)
    
    for cat in df['RM_cat'].cat.categories:
        subset = df[df['RM_cat'] == cat]
        if len(subset) > 0:
            print(f"  {cat}: ${subset['MEDV'].mean():.1f}k (n={len(subset)})")
    
    # Visualização
    print(f"\n📊 GERANDO GRÁFICO...")
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df['RM'], df['MEDV'], alpha=0.6, s=30, color='blue')
    
    # Linha de tendência
    z = np.polyfit(df['RM'], df['MEDV'], 1)
    p = np.poly1d(z)
    plt.plot(df['RM'], p(df['RM']), "r--", alpha=0.8, linewidth=2)
    
    plt.xlabel('RM - Número de Quartos')
    plt.ylabel('MEDV - Valor dos Imóveis ($1000s)')
    plt.title(f'Relação RM vs MEDV\\nr = {correlation:.4f}, p = {p_value:.4f}')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    print("="*60)
    print("TESTE DE HIPÓTESE CONCLUÍDO!")
    print("="*60)

if __name__ == "__main__":
    test_rm_medv_hypothesis()
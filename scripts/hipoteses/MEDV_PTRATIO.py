"""
Hipótese: Relação entre Razão Aluno-Professor (PTRATIO) e Valor dos Imóveis (MEDV)
H0: Não há correlação entre PTRATIO e MEDV
H1: Há correlação negativa entre PTRATIO e MEDV
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import os
import warnings
warnings.filterwarnings('ignore')

def test_ptratio_medv_hypothesis():
    print("="*60)
    print("HIPÓTESE: EDUCAÇÃO vs VALOR DOS IMÓVEIS")
    print("="*60)
    
    # Carregar dados
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', '..', 'HousingData.csv')
    df = pd.read_csv(csv_path)
    
    # Tratar valores ausentes
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    print("H0: Não há correlação entre PTRATIO e MEDV")
    print("H1: Há correlação negativa entre PTRATIO e MEDV")
    
    # Teste de correlação
    correlation, p_value = pearsonr(df['PTRATIO'], df['MEDV'])
    
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
        print("✓ CONCLUSÃO: Há correlação significativa")
    else:
        print(f"\n✗ DECISÃO: Não rejeitamos H0 (p ≥ {alpha})")
        print("✗ CONCLUSÃO: Não há evidência de correlação")
    
    # Categorias por qualidade
    print(f"\nCATEGORIAS:")
    bins = [0, 17, 19, 25]
    labels = ['Boa (<17)', 'Regular (17-19)', 'Baixa (>19)']
    df['Educacao'] = pd.cut(df['PTRATIO'], bins=bins, labels=labels)
    
    for cat in df['Educacao'].cat.categories:
        subset = df[df['Educacao'] == cat]
        if len(subset) > 0:
            print(f"  {cat}: ${subset['MEDV'].mean():.1f}k (n={len(subset)})")
    
    # Visualização
    plt.figure(figsize=(10, 6))
    plt.scatter(df['PTRATIO'], df['MEDV'], alpha=0.6, s=30, color='green')
    z = np.polyfit(df['PTRATIO'], df['MEDV'], 1)
    p = np.poly1d(z)
    plt.plot(df['PTRATIO'], p(df['PTRATIO']), "r--", alpha=0.8, linewidth=2)
    plt.xlabel('PTRATIO - Razão Aluno-Professor')
    plt.ylabel('MEDV - Valor dos Imóveis ($1000s)')
    plt.title(f'Relação PTRATIO vs MEDV\\nr = {correlation:.4f}, p = {p_value:.4f}')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    print("="*60)
    print("TESTE CONCLUÍDO!")
    print("="*60)

if __name__ == "__main__":
    test_ptratio_medv_hypothesis()
"""
Hipótese: Relação entre Acessibilidade a Rodovias (RAD) e Valor dos Imóveis (MEDV)
H0: Não há correlação entre RAD e MEDV
H1: Há correlação entre RAD e MEDV
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import os
import warnings
warnings.filterwarnings('ignore')

def test_rad_medv_hypothesis():
    print("="*60)
    print("HIPÓTESE: ACESSIBILIDADE vs VALOR DOS IMÓVEIS")
    print("="*60)
    
    # Carregar dados
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', '..', 'HousingData.csv')
    df = pd.read_csv(csv_path)
    
    # Tratar valores ausentes
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    print("H0: Não há correlação entre RAD e MEDV")
    print("H1: Há correlação entre RAD e MEDV")
    
    # Teste de correlação
    correlation, p_value = pearsonr(df['RAD'], df['MEDV'])
    
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
    
    # Acessibilidade por grupos
    print(f"\nGRUPOS DE ACESSIBILIDADE:")
    low_rad = df[df['RAD'] <= 5]
    high_rad = df[df['RAD'] >= 20]
    if len(low_rad) > 0 and len(high_rad) > 0:
        print(f"  Alta (RAD≤5): ${low_rad['MEDV'].mean():.1f}k (n={len(low_rad)})")
        print(f"  Baixa (RAD≥20): ${high_rad['MEDV'].mean():.1f}k (n={len(high_rad)})")
    
    # Visualização
    plt.figure(figsize=(10, 6))
    plt.scatter(df['RAD'], df['MEDV'], alpha=0.6, s=30, color='purple')
    z = np.polyfit(df['RAD'], df['MEDV'], 1)
    p = np.poly1d(z)
    plt.plot(df['RAD'], p(df['RAD']), "r--", alpha=0.8, linewidth=2)
    
    plt.xlabel('RAD - Índice de Acessibilidade a Rodovias')
    plt.ylabel('MEDV - Valor dos Imóveis ($1000s)')
    plt.title(f'Relação RAD vs MEDV\\nr = {correlation:.4f}, p = {p_value:.4f}')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    print("="*60)
    print("TESTE CONCLUÍDO!")
    print("="*60)

if __name__ == "__main__":
    test_rad_medv_hypothesis()
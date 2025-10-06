"""
Análise de Concentração e Distribuição
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def analyze_distributions():
    print("="*60)
    print("ANÁLISE DE CONCENTRAÇÃO E DISTRIBUIÇÃO")
    print("="*60)
    
    # Carregar e tratar dados
    df = pd.read_csv('../HousingData.csv')
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    print(f"Variáveis analisadas: {len(numeric_cols)}")
    
    # Análise das principais variáveis
    main_vars = ['MEDV', 'RM', 'LSTAT', 'CRIM', 'NOX']
    
    print(f"\nESTATÍSTICAS DAS PRINCIPAIS VARIÁVEIS:")
    print("-" * 50)
    
    for col in main_vars:
        mean_val = df[col].mean()
        std_val = df[col].std()
        skewness = df[col].skew()
        cv = (std_val / mean_val) * 100 if mean_val != 0 else 0
        
        # Interpretação da assimetria
        if abs(skewness) < 0.5:
            shape = "Simétrica"
        elif skewness > 0:
            shape = "Assimétrica à direita"
        else:
            shape = "Assimétrica à esquerda"
        
        print(f"\n{col}:")
        print(f"  Média: {mean_val:.3f} | Desvio: {std_val:.3f}")
        print(f"  CV: {cv:.1f}% | Assimetria: {skewness:.2f} ({shape})")
    
    # Visualização
    print(f"\n📊 GERANDO HISTOGRAMAS...")
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for i, col in enumerate(main_vars):
        axes[i].hist(df[col], bins=25, alpha=0.7, color='skyblue', edgecolor='black')
        axes[i].axvline(df[col].mean(), color='red', linestyle='--', linewidth=2, label='Média')
        axes[i].axvline(df[col].median(), color='green', linestyle='--', linewidth=2, label='Mediana')
        axes[i].set_title(f'{col}')
        axes[i].set_ylabel('Frequência')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
    
    if len(main_vars) < 6:
        axes[-1].remove()
    
    plt.tight_layout()
    plt.show()
    
    # Resumo
    high_cv = [col for col in main_vars if (df[col].std()/df[col].mean()*100) > 50]
    print(f"\nRESUMO:")
    print(f"  ✓ Alta variabilidade (CV>50%): {high_cv}")
    print("="*60)

if __name__ == "__main__":
    analyze_distributions()
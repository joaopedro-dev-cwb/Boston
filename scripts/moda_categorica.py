"""
Análise da Moda de Variáveis Categóricas
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def analyze_categorical_mode():
    print("="*60)
    print("ANÁLISE DA MODA - VARIÁVEIS CATEGÓRICAS")
    print("="*60)
    
    # Carregar dados
    df = pd.read_csv('HousingData.csv')
    
    # Tratar valores ausentes
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Variáveis categóricas: CHAS (binária) e RAD (discreta)
    categorical_cols = ['CHAS', 'RAD']
    print(f"Variáveis analisadas: {categorical_cols}")
    
    for col in categorical_cols:
        print(f"\n{col}:")
        
        # Moda e frequências
        moda = df[col].mode()[0]
        freq_moda = (df[col] == moda).sum()
        perc_moda = (freq_moda / len(df)) * 100
        
        print(f"  Moda: {moda}")
        print(f"  Frequência: {freq_moda} ({perc_moda:.1f}%)")
        
        # Distribuição
        distribuicao = df[col].value_counts().sort_index()
        print(f"  Distribuição:")
        for valor, freq in distribuicao.items():  # Top 5
            perc = (freq / len(df) * 100)
            print(f"    {valor}: {freq} ({perc:.1f}%)")
        
        # Variabilidade
        n_categorias = df[col].nunique()
        print(f"  Categorias únicas: {n_categorias}")
        
        # Interpretação
        if perc_moda > 60:
            interp = "Muito concentrada"
        elif perc_moda > 40:
            interp = "Moderadamente concentrada"
        else:
            interp = "Dispersa"
        print(f"  Interpretação: {interp}")
    
    # Visualização
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    for i, col in enumerate(categorical_cols):
        dist = df[col].value_counts().sort_index()
        axes[i].bar(range(len(dist)), dist.values, color='skyblue', edgecolor='black')
        axes[i].set_title(f'{col}')
        axes[i].set_xticks(range(len(dist)))
        axes[i].set_xticklabels(dist.index)
    
    plt.tight_layout()
    plt.show()
    print("="*60)

if __name__ == "__main__":
    analyze_categorical_mode()
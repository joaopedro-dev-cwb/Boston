"""
Análise Principal do Boston Housing Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configurar visualizações
plt.style.use('default')
sns.set_palette("husl")

def main():
    print("="*70)
    print("ANÁLISE BOSTON HOUSING - RESUMO EXECUTIVO")
    print("="*70)
    
    # Carregar e tratar dados
    df = pd.read_csv('HousingData.csv')
    print(f"Dataset: {df.shape[0]} imóveis, {df.shape[1]} variáveis")
    
    # Tratar valores ausentes
    missing = df.isnull().sum().sum()
    if missing > 0:
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
        print(f"Valores ausentes tratados: {missing}")
    
    # Estatísticas do preço (MEDV)
    print(f"\nPREÇO DOS IMÓVEIS (MEDV):")
    print(f"  Média: ${df['MEDV'].mean():.2f}k")
    print(f"  Mediana: ${df['MEDV'].median():.2f}k")
    print(f"  Faixa: ${df['MEDV'].min():.1f}k - ${df['MEDV'].max():.1f}k")
    
    # Top correlações
    correlations = df.corr()['MEDV'].sort_values(key=abs, ascending=False)
    print(f"\nTOP CORRELAÇÕES COM PREÇO:")
    for var, corr in correlations.iloc[1:6].items():  # Top 5 excluindo MEDV
        print(f"  {var:10s}: {corr:6.3f}")
    
    # Outliers principais
    print(f"\nOUTLIERS PRINCIPAIS:")
    for col in ['CRIM', 'ZN', 'B']:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1-1.5*IQR) | (df[col] > Q3+1.5*IQR)][col].count()
        if outliers > 0:
            print(f"  {col}: {outliers} ({outliers/len(df)*100:.1f}%)")
    
    # Resumo
    best_predictor = correlations.iloc[1:].abs().idxmax()
    best_corr = correlations[best_predictor]
    print(f"\n✓ Melhor preditor: {best_predictor} (r={best_corr:.3f})")
    print(f"✓ Dataset limpo e pronto para modelagem")
    
    print("="*70)
    print("ANÁLISE CONCLUÍDA!")
    print("="*70)

if __name__ == "__main__":
    main()
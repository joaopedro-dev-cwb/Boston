"""
Análise Principal do Boston Housing Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'HousingData.csv')
    df = pd.read_csv(csv_path)
    print(f"Dataset: {df.shape[0]} imóveis, {df.shape[1]} variáveis")
    
    # Tratar valores ausentes
    missing = df.isnull().sum().sum()
    if missing > 0:
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
        print(f"Valores ausentes tratados: {missing}")
    
    # Estatísticas gerais do dataset
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    print(f"\nVISÃO GERAL DO DATASET:")
    print(f"  Variáveis numéricas: {len(numeric_cols)}")
    print(f"  Registros completos: {len(df)}")
    
    # Estatísticas do preço (MEDV)
    print(f"\nPREÇO DOS IMÓVEIS (MEDV):")
    print(f"  Média: ${df['MEDV'].mean():.2f}k")
    print(f"  Mediana: ${df['MEDV'].median():.2f}k")
    print(f"  Desvio: ${df['MEDV'].std():.2f}k")
    print(f"  Faixa: ${df['MEDV'].min():.1f}k - ${df['MEDV'].max():.1f}k")
    print(f"  CV: {(df['MEDV'].std()/df['MEDV'].mean()*100):.1f}%")
    
    # Correlações completas com MEDV
    correlations = df.corr()['MEDV'].sort_values(key=abs, ascending=False)
    print(f"\nCORRELAÇÕES COM PREÇO (MEDV):")
    print(f"\n  CORRELAÇÕES FORTES (|r| > 0.6):")
    strong_corr = correlations[abs(correlations) > 0.6].iloc[1:]  # Excluindo MEDV
    for var, corr in strong_corr.items():
        direction = "positiva" if corr > 0 else "negativa" 
        print(f"    {var:8s}: {corr:6.3f} ({direction})")
    
    print(f"\n  CORRELAÇÕES MODERADAS (0.3 < |r| ≤ 0.6):")
    moderate_corr = correlations[(abs(correlations) > 0.3) & (abs(correlations) <= 0.6)]
    for var, corr in moderate_corr.items():
        direction = "positiva" if corr > 0 else "negativa"
        print(f"    {var:8s}: {corr:6.3f} ({direction})")
    
    print(f"\n  CORRELAÇÕES FRACAS (|r| ≤ 0.3):")
    weak_corr = correlations[abs(correlations) <= 0.3]
    for var, corr in weak_corr.items():
        print(f"    {var:8s}: {corr:6.3f}")
    
    # Análise de outliers para todas as variáveis
    print(f"\nANÁLISE DE OUTLIERS (Método IQR):")
    outlier_summary = []
    for col in numeric_cols:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1-1.5*IQR) | (df[col] > Q3+1.5*IQR)][col].count()
        if outliers > 0:
            outlier_summary.append((col, outliers, outliers/len(df)*100))
    
    outlier_summary.sort(key=lambda x: x[1], reverse=True)  # Ordenar por quantidade
    for col, count, pct in outlier_summary[:10]:  # Top 10
        print(f"  {col:8s}: {count:3d} outliers ({pct:4.1f}%)")
    
    # Estatísticas descritivas resumidas
    print(f"\nESTATÍSTICAS DESCRITIVAS - RESUMO:")
    print(f"\n  ALTA VARIABILIDADE (CV > 50%):")
    high_var = []
    for col in numeric_cols:
        cv = (df[col].std() / df[col].mean() * 100) if df[col].mean() != 0 else 0
        if cv > 50:
            high_var.append((col, cv))
    high_var.sort(key=lambda x: x[1], reverse=True)
    for col, cv in high_var:
        print(f"    {col:8s}: CV = {cv:5.1f}%")
    
    print(f"\n  BAIXA VARIABILIDADE (CV < 20%):")
    low_var = []
    for col in numeric_cols:
        cv = (df[col].std() / df[col].mean() * 100) if df[col].mean() != 0 else 0
        if cv < 20 and cv > 0:
            low_var.append((col, cv))
    low_var.sort(key=lambda x: x[1])
    for col, cv in low_var:
        print(f"    {col:8s}: CV = {cv:5.1f}%")
    
    # Resumo executivo final
    best_predictor = correlations.iloc[1:].abs().idxmax()
    best_corr = correlations[best_predictor]
    
    # CORREÇÃO: Calcular registros únicos que são outliers em pelo menos uma variável
    outlier_mask = pd.Series(False, index=df.index)
    for col in numeric_cols:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        col_outliers = (df[col] < Q1-1.5*IQR) | (df[col] > Q3+1.5*IQR)
        outlier_mask = outlier_mask | col_outliers
    
    unique_outliers = outlier_mask.sum()
    outlier_percentage = (unique_outliers / len(df)) * 100
    
    print(f"\nRESUMO EXECUTIVO:")
    print(f"  ✓ Melhor preditor: {best_predictor} (r={best_corr:.3f})")
    print(f"  ✓ Registros com outliers: {unique_outliers} ({outlier_percentage:.1f}%)")
    print(f"  ✓ Variáveis de alta variabilidade: {len(high_var)}")
    print(f"  ✓ Variáveis de baixa variabilidade: {len(low_var)}")
    print(f"  ✓ Correlações fortes (|r|>0.6): {len(strong_corr)}")
    print(f"  ✓ Dataset limpo e pronto para modelagem")
    
    print("="*70)
    print("ANÁLISE EXECUTIVA COMPLETA CONCLUÍDA!")
    print("="*70)

if __name__ == "__main__":
    main()
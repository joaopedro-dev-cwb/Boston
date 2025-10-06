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
    
    # Análise por categorias de status socioeconômico
    print(f"\nCATEGORIAS DE STATUS SOCIOECONÔMICO:")
    
    # Definir categorias baseadas em quartis
    q1 = df['LSTAT'].quantile(0.25)
    q2 = df['LSTAT'].quantile(0.50)
    q3 = df['LSTAT'].quantile(0.75)
    
    print(f"  Quartis LSTAT: Q1={q1:.1f}, Q2={q2:.1f}, Q3={q3:.1f}")
    
    # Criar categorias
    df['Status_Categoria'] = pd.cut(df['LSTAT'], 
                                   bins=[0, q1, q2, q3, 100], 
                                   labels=['Alto Status (Q1)', 'Médio-Alto (Q2)', 'Médio-Baixo (Q3)', 'Baixo Status (Q4)'])
    
    for cat in df['Status_Categoria'].cat.categories:
        subset = df[df['Status_Categoria'] == cat]
        if len(subset) > 0:
            lstat_mean = subset['LSTAT'].mean()
            medv_mean = subset['MEDV'].mean()
            print(f"  {cat}: LSTAT={lstat_mean:.1f}% | MEDV=${medv_mean:.1f}k (n={len(subset)})")
    
    # Análise de extremos
    print(f"\nANÁLISE DE EXTREMOS:")
    
    # 10% com melhor status (LSTAT mais baixo)
    melhor_status = df.nsmallest(int(len(df) * 0.1), 'LSTAT')
    # 10% com pior status (LSTAT mais alto)
    pior_status = df.nlargest(int(len(df) * 0.1), 'LSTAT')
    
    print(f"  Melhor Status (10% menor LSTAT):")
    print(f"    LSTAT médio: {melhor_status['LSTAT'].mean():.1f}%")
    print(f"    MEDV médio: ${melhor_status['MEDV'].mean():.1f}k")
    
    print(f"  Pior Status (10% maior LSTAT):")
    print(f"    LSTAT médio: {pior_status['LSTAT'].mean():.1f}%")
    print(f"    MEDV médio: ${pior_status['MEDV'].mean():.1f}k")
    
    diferenca_preco = melhor_status['MEDV'].mean() - pior_status['MEDV'].mean()
    print(f"  Diferença de Preço: ${diferenca_preco:.1f}k ({diferenca_preco/pior_status['MEDV'].mean()*100:.1f}% maior)")
    
    # Visualização
    plt.figure(figsize=(12, 8))
    
    # Subplot 1: Scatter plot
    plt.subplot(2, 2, 1)
    plt.scatter(df['LSTAT'], df['MEDV'], alpha=0.6, s=30, color='blue')
    z = np.polyfit(df['LSTAT'], df['MEDV'], 1)
    p = np.poly1d(z)
    plt.plot(df['LSTAT'], p(df['LSTAT']), "r--", alpha=0.8, linewidth=2)
    plt.xlabel('LSTAT - % Status Socioeconômico Baixo')
    plt.ylabel('MEDV - Valor dos Imóveis ($1000s)')
    plt.title(f'Relação LSTAT vs MEDV\nr = {correlation:.4f}, p = {p_value:.4f}')
    plt.grid(True, alpha=0.3)
    
    # Subplot 2: Boxplot por categoria
    plt.subplot(2, 2, 2)
    categories = ['Alto Status (Q1)', 'Médio-Alto (Q2)', 'Médio-Baixo (Q3)', 'Baixo Status (Q4)']
    medv_by_status = [df[df['Status_Categoria'] == cat]['MEDV'].values for cat in categories]
    plt.boxplot(medv_by_status, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    plt.xlabel('Quartis de Status (Q1=Melhor)')
    plt.ylabel('MEDV - Valor dos Imóveis ($1000s)')
    plt.title('Distribuição de Preços por Status')
    plt.grid(True, alpha=0.3)
    
    # Subplot 3: Histograma LSTAT
    plt.subplot(2, 2, 3)
    plt.hist(df['LSTAT'], bins=20, alpha=0.7, color='lightblue', edgecolor='black')
    plt.axvline(df['LSTAT'].mean(), color='red', linestyle='--', label=f'Média: {df["LSTAT"].mean():.1f}%')
    plt.xlabel('LSTAT - % Status Socioeconômico Baixo')
    plt.ylabel('Frequência')
    plt.title('Distribuição do Status Socioeconômico')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Subplot 4: Comparação de médias
    plt.subplot(2, 2, 4)
    status_means = [df[df['Status_Categoria'] == cat]['MEDV'].mean() for cat in categories]
    bars = plt.bar(range(len(categories)), status_means, color=['green', 'lightgreen', 'orange', 'red'], alpha=0.7)
    plt.xlabel('Categoria de Status')
    plt.ylabel('MEDV Médio ($1000s)')
    plt.title('Preço Médio por Categoria de Status')
    plt.xticks(range(len(categories)), ['Q1\n(Melhor)', 'Q2', 'Q3', 'Q4\n(Pior)'])
    
    # Adicionar valores nas barras
    for i, v in enumerate(status_means):
        plt.text(i, v + 0.5, f'${v:.1f}k', ha='center', va='bottom', fontweight='bold')
    
    plt.grid(True, alpha=0.3)
    
    plt.suptitle('Análise Completa: Status Socioeconômico vs Valor dos Imóveis', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    print("="*60)

if __name__ == "__main__":
    test_lstat_medv_hypothesis()
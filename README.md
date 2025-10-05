# Análise do Dataset Boston Housing - Versão Simplificada

## 📋 Descrição do Projeto

Este projeto contém uma análise estatística completa do dataset Boston Housing usando scripts Python independentes. Cada script é focado em um aspecto específico da análise de dados.

## 📊 Sobre o Dataset

O dataset Boston Housing contém informações sobre habitação na área metropolitana de Boston, com 506 observações e 14 variáveis:

- **CRIM**: Taxa de criminalidade per capita
- **ZN**: Proporção de terrenos residenciais com lotes > 25.000 pés²
- **INDUS**: Proporção de acres comerciais não-varejistas
- **CHAS**: Variável dummy para proximidade do Rio Charles (1 = próximo, 0 = distante)
- **NOX**: Concentração de óxidos nítricos (ppm)
- **RM**: Número médio de quartos por habitação
- **AGE**: Proporção de unidades ocupadas construídas antes de 1940
- **DIS**: Distância ponderada para 5 centros de emprego de Boston
- **RAD**: Índice de acessibilidade a rodovias radiais
- **TAX**: Taxa de imposto predial por $10.000
- **PTRATIO**: Razão aluno-professor por cidade
- **B**: Proporção de negros por cidade
- **LSTAT**: Porcentagem de população de baixa renda
- **MEDV**: Valor mediano das casas ocupadas pelos proprietários (em $1000s) - **VARIÁVEL TARGET**

## 🗂️ Estrutura do Projeto

```
Boston/
├── data/
│   └── HousingData.csv          # Dataset original
├── scripts/
│   ├── analise.py              # Script principal de análise
│   ├── concentracao_distribuicao.py  # Análise de distribuições
│   ├── moda_categorica.py      # Análise de variáveis categóricas
│   ├── correlacao.py          # Correlações básicas
│   ├── correlacao_geral.py    # Análise completa de correlações
│   └── hipoteses/
│       ├── MEDV_RM.py         # Hipótese: Quartos vs Valor
│       ├── MEDV_PTRATIO.py    # Hipótese: Educação vs Valor
│       └── MEDV_RAD.py        # Hipótese: Acessibilidade vs Valor
└── README.md                   # Este arquivo
```

## 📈 Scripts Disponíveis

### 1. **analise.py** - Análise Principal
- Carregamento e limpeza dos dados
- Estatísticas descritivas completas
- Visão geral do dataset
- Tratamento de valores ausentes

### 2. **concentracao_distribuicao.py** - Análise de Distribuições
- Histogramas de todas as variáveis numéricas
- Análise de concentração de dados
- Gráficos de densidade (KDE)
- Identificação de outliers
- Análise de quartis com boxplots

### 3. **moda_categorica.py** - Variáveis Categóricas
- Análise da variável CHAS (proximidade do rio)
- Cálculo de modas
- Gráficos de barras
- Análise de frequências

### 4. **correlacao.py** - Correlações Básicas
- Matriz de correlação completa
- Heatmap de correlações
- Identificação das correlações mais fortes
- Análise estatística básica

### 5. **correlacao_geral.py** - Análise Avançada de Correlações
- Correlações com significância estatística (p-valores)
- Análise detalhada das correlações com MEDV
- Scatter plots das principais correlações
- Teste de hipóteses para correlações

### 6. **Scripts de Hipóteses** (pasta `hipoteses/`)

#### **MEDV_RM.py** - Número de Quartos vs Valor
- **H0**: Não há correlação entre RM e MEDV
- **H1**: Há correlação positiva entre RM e MEDV
- Análise por categorias de quartos
- Comparação entre extremos
- Visualizações detalhadas

#### **MEDV_PTRATIO.py** - Qualidade Educacional vs Valor
- **H0**: Não há correlação entre PTRATIO e MEDV
- **H1**: Há correlação negativa entre PTRATIO e MEDV
- Análise de impacto educacional
- Categorização por qualidade educacional
- Cálculo do prêmio por educação

#### **MEDV_RAD.py** - Acessibilidade vs Valor
- **H0**: Não há correlação entre RAD e MEDV
- **H1**: Há correlação entre RAD e MEDV
- Teste qui-quadrado de independência
- Análise de padrões não-lineares
- Comparação entre níveis de acessibilidade

## 🚀 Como Executar

### Pré-requisitos
```bash
pip install pandas numpy matplotlib seaborn scipy
```

### Execução Individual
Cada script pode ser executado independentemente:

```bash
# Análise principal
python scripts/analise.py

# Análise de distribuições
python scripts/concentracao_distribuicao.py

# Análise de variáveis categóricas
python scripts/moda_categorica.py

# Correlações básicas
python scripts/correlacao.py

# Correlações avançadas
python scripts/correlacao_geral.py

# Testes de hipóteses
python scripts/hipoteses/MEDV_RM.py
python scripts/hipoteses/MEDV_PTRATIO.py
python scripts/hipoteses/MEDV_RAD.py
```

### Execução Completa
Para executar todos os scripts em sequência:

```bash
cd scripts
python analise.py
python concentracao_distribuicao.py
python moda_categorica.py
python correlacao.py
python correlacao_geral.py
cd hipoteses
python MEDV_RM.py
python MEDV_PTRATIO.py
python MEDV_RAD.py
```

## 📊 Principais Resultados Esperados

### Distribuições
- **MEDV**: Distribuição ligeiramente assimétrica à esquerda
- **RM**: Distribuição aproximadamente normal
- **CRIM**: Distribuição altamente assimétrica à direita

### Correlações Mais Fortes com MEDV
1. **LSTAT** (negativa): -0.74
2. **RM** (positiva): +0.70
3. **PTRATIO** (negativa): -0.51
4. **INDUS** (negativa): -0.48

### Testes de Hipóteses
- **RM vs MEDV**: Correlação positiva significativa (mais quartos = maior valor)
- **PTRATIO vs MEDV**: Correlação negativa significativa (melhor educação = maior valor)
- **RAD vs MEDV**: Relação complexa dependente do contexto urbano

## 🔍 Insights Principais

1. **Número de Quartos (RM)**: Fator mais importante para valorização
2. **Status Socioeconômico (LSTAT)**: Forte impacto negativo nos valores
3. **Qualidade Educacional (PTRATIO)**: Influência significativa na valorização
4. **Localização**: Proximidade do rio Charles valoriza imóveis
5. **Criminalidade (CRIM)**: Impacto negativo moderado nos valores

## 📈 Gráficos Gerados

Cada script gera visualizações específicas:
- Histogramas e boxplots (distribuições)
- Heatmaps de correlação
- Scatter plots com linhas de regressão
- Gráficos de barras (categóricas)
- Análises comparativas por quartis

## 🎯 Metodologia Estatística

- **Testes de Correlação**: Pearson com significância
- **Testes de Hipóteses**: t-test para diferenças de médias
- **Nível de Significância**: α = 0.05
- **Tratamento de Dados**: Imputação por mediana para valores ausentes

## 📝 Observações Importantes

1. **Dados Faltantes**: Tratados por imputação com mediana
2. **Outliers**: Identificados mas mantidos para análise realística
3. **Multicolinearidade**: Algumas variáveis são correlacionadas entre si
4. **Época dos Dados**: Dataset histórico (anos 1970), resultados podem não refletir mercado atual

## 🛠️ Tecnologias Utilizadas

- **Python 3.6+**
- **Pandas**: Manipulação de dados
- **NumPy**: Computação numérica
- **Matplotlib**: Visualizações básicas
- **Seaborn**: Visualizações estatísticas avançadas
- **SciPy**: Testes estatísticos

## 📄 Licença

Este projeto é para fins educacionais e de análise de dados.

---

**Desenvolvido para análise do dataset Boston Housing - Versão Simplificada com Scripts Independentes**
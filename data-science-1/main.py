#!/usr/bin/env python
# coding: utf-8

# # Desafio 3
# 
# Neste desafio, iremos praticar nossos conhecimentos sobre distribuições de probabilidade. Para isso,
# dividiremos este desafio em duas partes:
#     
# 1. A primeira parte contará com 3 questões sobre um *data set* artificial com dados de uma amostra normal e
#     uma binomial.
# 2. A segunda parte será sobre a análise da distribuição de uma variável do _data set_ [Pulsar Star](https://archive.ics.uci.edu/ml/datasets/HTRU2), contendo 2 questões.
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Setup_ geral

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sct
import seaborn as sns
from statsmodels.distributions.empirical_distribution import ECDF


# ## Parte 1

# ### _Setup_ da parte 1

# In[3]:


np.random.seed(42)
    
dataframe = pd.DataFrame({"normal": sct.norm.rvs(20, 4, size=10000),
                     "binomial": sct.binom.rvs(100, 0.2, size=10000)})


# ## Inicie sua análise a partir da parte 1 a partir daqui

# In[3]:


# Sua análise da parte 1 começa aqui.
dataframe.head(10)
# dataframe.quantile((0.25, 0.5, 0.75))
# ((dataframe['normal'].quantile((0.25)) - dataframe['binomial'].quantile(0.25)),(dataframe['normal'].quantile((0.5)) - dataframe['binomial'].quantile(0.5)),(dataframe['normal'].quantile((0.75)) - dataframe['binomial'].quantile(0.75)))
# round((dataframe['normal'].quantile((0.25))), 3)


# ## Questão 1
# 
# Qual a diferença entre os quartis (Q1, Q2 e Q3) das variáveis `normal` e `binomial` de `dataframe`? Responda como uma tupla de três elementos arredondados para três casas decimais.
# 
# Em outra palavras, sejam `q1_norm`, `q2_norm` e `q3_norm` os quantis da variável `normal` e `q1_binom`, `q2_binom` e `q3_binom` os quantis da variável `binom`, qual a diferença `(q1_norm - q1 binom, q2_norm - q2_binom, q3_norm - q3_binom)`?

# In[4]:


def q1():
    diff1 = round((dataframe['normal'].quantile((0.25)) - dataframe['binomial'].quantile(0.25)), 3)
    diff2 = round((dataframe['normal'].quantile((0.5)) - dataframe['binomial'].quantile(0.5)), 3)
    diff3 = round((dataframe['normal'].quantile((0.75)) - dataframe['binomial'].quantile(0.75)), 3)
    diff_all = (diff1, diff2, diff3)
    return diff_all


# Para refletir:
# 
# * Você esperava valores dessa magnitude?
# 
# * Você é capaz de explicar como distribuições aparentemente tão diferentes (discreta e contínua, por exemplo) conseguem dar esses valores?

# ## Questão 2
# 
# Considere o intervalo $[\bar{x} - s, \bar{x} + s]$, onde $\bar{x}$ é a média amostral e $s$ é o desvio padrão. Qual a probabilidade nesse intervalo, calculada pela função de distribuição acumulada empírica (CDF empírica) da variável `normal`? Responda como uma único escalar arredondado para três casas decimais.

# In[5]:


def q2():
    normal_mean = dataframe["normal"].mean()
    normal_std = dataframe["normal"].std()
    ecdf = ECDF(dataframe["normal"])
    dist = ecdf(normal_mean + normal_std) - ecdf(normal_mean - normal_std)
    return np.around(dist, 3)


# Para refletir:
# 
# * Esse valor se aproxima do esperado teórico?
# * Experimente também para os intervalos $[\bar{x} - 2s, \bar{x} + 2s]$ e $[\bar{x} - 3s, \bar{x} + 3s]$.

# ## Questão 3
# 
# Qual é a diferença entre as médias e as variâncias das variáveis `binomial` e `normal`? Responda como uma tupla de dois elementos arredondados para três casas decimais.
# 
# Em outras palavras, sejam `m_binom` e `v_binom` a média e a variância da variável `binomial`, e `m_norm` e `v_norm` a média e a variância da variável `normal`. Quais as diferenças `(m_binom - m_norm, v_binom - v_norm)`?

# In[7]:


def q3():
    m_binom = dataframe["binomial"].mean()
    v_binom = dataframe["binomial"].var()
    m_norm = dataframe["normal"].mean()
    v_norm = dataframe["normal"].var()
    diff_mean = np.around((m_binom - m_norm), 3)
    diff_var = np.around((v_binom - v_norm), 3)
    return (diff_mean, diff_var)


# Para refletir:
# 
# * Você esperava valore dessa magnitude?
# * Qual o efeito de aumentar ou diminuir $n$ (atualmente 100) na distribuição da variável `binomial`?

# ## Parte 2

# ### _Setup_ da parte 2

# In[4]:


stars = pd.read_csv("pulsar_stars.csv")

stars.rename({old_name: new_name
              for (old_name, new_name)
              in zip(stars.columns,
                     ["mean_profile", "sd_profile", "kurt_profile", "skew_profile", "mean_curve", "sd_curve", "kurt_curve", "skew_curve", "target"])
             },
             axis=1, inplace=True)

stars.loc[:, "target"] = stars.target.astype(bool)


# ## Inicie sua análise da parte 2 a partir daqui

# In[9]:


# Sua análise da parte 2 começa aqui.
stars.head(10)


# ## Questão 4
# 
# Considerando a variável `mean_profile` de `stars`:
# 
# 1. Filtre apenas os valores de `mean_profile` onde `target == 0` (ou seja, onde a estrela não é um pulsar).
# 2. Padronize a variável `mean_profile` filtrada anteriormente para ter média 0 e variância 1.
# 
# Chamaremos a variável resultante de `false_pulsar_mean_profile_standardized`.
# 
# Encontre os quantis teóricos para uma distribuição normal de média 0 e variância 1 para 0.80, 0.90 e 0.95 através da função `norm.ppf()` disponível em `scipy.stats`.
# 
# Quais as probabilidade associadas a esses quantis utilizando a CDF empírica da variável `false_pulsar_mean_profile_standardized`? Responda como uma tupla de três elementos arredondados para três casas decimais.

# In[8]:


def q4():
    false_pulsar_mean_profile = stars.loc[stars['target'] == False]

    false_pulsar_mean_profile_standardized = false_pulsar_mean_profile.copy()
    false_pulsar_mean_profile_standardized['mean_profile'] = (false_pulsar_mean_profile_standardized['mean_profile'] - false_pulsar_mean_profile_standardized['mean_profile'].mean()) / false_pulsar_mean_profile_standardized['mean_profile'].std()

    qt1 = sct.norm.ppf(0.8, loc=0, scale=1)
    qt2 = sct.norm.ppf(0.9, loc=0, scale=1)
    qt3 = sct.norm.ppf(0.95, loc=0, scale=1)

    ecdf = ECDF(false_pulsar_mean_profile_standardized["mean_profile"])

    pqt1 = np.around(ecdf(qt1), 3)
    pqt2 = np.around(ecdf(qt2), 3)
    pqt3 = np.around(ecdf(qt3), 3)

    return (pqt1, pqt2, pqt3)


# Para refletir:
# 
# * Os valores encontrados fazem sentido?
# * O que isso pode dizer sobre a distribuição da variável `false_pulsar_mean_profile_standardized`?

# ## Questão 5
# 
# Qual a diferença entre os quantis Q1, Q2 e Q3 de `false_pulsar_mean_profile_standardized` e os mesmos quantis teóricos de uma distribuição normal de média 0 e variância 1? Responda como uma tupla de três elementos arredondados para três casas decimais.

# In[15]:


def q5():
    false_pulsar_mean_profile = stars.loc[stars['target'] == False]

    false_pulsar_mean_profile_standardized = false_pulsar_mean_profile.copy()
    false_pulsar_mean_profile_standardized['mean_profile'] = (false_pulsar_mean_profile_standardized['mean_profile'] - false_pulsar_mean_profile_standardized['mean_profile'].mean()) / false_pulsar_mean_profile_standardized['mean_profile'].std()

    q1 = false_pulsar_mean_profile_standardized['mean_profile'].quantile((0.25))
    q2 = false_pulsar_mean_profile_standardized['mean_profile'].quantile((0.5))
    q3 = false_pulsar_mean_profile_standardized['mean_profile'].quantile((0.75))

    qt1 = sct.norm.ppf(0.25, loc=0, scale=1)
    qt2 = sct.norm.ppf(0.5, loc=0, scale=1)
    qt3 = sct.norm.ppf(0.75, loc=0, scale=1)

    diff1 = np.around((q1 - qt1), 3)
    diff2 = np.around((q2 - qt2), 3)
    diff3 = np.around((q3 - qt3), 3)

    return (diff1, diff2, diff3)


# Para refletir:
# 
# * Os valores encontrados fazem sentido?
# * O que isso pode dizer sobre a distribuição da variável `false_pulsar_mean_profile_standardized`?
# * Curiosidade: alguns testes de hipóteses sobre normalidade dos dados utilizam essa mesma abordagem.

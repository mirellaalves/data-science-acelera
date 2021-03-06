#!/usr/bin/env python
# coding: utf-8

# # Desafio 6
# 
# Neste desafio, vamos praticar _feature engineering_, um dos processos mais importantes e trabalhosos de ML. Utilizaremos o _data set_ [Countries of the world](https://www.kaggle.com/fernandol/countries-of-the-world), que contém dados sobre os 227 países do mundo com informações sobre tamanho da população, área, imigração e setores de produção.
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Setup_ geral

# In[81]:


import pandas as pd
import numpy as np
import seaborn as sns
import sklearn as sk
from sklearn.preprocessing import (
    OneHotEncoder, KBinsDiscretizer, StandardScaler
)
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.feature_extraction.text import (
    CountVectorizer, TfidfVectorizer
)


# In[82]:


# Algumas configurações para o matplotlib.
# %matplotlib inline

# from IPython.core.pylabtools import figsize


# figsize(12, 8)

# sns.set()


# In[83]:


countries = pd.read_csv("countries.csv")


# In[84]:


new_column_names = [
    "Country", "Region", "Population", "Area", "Pop_density", "Coastline_ratio",
    "Net_migration", "Infant_mortality", "GDP", "Literacy", "Phones_per_1000",
    "Arable", "Crops", "Other", "Climate", "Birthrate", "Deathrate", "Agriculture",
    "Industry", "Service"
]

countries.columns = new_column_names

countries.head(5)


# ## Observações
# 
# Esse _data set_ ainda precisa de alguns ajustes iniciais. Primeiro, note que as variáveis numéricas estão usando vírgula como separador decimal e estão codificadas como strings. Corrija isso antes de continuar: transforme essas variáveis em numéricas adequadamente.
# 
# Além disso, as variáveis `Country` e `Region` possuem espaços a mais no começo e no final da string. Você pode utilizar o método `str.strip()` para remover esses espaços.

# ## Inicia sua análise a partir daqui

# In[85]:


# substitui vírgula por ponto
countries['Pop_density'] = countries['Pop_density'].str.replace(',', '.')
countries['Coastline_ratio'] = countries['Coastline_ratio'].str.replace(',', '.')
countries['Net_migration'] = countries['Net_migration'].str.replace(',', '.')
countries['Infant_mortality'] = countries['Infant_mortality'].str.replace(',', '.')
countries['Literacy'] = countries['Literacy'].str.replace(',', '.')
countries['Phones_per_1000'] = countries['Phones_per_1000'].str.replace(',', '.')
countries['Arable'] = countries['Arable'].str.replace(',', '.')
countries['Crops'] = countries['Crops'].str.replace(',', '.')
countries['Other'] = countries['Other'].str.replace(',', '.')
countries['Climate'] = countries['Climate'].str.replace(',', '.')
countries['Birthrate'] = countries['Birthrate'].str.replace(',', '.')
countries['Deathrate'] = countries['Deathrate'].str.replace(',', '.')
countries['Agriculture'] = countries['Agriculture'].str.replace(',', '.')
countries['Industry'] = countries['Industry'].str.replace(',', '.')
countries['Service'] = countries['Service'].str.replace(',', '.')


# In[86]:


#converte string em float
countries['Pop_density'] = countries['Pop_density'].astype(float, errors = 'raise')
countries['Coastline_ratio'] = countries['Coastline_ratio'].astype(float, errors = 'raise')
countries['Net_migration'] = countries['Net_migration'].astype(float, errors = 'raise')
countries['Infant_mortality'] = countries['Infant_mortality'].astype(float, errors = 'raise')
countries['Literacy'] = countries['Literacy'].astype(float, errors = 'raise')
countries['Phones_per_1000'] = countries['Phones_per_1000'].astype(float, errors = 'raise')
countries['Arable'] = countries['Arable'].astype(float, errors = 'raise')
countries['Crops'] = countries['Crops'].astype(float, errors = 'raise')
countries['Other'] = countries['Other'].astype(float, errors = 'raise')
countries['Climate'] = countries['Climate'].astype(float, errors = 'raise')
countries['Birthrate'] = countries['Birthrate'].astype(float, errors = 'raise')
countries['Deathrate'] = countries['Deathrate'].astype(float, errors = 'raise')
countries['Agriculture'] = countries['Agriculture'].astype(float, errors = 'raise')
countries['Industry'] = countries['Industry'].astype(float, errors = 'raise')
countries['Service'] = countries['Service'].astype(float, errors = 'raise')


# In[87]:


# verifica novos tipos de dados
countries.dtypes


# ## Questão 1
# 
# Quais são as regiões (variável `Region`) presentes no _data set_? Retorne uma lista com as regiões únicas do _data set_ com os espaços à frente e atrás da string removidos (mas mantenha pontuação: ponto, hífen etc) e ordenadas em ordem alfabética.

# In[88]:


def q1():
    countries['Region'] = countries['Region'].apply(lambda x: x.strip())
    get_regions = countries['Region'].sort_values()
    return list(get_regions.unique())

print(q1())


# ## Questão 2
# 
# Discretizando a variável `Pop_density` em 10 intervalos com `KBinsDiscretizer`, seguindo o encode `ordinal` e estratégia `quantile`, quantos países se encontram acima do 90º percentil? Responda como um único escalar inteiro.

# In[89]:


def q2():
    discretizer = KBinsDiscretizer(n_bins=10, encode="ordinal", strategy="quantile")
    discretizer.fit(countries[["Pop_density"]])
    var_bins = discretizer.transform(countries[["Pop_density"]])
    return int(sum(var_bins >= 9))

print(q2())


# # Questão 3
# 
# Se codificarmos as variáveis `Region` e `Climate` usando _one-hot encoding_, quantos novos atributos seriam criados? Responda como um único escalar.

# In[90]:


def q3():
    one_hot_encoder = OneHotEncoder(sparse=False, dtype=int)
    features_encoded = one_hot_encoder.fit_transform(countries[["Region", "Climate"]])
    return features_encoded.shape[1]

print(q3())


# ## Questão 4
# 
# Aplique o seguinte _pipeline_:
# 
# 1. Preencha as variáveis do tipo `int64` e `float64` com suas respectivas medianas.
# 2. Padronize essas variáveis.
# 
# Após aplicado o _pipeline_ descrito acima aos dados (somente nas variáveis dos tipos especificados), aplique o mesmo _pipeline_ (ou `ColumnTransformer`) ao dado abaixo. Qual o valor da variável `Arable` após o _pipeline_? Responda como um único float arredondado para três casas decimais.

# In[91]:


test_country = [
    'Test Country', 'NEAR EAST', -0.19032480757326514,
    -0.3232636124824411, -0.04421734470810142, -0.27528113360605316,
    0.13255850810281325, -0.8054845935643491, 1.0119784924248225,
    0.6189182532646624, 1.0074863283776458, 0.20239896852403538,
    -0.043678728558593366, -0.13929748680369286, 1.3163604645710438,
    -0.3699637766938669, -0.6149300604558857, -0.854369594993175,
    0.263445277972641, 0.5712416961268142
]


# In[92]:


def q4():
    countries_missing = countries.copy()
    num_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("standart_scaler", StandardScaler())
    ])
    countries_missing_num = countries_missing.select_dtypes(include=['float64', 'int64'])
    num_pipeline.fit_transform(countries_missing_num)
    test_transformation = num_pipeline.transform([test_country[2:]])
    arable_transformation = test_transformation[:, countries_missing_num.columns.get_loc("Arable")]
    return round(arable_transformation.item(), 3)

print(q4())


# ## Questão 5
# 
# Descubra o número de _outliers_ da variável `Net_migration` segundo o método do _boxplot_, ou seja, usando a lógica:
# 
# $$x \notin [Q1 - 1.5 \times \text{IQR}, Q3 + 1.5 \times \text{IQR}] \Rightarrow x \text{ é outlier}$$
# 
# que se encontram no grupo inferior e no grupo superior.
# 
# Você deveria remover da análise as observações consideradas _outliers_ segundo esse método? Responda como uma tupla de três elementos `(outliers_abaixo, outliers_acima, removeria?)` ((int, int, bool)).

# In[93]:


def q5():
    net_migration_outlier = countries.Net_migration.copy()

    q1 = net_migration_outlier.quantile(0.25)
    q3 = net_migration_outlier.quantile(0.75)
    iqr = q3 - q1

    non_outlier_interval_iqr = [q1 - 1.5 * iqr, q3 + 1.5 * iqr]

    count_outliers_iqr_down = len(net_migration_outlier[(net_migration_outlier < non_outlier_interval_iqr[0])])
    count_outliers_iqr_up = len(net_migration_outlier[(net_migration_outlier > non_outlier_interval_iqr[1])])
    remove_outliers = bool((count_outliers_iqr_up + count_outliers_iqr_down)/net_migration_outlier.shape[0] < 0.1)

    return (count_outliers_iqr_down, count_outliers_iqr_up, remove_outliers)

print(q5())


# ## Questão 6
# Para as questões 6 e 7 utilize a biblioteca `fetch_20newsgroups` de datasets de test do `sklearn`
# 
# Considere carregar as seguintes categorias e o dataset `newsgroups`:
# 
# ```
# categories = ['sci.electronics', 'comp.graphics', 'rec.motorcycles']
# newsgroup = fetch_20newsgroups(subset="train", categories=categories, shuffle=True, random_state=42)
# ```
# 
# 
# Aplique `CountVectorizer` ao _data set_ `newsgroups` e descubra o número de vezes que a palavra _phone_ aparece no corpus. Responda como um único escalar.

# In[94]:


from sklearn.datasets import fetch_20newsgroups

categories = ['sci.electronics', 'comp.graphics', 'rec.motorcycles']
newsgroup = fetch_20newsgroups(subset="train", categories=categories, shuffle=True, random_state=42)


# In[95]:


def q6():
    count_vectorizer = CountVectorizer()
    newsgroup_counts = count_vectorizer.fit_transform(newsgroup.data)

    return int((newsgroup_counts[:, count_vectorizer.vocabulary_['phone']]).sum())

print(q6())


# ## Questão 7
# 
# Aplique `TfidfVectorizer` ao _data set_ `newsgroups` e descubra o TF-IDF da palavra _phone_. Responda como um único escalar arredondado para três casas decimais.

# In[96]:


def q7():
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer.fit(newsgroup.data)
    newsgroup_tfidf_vectorized = tfidf_vectorizer.transform(newsgroup.data)

    return float(np.round((newsgroup_tfidf_vectorized[:, tfidf_vectorizer.vocabulary_['phone']]).sum(), 3))

print(q7())


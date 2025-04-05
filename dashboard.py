# bibliotecas necessárias para dashboard
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import scipy.stats as stats

# página web para exibição 
st.set_page_config(layout="wide")

# cabeçalho
st.header("Análise de Dados Sobre Adoção de Pets")
st.sidebar.text("Andréa/Andriele/Jalisson")

# Carregar os dados
dados = pd.read_csv('pet_adoption_data (1).csv')
dados.head()

#calcular
quantidade_pet = dados["Pet"].value_counts().reset_index()
quantidade_porte = dados["Porte"].value_counts().reset_index()
quantidade_vacinado = dados["Vacinado"].value_counts().reset_index()
quantidade_taxa = dados["Taxa de adoção (Dólar)"].value_counts().reset_index()
tempo_abrigo = dados["Tempo no abrigo"].value_counts().reset_index()

# Definir a ordem correta dos portes
ordem_porte = ["Pequeno", "Médio", "Grande"]
quantidade_porte["Porte"] = pd.Categorical(quantidade_porte["Porte"], categories=ordem_porte, ordered=True)

# Reordenar os dados pela categoria definida
quantidade_porte = quantidade_porte.sort_values("Porte")

# Renomear as colunas
quantidade_pet.columns = ["Pet", "Quantidade"]
quantidade_porte.columns = ["Porte", "Quantidade"]
quantidade_vacinado.columns = ["Vacinado", "Quantidade"]
quantidade_taxa.columns = ["Taxa de adoção (Dólar)" , "Quantidade"]

# Calcular a frequência relativa (%) e adicionar à tabela
quantidade_pet["Frequência (%)"] = ((quantidade_pet["Quantidade"] / quantidade_pet["Quantidade"].sum()) * 100).round(2)
quantidade_porte["Frequência (%)"] = ((quantidade_porte["Quantidade"] / quantidade_porte["Quantidade"].sum()) * 100).round(2)
quantidade_vacinado["Frequência (%)"] = ((quantidade_vacinado["Quantidade"] / quantidade_vacinado["Quantidade"].sum()) * 100).round(2)
quantidade_taxa["Frequência (%)"] = ((quantidade_taxa["Quantidade"] / quantidade_taxa["Quantidade"].sum()) * 100).round(2)

# Definir os intervalos (bins) de 2 em 2
tempo_abrigo = dados["Tempo no abrigo"]

# Calcular a amplitude (Xmax - Xmin)
x_max = tempo_abrigo.max()
x_min = tempo_abrigo.min()
amplitude = x_max - x_min
bins = np.arange(tempo_abrigo.min(), tempo_abrigo.max() + 2, 2)

# Contar os elementos em cada intervalo
contagem, bin_edges = np.histogram(tempo_abrigo, bins=bins)

# Calcular a frequência relativa (%)
total = tempo_abrigo.count()
frequencia_percentual = (contagem / total) * 100

# Criar DataFrame com os resultados
dados_histograma = pd.DataFrame({
    "Intervalo (dias)": [f"{int(bin_edges[i])} - {int(bin_edges[i+1])}" for i in range(len(bin_edges)-1)],
    "Frequência Absoluta": contagem,
    "Frequência Relativa (%)": frequencia_percentual.round(2)
})

# Exibir os dados
st.sidebar.title("Dados Gerais")

opção = st.sidebar.radio("Clique na opção desejada",
                         ["Quantidade de Pet", "Tempo no Abrigo",
                           "Porte", "Pets Vacinados",
                            "Taxa de Adoção"])

if (opção == "Quantidade de Pet"):
    st.plotly_chart(px.bar(quantidade_pet, "Pet", "Quantidade", title="Quantidade de cada Pet"))   
   
elif (opção == "Tempo no Abrigo"):   
    st.plotly_chart(px.bar(dados_histograma, "Intervalo (dias)", "Frequência Absoluta", title="Tempo no Abrigo"))
   
elif (opção == "Pets Vacinados"): 
    st.plotly_chart(px.pie(quantidade_vacinado, "Vacinado", "Quantidade", title="Vacinados", labels={"Vacinado":"Sim"}))

elif (opção == "Taxa de Adoção"):   
    st.plotly_chart(px.bar(dados, "Pet", "Taxa de adoção (Dólar)", title="Taxa de Adoção"))
   
elif (opção == "Porte"):   
    st.plotly_chart(px.bar(quantidade_porte, "Porte", "Quantidade", title="Porte dos Pets"))

# Média, Moda, Mediana, Quartis, Mínimo, Máximo e Desvio Padrão 
st.sidebar.title("Estatísticas Gerais")
estatistica = st.sidebar.selectbox("Escolha uma opção", ["Idade", "Peso", "Tempo no Abrigo", "Taxa de Adoção"])
                                    
idade = dados["Idade (meses)"].describe()
peso = dados["Peso"].describe()
tempo_abrigo = dados["Tempo no abrigo"].describe()
taxa_adocao = dados["Taxa de adoção (Dólar)"].describe()

# Teste de normalidade por coluna
static, pvalue = stats.shapiro(dados["Idade (meses)"])
normalidade = "Segue distribuição normal ✅" if pvalue < 0.05 else "Não segue distribuição normal ❌"

static, pvalue = stats.shapiro(dados["Peso"])
normalidade = "Segue distribuição normal ✅" if pvalue < 0.05 else "Não segue distribuição normal ❌"

static, pvalue = stats.shapiro(dados["Tempo no abrigo"])
normalidade = "Segue distribuição normal ✅" if pvalue < 0.05 else "Não segue distribuição normal ❌"

static, pvalue = stats.shapiro(dados["Taxa de adoção (Dólar)"])
normalidade = "Segue distribuição normal ✅" if pvalue < 0.05 else "Não segue distribuição normal ❌"
   
if (estatistica == "Idade"):
    st.text("\nDescrição da Idade dos Pets em meses:")
    st.table(idade)
    st.text(f"Teste de Shapiro-Wilk: {normalidade}")
    skewness = stats.skew(dados["Idade (meses)"])
    kurt = stats.kurtosis(dados["Idade (meses)"])
    st.text(f"📊 Assimetria (Skewness) = {skewness}\n")
    st.text(f"📈 Curtose (Kurtosis) = {kurt}\n")

elif (estatistica == "Peso"):
    st.text("\nDescrição do Peso dos Pets:")
    st.table(peso)
    st.text(f"Teste de Shapiro-Wilk: {normalidade}")
    skewness = stats.skew(dados["Peso"])
    kurt = stats.kurtosis(dados["Peso"])
    st.text(f"📊 Assimetria (Skewness) = {skewness}\n")
    st.text(f"📈 Curtose (Kurtosis) = {kurt}\n")

elif (estatistica == "Tempo no Abrigo"):
    st.text("\nDescrição do Tempo dos Pets no Abrigo em dias:")
    st.table(tempo_abrigo)
    st.text(f"Teste de Shapiro-Wilk: {normalidade}")
    skewness = stats.skew(dados["Tempo no abrigo"])
    kurt = stats.kurtosis(dados["Tempo no abrigo"])
    st.text(f"📊 Assimetria (Skewness) = {skewness}\n")
    st.text(f"📈 Curtose (Kurtosis) = {kurt}\n")

elif (estatistica == "Taxa de Adoção"):
    st.text("\nDescrição da Taxa de Adoção dos Pets:")
    st.table(taxa_adocao)
    skewness = stats.skew(dados["Taxa de adoção (Dólar)"])
    kurt = stats.kurtosis(dados["Taxa de adoção (Dólar)"])
    st.text(f"Teste de Shapiro-Wilk: {normalidade}")
    st.text(f"📊 Assimetria (Skewness) = {skewness}\n")
    st.text(f"📈 Curtose (Kurtosis) = {kurt}\n")

# Solicitar ao usuário o tipo de pet para filtrar
st.sidebar.title("Estatísticas por Pet")

pet_desejado = st.sidebar.text_input("Digite o tipo de pet para análise: Cachorro 🐶 / Gato 🐈 \nCoelho 🐇 / Pássaro 🐦").strip()

# Filtrar os dados pelo tipo de pet escolhido
dados_filtrados = dados[dados["Pet"] == pet_desejado]

# Verificar se há registros para esse pet
if dados_filtrados.empty:
    st.text(f"Nenhum dado encontrado para '{pet_desejado}'. Verifique o nome e tente novamente.")
else:
    st.title(f"\n🐾 Estatísticas para {pet_desejado}:\n")

# Escolher por Pet
coluna = st.sidebar.selectbox("Escolha uma opção", ["Idade (meses)", "Peso", "Tempo no abrigo", "Taxa de adoção (Dólar)"])       

id_pet = (dados_filtrados[coluna]).describe()
peso_pet = (dados_filtrados[coluna]).describe()
tempo_pet = (dados_filtrados[coluna]).describe()
taxa_pet = (dados_filtrados[coluna]).describe()

skewness = stats.skew(dados_filtrados[coluna])
kurt = stats.kurtosis(dados_filtrados[coluna])

if len(dados_filtrados[coluna]) >= 3:
    static, pvalue = stats.shapiro(dados_filtrados[coluna])
    
else:
    st.text("Não há dados suficientes para realizar o teste de normalidade.")

if coluna == "Idade (meses)":
    st.table(id_pet)
    st.text(f"📌 Teste de normalidade =  {normalidade}\n")
    st.text(f"📊 Assimetria (Skewness) = {skewness}\n")
    st.text(f"📈 Curtose (Kurtosis) = {kurt}\n")

elif coluna == "Peso":  
    st.table(peso_pet)
    st.text(f"📌 Teste de normalidade =  {normalidade}\n")
    st.text(f"📊 Assimetria (Skewness) = {skewness}\n")
    st.text(f"📈 Curtose (Kurtosis) = {kurt}\n")
            
elif coluna == "Tempo no abrigo":
    st.table(tempo_pet)  
    st.text(f"📌 Teste de normalidade =  {normalidade}\n")
    st.text(f"📊 Assimetria (Skewness) = {skewness}\n")
    st.text(f"📈 Curtose (Kurtosis) = {kurt}\n") 

elif coluna == "Taxa de adoção (Dólar)":    
    st.table(taxa_pet)
    st.text(f"📌 Teste de normalidade =  {normalidade}\n")
    st.text(f"📊 Assimetria (Skewness) = {skewness}\n")
    st.text(f"📈 Curtose (Kurtosis) = {kurt}\n")

else:                
    st.text(f" ❌ Erro ao calcular {coluna}. Escolha uma opção válida.")    

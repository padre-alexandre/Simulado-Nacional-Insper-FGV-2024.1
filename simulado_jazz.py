##### Relatório Simulado Nacional Insper - Jazz Vestibular

##### Base de Dados

### Nome da Avaliação
### Turma
### Nome do aluno (a)
### Login do aluno (a)
### Disciplina
### Frente
### Assunto
### Número da questão
### Alternativa assinalada pelo aluno (a)
### Gabarito
### Certo ou Errado
### Tempo gasto
### Valor da questão

### Importação de bibliotecas

#from pickle import FALSE
#from tkinter import E
from cmath import sqrt
import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from funcoes import *
from matplotlib import pyplot as plt
from load_css_nova_id import local_css
from datetime import datetime


### Configurando a página

st.set_page_config(page_title="Relatório", page_icon="", layout="wide")
st.markdown('<style>body{background-color: #9E089E}</style>',unsafe_allow_html=True)

local_css("style_nova_id.css")

### Lista de cores e fontes

# Cor de fundo dos retângulos: #9E089E
# Cor de fundo da página: #FFF0FC
# Cor da fonte dos títulos: #9E089E
# Cor da fonte dos texto: #C81F6D e #9E089E
# Fonte: Arial

######################### Banco de Dados ########################
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Banco de Dados - Relatório Simulado Nacional').sheet1          # Enquanto estiver rodando na nuvem
#sheet = client.open('Banco de Dados - Relatório Simulado Nacional - Teste').sheet1   # Enquanto estiver rodando no local

#### Colunas (id, Data e Hora, Nome, Rede, Grupo, Gestor, Produto, Faixa de licenças, Namespace, NPS, Feedback)
row0 = ['Data e Hora', 'Turma','Nome','Login']

#banco_de_dados = sheet.get_all_records()
#banco_de_dados2 = pd.DataFrame(banco_de_dados)

### Cabeçalho principal

html_header="""
<head>
<title>Relatório</title>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<meta charset="utf-8">
<meta name="keywords" content="relatorio diagnostico, simulado nacional, insper">
<meta name="description" content="relatorio diagnostico simulado">
<meta name="author" content="Alexandre Fernandes">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<h1 style="font-size:300%; color: #9E089E; font-family:Georgia"> SIMULADO NACIONAL INSPER<br>
 <h2 style="color: #9E089E; font-family:Georgia">RELATÓRIO</h3> <br>
 <hr style= "  display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;"></h1>
"""

html_card_instagram="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #c5ffff; padding-top: 12px; width: 280px;
       height: 50px;">
        <p class="card-title" style="background-color:#c5ffff; color:#008181; font-family:Georgia; text-align: center; padding: 0px 0;">Instagram: @jazz_vestibular</p>
      </div>
    </div>
    """
html_card_whatsapp="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 280px;
       height: 50px;">
        <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size:16px; font-family:Georgia; text-align: center; padding: 0px 0;">Whatsapp: (32) 99802-5088</p>
      </div>
    </div>
    """
html_br="""
    <br>
    """

with st.container():
        col1, col2, col3 = st.columns([3,4,3])
        with col1:
            st.markdown(html_br, unsafe_allow_html=True)
        with col2:
            st.image('[LOGO 3] Jazz.png')
        with col3:
            st.markdown(html_br, unsafe_allow_html=True)

with st.container():
        col1, col2, col3, col4= st.columns([5, 5, 5, 5])
        with col1:
            st.markdown(html_br, unsafe_allow_html=True)
        with col2:
            st.markdown(html_card_instagram, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.write("##### [Clique aqui para ver nossa página](https://www.instagram.com/jazz_vestibular/)")
        with col3:
            st.markdown(html_card_whatsapp, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.write("##### [Clique aqui para falar conosco](https://api.whatsapp.com/send?phone=55032998025088)")
        with col4:
            st.markdown(html_br, unsafe_allow_html=True)

st.markdown(html_header, unsafe_allow_html=True)

### Leitura das bases de dados

base_matriz = pd.read_csv('./matrizquestoes.csv')

base_resultados = pd.read_csv('./resultado1fase.csv')
base_resultados_2fase = pd.read_csv('./resultado2fase.csv')
#base_resultados_2fase = pd.read_csv('./Jazz Vestibular - 2022.2 - Operacao - [RELATORIO] Base de Dados 2 fase copy.csv')

#base_resultados_2fase = pd.read_csv('./Jazz Vestibular - 2022.2 - Operacao - [RELATORIO] Base de Dados 2 fase copy.csv')

### Turmas

turma_eng = 'Simulado Nacional Insper 2023.2 - Engenharia'
turma_cien = 'Simulado Nacional Insper 2023.2 - Ciência da Computação'
turma_adm = 'Simulado Nacional Insper 2023.2 - Administração'
turma_eco = 'Simulado Nacional Insper 2023.2 - Economia'
turma_dir = 'Simulado Nacional Insper 2023.2 - Direito'

### Renomeando colunas e ajustando células vazias

for i in range(len(base_resultados['atividade_nome'])):
    if (base_resultados['turma'][i] == turma_eng or base_resultados['turma'][i] == turma_cien):
        if base_resultados['num_exercicio'][i] != 73:
            base_resultados['num_exercicio'][i] = base_resultados['num_exercicio'][i] + 24


base = pd.merge(base_resultados, base_matriz, on = 'num_exercicio', how = 'inner')

base.rename(columns = {'atividade_nome':'Nome da avaliação','turma':'Turma','aluno_nome':'Nome do aluno(a)','aluno_login':'Login do aluno(a)','num_exercicio':'Número da questão','resp_aluno':'Resposta do aluno(a)','gabarito':'Gabarito','certo_ou_errado':'Certo ou errado','tempo_no_exercicio(s)':'Tempo na questão','valor_do_exercicio':'Valor da questão','disciplina':'Disciplina','frente':'Frente','assunto':'Assunto'}, inplace = True)
base['Resposta do aluno(a)'] = base['Resposta do aluno(a)'].fillna('x')
base['Tempo na questão'] = base['Tempo na questão'].fillna(0)
base['Valor da questão'] = base['Valor da questão'].apply(lambda x: float(x.replace(".","").replace(",",".")))

### Resultados Gerais

base['Acerto'] = 0.00
base['Nota na questão'] = 0.00

for i in range(len(base['Nome da avaliação'])):
    if base['Certo ou errado'][i] == 'certo':
        base['Acerto'][i] = 1
        base['Nota na questão'][i] = base['Acerto'][i]*base['Valor da questão'][i]
    #if base['Número da questão'][i] == 73 and base['Resposta do aluno(a)'][i] != 'x':
    #    base['Acerto'][i] = float(base['Resposta do aluno(a)'][i])/base['Valor da questão'][i]
    #    base['Nota na questão'][i] = base['Acerto'][i]*base['Valor da questão'][i]

resultados_gerais = base.groupby(['Nome da avaliação','Turma','Nome do aluno(a)','Login do aluno(a)']).sum().reset_index()

#for i in range(len(resultados_gerais['Nome do aluno(a)'])):
#    if (resultados_gerais['Turma'][i] == turma_eng or resultados_gerais['Turma'][i] == turma_cien) and resultados_gerais['Nome da avaliação'][i] == 'Simulado Nacional Insper 1º fase - Matemática e Linguagens':
#        resultados_gerais['Nota na questão'][i] = (1/3)*resultados_gerais['Nota na questão'][i]
#    elif resultados_gerais['Turma'][i] == 'Simulado Nacional - Ciências da Computação' and resultados_gerais['Nome da avaliação'][i] == 'Simulado Nacional Insper 1º fase - Matemática e Linguagens':
#        resultados_gerais['Nota na questão'][i] = (1/3)*resultados_gerais['Nota na questão'][i]
#    elif  resultados_gerais['Nome da avaliação'][i] == 'Simulado Nacional Insper 1º fase - Matemática e Linguagens':
#        resultados_gerais['Nota na questão'][i] = (750/2000)*resultados_gerais['Nota na questão'][i]
#    
#    if resultados_gerais['Nome da avaliação'][i] == 'Simulado Nacional Insper 1º fase - Ciências Humanas':
#        resultados_gerais['Nota na questão'][i] = (250/1000)*resultados_gerais['Nota na questão'][i]
#
#    if resultados_gerais['Nome da avaliação'][i] == 'Simulado Nacional Insper 1º fase - Ciências da Natureza':
#        resultados_gerais['Nota na questão'][i] = (1/3)*resultados_gerais['Nota na questão'][i]
    
resultados_gerais2 = resultados_gerais.groupby(['Turma','Nome do aluno(a)','Login do aluno(a)']).sum().reset_index()
resultados_gerais2_aux = resultados_gerais2.copy()
for i in range(len(resultados_gerais2_aux['Login do aluno(a)'])):
    if (resultados_gerais2_aux['Turma'][i] == turma_eng or resultados_gerais2_aux['Turma'][i] == turma_cien):
        resultados_gerais2_aux['Nota na questão'][i] = (6/5)*resultados_gerais2_aux['Nota na questão'][i]
    else:
        resultados_gerais2_aux['Nota na questão'][i] = 1.25*resultados_gerais2_aux['Nota na questão'][i]


#resultados_gerais2 = resultados_gerais.drop(columns = ['Número da questão'])
resultados_gerais3 = resultados_gerais2_aux.sort_values(by = 'Nota na questão', ascending = False).reset_index(drop = True)                

### Selecionar o aluno
login_aluno = st.text_input('Digite o seu login', '')


#nome_aluno = resultados_gerais3.sort_values(by = 'Nome do aluno(a)')
#nome_aluno2 = inserir_linha(pd.DataFrame(data = nome_aluno['Nome do aluno(a)'].unique()),pd.DataFrame({0: 'Nome'}, index=[-1]))
#nome_aluno3 = str(st.selectbox('Selecione o aluno(a)',nome_aluno2[0]))

if len(login_aluno) > 0:
    nome_aluno3 = resultados_gerais3[resultados_gerais3['Login do aluno(a)'] == login_aluno]['Nome do aluno(a)'].reset_index()
    turma_aluno = resultados_gerais3[resultados_gerais3['Login do aluno(a)'] == login_aluno]['Turma'].reset_index() 
    row = [str(datetime.today()),turma_aluno['Turma'][0],nome_aluno3['Nome do aluno(a)'][0],login_aluno]
    index = 2
    sheet.insert_row(row, index)


    html_br="""
    <br>
    """
    html_download_pdfs="""
    <h2 style="font-size:200%; color: #9E089E; font-family:Georgia">PDF DO SIMULADO<br>
     <hr style= "  display: block;
      margin-top: 0.5em;
      margin-bottom: 0.5em;
      margin-left: auto;
      margin-right: auto;
      border-style: inset;
      border-width: 1.5px;"></h2>
    """
    st.markdown(html_download_pdfs, unsafe_allow_html=True)
    if turma_aluno['Turma'][0] == turma_eng or turma_aluno['Turma'][0] == turma_cien:
        st.markdown(get_binary_file_downloader_html('Simulado Nacional Insper 1ª fase - Engenharias e Ciências da Computação.pdf', 'Simulado Nacional Insper 1º fase'), unsafe_allow_html=True)
    else:
        st.markdown(get_binary_file_downloader_html('Simulado Nacional Insper 1ª fase - Administração, Economia e Direito.pdf', 'Simulado Nacional Insper 1º fase'), unsafe_allow_html=True)
    html_br="""
    <br>
    """
if login_aluno != '':
    resultados_gerais3.to_csv('resultado_compilado.csv')
    resultados_gerais_aluno = resultados_gerais3[resultados_gerais3['Nome do aluno(a)'] == nome_aluno3['Nome do aluno(a)'][0]].reset_index()
    resultados_gerais_aluno.rename(columns = {'index':'Classificação'}, inplace = True)
    resultados_gerais_aluno['Classificação'][0] = resultados_gerais_aluno['Classificação'][0] + 1
    
    
    resultados_gerais4 = resultados_gerais3[resultados_gerais3['Nota na questão'] > 0]
    resultados_gerais4_aux = resultados_gerais4[['Login do aluno(a)','Número da questão','Tempo na questão','Valor da questão','Unnamed: 10','Acerto','Nota na questão']]
    resultados_gerais5 = resultados_gerais4_aux.copy()
    #resultados_gerais5 = resultados_gerais4.groupby('Login do aluno(a)').mean().reset_index()

    alunos_fizeram = pd.DataFrame()
    alunos_fizeram['Nome do aluno(a)'] = resultados_gerais4['Nome do aluno(a)']

    ### Resultados gerais do aluno

    numero_candidatos = len(resultados_gerais4['Nome do aluno(a)'])
    aux = resultados_gerais4[resultados_gerais4['Turma'] == turma_eng]
    aux2 = resultados_gerais4[resultados_gerais4['Turma'] == turma_cien]
    numero_eng_cien = len(aux['Nome do aluno(a)']) + len(aux2['Nome do aluno(a)'])

    html_header_geral="""
    <h2 style="font-size:200%; color: #9E089E; font-family:Georgia"> 1º FASE<br>
     <hr style= "  display: block;
      margin-top: 0.5em;
      margin-bottom: 0.5em;
      margin-left: auto;
      margin-right: auto;
      border-style: inset;
      border-width: 1.5px;"></h2>
    """
    st.markdown(html_header_geral, unsafe_allow_html=True)

    html_card_header1="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota</h4>
      </div>
    </div>
    """
    html_card_footer1="""
    <div class="card">
      <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota máxima: 1000</p>
      </div>
    </div>
    """

    html_card_footer_med1="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(int(round(resultados_gerais5['Nota na questão'].mean(),0)))+"""</p>
      </div>
    </div>
    """

    html_card_header2="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Número de acertos</h4>
      </div>
    </div>
    """
    html_card_footer2="""
    <div class="card">
      <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Total de questões: 72</p>
      </div>
    </div>
    """
    html_card_footer_med2="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(int(round(resultados_gerais5['Acerto'].mean(),1)))+"""</p>
      </div>
    </div>
    """
    html_card_header3="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Classificação</h4>
      </div>
    </div>
    """
    html_card_footer3="""
    <div class="card">
      <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos)+"""</p>
      </div>
    </div>
    """
    
    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,20,1,20,1,20,1])
        with col1:
            st.write("")
        with col2:
            st.markdown(html_card_header1, unsafe_allow_html=True)
            fig_c1 = go.Figure(go.Indicator(
                mode="number+delta",
                value=round(resultados_gerais_aluno['Nota na questão'][0],1),
                number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais5['Nota na questão'].mean(),-1),0)), 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c1.update_layout(autosize=False,
                                 width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c1.update_traces(delta_decreasing_color="#FF4136",
                                delta_increasing_color="#3D9970",
                                delta_valueformat='.0f',
                                selector=dict(type='indicator'))
            st.plotly_chart(fig_c1)
            st.markdown(html_card_footer1, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_card_footer_med1, unsafe_allow_html=True)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_card_header2, unsafe_allow_html=True)
            fig_c2 = go.Figure(go.Indicator(
                mode="number+delta",
                value=round(truncar(resultados_gerais_aluno['Acerto'][0],0),0),
                number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': int(round(resultados_gerais5['Acerto'].mean(),0))},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c2.update_layout(autosize=False,
                                 width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c2.update_traces(delta_decreasing_color="#FF4136",
                                 delta_increasing_color="#3D9970",
                                 delta_valueformat='f',
                                 selector=dict(type='indicator'))
            st.plotly_chart(fig_c2)
            st.markdown(html_card_footer2, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_card_footer_med2, unsafe_allow_html=True)
        with col5:
            st.write("")
        with col6:
            st.markdown(html_card_header3, unsafe_allow_html=True)
            fig_c3 = go.Figure(go.Indicator(
                mode="number",
                value=resultados_gerais_aluno['Classificação'][0],
                number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': 1, 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c3.update_layout(autosize=False,
                                 width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                 delta_increasing_color="#FF4136",
                                 delta_valueformat='.3f',
                                 selector=dict(type='indicator'))
            st.plotly_chart(fig_c3)
            st.markdown(html_card_footer3, unsafe_allow_html=True)
        with col7:
            st.write("")
    
    st.markdown(html_br, unsafe_allow_html=True)
    st.markdown(html_br, unsafe_allow_html=True)

    ponto = str(round(100*(numero_candidatos-(resultados_gerais_aluno['Classificação'][0]-1))/numero_candidatos,0)).find('.')
    texto = str(round(100*(numero_candidatos-(resultados_gerais_aluno['Classificação'][0]-1))/numero_candidatos,0))[0:ponto]
    html_card_header_destaques_gerais="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
       height: 150px;">
        <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
      </div>
    </div>
    """    
    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([9,25,2,25,4])
        with col1:
            st.write("")
        with col2:
            # create the bins
            counts, bins = np.histogram(resultados_gerais4['Nota na questão'], bins=range(0, 1100, 100))
            bins = 0.5 * (bins[:-1] + bins[1:])
            fig = px.bar(x=bins, y=counts, labels={'x':'Nota no simulado', 'y':'Número de alunos'})
            fig.update_layout(title={'text': "Distribuição de notas", 'x': 0.5}, paper_bgcolor="#FFF0FC", 
                           plot_bgcolor="#FFF0FC", font={'color': "#9E089E", 'size': 14, 'family': "Georgia"}, height=400,
                           width=540,
                           legend=dict(orientation="h",
                                       yanchor="top",
                                       y=0.99,
                                       xanchor="left",
                                       x=0.01),
                           margin=dict(l=1, r=1, b=1, t=30))
            fig.add_vline(x=int(round(resultados_gerais_aluno['Nota na questão'][0],1)), line_width=7, line_dash="dash", line_color="#9E089E", annotation_text="Você está aqui!", annotation_position="top right")
            fig.add_vline(x=int(round(truncar(resultados_gerais5['Nota na questão'].mean(),-1),0)), line_width=7, line_dash="dash", line_color="#01ECEC", annotation_text="Média", annotation_position="top right")
            fig.update_xaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=6, rangemode="tozero",
                          showgrid=False, gridwidth=0.5, gridcolor='#f6f6f6')
            fig.update_yaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=10, rangemode="tozero",
                          showgrid=True, gridwidth=0.5, gridcolor='#f6f6f6')
            fig.update_traces(marker_color='#0010B3')
            st.plotly_chart(fig)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            if resultados_gerais_aluno['Classificação'][0] <= numero_candidatos:
                st.markdown(html_card_header_destaques_gerais, unsafe_allow_html=True)
        with col5:
            st.write("")

    #### Resultados gerais por disciplina
    
    base_alunos_fizeram = base[base['Nome do aluno(a)'].isin(alunos_fizeram['Nome do aluno(a)'])].reset_index(drop = True)

    base_alunos_fizeram_aux = base_alunos_fizeram.drop(columns = ['Nome da avaliação','Resposta do aluno(a)','Gabarito','Certo ou errado','Assunto'])

    resultados_gerais_disciplina = base_alunos_fizeram_aux.groupby(['Turma','Login do aluno(a)','Nome do aluno(a)','Disciplina']).sum().reset_index()
    
    resultados_gerais_disciplina2 = resultados_gerais_disciplina.drop(columns = ['Número da questão'])

    resultados_gerais_disciplina3 = resultados_gerais_disciplina2.sort_values(by = 'Nota na questão', ascending = False).reset_index(drop = True)
    
    resultados_gerais_disciplina3['Nota na questão'] = 1000*resultados_gerais_disciplina3['Nota na questão']/resultados_gerais_disciplina3['Valor da questão']
    resultados_gerais_disciplina3_aux = resultados_gerais_disciplina3.drop(columns = ['Turma','Login do aluno(a)','Nome do aluno(a)'])

    resultados_gerais_disciplina4 = resultados_gerais_disciplina3_aux.groupby('Disciplina').mean().reset_index()
    resultados_gerais_disciplina5 = resultados_gerais_disciplina4.sort_values(by = 'Disciplina', ascending = False)
    
    ### Resultados do aluno por disciplina
    
    resultados_disciplina_aluno = resultados_gerais_disciplina3[resultados_gerais_disciplina3['Login do aluno(a)'] == login_aluno].reset_index()
    resultados_disciplina_aluno2 = resultados_disciplina_aluno.sort_values(by = 'Disciplina', ascending = False)
    
    resultados_matematica = resultados_disciplina_aluno2[resultados_disciplina_aluno2['Disciplina'] == 'Matemática'].reset_index()
    resultados_linguagens = resultados_disciplina_aluno2[resultados_disciplina_aluno2['Disciplina'] == 'Linguagens'].reset_index()
    resultados_ciencias_hum = resultados_disciplina_aluno2[resultados_disciplina_aluno2['Disciplina'] == 'Ciências Humanas'].reset_index()
    resultados_ciencias_nat = resultados_disciplina_aluno2[resultados_disciplina_aluno2['Disciplina'] == 'Ciências da Natureza'].reset_index()
   
    resultados_gerais_disciplina3_mat = resultados_gerais_disciplina3[resultados_gerais_disciplina3['Disciplina'] == 'Matemática'].reset_index(drop = True).reset_index()
    resultados_gerais_disciplina3_lin = resultados_gerais_disciplina3[resultados_gerais_disciplina3['Disciplina'] == 'Linguagens'].reset_index(drop = True).reset_index()
    resultados_gerais_disciplina3_hum = resultados_gerais_disciplina3[resultados_gerais_disciplina3['Disciplina'] == 'Ciências Humanas'].reset_index(drop = True).reset_index()
    resultados_gerais_disciplina3_nat = resultados_gerais_disciplina3[resultados_gerais_disciplina3['Disciplina'] == 'Ciências da Natureza'].reset_index(drop = True).reset_index()
            
    classificacao_aluno_mat = resultados_gerais_disciplina3_mat[resultados_gerais_disciplina3_mat['Login do aluno(a)'] == login_aluno].reset_index()
    classificacao_aluno_lin = resultados_gerais_disciplina3_lin[resultados_gerais_disciplina3_lin['Login do aluno(a)'] == login_aluno].reset_index()
    classificacao_aluno_hum = resultados_gerais_disciplina3_hum[resultados_gerais_disciplina3_hum['Login do aluno(a)'] == login_aluno].reset_index()
    classificacao_aluno_nat = resultados_gerais_disciplina3_nat[resultados_gerais_disciplina3_nat['Login do aluno(a)'] == login_aluno].reset_index()  

    resultados_gerais_disciplina_med_mat = resultados_gerais_disciplina5[resultados_gerais_disciplina5['Disciplina'] == 'Matemática'].reset_index(drop = True)
    resultados_gerais_disciplina_med_lin = resultados_gerais_disciplina5[resultados_gerais_disciplina5['Disciplina'] == 'Linguagens'].reset_index(drop = True)
    resultados_gerais_disciplina_med_hum = resultados_gerais_disciplina5[resultados_gerais_disciplina5['Disciplina'] == 'Ciências Humanas'].reset_index(drop = True)
    resultados_gerais_disciplina_med_nat = resultados_gerais_disciplina5[resultados_gerais_disciplina5['Disciplina'] == 'Ciências da Natureza'].reset_index(drop = True)
    
    if len(resultados_ciencias_hum['Disciplina']) == 0:
        resultados_ciencias_fim = resultados_ciencias_nat.copy()
        resultados_gerais_disciplina3_fim = resultados_gerais_disciplina3_nat.copy()
        classificacao_aluno_fim = classificacao_aluno_nat.copy()
        resultados_gerais_disciplina_med_cie = resultados_gerais_disciplina_med_nat.copy()
    else:
        resultados_ciencias_fim = resultados_ciencias_hum.copy()
        resultados_gerais_disciplina3_fim = resultados_gerais_disciplina3_hum.copy()
        classificacao_aluno_fim = classificacao_aluno_hum.copy()
        resultados_gerais_disciplina_med_cie = resultados_gerais_disciplina_med_hum.copy()

    html_card_header1_disc="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota</h4>
      </div>
    </div>
    """
    html_card_footer1_disc="""
    <div class="card">
      <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota máxima: 1000</p>
      </div>
    </div>
    """
    html_card_footer1_disc_med_mat="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_mat['Nota na questão'].mean(),-1),0)))+"""</p>
      </div>
    </div>
    """
    html_card_footer1_disc_med_lin="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_lin['Nota na questão'].mean(),-1),0)))+"""</p>
      </div>
    </div>
    """
    if len(resultados_ciencias_hum['Nota na questão'] == 0):
        html_card_footer1_disc_med_cie="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
           height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_hum['Nota na questão'].mean(),-1),0)))+"""</p>
          </div>
        </div>
        """
    else:
        html_card_footer1_disc_med_cie="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
           height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_nat['Nota na questão'].mean(),-1),0)))+"""</p>
          </div>
        </div>
        """
    html_card_header2_disc="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Número de acertos</h4>
      </div>
    </div>
    """
    html_card_footer2_disc="""
    <div class="card">
      <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Total de questões: 24</p>
      </div>
    </div>
    """
    
    html_card_footer2_disc_med_mat="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_mat['Acerto'].mean(),-1),0)))+"""</p>
      </div>
    </div>
    """
    html_card_footer2_disc_med_lin="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_lin['Acerto'].mean(),-1),0)))+"""</p>
      </div>
    </div>
    """

  
    if resultados_gerais_aluno['Turma'][0] != turma_eng and resultados_gerais_aluno['Turma'][0] != turma_cien:
        html_card_footer2_disc_med_cie="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_hum['Acerto'].mean(),-1),0)))+"""</p>
      </div>
    </div>
    """
    else:
        html_card_footer2_disc_med_cie="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_nat['Acerto'].mean(),-1),0)))+"""</p>
      </div>
    </div>
    """  
    html_card_header3_disc="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Classificação</h4>
      </div>
    </div>
    """
    html_card_footer3_disc_matlin="""
        <div class="card">
          <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
           height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos)+"""</p>
          </div>
        </div>
        """
    if resultados_gerais_aluno['Turma'][0] != turma_eng and resultados_gerais_aluno['Turma'][0] != turma_cien:
        html_card_footer3_disc="""
        <div class="card">
          <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
           height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos-numero_eng_cien)+"""</p>
          </div>
        </div>
        """
    else:
        html_card_footer3_disc="""
        <div class="card">
          <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
           height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_eng_cien)+"""</p>
          </div>
        </div>
        """

    matematica_detalhes = base_alunos_fizeram[base_alunos_fizeram['Disciplina'] == 'Matemática']
    matematica_detalhes_media = matematica_detalhes.groupby(['Assunto']).mean(['Acerto']).reset_index()
    
    matematica_aluno = matematica_detalhes[matematica_detalhes['Login do aluno(a)'] == login_aluno]
    
    matematica_aluno_media = matematica_aluno.groupby('Assunto').mean(['Acerto']).reset_index()
    matematica_aluno_media2 = matematica_aluno.groupby('Assunto').count().reset_index()
    matematica_aluno_media3 = pd.DataFrame()
    matematica_aluno_media3['Assunto'] = matematica_aluno_media2['Assunto']
    matematica_aluno_media3['Número da questão'] = matematica_aluno_media2['Número da questão']

    matematica_tabela = pd.merge(matematica_aluno_media,matematica_detalhes_media, on = 'Assunto', how = 'inner')
    matematica_tabela2 = matematica_tabela.drop(columns = ['Número da questão_x','Número da questão_y','Valor da questão_x','Valor da questão_y','Nota na questão_x','Nota na questão_y','Tempo na questão_x','Tempo na questão_y'])
    matematica_tabela2.rename(columns = {'Acerto_x':'Resultado Individual decimal','Acerto_y':'Resultado Geral decimal'}, inplace = True)
    matematica_tabela2['Resultado Geral'] = ''
    matematica_tabela2['Resultado Individual'] = ''
    for i in range(len(matematica_tabela2['Assunto'])):
        matematica_tabela2['Resultado Geral'][i] = "{0:.0%}".format(matematica_tabela2['Resultado Geral decimal'][i])
        matematica_tabela2['Resultado Individual'][i] = "{0:.0%}".format(matematica_tabela2['Resultado Individual decimal'][i])
    matematica_tabela3 = pd.merge(matematica_tabela2,matematica_aluno_media3, on = 'Assunto', how = 'inner')
    matematica_tabela3.rename(columns = {'Número da questão':'Quantidade de questões'}, inplace = True)
    matematica_tabela3 = matematica_tabela3[['Assunto','Quantidade de questões','Resultado Individual', 'Resultado Geral','Resultado Individual decimal', 'Resultado Geral decimal']]
    matematica_tabela3['Status'] = ''
    for i in range(len(matematica_tabela3['Assunto'])):
        if matematica_tabela3['Resultado Individual decimal'][i] == 0:
            matematica_tabela3['Status'][i] = "🔴" 
        elif matematica_tabela3['Resultado Individual decimal'][i] >= matematica_tabela3['Resultado Geral decimal'][i]:
            matematica_tabela3['Status'][i] = "🟢"
        elif matematica_tabela3['Resultado Individual decimal'][i] - matematica_tabela3['Resultado Geral decimal'][i] > - 0.25:
            matematica_tabela3['Status'][i] = "🟡"
        else:
            matematica_tabela3['Status'][i] = "🔴"
    matematica_tabela3['Diferença'] = ''
    for i in range(len(matematica_tabela3['Assunto'])):
        matematica_tabela3['Diferença'][i] = matematica_tabela3['Resultado Individual decimal'][i] - matematica_tabela3['Resultado Geral decimal'][i]
    
    matematica_tabela_ordenado = matematica_tabela3.sort_values(by = 'Diferença')

    matematica_tabela_verde = matematica_tabela_ordenado[matematica_tabela_ordenado['Status'] == '🟢']
    matematica_tabela_verde_ordenado = matematica_tabela_verde.sort_values(by = 'Diferença', ascending = False).reset_index(drop = True)
    
    matematica_tabela_vermelho = matematica_tabela_ordenado[matematica_tabela_ordenado['Status'] == '🔴']
    matematica_tabela_vermelho_ordenado = matematica_tabela_vermelho.sort_values(by = 'Diferença', ascending = True).reset_index(drop = True)

    html_header_mat="""
    <h2 style="font-size:200%; color: #9E089E; font-family:Georgia"> MATEMÁTICA<br>
     <hr style= "  display: block;
      margin-top: 0.5em;
      margin-bottom: 0.5em;
      margin-left: auto;
      margin-right: auto;
      border-style: inset;
      border-width: 1.5px;"></h2>
    """
    if len(resultados_matematica['Nome do aluno(a)']) != 0:

        ### MATEMÁTICA

        st.markdown(html_header_mat, unsafe_allow_html=True)

        ### Block 1#########################################################################################
        with st.container():
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1,20,1,20,1,20,1])
            with col1:
                st.write("")
            with col2:
                st.markdown(html_card_header1_disc, unsafe_allow_html=True)
                fig_c1 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=round(resultados_matematica['Nota na questão'][0],1),
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais_disciplina_med_mat['Nota na questão'][0],-1),0)), 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c1.update_layout(autosize=False,
                                     width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                st.plotly_chart(fig_c1)
                st.markdown(html_card_footer1_disc, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_footer1_disc_med_mat, unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header2_disc, unsafe_allow_html=True)
                fig_c2 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=resultados_matematica['Acerto'][0],
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais_disciplina_med_mat['Acerto'][0],-1),0))},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c2.update_layout(autosize=False,
                                     width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c2.update_traces(delta_decreasing_color="#FF4136",
                                 delta_increasing_color="#3D9970",
                                 delta_valueformat='f',
                                 selector=dict(type='indicator'))
                st.plotly_chart(fig_c2)
                st.markdown(html_card_footer2_disc, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_footer2_disc_med_mat, unsafe_allow_html=True)
            with col5:
                st.write("")
            with col6:
                st.markdown(html_card_header3_disc, unsafe_allow_html=True)
                fig_c3 = go.Figure(go.Indicator(
                    mode="number",
                    value=classificacao_aluno_mat['index'][0]+1,
                    number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': 1, 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c3.update_layout(autosize=False,
                                     width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                     delta_increasing_color="#FF4136",
                                     delta_valueformat='.3f',
                                     selector=dict(type='indicator'))
                st.plotly_chart(fig_c3)
                st.markdown(html_card_footer3_disc_matlin, unsafe_allow_html=True)
            with col7:
                st.write("")
        html_br="""
        <br>
        """
        ponto = str(round(100*(numero_candidatos-(classificacao_aluno_mat['index'][0]))/numero_candidatos,0)).find('.')
        texto = str(round(100*(numero_candidatos-(classificacao_aluno_mat['index'][0]))/numero_candidatos,0))[0:ponto]
        html_card_header_destaques_mat="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
           height: 150px;">
            <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
          </div>
        </div>
        """  

        st.markdown(html_br, unsafe_allow_html=True)
        st.markdown(html_br, unsafe_allow_html=True)

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([9,25,2,25,4])
            with col1:
                st.write("")
            with col2:
               # create the bins
                counts, bins = np.histogram(resultados_gerais_disciplina3_mat['Nota na questão'], bins=range(0, 1100, 100))
                bins = 0.5 * (bins[:-1] + bins[1:])
                fig = px.bar(x=bins, y=counts, labels={'x':'Nota no simulado', 'y':'Número de alunos'})
                fig.update_layout(title={'text': "Distribuição de notas", 'x': 0.5}, paper_bgcolor="#FFF0FC", 
                               plot_bgcolor="#FFF0FC", font={'color': "#9E089E", 'size': 14, 'family': "Georgia"}, height=400,
                               width=540,
                               legend=dict(orientation="h",
                                           yanchor="top",
                                           y=0.99,
                                           xanchor="left",
                                           x=0.01),
                               margin=dict(l=1, r=1, b=1, t=30))
                fig.add_vline(x=int(resultados_matematica['Nota na questão']), line_width=7, line_dash="dash", line_color="#9E089E", annotation_text="Você está aqui!", annotation_position="top right")
                fig.add_vline(x=int(round(truncar(resultados_gerais_disciplina_med_mat['Nota na questão'][0],-1),0)), line_width=7, line_dash="dash", line_color="#01ECEC", annotation_text="Média", annotation_position="top right")
                fig.update_xaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=6, rangemode="tozero",
                              showgrid=False, gridwidth=0.5, gridcolor='#f6f6f6')
                fig.update_yaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=10, rangemode="tozero",
                              showgrid=True, gridwidth=0.5, gridcolor='#f6f6f6')
                fig.update_traces(marker_color='#0010B3')
                st.plotly_chart(fig)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_header_destaques_mat, unsafe_allow_html=True)
            with col5:
                st.write("")

        st.markdown(html_br, unsafe_allow_html=True)
        
        html_table=""" 
        <table bordercolor=#FFF0FC>
          <tr style="background-color:#9E089E; height: 90px; color:#FFFFFF; font-family:Georgia; font-size: 17px; text-align: center">
            <th style="width:350px; bordercolor=#FFF0FC">Assunto</th>
            <th style="width:150px; bordercolor=#FFF0FC">Quantidade de questões</th>
            <th style="width:150px; bordercolor=#FFF0FC">Resultado Individual</th>
            <th style="width:150px; bordercolor=#FFF0FC">Resultado Geral</th>
            <th style="width:150px; bordercolor=#FFF0FC">Status</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][0])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][0])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][0])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][0])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][0])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][1])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][1])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][1])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][1])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][1])+"""</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][2])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][2])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][2])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][2])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][2])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][3])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][3])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][3])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][3])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][3])+"""</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][4])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][4])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][4])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][4])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][4])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][5])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][5])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][5])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][5])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][5])+"""</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][6])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][6])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][6])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][6])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][6])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][7])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][7])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][7])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][7])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][7])+"""</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][8])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][8])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][8])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][8])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][8])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][9])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][9])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][9])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][9])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][9])+"""</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][10])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][10])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][10])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][10])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][10])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][11])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][11])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][11])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][11])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][11])+"""</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][12])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][12])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][12])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][12])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][12])+"""</th>
          </tr>
        </table>
        """

        html_card_header_melhores_resultados="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Seus melhores resultados</h5>
          </div>
        </div>
        """
        if len(matematica_tabela_verde_ordenado) > 0:
            html_card_header_melhores_resultados1="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(matematica_tabela_verde_ordenado['Assunto'][0])+"""</p>
              </div>
            </div>
            """
        if len(matematica_tabela_verde_ordenado) > 1:
            html_card_header_melhores_resultados2="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(matematica_tabela_verde_ordenado['Assunto'][1])+"""</p>
              </div>
            </div>
            """
        if len(matematica_tabela_verde_ordenado) > 2:
            html_card_header_melhores_resultados3="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(matematica_tabela_verde_ordenado['Assunto'][2])+"""</p>
              </div>
            </div>
            """
        html_card_header_pontos_melhorar="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Pontos que você pode melhorar</h5>
          </div>
        </div>
        """
        if len(matematica_tabela_vermelho_ordenado) > 0:
            html_card_header_pontos_melhorar1="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(matematica_tabela_vermelho_ordenado['Assunto'][0])+"""</p>
              </div>
            </div>
            """
        if len(matematica_tabela_vermelho_ordenado) > 1:
            html_card_header_pontos_melhorar2="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(matematica_tabela_vermelho_ordenado['Assunto'][1])+"""</p>
              </div>
            </div>
            """
        if len(matematica_tabela_vermelho_ordenado) > 2:
            html_card_header_pontos_melhorar3="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(matematica_tabela_vermelho_ordenado['Assunto'][2])+"""</p>
              </div>
            </div>
            """
        with st.container():
            col1, col2, col3, col4 = st.columns([0.5,12,0.5,10.5])
            with col1:
                st.write("")
            with col2:
                st.markdown(html_table, unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header_melhores_resultados, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                if len(matematica_tabela_verde_ordenado) > 0:
                    st.markdown(html_card_header_melhores_resultados1, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(matematica_tabela_verde_ordenado) > 1:
                    st.markdown(html_card_header_melhores_resultados2, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(matematica_tabela_verde_ordenado) > 2:
                    st.markdown(html_card_header_melhores_resultados3, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)

                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_header_pontos_melhorar, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                if len(matematica_tabela_vermelho_ordenado) > 0:
                    st.markdown(html_card_header_pontos_melhorar1, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(matematica_tabela_vermelho_ordenado) > 1:
                    st.markdown(html_card_header_pontos_melhorar2, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(matematica_tabela_vermelho_ordenado) > 2:
                    st.markdown(html_card_header_pontos_melhorar3, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)

        st.markdown(html_br, unsafe_allow_html=True)

        ### LINGUAGENS

        linguagens_detalhes = base_alunos_fizeram[base_alunos_fizeram['Disciplina'] == 'Linguagens']
    
        linguagens_detalhes_media = linguagens_detalhes.groupby('Assunto').mean(['Acerto']).reset_index()

        linguagens_aluno = linguagens_detalhes[linguagens_detalhes['Login do aluno(a)'] == login_aluno]

        linguagens_aluno_media = linguagens_aluno.groupby('Assunto').mean(['Acerto']).reset_index()
        linguagens_aluno_media2 = linguagens_aluno.groupby('Assunto').count().reset_index()
        linguagens_aluno_media3 = pd.DataFrame()
        linguagens_aluno_media3['Assunto'] = linguagens_aluno_media2['Assunto']
        linguagens_aluno_media3['Número da questão'] = linguagens_aluno_media2['Número da questão']

        linguagens_tabela = pd.merge(linguagens_aluno_media,linguagens_detalhes_media, on = 'Assunto', how = 'inner')
        linguagens_tabela2 = linguagens_tabela.drop(columns = ['Número da questão_x','Número da questão_y','Valor da questão_x','Valor da questão_y','Nota na questão_x','Nota na questão_y','Tempo na questão_x','Tempo na questão_y'])
        linguagens_tabela2.rename(columns = {'Acerto_x':'Resultado Individual decimal','Acerto_y':'Resultado Geral decimal'}, inplace = True)
        linguagens_tabela2['Resultado Geral'] = ''
        linguagens_tabela2['Resultado Individual'] = ''
        for i in range(len(linguagens_tabela2['Assunto'])):
            linguagens_tabela2['Resultado Geral'][i] = "{0:.0%}".format(linguagens_tabela2['Resultado Geral decimal'][i])
            linguagens_tabela2['Resultado Individual'][i] = "{0:.0%}".format(linguagens_tabela2['Resultado Individual decimal'][i])
        linguagens_tabela3 = pd.merge(linguagens_tabela2,linguagens_aluno_media3, on = 'Assunto', how = 'inner')
        linguagens_tabela3.rename(columns = {'Número da questão':'Quantidade de questões'}, inplace = True)
        linguagens_tabela3 = linguagens_tabela3[['Assunto','Quantidade de questões','Resultado Individual', 'Resultado Geral','Resultado Individual decimal', 'Resultado Geral decimal']]
        linguagens_tabela3['Status'] = ''
        for i in range(len(linguagens_tabela3['Assunto'])):
            if linguagens_tabela3['Resultado Individual decimal'][i] == 0:
                linguagens_tabela3['Status'][i] = "🔴" 
            elif linguagens_tabela3['Resultado Individual decimal'][i] >= linguagens_tabela3['Resultado Geral decimal'][i]:
                linguagens_tabela3['Status'][i] = "🟢"
            elif linguagens_tabela3['Resultado Individual decimal'][i] - linguagens_tabela3['Resultado Geral decimal'][i] > - 0.25:
                linguagens_tabela3['Status'][i] = "🟡"
            else:
                linguagens_tabela3['Status'][i] = "🔴"
        linguagens_tabela3['Diferença'] = ''
        for i in range(len(linguagens_tabela3['Assunto'])):
            linguagens_tabela3['Diferença'][i] = linguagens_tabela3['Resultado Individual decimal'][i] - linguagens_tabela3['Resultado Geral decimal'][i]

        linguagens_tabela_ordenado = linguagens_tabela3.sort_values(by = 'Diferença')

        linguagens_tabela_verde = linguagens_tabela_ordenado[linguagens_tabela_ordenado['Status'] == '🟢']
        linguagens_tabela_verde_ordenado = linguagens_tabela_verde.sort_values(by = 'Diferença', ascending = False).reset_index(drop = True)

        linguagens_tabela_vermelho = linguagens_tabela_ordenado[linguagens_tabela_ordenado['Status'] == '🔴']
        linguagens_tabela_vermelho_ordenado = linguagens_tabela_vermelho.sort_values(by = 'Diferença', ascending = True).reset_index(drop = True)

        html_header_lin="""
        <h2 style="font-size:200%; color: #9E089E; font-family:Georgia"> LINGUAGENS<br>
         <hr style= "  display: block;
          margin-top: 0.5em;
          margin-bottom: 0.5em;
          margin-left: auto;
          margin-right: auto;
          border-style: inset;
          border-width: 1.5px;"></h2>
        """
        st.markdown(html_header_lin, unsafe_allow_html=True)
        ### Block 1#########################################################################################
        with st.container():
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1,20,1,20,1,20,1])
            with col1:
                st.write("")
            with col2:
                st.markdown(html_card_header1_disc, unsafe_allow_html=True)
                fig_c1 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=round(resultados_linguagens['Nota na questão'][0],1),
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais_disciplina_med_lin['Nota na questão'][0],-1),0)), 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c1.update_layout(autosize=False,
                                     width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                st.plotly_chart(fig_c1)
                st.markdown(html_card_footer1_disc, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_footer1_disc_med_lin, unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header2_disc, unsafe_allow_html=True)
                fig_c2 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=resultados_linguagens['Acerto'][0],
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais_disciplina_med_lin['Acerto'][0],-1),0))},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c2.update_layout(autosize=False,
                                     width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c2.update_traces(delta_decreasing_color="#FF4136",
                                 delta_increasing_color="#3D9970",
                                 delta_valueformat='f',
                                 selector=dict(type='indicator'))
                st.plotly_chart(fig_c2)
                st.markdown(html_card_footer2_disc, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_footer2_disc_med_lin, unsafe_allow_html=True)
            with col5:
                st.write("")
            with col6:
                st.markdown(html_card_header3_disc, unsafe_allow_html=True)
                fig_c3 = go.Figure(go.Indicator(
                    mode="number",
                    value=classificacao_aluno_lin['index'][0]+1,
                    number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': 1, 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c3.update_layout(autosize=False,
                                     width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                     delta_increasing_color="#FF4136",
                                     delta_valueformat='.3f',
                                     selector=dict(type='indicator'))
                st.plotly_chart(fig_c3)
                st.markdown(html_card_footer3_disc_matlin, unsafe_allow_html=True)
            with col7:
                st.write("")
        html_br="""
        <br>
        """
        st.markdown(html_br, unsafe_allow_html=True)

        ponto = str(round(100*(numero_candidatos-(classificacao_aluno_lin['index'][0]))/numero_candidatos,0)).find('.')
        texto = str(round(100*(numero_candidatos-(classificacao_aluno_lin['index'][0]))/numero_candidatos,0))[0:ponto]
        html_card_header_destaques_lin="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
           height: 150px;">
            <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
          </div>
        </div>
        """  

        st.markdown(html_br, unsafe_allow_html=True)

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([9,25,2,25,4])
            with col1:
                st.write("")
            with col2:
               # create the bins
                counts, bins = np.histogram(resultados_gerais_disciplina3_lin['Nota na questão'], bins=range(0, 1100, 100))
                bins = 0.5 * (bins[:-1] + bins[1:])
                fig = px.bar(x=bins, y=counts, labels={'x':'Nota no simulado', 'y':'Número de alunos'})
                fig.update_layout(title={'text': "Distribuição de notas", 'x': 0.5}, paper_bgcolor="#FFF0FC", 
                               plot_bgcolor="#FFF0FC", font={'color': "#9E089E", 'size': 14, 'family': "Georgia"}, height=400,
                               width=540,
                               legend=dict(orientation="h",
                                           yanchor="top",
                                           y=0.99,
                                           xanchor="left",
                                           x=0.01),
                               margin=dict(l=1, r=1, b=1, t=30))
                fig.add_vline(x=int(resultados_linguagens['Nota na questão']), line_width=7, line_dash="dash", line_color="#9E089E", annotation_text="Você está aqui!", annotation_position="top right")
                fig.add_vline(x=int(round(truncar(resultados_gerais_disciplina_med_lin['Nota na questão'][0],-1),0)), line_width=7, line_dash="dash", line_color="#01ECEC", annotation_text="Média", annotation_position="top right")
                fig.update_xaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=6, rangemode="tozero",
                              showgrid=False, gridwidth=0.5, gridcolor='#f6f6f6')
                fig.update_yaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=10, rangemode="tozero",
                              showgrid=True, gridwidth=0.5, gridcolor='#f6f6f6')
                fig.update_traces(marker_color='#0010B3')
                st.plotly_chart(fig)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_header_destaques_lin, unsafe_allow_html=True)
            with col5:
                st.write("")

        html_table_lin=""" 
        <table bordercolor=#FFF0FC>
          <tr style="background-color:#9E089E; height: 90px; color:#FFFFFF; font-family:Georgia; font-size: 17px; text-align: center">
            <th style="width:350px; bordercolor=#FFF0FC">Assunto</th>
            <th style="width:150px; bordercolor=#FFF0FC">Quantidade de questões</th>
            <th style="width:150px; bordercolor=#FFF0FC">Resultado Individual</th>
            <th style="width:150px; bordercolor=#FFF0FC">Resultado Geral</th>
            <th style="width:150px; bordercolor=#FFF0FC">Status</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(linguagens_tabela3['Assunto'][0])+"""</th>
            <th>"""+str(linguagens_tabela3['Quantidade de questões'][0])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Individual'][0])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Geral'][0])+"""</th>
            <th>"""+str(linguagens_tabela3['Status'][0])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(linguagens_tabela3['Assunto'][1])+"""</th>
            <th>"""+str(linguagens_tabela3['Quantidade de questões'][1])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Individual'][1])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Geral'][1])+"""</th>
            <th>"""+str(linguagens_tabela3['Status'][1])+"""</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(linguagens_tabela3['Assunto'][2])+"""</th>
            <th>"""+str(linguagens_tabela3['Quantidade de questões'][2])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Individual'][2])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Geral'][2])+"""</th>
            <th>"""+str(linguagens_tabela3['Status'][2])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(linguagens_tabela3['Assunto'][3])+"""</th>
            <th>"""+str(linguagens_tabela3['Quantidade de questões'][3])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Individual'][3])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Geral'][3])+"""</th>
            <th>"""+str(linguagens_tabela3['Status'][3])+"""</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(linguagens_tabela3['Assunto'][4])+"""</th>
            <th>"""+str(linguagens_tabela3['Quantidade de questões'][4])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Individual'][4])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Geral'][4])+"""</th>
            <th>"""+str(linguagens_tabela3['Status'][4])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(linguagens_tabela3['Assunto'][5])+"""</th>
            <th>"""+str(linguagens_tabela3['Quantidade de questões'][5])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Individual'][5])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Geral'][5])+"""</th>
            <th>"""+str(linguagens_tabela3['Status'][5])+"""</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(linguagens_tabela3['Assunto'][6])+"""</th>
            <th>"""+str(linguagens_tabela3['Quantidade de questões'][6])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Individual'][6])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Geral'][6])+"""</th>
            <th>"""+str(linguagens_tabela3['Status'][6])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(linguagens_tabela3['Assunto'][7])+"""</th>
            <th>"""+str(linguagens_tabela3['Quantidade de questões'][7])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Individual'][7])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Geral'][7])+"""</th>
            <th>"""+str(linguagens_tabela3['Status'][7])+"""</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(linguagens_tabela3['Assunto'][8])+"""</th>
            <th>"""+str(linguagens_tabela3['Quantidade de questões'][8])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Individual'][8])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Geral'][8])+"""</th>
            <th>"""+str(linguagens_tabela3['Status'][8])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(linguagens_tabela3['Assunto'][9])+"""</th>
            <th>"""+str(linguagens_tabela3['Quantidade de questões'][9])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Individual'][9])+"""</th>
            <th>"""+str(linguagens_tabela3['Resultado Geral'][9])+"""</th>
            <th>"""+str(linguagens_tabela3['Status'][9])+"""</th>
          </tr>
        </table>
        """

        html_card_header_melhores_resultados_lin="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Seus melhores resultados</h5>
          </div>
        </div>
        """
        if len(linguagens_tabela_verde_ordenado) > 0:
            html_card_header_melhores_resultados1_lin="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(linguagens_tabela_verde_ordenado['Assunto'][0])+"""</p>
              </div>
            </div>
            """
        if len(linguagens_tabela_verde_ordenado) > 1:
            html_card_header_melhores_resultados2_lin="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(linguagens_tabela_verde_ordenado['Assunto'][1])+"""</p>
              </div>
            </div>
            """
        if len(linguagens_tabela_verde_ordenado) > 2:
            html_card_header_melhores_resultados3_lin="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(linguagens_tabela_verde_ordenado['Assunto'][2])+"""</p>
              </div>
            </div>
            """
        html_card_header_pontos_melhorar_lin="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Pontos que você pode melhorar</h5>
          </div>
        </div>
        """
        if len(linguagens_tabela_vermelho_ordenado) > 0:
            html_card_header_pontos_melhorar1_lin="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(linguagens_tabela_vermelho_ordenado['Assunto'][0])+"""</p>
              </div>
            </div>
            """
        if len(linguagens_tabela_vermelho_ordenado) > 1:
            html_card_header_pontos_melhorar2_lin="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(linguagens_tabela_vermelho_ordenado['Assunto'][1])+"""</p>
              </div>
            </div>
            """
        if len(linguagens_tabela_vermelho_ordenado) > 2:
            html_card_header_pontos_melhorar3_lin="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(linguagens_tabela_vermelho_ordenado['Assunto'][2])+"""</p>
              </div>
            </div>
            """
        
        with st.container():
            col1, col2, col3, col4 = st.columns([0.5,12,0.5,10.5])
            with col1:
                st.write("")
            with col2:
                st.markdown(html_table_lin, unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header_melhores_resultados_lin, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                if len(linguagens_tabela_verde_ordenado) > 0:
                    st.markdown(html_card_header_melhores_resultados1_lin, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(linguagens_tabela_verde_ordenado) > 1:
                    st.markdown(html_card_header_melhores_resultados2_lin, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(linguagens_tabela_verde_ordenado) > 2:
                    st.markdown(html_card_header_melhores_resultados3_lin, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)

                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_header_pontos_melhorar_lin, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                if len(linguagens_tabela_vermelho_ordenado) > 0:
                    st.markdown(html_card_header_pontos_melhorar1_lin, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(linguagens_tabela_vermelho_ordenado) > 1:
                    st.markdown(html_card_header_pontos_melhorar2_lin, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(linguagens_tabela_vermelho_ordenado) > 2:
                    st.markdown(html_card_header_pontos_melhorar3_lin, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)

        st.markdown(html_br, unsafe_allow_html=True)

        if resultados_gerais_aluno['Turma'][0] != turma_eng and resultados_gerais_aluno['Turma'][0] != turma_cien:
            ciencias_detalhes = base_alunos_fizeram[base_alunos_fizeram['Disciplina'] == 'Ciências Humanas']
        else:
            ciencias_detalhes = base_alunos_fizeram[base_alunos_fizeram['Disciplina'] == 'Ciências da Natureza']
    
        ciencias_detalhes_media = ciencias_detalhes.groupby('Assunto').mean(['Acerto']).reset_index()

        ciencias_aluno = ciencias_detalhes[ciencias_detalhes['Login do aluno(a)'] == login_aluno]

        ciencias_aluno_media = ciencias_aluno.groupby('Assunto').mean(['Acerto']).reset_index()
        ciencias_aluno_media2 = ciencias_aluno.groupby('Assunto').count().reset_index()
        ciencias_aluno_media3 = pd.DataFrame()
        ciencias_aluno_media3['Assunto'] = ciencias_aluno_media2['Assunto']
        ciencias_aluno_media3['Número da questão'] = ciencias_aluno_media2['Número da questão']

        ciencias_tabela = pd.merge(ciencias_aluno_media,ciencias_detalhes_media, on = 'Assunto', how = 'inner')
        ciencias_tabela2 = ciencias_tabela.drop(columns = ['Número da questão_x','Número da questão_y','Valor da questão_x','Valor da questão_y','Nota na questão_x','Nota na questão_y','Tempo na questão_x','Tempo na questão_y'])
        ciencias_tabela2.rename(columns = {'Acerto_x':'Resultado Individual decimal','Acerto_y':'Resultado Geral decimal'}, inplace = True)
        ciencias_tabela2['Resultado Geral'] = ''
        ciencias_tabela2['Resultado Individual'] = ''
        for i in range(len(ciencias_tabela2['Assunto'])):
            ciencias_tabela2['Resultado Geral'][i] = "{0:.0%}".format(ciencias_tabela2['Resultado Geral decimal'][i])
            ciencias_tabela2['Resultado Individual'][i] = "{0:.0%}".format(ciencias_tabela2['Resultado Individual decimal'][i])
        ciencias_tabela3 = pd.merge(ciencias_tabela2,ciencias_aluno_media3, on = 'Assunto', how = 'inner')
        
        ciencias_tabela3.rename(columns = {'Número da questão':'Quantidade de questões'}, inplace = True)
        ciencias_tabela3 = ciencias_tabela3[['Assunto','Quantidade de questões','Resultado Individual', 'Resultado Geral','Resultado Individual decimal', 'Resultado Geral decimal']]
        ciencias_tabela3['Status'] = ''
        for i in range(len(ciencias_tabela3['Assunto'])):
            if ciencias_tabela3['Resultado Individual decimal'][i] == 0:
                ciencias_tabela3['Status'][i] = "🔴" 
            elif ciencias_tabela3['Resultado Individual decimal'][i] >= ciencias_tabela3['Resultado Geral decimal'][i]:
                ciencias_tabela3['Status'][i] = "🟢"
            elif ciencias_tabela3['Resultado Individual decimal'][i] - ciencias_tabela3['Resultado Geral decimal'][i] > - 0.25:
                ciencias_tabela3['Status'][i] = "🟡"
            else:
                ciencias_tabela3['Status'][i] = "🔴"
        ciencias_tabela3['Diferença'] = ''
        for i in range(len(ciencias_tabela3['Assunto'])):
            ciencias_tabela3['Diferença'][i] = ciencias_tabela3['Resultado Individual decimal'][i] - ciencias_tabela3['Resultado Geral decimal'][i]

        ciencias_tabela_ordenado = ciencias_tabela3.sort_values(by = 'Diferença')

        ciencias_tabela_verde = ciencias_tabela_ordenado[ciencias_tabela_ordenado['Status'] == '🟢']
        ciencias_tabela_verde_ordenado = ciencias_tabela_verde.sort_values(by = 'Diferença', ascending = False).reset_index(drop = True)

        ciencias_tabela_vermelho = ciencias_tabela_ordenado[ciencias_tabela_ordenado['Status'] == '🔴']
        ciencias_tabela_vermelho_ordenado = ciencias_tabela_vermelho.sort_values(by = 'Diferença', ascending = True).reset_index(drop = True)

        html_header_hum="""
        <h2 style="font-size:200%; color: #9E089E; font-family:Georgia"> CIÊNCIAS HUMANAS<br>
         <hr style= "  display: block;
          margin-top: 0.5em;
          margin-bottom: 0.5em;
          margin-left: auto;
          margin-right: auto;
          border-style: inset;
          border-width: 1.5px;"></h2>
        """

        html_header_nat="""
        <h2 style="font-size:200%; color: #9E089E; font-family:Georgia"> CIÊNCIAS DA NATUREZA<br>
         <hr style= "  display: block;
          margin-top: 0.5em;
          margin-bottom: 0.5em;
          margin-left: auto;
          margin-right: auto;
          border-style: inset;
          border-width: 1.5px;"></h2>
        """
        if len(resultados_ciencias_hum['Disciplina']) == 0:
            st.markdown(html_header_nat, unsafe_allow_html=True)
        else:
            st.markdown(html_header_hum, unsafe_allow_html=True)

        ### Block 1#########################################################################################
        with st.container():
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1,20,1,20,1,20,1])
            with col1:
                st.write("")
            with col2:
                st.markdown(html_card_header1_disc, unsafe_allow_html=True)
                fig_c1 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=round(resultados_ciencias_fim['Nota na questão'][0],1),
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais_disciplina_med_cie['Nota na questão'][0],-1),0)), 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c1.update_layout(autosize=False,
                                     width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                st.plotly_chart(fig_c1)
                st.markdown(html_card_footer1_disc, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_footer1_disc_med_cie, unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header2_disc, unsafe_allow_html=True)
                fig_c2 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=resultados_ciencias_fim['Acerto'][0],
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais_disciplina_med_cie['Acerto'][0],-1),0))},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c2.update_layout(autosize=False,
                                     width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c2.update_traces(delta_decreasing_color="#FF4136",
                                 delta_increasing_color="#3D9970",
                                 delta_valueformat='f',
                                 selector=dict(type='indicator'))
                st.plotly_chart(fig_c2)
                st.markdown(html_card_footer2_disc, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_footer2_disc_med_cie, unsafe_allow_html=True)
            with col5:
                st.write("")
            with col6:
                st.markdown(html_card_header3_disc, unsafe_allow_html=True)
                fig_c3 = go.Figure(go.Indicator(
                    mode="number",
                    value=classificacao_aluno_fim['index'][0]+1,
                    number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': 1, 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c3.update_layout(autosize=False,
                                     width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                     delta_increasing_color="#FF4136",
                                     delta_valueformat='.3f',
                                     selector=dict(type='indicator'))
                st.plotly_chart(fig_c3)
                st.markdown(html_card_footer3_disc, unsafe_allow_html=True)
            with col7:
                st.write("")
        html_br="""
        <br>
        """
        st.markdown(html_br, unsafe_allow_html=True)
        if resultados_gerais_aluno['Turma'][0] != turma_eng and resultados_gerais_aluno['Turma'][0] != turma_cien:
            ponto = str(round(100*((numero_candidatos-numero_eng_cien)-(classificacao_aluno_fim['index'][0]))/(numero_candidatos-numero_eng_cien),0)).find('.')
            texto = str(round(100*((numero_candidatos-numero_eng_cien)-(classificacao_aluno_fim['index'][0]))/(numero_candidatos-numero_eng_cien),0))[0:ponto]
        else:
            ponto = str(round(100*((numero_eng_cien)-(classificacao_aluno_fim['index'][0]))/(numero_eng_cien),0)).find('.')
            texto = str(round(100*((numero_eng_cien)-(classificacao_aluno_fim['index'][0]))/(numero_eng_cien),0))[0:ponto]
       
        html_card_header_destaques_cie="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
           height: 150px;">
            <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
          </div>
        </div>
        """  

        st.markdown(html_br, unsafe_allow_html=True)

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([9,25,2,25,4])
            with col1:
                st.write("")
            with col2:
               # create the bins
                counts, bins = np.histogram(resultados_gerais_disciplina3_fim['Nota na questão'], bins=range(0, 1100, 100))
                bins = 0.5 * (bins[:-1] + bins[1:])
                fig = px.bar(x=bins, y=counts, labels={'x':'Nota no simulado', 'y':'Número de alunos'})
                fig.update_layout(title={'text': "Distribuição de notas", 'x': 0.5}, paper_bgcolor="#FFF0FC", 
                               plot_bgcolor="#FFF0FC", font={'color': "#9E089E", 'size': 14, 'family': "Georgia"}, height=400,
                               width=540,
                               legend=dict(orientation="h",
                                           yanchor="top",
                                           y=0.99,
                                           xanchor="left",
                                           x=0.01),
                               margin=dict(l=1, r=1, b=1, t=30))
                fig.add_vline(x=int(resultados_ciencias_fim['Nota na questão']), line_width=7, line_dash="dash", line_color="#9E089E", annotation_text="Você está aqui!", annotation_position="top right")
                fig.add_vline(x=int(round(truncar(resultados_gerais_disciplina_med_cie['Nota na questão'][0],-1),0)), line_width=7, line_dash="dash", line_color="#01ECEC", annotation_text="Média", annotation_position="top right")
                fig.update_xaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=6, rangemode="tozero",
                              showgrid=False, gridwidth=0.5, gridcolor='#f6f6f6')
                fig.update_yaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=10, rangemode="tozero",
                              showgrid=True, gridwidth=0.5, gridcolor='#f6f6f6')
                fig.update_traces(marker_color='#0010B3')
                st.plotly_chart(fig)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_header_destaques_cie, unsafe_allow_html=True)
            with col5:
                st.write("")
        if turma_aluno['Turma'][0] != turma_eng and turma_aluno['Turma'][0] != turma_cien:
            html_table_cie_hum=""" 
            <table bordercolor=#FFF0FC>
            <tr style="background-color:#9E089E; height: 90px; color:#FFFFFF; font-family:Georgia; font-size: 17px; text-align: center">
                <th style="width:350px; bordercolor=#FFF0FC">Assunto</th>
                <th style="width:150px; bordercolor=#FFF0FC">Quantidade de questões</th>
                <th style="width:150px; bordercolor=#FFF0FC">Resultado Individual</th>
                <th style="width:150px; bordercolor=#FFF0FC">Resultado Geral</th>
                <th style="width:150px; bordercolor=#FFF0FC">Status</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][0])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][0])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][0])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][0])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][0])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][1])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][1])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][1])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][1])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][1])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][2])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][2])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][2])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][2])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][2])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][3])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][3])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][3])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][3])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][3])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][4])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][4])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][4])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][4])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][4])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][5])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][5])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][5])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][5])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][5])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][6])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][6])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][6])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][6])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][6])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][7])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][7])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][7])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][7])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][7])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][8])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][8])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][8])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][8])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][8])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][9])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][9])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][9])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][9])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][9])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][10])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][10])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][10])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][10])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][10])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][11])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][11])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][11])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][11])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][11])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][12])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][12])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][12])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][12])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][12])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][13])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][13])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][13])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][13])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][13])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][14])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][14])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][14])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][14])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][14])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][15])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][15])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][15])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][15])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][15])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][16])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][16])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][16])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][16])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][16])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][17])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][17])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][17])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][17])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][17])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][18])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][18])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][18])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][18])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][18])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][19])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][19])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][19])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][19])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][19])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][20])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][20])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][20])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][20])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][20])+"""</th>
            </tr>
            </tr>
            </tr>
            </table>
            """
        else:
            html_table_cie_nat=""" 
            <table bordercolor=#FFF0FC>
            <tr style="background-color:#9E089E; height: 90px; color:#FFFFFF; font-family:Georgia; font-size: 17px; text-align: center">
                <th style="width:350px; bordercolor=#FFF0FC">Assunto</th>
                <th style="width:150px; bordercolor=#FFF0FC">Quantidade de questões</th>
                <th style="width:150px; bordercolor=#FFF0FC">Resultado Individual</th>
                <th style="width:150px; bordercolor=#FFF0FC">Resultado Geral</th>
                <th style="width:150px; bordercolor=#FFF0FC">Status</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][0])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][0])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][0])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][0])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][0])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][1])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][1])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][1])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][1])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][1])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][2])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][2])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][2])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][2])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][2])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][3])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][3])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][3])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][3])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][3])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][4])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][4])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][4])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][4])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][4])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][5])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][5])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][5])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][5])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][5])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][6])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][6])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][6])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][6])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][6])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][7])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][7])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][7])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][7])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][7])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][8])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][8])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][8])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][8])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][8])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][9])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][9])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][9])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][9])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][9])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][10])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][10])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][10])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][10])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][10])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][11])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][11])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][11])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][11])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][11])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][12])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][12])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][12])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][12])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][12])+"""</th>
            </tr>
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][13])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][13])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][13])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][13])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][13])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][14])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][14])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][14])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][14])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][14])+"""</th>
            </tr>
            </table>
            """

        html_card_header_melhores_resultados_cie="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Seus melhores resultados</h5>
          </div>
        </div>
        """
        if len(ciencias_tabela_verde_ordenado) > 0:
            html_card_header_melhores_resultados1_cie="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(ciencias_tabela_verde_ordenado['Assunto'][0])+"""</p>
              </div>
            </div>
            """
        if len(ciencias_tabela_verde_ordenado) > 1:
            html_card_header_melhores_resultados2_cie="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(ciencias_tabela_verde_ordenado['Assunto'][1])+"""</p>
              </div>
            </div>
            """
        if len(ciencias_tabela_verde_ordenado) > 2:
            html_card_header_melhores_resultados3_cie="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(ciencias_tabela_verde_ordenado['Assunto'][2])+"""</p>
              </div>
            </div>
            """
        html_card_header_pontos_melhorar_cie="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Pontos que você pode melhorar</h5>
          </div>
        </div>
        """
        if len(ciencias_tabela_vermelho_ordenado) > 0:
            html_card_header_pontos_melhorar1_cie="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(ciencias_tabela_vermelho_ordenado['Assunto'][0])+"""</p>
              </div>
            </div>
            """
        if len(ciencias_tabela_vermelho_ordenado) > 1:
            html_card_header_pontos_melhorar2_cie="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(ciencias_tabela_vermelho_ordenado['Assunto'][1])+"""</p>
              </div>
            </div>
            """
        if len(ciencias_tabela_vermelho_ordenado) > 2:
            html_card_header_pontos_melhorar3_cie="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(ciencias_tabela_vermelho_ordenado['Assunto'][2])+"""</p>
              </div>
            </div>
            """

        with st.container():
            col1, col2, col3, col4 = st.columns([0.5,12,0.5,10.5])
            with col1:
                st.write("")
            with col2:
                if turma_aluno['Turma'][0] == turma_eng or turma_aluno['Turma'][0] == turma_cien:
                    st.markdown(html_table_cie_nat, unsafe_allow_html=True)
                else:
                    st.markdown(html_table_cie_hum, unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header_melhores_resultados_cie, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                if len(ciencias_tabela_verde_ordenado) > 0:
                    st.markdown(html_card_header_melhores_resultados1_cie, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(ciencias_tabela_verde_ordenado) > 1:
                    st.markdown(html_card_header_melhores_resultados2_cie, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(ciencias_tabela_verde_ordenado) > 2:
                    st.markdown(html_card_header_melhores_resultados3_cie, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)

                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_header_pontos_melhorar_cie, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                if len(ciencias_tabela_vermelho_ordenado) > 0:
                    st.markdown(html_card_header_pontos_melhorar1_cie, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(ciencias_tabela_vermelho_ordenado) > 1:
                    st.markdown(html_card_header_pontos_melhorar2_cie, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(ciencias_tabela_vermelho_ordenado) > 2:
                    st.markdown(html_card_header_pontos_melhorar3_cie, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)

        st.markdown(html_br, unsafe_allow_html=True)
        st.markdown(html_br, unsafe_allow_html=True)

    ### Redação

    base_redacao = pd.read_csv('./resultadoredacao.csv')
    
    base_redacao['Acerto'] = 0.00
    for i in range(len(base_redacao)):
        base_redacao['Acerto'][i] = base_redacao['Nota na questão'][i]/base_redacao['Valor da questão'][i]
    
    base_redacao2 = base_redacao[base_redacao['Nota na questão'] >= 0]
    base_redacao_aux = base_redacao[base_redacao['Nota na questão'] > 0]
    
    redacao_detalhes_media = base_redacao_aux.groupby('Competência').mean(['Acerto']).reset_index()
    
    redacao_aluno = base_redacao2[base_redacao2['Login do aluno(a)'] == login_aluno]
    
    redacao_aluno_media = redacao_aluno.groupby('Competência').mean(['Acerto']).reset_index()

    redacao_aluno_media2 = redacao_aluno.groupby('Competência').count().reset_index()

    redacao_aluno_media3 = pd.DataFrame()
    redacao_aluno_media3['Competência'] = redacao_aluno_media2['Competência']
    redacao_aluno_media3['Nota na questão'] = redacao_aluno_media2['Nota na questão']
    
    redacao_tabela = pd.merge(redacao_aluno_media,redacao_detalhes_media, on = 'Competência', how = 'inner')

    redacao_tabela2 = redacao_tabela.drop(columns = ['Valor da questão_x','Valor da questão_y','Nota na questão_x','Nota na questão_y'])
    redacao_tabela2.rename(columns = {'Acerto_x':'Resultado Individual decimal','Acerto_y':'Resultado Geral decimal'}, inplace = True)
    redacao_tabela2['Resultado Geral'] = ''
    redacao_tabela2['Resultado Individual'] = ''
    
    for i in range(len(redacao_tabela2['Competência'])):
        redacao_tabela2['Resultado Geral'][i] = "{0:.0%}".format(redacao_tabela2['Resultado Geral decimal'][i])
        redacao_tabela2['Resultado Individual'][i] = "{0:.0%}".format(redacao_tabela2['Resultado Individual decimal'][i])
    redacao_tabela3 = pd.merge(redacao_tabela2,redacao_aluno_media3, on = 'Competência', how = 'inner')
    
    redacao_tabela3 = redacao_tabela3[['Competência','Resultado Individual', 'Resultado Geral','Resultado Individual decimal', 'Resultado Geral decimal']]
    redacao_tabela3['Status'] = ''
    for i in range(len(redacao_tabela3['Competência'])):
        if redacao_tabela3['Resultado Individual decimal'][i] == 0:
            redacao_tabela3['Status'][i] = "🔴" 
        elif redacao_tabela3['Resultado Individual decimal'][i] >= redacao_tabela3['Resultado Geral decimal'][i]:
            redacao_tabela3['Status'][i] = "🟢"
        elif redacao_tabela3['Resultado Individual decimal'][i] - redacao_tabela3['Resultado Geral decimal'][i] > - 0.25:
            redacao_tabela3['Status'][i] = "🟡"
        else:
            redacao_tabela3['Status'][i] = "🔴"
    redacao_tabela3['Diferença'] = ''

    for i in range(len(redacao_tabela3['Competência'])):
        redacao_tabela3['Diferença'][i] = redacao_tabela3['Resultado Individual decimal'][i] - redacao_tabela3['Resultado Geral decimal'][i]
    
    redacao_tabela_ordenado = redacao_tabela3.sort_values(by = 'Diferença')

    redacao_tabela_verde = redacao_tabela_ordenado[redacao_tabela_ordenado['Status'] == '🟢']
    redacao_tabela_verde_ordenado = redacao_tabela_verde.sort_values(by = 'Diferença', ascending = False).reset_index(drop = True)
    
    redacao_tabela_vermelho = redacao_tabela_ordenado[redacao_tabela_ordenado['Status'] == '🔴']
    redacao_tabela_vermelho_ordenado = redacao_tabela_vermelho.sort_values(by = 'Diferença', ascending = True).reset_index(drop = True)

    html_header_red="""
    <h2 style="font-size:200%; color: #9E089E; font-family:Georgia"> REDAÇÃO<br>
     <hr style= "  display: block;
      margin-top: 0.5em;
      margin-bottom: 0.5em;
      margin-left: auto;
      margin-right: auto;
      border-style: inset;
      border-width: 1.5px;"></h2>
    """

    html_card_footer1_disc_med_red="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(200+0.8*200*redacao_tabela3['Resultado Geral decimal'].sum(),0)))+"""</p>
      </div>
    </div>
    """

    base_redacao_disciplina = base_redacao2.groupby('Login do aluno(a)').sum().reset_index()
    
    for i in range(len(base_redacao_disciplina['Login do aluno(a)'])):
        if base_redacao_disciplina['Nota na questão'][i] > 0:
            base_redacao_disciplina['Nota na questão'][i] = 200 + 0.8*base_redacao_disciplina['Nota na questão'][i]
    #base_redacao_disciplina['Nota na questão'] = 200 + 0.8*base_redacao_disciplina['Nota na questão']

    base_redacao_disciplina2 = base_redacao_disciplina.sort_values(by = 'Nota na questão', ascending = False).reset_index()

    classificacao_aluno_red = base_redacao_disciplina2[base_redacao_disciplina2['Login do aluno(a)'] == login_aluno].reset_index()
    #st.write(len(classificacao_aluno_red))
    #if classificacao_aluno_red['level_0'][0] > numero_candidatos and len(classificacao_aluno_red) > 0:
    #    classificacao_aluno_red['level_0'][0] = numero_candidatos

    if len(classificacao_aluno_red) == 0:
        class_aluno_red = numero_candidatos
    else: 
        class_aluno_red = classificacao_aluno_red['level_0'][0]
    
    ponto = str(round(100*(numero_candidatos-(class_aluno_red))/numero_candidatos,0)).find('.')
    texto = str(round(100*(numero_candidatos-(class_aluno_red))/numero_candidatos,0))[0:ponto]
    
    
    html_card_header_destaques_red="""
    <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
            height: 150px;">
            <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
        </div>
    </div>
    """  
    for i in range(len(redacao_aluno_media['Nota na questão'])):
        if redacao_aluno_media['Nota na questão'][i] == 0:
            redacao_aluno_media['Nota na questão'][i] = - 50

    if len(redacao_tabela3['Status']) != 0:
        
        ### REDAÇÃO
        
        st.markdown(html_header_red, unsafe_allow_html=True)
        
        ### Block 1#########################################################################################
        with st.container():
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1,20,1,20,1,20,1])
            with col1:
                st.write("")
            with col2:
                st.markdown(html_card_header1_disc, unsafe_allow_html=True)
                fig_c1 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=round(200+0.8*redacao_aluno_media['Nota na questão'].sum(),1),
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': int(round(200+0.8*200*redacao_tabela3['Resultado Geral decimal'].sum(),0)), 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c1.update_layout(autosize=False,
                                     width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                st.plotly_chart(fig_c1)
                st.markdown(html_card_footer1_disc, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_footer1_disc_med_red, unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header3_disc, unsafe_allow_html=True)
                fig_c3 = go.Figure(go.Indicator(
                    mode="number",
                    value=classificacao_aluno_red['level_0'][0]+1,
                    number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': 1, 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c3.update_layout(autosize=False,
                                     width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                     delta_increasing_color="#FF4136",
                                     delta_valueformat='.3f',
                                     selector=dict(type='indicator'))
                st.plotly_chart(fig_c3)
                st.markdown(html_card_footer3_disc_matlin, unsafe_allow_html=True)
            with col5:
                st.write("")
            with col6:
                st.write("")
            with col7:
                st.write("")
        html_br="""
        <br>
        """

        st.markdown(html_br, unsafe_allow_html=True)
        st.markdown(html_br, unsafe_allow_html=True)
        
        base_redacao3 = base_redacao2.groupby('Login do aluno(a)').sum().reset_index()
        for i in range(len(base_redacao3['Nota na questão'])):
            if base_redacao3['Nota na questão'][i] > 0:
                base_redacao3['Nota na questão'][i] = 200 + 0.8*base_redacao3['Nota na questão'][i]
        base_redacao4 = base_redacao3[base_redacao3['Login do aluno(a)'] == login_aluno]
        base_redacao3aux = base_redacao3[base_redacao3['Nota na questão'] > 0]
        st.dataframe(base_redacao3aux)
        base_redacao5 = base_redacao3aux.mean('Nota na questão')

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([9,25,2,25,4])
            with col1:
                st.write("")
            with col2:
               # create the bins
                counts, bins = np.histogram(base_redacao3aux['Nota na questão'], bins=range(0, 1100, 100))
                bins = 0.5 * (bins[:-1] + bins[1:])
                fig = px.bar(x=bins, y=counts, labels={'x':'Nota no simulado', 'y':'Número de alunos'})
                fig.update_layout(title={'text': "Distribuição de notas", 'x': 0.5}, paper_bgcolor="#FFF0FC", 
                               plot_bgcolor="#FFF0FC", font={'color': "#9E089E", 'size': 14, 'family': "Georgia"}, height=400,
                               width=540,
                               legend=dict(orientation="h",
                                           yanchor="top",
                                           y=0.99,
                                           xanchor="left",
                                           x=0.01),
                               margin=dict(l=1, r=1, b=1, t=30))
                fig.add_vline(x=int(base_redacao4['Nota na questão']), line_width=7, line_dash="dash", line_color="#9E089E", annotation_text="Você está aqui!", annotation_position="top right")
                fig.add_vline(x=int(round(truncar(base_redacao5['Nota na questão'],-1),0)), line_width=7, line_dash="dash", line_color="#01ECEC", annotation_text="Média", annotation_position="top right")
                fig.update_xaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=6, rangemode="tozero",
                              showgrid=False, gridwidth=0.5, gridcolor='#f6f6f6')
                fig.update_yaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=10, rangemode="tozero",
                              showgrid=True, gridwidth=0.5, gridcolor='#f6f6f6')
                fig.update_traces(marker_color='#0010B3')
                st.plotly_chart(fig)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_header_destaques_red, unsafe_allow_html=True)
            with col5:
                st.write("")

        st.markdown(html_br, unsafe_allow_html=True)

        html_table=""" 
        <table bordercolor=#FFF0FC>
          <tr style="background-color:#9E089E; height: 90px; color:#FFFFFF; font-family:Georgia; font-size: 17px; text-align: center">
            <th style="width:350px; bordercolor=#FFF0FC">Competência</th>
            <th style="width:150px; bordercolor=#FFF0FC">Resultado Individual</th>
            <th style="width:150px; bordercolor=#FFF0FC">Resultado Geral</th>
            <th style="width:150px; bordercolor=#FFF0FC">Status</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(redacao_tabela3['Competência'][0])+"""</th>
            <th>"""+str(redacao_tabela3['Resultado Individual'][0])+"""</th>
            <th>"""+str(redacao_tabela3['Resultado Geral'][0])+"""</th>
            <th>"""+str(redacao_tabela3['Status'][0])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(redacao_tabela3['Competência'][1])+"""</th>
            <th>"""+str(redacao_tabela3['Resultado Individual'][1])+"""</th>
            <th>"""+str(redacao_tabela3['Resultado Geral'][1])+"""</th>
            <th>"""+str(redacao_tabela3['Status'][1])+"""</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(redacao_tabela3['Competência'][2])+"""</th>
            <th>"""+str(redacao_tabela3['Resultado Individual'][2])+"""</th>
            <th>"""+str(redacao_tabela3['Resultado Geral'][2])+"""</th>
            <th>"""+str(redacao_tabela3['Status'][2])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(redacao_tabela3['Competência'][3])+"""</th>
            <th>"""+str(redacao_tabela3['Resultado Individual'][3])+"""</th>
            <th>"""+str(redacao_tabela3['Resultado Geral'][3])+"""</th>
            <th>"""+str(redacao_tabela3['Status'][3])+"""</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(redacao_tabela3['Competência'][4])+"""</th>
            <th>"""+str(redacao_tabela3['Resultado Individual'][4])+"""</th>
            <th>"""+str(redacao_tabela3['Resultado Geral'][4])+"""</th>
            <th>"""+str(redacao_tabela3['Status'][4])+"""</th>
          </tr>
        </table>
        """

        html_card_header_melhores_resultados="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Seus melhores resultados</h5>
          </div>
        </div>
        """
        if len(redacao_tabela_verde_ordenado) > 0:
            html_card_header_melhores_resultados1="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(redacao_tabela_verde_ordenado['Competência'][0])+"""</p>
              </div>
            </div>
            """
        if len(redacao_tabela_verde_ordenado) > 1:
            html_card_header_melhores_resultados2="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(redacao_tabela_verde_ordenado['Competência'][1])+"""</p>
              </div>
            </div>
            """
        if len(redacao_tabela_verde_ordenado) > 2:
            html_card_header_melhores_resultados3="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(redacao_tabela_verde_ordenado['Competência'][2])+"""</p>
              </div>
            </div>
            """
        html_card_header_pontos_melhorar="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Pontos que você pode melhorar</h5>
          </div>
        </div>
        """
        if len(redacao_tabela_vermelho_ordenado) > 0:
            html_card_header_pontos_melhorar1="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(redacao_tabela_vermelho_ordenado['Competência'][0])+"""</p>
              </div>
            </div>
            """
        if len(redacao_tabela_vermelho_ordenado) > 1:
            html_card_header_pontos_melhorar2="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(redacao_tabela_vermelho_ordenado['Competência'][1])+"""</p>
              </div>
            </div>
            """
        if len(redacao_tabela_vermelho_ordenado) > 2:
            html_card_header_pontos_melhorar3="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(redacao_tabela_vermelho_ordenado['Competência'][2])+"""</p>
              </div>
            </div>
            """
        with st.container():
            col1, col2, col3, col4 = st.columns([0.5,12,0.5,10.5])
            with col1:
                st.write("")
            with col2:
                st.markdown(html_table, unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header_melhores_resultados, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                if len(redacao_tabela_verde_ordenado) > 0:
                    st.markdown(html_card_header_melhores_resultados1, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(redacao_tabela_verde_ordenado) > 1:
                    st.markdown(html_card_header_melhores_resultados2, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(redacao_tabela_verde_ordenado) > 2:
                    st.markdown(html_card_header_melhores_resultados3, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)

                st.markdown(html_br, unsafe_allow_html=True)
                st.markdown(html_card_header_pontos_melhorar, unsafe_allow_html=True)
                st.markdown(html_br, unsafe_allow_html=True)
                if len(redacao_tabela_vermelho_ordenado) > 0:
                    st.markdown(html_card_header_pontos_melhorar1, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(redacao_tabela_vermelho_ordenado) > 1:
                    st.markdown(html_card_header_pontos_melhorar2, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)
                if len(redacao_tabela_vermelho_ordenado) > 2:
                    st.markdown(html_card_header_pontos_melhorar3, unsafe_allow_html=True)
                    st.markdown(html_br, unsafe_allow_html=True)

        st.markdown(html_br, unsafe_allow_html=True)

    html_subtitle="""
    <h2 style="color:#9E089E; font-family:Georgia;"> DETALHAMENTO POR QUESTÃO
    <hr style= "  display: block;
        margin-top: 0.5em;
        margin-bottom: 0.5em;
        margin-left: auto;
        margin-right: auto;
        border-style: inset;
        border-width: 1.5px;"></h2>
    """
    st.markdown(html_subtitle, unsafe_allow_html=True)
        
        
    tabela_detalhes = base.copy()
        
    for i in range(len(tabela_detalhes['Nome do aluno(a)'])):
        if tabela_detalhes['Resposta do aluno(a)'][i] == 'a':
           tabela_detalhes['Resposta do aluno(a)'][i] = 'A'
        elif tabela_detalhes['Resposta do aluno(a)'][i] == 'b':
            tabela_detalhes['Resposta do aluno(a)'][i] = 'B'
        elif tabela_detalhes['Resposta do aluno(a)'][i] == 'c':
            tabela_detalhes['Resposta do aluno(a)'][i] = 'C'
        elif tabela_detalhes['Resposta do aluno(a)'][i] == 'd':
            tabela_detalhes['Resposta do aluno(a)'][i] = 'D'
        elif tabela_detalhes['Resposta do aluno(a)'][i] == 'e':
            tabela_detalhes['Resposta do aluno(a)'][i] = 'E'
        else:
            tabela_detalhes['Resposta do aluno(a)'][i] = ''

        if tabela_detalhes['Gabarito'][i] == 'a':
            tabela_detalhes['Gabarito'][i] = 'A'
        elif tabela_detalhes['Gabarito'][i] == 'b':
            tabela_detalhes['Gabarito'][i] = 'B'
        elif tabela_detalhes['Gabarito'][i] == 'c':
            tabela_detalhes['Gabarito'][i] = 'C'
        elif tabela_detalhes['Gabarito'][i] == 'd':
            tabela_detalhes['Gabarito'][i] = 'D'
        elif tabela_detalhes['Gabarito'][i] == 'e':
            tabela_detalhes['Gabarito'][i] = 'E'
        else:
            tabela_detalhes['Gabarito'][i] = ''
    tabela_detalhes_fizeram = tabela_detalhes[tabela_detalhes['Nome do aluno(a)'].isin(alunos_fizeram['Nome do aluno(a)'])].reset_index(drop = True)
    tabela_detalhes_aluno = tabela_detalhes[tabela_detalhes['Login do aluno(a)'] == login_aluno]
    tabela_detalhes_aluno2 = tabela_detalhes_aluno.drop(columns = ['Nota na questão','Valor da questão','Nome do aluno(a)','Login do aluno(a)','Certo ou errado'])
    tabela_detalhes_media = tabela_detalhes_fizeram.groupby('Número da questão').mean().reset_index()
    tabela_detalhes_media2 = tabela_detalhes_media.drop(columns = ['Nota na questão','Valor da questão'])

    tabela_detalhes_aluno3 = pd.merge(tabela_detalhes_aluno2, tabela_detalhes_media2, on = 'Número da questão', how = 'inner')
        
    if turma_aluno['Turma'][0] == turma_eng or turma_aluno['Turma'][0] == turma_cien:
        for i in range(len(tabela_detalhes_aluno3['Número da questão'])):
            if tabela_detalhes_aluno3['Número da questão'][i] < 73:
                tabela_detalhes_aluno3['Número da questão'][i] = tabela_detalhes_aluno3['Número da questão'][i] - 24
            if tabela_detalhes_aluno3['Número da questão'][i] > 73:
                tabela_detalhes_aluno3['Número da questão'][i] = tabela_detalhes_aluno3['Número da questão'][i] - 25

        #for i in range(len(tabela_detalhes_aluno3['Número da questão'])):
            #if tabela_detalhes_aluno3['Número da questão'][i] > 90:
            #    tabela_detalhes_aluno3['Número da questão'][i] = tabela_detalhes_aluno3['Número da questão'][i] - 30
    tabela_detalhes_aluno5 = tabela_detalhes_aluno3.drop(columns = ['Nome da avaliação','Turma'])
    tabela_detalhes_aluno4 = tabela_detalhes_aluno5.sort_values(by = 'Número da questão', ascending = True).reset_index()
    cor_back = []
    cor_texto = []
        
    for i in range(len(tabela_detalhes_aluno4['Número da questão'])):
        minutes, seconds= divmod(tabela_detalhes_aluno4['Tempo na questão_x'][i], 60)
        aux1 = str(round(minutes,0)).find('.')
        texto1 = str(round(minutes,0))[0:aux1]
        aux2 = str(round(seconds,0)).find('.')  
        texto2 = str(round(seconds,0))[0:aux2]  
        tabela_detalhes_aluno4['Tempo na questão_x'][i] = texto1+' min '+texto2+' s' 
        minutes, seconds= divmod(tabela_detalhes_aluno4['Tempo na questão_y'][i], 60)
        aux1 = str(round(minutes,0)).find('.')
        texto1 = str(round(minutes,0))[0:aux1]
        aux2 = str(round(seconds,0)).find('.')  
        texto2 = str(round(seconds,0))[0:aux2]  
        tabela_detalhes_aluno4['Tempo na questão_y'][i] = texto1+' min '+texto2+' s' 
        tabela_detalhes_aluno4['Acerto_x'][i] = "{0:.0%}".format(tabela_detalhes_aluno4['Acerto_x'][i])
        tabela_detalhes_aluno4['Acerto_y'][i] = "{0:.0%}".format(tabela_detalhes_aluno4['Acerto_y'][i])
            
        if tabela_detalhes_aluno4['Resposta do aluno(a)'][i] == tabela_detalhes_aluno4['Gabarito'][i]:# or (tabela_detalhes_aluno4['Número da questão'][i] == 73 and tabela_detalhes_aluno4['Acerto_x'][i] > tabela_detalhes_aluno4['Acerto_y'][i]): #tabela_detalhes_aluno4['Acerto_x'][i] == '100%' or tabela_detalhes_aluno4['Acerto_x'][i] > tabela_detalhes_aluno4['Acerto_y'][i]:
            cor_back.append('#a5ffa5')
            cor_texto.append('#008800')
        else:
            cor_back.append('#ffb1b1')
            cor_texto.append('#a80000')
        
    tabela_detalhes_aluno4 = tabela_detalhes_aluno4[['Número da questão','Disciplina','Assunto','Resposta do aluno(a)','Gabarito','Acerto_x','Acerto_y','Tempo na questão_x','Tempo na questão_y']]
    tabela_detalhes_aluno4.rename(columns = {'Disciplina':'Área do conhecimento','Acerto_x':'Resultado Individual','Acerto_y':'Resultado Geral','Tempo na questão_x':'Tempo na questão','Tempo na questão_y':'Média geral'}, inplace = True)
        #tabela_detalhes_aluno5 = tabela_detalhes_aluno4.sort_values(by = 'Número da questão', ascending = True).reset_index()
        
    tabela_final = tabela_questoes(tabela_detalhes_aluno4,'Número da questão','Área do conhecimento','Assunto','Resposta do aluno(a)','Gabarito','Resultado Individual','Resultado Geral','Tempo na questão','Média geral',cor_texto,cor_back)
        
    with st.container():
        col1, col2, col3 = st.columns([0.5, 20, 0.5])
        with col1:
            st.write("")
        with col2:
            st.markdown(tabela_final, unsafe_allow_html=True)
        with col3:
            st.write("")

    html_header_2fase="""
    <h2 style="font-size:200%; color: #9E089E; font-family:Georgia"> 2º FASE<br>
     <hr style= "  display: block;
      margin-top: 0.5em;
      margin-bottom: 0.5em;
      margin-left: auto;
      margin-right: auto;
      border-style: inset;
      border-width: 1.5px;"></h2>
    """
    st.markdown(html_br, unsafe_allow_html=True)
    st.markdown(html_header_2fase, unsafe_allow_html=True)
    
    
    for i in range(len(base_resultados_2fase['Login do aluno(a)'])):
        base_resultados_2fase['Tema 1 - Comunicação assertiva'][i] = float(str(base_resultados_2fase['Tema 1 - Comunicação assertiva'][i]).replace(',','.'))
        base_resultados_2fase['Tema 1 - Interação com pessoas'][i] = float(str(base_resultados_2fase['Tema 1 - Interação com pessoas'][i]).replace(',','.'))
        base_resultados_2fase['Tema 1 - Pensamento crítico'][i] = float(str(base_resultados_2fase['Tema 1 - Pensamento crítico'][i]).replace(',','.'))
        base_resultados_2fase['Tema 1 - Aprender a aprender'][i] = float(str(base_resultados_2fase['Tema 1 - Aprender a aprender'][i]).replace(',','.'))
        base_resultados_2fase['Tema 2 - Comunicação assertiva'][i] = float(str(base_resultados_2fase['Tema 2 - Comunicação assertiva'][i]).replace(',','.'))
        base_resultados_2fase['Tema 2 - Interação com pessoas'][i] = float(str(base_resultados_2fase['Tema 2 - Interação com pessoas'][i]).replace(',','.'))
        base_resultados_2fase['Tema 2 - Pensamento crítico'][i] = float(str(base_resultados_2fase['Tema 2 - Pensamento crítico'][i]).replace(',','.'))
        base_resultados_2fase['Tema 2 - Aprender a aprender'][i] = float(str(base_resultados_2fase['Tema 2 - Aprender a aprender'][i]).replace(',','.'))
        base_resultados_2fase['Tema 3 - Comunicação assertiva'][i] = float(str(base_resultados_2fase['Tema 3 - Comunicação assertiva'][i]).replace(',','.'))
        base_resultados_2fase['Tema 3 - Interação com pessoas'][i] = float(str(base_resultados_2fase['Tema 3 - Interação com pessoas'][i]).replace(',','.'))
        base_resultados_2fase['Tema 3 - Pensamento crítico'][i] = float(str(base_resultados_2fase['Tema 3 - Pensamento crítico'][i]).replace(',','.'))
        base_resultados_2fase['Tema 4 - Comunicação assertiva'][i] = float(str(base_resultados_2fase['Tema 4 - Comunicação assertiva'][i]).replace(',','.'))
        base_resultados_2fase['Tema 4 - Interação com pessoas'][i] = float(str(base_resultados_2fase['Tema 4 - Interação com pessoas'][i]).replace(',','.'))
        base_resultados_2fase['Tema 4 - Pensamento crítico'][i] = float(str(base_resultados_2fase['Tema 4 - Pensamento crítico'][i]).replace(',','.'))
        if base_resultados_2fase['Tema 1 - Comunicação assertiva'][i] > 0:
            base_resultados_2fase['Tema 1 - Comunicação assertiva'][i] = base_resultados_2fase['Tema 1 - Comunicação assertiva'][i]
        else:
            base_resultados_2fase['Tema 1 - Comunicação assertiva'][i] = 0

        if base_resultados_2fase['Tema 1 - Interação com pessoas'][i] > 0:
            base_resultados_2fase['Tema 1 - Interação com pessoas'][i] = base_resultados_2fase['Tema 1 - Interação com pessoas'][i]
        else:
            base_resultados_2fase['Tema 1 - Interação com pessoas'][i] = 0

        if base_resultados_2fase['Tema 1 - Pensamento crítico'][i] > 0:
            base_resultados_2fase['Tema 1 - Pensamento crítico'][i] = base_resultados_2fase['Tema 1 - Pensamento crítico'][i]
        else:
            base_resultados_2fase['Tema 1 - Pensamento crítico'][i] = 0

        if base_resultados_2fase['Tema 1 - Aprender a aprender'][i] > 0:
            base_resultados_2fase['Tema 1 - Aprender a aprender'][i] = base_resultados_2fase['Tema 1 - Aprender a aprender'][i]
        else:
            base_resultados_2fase['Tema 1 - Aprender a aprender'][i] = 0

        if base_resultados_2fase['Tema 2 - Comunicação assertiva'][i] > 0:
            base_resultados_2fase['Tema 2 - Comunicação assertiva'][i] = base_resultados_2fase['Tema 2 - Comunicação assertiva'][i]
        else:
            base_resultados_2fase['Tema 2 - Comunicação assertiva'][i] = 0

        if base_resultados_2fase['Tema 2 - Interação com pessoas'][i] > 0:
            base_resultados_2fase['Tema 2 - Interação com pessoas'][i] = base_resultados_2fase['Tema 2 - Interação com pessoas'][i]
        else:
            base_resultados_2fase['Tema 2 - Interação com pessoas'][i] = 0

        if base_resultados_2fase['Tema 2 - Pensamento crítico'][i] > 0:
            base_resultados_2fase['Tema 2 - Pensamento crítico'][i] = base_resultados_2fase['Tema 2 - Pensamento crítico'][i]
        else:
            base_resultados_2fase['Tema 2 - Pensamento crítico'][i] = 0

        if base_resultados_2fase['Tema 2 - Aprender a aprender'][i] > 0:
            base_resultados_2fase['Tema 2 - Aprender a aprender'][i] = base_resultados_2fase['Tema 2 - Aprender a aprender'][i]
        else:
            base_resultados_2fase['Tema 2 - Aprender a aprender'][i] = 0

        if base_resultados_2fase['Tema 3 - Comunicação assertiva'][i] > 0:
            base_resultados_2fase['Tema 3 - Comunicação assertiva'][i] = base_resultados_2fase['Tema 3 - Comunicação assertiva'][i]
        else:
            base_resultados_2fase['Tema 3 - Comunicação assertiva'][i] = 0

        if base_resultados_2fase['Tema 3 - Interação com pessoas'][i] > 0:
            base_resultados_2fase['Tema 3 - Interação com pessoas'][i] = base_resultados_2fase['Tema 3 - Interação com pessoas'][i]
        else:
            base_resultados_2fase['Tema 3 - Interação com pessoas'][i] = 0

        if base_resultados_2fase['Tema 3 - Pensamento crítico'][i] > 0:
            base_resultados_2fase['Tema 3 - Pensamento crítico'][i] = base_resultados_2fase['Tema 3 - Pensamento crítico'][i]
        else:
            base_resultados_2fase['Tema 3 - Pensamento crítico'][i] = 0

        if base_resultados_2fase['Tema 4 - Comunicação assertiva'][i] > 0:
            base_resultados_2fase['Tema 4 - Comunicação assertiva'][i] = base_resultados_2fase['Tema 4 - Comunicação assertiva'][i]
        else:
            base_resultados_2fase['Tema 4 - Comunicação assertiva'][i] = 0

        if base_resultados_2fase['Tema 4 - Interação com pessoas'][i] > 0:
            base_resultados_2fase['Tema 4 - Interação com pessoas'][i] = base_resultados_2fase['Tema 4 - Interação com pessoas'][i]
        else:
            base_resultados_2fase['Tema 4 - Interação com pessoas'][i] = 0

        if base_resultados_2fase['Tema 4 - Pensamento crítico'][i] > 0:
            base_resultados_2fase['Tema 4 - Pensamento crítico'][i] = base_resultados_2fase['Tema 4 - Pensamento crítico'][i]
        else:
            base_resultados_2fase['Tema 4 - Pensamento crítico'][i] = 0

    base_resultados_2fase['Nota 2º fase'] = 0.00
    base_resultados_2fase['Nota 2º fase'] = (750*base_resultados_2fase['Tema 1 - Comunicação assertiva']/12 + 750*base_resultados_2fase['Tema 1 - Interação com pessoas']/12 + 750*base_resultados_2fase['Tema 1 - Pensamento crítico']/12 + 250*base_resultados_2fase['Tema 1 - Aprender a aprender']/2 + 750*base_resultados_2fase['Tema 2 - Comunicação assertiva']/12 +  750*base_resultados_2fase['Tema 2 - Interação com pessoas']/12 + 750*base_resultados_2fase['Tema 2 - Pensamento crítico']/12 + 250*base_resultados_2fase['Tema 2 - Aprender a aprender']/2 + 750*base_resultados_2fase['Tema 3 - Comunicação assertiva']/12 + 750*base_resultados_2fase['Tema 3 - Interação com pessoas']/12 + 750*base_resultados_2fase['Tema 3 - Pensamento crítico']/12 + 750*base_resultados_2fase['Tema 4 - Comunicação assertiva']/12 + 750*base_resultados_2fase['Tema 4 - Interação com pessoas']/12 + 750*base_resultados_2fase['Tema 4 - Pensamento crítico']/12)/4


    #base_resultados_2fase2 = base_resultados_2fase[base_resultados_2fase['Tema 1 - Comunicação assertiva'] > 0]
    
    ### Resultados gerais do aluno
    base_resultados_2fase = base_resultados_2fase[base_resultados_2fase['Nota 2º fase'] >= 0]
    base_resultados_2faseaux = base_resultados_2fase[base_resultados_2fase['Nota 2º fase'] > 0]
    numero_candidatos = len(base_resultados_2faseaux['Nome do aluno(a)'])

    html_card_header1="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota</h4>
      </div>
    </div>
    """
    html_card_footer1="""
    <div class="card">
      <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota máxima: 1000</p>
      </div>
    </div>
    """

    html_card_footer_med1="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(int(round(base_resultados_2faseaux['Nota 2º fase'].mean(),0)))+"""</p>
      </div>
    </div>
    """
    html_card_header3="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Classificação</h4>
      </div>
    </div>
    """
    html_card_footer3="""
    <div class="card">
      <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos)+"""</p>
      </div>
    </div>
    """
    base_resultados_2fase_aluno = base_resultados_2fase.sort_values(by = 'Nota 2º fase', ascending = False).reset_index(drop = True).reset_index()
    base_resultados_2fase_aluno.rename(columns = {'index':'Classificação'}, inplace = True)

    base_resultados_2fase_aluno2 = base_resultados_2fase_aluno[base_resultados_2fase_aluno['Login do aluno(a)'] == login_aluno].reset_index()
    for i in range(len(base_resultados_2fase_aluno2['Nota 2º fase'])):
        if base_resultados_2fase_aluno2['Nota 2º fase'][i] == 0:
            base_resultados_2fase_aluno2['Classificação'][0] = numero_candidatos + 1
        else:
            base_resultados_2fase_aluno2['Classificação'][0] = base_resultados_2fase_aluno2['Classificação'][0] + 1
    base_resultados_2faseaux = base_resultados_2fase[base_resultados_2fase['Nota 2º fase'] > 0]
    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,20,1,20,1,20,1])
        with col1:
            st.write("")
        with col2:
            st.markdown(html_card_header1, unsafe_allow_html=True)
            fig_c1 = go.Figure(go.Indicator(
                mode="number+delta",
                value=round(base_resultados_2fase_aluno2['Nota 2º fase'].mean(),1),
                number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': int(round(truncar(base_resultados_2faseaux['Nota 2º fase'].mean(),-1),0)), 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c1.update_layout(autosize=False,
                                 width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c1.update_traces(delta_decreasing_color="#FF4136",
                                delta_increasing_color="#3D9970",
                                delta_valueformat='.0f',
                                selector=dict(type='indicator'))
            st.plotly_chart(fig_c1)
            st.markdown(html_card_footer1, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_card_footer_med1, unsafe_allow_html=True)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_card_header3, unsafe_allow_html=True)
            fig_c3 = go.Figure(go.Indicator(
                mode="number",
                value=base_resultados_2fase_aluno2['Classificação'][0],
                number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': 1, 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c3.update_layout(autosize=False,
                                 width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                 delta_increasing_color="#FF4136",
                                 delta_valueformat='.3f',
                                 selector=dict(type='indicator'))
            st.plotly_chart(fig_c3)
            st.markdown(html_card_footer3, unsafe_allow_html=True)
        with col5:
            st.write("")
        with col6:
            st.write("")
        with col7:
            st.write("")
    
    st.markdown(html_br, unsafe_allow_html=True)
    st.markdown(html_br, unsafe_allow_html=True)

    ponto = str(round(100*(numero_candidatos-(base_resultados_2fase_aluno2['Classificação'][0]-1))/numero_candidatos,0)).find('.')
    texto = str(round(100*(numero_candidatos-(base_resultados_2fase_aluno2['Classificação'][0]-1))/numero_candidatos,0))[0:ponto]
    html_card_header_destaques_gerais="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
       height: 150px;">
        <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
      </div>
    </div>
    """    
    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([9,25,2,25,4])
        with col1:
            st.write("")
        with col2:
            # create the bins
            counts, bins = np.histogram(base_resultados_2faseaux['Nota 2º fase'], bins=range(0, 1100, 100))
            bins = 0.5 * (bins[:-1] + bins[1:])
            fig = px.bar(x=bins, y=counts, labels={'x':'Nota no simulado', 'y':'Número de alunos'})
            fig.update_layout(title={'text': "Distribuição de notas", 'x': 0.5}, paper_bgcolor="#FFF0FC", 
                           plot_bgcolor="#FFF0FC", font={'color': "#9E089E", 'size': 14, 'family': "Georgia"}, height=400,
                           width=540,
                           legend=dict(orientation="h",
                                       yanchor="top",
                                       y=0.99,
                                       xanchor="left",
                                       x=0.01),
                           margin=dict(l=1, r=1, b=1, t=30))
            fig.add_vline(x=int(round(base_resultados_2fase_aluno2['Nota 2º fase'].mean(),1)), line_width=7, line_dash="dash", line_color="#9E089E", annotation_text="Você está aqui!", annotation_position="top right")
            fig.add_vline(x=int(round(truncar(base_resultados_2faseaux['Nota 2º fase'].mean(),-1),0)), line_width=7, line_dash="dash", line_color="#01ECEC", annotation_text="Média", annotation_position="top right")
            fig.update_xaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=6, rangemode="tozero",
                          showgrid=False, gridwidth=0.5, gridcolor='#f6f6f6')
            fig.update_yaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=10, rangemode="tozero",
                          showgrid=True, gridwidth=0.5, gridcolor='#f6f6f6')
            fig.update_traces(marker_color='#0010B3')
            st.plotly_chart(fig)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_card_header_destaques_gerais, unsafe_allow_html=True)
        with col5:
            st.write("")

    base_resultados_2fase_debate = pd.DataFrame()
    base_resultados_2fase_debate = base_resultados_2fase
    
    base_resultados_2fase_debate2 = base_resultados_2fase_debate.drop(columns = ['Tema 1 - Aprender a aprender','Tema 2 - Aprender a aprender'])
   
    base_resultados_2fase_debate2['Nota 2º fase'] = 1000*(750*base_resultados_2fase_debate2['Tema 1 - Comunicação assertiva']/12 + 750*base_resultados_2fase_debate2['Tema 1 - Interação com pessoas']/12 + 750*base_resultados_2fase_debate2['Tema 1 - Pensamento crítico']/12 + 750*base_resultados_2fase_debate2['Tema 2 - Comunicação assertiva']/12 +  750*base_resultados_2fase_debate2['Tema 2 - Interação com pessoas']/12 + 750*base_resultados_2fase_debate2['Tema 2 - Pensamento crítico']/12 + 750*base_resultados_2fase_debate2['Tema 3 - Comunicação assertiva']/12 + 750*base_resultados_2fase_debate2['Tema 3 - Interação com pessoas']/12 + 750*base_resultados_2fase_debate2['Tema 3 - Pensamento crítico']/12 + 750*base_resultados_2fase_debate2['Tema 4 - Comunicação assertiva']/12 + 750*base_resultados_2fase_debate2['Tema 4 - Interação com pessoas']/12 + 750*base_resultados_2fase_debate2['Tema 4 - Pensamento crítico']/12)/3000
    base_resultados_2fase_debate2aux = base_resultados_2fase_debate2[base_resultados_2fase_debate2['Nota 2º fase'] > 0]
    html_header_2fase="""
    <h2 style="font-size:200%; color: #9E089E; font-family:Georgia"> DEBATE<br>
     <hr style= "  display: block;
      margin-top: 0.5em;
      margin-bottom: 0.5em;
      margin-left: auto;
      margin-right: auto;
      border-style: inset;
      border-width: 1.5px;"></h2>
    """
    st.markdown(html_br, unsafe_allow_html=True)
    st.markdown(html_header_2fase, unsafe_allow_html=True)

    html_card_header1="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota</h4>
      </div>
    </div>
    """
    html_card_footer1="""
    <div class="card">
      <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota máxima: 1000</p>
      </div>
    </div>
    """

    html_card_footer_med1="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background:#FFA73E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(int(round(base_resultados_2fase_debate2aux['Nota 2º fase'].mean(),0)))+"""</p>
      </div>
    </div>
    """
    html_card_header3="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Classificação</h4>
      </div>
    </div>
    """
    html_card_footer3="""
    <div class="card">
      <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos)+"""</p>
      </div>
    </div>
    """
    base_resultados_2fase_aluno_debate = base_resultados_2fase_debate2.sort_values(by = 'Nota 2º fase', ascending = False).reset_index(drop = True).reset_index()
    base_resultados_2fase_aluno_debate.rename(columns = {'index':'Classificação'}, inplace = True)
    base_resultados_2fase_aluno_debate2 = base_resultados_2fase_aluno_debate[base_resultados_2fase_aluno_debate['Login do aluno(a)'] == login_aluno].reset_index()
    if base_resultados_2fase_aluno_debate2['Nota 2º fase'][0] == 0:
        base_resultados_2fase_aluno_debate2['Classificação'][0] = numero_candidatos + 1
    else:
        base_resultados_2fase_aluno_debate2['Classificação'][0] = base_resultados_2fase_aluno_debate2['Classificação'][0] + 1
    
    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,20,1,20,1,20,1])
        with col1:
            st.write("")
        with col2:
            st.markdown(html_card_header1, unsafe_allow_html=True)
            fig_c1 = go.Figure(go.Indicator(
                mode="number+delta",
                value=round(base_resultados_2fase_aluno_debate2['Nota 2º fase'].mean(),1),
                number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': int(round(truncar(base_resultados_2fase_debate2aux['Nota 2º fase'].mean(),-1),0)), 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c1.update_layout(autosize=False,
                                 width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c1.update_traces(delta_decreasing_color="#FF4136",
                                delta_increasing_color="#3D9970",
                                delta_valueformat='.0f',
                                selector=dict(type='indicator'))
            st.plotly_chart(fig_c1)
            st.markdown(html_card_footer1, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_card_footer_med1, unsafe_allow_html=True)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_card_header3, unsafe_allow_html=True)
            fig_c3 = go.Figure(go.Indicator(
                mode="number",
                value=base_resultados_2fase_aluno_debate2['Classificação'][0],
                number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': 1, 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c3.update_layout(autosize=False,
                                 width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                 delta_increasing_color="#FF4136",
                                 delta_valueformat='.3f',
                                 selector=dict(type='indicator'))
            st.plotly_chart(fig_c3)
            st.markdown(html_card_footer3, unsafe_allow_html=True)
        with col5:
            st.write("")
        with col6:
            st.write("")
        with col7:
            st.write("")
    
    st.markdown(html_br, unsafe_allow_html=True)
    st.markdown(html_br, unsafe_allow_html=True)

    ponto = str(round(100*(numero_candidatos-(base_resultados_2fase_aluno_debate2['Classificação'][0]-1))/numero_candidatos,0)).find('.')
    texto = str(round(100*(numero_candidatos-(base_resultados_2fase_aluno_debate2['Classificação'][0]-1))/numero_candidatos,0))[0:ponto]
    html_card_header_destaques_gerais="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
       height: 150px;">
        <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
      </div>
    </div>
    """    
    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([9,25,2,25,4])
        with col1:
            st.write("")
        with col2:
            # create the bins
            counts, bins = np.histogram(base_resultados_2fase_debate2aux['Nota 2º fase'], bins=range(0, 1100, 100))
            bins = 0.5 * (bins[:-1] + bins[1:])
            fig = px.bar(x=bins, y=counts, labels={'x':'Nota no simulado', 'y':'Número de alunos'})
            fig.update_layout(title={'text': "Distribuição de notas", 'x': 0.5}, paper_bgcolor="#FFF0FC", 
                           plot_bgcolor="#FFF0FC", font={'color': "#9E089E", 'size': 14, 'family': "Georgia"}, height=400,
                           width=540,
                           legend=dict(orientation="h",
                                       yanchor="top",
                                       y=0.99,
                                       xanchor="left",
                                       x=0.01),
                           margin=dict(l=1, r=1, b=1, t=30))
            fig.add_vline(x=int(round(base_resultados_2fase_aluno_debate2['Nota 2º fase'].mean(),1)), line_width=7, line_dash="dash", line_color="#9E089E", annotation_text="Você está aqui!", annotation_position="top right")
            fig.add_vline(x=int(round(truncar(base_resultados_2fase_debate2aux['Nota 2º fase'].mean(),-1),0)), line_width=7, line_dash="dash", line_color="#01ECEC", annotation_text="Média", annotation_position="top right")
            fig.update_xaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=6, rangemode="tozero",
                          showgrid=False, gridwidth=0.5, gridcolor='#f6f6f6')
            fig.update_yaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=10, rangemode="tozero",
                          showgrid=True, gridwidth=0.5, gridcolor='#f6f6f6')
            fig.update_traces(marker_color='#0010B3')
            st.plotly_chart(fig)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_card_header_destaques_gerais, unsafe_allow_html=True)
        with col5:
            st.write("")

    base_resultados_2fase_debate3 = base_resultados_2fase_debate2[base_resultados_2fase_debate2['Login do aluno(a)'] == login_aluno].reset_index()

    data = [
    {'Temas': 'Tema 1',  'Comunicação Assertiva - Resultado Individual': base_resultados_2fase_debate3['Tema 1 - Comunicação assertiva'][0], 'Comunicação Assertiva - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 1 - Comunicação assertiva'].mean(),1), 'Interação com pessoas - Resultado Individual':base_resultados_2fase_debate3['Tema 1 - Interação com pessoas'][0], 'Interação com pessoas - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 1 - Interação com pessoas'].mean(),1), 'Pensamento crítico - Resultado Individual': base_resultados_2fase_debate3['Tema 1 - Pensamento crítico'][0], 'Pensamento crítico - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 1 - Pensamento crítico'].mean(),1)},


    {'Temas': 'Tema 2', 'Comunicação Assertiva - Resultado Individual': base_resultados_2fase_debate3['Tema 2 - Comunicação assertiva'][0], 'Comunicação Assertiva - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 2 - Comunicação assertiva'].mean(),1), 'Interação com pessoas - Resultado Individual':base_resultados_2fase_debate3['Tema 2 - Interação com pessoas'][0], 'Interação com pessoas - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 2 - Interação com pessoas'].mean(),1), 'Pensamento crítico - Resultado Individual': base_resultados_2fase_debate3['Tema 2 - Pensamento crítico'][0], 'Pensamento crítico - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 2 - Pensamento crítico'].mean(),1)}, 


    {'Temas': 'Tema 3', 'Comunicação Assertiva - Resultado Individual': base_resultados_2fase_debate3['Tema 3 - Comunicação assertiva'][0], 'Comunicação Assertiva - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 3 - Comunicação assertiva'].mean(),1), 'Interação com pessoas - Resultado Individual':base_resultados_2fase_debate3['Tema 3 - Interação com pessoas'][0], 'Interação com pessoas - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 3 - Interação com pessoas'].mean(),1), 'Pensamento crítico - Resultado Individual': base_resultados_2fase_debate3['Tema 3 - Pensamento crítico'][0], 'Pensamento crítico - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 3 - Pensamento crítico'].mean(),1)},


    {'Temas': 'Tema 4', 'Comunicação Assertiva - Resultado Individual': base_resultados_2fase_debate3['Tema 4 - Comunicação assertiva'][0], 'Comunicação Assertiva - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 4 - Comunicação assertiva'].mean(),1), 'Interação com pessoas - Resultado Individual':base_resultados_2fase_debate3['Tema 4 - Interação com pessoas'][0], 'Interação com pessoas - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 4 - Interação com pessoas'].mean(),1), 'Pensamento crítico - Resultado Individual': base_resultados_2fase_debate3['Tema 4 - Pensamento crítico'][0], 'Pensamento crítico - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 4 - Pensamento crítico'].mean(),1)},


    {'Temas': 'Total', 'Comunicação Assertiva - Resultado Individual': round((base_resultados_2fase_debate3['Tema 1 - Comunicação assertiva'][0]+base_resultados_2fase_debate3['Tema 2 - Comunicação assertiva'][0]+base_resultados_2fase_debate3['Tema 3 - Comunicação assertiva'][0]+base_resultados_2fase_debate3['Tema 4 - Comunicação assertiva'][0])/4,1), 'Comunicação Assertiva - Resultado Geral': round((base_resultados_2fase_debate2aux['Tema 1 - Comunicação assertiva'].mean() + base_resultados_2fase_debate2aux['Tema 2 - Comunicação assertiva'].mean() + base_resultados_2fase_debate2aux['Tema 3 - Comunicação assertiva'].mean() + base_resultados_2fase_debate2aux['Tema 4 - Comunicação assertiva'].mean())/4,1), 'Interação com pessoas - Resultado Individual': round((base_resultados_2fase_debate3['Tema 1 - Interação com pessoas'][0]+base_resultados_2fase_debate3['Tema 2 - Interação com pessoas'][0]+base_resultados_2fase_debate3['Tema 3 - Interação com pessoas'][0]+base_resultados_2fase_debate3['Tema 4 - Interação com pessoas'][0])/4,1), 'Interação com pessoas - Resultado Geral': round(((base_resultados_2fase_debate2aux['Tema 1 - Interação com pessoas'].mean() + base_resultados_2fase_debate2aux['Tema 2 - Interação com pessoas'].mean() + base_resultados_2fase_debate2aux['Tema 3 - Interação com pessoas'].mean() + base_resultados_2fase_debate2aux['Tema 4 - Interação com pessoas'].mean())/4),1), 'Pensamento crítico - Resultado Individual': round((base_resultados_2fase_debate3['Tema 1 - Pensamento crítico'][0]+base_resultados_2fase_debate3['Tema 2 - Pensamento crítico'][0]+base_resultados_2fase_debate3['Tema 3 - Pensamento crítico'][0]+base_resultados_2fase_debate3['Tema 4 - Pensamento crítico'][0])/4,1), 'Pensamento crítico - Resultado Geral': round((base_resultados_2fase_debate2aux['Tema 1 - Pensamento crítico'].mean() + base_resultados_2fase_debate2aux['Tema 2 - Pensamento crítico'].mean() + base_resultados_2fase_debate2aux['Tema 3 - Pensamento crítico'].mean() + base_resultados_2fase_debate2aux['Tema 4 - Pensamento crítico'].mean())/4,1)}
    ]

    tabela_debate = pd.DataFrame(data)
    cor_back = []
    cor_texto = []
    for i in range(len(tabela_debate)):
        if (tabela_debate['Comunicação Assertiva - Resultado Individual'][i]+ tabela_debate['Interação com pessoas - Resultado Individual'][i] + tabela_debate['Pensamento crítico - Resultado Individual'][i]) > (tabela_debate['Comunicação Assertiva - Resultado Geral'][i] + tabela_debate['Interação com pessoas - Resultado Geral'][i] + tabela_debate['Pensamento crítico - Resultado Geral'][i]):
            cor_back.append('#a5ffa5')
            cor_texto.append('#008800')
        else:
            cor_back.append('#ffb1b1')
            cor_texto.append('#a80000')

    #tabela_detalhes_aluno_debate = tabela_debate.sort_values(by = 'Temas', ascending = True).reset_index()
        
    tabela_final = tabela_questoes_debate(tabela_debate,'Temas', 'Comunicação Assertiva - Resultado Individual', 'Comunicação Assertiva - Resultado Geral', 'Interação com pessoas - Resultado Individual', 'Interação com pessoas - Resultado Geral', 'Pensamento crítico - Resultado Individual', 'Pensamento crítico - Resultado Geral', cor_texto,cor_back)

    tabela_temas_debate = pd.DataFrame()

    tabela_temas_debate['Temas'] = ['Tema 1 -  Empresas devem contratar pessoas que tiveram comportamentos racistas no passado?', 'Tema 2 -  A solução para a crise econômica do sistema público de saúde no Brasil é a parceria privada?', 'Tema 3 - Incentivos fiscais, como a Lei Rouanet, são boas medidas para melhorar a cultura no Brasil?', 'Tema 4 - É correto ter a mesma quantidade de vagas pra mulheres e homens nas faculdades?']

    cor_back_debate = []
    cor_texto_debate = []
    for i in range(len(tabela_temas_debate)):
        cor_back_debate.append('#a5ffa5')
        cor_texto_debate.append('#008800')

    tabela_final_temas_debate = fun_tabela_temas_debate(tabela_temas_debate,'Temas',cor_texto_debate,cor_back_debate)

    with st.container():
            col1, col2, col3 = st.columns([6, 20, 7])
            with col1:
                st.write("")
            with col2:
                st.markdown(tabela_final_temas_debate, unsafe_allow_html=True)
            with col3:
                st.write("")

    st.markdown(html_br, unsafe_allow_html=True)

    with st.container():
            col1, col2, col3 = st.columns([6, 20, 7])
            with col1:
                st.write("")
            with col2:
                st.markdown(tabela_final, unsafe_allow_html=True)
            with col3:
                st.write("")
    

    ### ARGUIÇÃO

    base_resultados_2fase_arguicao = pd.DataFrame()
    base_resultados_2fase_arguicao = base_resultados_2fase
    
    base_resultados_2fase_arguicao2 = base_resultados_2fase_arguicao.drop(columns = ['Tema 1 - Comunicação assertiva','Tema 1 - Interação com pessoas','Tema 1 - Pensamento crítico','Tema 2 - Comunicação assertiva','Tema 2 - Interação com pessoas','Tema 2 - Pensamento crítico','Tema 3 - Comunicação assertiva','Tema 3 - Interação com pessoas','Tema 3 - Pensamento crítico','Tema 4 - Comunicação assertiva','Tema 4 - Interação com pessoas','Tema 4 - Pensamento crítico'])
   
    base_resultados_2fase_arguicao2['Nota 2º fase'] = 125*(base_resultados_2fase_arguicao2['Tema 1 - Aprender a aprender'] + base_resultados_2fase_arguicao2['Tema 2 - Aprender a aprender'])
    base_resultados_2fase_arguicao2aux = base_resultados_2fase_arguicao2[base_resultados_2fase_arguicao2['Nota 2º fase'] > 0]

    html_header_2fase="""
    <h2 style="font-size:200%; color: #9E089E; font-family:Georgia"> ARGUIÇÃO<br>
     <hr style= "  display: block;
      margin-top: 0.5em;
      margin-bottom: 0.5em;
      margin-left: auto;
      margin-right: auto;
      border-style: inset;
      border-width: 1.5px;"></h2>
    """
    st.markdown(html_br, unsafe_allow_html=True)
    st.markdown(html_header_2fase, unsafe_allow_html=True)

    html_card_header1="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota</h4>
      </div>
    </div>
    """
    html_card_footer1="""
    <div class="card">
      <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota máxima: 1000</p>
      </div>
    </div>
    """

    html_card_footer_med1="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(int(round(base_resultados_2fase_arguicao2aux['Nota 2º fase'].mean(),0)))+"""</p>
      </div>
    </div>
    """
    html_card_header3="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Classificação</h4>
      </div>
    </div>
    """
    html_card_footer3="""
    <div class="card">
      <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos)+"""</p>
      </div>
    </div>
    """
    base_resultados_2fase_aluno_arguicao = base_resultados_2fase_arguicao2.sort_values(by = 'Nota 2º fase', ascending = False).reset_index(drop = True).reset_index()
    base_resultados_2fase_aluno_arguicao.rename(columns = {'index':'Classificação'}, inplace = True)

    base_resultados_2fase_aluno_arguicao2 = base_resultados_2fase_aluno_arguicao[base_resultados_2fase_aluno_arguicao['Login do aluno(a)'] == login_aluno].reset_index()

    if base_resultados_2fase_aluno_arguicao2['Nota 2º fase'][0] == 0:
        base_resultados_2fase_aluno_arguicao2['Classificação'][0] = numero_candidatos + 1
    else:
        base_resultados_2fase_aluno_arguicao2['Classificação'][0] = base_resultados_2fase_aluno_arguicao2['Classificação'][0] + 1
    

    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,20,1,20,1,20,1])
        with col1:
            st.write("")
        with col2:
            st.markdown(html_card_header1, unsafe_allow_html=True)
            fig_c1 = go.Figure(go.Indicator(
                mode="number+delta",
                value=round(base_resultados_2fase_aluno_arguicao2['Nota 2º fase'].mean(),1),
                number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': int(round(truncar(base_resultados_2fase_arguicao2aux['Nota 2º fase'].mean(),-1),0)), 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c1.update_layout(autosize=False,
                                 width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c1.update_traces(delta_decreasing_color="#FF4136",
                                delta_increasing_color="#3D9970",
                                delta_valueformat='.0f',
                                selector=dict(type='indicator'))
            st.plotly_chart(fig_c1)
            st.markdown(html_card_footer1, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_card_footer_med1, unsafe_allow_html=True)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_card_header3, unsafe_allow_html=True)
            fig_c3 = go.Figure(go.Indicator(
                mode="number",
                value=base_resultados_2fase_aluno_arguicao2['Classificação'][0],
                number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': 1, 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c3.update_layout(autosize=False,
                                 width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                 delta_increasing_color="#FF4136",
                                 delta_valueformat='.3f',
                                 selector=dict(type='indicator'))
            st.plotly_chart(fig_c3)
            st.markdown(html_card_footer3, unsafe_allow_html=True)
        with col5:
            st.write("")
        with col6:
            st.write("")
        with col7:
            st.write("")
    
    st.markdown(html_br, unsafe_allow_html=True)
    st.markdown(html_br, unsafe_allow_html=True)

    ponto = str(round(100*(numero_candidatos-(base_resultados_2fase_aluno_arguicao2['Classificação'][0]-1))/numero_candidatos,0)).find('.')
    texto = str(round(100*(numero_candidatos-(base_resultados_2fase_aluno_arguicao2['Classificação'][0]-1))/numero_candidatos,0))[0:ponto]
    html_card_header_destaques_gerais="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
       height: 150px;">
        <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
      </div>
    </div>
    """    
    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([9,25,2,25,4])
        with col1:
            st.write("")
        with col2:
            # create the bins
            counts, bins = np.histogram(base_resultados_2fase_arguicao2aux['Nota 2º fase'], bins=range(0, 1100, 100))
            bins = 0.5 * (bins[:-1] + bins[1:])
            fig = px.bar(x=bins, y=counts, labels={'x':'Nota no simulado', 'y':'Número de alunos'})
            fig.update_layout(title={'text': "Distribuição de notas", 'x': 0.5}, paper_bgcolor="#FFF0FC", 
                           plot_bgcolor="#FFF0FC", font={'color': "#9E089E", 'size': 14, 'family': "Georgia"}, height=400,
                           width=540,
                           legend=dict(orientation="h",
                                       yanchor="top",
                                       y=0.99,
                                       xanchor="left",
                                       x=0.01),
                           margin=dict(l=1, r=1, b=1, t=30))
            fig.add_vline(x=int(round(base_resultados_2fase_aluno_arguicao2['Nota 2º fase'].mean(),1)), line_width=7, line_dash="dash", line_color="#9E089E", annotation_text="Você está aqui!", annotation_position="top right")
            fig.add_vline(x=int(round(truncar(base_resultados_2fase_arguicao2aux['Nota 2º fase'].mean(),-1),0)), line_width=7, line_dash="dash", line_color="#01ECEC", annotation_text="Média", annotation_position="top right")
            fig.update_xaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=6, rangemode="tozero",
                          showgrid=False, gridwidth=0.5, gridcolor='#f6f6f6')
            fig.update_yaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=10, rangemode="tozero",
                          showgrid=True, gridwidth=0.5, gridcolor='#f6f6f6')
            fig.update_traces(marker_color='#0010B3')
            st.plotly_chart(fig)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_card_header_destaques_gerais, unsafe_allow_html=True)
        with col5:
            st.write("")

    base_resultados_2fase_arguicao3 = base_resultados_2fase_arguicao2[base_resultados_2fase_arguicao2['Login do aluno(a)'] == login_aluno].reset_index()

    data2 = [
    {'Temas': 'Tema 1',  'Aprender a aprender - Resultado Individual': base_resultados_2fase_arguicao3['Tema 1 - Aprender a aprender'][0], 'Aprender a aprender - Resultado Geral': round(base_resultados_2fase_arguicao2aux['Tema 1 - Aprender a aprender'].mean(),1)},

    {'Temas': 'Tema 2', 'Aprender a aprender - Resultado Individual': base_resultados_2fase_arguicao3['Tema 2 - Aprender a aprender'][0], 'Aprender a aprender - Resultado Geral': round(base_resultados_2fase_arguicao2aux['Tema 2 - Aprender a aprender'].mean(),1)},

    {'Temas': 'Total', 'Aprender a aprender - Resultado Individual': round((base_resultados_2fase_arguicao3['Tema 1 - Aprender a aprender'][0]+base_resultados_2fase_arguicao3['Tema 2 - Aprender a aprender'][0])/2,1), 'Aprender a aprender - Resultado Geral': round((base_resultados_2fase_arguicao2aux['Tema 1 - Aprender a aprender'].mean() + base_resultados_2fase_arguicao2aux['Tema 2 - Aprender a aprender'].mean())/2,1)}
    ]
    tabela_arguicao = pd.DataFrame(data2)
    cor_back = []
    cor_texto = []
    for i in range(len(tabela_arguicao)):
        if (tabela_arguicao['Aprender a aprender - Resultado Individual'][i] > tabela_arguicao['Aprender a aprender - Resultado Geral'][i]):
            cor_back.append('#a5ffa5')
            cor_texto.append('#008800')
        else:
            cor_back.append('#ffb1b1')
            cor_texto.append('#a80000')

    #tabela_detalhes_aluno_debate = tabela_debate.sort_values(by = 'Temas', ascending = True).reset_index()
        
    tabela_final2 = tabela_questoes_arguicao(tabela_arguicao,'Temas', 'Aprender a aprender - Resultado Individual', 'Aprender a aprender - Resultado Geral', cor_texto,cor_back)

    tabela_temas_arguicao = pd.DataFrame()

    tabela_temas_arguicao['Temas'] = ['Tema 1 - Deveria ser instalada inteligência artificial mas casas da população para evitar violência contra mulheres e crianças?','Tema 2 - Assim como o IPVA, as multas de trânsito deveriam ser proporcionais ao valor do veículo?']

    cor_back_arguicao = []
    cor_texto_arguicao = []
    for i in range(len(tabela_temas_arguicao)):
        cor_back_arguicao.append('#a5ffa5')
        cor_texto_arguicao.append('#008800')

    tabela_final_temas_arguicao = fun_tabela_temas_arguicao(tabela_temas_arguicao,'Temas',cor_texto_arguicao,cor_back_arguicao)

    with st.container():
            col1, col2, col3 = st.columns([3, 5 , 3])
            with col1:
                st.write("")
            with col2:
                st.markdown(tabela_final_temas_arguicao, unsafe_allow_html=True)
            with col3:
                st.write("")   

    st.markdown(html_br, unsafe_allow_html=True)

    with st.container():
            col1, col2, col3 = st.columns([3, 5, 3])
            with col1:
                st.write("")
            with col2:
                st.markdown(tabela_final2, unsafe_allow_html=True)
            with col3:
                st.write("")
    
    primeira_fase = resultados_gerais5
    primeira_fase2 = primeira_fase.drop(columns = ['Número da questão','Tempo na questão','Valor da questão','Unnamed: 10','Acerto'])
    segunda_fase = base_resultados_2fase
    
    segunda_fase2 = segunda_fase.drop(columns = ['Tema 1 - Comunicação assertiva','Tema 2 - Comunicação assertiva','Tema 3 - Comunicação assertiva','Tema 4 - Comunicação assertiva', 'Tema 1 - Interação com pessoas', 'Tema 2 - Interação com pessoas', 'Tema 3 - Interação com pessoas', 'Tema 4 - Interação com pessoas', 'Tema 1 - Pensamento crítico', 'Tema 2 - Pensamento crítico', 'Tema 3 - Pensamento crítico', 'Tema 4 - Pensamento crítico', 'Tema 1 - Aprender a aprender', 'Tema 2 - Aprender a aprender']) 
    segunda_fase3 = pd.merge(segunda_fase2, base_redacao_disciplina2, on = 'Login do aluno(a)', how = 'left')
    segunda_fase3.rename(columns = {'Nota na questão':'Nota Redação'}, inplace = True)

    segunda_fase3['Nota Final 2º fase'] = 0.25*segunda_fase3['Nota Redação'] + 0.75*segunda_fase3['Nota 2º fase']
    primeira_fase2.rename(columns = {'Nota na questão':'Nota 1º fase'}, inplace = True)
    

    resultado_final = pd.merge(segunda_fase3, primeira_fase2, on = 'Login do aluno(a)', how = 'left')
    for i in range(len(resultado_final['Login do aluno(a)'])):
        if resultado_final['Nota 1º fase'][i] > 0:
            resultado_final['Nota 1º fase'][i] = resultado_final['Nota 1º fase'][i]
        else:
            resultado_final['Nota 1º fase'][i] = 0
    resultado_final['Nota Final'] = 0.00
    for i in range(len(resultado_final['Login do aluno(a)'])):
        #resultado_final['Nota Final'][i] = sqrt(sqrt(float(resultado_final['Nota 1º fase'][i])*float(resultado_final['Nota 1º fase'][i])*float(resultado_final['Nota 1º fase'][i])*float(resultado_final['Nota 2º fase'][i])))
        resultado_final['Nota Final'][i] = ((resultado_final['Nota 1º fase'][i]**3)*resultado_final['Nota Final 2º fase'][i])**0.25


    html_header_2fase="""
    <h2 style="font-size:200%; color: #9E089E; font-family:Georgia"> RESULTADO FINAL<br>
     <hr style= "  display: block;
      margin-top: 0.5em;
      margin-bottom: 0.5em;
      margin-left: auto;
      margin-right: auto;
      border-style: inset;
      border-width: 1.5px;"></h2>
    """
    st.markdown(html_br, unsafe_allow_html=True)
    st.markdown(html_header_2fase, unsafe_allow_html=True)
    
    resultado_final2 = resultado_final[resultado_final['Nota Final 2º fase'] >= 0]
    
    resultado_finalaux = resultado_final[resultado_final['Nota Final 2º fase'] > 0]
    numero_candidatos = len(resultado_finalaux['Nome do aluno(a)'])

    html_card_header1="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota</h4>
      </div>
    </div>
    """
    html_card_footer1="""
    <div class="card">
      <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota máxima: 1000</p>
      </div>
    </div>
    """

    html_card_footer_med1="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(int(round(resultado_finalaux['Nota Final'].mean(),0)))+"""</p>
      </div>
    </div>
    """
    html_card_header3="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Classificação</h4>
      </div>
    </div>
    """
    html_card_footer3="""
    <div class="card">
      <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
       height: 50px;">
        <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos)+"""</p>
      </div>
    </div>
    """

    resultado_final_aluno = resultado_final.sort_values(by = 'Nota Final', ascending = False).reset_index(drop = True).reset_index()
    resultado_final_aluno.rename(columns = {'level_0':'Classificação'}, inplace = True)

    resultado_final_aluno2 = resultado_final_aluno[resultado_final_aluno['Login do aluno(a)'] == login_aluno].reset_index()
    for i in range(len(resultado_final_aluno2['Nota Final'])):
        if resultado_final_aluno2['Nota Final'][i] == 0:
            resultado_final_aluno2['Classificação'][0] = numero_candidatos + 1
        else:
            resultado_final_aluno2['Classificação'][0] = resultado_final_aluno2['Classificação'][0] + 1

    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,20,1,20,1,20,1])
        with col1:
            st.write("")
        with col2:
            st.markdown(html_card_header1, unsafe_allow_html=True)
            fig_c1 = go.Figure(go.Indicator(
                mode="number+delta",
                value=round(resultado_final_aluno2['Nota Final'].mean(),1),
                number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': int(round(truncar(resultado_finalaux['Nota Final'].mean(),-1),0)), 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c1.update_layout(autosize=False,
                                 width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c1.update_traces(delta_decreasing_color="#FF4136",
                                delta_increasing_color="#3D9970",
                                delta_valueformat='.0f',
                                selector=dict(type='indicator'))
            st.plotly_chart(fig_c1)
            st.markdown(html_card_footer1, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_card_footer_med1, unsafe_allow_html=True)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_card_header3, unsafe_allow_html=True)
            fig_c3 = go.Figure(go.Indicator(
                mode="number",
                value=resultado_final_aluno2['Classificação'][0],
                number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': 1, 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c3.update_layout(autosize=False,
                                 width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                 delta_increasing_color="#FF4136",
                                 delta_valueformat='.3f',
                                 selector=dict(type='indicator'))
            st.plotly_chart(fig_c3)
            st.markdown(html_card_footer3, unsafe_allow_html=True)
        with col5:
            st.write("")
        with col6:
            st.write("")
        with col7:
            st.write("")
    
    st.markdown(html_br, unsafe_allow_html=True)
    st.markdown(html_br, unsafe_allow_html=True)

    ponto = str(round(100*(numero_candidatos-(resultado_final_aluno2['Classificação'][0]-1))/numero_candidatos,0)).find('.')
    texto = str(round(100*(numero_candidatos-(resultado_final_aluno2['Classificação'][0]-1))/numero_candidatos,0))[0:ponto]
    html_card_header_destaques_gerais="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
       height: 150px;">
        <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
      </div>
    </div>
    """    
    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([9,25,2,25,4])
        with col1:
            st.write("")
        with col2:
            # create the bins
            counts, bins = np.histogram(resultado_finalaux['Nota Final'], bins=range(0, 1100, 100))
            bins = 0.5 * (bins[:-1] + bins[1:])
            fig = px.bar(x=bins, y=counts, labels={'x':'Nota no simulado', 'y':'Número de alunos'})
            fig.update_layout(title={'text': "Distribuição de notas", 'x': 0.5}, paper_bgcolor="#FFF0FC", 
                           plot_bgcolor="#FFF0FC", font={'color': "#9E089E", 'size': 14, 'family': "Georgia"}, height=400,
                           width=540,
                           legend=dict(orientation="h",
                                       yanchor="top",
                                       y=0.99,
                                       xanchor="left",
                                       x=0.01),
                           margin=dict(l=1, r=1, b=1, t=30))
            if resultado_final_aluno2['Classificação'][0] <= numero_candidatos:
                fig.add_vline(x=int(round(resultado_final_aluno2['Nota Final'].mean(),1)), line_width=7, line_dash="dash", line_color="#9E089E", annotation_text="Você está aqui!", annotation_position="top right")
            fig.add_vline(x=int(round(truncar(resultado_finalaux['Nota Final'].mean(),-1),0)), line_width=7, line_dash="dash", line_color="#01ECEC", annotation_text="Média", annotation_position="top right")
            fig.update_xaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=6, rangemode="tozero",
                          showgrid=False, gridwidth=0.5, gridcolor='#f6f6f6')
            fig.update_yaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=10, rangemode="tozero",
                          showgrid=True, gridwidth=0.5, gridcolor='#f6f6f6')
            fig.update_traces(marker_color='#0010B3')
            st.plotly_chart(fig)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            st.markdown(html_br, unsafe_allow_html=True)
            if resultado_final_aluno2['Classificação'][0] <= numero_candidatos:
                st.markdown(html_card_header_destaques_gerais, unsafe_allow_html=True)
        with col5:
            st.write("")
    html_final="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #9E089E; padding-top: 20px; padding-bottom: 20px; width: 800px;
       height: 100px;">
        <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Sucesso é o acúmulo de pequenos esforços, repetidos dia e noite. Robert Collier</h5>
      </div>
    </div>
    """ 

    with st.container():
        col1, col2, col3 = st.columns([1,3,2.5])
        with col1:
            st.write("")
        with col2:
            st.markdown(html_final, unsafe_allow_html=True)
        with col3:
            st.write("")
        

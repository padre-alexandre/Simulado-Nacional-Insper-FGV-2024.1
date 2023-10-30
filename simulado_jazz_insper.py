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
from PIL import Image

### Configurando a página

st.set_page_config(page_title="Relatório", page_icon="", layout="wide")
st.markdown('<style>body{background-color: #9E089E}</style>',unsafe_allow_html=True)

local_css("style_nova_id.css")

######################### Banco de Dados ########################
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

#sheet = client.open('Banco de Dados - Relatório Simulado Nacional').sheet1          # Enquanto estiver rodando na nuvem
sheet = client.open('Banco de Dados - Relatório Simulado Nacional - Teste').sheet1   # Enquanto estiver rodando no local

row0 = ['Data e Hora', 'Turma','Nome','Login']

import streamlit as st

@st.cache
def html_header():
    html_header = """
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
    return html_header

@st.cache
def html_card_instagram():
    html_card_instagram="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #c5ffff; padding-top: 12px; width: 280px;
       height: 50px;">
        <p class="card-title" style="background-color:#c5ffff; color:#008181; font-family:Georgia; text-align: center; padding: 0px 0;">Instagram: @jazz_vestibular</p>
      </div>
    </div>
    """
    return html_card_instagram

@st.cache
def html_card_whatsapp():
    html_card_whatsapp="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 280px;
       height: 50px;">
        <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size:16px; font-family:Georgia; text-align: center; padding: 0px 0;">Whatsapp: (32) 99802-5088</p>
      </div>
    </div>
    """
    return html_card_whatsapp

@st.cache
def html_br():
    html_br="""
    <br>
    """
    return html_br

with st.container():
        col1, col2, col3 = st.columns([3,4,3])
        with col1:
            st.markdown(html_br(), unsafe_allow_html=True)
        with col2:
            st.image('[LOGO 3] Jazz.png')
        with col3:
            st.markdown(html_br(), unsafe_allow_html=True)

with st.container():
        col1, col2, col3, col4= st.columns([5, 5, 5, 5])
        with col1:
            st.markdown(html_br(), unsafe_allow_html=True)
        with col2:
            st.markdown(html_card_instagram(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.write("##### [Clique aqui para ver nossa página](https://www.instagram.com/jazz_vestibular/)")
        with col3:
            st.markdown(html_card_whatsapp(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.write("##### [Clique aqui para falar conosco](https://api.whatsapp.com/send?phone=55032998025088)")
        with col4:
            st.markdown(html_br(), unsafe_allow_html=True)

st.markdown(html_header(), unsafe_allow_html=True)

#@st.cache
def leitura_bases_dados():
    base_matriz = pd.read_csv('./matrizquestoes.csv')
    base_resultados = pd.read_csv('./resultado1fase.csv')
    base_resultados_2fase = pd.read_csv('./resultado2fase.csv')

    turma_eng = 'Simulado Nacional Insper 2024.1 - Engenharia'
    turma_cien = 'Simulado Nacional Insper 2024.1 - Ciência da Computação'
    turma_adm = 'Simulado Nacional Insper 2024.1 - Administração'
    turma_eco = 'Simulado Nacional Insper 2024.1 - Economia'
    turma_dir = 'Simulado Nacional Insper 2024.1 - Direito'

    for i in range(len(base_resultados['atividade_nome'])):
        if (base_resultados['turma'][i] == turma_eng or base_resultados['turma'][i] == turma_cien):
            if base_resultados['num_exercicio'][i] < 25:
                base_resultados['num_exercicio'][i] = base_resultados['num_exercicio'][i] + 73
    
    base = pd.merge(base_resultados, base_matriz, on = 'num_exercicio', how = 'inner')

    base.rename(columns = {'atividade_nome':'Nome da avaliação','turma':'Turma','aluno_nome':'Nome do aluno(a)','aluno_login':'Login do aluno(a)','num_exercicio':'Número da questão','resp_aluno':'Resposta do aluno(a)','gabarito':'Gabarito','certo_ou_errado':'Certo ou errado','tempo_no_exercicio(s)':'Tempo na questão','valor_do_exercicio':'Valor da questão','disciplina':'Disciplina','frente':'Frente','assunto':'Assunto'}, inplace = True)
    base['Resposta do aluno(a)'] = base['Resposta do aluno(a)'].fillna('x')
    base['Tempo na questão'] = base['Tempo na questão'].fillna(0)
    base['Valor da questão'] = base['Valor da questão'].apply(lambda x: float(x.replace(".","").replace(",",".")))

    base['Acerto'] = 0.00
    base['Nota na questão'] = 0.00

    for i in range(len(base['Nome da avaliação'])):
        if (base['Certo ou errado'][i] == 'certo' and base['Número da questão'][i] != 73):
            base['Acerto'][i] = 1
            base['Nota na questão'][i] = base['Acerto'][i]*base['Valor da questão'][i]

    resultados_gerais = base.groupby(['Nome da avaliação','Turma','Nome do aluno(a)','Login do aluno(a)']).sum().reset_index()
    
    resultados_gerais2 = resultados_gerais.groupby(['Turma','Nome do aluno(a)','Login do aluno(a)']).sum().reset_index()

    resultados_gerais2_aux = resultados_gerais2.copy()
    for i in range(len(resultados_gerais2_aux['Login do aluno(a)'])):
        #if (resultados_gerais2_aux['Turma'][i] == turma_eng or resultados_gerais2_aux['Turma'][i] == turma_cien):
        #    resultados_gerais2_aux['Nota na questão'][i] = (6/5)*resultados_gerais2_aux['Nota na questão'][i]
        #else:
        resultados_gerais2_aux['Nota na questão'][i] = 1.25*resultados_gerais2_aux['Nota na questão'][i]

    resultados_gerais3 = resultados_gerais2_aux.sort_values(by = 'Nota na questão', ascending = False).reset_index(drop = True)  
    resultados_gerais3["Login do aluno(a)"] = resultados_gerais3["Login do aluno(a)"].apply(extract_login)  

    return resultados_gerais3, turma_eng, turma_cien, base, base_resultados_2fase

login_aluno = st.text_input('Digite o seu login', '')

@st.cache(suppress_st_warning=True)
def fase_1(login_aluno, turma_eng, turma_cien, resultados_gerais3):
    #resultados_gerais3 = leitura_bases_dados()
    resultados_gerais3.to_csv('resultado_compilado.csv')

    nome_aluno3 = resultados_gerais3[resultados_gerais3['Login do aluno(a)'] == login_aluno]['Nome do aluno(a)'].reset_index()
    turma_aluno = resultados_gerais3[resultados_gerais3['Login do aluno(a)'] == login_aluno]['Turma'].reset_index() 

    resultados_gerais_aluno = resultados_gerais3[resultados_gerais3['Nome do aluno(a)'] == nome_aluno3['Nome do aluno(a)'][0]].reset_index()
    resultados_gerais_aluno.rename(columns = {'index':'Classificação'}, inplace = True)
    resultados_gerais_aluno['Classificação'][0] = resultados_gerais_aluno['Classificação'][0] + 1
    
    resultados_gerais_aluno['Tempo na questão2'] = ''

    hours_aluno, minutes = divmod(int(resultados_gerais_aluno['Tempo na questão'][0]), 3600)
    minutes_certo, seconds= divmod(minutes, 60)
    resultados_gerais_aluno['Tempo na questão2'][0] = ' h '+str(minutes_certo)+' min '+str(seconds)+' s'

    resultados_gerais4 = resultados_gerais3[resultados_gerais3['Nota na questão'] > 0]
    resultados_gerais4_aux = resultados_gerais4[['Login do aluno(a)','Número da questão','Tempo na questão','Valor da questão','Acerto','Nota na questão']]
    resultados_gerais5 = resultados_gerais4_aux.copy()
    #resultados_gerais5 = resultados_gerais4.groupby('Login do aluno(a)').mean().reset_index()

    resultados_gerais5['Tempo na questão2'] = ''
    for i in range(len(resultados_gerais5['Tempo na questão'])):
        hours, minutes = divmod(resultados_gerais5['Tempo na questão'][i], 3600)
        minutes_certo, seconds= divmod(minutes, 60)
        resultados_gerais5['Tempo na questão2'][i] = str(hours)+' h '+str(minutes_certo)+' min '+str(seconds)+' s' 

    resultados_gerais_media_tempo = resultados_gerais5['Tempo na questão'].mean()  
    hours_media, minutes_media = divmod(int(resultados_gerais_media_tempo), 3600) 
    minutes_certo_media, seconds_media = divmod(minutes_media, 60)
    resultados_gerais_media_tempo_str = str(hours_media)+' h '+str(minutes_certo_media)+' min '+str(seconds_media)+' s' 

    alunos_fizeram = pd.DataFrame()
    alunos_fizeram['Nome do aluno(a)'] = resultados_gerais4['Nome do aluno(a)']

    ### Resultados gerais do aluno

    numero_candidatos = len(resultados_gerais4['Nome do aluno(a)'])
    aux = resultados_gerais4[resultados_gerais4['Turma'] == turma_eng]
    aux2 = resultados_gerais4[resultados_gerais4['Turma'] == turma_cien]
    numero_eng_cien = len(aux['Nome do aluno(a)']) + len(aux2['Nome do aluno(a)'])

    return resultados_gerais_aluno, resultados_gerais5, numero_candidatos, resultados_gerais4, alunos_fizeram, numero_eng_cien, turma_aluno, resultados_gerais_media_tempo_str, hours_aluno
    
def fase_1_show(resultados_gerais_aluno, resultados_gerais5, numero_candidatos, resultados_gerais4, resultados_gerais_media_tempo_str, hours_aluno):
    
    @st.cache
    def html_header_geral():
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
        return html_header_geral
    
    st.markdown(html_header_geral(), unsafe_allow_html=True)

    @st.cache
    def html_card_header1():
        html_card_header1="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota</h4>
        </div>
        </div>
        """
        return html_card_header1
    
    @st.cache
    def html_card_footer1():
        html_card_footer1="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota máxima: 1000</p>
        </div>
        </div>
        """
        return html_card_footer1
    
    @st.cache
    def html_card_footer_med1(resultados_gerais5):
        html_card_footer_med1="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(int(round(resultados_gerais5['Nota na questão'].mean(),0)))+"""</p>
        </div>
        </div>
        """
        return html_card_footer_med1
    
    @st.cache
    def html_card_header2():
        html_card_header2="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Número de acertos</h4>
        </div>
        </div>
        """
        return html_card_header2
    
    @st.cache
    def html_card_footer2():
        html_card_footer2="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Total de questões: 72</p>
        </div>
        </div>
        """
        return html_card_footer2
    
    @st.cache
    def html_card_footer_med2(resultados_gerais5):
        html_card_footer_med2="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(int(round(resultados_gerais5['Acerto'].mean(),1)))+"""</p>
        </div>
        </div>
        """
        return html_card_footer_med2
    
    @st.cache
    def html_card_header3():
        html_card_header3="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Classificação</h4>
        </div>
        </div>
        """
        return html_card_header3
    
    @st.cache
    def html_card_footer3(numero_candidatos):
        html_card_footer3="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos)+"""</p>
        </div>
        </div>
        """
        return html_card_footer3
    
    @st.cache
    def html_card_header4():
        html_card_header4="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Tempo</h4>
        </div>
        </div>
        """
        return html_card_header4

    @st.cache
    def html_card_footer4(numero_candidatos):
        html_card_footer4="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Duracão: 5 h 15 min</p>
        </div>
        </div>
        """
        return html_card_footer4

    @st.cache
    def html_card_footer_med4(numero_candidatos):
        html_card_footer_med4="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(resultados_gerais_media_tempo_str)+"""</p>
        </div>
        </div>
        """
        return html_card_footer_med4
    
    @st.cache
    def html_card_header4():
        html_card_header4="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Tempo</h4>
        </div>
        </div>
        """
        return html_card_header4

    
    
    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1,20,1,20,1,20,1,20,1])
        with col1:
            st.write("")
        with col2:
            st.markdown(html_card_header1(), unsafe_allow_html=True)
            fig_c1 = go.Figure(go.Indicator(
                mode="number+delta",
                value=round(resultados_gerais_aluno['Nota na questão'][0],1),
                number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais5['Nota na questão'].mean(),-1),0)), 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c1.update_layout(autosize=False,
                                 width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c1.update_traces(delta_decreasing_color="#FF4136",
                                delta_increasing_color="#3D9970",
                                delta_valueformat='.0f',
                                selector=dict(type='indicator'))
            st.plotly_chart(fig_c1)
            st.markdown(html_card_footer1(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_footer_med1(resultados_gerais5), unsafe_allow_html=True)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_card_header2(), unsafe_allow_html=True)
            fig_c2 = go.Figure(go.Indicator(
                mode="number+delta",
                value=round(truncar(resultados_gerais_aluno['Acerto'][0],0),0),
                number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': int(round(resultados_gerais5['Acerto'].mean(),0))},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c2.update_layout(autosize=False,
                                 width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c2.update_traces(delta_decreasing_color="#FF4136",
                                 delta_increasing_color="#3D9970",
                                 delta_valueformat='f',
                                 selector=dict(type='indicator'))
            st.plotly_chart(fig_c2)
            st.markdown(html_card_footer2(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_footer_med2(resultados_gerais5), unsafe_allow_html=True)
        with col5:
            st.write("")
        with col6:
            st.markdown(html_card_header3(), unsafe_allow_html=True)
            fig_c3 = go.Figure(go.Indicator(
                mode="number",
                value=resultados_gerais_aluno['Classificação'][0],
                number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': 1, 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c3.update_layout(autosize=False,
                                 width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                 delta_increasing_color="#FF4136",
                                 delta_valueformat='.3f',
                                 selector=dict(type='indicator'))
            st.plotly_chart(fig_c3)
            st.markdown(html_card_footer3(numero_candidatos), unsafe_allow_html=True)
        with col7:
            st.write("")
        with col8:
            st.markdown(html_card_header4(), unsafe_allow_html=True)
            fig_c2 = go.Figure(go.Indicator(
                mode="number+delta",
                value=hours_aluno,
                number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}, "valueformat": ".0f", "suffix": resultados_gerais_aluno['Tempo na questão2'][0]},
                #delta={'position': "bottom", 'reference': int(round(resultados_gerais5['Acerto'].mean(),0))},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c2.update_layout(autosize=False,
                                 width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c2.update_traces(delta_decreasing_color="#FF4136",
                                 delta_increasing_color="#3D9970",
                                 delta_valueformat='f',
                                 selector=dict(type='indicator'))
            st.plotly_chart(fig_c2)
            st.markdown(html_card_footer4(numero_candidatos), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_footer_med4(numero_candidatos), unsafe_allow_html=True)
        with col9:
            st.write("")
    
    st.markdown(html_br(), unsafe_allow_html=True)
    st.markdown(html_br(), unsafe_allow_html=True)

    ponto = str(round(100*(numero_candidatos-(resultados_gerais_aluno['Classificação'][0]-1))/numero_candidatos,0)).find('.')
    texto = str(round(100*(numero_candidatos-(resultados_gerais_aluno['Classificação'][0]-1))/numero_candidatos,0))[0:ponto]

    @st.cache
    def html_card_header_destaques_gerais(texto):
        html_card_header_destaques_gerais="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
        height: 150px;">
            <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
        </div>
        </div>
        """
        return html_card_header_destaques_gerais
    
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
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            if resultados_gerais_aluno['Classificação'][0] <= numero_candidatos:
                st.markdown(html_card_header_destaques_gerais(texto), unsafe_allow_html=True)
        with col5:
            st.write("")

@st.cache()
def resultados_gerais_disciplina(base, alunos_fizeram):

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
    resultados_gerais_disciplina3["Login do aluno(a)"] = resultados_gerais_disciplina3["Login do aluno(a)"].apply(extract_login)    
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

    return base_alunos_fizeram, resultados_matematica, resultados_gerais_disciplina_med_mat, classificacao_aluno_mat, resultados_gerais_disciplina3_mat, resultados_ciencias_hum, resultados_linguagens, resultados_gerais_disciplina_med_lin, classificacao_aluno_lin, resultados_gerais_disciplina3_lin, resultados_ciencias_fim, resultados_gerais_disciplina_med_cie, classificacao_aluno_fim, resultados_gerais_disciplina3_fim, resultados_gerais_disciplina_med_hum

@st.cache    
def html_disciplinas(resultados_ciencias_hum, resultados_gerais_aluno, turma_eng, turma_cien):

    @st.cache
    def html_card_header1_disc():
        html_card_header1_disc="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota</h4>
        </div>
        </div>
        """
        return html_card_header1_disc
    
    @st.cache
    def html_card_footer1_disc():
        html_card_footer1_disc="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota máxima: 1000</p>
        </div>
        </div>
        """
        return html_card_footer1_disc
    
    @st.cache
    def html_card_footer1_disc_med_mat(resultados_gerais_disciplina_med_mat):
        html_card_footer1_disc_med_mat="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_mat['Nota na questão'].mean(),-1),0)))+"""</p>
        </div>
        </div>
        """
        return html_card_footer1_disc_med_mat
    
    @st.cache
    def html_card_footer1_disc_med_lin(resultados_gerais_disciplina_med_lin):
        html_card_footer1_disc_med_lin="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_lin['Nota na questão'].mean(),-1),0)))+"""</p>
        </div>
        </div>
        """
        return html_card_footer1_disc_med_lin
    
    if len(resultados_ciencias_hum['Nota na questão'] == 0):

        @st.cache
        def html_card_footer1_disc_med_cie(resultados_gerais_disciplina_med_hum):
            html_card_footer1_disc_med_cie="""
            <div class="card">
            <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
            height: 50px;">
                <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_hum['Nota na questão'].mean(),-1),0)))+"""</p>
            </div>
            </div>
            """
            return html_card_footer1_disc_med_cie

    else:

        @st.cache
        def html_card_footer1_disc_med_cie(resultados_gerais_disciplina_med_nat):
            html_card_footer1_disc_med_cie="""
            <div class="card">
            <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
            height: 50px;">
                <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_nat['Nota na questão'].mean(),-1),0)))+"""</p>
            </div>
            </div>
            """
            return html_card_footer1_disc_med_cie
        
    @st.cache
    def html_card_header2_disc():
        html_card_header2_disc="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Número de acertos</h4>
        </div>
        </div>
        """
        return html_card_header2_disc
    
    @st.cache
    def html_card_footer2_disc():
        html_card_footer2_disc="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Total de questões: 24</p>
        </div>
        </div>
        """
        return html_card_footer2_disc
    
    @st.cache
    def html_card_footer2_disc_med_mat(resultados_gerais_disciplina_med_mat):
        html_card_footer2_disc_med_mat="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_mat['Acerto'].mean(),-1),0)))+"""</p>
        </div>
        </div>
        """
        return html_card_footer2_disc_med_mat
    
    @st.cache
    def html_card_footer2_disc_med_lin(resultados_gerais_disciplina_med_lin):
        html_card_footer2_disc_med_lin="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_lin['Acerto'].mean(),-1),0)))+"""</p>
        </div>
        </div>
        """
        return html_card_footer2_disc_med_lin
    
    if resultados_gerais_aluno['Turma'][0] != turma_eng and resultados_gerais_aluno['Turma'][0] != turma_cien:

        @st.cache
        def html_card_footer2_disc_med_cie(resultados_gerais_disciplina_med_hum):
            html_card_footer2_disc_med_cie="""
            <div class="card">
            <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
            height: 50px;">
                <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_hum['Acerto'].mean(),-1),0)))+"""</p>
            </div>
            </div>
            """
            return html_card_footer2_disc_med_cie

    else:

        @st.cache
        def html_card_footer2_disc_med_cie(resultados_gerais_disciplina_med_nat):
            html_card_footer2_disc_med_cie="""
            <div class="card">
            <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
            height: 50px;">
                <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(truncar(resultados_gerais_disciplina_med_nat['Acerto'].mean(),-1),0)))+"""</p>
            </div>
            </div>
            """
            return html_card_footer2_disc_med_cie
        
    @st.cache
    def html_card_header3_disc():
        html_card_header3_disc="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Classificação</h4>
        </div>
        </div>
        """
        return html_card_header3_disc
    
    @st.cache
    def html_card_footer3_disc_matlin():
        html_card_footer3_disc_matlin="""
        <div class="card">
          <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 280px;
           height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos)+"""</p>
          </div>
        </div>
        """
        return html_card_footer3_disc_matlin
    
    if resultados_gerais_aluno['Turma'][0] != turma_eng and resultados_gerais_aluno['Turma'][0] != turma_cien:

        @st.cache
        def html_card_footer3_disc(numero_candidatos, numero_eng_cien):
            html_card_footer3_disc="""
            <div class="card">
            <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 280px;
            height: 50px;">
                <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos-numero_eng_cien)+"""</p>
            </div>
            </div>
            """
            return html_card_footer3_disc

    else:

        @st.cache
        def html_card_footer3_disc(numero_candidatos, numero_eng_cien):
            html_card_footer3_disc="""
            <div class="card">
            <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 280px;
            height: 50px;">
                <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_eng_cien)+"""</p>
            </div>
            </div>
            """
            return html_card_footer3_disc
    
    return html_card_header1_disc, html_card_footer1_disc, html_card_footer1_disc_med_mat, html_card_footer1_disc_med_lin, html_card_footer1_disc_med_cie, html_card_header2_disc, html_card_footer2_disc, html_card_footer2_disc_med_mat, html_card_footer2_disc_med_lin, html_card_footer2_disc_med_cie, html_card_header3_disc, html_card_footer3_disc_matlin, html_card_footer3_disc

@st.cache
def tratamento_dados_mat(base_alunos_fizeram):

    matematica_detalhes = base_alunos_fizeram[base_alunos_fizeram['Disciplina'] == 'Matemática']
    matematica_detalhes_media = matematica_detalhes.groupby(['Assunto']).mean(['Acerto']).reset_index()

    matematica_detalhes["Login do aluno(a)"] = matematica_detalhes["Login do aluno(a)"].apply(extract_login)    
    matematica_aluno = matematica_detalhes[matematica_detalhes['Login do aluno(a)'] == login_aluno]

    matematica_aluno_tempo = 24*matematica_aluno['Tempo na questão'].mean()
    hours_aluno_mat, minutes_aluno = divmod(int(matematica_aluno_tempo), 3600)
    minutes_certo, seconds = divmod(minutes_aluno, 60)
    matematica_aluno_tempo_str = ' h '+str(minutes_certo)+' min '+str(seconds)+' s' 

    matematica_media_tempo = 24*matematica_detalhes['Tempo na questão'].mean()
    hours_mat_media, minutes_mat_media = divmod(int(matematica_media_tempo), 3600)
    minutes_certo, seconds_mat_media = divmod(minutes_mat_media, 60)
    matematica_media_tempo_str = str(hours_mat_media)+' h '+str(minutes_certo)+' min '+str(seconds_mat_media)+' s' 

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

    return matematica_tabela3, matematica_tabela_verde_ordenado, matematica_tabela_vermelho_ordenado, matematica_media_tempo_str, matematica_aluno_tempo_str, hours_aluno_mat

def mat_show(resultados_matematica, resultados_gerais_disciplina_med_mat, classificacao_aluno_mat, resultados_gerais_disciplina3_mat, matematica_media_tempo_str, matematica_aluno_tempo_str, hours_aluno_mat):

    @st.cache
    def html_header_mat():
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
        return html_header_mat
    
    @st.cache
    def html_card_footer_med_mat3():
        html_card_footer_med_mat3="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(matematica_media_tempo_str)+"""</p>
        </div>
        </div>
        """
        return html_card_footer_med_mat3

    @st.cache
    def html_card_footer_duracao3():
        html_card_footer_duracao3="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;"></p>
        </div>
        </div>
        """
        return html_card_footer_duracao3
    
    @st.cache
    def html_card_header4():
        html_card_header4="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Tempo</h4>
        </div>
        </div>
        """
        return html_card_header4

    
    
    if len(resultados_matematica['Nome do aluno(a)']) != 0:

        ### MATEMÁTICA

        st.markdown(html_header_mat(), unsafe_allow_html=True)

        ### Block 1#########################################################################################
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1,20,1,20,1,20,1,20,1])
            with col1:
                st.write("")
            with col2:
                st.markdown(html_card_header1_disc(), unsafe_allow_html=True)
                fig_c1 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=round(resultados_matematica['Nota na questão'][0],1),
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais_disciplina_med_mat['Nota na questão'][0],-1),0)), 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c1.update_layout(autosize=False,
                                     width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                st.plotly_chart(fig_c1)
                st.markdown(html_card_footer1_disc(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_footer1_disc_med_mat(resultados_gerais_disciplina_med_mat), unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header2_disc(), unsafe_allow_html=True)
                fig_c2 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=resultados_matematica['Acerto'][0],
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais_disciplina_med_mat['Acerto'][0],-1),0))},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c2.update_layout(autosize=False,
                                     width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c2.update_traces(delta_decreasing_color="#FF4136",
                                 delta_increasing_color="#3D9970",
                                 delta_valueformat='f',
                                 selector=dict(type='indicator'))
                st.plotly_chart(fig_c2)
                st.markdown(html_card_footer2_disc(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_footer2_disc_med_mat(resultados_gerais_disciplina_med_mat), unsafe_allow_html=True)
            with col5:
                st.write("")
            with col6:
                st.markdown(html_card_header3_disc(), unsafe_allow_html=True)
                fig_c3 = go.Figure(go.Indicator(
                    mode="number",
                    value=classificacao_aluno_mat['index'][0]+1,
                    number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': 1, 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c3.update_layout(autosize=False,
                                     width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                     delta_increasing_color="#FF4136",
                                     delta_valueformat='.3f',
                                     selector=dict(type='indicator'))
                st.plotly_chart(fig_c3)
                st.markdown(html_card_footer3_disc_matlin(), unsafe_allow_html=True)
            with col7:
                st.write("")
            with col8:
                st.markdown(html_card_header4(), unsafe_allow_html=True)
                fig_c2 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=hours_aluno_mat,
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}, "valueformat": ".0f", "suffix": matematica_aluno_tempo_str},
                    #delta={'position': "bottom", 'reference': int(round(resultados_gerais5['Acerto'].mean(),0))},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c2.update_layout(autosize=False,
                                    width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                    paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c2.update_traces(delta_decreasing_color="#FF4136",
                                    delta_increasing_color="#3D9970",
                                    delta_valueformat='f',
                                    selector=dict(type='indicator'))
                st.plotly_chart(fig_c2)
                st.markdown(html_card_footer_duracao3(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_footer_med_mat3(), unsafe_allow_html=True)
            with col9:
                st.write("")

        
        ponto = str(round(100*(numero_candidatos-(classificacao_aluno_mat['index'][0]))/numero_candidatos,0)).find('.')
        texto = str(round(100*(numero_candidatos-(classificacao_aluno_mat['index'][0]))/numero_candidatos,0))[0:ponto] 

        @st.cache
        def html_card_header_destaques_mat(texto):
            html_card_header_destaques_mat="""
            <div class="card">
            <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
            height: 150px;">
                <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
            </div>
            </div>
            """ 
            return html_card_header_destaques_mat

        st.markdown(html_br(), unsafe_allow_html=True)
        st.markdown(html_br(), unsafe_allow_html=True)

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
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_header_destaques_mat(texto), unsafe_allow_html=True)
            with col5:
                st.write("")

        st.markdown(html_br(), unsafe_allow_html=True)

@st.cache
def html_mat(matematica_tabela3, matematica_tabela_verde_ordenado, matematica_tabela_vermelho_ordenado):

    @st.cache
    def html_table(matematica_tabela3):
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
            <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][13])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][13])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][13])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][13])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][13])+"""</th>
          </tr>
          <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][14])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][14])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][14])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][14])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][14])+"""</th>
          </tr>
          <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
            <th>"""+str(matematica_tabela3['Assunto'][15])+"""</th>
            <th>"""+str(matematica_tabela3['Quantidade de questões'][15])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Individual'][15])+"""</th>
            <th>"""+str(matematica_tabela3['Resultado Geral'][15])+"""</th>
            <th>"""+str(matematica_tabela3['Status'][15])+"""</th>
          </tr>
        </table>
        """
        return html_table
    
    @st.cache
    def html_card_header_melhores_resultados():
        html_card_header_melhores_resultados="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Seus melhores resultados</h5>
          </div>
        </div>
        """
        return html_card_header_melhores_resultados
    
    html_card_header_melhores_resultados1 = ""
    if len(matematica_tabela_verde_ordenado) > 0:

        @st.cache
        def html_card_header_melhores_resultados1(matematica_tabela_verde_ordenado):
            html_card_header_melhores_resultados1="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(matematica_tabela_verde_ordenado['Assunto'][0])+"""</p>
              </div>
            </div>
            """
            return html_card_header_melhores_resultados1
    
    html_card_header_melhores_resultados2 = ""
    if len(matematica_tabela_verde_ordenado) > 1:

        @st.cache
        def html_card_header_melhores_resultados2(matematica_tabela_verde_ordenado):
            html_card_header_melhores_resultados2="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(matematica_tabela_verde_ordenado['Assunto'][1])+"""</p>
              </div>
            </div>
            """
            return html_card_header_melhores_resultados2
    
    html_card_header_melhores_resultados3 = ""
    if len(matematica_tabela_verde_ordenado) > 2:

        @st.cache
        def html_card_header_melhores_resultados3(matematica_tabela_verde_ordenado):
            html_card_header_melhores_resultados3="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(matematica_tabela_verde_ordenado['Assunto'][2])+"""</p>
              </div>
            </div>
            """
            return html_card_header_melhores_resultados3
    
    @st.cache
    def html_card_header_pontos_melhorar():
        html_card_header_pontos_melhorar="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Pontos que você pode melhorar</h5>
          </div>
        </div>
        """
        return html_card_header_pontos_melhorar
    
    html_card_header_pontos_melhorar1 = ""
    if len(matematica_tabela_vermelho_ordenado) > 0:

        @st.cache
        def html_card_header_pontos_melhorar1(matematica_tabela_vermelho_ordenado):
            html_card_header_pontos_melhorar1="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(matematica_tabela_vermelho_ordenado['Assunto'][0])+"""</p>
              </div>
            </div>
            """
            return html_card_header_pontos_melhorar1
    
    html_card_header_pontos_melhorar2 = ""
    if len(matematica_tabela_vermelho_ordenado) > 1:

        @st.cache
        def html_card_header_pontos_melhorar2(matematica_tabela_vermelho_ordenado):
            html_card_header_pontos_melhorar2="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(matematica_tabela_vermelho_ordenado['Assunto'][1])+"""</p>
              </div>
            </div>
            """
            return html_card_header_pontos_melhorar2
    
    html_card_header_pontos_melhorar3 = ""
    if len(matematica_tabela_vermelho_ordenado) > 2:

        @st.cache
        def html_card_header_pontos_melhorar3(matematica_tabela_vermelho_ordenado):
            html_card_header_pontos_melhorar3="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(matematica_tabela_vermelho_ordenado['Assunto'][2])+"""</p>
              </div>
            </div>
            """
            return html_card_header_pontos_melhorar3
    
    return html_table, html_card_header_melhores_resultados, html_card_header_melhores_resultados1, html_card_header_melhores_resultados2, html_card_header_melhores_resultados3, html_card_header_pontos_melhorar, html_card_header_pontos_melhorar1, html_card_header_pontos_melhorar2, html_card_header_pontos_melhorar3
    
def mat_show2():

    with st.container():
            col1, col2, col3, col4 = st.columns([0.5,12,0.5,10.5])
            with col1:
                st.write("")
            with col2:
                st.markdown(html_table(matematica_tabela3), unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header_melhores_resultados(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                if len(matematica_tabela_verde_ordenado) > 0:
                    st.markdown(html_card_header_melhores_resultados1(matematica_tabela_verde_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)
                if len(matematica_tabela_verde_ordenado) > 1:
                    st.markdown(html_card_header_melhores_resultados2(matematica_tabela_verde_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)
                if len(matematica_tabela_verde_ordenado) > 2:
                    st.markdown(html_card_header_melhores_resultados3(matematica_tabela_verde_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)

                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_header_pontos_melhorar(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                if len(matematica_tabela_vermelho_ordenado) > 0:
                    st.markdown(html_card_header_pontos_melhorar1(matematica_tabela_vermelho_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)
                if len(matematica_tabela_vermelho_ordenado) > 1:
                    st.markdown(html_card_header_pontos_melhorar2(matematica_tabela_vermelho_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)
                if len(matematica_tabela_vermelho_ordenado) > 2:
                    st.markdown(html_card_header_pontos_melhorar3(matematica_tabela_vermelho_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)

    st.markdown(html_br(), unsafe_allow_html=True)    

@st.cache
def tratamento_dados_lin(base_alunos_fizeram):

    linguagens_detalhes = base_alunos_fizeram[base_alunos_fizeram['Disciplina'] == 'Linguagens']

    linguagens_detalhes_media = linguagens_detalhes.groupby(['Assunto']).mean(['Acerto']).reset_index()

    linguagens_detalhes["Login do aluno(a)"] = linguagens_detalhes["Login do aluno(a)"].apply(extract_login) 
    linguagens_aluno = linguagens_detalhes[linguagens_detalhes['Login do aluno(a)'] == login_aluno]

    linguagens_aluno_tempo = 24*linguagens_aluno['Tempo na questão'].mean()

    hours_aluno_lin, minutes_aluno = divmod(int(linguagens_aluno_tempo), 3600)
    minutes_certo, seconds = divmod(minutes_aluno, 60)
    linguagens_aluno_tempo_str = ' h '+str(minutes_certo)+' min '+str(seconds)+' s' 

    linguagens_media_tempo = 24*linguagens_detalhes['Tempo na questão'].mean()
    hours_lin_media, minutes_lin_media = divmod(int(linguagens_media_tempo), 3600)
    minutes_certo, seconds_mat_media = divmod(minutes_lin_media, 60)
    linguagens_media_tempo_str = str(hours_lin_media)+' h '+str(minutes_certo)+' min '+str(seconds_mat_media)+' s'

    linguagens_detalhes["Login do aluno(a)"] = linguagens_detalhes["Login do aluno(a)"].apply(extract_login)    
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
    
    return linguagens_tabela3, linguagens_tabela_verde_ordenado, linguagens_tabela_vermelho_ordenado, linguagens_media_tempo_str, hours_aluno_lin, linguagens_aluno_tempo_str
  
def lin_show(resultados_linguagens, resultados_gerais_disciplina_med_lin, classificacao_aluno_lin, resultados_gerais_disciplina3_lin, linguagens_media_tempo_str, hours_aluno_lin, linguagens_aluno_tempo_str):

    @st.cache
    def html_header_lin():
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
        return html_header_lin
    
    @st.cache
    def html_card_footer_med_lin3(linguagens_media_tempo_str):
        html_card_footer_med_lin3="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(linguagens_media_tempo_str)+"""</p>
        </div>
        </div>
        """
        return html_card_footer_med_lin3

    @st.cache
    def html_card_footer_duracao3():
        html_card_footer_duracao3="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;"></p>
        </div>
        </div>
        """
        return html_card_footer_duracao3

    @st.cache
    def html_card_header4():
        html_card_header4="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Tempo</h4>
        </div>
        </div>
        """
        return html_card_header4
    
    if len(resultados_linguagens['Nome do aluno(a)']) != 0:

        ### LINGUAGENS

        st.markdown(html_header_lin(), unsafe_allow_html=True)

        ### Block 1#########################################################################################
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1,20,1,20,1,20,1,20,1])
            with col1:
                st.write("")
            with col2:
                st.markdown(html_card_header1_disc(), unsafe_allow_html=True)
                fig_c1 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=round(resultados_linguagens['Nota na questão'][0],1),
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais_disciplina_med_lin['Nota na questão'][0],-1),0)), 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c1.update_layout(autosize=False,
                                     width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                st.plotly_chart(fig_c1)
                st.markdown(html_card_footer1_disc(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_footer1_disc_med_mat(resultados_gerais_disciplina_med_lin), unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header2_disc(), unsafe_allow_html=True)
                fig_c2 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=resultados_linguagens['Acerto'][0],
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais_disciplina_med_lin['Acerto'][0],-1),0))},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c2.update_layout(autosize=False,
                                     width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c2.update_traces(delta_decreasing_color="#FF4136",
                                 delta_increasing_color="#3D9970",
                                 delta_valueformat='f',
                                 selector=dict(type='indicator'))
                st.plotly_chart(fig_c2)
                st.markdown(html_card_footer2_disc(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_footer2_disc_med_mat(resultados_gerais_disciplina_med_lin), unsafe_allow_html=True)
            with col5:
                st.write("")
            with col6:
                st.markdown(html_card_header3_disc(), unsafe_allow_html=True)
                fig_c3 = go.Figure(go.Indicator(
                    mode="number",
                    value=classificacao_aluno_lin['index'][0]+1,
                    number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': 1, 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c3.update_layout(autosize=False,
                                     width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                     delta_increasing_color="#FF4136",
                                     delta_valueformat='.3f',
                                     selector=dict(type='indicator'))
                st.plotly_chart(fig_c3)
                st.markdown(html_card_footer3_disc_matlin(), unsafe_allow_html=True)
            with col7:
                st.write("")
            with col8:
                st.markdown(html_card_header4(), unsafe_allow_html=True)
                fig_c2 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=hours_aluno_lin,
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}, "valueformat": ".0f", "suffix": linguagens_aluno_tempo_str},
                    #delta={'position': "bottom", 'reference': int(round(resultados_gerais5['Acerto'].mean(),0))},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c2.update_layout(autosize=False,
                                    width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                    paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c2.update_traces(delta_decreasing_color="#FF4136",
                                    delta_increasing_color="#3D9970",
                                    delta_valueformat='f',
                                    selector=dict(type='indicator'))
                st.plotly_chart(fig_c2)
                st.markdown(html_card_footer_duracao3(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_footer_med_lin3(linguagens_media_tempo_str), unsafe_allow_html=True)
            with col9:
                st.write("")
        
        ponto = str(round(100*(numero_candidatos-(classificacao_aluno_lin['index'][0]))/numero_candidatos,0)).find('.')
        texto = str(round(100*(numero_candidatos-(classificacao_aluno_lin['index'][0]))/numero_candidatos,0))[0:ponto] 

        @st.cache
        def html_card_header_destaques_lin(texto):
            html_card_header_destaques_lin="""
            <div class="card">
            <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
            height: 150px;">
                <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
            </div>
            </div>
            """ 
            return html_card_header_destaques_lin

        st.markdown(html_br(), unsafe_allow_html=True)
        st.markdown(html_br(), unsafe_allow_html=True)

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
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_header_destaques_lin(texto), unsafe_allow_html=True)
            with col5:
                st.write("")

        st.markdown(html_br(), unsafe_allow_html=True)

@st.cache
def html_lin(linguagens_tabela3, linguagens_tabela_verde_ordenado, linguagens_tabela_vermelho_ordenado):

    @st.cache
    def html_table(linguagens_tabela3):
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
        </table>
        """
        return html_table
    
    @st.cache
    def html_card_header_melhores_resultados():
        html_card_header_melhores_resultados="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Seus melhores resultados</h5>
          </div>
        </div>
        """
        return html_card_header_melhores_resultados
    
    html_card_header_melhores_resultados1 = ""
    if len(linguagens_tabela_verde_ordenado) > 0:

        @st.cache
        def html_card_header_melhores_resultados1(linguagens_tabela_verde_ordenado):
            html_card_header_melhores_resultados1="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(linguagens_tabela_verde_ordenado['Assunto'][0])+"""</p>
              </div>
            </div>
            """
            return html_card_header_melhores_resultados1
    
    html_card_header_melhores_resultados2 = ""
    if len(linguagens_tabela_verde_ordenado) > 1:

        @st.cache
        def html_card_header_melhores_resultados2(linguagens_tabela_verde_ordenado):
            html_card_header_melhores_resultados2="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(linguagens_tabela_verde_ordenado['Assunto'][1])+"""</p>
              </div>
            </div>
            """
            return html_card_header_melhores_resultados2
    
    html_card_header_melhores_resultados3 = ""
    if len(linguagens_tabela_verde_ordenado) > 2:

        @st.cache
        def html_card_header_melhores_resultados3(linguagens_tabela_verde_ordenado):
            html_card_header_melhores_resultados3="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(linguagens_tabela_verde_ordenado['Assunto'][2])+"""</p>
              </div>
            </div>
            """
            return html_card_header_melhores_resultados3
    
    @st.cache
    def html_card_header_pontos_melhorar():
        html_card_header_pontos_melhorar="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Pontos que você pode melhorar</h5>
          </div>
        </div>
        """
        return html_card_header_pontos_melhorar
    
    html_card_header_pontos_melhorar1 = ""
    if len(linguagens_tabela_vermelho_ordenado) > 0:

        @st.cache
        def html_card_header_pontos_melhorar1(linguagens_tabela_vermelho_ordenado):
            html_card_header_pontos_melhorar1="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(linguagens_tabela_vermelho_ordenado['Assunto'][0])+"""</p>
              </div>
            </div>
            """
            return html_card_header_pontos_melhorar1
    
    html_card_header_pontos_melhorar2 = ""
    if len(linguagens_tabela_vermelho_ordenado) > 1:

        @st.cache
        def html_card_header_pontos_melhorar2(linguagens_tabela_vermelho_ordenado):
            html_card_header_pontos_melhorar2="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(linguagens_tabela_vermelho_ordenado['Assunto'][1])+"""</p>
              </div>
            </div>
            """
            return html_card_header_pontos_melhorar2
    
    html_card_header_pontos_melhorar3 = ""
    if len(linguagens_tabela_vermelho_ordenado) > 2:

        @st.cache
        def html_card_header_pontos_melhorar3(linguagens_tabela_vermelho_ordenado):
            html_card_header_pontos_melhorar3="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(linguagens_tabela_vermelho_ordenado['Assunto'][2])+"""</p>
              </div>
            </div>
            """
            return html_card_header_pontos_melhorar3
    
    return html_table, html_card_header_melhores_resultados, html_card_header_melhores_resultados1, html_card_header_melhores_resultados2, html_card_header_melhores_resultados3, html_card_header_pontos_melhorar, html_card_header_pontos_melhorar1, html_card_header_pontos_melhorar2, html_card_header_pontos_melhorar3
           
def lin_show2():

    with st.container():
            col1, col2, col3, col4 = st.columns([0.5,12,0.5,10.5])
            with col1:
                st.write("")
            with col2:
                st.markdown(html_table(linguagens_tabela3), unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header_melhores_resultados(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                if len(linguagens_tabela_verde_ordenado) > 0:
                    st.markdown(html_card_header_melhores_resultados1(linguagens_tabela_verde_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)
                if len(linguagens_tabela_verde_ordenado) > 1:
                    st.markdown(html_card_header_melhores_resultados2(linguagens_tabela_verde_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)
                if len(linguagens_tabela_verde_ordenado) > 2:
                    st.markdown(html_card_header_melhores_resultados3(linguagens_tabela_verde_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)

                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_header_pontos_melhorar(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                if len(linguagens_tabela_vermelho_ordenado) > 0:
                    st.markdown(html_card_header_pontos_melhorar1(linguagens_tabela_vermelho_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)
                if len(linguagens_tabela_vermelho_ordenado) > 1:
                    st.markdown(html_card_header_pontos_melhorar2(linguagens_tabela_vermelho_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)
                if len(linguagens_tabela_vermelho_ordenado) > 2:
                    st.markdown(html_card_header_pontos_melhorar3(linguagens_tabela_vermelho_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)

    st.markdown(html_br(), unsafe_allow_html=True)    

@st.cache
def tratamento_dados_cie(base_alunos_fizeram, resultados_gerais_aluno):

    if resultados_gerais_aluno['Turma'][0] != turma_eng and resultados_gerais_aluno['Turma'][0] != turma_cien:
        ciencias_detalhes = base_alunos_fizeram[base_alunos_fizeram['Disciplina'] == 'Ciências Humanas']
    else:
        ciencias_detalhes = base_alunos_fizeram[base_alunos_fizeram['Disciplina'] == 'Ciências da Natureza']
    
    ciencias_detalhes_media = ciencias_detalhes.groupby('Assunto').mean(['Acerto']).reset_index()
    ciencias_detalhes["Login do aluno(a)"] = ciencias_detalhes["Login do aluno(a)"].apply(extract_login) 
    ciencias_aluno = ciencias_detalhes[ciencias_detalhes['Login do aluno(a)'] == login_aluno]

    ciencias_aluno_tempo = 24*ciencias_aluno['Tempo na questão'].mean()
    hours_aluno_cie, minutes_aluno = divmod(int(ciencias_aluno_tempo), 3600)
    minutes_certo, seconds = divmod(minutes_aluno, 60)
    ciencias_aluno_tempo_str = ' h '+str(minutes_certo)+' min '+str(seconds)+' s' 

    ciencias_media_tempo = 24*ciencias_detalhes['Tempo na questão'].mean()
    hours_cie_media, minutes_cie_media = divmod(int(ciencias_media_tempo), 3600)
    minutes_certo, seconds_cie_media = divmod(minutes_cie_media, 60)
    ciencias_media_tempo_str = str(hours_cie_media)+' h '+str(minutes_certo)+' min '+str(seconds_cie_media)+' s'

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

    return ciencias_tabela3, ciencias_tabela_verde_ordenado, ciencias_tabela_vermelho_ordenado, hours_aluno_cie, ciencias_aluno_tempo_str, ciencias_media_tempo_str

def cie_show(resultados_ciencias_fim, resultados_gerais_disciplina_med_cie, classificacao_aluno_fim, resultados_gerais_disciplina3_fim, numero_eng_cien, turma_eng, turma_cien, numero_candidatos, hours_aluno_cie, ciencias_aluno_tempo_str, ciencias_media_tempo_str):

    @st.cache
    def html_header_hum():
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
        return html_header_hum
    
    @st.cache
    def html_header_nat():
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
        return html_header_nat
    
    @st.cache
    def html_card_footer_duracao3():
        html_card_footer_duracao3="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(ciencias_media_tempo_str)+"""</p>
        </div>
        </div>
        """
        return html_card_footer_duracao3
    
    @st.cache
    def html_card_header4():
        html_card_header4="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Tempo</h4>
        </div>
        </div>
        """
        return html_card_header4
    
    @st.cache
    def html_card_footer4():
        html_card_footer4="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;"></p>
        </div>
        </div>
        """
        return html_card_footer4
    
    if len(resultados_ciencias_hum['Disciplina']) == 0:
        st.markdown(html_header_nat(), unsafe_allow_html=True)
    else:
        st.markdown(html_header_hum(), unsafe_allow_html=True)

        ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1,20,1,20,1,20,1,20,1])
        with col1:
            st.write("")
        with col2:
            st.markdown(html_card_header1_disc(), unsafe_allow_html=True)
            fig_c1 = go.Figure(go.Indicator(
                mode="number+delta",
                value=round(resultados_ciencias_fim['Nota na questão'][0],1),
                number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais_disciplina_med_cie['Nota na questão'][0],-1),0)), 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c1.update_layout(autosize=False,
                                    width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                    paper_bgcolor="#FFF0FC", font={'size': 20})
            st.plotly_chart(fig_c1)
            st.markdown(html_card_footer1_disc(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_footer1_disc_med_cie(resultados_gerais_disciplina_med_hum), unsafe_allow_html=True)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_card_header2_disc(), unsafe_allow_html=True)
            fig_c2 = go.Figure(go.Indicator(
                mode="number+delta",
                value=resultados_ciencias_fim['Acerto'][0],
                number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': int(round(truncar(resultados_gerais_disciplina_med_cie['Acerto'][0],-1),0))},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c2.update_layout(autosize=False,
                                    width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                    paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c2.update_traces(delta_decreasing_color="#FF4136",
                                delta_increasing_color="#3D9970",
                                delta_valueformat='f',
                                selector=dict(type='indicator'))
            st.plotly_chart(fig_c2)
            st.markdown(html_card_footer2_disc(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_footer2_disc_med_cie(resultados_gerais_disciplina_med_hum), unsafe_allow_html=True)
        with col5:
            st.write("")
        with col6:
            st.markdown(html_card_header3_disc(), unsafe_allow_html=True)
            fig_c3 = go.Figure(go.Indicator(
                mode="number",
                value=classificacao_aluno_fim['index'][0]+1,
                number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': 1, 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c3.update_layout(autosize=False,
                                    width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                    paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                    delta_increasing_color="#FF4136",
                                    delta_valueformat='.3f',
                                    selector=dict(type='indicator'))
            st.plotly_chart(fig_c3)
            st.markdown(html_card_footer3_disc(numero_candidatos, numero_eng_cien), unsafe_allow_html=True)
        with col7:
            st.write("")
        with col8:
                st.markdown(html_card_header4(), unsafe_allow_html=True)
                fig_c2 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=hours_aluno_cie,
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}, "valueformat": ".0f", "suffix": ciencias_aluno_tempo_str},
                    #delta={'position': "bottom", 'reference': int(round(resultados_gerais5['Acerto'].mean(),0))},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c2.update_layout(autosize=False,
                                    width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                    paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c2.update_traces(delta_decreasing_color="#FF4136",
                                    delta_increasing_color="#3D9970",
                                    delta_valueformat='f',
                                    selector=dict(type='indicator'))
                st.plotly_chart(fig_c2)
                st.markdown(html_card_footer4(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_footer_duracao3(), unsafe_allow_html=True)
        with col9:
                st.write("")

    st.markdown(html_br(), unsafe_allow_html=True)
    if resultados_gerais_aluno['Turma'][0] != turma_eng and resultados_gerais_aluno['Turma'][0] != turma_cien:
        ponto = str(round(100*((numero_candidatos-numero_eng_cien)-(classificacao_aluno_fim['index'][0]))/(numero_candidatos-numero_eng_cien),0)).find('.')
        texto = str(round(100*((numero_candidatos-numero_eng_cien)-(classificacao_aluno_fim['index'][0]))/(numero_candidatos-numero_eng_cien),0))[0:ponto]
    else:
        ponto = str(round(100*((numero_eng_cien)-(classificacao_aluno_fim['index'][0]))/(numero_eng_cien),0)).find('.')
        texto = str(round(100*((numero_eng_cien)-(classificacao_aluno_fim['index'][0]))/(numero_eng_cien),0))[0:ponto]
    
    @st.cache
    def html_card_header_destaques_cie(texto):
        html_card_header_destaques_cie="""
    <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
        height: 150px;">
        <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
        </div>
    </div>
     """
        return html_card_header_destaques_cie

      

    st.markdown(html_br(), unsafe_allow_html=True)

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
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_header_destaques_cie(texto), unsafe_allow_html=True)
        with col5:
            st.write("")

@st.cache
def html_cie(ciencias_tabela3, turma_aluno, turma_eng, turma_cien, ciencias_tabela_verde_ordenado, ciencias_tabela_vermelho_ordenado):

    html_table_cie_hum = ""
    html_table_cie_nat = ""
    if turma_aluno['Turma'][0] != turma_eng and turma_aluno['Turma'][0] != turma_cien:
            
        @st.cache
        def html_table_cie_hum(ciencias_tabela3):
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
                        <tr style="background-color:#f7d4f0; height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][21])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][21])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][21])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][21])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][21])+"""</th>
            </tr>
            <tr style="height: 42px; color:#C81F6D; font-size: 16px;text-align: center">
                <th>"""+str(ciencias_tabela3['Assunto'][22])+"""</th>
                <th>"""+str(ciencias_tabela3['Quantidade de questões'][22])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Individual'][22])+"""</th>
                <th>"""+str(ciencias_tabela3['Resultado Geral'][22])+"""</th>
                <th>"""+str(ciencias_tabela3['Status'][22])+"""</th>
            </tr>
            </table>
            """
            return html_table_cie_hum
            
    else:
        
        @st.cache
        def html_table_cie_nat(ciencias_tabela3):
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
            </table>
            """
            return html_table_cie_nat
            
    @st.cache
    def html_card_header_melhores_resultados_cie():
        html_card_header_melhores_resultados_cie="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Seus melhores resultados</h5>
          </div>
        </div>
        """
        return html_card_header_melhores_resultados_cie

    html_card_header_melhores_resultados1_cie = ""
    if len(ciencias_tabela_verde_ordenado) > 0:
            
        @st.cache
        def html_card_header_melhores_resultados1_cie(ciencias_tabela_verde_ordenado):
            html_card_header_melhores_resultados1_cie="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(ciencias_tabela_verde_ordenado['Assunto'][0])+"""</p>
              </div>
            </div>
            """
            return html_card_header_melhores_resultados1_cie

    html_card_header_melhores_resultados2_cie = ""
    if len(ciencias_tabela_verde_ordenado) > 1:
            
        @st.cache
        def html_card_header_melhores_resultados2_cie(ciencias_tabela_verde_ordenado):
            html_card_header_melhores_resultados2_cie="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(ciencias_tabela_verde_ordenado['Assunto'][1])+"""</p>
              </div>
            </div>
            """
            return html_card_header_melhores_resultados2_cie

    html_card_header_melhores_resultados3_cie="" 
    if len(ciencias_tabela_verde_ordenado) > 2:
            
        @st.cache
        def html_card_header_melhores_resultados3_cie(ciencias_tabela_verde_ordenado):
            html_card_header_melhores_resultados3_cie="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(ciencias_tabela_verde_ordenado['Assunto'][2])+"""</p>
              </div>
            </div>
            """
            return html_card_header_melhores_resultados3_cie

    @st.cache
    def html_card_header_pontos_melhorar_cie():
        html_card_header_pontos_melhorar_cie="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
        height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Pontos que você pode melhorar</h5>
        </div>
        </div>
        """
        return html_card_header_pontos_melhorar_cie       
    
    html_card_header_pontos_melhorar1_cie = ""
    if len(ciencias_tabela_vermelho_ordenado) > 0:
            
        @st.cache
        def html_card_header_pontos_melhorar1_cie(ciencias_tabela_vermelho_ordenado):
            html_card_header_pontos_melhorar1_cie="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(ciencias_tabela_vermelho_ordenado['Assunto'][0])+"""</p>
              </div>
            </div>
            """
            return html_card_header_pontos_melhorar1_cie

    html_card_header_pontos_melhorar2_cie=""      
    if len(ciencias_tabela_vermelho_ordenado) > 1:
            
        @st.cache
        def html_card_header_pontos_melhorar2_cie(ciencias_tabela_vermelho_ordenado):
            html_card_header_pontos_melhorar2_cie="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(ciencias_tabela_vermelho_ordenado['Assunto'][1])+"""</p>
              </div>
            </div>
            """
            return html_card_header_pontos_melhorar2_cie
        
    html_card_header_pontos_melhorar3_cie=""      
    if len(ciencias_tabela_vermelho_ordenado) > 2:
            
        @st.cache
        def html_card_header_pontos_melhorar3_cie(ciencias_tabela_vermelho_ordenado):
            html_card_header_pontos_melhorar3_cie="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(ciencias_tabela_vermelho_ordenado['Assunto'][2])+"""</p>
              </div>
            </div>
            """
            return html_card_header_pontos_melhorar3_cie
        
    return html_table_cie_hum, html_table_cie_nat, html_card_header_melhores_resultados_cie, html_card_header_melhores_resultados1_cie, html_card_header_melhores_resultados2_cie, html_card_header_melhores_resultados3_cie, html_card_header_pontos_melhorar_cie, html_card_header_pontos_melhorar1_cie, html_card_header_pontos_melhorar2_cie, html_card_header_pontos_melhorar3_cie

def cie_show2(turma_aluno, turma_eng, turma_cien):

    with st.container():
        col1, col2, col3, col4 = st.columns([0.5,12,0.5,10.5])
        with col1:
            st.write("")
        with col2:
            if turma_aluno['Turma'][0] == turma_eng or turma_aluno['Turma'][0] == turma_cien:
                st.markdown(html_table_cie_nat(ciencias_tabela3), unsafe_allow_html=True)
            else:
                st.markdown(html_table_cie_hum(ciencias_tabela3), unsafe_allow_html=True)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_card_header_melhores_resultados_cie(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            if len(ciencias_tabela_verde_ordenado) > 0:
                st.markdown(html_card_header_melhores_resultados1_cie(ciencias_tabela_verde_ordenado), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
            if len(ciencias_tabela_verde_ordenado) > 1:
                st.markdown(html_card_header_melhores_resultados2_cie(ciencias_tabela_verde_ordenado), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
            if len(ciencias_tabela_verde_ordenado) > 2:
                st.markdown(html_card_header_melhores_resultados3_cie(ciencias_tabela_verde_ordenado), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)

            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_header_pontos_melhorar_cie(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            if len(ciencias_tabela_vermelho_ordenado) > 0:
                st.markdown(html_card_header_pontos_melhorar1_cie(ciencias_tabela_vermelho_ordenado), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
            if len(ciencias_tabela_vermelho_ordenado) > 1:
                st.markdown(html_card_header_pontos_melhorar2_cie(ciencias_tabela_vermelho_ordenado), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
            if len(ciencias_tabela_vermelho_ordenado) > 2:
                st.markdown(html_card_header_pontos_melhorar3_cie(ciencias_tabela_vermelho_ordenado), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)

    st.markdown(html_br(), unsafe_allow_html=True)
    st.markdown(html_br(), unsafe_allow_html=True)    

#@st.cache
def tratamento_dados_red():

    base_redacao = pd.read_csv('./resultadoredacao.csv')
    
    base_redacao['Acerto'] = 0.00
    for i in range(len(base_redacao)):
        base_redacao['Acerto'][i] = base_redacao['Nota na questão'][i]/base_redacao['Valor da questão'][i]
    
    base_redacao2 = base_redacao[base_redacao['Nota na questão'] >= 0]
    base_redacao_aux = base_redacao[base_redacao['Nota na questão'] > 0]
    
    redacao_detalhes_media = base_redacao_aux.groupby('Competência').mean(['Acerto']).reset_index()
    base_redacao2["Login do aluno(a)"] = base_redacao2["Login do aluno(a)"].apply(extract_login) 
    redacao_aluno = base_redacao2[base_redacao2['Login do aluno(a)'] == login_aluno]
    
    redacao_aluno_media = redacao_aluno.groupby('Competência').mean(['Acerto']).reset_index()

    redacao_aluno_media2 = redacao_aluno.groupby('Competência').count().reset_index()

    redacao_aluno_media3 = pd.DataFrame()
    redacao_aluno_media3['Competência'] = redacao_aluno_media2['Competência']
    redacao_aluno_media3['Nota na questão'] = redacao_aluno_media2['Nota na questão']
    
    base["Login do aluno(a)"] = base["Login do aluno(a)"].apply(extract_login) 

    redacao_tempo = pd.merge(base_redacao2, base, on = ['Login do aluno(a)'], how = 'left')

    redacao_tempo2 = redacao_tempo[redacao_tempo['Número da questão'] == 73]
    redacao_tempo3 = redacao_tempo2[redacao_tempo2['Nota na questão_x'] > 0]

    redacao_aluno_tempo2 = redacao_tempo2[redacao_tempo2['Login do aluno(a)'] == login_aluno]

    redacao_aluno_tempo = redacao_aluno_tempo2['Tempo na questão'].mean()
    hours_aluno_red, minutes_aluno = divmod(int(redacao_aluno_tempo), 3600)
    minutes_certo, seconds = divmod(minutes_aluno, 60)
    redacao_aluno_tempo_str = ' h '+str(minutes_certo)+' min '+str(seconds)+' s' 

    redacao_media_tempo = redacao_tempo3['Tempo na questão'].mean()
    hours_red_media, minutes_red_media = divmod(int(redacao_media_tempo), 3600)
    minutes_certo, seconds_red_media = divmod(minutes_red_media, 60)
    redacao_media_tempo_str = str(hours_red_media)+' h '+str(minutes_certo)+' min '+str(seconds_red_media)+' s'

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

    return base_redacao2, redacao_aluno_media, redacao_tabela3, redacao_tabela_verde_ordenado, redacao_tabela_vermelho_ordenado, redacao_aluno_tempo_str, redacao_media_tempo_str, hours_aluno_red           

def red_show(base_redacao2, redacao_aluno_media, redacao_tabela3, redacao_aluno_tempo_str, redacao_media_tempo_str, hours_aluno_red):

    @st.cache
    def html_card_header3():
        html_card_header3="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Classificação</h4>
        </div>
        </div>
        """
        return html_card_header3

    html_header_red = ""
    @st.cache
    def html_header_red():
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
        return html_header_red

    html_card_footer1_disc_med_red = ""
    @st.cache
    def html_card_footer1_disc_med_red(redacao_tabela3):
        html_card_footer1_disc_med_red="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Media Geral: """+str(int(round(200+0.8*200*redacao_tabela3['Resultado Geral decimal'].sum(),0)))+"""</p>
        </div>
        </div>
        """
        return html_card_footer1_disc_med_red

    html_card_footer_med_red3 = ""
    @st.cache
    def html_card_footer_med_red3(redacao_media_tempo_str):
        html_card_footer_med_red3="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(redacao_media_tempo_str)+"""</p>
        </div>
        </div>
        """
        return html_card_footer_med_red3

    base_redacao_disciplina = base_redacao2.groupby('Login do aluno(a)').sum().reset_index()
    
    for i in range(len(base_redacao_disciplina['Login do aluno(a)'])):
        if base_redacao_disciplina['Nota na questão'][i] > 0:
            base_redacao_disciplina['Nota na questão'][i] = 200 + 0.8*base_redacao_disciplina['Nota na questão'][i]
    #base_redacao_disciplina['Nota na questão'] = 200 + 0.8*base_redacao_disciplina['Nota na questão']

    base_redacao_disciplina2 = base_redacao_disciplina.sort_values(by = 'Nota na questão', ascending = False).reset_index()
    base_redacao_disciplina2["Login do aluno(a)"] = base_redacao_disciplina2["Login do aluno(a)"].apply(extract_login) 
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
    
    html_card_header_destaques_red = ""
    @st.cache
    def html_card_header_destaques_red(texto):
        html_card_header_destaques_red="""
        <div class="card">
            <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
                height: 150px;">
                <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
            </div>
        </div>
        """ 
        return html_card_header_destaques_red

    @st.cache
    def html_card_footer_med_red3():
        html_card_footer_med_red3="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(ciencias_media_tempo_str)+"""</p>
        </div>
        </div>
        """
        return html_card_footer_med_red3
    
    @st.cache
    def html_card_footer4():
        html_card_footer4="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 280px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;"></p>
        </div>
        </div>
        """
        return html_card_footer4


     
    for i in range(len(redacao_aluno_media['Nota na questão'])):
        if redacao_aluno_media['Nota na questão'][i] == 0:
            redacao_aluno_media['Nota na questão'][i] = - 50

    if len(redacao_tabela3['Status']) != 0:
        
        ### REDAÇÃO
        
        st.markdown(html_header_red(), unsafe_allow_html=True)
        
        ### Block 1#########################################################################################
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1,20,1,20,1,20,1,20,1])
            with col1:
                st.write("")
            with col2:
                st.markdown(html_card_header1_disc(), unsafe_allow_html=True)
                fig_c1 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=round(200+0.8*redacao_aluno_media['Nota na questão'].sum(),1),
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': int(round(200+0.8*200*redacao_tabela3['Resultado Geral decimal'].sum(),0)), 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c1.update_layout(autosize=False,
                                     width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                st.plotly_chart(fig_c1)
                st.markdown(html_card_footer1_disc(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_footer1_disc_med_red(redacao_tabela3), unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header3_disc(), unsafe_allow_html=True)
                fig_c3 = go.Figure(go.Indicator(
                    mode="number",
                    value=classificacao_aluno_red['level_0'][0]+1,
                    number={'suffix': "º", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                    delta={'position': "bottom", 'reference': 1, 'relative': False},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c3.update_layout(autosize=False,
                                     width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                     paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c3.update_traces(delta_decreasing_color="#3D9970",
                                     delta_increasing_color="#FF4136",
                                     delta_valueformat='.3f',
                                     selector=dict(type='indicator'))
                st.plotly_chart(fig_c3)
                st.markdown(html_card_footer3_disc_matlin(), unsafe_allow_html=True)
            with col5:
                st.write("")
            with col6:
                st.markdown(html_card_header3(), unsafe_allow_html=True)
                fig_c2 = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=hours_aluno_red,
                    number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}, "valueformat": ".0f", "suffix": redacao_aluno_tempo_str},
                    #delta={'position': "bottom", 'reference': int(round(resultados_gerais5['Acerto'].mean(),0))},
                    domain={'x': [0, 1], 'y': [0, 1]}))
                fig_c2.update_layout(autosize=False,
                                    width=280, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                    paper_bgcolor="#FFF0FC", font={'size': 20})
                fig_c2.update_traces(delta_decreasing_color="#FF4136",
                                    delta_increasing_color="#3D9970",
                                    delta_valueformat='f',
                                    selector=dict(type='indicator'))
                st.plotly_chart(fig_c2)
                st.markdown(html_card_footer4(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_footer_med_red3(), unsafe_allow_html=True)
            with col7:
                st.write("")
            with col8:
                st.write("")
            with col9:
                st.write("")

        st.markdown(html_br(), unsafe_allow_html=True)
        st.markdown(html_br(), unsafe_allow_html=True)
        
        base_redacao3 = base_redacao2.groupby('Login do aluno(a)').sum().reset_index()
        for i in range(len(base_redacao3['Nota na questão'])):
            if base_redacao3['Nota na questão'][i] > 0:
                base_redacao3['Nota na questão'][i] = 200 + 0.8*base_redacao3['Nota na questão'][i]
 
        base_redacao4 = base_redacao3[base_redacao3['Login do aluno(a)'] == login_aluno]
        base_redacao3aux = base_redacao3[base_redacao3['Nota na questão'] > 0]

        base_redacao5 = base_redacao3aux['Nota na questão'].mean()

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
                fig.add_vline(x=int(round(truncar(base_redacao5,-1),0)), line_width=7, line_dash="dash", line_color="#01ECEC", annotation_text="Média", annotation_position="top right")
                fig.update_xaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=6, rangemode="tozero",
                              showgrid=False, gridwidth=0.5, gridcolor='#f6f6f6')
                fig.update_yaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=10, rangemode="tozero",
                              showgrid=True, gridwidth=0.5, gridcolor='#f6f6f6')
                fig.update_traces(marker_color='#0010B3')
                st.plotly_chart(fig)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_header_destaques_red(texto), unsafe_allow_html=True)
            with col5:
                st.write("")

        st.markdown(html_br(), unsafe_allow_html=True)

    return base_redacao_disciplina2

@st.cache
def html_red(redacao_tabela3, redacao_tabela_verde_ordenado, redacao_tabela_vermelho_ordenado):

    html_table = ""
    @st.cache
    def html_table(redacao_tabela3):
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
        return html_table

    html_card_header_melhores_resultados = ""
    @st.cache
    def html_card_header_melhores_resultados():
        html_card_header_melhores_resultados="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Seus melhores resultados</h5>
          </div>
        </div>
        """
        return html_card_header_melhores_resultados
    

    html_card_header_melhores_resultados1 = ""  
    if len(redacao_tabela_verde_ordenado) > 0:

        @st.cache
        def html_card_header_melhores_resultados1(redacao_tabela_verde_ordenado):
            html_card_header_melhores_resultados1="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(redacao_tabela_verde_ordenado['Competência'][0])+"""</p>
              </div>
            </div>
            """
            return html_card_header_melhores_resultados1    

    html_card_header_melhores_resultados2 = ""
    if len(redacao_tabela_verde_ordenado) > 1:

        @st.cache
        def html_card_header_melhores_resultados2(redacao_tabela_verde_ordenado):
            html_card_header_melhores_resultados2="""
            <div class="card">
            <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
            height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(redacao_tabela_verde_ordenado['Competência'][1])+"""</p>
            </div>
            </div>
            """
            return html_card_header_melhores_resultados2

    html_card_header_melhores_resultados3 = ""       
    if len(redacao_tabela_verde_ordenado) > 2:

       
        @st.cache
        def html_card_header_melhores_resultados3(redacao_tabela_verde_ordenado):
            html_card_header_melhores_resultados3="""
            <div class="card">
            <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #a5ffa5; padding-top: 12px; width: 495px;
            height: 50px;">
                <p class="card-title" style="background-color:#a5ffa5; color:#008800; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🟢 """+str(redacao_tabela_verde_ordenado['Competência'][2])+"""</p>
            </div>
            </div>
            """
            return html_card_header_melhores_resultados3
            
    html_card_header_pontos_melhorar = ""
    @st.cache
    def html_card_header_pontos_melhorar():
        html_card_header_pontos_melhorar="""
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 30px; width: 495px;
           height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Pontos que você pode melhorar</h5>
          </div>
        </div>
        """
        return html_card_header_pontos_melhorar

    html_card_header_pontos_melhorar1 = ""
    if len(redacao_tabela_vermelho_ordenado) > 0:

        
        @st.cache
        def html_card_header_pontos_melhorar1(redacao_tabela_vermelho_ordenado):
            html_card_header_pontos_melhorar1="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(redacao_tabela_vermelho_ordenado['Competência'][0])+"""</p>
              </div>
            </div>
            """
            return html_card_header_pontos_melhorar1
        
    html_card_header_pontos_melhorar2 = ""    
    if len(redacao_tabela_vermelho_ordenado) > 1:

        @st.cache
        def html_card_header_pontos_melhorar2(redacao_tabela_vermelho_ordenado):
            html_card_header_pontos_melhorar2="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(redacao_tabela_vermelho_ordenado['Competência'][1])+"""</p>
              </div>
            </div>
            """
            return html_card_header_pontos_melhorar2
        
    html_card_header_pontos_melhorar3 = ""
    if len(redacao_tabela_vermelho_ordenado) > 2:

        @st.cache
        def html_card_header_pontos_melhorar3(redacao_tabela_vermelho_ordenado):
            html_card_header_pontos_melhorar3="""
            <div class="card">
              <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #ffb1b1; padding-top: 12px; width: 495px;
               height: 50px;">
                <p class="card-title" style="background-color:#ffb1b1; color:#a80000; font-size: 20px;  font-family:Georgia; text-align: center; padding: 0px 0;">🔴 """+str(redacao_tabela_vermelho_ordenado['Competência'][2])+"""</p>
              </div>
            </div>
            """
            return html_card_header_pontos_melhorar3
        
    return html_table, html_card_header_melhores_resultados, html_card_header_melhores_resultados1, html_card_header_melhores_resultados2, html_card_header_melhores_resultados3, html_card_header_pontos_melhorar, html_card_header_pontos_melhorar1, html_card_header_pontos_melhorar2, html_card_header_pontos_melhorar3

def red_show2(redacao_tabela3):

    with st.container():
            col1, col2, col3, col4 = st.columns([0.5,12,0.5,10.5])
            with col1:
                st.write("")
            with col2:
                st.markdown(html_table(redacao_tabela3), unsafe_allow_html=True)
            with col3:
                st.write("")
            with col4:
                st.markdown(html_card_header_melhores_resultados(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                if len(redacao_tabela_verde_ordenado) > 0:
                    st.markdown(html_card_header_melhores_resultados1(redacao_tabela_verde_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)
                if len(redacao_tabela_verde_ordenado) > 1:
                    st.markdown(html_card_header_melhores_resultados2(redacao_tabela_verde_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)
                if len(redacao_tabela_verde_ordenado) > 2:
                    st.markdown(html_card_header_melhores_resultados3(redacao_tabela_verde_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)

                st.markdown(html_br(), unsafe_allow_html=True)
                st.markdown(html_card_header_pontos_melhorar(), unsafe_allow_html=True)
                st.markdown(html_br(), unsafe_allow_html=True)
                if len(redacao_tabela_vermelho_ordenado) > 0:
                    st.markdown(html_card_header_pontos_melhorar1(redacao_tabela_vermelho_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)
                if len(redacao_tabela_vermelho_ordenado) > 1:
                    st.markdown(html_card_header_pontos_melhorar2(redacao_tabela_vermelho_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)
                if len(redacao_tabela_vermelho_ordenado) > 2:
                    st.markdown(html_card_header_pontos_melhorar3(redacao_tabela_vermelho_ordenado), unsafe_allow_html=True)
                    st.markdown(html_br(), unsafe_allow_html=True)

    st.markdown(html_br(), unsafe_allow_html=True)

    if redacao_tabela3['Resultado Individual decimal'].sum() > 0:
        st.image("redacao_"+login_aluno+".png", caption=f"Redação", use_column_width=True, align='center')

def fotos_questao(turma_aluno, turma_eng, turma_cien):

    html_subtitle = ""
    @st.cache
    def html_subtitle():
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
        return html_subtitle

    
    st.markdown(html_subtitle(), unsafe_allow_html=True)

    numeros_e_imagens = {i: f"Questão {str(i).zfill(2)}.png" for i in range(1, 73)}

    selecionado = ""
    num_selecionado = ""
    # Inicializa a grade
    botoes_por_linha = 24
    num_linhas = len(numeros_e_imagens) // botoes_por_linha
    # Exibe os botões em colunas
    for numero in range(1, len(numeros_e_imagens) + 1, botoes_por_linha):
        colunas = st.columns(botoes_por_linha)
        for i in range(botoes_por_linha):
            coluna = colunas[i]
            if numero + i <= len(numeros_e_imagens):
                if coluna.button(f"{str(numero + i).zfill(2)}"):
                    selecionado = numeros_e_imagens[numero + i]
                    num_selecionado = numero
                    i_selecionado = i

    if (selecionado != "" and num_selecionado != ""):
        if (turma_aluno['Turma'][0] != turma_eng and turma_aluno['Turma'][0] != turma_cien):

            st.image(selecionado, caption=f"Questão {num_selecionado + i_selecionado}", use_column_width=True)
        else:
            if (num_selecionado + i_selecionado) < 25:
                st.image(selecionado, caption=f"Questão {num_selecionado + i_selecionado + 73}", use_column_width=True)

def detalhamento(base):
        
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
    tabela_detalhes["Login do aluno(a)"] = tabela_detalhes["Login do aluno(a)"].apply(extract_login) 
    tabela_detalhes_aluno = tabela_detalhes[tabela_detalhes['Login do aluno(a)'] == login_aluno]
    tabela_detalhes_aluno2 = tabela_detalhes_aluno.drop(columns = ['Nota na questão','Valor da questão','Nome do aluno(a)','Login do aluno(a)','Certo ou errado'])
    tabela_detalhes_media = tabela_detalhes_fizeram.groupby('Número da questão').mean(['Acerto']).reset_index()
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
        

def fase_2(base_resultados_2fase):

    html_header_2fase = ""
    @st.cache
    def html_header_2fase():
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
        return html_header_2fase

    
    st.markdown(html_br(), unsafe_allow_html=True)
    st.markdown(html_header_2fase(), unsafe_allow_html=True)
    
    
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

    segunda_fase = base_resultados_2fase.copy()
    
    segunda_fase2 = segunda_fase.drop(columns = ['Tema 1 - Comunicação assertiva','Tema 2 - Comunicação assertiva','Tema 3 - Comunicação assertiva','Tema 4 - Comunicação assertiva', 'Tema 1 - Interação com pessoas', 'Tema 2 - Interação com pessoas', 'Tema 3 - Interação com pessoas', 'Tema 4 - Interação com pessoas', 'Tema 1 - Pensamento crítico', 'Tema 2 - Pensamento crítico', 'Tema 3 - Pensamento crítico', 'Tema 4 - Pensamento crítico', 'Tema 1 - Aprender a aprender', 'Tema 2 - Aprender a aprender']) 
    segunda_fase3 = pd.merge(segunda_fase2, base_redacao_disciplina2, on = 'Login do aluno(a)', how = 'outer')
    segunda_fase3.rename(columns = {'Nota na questão':'Nota Redação'}, inplace = True)
    segunda_fase3['Nota 2º fase'] = segunda_fase3['Nota 2º fase'].fillna(0)
    #segunda_fase3['Nota 2º fase'] = segunda_fase3['Nota 2º fase'].replace("<NA>", 0)
    segunda_fase3['Nota Final 2º fase'] = 0.25*segunda_fase3['Nota Redação'] + 0.75*segunda_fase3['Nota 2º fase']
    segunda_fase4 = segunda_fase3[segunda_fase3['Nota Final 2º fase'] > 0]
    
    #base_resultados_2fase2 = base_resultados_2fase[base_resultados_2fase['Tema 1 - Comunicação assertiva'] > 0]
    
    ### Resultados gerais do aluno
    base_resultados_2fase = base_resultados_2fase[base_resultados_2fase['Nota 2º fase'] >= 0]
    base_resultados_2faseaux = base_resultados_2fase[base_resultados_2fase['Nota 2º fase'] > 0]
    numero_candidatos_2fase = len(segunda_fase4['Nota Final 2º fase'])

    return numero_candidatos_2fase, segunda_fase4

@st.cache
def html_fase_2():

    html_card_header1 = ""
    @st.cache
    def html_card_header1():
        html_card_header1="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota</h4>
        </div>
        </div>
        """
        return html_card_header1

    html_card_footer1 = ""
    @st.cache
    def html_card_footer1():
        html_card_footer1="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota máxima: 1000</p>
        </div>
        </div>
        """
        return html_card_footer1
    
    html_card_footer_med1 = ""
    @st.cache
    def html_card_footer_med1(base_resultados_2faseaux):
        html_card_footer_med1="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(int(round(base_resultados_2faseaux['Nota Final 2º fase'].mean(),0)))+"""</p>
        </div>
        </div>
        """
        return html_card_footer_med1

    html_card_header3 = ""
    @st.cache
    def html_card_header3():
        html_card_header3="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Classificação</h4>
        </div>
        </div>
        """
        return html_card_header3
    
    html_card_footer3 = ""
    @st.cache
    def html_card_footer3(numero_candidatos):
        html_card_footer3="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos)+"""</p>
        </div>
        </div>
        """
        return html_card_footer3
    
    return html_card_header1, html_card_footer1, html_card_footer_med1, html_card_header3, html_card_footer3
    
def fase_2_show(numero_candidatos_2fase, segunda_fase4):

    base_resultados_2fase_aluno = segunda_fase4.sort_values(by = 'Nota Final 2º fase', ascending = False).reset_index(drop = True).reset_index()


    base_resultados_2fase_aluno2 = base_resultados_2fase_aluno[base_resultados_2fase_aluno['Login do aluno(a)'] == login_aluno]
    base_resultados_2fase_aluno2.rename(columns = {'level_0':'Classificação'}, inplace = True)
    base_resultados_2fase_aluno2 = base_resultados_2fase_aluno2.reset_index(drop = True)

    if len(base_resultados_2fase_aluno2) > 0:
        #for i in range(len(base_resultados_2fase_aluno2['Nota Final 2º fase'])):
        if base_resultados_2fase_aluno2['Nota Final 2º fase'][0] > 0:
            base_resultados_2fase_aluno2['Classificação'][0] = base_resultados_2fase_aluno2['Classificação'][0] + 1
        else:
            base_resultados_2fase_aluno2['Classificação'][0] = numero_candidatos_2fase + 1
    else: 
        base_resultados_2fase_aluno2 = pd.DataFrame(columns = ['Nota Final 2º fase','Classificação'], index=range(2))
        base_resultados_2fase_aluno2['Nota Final 2º fase'][0] = 0
        base_resultados_2fase_aluno2['Classificação'][0] = numero_candidatos_2fase + 1

    base_resultados_2faseaux = segunda_fase4[segunda_fase4['Nota Final 2º fase'] > 0]

    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,20,1,20,1,20,1])
        with col1:
            st.write("")
        with col2:
            st.markdown(html_card_header1(), unsafe_allow_html=True)
            fig_c1 = go.Figure(go.Indicator(
                mode="number+delta",
                value=round(base_resultados_2fase_aluno2['Nota Final 2º fase'][0],1),
                number={'suffix': "", "font": {"size": 40, 'color': "#9E089E", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': int(round(truncar(base_resultados_2faseaux['Nota Final 2º fase'].mean(),-1),0)), 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c1.update_layout(autosize=False,
                                 width=350, height=90, margin=dict(l=20, r=20, b=20, t=50),
                                 paper_bgcolor="#FFF0FC", font={'size': 20})
            fig_c1.update_traces(delta_decreasing_color="#FF4136",
                                delta_increasing_color="#3D9970",
                                delta_valueformat='.0f',
                                selector=dict(type='indicator'))
            st.plotly_chart(fig_c1)
            st.markdown(html_card_footer1(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_footer_med1(base_resultados_2faseaux), unsafe_allow_html=True)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_card_header3(), unsafe_allow_html=True)
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
            st.markdown(html_card_footer3(numero_candidatos_2fase), unsafe_allow_html=True)
        with col5:
            st.write("")
        with col6:
            st.write("")
        with col7:
            st.write("")
    
    st.markdown(html_br(), unsafe_allow_html=True)
    st.markdown(html_br(), unsafe_allow_html=True)

    ponto = str(round(100*(numero_candidatos_2fase-(base_resultados_2fase_aluno2['Classificação'][0]-1))/numero_candidatos_2fase,0)).find('.')
    texto = str(round(100*(numero_candidatos_2fase-(base_resultados_2fase_aluno2['Classificação'][0]-1))/numero_candidatos_2fase,0))[0:ponto]

    html_card_header_destaques_gerais = ""
    @st.cache
    def html_card_header_destaques_gerais(texto):
        html_card_header_destaques_gerais="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
        height: 150px;">
            <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
        </div>
        </div>
        """ 
        return html_card_header_destaques_gerais

       
    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([9,25,2,25,4])
        with col1:
            st.write("")
        with col2:
            # create the bins
            counts, bins = np.histogram(base_resultados_2faseaux['Nota Final 2º fase'], bins=range(0, 1100, 100))
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
            fig.add_vline(x=int(round(base_resultados_2fase_aluno2['Nota Final 2º fase'].mean(),1)), line_width=7, line_dash="dash", line_color="#9E089E", annotation_text="Você está aqui!", annotation_position="top right")
            fig.add_vline(x=int(round(truncar(base_resultados_2faseaux['Nota Final 2º fase'].mean(),-1),0)), line_width=7, line_dash="dash", line_color="#01ECEC", annotation_text="Média", annotation_position="top right")
            fig.update_xaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=6, rangemode="tozero",
                          showgrid=False, gridwidth=0.5, gridcolor='#f6f6f6')
            fig.update_yaxes(showline=True, linewidth=1, linecolor='#9E089E', mirror=False, nticks=10, rangemode="tozero",
                          showgrid=True, gridwidth=0.5, gridcolor='#f6f6f6')
            fig.update_traces(marker_color='#0010B3')
            st.plotly_chart(fig)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_header_destaques_gerais(texto), unsafe_allow_html=True)
        with col5:
            st.write("")

def debate(base_resultados_2fase):

    base_resultados_2fase_debate = pd.DataFrame()
    base_resultados_2fase_debate = base_resultados_2fase
    
    base_resultados_2fase_debate2 = base_resultados_2fase_debate.drop(columns = ['Tema 1 - Aprender a aprender','Tema 2 - Aprender a aprender'])
   
    base_resultados_2fase_debate2['Nota 2º fase'] = 1000*(750*base_resultados_2fase_debate2['Tema 1 - Comunicação assertiva']/12 + 750*base_resultados_2fase_debate2['Tema 1 - Interação com pessoas']/12 + 750*base_resultados_2fase_debate2['Tema 1 - Pensamento crítico']/12 + 750*base_resultados_2fase_debate2['Tema 2 - Comunicação assertiva']/12 +  750*base_resultados_2fase_debate2['Tema 2 - Interação com pessoas']/12 + 750*base_resultados_2fase_debate2['Tema 2 - Pensamento crítico']/12 + 750*base_resultados_2fase_debate2['Tema 3 - Comunicação assertiva']/12 + 750*base_resultados_2fase_debate2['Tema 3 - Interação com pessoas']/12 + 750*base_resultados_2fase_debate2['Tema 3 - Pensamento crítico']/12 + 750*base_resultados_2fase_debate2['Tema 4 - Comunicação assertiva']/12 + 750*base_resultados_2fase_debate2['Tema 4 - Interação com pessoas']/12 + 750*base_resultados_2fase_debate2['Tema 4 - Pensamento crítico']/12)/3000
    base_resultados_2fase_debate2aux = base_resultados_2fase_debate2[base_resultados_2fase_debate2['Nota 2º fase'] > 0]

    numero_candidatos_deb_arg = len(base_resultados_2fase_debate2aux)

    html_header_2fase = ""
    @st.cache
    def html_header_2fase():
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
        return html_header_2fase

    
    st.markdown(html_br(), unsafe_allow_html=True)
    st.markdown(html_header_2fase(), unsafe_allow_html=True)

    return base_resultados_2fase_debate2aux, base_resultados_2fase_debate2, numero_candidatos_deb_arg

@st.cache
def html_debate(base_resultados_2fase_debate2aux, numero_candidatos_deb_arg):

    html_card_header1 = ""
    @st.cache
    def html_card_header1():
        html_card_header1="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota</h4>
        </div>
        </div>
        """
        return html_card_header1
    
    html_card_footer1 = ""
    @st.cache
    def html_card_footer1():
        html_card_footer1="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota máxima: 1000</p>
        </div>
        </div>
        """
        return html_card_footer1

    html_card_footer_med1 = ""
    @st.cache
    def html_card_footer_med1(base_resultados_2fase_debate2aux):
        html_card_footer_med1="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background:#FFA73E; padding-top: 12px; width: 350px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(int(round(base_resultados_2fase_debate2aux['Nota 2º fase'].mean(),0)))+"""</p>
        </div>
        </div>
        """
        return html_card_footer_med1
    
    html_card_header3 = ""
    @st.cache
    def html_card_header3():
        html_card_header3="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Classificação</h4>
        </div>
        </div>
        """
        return html_card_header3

    html_card_footer3_debate = ""
    @st.cache
    def html_card_footer3_debate(numero_candidatos_deb_arg):
        html_card_footer3_debate="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos_deb_arg)+"""</p>
        </div>
        </div>
        """
        return html_card_footer3_debate
    
    return html_card_header1, html_card_footer1, html_card_footer_med1, html_card_header3, html_card_footer3_debate
    
def debate_show(base_resultados_2fase_debate2, base_resultados_2fase_debate2aux, numero_candidatos_deb_arg):
    
    base_resultados_2fase_aluno_debate = base_resultados_2fase_debate2.sort_values(by = 'Nota 2º fase', ascending = False).reset_index(drop = True).reset_index()

    base_resultados_2fase_aluno_debate.rename(columns = {'index':'Classificação'}, inplace = True)
    base_resultados_2fase_aluno_debate2 = base_resultados_2fase_aluno_debate[base_resultados_2fase_aluno_debate['Login do aluno(a)'] == login_aluno].reset_index()
    if len(base_resultados_2fase_aluno_debate2) > 0:
        if base_resultados_2fase_aluno_debate2['Nota 2º fase'][0] == 0:
            base_resultados_2fase_aluno_debate2['Classificação'][0] = numero_candidatos_deb_arg + 1
        else:
            base_resultados_2fase_aluno_debate2['Classificação'][0] = base_resultados_2fase_aluno_debate2['Classificação'][0] + 1
    else:
        base_resultados_2fase_aluno_debate2 = pd.DataFrame(columns = ['Nota 2º fase','Classificação'], index=range(2))
        base_resultados_2fase_aluno_debate2['Nota 2º fase'][0] = 0
        base_resultados_2fase_aluno_debate2['Classificação'][0] = numero_candidatos_deb_arg + 1

    
    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,20,1,20,1,20,1])
        with col1:
            st.write("")
        with col2:
            st.markdown(html_card_header1(), unsafe_allow_html=True)
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
            st.markdown(html_card_footer1(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_footer_med1(base_resultados_2fase_debate2aux), unsafe_allow_html=True)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_card_header3(), unsafe_allow_html=True)
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
            st.markdown(html_card_footer3(numero_candidatos_deb_arg), unsafe_allow_html=True)
        with col5:
            st.write("")
        with col6:
            st.write("")
        with col7:
            st.write("")
    
    st.markdown(html_br(), unsafe_allow_html=True)
    st.markdown(html_br(), unsafe_allow_html=True)

    ponto = str(round(100*(numero_candidatos_deb_arg-(base_resultados_2fase_aluno_debate2['Classificação'][0]-1))/numero_candidatos_deb_arg,0)).find('.')
    texto = str(round(100*(numero_candidatos_deb_arg-(base_resultados_2fase_aluno_debate2['Classificação'][0]-1))/numero_candidatos_deb_arg,0))[0:ponto]

    html_card_header_destaques_gerais = ""
    @st.cache
    def html_card_header_destaques_gerais(texto):
        html_card_header_destaques_gerais="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
        height: 150px;">
            <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
        </div>
        </div>
        """  
        return html_card_header_destaques_gerais

      
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
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_header_destaques_gerais(texto), unsafe_allow_html=True)
        with col5:
            st.write("")

    base_resultados_2fase_debate3 = base_resultados_2fase_debate2[base_resultados_2fase_debate2['Login do aluno(a)'] == login_aluno].reset_index()
    if len(base_resultados_2fase_debate3) > 0:
        data = [
        {'Temas': 'Tema 1',  'Comunicação Assertiva - Resultado Individual': base_resultados_2fase_debate3['Tema 1 - Comunicação assertiva'][0], 'Comunicação Assertiva - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 1 - Comunicação assertiva'].mean(),1), 'Interação com pessoas - Resultado Individual':base_resultados_2fase_debate3['Tema 1 - Interação com pessoas'][0], 'Interação com pessoas - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 1 - Interação com pessoas'].mean(),1), 'Pensamento crítico - Resultado Individual': base_resultados_2fase_debate3['Tema 1 - Pensamento crítico'][0], 'Pensamento crítico - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 1 - Pensamento crítico'].mean(),1)},


        {'Temas': 'Tema 2', 'Comunicação Assertiva - Resultado Individual': base_resultados_2fase_debate3['Tema 2 - Comunicação assertiva'][0], 'Comunicação Assertiva - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 2 - Comunicação assertiva'].mean(),1), 'Interação com pessoas - Resultado Individual':base_resultados_2fase_debate3['Tema 2 - Interação com pessoas'][0], 'Interação com pessoas - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 2 - Interação com pessoas'].mean(),1), 'Pensamento crítico - Resultado Individual': base_resultados_2fase_debate3['Tema 2 - Pensamento crítico'][0], 'Pensamento crítico - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 2 - Pensamento crítico'].mean(),1)}, 


        {'Temas': 'Tema 3', 'Comunicação Assertiva - Resultado Individual': base_resultados_2fase_debate3['Tema 3 - Comunicação assertiva'][0], 'Comunicação Assertiva - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 3 - Comunicação assertiva'].mean(),1), 'Interação com pessoas - Resultado Individual':base_resultados_2fase_debate3['Tema 3 - Interação com pessoas'][0], 'Interação com pessoas - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 3 - Interação com pessoas'].mean(),1), 'Pensamento crítico - Resultado Individual': base_resultados_2fase_debate3['Tema 3 - Pensamento crítico'][0], 'Pensamento crítico - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 3 - Pensamento crítico'].mean(),1)},


        {'Temas': 'Tema 4', 'Comunicação Assertiva - Resultado Individual': base_resultados_2fase_debate3['Tema 4 - Comunicação assertiva'][0], 'Comunicação Assertiva - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 4 - Comunicação assertiva'].mean(),1), 'Interação com pessoas - Resultado Individual':base_resultados_2fase_debate3['Tema 4 - Interação com pessoas'][0], 'Interação com pessoas - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 4 - Interação com pessoas'].mean(),1), 'Pensamento crítico - Resultado Individual': base_resultados_2fase_debate3['Tema 4 - Pensamento crítico'][0], 'Pensamento crítico - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 4 - Pensamento crítico'].mean(),1)},


        {'Temas': 'Total', 'Comunicação Assertiva - Resultado Individual': round((base_resultados_2fase_debate3['Tema 1 - Comunicação assertiva'][0]+base_resultados_2fase_debate3['Tema 2 - Comunicação assertiva'][0]+base_resultados_2fase_debate3['Tema 3 - Comunicação assertiva'][0]+base_resultados_2fase_debate3['Tema 4 - Comunicação assertiva'][0])/4,1), 'Comunicação Assertiva - Resultado Geral': round((base_resultados_2fase_debate2aux['Tema 1 - Comunicação assertiva'].mean() + base_resultados_2fase_debate2aux['Tema 2 - Comunicação assertiva'].mean() + base_resultados_2fase_debate2aux['Tema 3 - Comunicação assertiva'].mean() + base_resultados_2fase_debate2aux['Tema 4 - Comunicação assertiva'].mean())/4,1), 'Interação com pessoas - Resultado Individual': round((base_resultados_2fase_debate3['Tema 1 - Interação com pessoas'][0]+base_resultados_2fase_debate3['Tema 2 - Interação com pessoas'][0]+base_resultados_2fase_debate3['Tema 3 - Interação com pessoas'][0]+base_resultados_2fase_debate3['Tema 4 - Interação com pessoas'][0])/4,1), 'Interação com pessoas - Resultado Geral': round(((base_resultados_2fase_debate2aux['Tema 1 - Interação com pessoas'].mean() + base_resultados_2fase_debate2aux['Tema 2 - Interação com pessoas'].mean() + base_resultados_2fase_debate2aux['Tema 3 - Interação com pessoas'].mean() + base_resultados_2fase_debate2aux['Tema 4 - Interação com pessoas'].mean())/4),1), 'Pensamento crítico - Resultado Individual': round((base_resultados_2fase_debate3['Tema 1 - Pensamento crítico'][0]+base_resultados_2fase_debate3['Tema 2 - Pensamento crítico'][0]+base_resultados_2fase_debate3['Tema 3 - Pensamento crítico'][0]+base_resultados_2fase_debate3['Tema 4 - Pensamento crítico'][0])/4,1), 'Pensamento crítico - Resultado Geral': round((base_resultados_2fase_debate2aux['Tema 1 - Pensamento crítico'].mean() + base_resultados_2fase_debate2aux['Tema 2 - Pensamento crítico'].mean() + base_resultados_2fase_debate2aux['Tema 3 - Pensamento crítico'].mean() + base_resultados_2fase_debate2aux['Tema 4 - Pensamento crítico'].mean())/4,1)}
        ]
    else:
        data = [
        {'Temas': 'Tema 1',  'Comunicação Assertiva - Resultado Individual': 0, 'Comunicação Assertiva - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 1 - Comunicação assertiva'].mean(),1), 'Interação com pessoas - Resultado Individual':0, 'Interação com pessoas - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 1 - Interação com pessoas'].mean(),1), 'Pensamento crítico - Resultado Individual': 0, 'Pensamento crítico - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 1 - Pensamento crítico'].mean(),1)},


        {'Temas': 'Tema 2', 'Comunicação Assertiva - Resultado Individual': 0, 'Comunicação Assertiva - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 2 - Comunicação assertiva'].mean(),1), 'Interação com pessoas - Resultado Individual':0, 'Interação com pessoas - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 2 - Interação com pessoas'].mean(),1), 'Pensamento crítico - Resultado Individual': 0, 'Pensamento crítico - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 2 - Pensamento crítico'].mean(),1)}, 


        {'Temas': 'Tema 3', 'Comunicação Assertiva - Resultado Individual': 0, 'Comunicação Assertiva - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 3 - Comunicação assertiva'].mean(),1), 'Interação com pessoas - Resultado Individual':0, 'Interação com pessoas - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 3 - Interação com pessoas'].mean(),1), 'Pensamento crítico - Resultado Individual': 0, 'Pensamento crítico - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 3 - Pensamento crítico'].mean(),1)},


        {'Temas': 'Tema 4', 'Comunicação Assertiva - Resultado Individual': 0, 'Comunicação Assertiva - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 4 - Comunicação assertiva'].mean(),1), 'Interação com pessoas - Resultado Individual':0, 'Interação com pessoas - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 4 - Interação com pessoas'].mean(),1), 'Pensamento crítico - Resultado Individual': 0, 'Pensamento crítico - Resultado Geral': round(base_resultados_2fase_debate2aux['Tema 4 - Pensamento crítico'].mean(),1)},


        {'Temas': 'Total', 'Comunicação Assertiva - Resultado Individual': 0, 'Comunicação Assertiva - Resultado Geral': round((base_resultados_2fase_debate2aux['Tema 1 - Comunicação assertiva'].mean() + base_resultados_2fase_debate2aux['Tema 2 - Comunicação assertiva'].mean() + base_resultados_2fase_debate2aux['Tema 3 - Comunicação assertiva'].mean() + base_resultados_2fase_debate2aux['Tema 4 - Comunicação assertiva'].mean())/4,1), 'Interação com pessoas - Resultado Individual': 0, 'Interação com pessoas - Resultado Geral': round(((base_resultados_2fase_debate2aux['Tema 1 - Interação com pessoas'].mean() + base_resultados_2fase_debate2aux['Tema 2 - Interação com pessoas'].mean() + base_resultados_2fase_debate2aux['Tema 3 - Interação com pessoas'].mean() + base_resultados_2fase_debate2aux['Tema 4 - Interação com pessoas'].mean())/4),1), 'Pensamento crítico - Resultado Individual':  0, 'Pensamento crítico - Resultado Geral': round((base_resultados_2fase_debate2aux['Tema 1 - Pensamento crítico'].mean() + base_resultados_2fase_debate2aux['Tema 2 - Pensamento crítico'].mean() + base_resultados_2fase_debate2aux['Tema 3 - Pensamento crítico'].mean() + base_resultados_2fase_debate2aux['Tema 4 - Pensamento crítico'].mean())/4,1)}
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

    tabela_temas_debate['Temas'] = ['Tema 1 -  Deveria continuar havendo isenção de transporte público para idosos?', 'Tema 2 -  Médicos podem usar procedimentos "não-científicos" para tratar os pacientes?', 'Tema 3 - As questões religiosas deveriam ser um respaldo para que o crime de homofobia seja aplicado de maneira mais leve?', 'Tema 4 - O governo deveria subsidiar o ensino em instituições privadas para estudantes de baixa renda?']

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

    st.markdown(html_br(), unsafe_allow_html=True)

    with st.container():
            col1, col2, col3 = st.columns([6, 20, 7])
            with col1:
                st.write("")
            with col2:
                st.markdown(tabela_final, unsafe_allow_html=True)
            with col3:
                st.write("")

def arguicao(base_resultados_2fase):

    base_resultados_2fase_arguicao = pd.DataFrame()
    base_resultados_2fase_arguicao = base_resultados_2fase
    
    base_resultados_2fase_arguicao2 = base_resultados_2fase_arguicao.drop(columns = ['Tema 1 - Comunicação assertiva','Tema 1 - Interação com pessoas','Tema 1 - Pensamento crítico','Tema 2 - Comunicação assertiva','Tema 2 - Interação com pessoas','Tema 2 - Pensamento crítico','Tema 3 - Comunicação assertiva','Tema 3 - Interação com pessoas','Tema 3 - Pensamento crítico','Tema 4 - Comunicação assertiva','Tema 4 - Interação com pessoas','Tema 4 - Pensamento crítico'])
   
    base_resultados_2fase_arguicao2['Nota 2º fase'] = 125*(base_resultados_2fase_arguicao2['Tema 1 - Aprender a aprender'] + base_resultados_2fase_arguicao2['Tema 2 - Aprender a aprender'])
    base_resultados_2fase_arguicao2aux = base_resultados_2fase_arguicao2[base_resultados_2fase_arguicao2['Nota 2º fase'] > 0]

    html_header_2fase = ""
    @st.cache
    def html_header_2fase():
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
        return html_header_2fase

    
    st.markdown(html_br(), unsafe_allow_html=True)
    st.markdown(html_header_2fase(), unsafe_allow_html=True)

    return base_resultados_2fase_arguicao2aux, base_resultados_2fase_arguicao2

@st.cache
def html_arguicao(base_resultados_2fase_arguicao2aux, numero_candidatos_deb_arg):

    html_card_header1 = ""
    @st.cache
    def html_card_header1():
        html_card_header1="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota</h4>
        </div>
        </div>
        """
        return html_card_header1

    html_card_footer1 = ""
    @st.cache
    def html_card_footer1():
        html_card_footer1="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota máxima: 1000</p>
        </div>
        </div>
        """
        return html_card_footer1

    html_card_footer_med1 = ""
    @st.cache
    def html_card_footer_med1(base_resultados_2fase_arguicao2aux):
        html_card_footer_med1="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(int(round(base_resultados_2fase_arguicao2aux['Nota 2º fase'].mean(),0)))+"""</p>
        </div>
        </div>
        """
        return html_card_footer_med1

    html_card_header3 = ""
    @st.cache
    def html_card_header3(base_resultados_2fase_arguicao2aux):
        html_card_header3="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Classificação</h4>
        </div>
        </div>
        """
        return html_card_header3
    
    html_card_footer3_arguicao = ""
    @st.cache
    def html_card_footer3_arguicao(numero_candidatos_deb_arg):
        html_card_footer3_arguicao="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos_deb_arg)+"""</p>
        </div>
        </div>
        """
        return html_card_footer3_arguicao
    
    return html_card_header1, html_card_footer1, html_card_footer_med1, html_card_header3, html_card_footer3

def arguicao_show(base_resultados_2fase_arguicao2, base_resultados_2fase_arguicao2aux, numero_candidatos_deb_arg):

    base_resultados_2fase_aluno_arguicao = base_resultados_2fase_arguicao2.sort_values(by = 'Nota 2º fase', ascending = False).reset_index(drop = True).reset_index()
    base_resultados_2fase_aluno_arguicao.rename(columns = {'index':'Classificação'}, inplace = True)

    base_resultados_2fase_aluno_arguicao2 = base_resultados_2fase_aluno_arguicao[base_resultados_2fase_aluno_arguicao['Login do aluno(a)'] == login_aluno].reset_index()

    if len(base_resultados_2fase_aluno_arguicao2) > 0:

        if base_resultados_2fase_aluno_arguicao2['Nota 2º fase'][0] == 0:
            base_resultados_2fase_aluno_arguicao2['Classificação'][0] = numero_candidatos_deb_arg + 1
        else:
            base_resultados_2fase_aluno_arguicao2['Classificação'][0] = base_resultados_2fase_aluno_arguicao2['Classificação'][0] + 1
    
    else:
        base_resultados_2fase_aluno_arguicao2 = pd.DataFrame(columns = ['Nota 2º fase','Classificação'], index=range(2))
        base_resultados_2fase_aluno_arguicao2['Nota 2º fase'][0] = 0
        base_resultados_2fase_aluno_arguicao2['Classificação'][0] = numero_candidatos_deb_arg + 1

    ### Block 1#########################################################################################
    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,20,1,20,1,20,1])
        with col1:
            st.write("")
        with col2:
            st.markdown(html_card_header1(), unsafe_allow_html=True)
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
            st.markdown(html_card_footer1(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_footer_med1(base_resultados_2fase_arguicao2aux), unsafe_allow_html=True)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_card_header3(base_resultados_2fase_arguicao2aux), unsafe_allow_html=True)
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
            st.markdown(html_card_footer3_arguicao(numero_candidatos_deb_arg), unsafe_allow_html=True)
        with col5:
            st.write("")
        with col6:
            st.write("")
        with col7:
            st.write("")
    
    st.markdown(html_br(), unsafe_allow_html=True)
    st.markdown(html_br(), unsafe_allow_html=True)

    ponto = str(round(100*(numero_candidatos_deb_arg-(base_resultados_2fase_aluno_arguicao2['Classificação'][0]-1))/numero_candidatos_deb_arg,0)).find('.')
    texto = str(round(100*(numero_candidatos_deb_arg-(base_resultados_2fase_aluno_arguicao2['Classificação'][0]-1))/numero_candidatos_deb_arg,0))[0:ponto]

    html_card_header_destaques_gerais = ""
    @st.cache
    def html_card_header_destaques_gerais(texto):
        html_card_header_destaques_gerais="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
        height: 150px;">
            <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
        </div>
        </div>
        """
        return html_card_header_destaques_gerais

        
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
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_header_destaques_gerais(texto), unsafe_allow_html=True)
        with col5:
            st.write("")

    base_resultados_2fase_arguicao3 = base_resultados_2fase_arguicao2[base_resultados_2fase_arguicao2['Login do aluno(a)'] == login_aluno].reset_index()

    if len(base_resultados_2fase_arguicao3) > 0:

        data2 = [
        {'Temas': 'Tema 1',  'Aprender a aprender - Resultado Individual': base_resultados_2fase_arguicao3['Tema 1 - Aprender a aprender'][0], 'Aprender a aprender - Resultado Geral': round(base_resultados_2fase_arguicao2aux['Tema 1 - Aprender a aprender'].mean(),1)},

        {'Temas': 'Tema 2', 'Aprender a aprender - Resultado Individual': base_resultados_2fase_arguicao3['Tema 2 - Aprender a aprender'][0], 'Aprender a aprender - Resultado Geral': round(base_resultados_2fase_arguicao2aux['Tema 2 - Aprender a aprender'].mean(),1)},

        {'Temas': 'Total', 'Aprender a aprender - Resultado Individual': round((base_resultados_2fase_arguicao3['Tema 1 - Aprender a aprender'][0]+base_resultados_2fase_arguicao3['Tema 2 - Aprender a aprender'][0])/2,1), 'Aprender a aprender - Resultado Geral': round((base_resultados_2fase_arguicao2aux['Tema 1 - Aprender a aprender'].mean() + base_resultados_2fase_arguicao2aux['Tema 2 - Aprender a aprender'].mean())/2,1)}
        ]

    else: 

        data2 = [
        {'Temas': 'Tema 1',  'Aprender a aprender - Resultado Individual': 0, 'Aprender a aprender - Resultado Geral': round(base_resultados_2fase_arguicao2aux['Tema 1 - Aprender a aprender'].mean(),1)},

        {'Temas': 'Tema 2', 'Aprender a aprender - Resultado Individual': 0, 'Aprender a aprender - Resultado Geral': round(base_resultados_2fase_arguicao2aux['Tema 2 - Aprender a aprender'].mean(),1)},

        {'Temas': 'Total', 'Aprender a aprender - Resultado Individual': 0, 'Aprender a aprender - Resultado Geral': round((base_resultados_2fase_arguicao2aux['Tema 1 - Aprender a aprender'].mean() + base_resultados_2fase_arguicao2aux['Tema 2 - Aprender a aprender'].mean())/2,1)}
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

    tabela_temas_arguicao['Temas'] = ['Tema 1 - Presos deveriam ser liberados devido ao risco de infecção por doenças transmitidas em aglomerações?','Tema 2 - A água ao invés de ser privatizada deveria ser um recurso público?']

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

    st.markdown(html_br(), unsafe_allow_html=True)

    with st.container():
            col1, col2, col3 = st.columns([3, 5, 3])
            with col1:
                st.write("")
            with col2:
                st.markdown(tabela_final2, unsafe_allow_html=True)
            with col3:
                st.write("")

def fase_1_2(resultados_gerais5, base_resultados_2fase, base_redacao_disciplina2):

    primeira_fase = resultados_gerais5
    primeira_fase2 = primeira_fase.drop(columns = ['Número da questão','Tempo na questão','Valor da questão','Acerto'])
    segunda_fase = base_resultados_2fase
    
    segunda_fase2 = segunda_fase.drop(columns = ['Tema 1 - Comunicação assertiva','Tema 2 - Comunicação assertiva','Tema 3 - Comunicação assertiva','Tema 4 - Comunicação assertiva', 'Tema 1 - Interação com pessoas', 'Tema 2 - Interação com pessoas', 'Tema 3 - Interação com pessoas', 'Tema 4 - Interação com pessoas', 'Tema 1 - Pensamento crítico', 'Tema 2 - Pensamento crítico', 'Tema 3 - Pensamento crítico', 'Tema 4 - Pensamento crítico', 'Tema 1 - Aprender a aprender', 'Tema 2 - Aprender a aprender']) 
    segunda_fase3 = pd.merge(segunda_fase2, base_redacao_disciplina2, on = 'Login do aluno(a)', how = 'outer')
    segunda_fase3.rename(columns = {'Nota na questão':'Nota Redação'}, inplace = True)

    segunda_fase3['Nota 2º fase'] = segunda_fase3['Nota 2º fase'].fillna(0)
    segunda_fase3['Nota Final 2º fase'] = 0.25*segunda_fase3['Nota Redação'] + 0.75*segunda_fase3['Nota 2º fase']
    primeira_fase2.rename(columns = {'Nota na questão':'Nota 1º fase'}, inplace = True)
    

    resultado_final = pd.merge(segunda_fase3, primeira_fase2, on = 'Login do aluno(a)', how = 'right')
    for i in range(len(resultado_final['Login do aluno(a)'])):
        if resultado_final['Nota 1º fase'][i] > 0:
            resultado_final['Nota 1º fase'][i] = resultado_final['Nota 1º fase'][i]
        else:
            resultado_final['Nota 1º fase'][i] = 0
    resultado_final['Nota Final'] = 0.00
    for i in range(len(resultado_final['Login do aluno(a)'])):
        #resultado_final['Nota Final'][i] = sqrt(sqrt(float(resultado_final['Nota 1º fase'][i])*float(resultado_final['Nota 1º fase'][i])*float(resultado_final['Nota 1º fase'][i])*float(resultado_final['Nota 2º fase'][i])))
        resultado_final['Nota Final'][i] = ((resultado_final['Nota 1º fase'][i]**3)*resultado_final['Nota Final 2º fase'][i])**0.25

    html_header_2fase = ""
    @st.cache
    def html_header_2fase():
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
        return html_header_2fase

    st.markdown(html_br(), unsafe_allow_html=True)
    st.markdown(html_header_2fase(), unsafe_allow_html=True)
    
    resultado_final2 = resultado_final[resultado_final['Nota Final 2º fase'] >= 0]
    
    resultado_finalaux = resultado_final[resultado_final['Nota Final 2º fase'] > 0]

    numero_candidatos = len(resultado_finalaux['Nome do aluno(a)'])

    return resultado_final, resultado_finalaux

@st.cache
def html_fase_1_2():

    html_card_header1 = ""
    @st.cache
    def html_card_header1():
        html_card_header1="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota</h4>
        </div>
        </div>
        """
        return html_card_header1

    html_card_footer1 = ""
    @st.cache
    def html_card_footer1():
        html_card_footer1="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Nota máxima: 1000</p>
        </div>
        </div>
        """
        return html_card_footer1

    html_card_footer_med1 = ""
    @st.cache
    def html_card_footer_med1(resultado_finalaux):
        html_card_footer_med1="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #FFA73E; padding-top: 12px; width: 350px;
        height: 50px;">
            <p class="card-title" style="background-color:#FFA73E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Média Geral: """+str(int(round(resultado_finalaux['Nota Final'].mean(),0)))+"""</p>
        </div>
        </div>
        """
        return html_card_footer_med1

    html_card_header3 = ""
    @st.cache
    def html_card_header3():
        html_card_header3="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <h4 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Classificação</h4>
        </div>
        </div>
        """
        return html_card_header3
    
    html_card_footer3 = ""
    @st.cache
    def html_card_footer3(numero_candidatos):
        html_card_footer3="""
        <div class="card">
        <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #9E089E; padding-top: 12px; width: 350px;
        height: 50px;">
            <p class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Quantidade de alunos: """+str(numero_candidatos)+"""</p>
        </div>
        </div>
        """
        return html_card_footer3
    
def fase_1_2_show(resultado_final, resultado_finalaux):

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
            st.markdown(html_card_header1(), unsafe_allow_html=True)
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
            st.markdown(html_card_footer1(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_card_footer_med1(base_resultados_2fase_arguicao2aux), unsafe_allow_html=True)
        with col3:
            st.write("")
        with col4:
            st.markdown(html_card_header3(base_resultados_2fase_arguicao2aux), unsafe_allow_html=True)
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
            st.markdown(html_card_footer3(numero_candidatos), unsafe_allow_html=True)
        with col5:
            st.write("")
        with col6:
            st.write("")
        with col7:
            st.write("")
    
    st.markdown(html_br(), unsafe_allow_html=True)
    st.markdown(html_br(), unsafe_allow_html=True)

    ponto = str(round(100*(numero_candidatos-(resultado_final_aluno2['Classificação'][0]-1))/numero_candidatos,0)).find('.')
    texto = str(round(100*(numero_candidatos-(resultado_final_aluno2['Classificação'][0]-1))/numero_candidatos,0))[0:ponto]

    html_card_header_destaques_gerais = ""
    @st.cache
    def html_card_header_destaques_gerais(texto):
        html_card_header_destaques_gerais="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #0010B3; padding-top: 60px; width: 495px;
        height: 150px;">
            <h5 class="card-title" style="background-color:#0010B3; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Você foi melhor que """+texto+"""% dos alunos!</h5>
        </div>
        </div>
        """ 
        return html_card_header_destaques_gerais

       
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
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            st.markdown(html_br(), unsafe_allow_html=True)
            if resultado_final_aluno2['Classificação'][0] <= numero_candidatos:
                st.markdown(html_card_header_destaques_gerais(texto), unsafe_allow_html=True)
        with col5:
            st.write("")

    html_final = ""
    @st.cache
    def html_final(texto):
        html_final="""
        <div class="card">
        <div class="card-body" style="border-radius: 10px 10px 10px 10px; background: #9E089E; padding-top: 20px; padding-bottom: 20px; width: 800px;
        height: 100px;">
            <h5 class="card-title" style="background-color:#9E089E; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Sucesso é o acúmulo de pequenos esforços, repetidos dia e noite. Robert Collier</h5>
        </div>
        </div>
        """ 
        return html_final 

    with st.container():
        col1, col2, col3 = st.columns([1,3,2.5])
        with col1:
            st.write("")
        with col2:
            st.markdown(html_final(texto), unsafe_allow_html=True)
        with col3:
            st.write("")  

if login_aluno != '':
    resultados_gerais3, turma_eng, turma_cien, base, base_resultados_2fase = leitura_bases_dados()
    
    resultados_gerais_aluno, resultados_gerais5, numero_candidatos, resultados_gerais4, alunos_fizeram, numero_eng_cien, turma_aluno, resultados_gerais_media_tempo_str, hours_aluno = fase_1(login_aluno, turma_eng, turma_cien, resultados_gerais3)
    
    fase_1_show(resultados_gerais_aluno, resultados_gerais5, numero_candidatos, resultados_gerais4, resultados_gerais_media_tempo_str, hours_aluno)
    
    base_alunos_fizeram, resultados_matematica, resultados_gerais_disciplina_med_mat, classificacao_aluno_mat, resultados_gerais_disciplina3_mat, resultados_ciencias_hum, resultados_linguagens, resultados_gerais_disciplina_med_lin, classificacao_aluno_lin, resultados_gerais_disciplina3_lin, resultados_ciencias_fim, resultados_gerais_disciplina_med_cie, classificacao_aluno_fim, resultados_gerais_disciplina3_fim, resultados_gerais_disciplina_med_hum = resultados_gerais_disciplina(base, alunos_fizeram)
    
    html_card_header1_disc, html_card_footer1_disc, html_card_footer1_disc_med_mat, html_card_footer1_disc_med_lin, html_card_footer1_disc_med_cie, html_card_header2_disc, html_card_footer2_disc, html_card_footer2_disc_med_mat, html_card_footer2_disc_med_lin, html_card_footer2_disc_med_cie, html_card_header3_disc, html_card_footer3_disc_matlin, html_card_footer3_disc = html_disciplinas(resultados_ciencias_hum, resultados_gerais_aluno, turma_eng, turma_cien)

    matematica_tabela3, matematica_tabela_verde_ordenado, matematica_tabela_vermelho_ordenado, matematica_media_tempo_str, matematica_aluno_tempo_str, hours_aluno_mat = tratamento_dados_mat(base_alunos_fizeram)
    
    mat_show(resultados_matematica, resultados_gerais_disciplina_med_mat, classificacao_aluno_mat, resultados_gerais_disciplina3_mat, matematica_media_tempo_str, matematica_aluno_tempo_str, hours_aluno_mat)

    html_table, html_card_header_melhores_resultados, html_card_header_melhores_resultados1, html_card_header_melhores_resultados2, html_card_header_melhores_resultados3, html_card_header_pontos_melhorar, html_card_header_pontos_melhorar1, html_card_header_pontos_melhorar2, html_card_header_pontos_melhorar3 = html_mat(matematica_tabela3, matematica_tabela_verde_ordenado, matematica_tabela_vermelho_ordenado)

    mat_show2()

    linguagens_tabela3, linguagens_tabela_verde_ordenado, linguagens_tabela_vermelho_ordenado, linguagens_media_tempo_str, hours_aluno_lin, linguagens_aluno_tempo_str = tratamento_dados_lin(base_alunos_fizeram)
    
    lin_show(resultados_linguagens, resultados_gerais_disciplina_med_lin, classificacao_aluno_lin, resultados_gerais_disciplina3_lin, linguagens_media_tempo_str, hours_aluno_lin, linguagens_aluno_tempo_str)

    html_table, html_card_header_melhores_resultados, html_card_header_melhores_resultados1, html_card_header_melhores_resultados2, html_card_header_melhores_resultados3, html_card_header_pontos_melhorar, html_card_header_pontos_melhorar1, html_card_header_pontos_melhorar2, html_card_header_pontos_melhorar3 = html_lin(linguagens_tabela3, linguagens_tabela_verde_ordenado, linguagens_tabela_vermelho_ordenado)

    lin_show2()

    ciencias_tabela3, ciencias_tabela_verde_ordenado, ciencias_tabela_vermelho_ordenado, hours_aluno_cie, ciencias_aluno_tempo_str, ciencias_media_tempo_str = tratamento_dados_cie(base_alunos_fizeram, resultados_gerais_aluno)

    cie_show(resultados_ciencias_fim, resultados_gerais_disciplina_med_cie, classificacao_aluno_fim, resultados_gerais_disciplina3_fim, numero_eng_cien, turma_eng, turma_cien, numero_candidatos, hours_aluno_cie, ciencias_aluno_tempo_str, ciencias_media_tempo_str)

    html_table_cie_hum, html_table_cie_nat, html_card_header_melhores_resultados_cie, html_card_header_melhores_resultados1_cie, html_card_header_melhores_resultados2_cie, html_card_header_melhores_resultados3_cie, html_card_header_pontos_melhorar_cie, html_card_header_pontos_melhorar1_cie, html_card_header_pontos_melhorar2_cie, html_card_header_pontos_melhorar3_cie = html_cie(ciencias_tabela3, turma_aluno, turma_eng, turma_cien, ciencias_tabela_verde_ordenado, ciencias_tabela_vermelho_ordenado)

    cie_show2(turma_aluno, turma_eng, turma_cien)

    base_redacao2, redacao_aluno_media, redacao_tabela3, redacao_tabela_verde_ordenado, redacao_tabela_vermelho_ordenado, redacao_aluno_tempo_str, redacao_media_tempo_str, hours_aluno_red = tratamento_dados_red()

    base_redacao_disciplina2 = red_show(base_redacao2, redacao_aluno_media, redacao_tabela3, redacao_aluno_tempo_str, redacao_media_tempo_str, hours_aluno_red)

    html_table, html_card_header_melhores_resultados, html_card_header_melhores_resultados1, html_card_header_melhores_resultados2, html_card_header_melhores_resultados3, html_card_header_pontos_melhorar, html_card_header_pontos_melhorar1, html_card_header_pontos_melhorar2, html_card_header_pontos_melhorar3 = html_red(redacao_tabela3, redacao_tabela_verde_ordenado, redacao_tabela_vermelho_ordenado)

    red_show2(redacao_tabela3)

    fotos_questao(turma_aluno, turma_eng, turma_cien)

    detalhamento(base)

    numero_candidatos_2fase, segunda_fase4 = fase_2(base_resultados_2fase)

    html_card_header1, html_card_footer1, html_card_footer_med1, html_card_header3, html_card_footer3 = html_fase_2()

    fase_2_show(numero_candidatos_2fase, segunda_fase4)

    base_resultados_2fase_debate2aux, base_resultados_2fase_debate2, numero_candidatos_deb_arg = debate(base_resultados_2fase)

    html_card_header1, html_card_footer1, html_card_footer_med1, html_card_header3, html_card_footer3_debate = html_debate(base_resultados_2fase_debate2aux, numero_candidatos_deb_arg)

    debate_show(base_resultados_2fase_debate2, base_resultados_2fase_debate2aux, numero_candidatos_deb_arg)

    base_resultados_2fase_arguicao2aux, base_resultados_2fase_arguicao2 = arguicao(base_resultados_2fase)

    html_card_header1, html_card_footer1, html_card_footer_med1, html_card_header3, html_card_footer3_arguicao = html_arguicao(base_resultados_2fase_arguicao2aux, numero_candidatos_deb_arg)

    arguicao_show(base_resultados_2fase_arguicao2, base_resultados_2fase_arguicao2aux, numero_candidatos_deb_arg)

    resultado_final, resultado_finalaux = fase_1_2(resultados_gerais5, base_resultados_2fase, base_redacao_disciplina2)

    html_fase_1_2()

    fase_1_2_show(resultado_final, resultado_finalaux)












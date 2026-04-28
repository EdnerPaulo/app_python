import streamlit as st
# sqlalchemy
# modelagem
from sqlalchemy.ext.declarative import declarative_base
# drive motor a conexão
from sqlalchemy import create_engine, Column, Integer, String
# perssistencia  - ler e salvar
from sqlalchemy.orm import sessionmaker

# url  - banco de dados
URL = 'postgresql://neondb_owner:***************@ep-fragrant-voice-anlgsfiw-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

engine = create_engine(URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# classe da base do itinerario ORM (Object-Relational Mapping ou Mapeamento Objeto-Relacional)

class Itinerario(Base):
    __tablename__ = 'Itinerario_de_Aula' 
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    descricao = Column(String)

Base.metadata.create_all(engine)


st.set_page_config(page_title='FORMULARIO DE ITINERARIO')
st.title('CADASTRO DE ITINERARIO 2026')
st.info('OS DADOS SERÃO SALVOS DIRETAMENTE NO POSTGREESQL DA NUVEM NEON.TECH')

with st.form('Formulario', clear_on_submit=True):
    nome_input = st.text_input('NOME DO ITINERARIO')
    desc_input = st.text_input('DESCRIÇÃO')
    botao = st.form_submit_button('SALVAR DADOS')

if botao:
    if nome_input:
        session = Session()
        novo_registro = Itinerario(nome = nome_input, descricao = desc_input)
        session.add(novo_registro)
        session.commit()
        session.close()
        st.success(f'SUCESSO {nome_input} FOI SALVO COM SUCESSO')
    else:
        st.error('Por favor, preemcha corretamente')

# atualização em tempo real
st.divider()
st.subheader('REGISTRO ATUAL')
session = Session()
dados = session.query(Itinerario).all()
session.close()

if dados :
    for item in dados:
        st.write(f'{item.nome}: {item.descricao}')
        


import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# url  -  banco de dados
URL_NEON = 'postgresql://neondb_owner:npg_dYP6QxoeOk1D@ep-fragrant-voice-anlgsfiw-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require'

engine = create_engine(URL_NEON)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# --- 2. O ORM (MAPEAMENTO) ---
# Explique que esta classe vira a tabela no banco de dados
class Itinerario(Base):
    __tablename__ = 'itinerarios_aula'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    descricao = Column(String)

# Comando que cria a tabela no Neon automaticamente
Base.metadata.create_all(engine)





# FRAME STREAMLIT INTERFACE GRAFICA 
st.set_page_config(page_title="Aula SQL + ORM", page_icon="")
st.title(" Cadastro de Itinerários 2026")
st.info("Os dados abaixo serão salvos diretamente no PostgreSQL da nuvem (Neon.tech).")

with st.form("form_itinerario", clear_on_submit=True):
    nome_input = st.text_input("Nome do Itinerário")
    desc_input = st.text_area("Breve Descrição")
    botao = st.form_submit_button("Salvar no Banco de Dados")

if botao:
    if nome_input:
        # O ORM traduzindo o objeto para SQL e salvando
        session = Session()
        novo_registro = Itinerario(nome=nome_input, descricao=desc_input)
        session.add(novo_registro)
        session.commit()
        session.close()
        st.success(f"Sucesso! '{nome_input}' foi gravado no Neon Tech.")
    else:
        st.error("Por favor, preencha o nome do itinerário.")

# --- VISUALIZAÇÃO EM TEMPO REAL ---
st.divider()
st.subheader("Registros Atuais no Postgres")
session = Session()
dados = session.query(Itinerario).all()
session.close()

if dados:
    for item in dados:
        st.write(f" **{item.nome}**: {item.descricao}")
import streamlit as st
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, event
from sqlalchemy.orm import sessionmaker
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title='SISTEMA DE ITINERÁRIO', layout='centered')

# --- CONEXÃO COM O BANCO DE DADOS ---
# Usamos cache para evitar que o Streamlit crie novas conexões a cada refresh
@st.cache_resource
def configurar_banco():
    # URL com sslmode obrigatorio para Neon
    URL = 'postgresql://neondb_owner:npg_dYP6QxoeOk1D@ep-fragrant-voice-anlgsfiw-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require'
    
    try:
        # pool_pre_ping: testa a conexão antes de cada operação
        # pool_recycle: renova a conexão a cada 300 segundos para evitar queda pelo servidor
        engine = create_engine(
            URL, 
            pool_pre_ping=True, 
            pool_recycle=300,
            connect_args={"connect_timeout": 10}
        )
        return engine
    except Exception as e:
        st.error(f"Erro ao configurar o motor do banco: {e}")
        return None

engine = configurar_banco()
Session = sessionmaker(bind=engine)
Base = declarative_base()

# --- MODELO DA TABELA ---
class Itinerario(Base):
    __tablename__ = 'itinerarios_2026' # Nome sem espaços para evitar erros de SQL
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)

# Tenta criar a tabela apenas se a conexão estiver ativa
if engine:
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        st.warning("Aviso: Não foi possível verificar/criar tabelas. Verifique sua conexão de rede.")
        st.stop()

# --- INTERFACE STREAMLIT ---
st.title('🚀 CADASTRO DE ITINERÁRIO 2026')
st.caption('Conectado ao PostgreSQL (Neon.tech)')

# Formulário de entrada
with st.form('meu_formulario', clear_on_submit=True):
    nome_input = st.text_input('NOME DO ITINERÁRIO')
    desc_input = st.text_area('DESCRIÇÃO DO CONTEÚDO')
    botao_salvar = st.form_submit_button('SALVAR NO BANCO')

# Lógica para salvar
if botao_salvar:
    if nome_input:
        session = Session()
        try:
            # CORREÇÃO: Usando argumentos nomeados (nome=...)
            novo_item = Itinerario(nome=nome_input, descricao=desc_input)
            session.add(novo_item)
            session.commit()
            st.success(f"✅ '{nome_input}' salvo com sucesso!")
            time.sleep(1) # Pequena pausa para o banco processar
            st.rerun()    # Recarrega a página para mostrar o dado novo
        except Exception as e:
            session.rollback()
            st.error(f"Erro ao salvar: {e}")
        finally:
            session.close()
    else:
        st.error("O campo 'NOME' é obrigatório!")

# --- EXIBIÇÃO DOS DADOS ---
st.divider()
st.subheader('📋 REGISTROS NO BANCO')

if engine:
    session = Session()
    try:
        registros = session.query(Itinerario).all()
        if registros:
            for item in registros:
                with st.expander(f"📍 {item.nome}"):
                    st.write(f"**Descrição:** {item.descricao}")
                    st.caption(f"ID no Banco: {item.id}")
        else:
            st.info("Nenhum registro encontrado.")
    except Exception as e:
        st.error(f"Erro ao ler dados: {e}")
    finally:
        session.close()
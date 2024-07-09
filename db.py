"""
Objetos do sqlalchemy core para a realização da conexão e operação do Banco de Dados
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


DB_CONNECTION = 'sqlite:///mydatabase.db' #para mudar de banco de dados basta trocar essa string, consultar slide
engine = create_engine(DB_CONNECTION, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

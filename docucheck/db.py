import sqlalchemy as sa
import datetime as dt
from sqlalchemy.orm import (
    Mapped,
    mapped_column, 
    sessionmaker, 
    declarative_base,
    relationship
)

engine = sa.create_engine("postgresql+psycopg2://postgres:postgres@localhost/test")
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Consulta(Base):
    __tablename__ = "consulta"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    data_consulta: Mapped[dt.date] = mapped_column(sa.Date, nullable=False)
    id_empresa: Mapped[int] = mapped_column(sa.ForeignKey("empresa.id"), nullable=False)
    
    empresa = relationship("Empresa", back_populates="consulta")

    def __init__ (self, data_consulta: dt.date, id_empresa: int):
        super().__init__()
        self.data_consulta = data_consulta
        self.id_empresa = id_empresa
    
    def __repr__(self):
        return f"<Consulta(id={self.id}, data_consulta={self.data_consulta}, id_empresa={self.id_empresa})>"

class Documento(Base):
    __tablename__ = "documento"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    tipo: Mapped[str] = mapped_column(sa.VARCHAR(255), nullable=False)

    def __init__ (self, tipo: str):
        super().__init__()
        self.tipo = tipo
        
    def __repr__(self):
        return f"<Documento(id={self.id}, tipo={self.tipo})>"
    
class Empresa(Base):
    __tablename__ = "empresa"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(sa.VARCHAR(255), nullable=False)
    cnpj: Mapped[str] = mapped_column(sa.CHAR(11), nullable=False)
    email: Mapped[str] = mapped_column(sa.VARCHAR(255), nullable=False)

    consultas = relationship("Consulta", back_populates="empresa")
    documentos = relationship("EmpresaDocumento", back_populates="empresa")

    def __init__ (self, nome: str, cnpj: str, email: str):
        super().__init__()
        self.nome = nome
        self.cnpj = cnpj
        self.email = email

    def __repr__(self):
        return f"<Empresa(id={self.id}, nome={self.nome}, cnpj={self.cnpj}, email={self.email})>"
        
class EmpresaDocumento(Base):
    __tablename__ = "empresa_documento"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    data_inicio: Mapped[dt.date] = mapped_column(sa.Date, nullable=False)
    data_vencimento: Mapped[dt.date] = mapped_column(sa.Date, nullable=False)
    id_empresa: Mapped[int] = mapped_column(sa.ForeignKey("empresa"), nullable=False)
    id_documento: Mapped[int] = mapped_column(sa.ForeignKey("documento"), nullable=False)
    
    empresa = relationship("Empresa", back_populates="documentos")
    documento = relationship("Documento")
    
    def __init__ (self, data_inicio: dt.date, data_vencimento: dt.date, id_empresa: int, id_documento: int):
        super().__init__()
        self.data_inicio = data_inicio
        self.data_vencimento = data_vencimento
        self.id_empresa = id_empresa
        self.id_documento = id_documento
    
    def __repr__(self):
        return f"<EmpresaDocumento(id={self.id}, data_inicio={self.data_inicio}, data_vencimento={self.data_vencimento}, id_empresa={self.id_empresa}, id_documento={self.id_documento})>"
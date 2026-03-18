from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    telefone = Column(String(20))
    cpf = Column(String(14), nullable=False, unique=True)  # Novo campo
    senha_hash = Column(String(255), nullable=False)

    reservas = relationship("Reserva", back_populates="cliente")  # Relacionamento com Reserva

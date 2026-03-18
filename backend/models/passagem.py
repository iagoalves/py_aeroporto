from sqlalchemy import Column, Integer, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Passagem(Base):
    __tablename__ = 'passagens'

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    voo_id = Column(Integer, ForeignKey('voos.id'), nullable=False)

    # Relacionamentos
    cliente = relationship("Cliente", back_populates="passagens")
    voo = relationship("Voo", back_populates="passagens")

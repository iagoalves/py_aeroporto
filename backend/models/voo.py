from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.types import DECIMAL

class Voo(Base):
    __tablename__ = 'voo'

    id = Column(Integer, primary_key=True, index=True)
    numero_voo = Column(String(20), nullable=False)
    companhia_id = Column(Integer, ForeignKey("companhia_aerea.id"), nullable=False)
    origem_id = Column(Integer, ForeignKey("aeroporto.id"), nullable=False)
    destino_id = Column(Integer, ForeignKey("aeroporto.id"), nullable=False)
    aeronave_id = Column(Integer, ForeignKey("aeronave.id"), nullable=False)  # Adicionando a chave estrangeira
    partida_prevista = Column(DateTime, nullable=False)
    chegada_prevista = Column(DateTime, nullable=False)
    custo = Column(DECIMAL(10, 2), nullable=False)

    companhia = relationship("CompanhiaAerea", back_populates="voos")
    aeronave = relationship("Aeronave", back_populates="voos")  # Relacionamento com Aeronave
    origem = relationship("Aeroporto", foreign_keys=[origem_id], back_populates="voos_origem")
    destino = relationship("Aeroporto", foreign_keys=[destino_id], back_populates="voos_destino")

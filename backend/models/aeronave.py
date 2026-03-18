from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Aeronave(Base):
    __tablename__ = 'aeronave'

    id = Column(Integer, primary_key=True, index=True)
    modelo = Column(String(100), nullable=False)
    capacidade = Column(Integer, nullable=False)
    companhia_id = Column(Integer, ForeignKey("companhia_aerea.id"), nullable=False)

    companhia = relationship("CompanhiaAerea", back_populates="aeronaves")
    voos = relationship("Voo", back_populates="aeronave")  # Relacionamento com Voo

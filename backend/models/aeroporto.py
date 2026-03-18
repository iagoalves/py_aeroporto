from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base

class Aeroporto(Base):
    __tablename__ = 'aeroporto'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    estado = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    pais = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    codigo_iata = Column(String(10))
    codigo_icao = Column(String(10))

    voos_origem = relationship("Voo", foreign_keys='Voo.origem_id', back_populates="origem")
    voos_destino = relationship("Voo", foreign_keys='Voo.destino_id', back_populates="destino")
    companhias = relationship("models.companhia_aeroporto.CompanhiaAeroporto", back_populates="aeroporto")


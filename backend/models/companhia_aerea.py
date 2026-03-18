from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class CompanhiaAerea(Base):
    __tablename__ = 'companhia_aerea'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)

    voos = relationship("Voo", back_populates="companhia")
    aeroportos = relationship("CompanhiaAeroporto", back_populates="companhia")
    aeronaves = relationship("Aeronave", back_populates="companhia")

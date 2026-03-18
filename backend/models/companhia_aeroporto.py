from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class CompanhiaAeroporto(Base):
    __tablename__ = 'companhia_aeroporto'

    id = Column(Integer, primary_key=True, index=True)
    companhia_id = Column(Integer, ForeignKey("companhia_aerea.id"), nullable=False)
    aeroporto_id = Column(Integer, ForeignKey("aeroporto.id"), nullable=False)

    companhia = relationship("CompanhiaAerea", back_populates="aeroportos")
    aeroporto = relationship("Aeroporto", back_populates="companhias")

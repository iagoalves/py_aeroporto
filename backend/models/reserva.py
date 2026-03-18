from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from models.database import Base

class Reserva(Base):
    __tablename__ = 'reservas'
    id = Column(Integer, primary_key=True)
    voo_id = Column(Integer)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    localizador = Column(String)
    numero_eticket = Column(String)
    status_pagamento = Column(String(20), default="pendente")
    cliente = relationship("Cliente", back_populates="reservas")

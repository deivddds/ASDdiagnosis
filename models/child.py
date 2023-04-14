from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.database import Base

class Niño(Base):
    __tablename__ = "niños"

    id_niño = Column(Integer, primary_key=True)
    dni_profesional = Column(String, ForeignKey("profesionales.dni"))
    nombre = Column(String)
    apellidos = Column(String)
    fecha_nacimiento = Column(Date)
    genero = Column(String)
    antecedentes_familiares = Column(String)
    diagnostico_previo = Column(String)
    observaciones = Column(String)
    color = Column(String)

    profesional = relationship("Profesional", back_populates="niños")
    diagnosticos = relationship("Diagnosis", back_populates="niño")

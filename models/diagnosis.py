from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import Base

class Diagnosis(Base):
    __tablename__ = "diagnosticos"

    id_diagnostico = Column(Integer, primary_key=True)
    id_niño = Column(Integer, ForeignKey("niños.id_niño"))
    fecha_diagnostico = Column(String)
    foto = Column(String)
    bloque2_variables = Column(String)
    bloque3_variables = Column(String)

    niño = relationship("Niño", back_populates="diagnosticos") 

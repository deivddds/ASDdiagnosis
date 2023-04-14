from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import Base

class Profesional(Base):
    __tablename__ = "profesionales"

    dni = Column(String, primary_key=True)
    nombre = Column(String)
    disciplina = Column(String)
    hashed_pass = Column(String)

    niños = relationship("Niño", back_populates="profesional")  # Utilizar el nombre de la clase como string

    def set_password(self, password):
        self.hashed_pass = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    @classmethod
    def verify_profesional(cls, session, dni, password):
        profesional = session.query(cls).filter(cls.dni == dni).first()
        if profesional is None:
            return False

        return check_password_hash(profesional.hashed_pass, password)

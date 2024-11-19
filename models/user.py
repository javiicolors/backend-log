from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from supabase_ import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # Relación con Download
    downloads = relationship("Download", back_populates="user", cascade="all, delete-orphan")


    # Método de clase para cifrar la contraseña
    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    # Método de instancia para verificar la contraseña
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

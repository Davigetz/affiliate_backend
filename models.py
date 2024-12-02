from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Modelo de Usuario
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    products = relationship("Product", back_populates="owner")


# Modelo de Producto actualizado
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    affiliate_link = Column(String, nullable=False)
    clicks = Column(Integer, default=0)  # Nuevo campo para clics
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")
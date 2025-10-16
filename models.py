from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class DecBase(DeclarativeBase):
    pass

class Pelicula(DecBase):
    __tablename__ = "peliculas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, unique=True, index=True, nullable=False)
    genero = Column(String, nullable=False)
    disponible = Column(Boolean, default=True)

    alquileres = relationship("Alquiler", back_populates="pelicula")

    # Métodos de negocio
    def alquilar_peli(self):
        if not self.disponible:
            raise ValueError("La película ya está alquilada")
        self.disponible = False

    def devolver_peli(self):
        self.disponible = True

class Cliente(DecBase): 
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)

    alquileres = relationship("Alquiler", back_populates="cliente")

class Alquiler(DecBase): 
    __tablename__ = "alquileres"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    pelicula_id = Column(Integer, ForeignKey("peliculas.id"), nullable=False, unique=True) # Solo una persona puede alquilar a la vez

    cliente = relationship("Cliente", back_populates="alquileres")
    pelicula = relationship("Pelicula", back_populates="alquileres")
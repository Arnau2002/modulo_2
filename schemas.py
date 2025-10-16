from pydantic import BaseModel, ConfigDict
from typing import Optional



# PELICULA SCHEMAS

# Esquema base usado para crear/actualizar
# donde el cliente no conoce ni envía el 'id' ni el estado 'disponible'
class PeliculaBase(BaseModel):
    titulo: str
    genero: str

# Esquema usado para la respuesta de la API (incluye ID y disponible)
class Pelicula(PeliculaBase):
    id: int
    disponible: bool

    model_config = ConfigDict(from_attributes=True) # Permite mapeo con SQLAlchemy ORM (anteriormente orm_mode = True)





# CLIENTE SCHEMAS

class ClienteBase(BaseModel):
    nombre: str

class Cliente(ClienteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)





# ALQUILER SCHEMAS

# necesitamos saber el ID del cliente y la película a alquilar.
class AlquilerBase(BaseModel):
    cliente_id: int
    pelicula_id: int

class Alquiler(AlquilerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
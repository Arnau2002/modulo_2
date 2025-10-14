from pydantic import BaseModel

# Clase Pydantic
class Pelicula(BaseModel):
    id: int | None = None
    titulo: str
    genero: str
    disponible: bool = True

    # Métodos
    def alquilar(self):
        if not self.disponible:
            raise ValueError("La película ya está alquilada")
        self.disponible = False

    def devolver(self):
        self.disponible = True
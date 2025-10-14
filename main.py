from fastapi import FastAPI, HTTPException
from clases.pelicula import Pelicula

app = FastAPI(title="API Videoclub", version="1.0.1")


# Base de datos en memoria
peliculas: list[Pelicula] = []


@app.get("/peliculas/", response_model=list[Pelicula])
def listar_peliculas():
    """Devuelve la lista de películas"""
    return peliculas


@app.post("/peliculas/", response_model=Pelicula)
def agregar_pelicula(pelicula: Pelicula):
    """Crea una nueva película si no existe otra con el mismo título"""
    # Verificar si ya existe una película con el mismo título
    for peli in peliculas:
        if peli.titulo.lower() == pelicula.titulo.lower():
            raise HTTPException(status_code=400, detail="Ya existe una película con ese título")

    nueva_id = len(peliculas) + 1
    nueva_pelicula = Pelicula(id=nueva_id, titulo=pelicula.titulo, genero=pelicula.genero)
    peliculas.append(nueva_pelicula)
    return nueva_pelicula


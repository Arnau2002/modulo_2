from fastapi import FastAPI, HTTPException
from clases.pelicula import Pelicula

app = FastAPI(title="API Videoclub", version="1.0.1")


# Base de datos en memoria
peliculas: list[Pelicula] = []




# endpoints para gestionar películas

@app.get("/peliculas/", response_model=list[Pelicula])
def listar_peliculas():
    """Devuelve la lista de películas"""
    return peliculas




@app.post("/peliculas/", response_model=Pelicula)
def agregar_pelicula(pelicula: Pelicula):
    """Crea una nueva película si no existe otra con el mismo título"""
    # Verificar si ya existe una película con el mismo título
    for peli in peliculas:
        if peli.titulo.lower() == pelicula.titulo.lower(): # evitar duplicados ignorando mayúsculas
            raise HTTPException(status_code=400, detail="Ya existe una película con ese título")

    nueva_id = len(peliculas) + 1
    nueva_pelicula = Pelicula(id=nueva_id, titulo=pelicula.titulo, genero=pelicula.genero)
    peliculas.append(nueva_pelicula)
    return nueva_pelicula






# endpoints para alquilar y devolver películas


@app.post("/peliculas/{pelicula_id}/alquilar", response_model=Pelicula)
def alquilar_pelicula(pelicula_id: int):
    
    # Buscamos la película por su ID
    pelicula = next((peli for peli in peliculas if peli.id == pelicula_id), None)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    # Intentamos alquilar, si ya estaba alquilada lanza error
    try:
        pelicula.alquilar()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return pelicula



@app.post("/peliculas/{pelicula_id}/devolver", response_model=Pelicula)
def devolver_pelicula(pelicula_id: int): #marcar película como disponible (devuelta)
    pelicula = next((p for p in peliculas if p.id == pelicula_id), None)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    pelicula.devolver()
    return pelicula
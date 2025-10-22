from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import crud

from database import engine, SessionLocal
from models import DecBase, Pelicula as ORM_Pelicula, Cliente as ORM_Cliente
from schemas import (
    Pelicula as SchemaPelicula, 
    PeliculaBase as SchemaPeliculaBase,
    Cliente as SchemaCliente,
    ClienteBase as SchemaClienteBase,
    Alquiler as SchemaAlquiler,
    AlquilerBase as SchemaAlquilerBase
)

app = FastAPI(title="API Videoclub (GET, POST, DELETE)", version="1.0.4")

# Crear todas las tablas
DecBase.metadata.create_all(bind=engine)

# estructura para la comunicación con base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





# --> ENDPOINTS PELÍCULAS (GET, POST, DELETE)


@app.get("/peliculas/", response_model=list[SchemaPelicula])
def listar_peliculas(db: Session = Depends(get_db)):
    # Se devuelve la lista de películas
    return crud.get_peliculas(db=db)

@app.post("/peliculas/", response_model=SchemaPelicula, status_code=status.HTTP_201_CREATED)
def agregar_pelicula(pelicula: SchemaPeliculaBase, db: Session = Depends(get_db)):
    # Se crea una nueva película.
    try:
        return crud.create_pelicula(db=db, pelicula=pelicula)
    except IntegrityError:
        # Captura el error relanzado por crud.py
        raise HTTPException(status_code=400, detail="Ya existe una película con ese título")

@app.delete("/peliculas/{pelicula_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    # Se elimina una película por su ID
    if not crud.delete_recurso(db=db, orm_model=ORM_Pelicula, item_id=pelicula_id):
        raise HTTPException(status_code=404, detail="Película no encontrada")
    # No retorna contenido (204 NO CONTENT)






# --> ENDPOINTS CLIENTES (GET, POST, DELETE)


@app.get("/clientes/", response_model=list[SchemaCliente])
def listar_clientes(db: Session = Depends(get_db)):
    return crud.get_clientes(db=db)

@app.post("/clientes/", response_model=SchemaCliente, status_code=status.HTTP_201_CREATED)
def agregar_cliente(cliente: SchemaClienteBase, db: Session = Depends(get_db)):
    # Se crea un nuevo cliente.
    try:
        return crud.create_cliente(db=db, cliente=cliente)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Ya existe un cliente con ese nombre")

@app.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    # Elimina 3l cliente por su ID.
    if not crud.delete_recurso(db=db, orm_model=ORM_Cliente, item_id=cliente_id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")






# --> ENDPOINTS ALQUILERES (GET, POST, DELETE - simular Transacciones)

@app.get("/alquileres/", response_model=list[SchemaAlquiler])
def listar_alquileres(db: Session = Depends(get_db)):
    return crud.get_alquileres(db=db)

@app.post("/alquileres/", response_model=SchemaAlquiler, status_code=status.HTTP_201_CREATED)
def crear_alquiler(alquiler_data: SchemaAlquilerBase, db: Session = Depends(get_db)):
    # Crea un nuevo alquiler, verificando stock y existencia.
    
    # Llama a la función transaccional de crud.py
    alquiler, error = crud.create_alquiler_transaccion(
        db=db, 
        cliente_id=alquiler_data.cliente_id, 
        pelicula_id=alquiler_data.pelicula_id
    )
    
    if error == "Recurso no encontrado":
        raise HTTPException(status_code=404, detail="Cliente o Película no encontrado")
    elif error:
        raise HTTPException(status_code=400, detail=error)
        
    return alquiler

@app.delete("/alquileres/{alquiler_id}", status_code=status.HTTP_204_NO_CONTENT)
def devolver_pelicula_formal(alquiler_id: int, db: Session = Depends(get_db)):
    # Elimina el registro de alquiler y marca la película como disponible (Devolución)
    if not crud.delete_alquiler_devolucion(db=db, alquiler_id=alquiler_id):
        raise HTTPException(status_code=404, detail="Registro de alquiler no encontrado")
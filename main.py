from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import engine, SessionLocal
from models import DecBase, Pelicula as ORM_Pelicula, Cliente as ORM_Cliente, Alquiler as ORM_Alquiler
from schemas import (
    Pelicula as SchemaPelicula, 
    PeliculaBase as SchemaPeliculaBase,
    Cliente as SchemaCliente,
    ClienteBase as SchemaClienteBase,
    Alquiler as SchemaAlquiler,
    AlquilerBase as SchemaAlquilerBase
)

app = FastAPI(title="API Videoclub (SQLAlchemy)", version="1.0.3")

# Crear todas las tablas
DecBase.metadata.create_all(bind=engine)


# estructura para la comunicación con base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()







# --> ENDPOINTS GESTIÓN DE PELÍCULAS

@app.get("/peliculas/", response_model=list[SchemaPelicula])
def listar_peliculas(db: Session = Depends(get_db)):
    """Devuelve la lista de películas"""
    return db.query(ORM_Pelicula).all()


@app.post("/peliculas/", response_model=SchemaPelicula)
def agregar_pelicula(pelicula: SchemaPeliculaBase, db: Session = Depends(get_db)): # Crea una nueva película si no existe otra con el mismo título"
    
    nueva_pelicula = ORM_Pelicula(**pelicula.model_dump()) # Crea instancia del modelo ORM

    try:
        db.add(nueva_pelicula) #registramos película
        db.commit()
        db.refresh(nueva_pelicula)
        return nueva_pelicula
    except IntegrityError:
        db.rollback() # # Si algo falla  por ejemplo:título repetido, deshacemos la transacción.
        raise HTTPException(status_code=400, detail="Ya existe una película con ese título")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")











# --> ENDPOINTS CLIENTES

@app.get("/clientes/", response_model=list[SchemaCliente])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(ORM_Cliente).all()


@app.post("/clientes/", response_model=SchemaCliente)
def agregar_cliente(cliente: SchemaClienteBase, db: Session = Depends(get_db)):
    """Crea un nuevo cliente si no existe otro con el mismo nombre"""
    nuevo_cliente = ORM_Cliente(**cliente.model_dump())

    try:
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)
        return nuevo_cliente
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Ya existe un cliente con ese nombre")






# --> ENDPOINTS ALQUILERES


@app.get("/alquileres/", response_model=list[SchemaAlquiler])
def listar_alquileres(db: Session = Depends(get_db)):
    """Lista todos los alquileres existentes"""
    return db.query(ORM_Alquiler).all()

@app.post("/alquileres/", response_model=SchemaAlquiler)
def crear_alquiler(alquiler_data: SchemaAlquilerBase, db: Session = Depends(get_db)):
    """
    Crea un nuevo alquiler asociando un cliente y una película.
    Verifica que existan ambos y que la película esté disponible.
    """
    cliente = db.query(ORM_Cliente).filter(ORM_Cliente.id == alquiler_data.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    pelicula = db.query(ORM_Pelicula).filter(ORM_Pelicula.id == alquiler_data.pelicula_id).first()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    # Intentamos alquilar la película (modifica su estado disponible)
    try:
        pelicula.alquilar_peli()
        
        # Crear el registro del alquiler
        nuevo_alquiler = ORM_Alquiler(
            cliente_id=cliente.id,
            pelicula_id=pelicula.id
        )
        
        db.add(nuevo_alquiler)
        db.commit()
        db.refresh(nuevo_alquiler)
        return nuevo_alquiler
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="La película ya está alquilada (registro de alquiler existente)")
    




@app.delete("/alquileres/{alquiler_id}", status_code=204)

# Elimina el registro de alquiler por ID y marca la película como disponible (Devolución)
def devolver_pelicula_formal(alquiler_id: int, db: Session = Depends(get_db)):
    
    # Buscar el registro de alquiler
    alquiler = db.query(ORM_Alquiler).filter(ORM_Alquiler.id == alquiler_id).first()
    if not alquiler:
        raise HTTPException(status_code=404, detail="Registro de alquiler no encontrado")

    # Guardamos el ID de la película antes de borrar el registro de alquiler
    pelicula_id = alquiler.pelicula_id 

    # Eliminar el registro de alquiler (DELETE)
    db.delete(alquiler)
    
    # Marcar la película como disponible (Stock)
    pelicula = db.query(ORM_Pelicula).filter(ORM_Pelicula.id == pelicula_id).first()
    if pelicula:
        pelicula.devolver_peli() # Llama al método de models.py para cambiar el stock

    # Confirmar el borrado de alquiler y cambio de stock
    db.commit()
    
    return {"message": "Devolución completada."}
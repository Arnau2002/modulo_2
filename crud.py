# crud.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Pelicula, Cliente, Alquiler
from schemas import PeliculaBase, ClienteBase # Solo necesitamos los esquemas base para la entrada

# ------------------------------------
# OPERACIONES CRUD GENÉRICAS
# ------------------------------------

def get_peliculas(db: Session):
    """Lee todas las películas."""
    return db.query(Pelicula).all()

def get_clientes(db: Session):
    """Lee todos los clientes."""
    return db.query(Cliente).all()

def get_alquileres(db: Session):
    """Lee todos los alquileres activos."""
    return db.query(Alquiler).all()

def create_pelicula(db: Session, pelicula: PeliculaBase):
    """Crea una película y maneja el error de integridad (título único)."""
    nueva_pelicula = Pelicula(**pelicula.model_dump())
    try:
        db.add(nueva_pelicula)
        db.commit()
        db.refresh(nueva_pelicula)
        return nueva_pelicula
    except IntegrityError:
        db.rollback()
        # Relanzamos la excepción para que main.py la maneje con un HTTPException
        raise IntegrityError("Ya existe una película con ese título", None, None)

def create_cliente(db: Session, cliente: ClienteBase):
    """Crea un cliente y maneja el error de integridad (nombre único)."""
    nuevo_cliente = Cliente(**cliente.model_dump())
    try:
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)
        return nuevo_cliente
    except IntegrityError:
        db.rollback()
        raise IntegrityError("Ya existe un cliente con ese nombre", None, None)

def delete_recurso(db: Session, orm_model, item_id: int):
    """Función genérica para eliminar Película o Cliente por ID."""
    item = db.query(orm_model).filter(orm_model.id == item_id).first()
    if not item:
        return None # No encontrado

    db.delete(item)
    db.commit()
    return item


# LÓGICA DE NEGOCIO Y TRANSACCIONES
# ------------------------------------

def create_alquiler_transaccion(db: Session, cliente_id: int, pelicula_id: int):
    """
    Gestiona la transacción completa: actualiza stock y crea el registro de alquiler.
    """
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first()

    if not cliente or not pelicula:
        return None, "Recurso no encontrado" # Devuelve una tupla de error

    try:
        # 1. Lógica POO: Cambia el estado de stock
        pelicula.alquilar_peli()
        
        # 2. Crea el registro de alquiler
        nuevo_alquiler = Alquiler(cliente_id=cliente.id, pelicula_id=pelicula.id)
        db.add(nuevo_alquiler)
        
        db.commit() # ¡Guardamos los dos cambios a la vez!
        db.refresh(nuevo_alquiler)
        return nuevo_alquiler, None # Devuelve el objeto y None para el error
    
    except ValueError as e:
        db.rollback()
        return None, str(e) # Película no disponible
    except IntegrityError:
        db.rollback()
        return None, "La película ya está alquilada (registro existente)"

def delete_alquiler_devolucion(db: Session, alquiler_id: int):
    """Elimina el registro de alquiler y devuelve el stock."""
    alquiler = db.query(Alquiler).filter(Alquiler.id == alquiler_id).first()
    if not alquiler:
        return False # No se encontró

    # 1. Acceder y devolver stock de la película relacionada
    pelicula = db.query(Pelicula).filter(Pelicula.id == alquiler.pelicula_id).first()
    if pelicula:
        pelicula.devolver_peli() 
    
    # 2. Eliminar el registro de alquiler
    db.delete(alquiler)
    
    db.commit() # Guardamos los dos cambios
    return True
## API VIDEOCLUB (FASTAPI + SQLAlchemy) Actividad módulo 2: Programación Avanzada.

#### Cómo Arrancar
Asegúrate de tener las dependencias (fastapi, uvicorn, sqlalchemy, requests).

Ejecuta el servidor:Bashuvicorn main:app --reload


### Endpoints Clave (GET, POST, DELETE)

funciones principales de la API:

* Creación y Listado: Usa POST en /peliculas/ y /clientes/ para crear recursos, y GET en /peliculas/ y /clientes/ para listarlos.

* Alquiler Transaccional: Usa POST en /alquileres/ para alquilar una película. Esta operación reserva el stock y crea el registro de alquiler en un solo paso.

* Devolución Transaccional: Usa DELETE en /alquileres/{id} para procesar la devolución. Esta operación libera el stock y borra el registro.

* Borrado de Recursos: Usa DELETE en /peliculas/{id} y /clientes/{id} para limpiar la base de datos.

### PruebasPara validar el flujo completo (creación, alquiler, devolución y borrado):

* test_request.py
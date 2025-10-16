import requests

BASE_URL = "http://127.0.0.1:8000"


# PRUEBA PELÍCULAS
print("--> PELÍCULAS")

# Crear película
pelicula_data = {
    
    "titulo": "hola", 
    "genero": "comedia"
    
    }

response = requests.post(f"{BASE_URL}/peliculas/", json=pelicula_data)
print(f"código respuesta: {response.status_code}")
print(f"respuesta: {response.json()}")
pelicula = response.json()
print(f"Película AÑADIDA: {pelicula['titulo']}\n")

# Listar películas
response = requests.get(f"{BASE_URL}/peliculas/")
print(f"código respuesta: {response.status_code}")
print(f"respuesta: {response.json()}\n")







# -----------------------------
# PRUEBAS DE CLIENTES
# -----------------------------
print("\n--> CLIENTES")

# Crear cliente
cliente_data = {"nombre": "Arnau"}
response = requests.post(f"{BASE_URL}/clientes/", json=cliente_data)
print("POST crear cliente:", response.status_code, response.json())

# Listar clientes
response = requests.get(f"{BASE_URL}/clientes/")
print("GET listar clientes:", response.status_code, response.json())

# -----------------------------
# PRUEBAS DE ALQUILERES
# -----------------------------
print("\n--> ALQUILERES")

# Crear alquiler
alquiler_data = {"cliente_id": 1, "pelicula_id": 1}
response = requests.post(f"{BASE_URL}/alquileres/", json=alquiler_data)
print("POST crear alquiler:", response.status_code, response.json())

# Listar alquileres
response = requests.get(f"{BASE_URL}/alquileres/")
print("GET listar alquileres:", response.status_code, response.json())

# Intentar alquilar misma película de nuevo (debe fallar)
response = requests.post(f"{BASE_URL}/alquileres/", json=alquiler_data)
print("POST crear alquiler duplicado:", response.status_code, response.json())






# PRUEBA DEVOLUCIÓN FORMAL (DELETE)
print("\n--> DEVOLUCIÓN FORMAL")

# Recuperar el ID del alquiler que se creó (asumimos que es el ID 1)
alquiler_id_a_borrar = 1 

# Ejecutar la devolución (DELETE)
response = requests.delete(f"{BASE_URL}/alquileres/{alquiler_id_a_borrar}")
print(f"DELETE devolver alquiler (ID {alquiler_id_a_borrar}):", response.status_code)

# Verificar que la película 1 está ahora disponible
response = requests.get(f"{BASE_URL}/peliculas/")
print("GET estado Película 1:", response.status_code, [p for p in response.json() if p['id'] == 1][0]['disponible'])
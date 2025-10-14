import requests

BASE_URL = "http://127.0.0.1:8000"


# PRUEBA PELÍCULAS
print("--> PELÍCULAS")

# Crear película
pelicula_data = {
    
    "titulo": "hola", 
    "genero": "terror"
    
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




# Alquilar película
response = requests.post(f"{BASE_URL}/peliculas/1/alquilar")
print(f"código respuesta: {response.status_code}")
print(f"respuesta: {response.json()}")
pelicula = response.json()
print(f"Película alquilada: {pelicula['titulo']} - Disponible: {pelicula['disponible']}\n")

# Devolver película
response = requests.post(f"{BASE_URL}/peliculas/1/devolver")
print(f"código respuesta: {response.status_code}")
print(f"respuesta: {response.json()}")
pelicula = response.json()
print(f"Película devuelta: {pelicula['titulo']} - Disponible: {pelicula['disponible']}\n")


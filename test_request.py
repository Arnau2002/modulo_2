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

# Listar películas
response = requests.get(f"{BASE_URL}/peliculas/")
print(f"código respuesta: {response.status_code}")
print(f"respuesta: {response.json()}")


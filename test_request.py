import requests
import time


BASE_URL = "http://127.0.0.1:8000/"

# ejemplo de datos
PELICULA_DATA = {"titulo": "Shrek", "genero": "Ciencia Ficción"}
CLIENTE_DATA = {"nombre": "Arnau Climent"}
ALQUILER_DATA = {"cliente_id": 1, "pelicula_id": 1}
ALQUILER_ID = 1 # ID esperado para el primer alquiler

time.sleep(2) # Pequeña espera por si la DB tarda en iniciar


#DESCOMENTAR PASO A PASO PARA PROBAR CADA SECCIÓN!!!


#####################################
# 1. CREACIÓN DE RECURSOS (POST)
####################################

print("="*35)
print("1. CREACIÓN DE RECURSOS (POST)")
print("="*35)

# 1.1 POST Película
print("\n--> POST /peliculas/")
response = requests.post(f"{BASE_URL}/peliculas/", json=PELICULA_DATA)
print(f"Código: {response.status_code} | Película creada: {response.json().get('titulo', 'ERROR')}")

# 1.2 POST Cliente
print("--> POST /clientes/")
response = requests.post(f"{BASE_URL}/clientes/", json=CLIENTE_DATA)
print(f"Código: {response.status_code} | Cliente creado: {response.json().get('nombre', 'ERROR')}")

# 1.3 GET Listar Películas y Clientes (Verificación)
print("\n--> GET /peliculas/ (Verificación)")
response = requests.get(f"{BASE_URL}/peliculas/")
print(f"Código: {response.status_code} | Total de películas: {len(response.json())}")






##################################################
# 2. FLUJO TRANSACCIONAL: ALQUILER Y DEVOLUCIÓN
###################################################


# print("\n"+"="*34)
# print("2. ALQUILER Y DEVOLUCIÓN (TRANSACCIÓN)")
# print("="*34)

# # 2.1 POST Alquiler (ÉXITO)
# print("\n--> POST /alquileres/ (Alquilar)")
# response = requests.post(f"{BASE_URL}/alquileres/", json=ALQUILER_DATA)
# print(f"Código: {response.status_code} | Alquiler ID: {response.json().get('id', 'ERROR')}")

# # 2.2 GET Verificación de Stock (DEBE ESTAR NO DISPONIBLE --> Flase)
# print("--> GET /peliculas/ (Verificar Stock)")
# response = requests.get(f"{BASE_URL}/peliculas/")
# print(f"Código: {response.status_code} | Película 1 Disponible: {response.json()[0]['disponible']}")

# # 2.3 POST Alquiler fallido (Prueba de stock. Debe fallar con 400)
# print("\n--> POST /alquileres/ (Fallo por Stock)")
# response = requests.post(f"{BASE_URL}/alquileres/", json=ALQUILER_DATA)
# print(f"Código: {response.status_code} | Detalle de error: {response.json().get('detail', 'OK')}")

# # 2.4 DELETE Devolución (Usa el ID 1)
# print("\n--> DELETE /alquileres/{id} (Devolución Formal)")
# response = requests.delete(f"{BASE_URL}/alquileres/{ALQUILER_ID}")
# print(f"Código: {response.status_code} | Estado: Devolución completada (204 esperado)")

# # 2.5 GET Verificación de Stock (DEBE ESTAR DISPONIBLE DE NUEVO --> True)
# print("--> GET /peliculas/ (Verificar Stock después)")
# response = requests.get(f"{BASE_URL}/peliculas/")
# print(f"Código: {response.status_code} | Película 1 Disponible: {response.json()[0]['disponible']}")







###################################
# 3. LIMPIEZA FINAL (DELETE)
###################################
# print("\n"+"="*35)
# print("3. LIMPIEZA FINAL DE RECURSOS (DELETE)")
# print("="*35)

# # 3.1 DELETE Película (ID 1)
# print("\n--> DELETE /peliculas/{id}")
# response = requests.delete(f"{BASE_URL}/peliculas/{ALQUILER_DATA['pelicula_id']}")
# print(f"Código: {response.status_code} | Película eliminada")

# # 3.2 DELETE Cliente (ID 1)
# print("--> DELETE /clientes/{id}")
# response = requests.delete(f"{BASE_URL}/clientes/{ALQUILER_DATA['cliente_id']}")
# print(f"Código: {response.status_code} | Cliente eliminado")

# # 3.3 GET Verificación final (DEBE MOSTRAR 0 PELICULAS)
# print("\n--> GET /peliculas/ (Verificación final)")
# response = requests.get(f"{BASE_URL}/peliculas/")
# print(f"Código: {response.status_code} | Total de películas: {len(response.json())}")



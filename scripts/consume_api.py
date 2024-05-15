import requests

# URL de la API
api_url = "http://34.70.175.35:8000/api/products"

# Realizar una solicitud GET a la API
response = requests.get(api_url)

# Verificar que la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    print("Solicitud exitosa")
    # Obtener los datos en formato JSON
    products = response.json()
    # Aquí puedes procesar los datos si es necesario
    print(products)
else:
    print(f"Error en la solicitud: {response.status_code}")

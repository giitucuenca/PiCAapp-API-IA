import requests

# URL del servicio y parámetros
url = "http://127.0.0.1:5000/generar"
#url = "https://2587-192-188-47-244.ngrok-free.app/generar"
"""
parametros = {
    "lista": "salir/al"
}
"""

datos = {
    "lista": ["me", "duele"]
}


# Encabezado "Content-Type"
headers = {
    "Content-Type": "application/json",  # Especifica el tipo de contenido como JSON
    "mode": "cors"
}

# Hacer la solicitud POST al servicio con el encabezado
response = requests.post(url, json=datos, headers=headers)

# Obtener la respuesta en formato JSON
resultado = response.json()

# Imprimir el resultado
print(type(resultado['frases']))
print("Resultado:", resultado['frases'])
print("Resultado sem:", resultado['frases_sem'])

# res GET
res = response.text

# Imprimir el resultado
# print(res)

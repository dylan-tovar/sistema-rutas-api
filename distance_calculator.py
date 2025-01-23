import requests

def calcular_matriz_distancias(direcciones):
    # Verificamos que las direcciones sean una lista de diccionarios
    if not all(isinstance(direccion, dict) and 'lat' in direccion and 'lon' in direccion for direccion in direcciones):
        raise ValueError("Las direcciones deben ser una lista de diccionarios con las claves 'lat' y 'lon'.")
    
    # Preparamos las coordenadas en el formato que requiere OSRM
    coordenadas = ";".join([f"{direccion['lon']},{direccion['lat']}" for direccion in direcciones])
    
    # URL del servidor OSRM para la matriz de distancias
    url = f"http://router.project-osrm.org/table/v1/driving/{coordenadas}?annotations=distance"
    
    # Hacemos la solicitud GET a OSRM
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Error en la solicitud a OSRM. Asegúrate de que el servidor OSRM está funcionando.")
    
    # Extraemos la matriz de distancias de la respuesta de OSRM
    distance_matrix = response.json().get("distances", [])
    
    # Convertimos los valores a enteros (en metros) y verificamos la matriz
    matriz = [[int(distancia) for distancia in fila] for fila in distance_matrix]
    return matriz


# API de Pptimización de Rutas de Entregas

> Desarrollada como parte del proyecto de [Sistema de Optimización de rutas de entregas](https://github.com/dylan-tovar/sistema-rutas-laravel).

Esta API en Python provee un servicio para optimizar rutas de entrega utilizando el **Vehicle Routing Problem (VRP)** resuelto con la librería [Google OR-Tools](https://developers.google.com/optimization/routing) y una matriz de distancias calculada mediante el servidor público [OSRM (Open Source Routing Machine)](http://project-osrm.org/).

Dado un conjunto de direcciones geográficas (latitud y longitud) y un número de vehículos disponibles, la API devuelve rutas optimizadas que minimizan la distancia total recorrida por todos los vehículos.

![e](https://developers.google.com/static/optimization/images/routing/vrpgs_solution.svg)

---

## Tecnologías principales

* Python 3.x
* Flask (framework web para la API REST)
* Google OR-Tools (solver para problemas de optimización de rutas)
* OSRM (API pública para obtener matriz de distancias entre puntos)
* Flask-CORS (para permitir llamadas desde clientes en otros orígenes)

---

## Archivos principales

* **app.py**: Archivo principal que define la API REST con Flask.

  * Ruta `/optimizar_ruta` que recibe un POST con direcciones y número de vehículos.
  * Implementa la lógica para construir la matriz de distancias, resolver el VRP y devolver la respuesta con las rutas optimizadas.

* **distance\_calculator.py**: Módulo para calcular la matriz de distancias entre las direcciones usando OSRM.

  * Hace una consulta HTTP a OSRM para obtener la matriz de distancias de conducción.
  * Valida el formato de las direcciones y devuelve la matriz en metros.

---


## Uso

### Endpoint principal

* **POST** `/optimizar_ruta`

#### Cuerpo JSON esperado:

```json
{
  "direcciones": [
    {"lat": 10.491, "lon": -66.902},
    {"lat": 10.496, "lon": -66.895},
    {"lat": 10.503, "lon": -66.900}
  ],
  "vehiculos_disponibles": 2
}
```

* `direcciones`: Lista de objetos con latitud y longitud. El primer elemento es considerado el depósito (punto inicial y final).
* `vehiculos_disponibles`: Número entero de vehículos para repartir la carga.

#### Respuesta exitosa:

```json
{
  "rutas": {
    "0": [0, 2, 0],
    "1": [0, 1, 0]
  },
  "distancia_total": 10250,
  "mensaje": "Rutas optimizadas calculadas exitosamente"
}
```

* `rutas`: Diccionario donde cada clave es un ID de vehículo y su valor es la lista de índices de nodos en la ruta (incluye depósito como inicio y final).
* `distancia_total`: Distancia total combinada en metros.
* `mensaje`: Mensaje informativo.

#### Errores comunes:

* Si no se envían al menos dos direcciones, devuelve error 400 con mensaje.
* Si OSRM no responde correctamente o hay problemas en la optimización, se devuelve un error con descripción.

---

## Detalles técnicos

* Las rutas se generan garantizando que cada vehículo empiece y termine en el depósito (índice 0).
* CORS está habilitado para permitir consumos desde aplicaciones frontend o clientes externos.

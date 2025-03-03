![Logo del proyecto](https://i.imgur.com/2Pq8eWY.png)


# Hbnb - Estructura del Proyecto

Este proyecto implementa la arquitectura de la aplicacion HBnB, estructurada en capas para garantizar modularidad, mantenimiento y escalabiidad. La aplicacion se basa en FLask para la API, un patron Facade para simplificar la comunicacion entre capas, y un sistema de almacenamiento que actualmente utiliza un repositiorio en memoria (proximamente este sera reemplazado por SQLAlchemy).

## 📂 Estructura del Proyecto

```
hbnb/
  part2/
    |── app/
    │    ├── __init__.py              # Inicialización del paquete `app`
    │    ├── api/
    │    │     ├── __init__.py        # Inicialización del paquete `api`
    │    │     ├── v1/
    │    │        ├── __init__.py     # Inicialización de la versión 1 de la API
    │    │        ├── users.py        # Endpoints relacionados con usuarios
    │    │        ├── places.py       # Endpoints relacionados con lugares
    │    │        ├── reviews.py      # Endpoints de reseñas
    │    │        ├── amenities.py    # Endpoints de servicios y comodidades
    │    ├── models/
    │    │   ├── __init__.py         # Inicialización del paquete `models`
    │    │   ├── user.py             # Modelo de datos para usuarios
    │    │   ├── place.py            # Modelo de datos para lugares
    │    │   ├── review.py           # Modelo de datos para reseñas
    │    │   ├── amenity.py          # Modelo de datos para comodidades
    │    ├── services/
    │    │   ├── __init__.py         # Inicialización del paquete `services`
    │    │   ├── facade.py           # Implementación del patrón Fachada para comunicación entre capas
    │    ├── persistence/
    │        ├── __init__.py         # Inicialización del paquete `persistence`
    │        ├── repository.py       # Repositorio en memoria para gestión de datos (a reemplazar con SQLAlchemy)
    ├── run.py                       # Script principal para ejecutar la aplicación Flask
    ├── config.py                    # Configuración general del proyecto
    ├── requirements.txt             # Dependencias del proyecto
    ├── README.md                    # Documentación del proyecto
```

## Arquitectura y Funcionalidades

Capa de Presentacion(api/): Define los endpoints de la API con Flask.
Capa BusinessLogic(services/): implementa reglas utilizando el patron Facade.
Capa Persistence (persistence/): Maneja el almacenamiento de datos, actualmente en memoria, ya que sera cambiado por SQLAlchemy.


### /PART2/

- **/App: Contiene todos los subdirectorios y archivos para el funcionamiento de la aplicacion**
  - **/Api: Contiene todos los enpoints**
    - **/V1**
      - `__init__.py`: kjbdsf
      - `users.py`: fgdgf 
      - `places.py`: dfg dfg 
      - `reviews.py`: dfgdfg
      - `amenities.py`: dfgdfg
  - **/Models: Contiene todos los modelos del proyecto**
    - `__init__.py`: fg
    - `user.py`: dfg
    - `place.py`: kdfg
    - `review.py`: msdfg
    - `amenity.py`: mdfg
  - **/Services: Contiene la facade**
    - `__init__.py`: dfg
    - `facade.py`: bksjd
  - **/Persistence: Contiene la gestion de datos (se reemplazara con SQLAlchemy)**
    - `__init__.py`: nsdf
    - `repository.py`: dgh
  - **/Tests: Contiene todos los tests**
    - `Test1.py`: g
- `run.py`:
- `config.py`:
- `requirements.txt`:
- `README.md`: 

## Flowchart

![IMAGE](https://i.imgur.com/7ch2DTL.png)


# Tests

## Pruebas para Endpoints de la API

**Descripcion**

En este apartado se registran las pruebass realizadas en los endpoints de la API, incluyendo Usuaris, Places, Reviews, Amenities. Se incluyen tambien los test finales probados, datos de entrada, resultados esperados, resultados actuales y cualquier otro error dado por la misma.

### 1. Pruebas de Endopoints de Usuarios

**Puntos finales probados**

1. POST /api/v1/users - Crear un Usuario
2. GET /api/v1/users - Listar todos los Usuarios
3. GET /api/v1/users/{id} - Obtener un Usuario por ID
4. PUT /api/v1/users/{id} - Actualizar un Usuario

**Detalles de Pruebas**

1. Crear un Usuario
   - Entrada
     ```
     {
       "first_name": "Jane",
       "last_name": "Doe",
       "email": "jane.doe@example.com"
     }
     ```
   - Resultado Esperado: Codigo de estado 201 (Creado)
   - Resultado Actual: Codigo de estado 201 (Creado)

2. Obtener un Usuario con ID invalido
   - Entrada: ID inexistente
   - Resultado Esperado: Codigo de estado 404 (No encontrado)
   - Resultado Actual: Codigo de estado 404 (No encontrado)

### 2. Pruebas de Endpoints de Places

**Puntos finales probados**

1. Post /api/v1/places/ - Crear un lugar
2. GET /api/v1/places/ - Listar todos los lugares
3. GET /api/v1/places/{id} - Obtener detalles de un lugar
4. PUT /api/v1/places/{id} - Actualizar un lugar

**Detalles de Pruebas**

1. Crear un Place
   - Entrada:
     ```
     {
       "title": "Cozy Apartment",
       "description": "A nice place to stay",
       "price": 100.0,
       "latitude": 37.7749,
       "longitude": -122.4194,
       "owner_id": "1"
     }
     ```
   - Resultado Esperado: Codigo de estado 201 (Creado)
   - Resultado Actual: Codigo de estado 201 (Creado)


### 3. Pruebas de Endpoints de Reviews

**Puntos finales probados**

1. POST /api/v1/reviews/ - Crear una reviews
2. GET /api/v1/reviews/ - Listar todas las reviews
3. GET /api/v1/reviews/{id} - Obtener detalles de una reviews
4. DELETE /api/v1/reviews/{id} - Eliminar una reviews

**Detalles de Pruebas**

1. Crear una Reviews
   - Entrada:
     ```
     {
       "text": "Great place to stay!",
       "rating": 5,
       "user_id": "1",
       "place_id": "1"
     }
     ```
   - Resultado Esperado: Codigo de estado 201 (Creado)
   - Resultado Actual: Codigo de estado 201 (Creado)

2. Intentar Obtener una Review con ID Invalido
   - Entrada: ID inexistente
   - Resultado Esperado: Codigo de estado 404 (No encontrado)
   - Resultado Actual: Codigo de estado 404 (No encontrado)


### 4. Pruebas de Endpoints de Amenities

**Puntos Finales Probados**

1. POST /api/v1/amenities/ - Crear una amenity
2. GET /api/v1/amenities/ - Listar todas las amenities
3. GET /api/v1/amenities/{id} - Obtener una amenity por ID
4. PUT /api/v1/amenities/{id} - Actualizar una amenity

**Detalles de Pruebas**

1. Crear una Amenity
   - Entrada
     ```
     {
       "name": "Wifi"
     }
     ```
   - Resultado Esperado: Codigo de estado 201 (Creado)
   - Resultado Actual: Codigo de estado 201 (Creado)

2. Obtener una Amenity con ID Invalido
   - Entrada: ID inexistente
   - Resultado Esperado: Codigo de estado 404 (No encontrado)
   - Resultado Actual: Codigo de estado 404 (No encontrado)

**Conclusion**

Los Test cubren los casos basicos de creacion, consulta, actualizacion y manejo de errores en los endpoints de usuarios, lugares, reseñas y amenidades.
A medida que avancemos en el proyecto, se va a corregir errores menores y se mejoraran validaciones.

## Authors

This project was co-authored by Lucas Andrada and Federico Angeriz. Cohort 25 ![GIF animado](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWJ1dG0xNGp5cHcxNWVlaXdyeTY2OGJycGhiZHA0OWlucTlyeXU2YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/V6FfiRnRLpF0uarooy/giphy.gif)

![Logo del proyecto](https://i.imgur.com/2Pq8eWY.png)


# Hbnb - Estructura del Proyecto

Este proyecto implementa la arquitectura de la aplicacion HBnB, estructurada en capas para garantizar modularidad, mantenimiento y escalabiidad. La aplicacion se basa en FLask para la API, un patron Facade para simplificar la comunicacion entre capas, y un sistema de almacenamiento que actualmente utiliza un repositiorio en memoria (proximamente este sera reemplazado por SQLAlchemy).

## 📂 Estructura del Proyecto

```
hbnb/
  part2/
    |── app/
    │    ├── __init__.py             # Inicialización del paquete `app`
    │    ├── api/
    │    │     ├── __init__.py         # Inicialización del paquete `api`
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
    ├── run.py                      # Script principal para ejecutar la aplicación Flask
    ├── config.py                    # Configuración general del proyecto
    ├── requirements.txt             # Dependencias del proyecto
    ├── README.md                    # Documentación del proyecto
```

## Arquitectura y Funcionalidades

Capa de Presentacion(api/): Define los endpoints de la API con Flask.
Capa BusinessLogic(services/): implementa reglas utilizando el patron Facade.
Capa Persistence (persistence/): Maneja el almacenamiento de datos, actualmente en memoria, ya que sera cambiado por SQLAlchemy.


### /APP/


## Authors

This project was co-authored by Lucas Andrada and Federico Angeriz. Cohort 25 ![GIF animado](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWJ1dG0xNGp5cHcxNWVlaXdyeTY2OGJycGhiZHA0OWlucTlyeXU2YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/V6FfiRnRLpF0uarooy/giphy.gif)



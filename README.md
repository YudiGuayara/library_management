# API de Gestión de Biblioteca

Esta es una API RESTful desarrollada con Flask para gestionar materiales de una biblioteca.

## Instalación

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/YudiGuayara/library_management.git
   cd library_management

Tambien debes instalar la siguiente dependencia:

    pip install -r requirements.txt


## Configuración

1. Asegúrate de tener Python y pip instalados en tu sistema.

2. Configura las variables de entorno necesarias en tu archivo `.env`. Asegúrate de incluir las variables como `DATABASE_URI`, `SECRET_KEY`, etc.

## Uso

1. Ejecuta la aplicación:
    python run.py


La aplicación se ejecutará en `http://127.0.0.1:5000/`.

2. Utiliza Postman o cualquier otra herramienta similar para realizar las siguientes operaciones:

- **Obtener todos los materiales:**
  - Método: GET
  - URL: `http://127.0.0.1:5000/api/materials`

- **Obtener un material por ID:**
  - Método: GET
  - URL: `http://127.0.0.1:5000/api/materials/<material_id>`
  - Sustituye `<material_id>` por un ID válido en tu base de datos.

- **Crear un nuevo material:**
  - Método: POST
  - URL: `http://127.0.0.1:5000/api/materials`
  - Encabezado `Content-Type`: application/json
  - Cuerpo:
    ```json
    {
        "title": "Título del material",
        "author": "Autor del material",
        "year": 2023
        // Añade otros campos según sea necesario
    }
    ```

- **Actualizar un material existente:**
  - Método: PUT
  - URL: `http://127.0.0.1:5000/api/materials/<material_id>`
  - Encabezado `Content-Type`: application/json
  - Cuerpo:
    ```json
    {
        "title": "Nuevo título del material",
        "author": "Nuevo autor del material",
        "year": 2024
        // Actualiza otros campos según sea necesario
    }
    ```

- **Borrar un material:**
  - Método: DELETE
  - URL: `http://127.0.0.1:5000/api/materials/<material_id>`

- **Prestar un material:**
  - Método: POST
  - URL: `http://127.0.0.1:5000/api/borrow`
  - Encabezado `Content-Type`: application/json
  - Cuerpo:
    ```json
    {
        "material_id": "<material_id>",
        "borrower_name": "Nombre del usuario que solicita el préstamo"
    }
    ```

- **Devolver un material:**
  - Método: POST
  - URL: `http://127.0.0.1:5000/api/return`
  - Encabezado `Content-Type`: application/json
  - Cuerpo:
    ```json
    {
        "material_id": "<material_id>"
    }
    ```

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún problema o tienes alguna mejora, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](https://opensource.org/licenses/MIT).


Para testear: 

Agregar un material: POST a http://127.0.0.1:5000/api/materials
Obtener todos los materiales: GET a http://127.0.0.1:5000/api/materials
Obtener un material por ID: GET a http://127.0.0.1:5000/api/materials/<material_id>
Prestar un material: POST a http://127.0.0.1:5000/api/borrow
Devolver un material: POST a http://127.0.0.1:5000/api/return

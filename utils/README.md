# SD_P2P - Sistema de Intercambio de Archivos Peer-to-Peer

Este proyecto implementa un sistema de intercambio de archivos en una red P2P no estructurada basada en un servidor de **Directorio y Localización**. La comunicación entre peers se realiza a través de **Flask** para los endpoints HTTP y **gRPC** para llamadas a procedimientos remotos.

## Descripción General

El sistema permite que varios peers se conecten, compartan archivos y realicen búsquedas en la red para descargar archivos desde otros peers. Está compuesto por dos componentes principales:
1. **Servidor gRPC**: Encargado de las operaciones de búsqueda y descarga de archivos.
2. **API REST**: Proporciona endpoints HTTP para el manejo de sesión y gestión de peers.

## Instalación Previa

Antes de ejecutar el sistema, es necesario instalar las dependencias y compilar el archivo `.proto` para generar las clases de gRPC.

### Instalaciones

1. Instalar el compilador de gRPC:
   ```bash
   pip install grpcio-tools
   ```

2. Compilar el archivo `catalog.proto` para generar los archivos Python necesarios:
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. catalog.proto
   ```

   Este comando generará dos archivos:
   - `catalog_pb2.py`: Define los mensajes gRPC.
   - `catalog_pb2_grpc.py`: Define las clases de los servicios gRPC.

3. ejecutar servidores en entornos virtuales
    - pip install pipenv    
    - pipenv install grpcio-tools grpcio googleapis-common-protos
    - pipenv shell  
    - pip install flask
     

## Estructura del Proyecto

El proyecto utiliza los siguientes módulos y dependencias:

- **logging**: Para la configuración y gestión de logs.
- **Flask**: Framework para manejar las peticiones HTTP.
- **grpc**: Framework para la comunicación RPC.
- **catalog_pb2_grpc y catalog_pb2**: Archivos generados a partir del archivo `catalog.proto`, que definen las clases y servicios gRPC.
- **concurrent.futures**: Para manejar la ejecución de tareas de forma asíncrona.

### Funcionalidades Principales

#### Servidor gRPC
- `start_grpc_server()`: Inicia el servidor gRPC y expone los servicios definidos en `catalog.proto`.

#### API REST
- **Login** (`/login` - POST): Registra un peer en el sistema con su IP, URL y archivos compartidos.
- **Index** (`/index` - POST): Muestra información sobre los peers conectados y los archivos que comparten.
- **Search** (`/search` - POST): Permite buscar un archivo en los peers conectados.
- **Logout** (`/logout` - POST): Desconecta un peer del sistema.
- **Descargar** (`/descargar` - GET): Inicia la descarga de un archivo desde un peer utilizando gRPC.

### Clases y Servicios gRPC

- **CatalogServicer**: Implementa los servicios gRPC definidos en `catalog.proto`:
  - `Search`: Busca archivos entre los peers conectados.
  - `Download`: Maneja las solicitudes de descarga de archivos.
  - `Upload`: Maneja las solicitudes de subida de archivos (pendiente de implementación).

### Variables Globales

- **app**: Instancia de la aplicación Flask.
- **peers**: Diccionario que almacena la información de los peers conectados (usuario, IP, archivos compartidos, etc.).

## Uso del Sistema

1. Ejecuta el script principal para iniciar el servidor Flask y el servidor gRPC.
2. Usa los siguientes endpoints HTTP para interactuar con el sistema.

### Ejemplos de Peticiones

#### Login (Registrar un Peer)
```json
POST /login
{
    "user": "peer1",
    "password": "peer11",
    "ip": "127.0.0.1",
    "port": 5001,
    "archivos": ["file1.txt,file2.txt,file3.txt"]
}
```

#### Index (Consultar Información de un Peer)
```json
POST /index
{
    "ip": "127.0.0.1",
    "url": "http://127.0.0.1:5001"
}
```

#### Search (Buscar un Archivo)
```json
POST /search
{
    "archivo": "file1.txt"
}
```

#### Logout (Desconectar un Peer)
```json
POST /logout
{
    "ip": "127.0.0.1",
    "url": "http://127.0.0.1:5001"
}
```

## Notas Adicionales

- Actualmente, el sistema está en fase de construcción y prueba. La funcionalidad de subida de archivos (Upload) aún no está completamente implementada.
- Se pueden realizar pruebas de los endpoints mencionados utilizando herramientas como **Postman** o **curl**.

## Contribuciones

Este proyecto está abierto a contribuciones. Si tienes sugerencias o mejoras, no dudes en enviar un **pull request** o abrir un **issue**.


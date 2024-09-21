# SD_P2P - Sistema de Intercambio de Archivos Peer-to-Peer
Este proyecto implementa un sistema de intercambio de archivos en una red P2P basada en un servidor de **Directorio y Localización**. La comunicación entre peers y servidor se realiza a través de un **API** con interacciones HTTP y **gRPC** para la comunicación entre peers.

## Descripción General

El sistema permite que múltiples peers se conecten, compartan archivos y realicen búsquedas en la red para descargar archivos desde otros peers. Está compuesto por dos componentes principales:

1. **Servidor gRPC**: Encargado de las operaciones de búsqueda y descarga de archivos.
2. **API REST**: Proporciona endpoints HTTP para el manejo de sesión y gestión de peers.

## Descripción

`SD_P2P` es una implementación de red peer-to-peer (P2P) que facilita el intercambio de archivos de manera descentralizada entre peers, empleando tanto API REST como gRPC. El objetivo es proporcionar una plataforma de distribución de archivos eficiente y sin necesidad de un servidor centralizado.

## Funcionalidades

- **Login**: Autenticación de usuarios.
- **Index**: Indexación de archivos disponibles en los peers.
- **Search**: Búsqueda de archivos en la red P2P.
- **DownloadFile**: Descarga de archivos desde otros peers.
- **UploadFile**  :Carga de archivos en los peers
- **Logout**: Desconexión de usuarios.

## Requisitos

* Python 3.8 o superior
* Paquetes de Python
    - `requests`
    - `grpcio`
    - `grpcio-tools`
    - `protobuf`

## Instalación

1. Clona el repositorio:
    ```bash
   git clone https://github.com/AndresT1234/SD_P2P.git
   ```
   

## Preparacion Previa

Antes de ejecutar el sistema, es necesario instalar las dependencias y compilar el archivo `.proto` para generar las clases de gRPC.

### Instalaciones

1. Instalar el compilador de gRPC:
   ```bash
   pip install grpcio-tools
   ```

2. Compilar el archivo `peer.proto` para generar los archivos Python necesarios:
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. peer.proto
   ```

   Este comando generará los siguientes archivos:
   - `catalog_pb2.py`: Define los mensajes gRPC.
   - `catalog_pb2_grpc.py`: Define las clases de los servicios gRPC.
     

## Estructura del Proyecto

El proyecto utiliza los siguientes módulos y dependencias clave:

- **logging**: Para la configuración y gestión de logs.
- **Flask**: Framework para manejar las peticiones HTTP.
- **grpc**: Framework para la comunicación RPC.
- **sys**: Para la gestión del sistema y variables de entorno
- **secrets**: Para la generación del token aleatorio.
- **os**: para manejo de rutas y archivo.
- **request**: Para manejar las solicitudes HTTP en Flask.
- **jsonify**: Para convertir las respuestas en formato JSON en Flask.
- **json**: Para trabajar con datos en formato JSON.
- **catalog_pb2_grpc y catalog_pb2**: Archivos generados a partir del archivo `catalog.proto`, que definen las clases y servicios gRPC.
- **concurrent.futures**: Para manejar la ejecución de tareas de forma asíncrona.



### Funcionalidades Principales


#### gRPC
--------------Servidor gRPC----------------------------
### Función para iniciar el servidor gRPC

- `server()`: Inicia el servidor gRPC y expone los servicios definidos en `peer.proto`. Este método configura y ejecuta el servidor para que pueda recibir y manejar solicitudes gRPC.


#### API REST
--------------API REST--------------

- **Login** (`/login` - POST): Registra un peer en el sistema con su usuario, contraseña, IP, puerto y archivos.
- **Index** (`/index` - POST): Muestra información sobre los peers conectados y los archivos que comparten. Se le pasa la IP y el URL del peer.
- **Search** (`/search` - GET): Permite buscar un archivo en la red de los peers conectados. Se le pasa el nombre del archivo que se desea buscar.
- **Logout** (`/logout` - POST): Desconecta un peer del sistema.
- **loadfiles** (`/loadfiles` - PUT):  Inicia la descarga de un archivo desde otro peer utilizando gRPC.



### Clases y Servicios gRPC
--------------Class PeerService---------
### Clase que implementa los métodos de PeerService

- `__init__(self)`: Constructor que inicializa las variables necesarias para el servicio gRPC.

- `UploadFile(self, request)`: Maneja las solicitudes de subida de archivos a la red P2P. Este método recibe un archivo desde un peer y lo almacena en el sistema, actualizando el índice de archivos disponibles en la red.

- `DownloadFile(self, request, context)`: Maneja las solicitudes de descarga de archivos desde la red P2P. Este método permite a un peer descargar un archivo almacenado en otro peer de la red.


----------------------
### Variables Globales

- **app**: Instancia de la aplicación Flask.
- **peers**: Diccionario que almacena la información de los peers conectados (usuario, IP, archivos compartidos, etc.).


---------------------
## Uso del Sistema

Para ejecutar el sistema, sigue estos pasos:

1. **Iniciar el Servidor Flask y el Servidor gRPC**:

    ### Para iniciar el servidor Flask , usa el siguiente comando:

        ./ApiRest/ python Server.py #server Api

    ### Cada peer debe ejecutar su propio servidor gRPC para poder compartir y descargar archivos. Para iniciar el servidor gRPC de un peer, usa el siguiente comando:

        ./Peer/Peer1/ python peer1_server.py #peer server 1
        ./Peer/Peer2/ python peer2_server.py #peer server 2
        ./Peer/Peer3/ python peer3_server.py #peer server 3
        ./Peer/Peer4/ python peer4_server.py #peer server 4


2. **Interactuar con el Sistema**:
    Usa los siguientes endpoints HTTP para interactuar con el sistema:

    - **Login** (`/login` - POST): Registra un peer en el sistema con su usuario, contraseña, IP, puerto y archivos.
    - **Index** (`/index` - GET): Muestra información sobre los peers conectados y los archivos que comparten. Se le pasa la IP y el URL del peer.
    - **Search** (`/search` - GET): Permite buscar un archivo en los peers conectados. Se le pasa el nombre del archivo que se desea buscar.
    - **Logout** (`/logout` - POST): Desconecta un peer del sistema.
    - **Descargar** (`/loadfiles` - POST): Inicia la descarga de un archivo desde un peer utilizando gRPC.

3. **Realizar Operaciones**:
    Una vez que los servidores y clientes están en ejecución, puedes realizar operaciones como subir archivos, buscar archivos, y descargar archivos utilizando los endpoints HTTP y los métodos gRPC proporcionados.

4. **Ejecutar los clientes**
-----------------IMPORTANTE-----------------------------------
Los peers también pueden ejecutar clientes para interactuar con otros peers en la red. Para iniciar un cliente peer: Recuerda que cada peer debe estar registrado en el sistema utilizando el endpoint `/login` antes de poder realizar otras operaciones.

## por ejemplo:
    ./Peers/peer1/ python client.py /login

---------------------
## Contribuciones
Este proyecto está abierto a contribuciones. Si tienes sugerencias o mejoras, no dudes en enviar un **pull request** o abrir un **issue**.


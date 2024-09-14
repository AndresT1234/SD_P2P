# SD_P2P

_La versión inicial sugiere realizarla en un esquema de red P2P no estructurada basada en servidor de  Directorio y Localización_

* creacion de archivo texto catalog.proto 
"se define el paquete, los mensajes y los servicios que tendra"


* instalaciones previas:

 * pip install grpcio-tools 
 "instalacion de compilador"

 * python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. catalog.proto
 "teniendo listo el archivo .proto, Este comando generará dos archivos Python: catalog_pb2.py y catalog_pb2_grpc.py. Estos archivos contienen las clases y métodos necesarios para trabajar con los mensajes y servicios definidos en catalog.proto"


Este script implementa un sistema de intercambio de archivos Peer-to-Peer (P2P) utilizando Flask para los endpoints HTTP y gRPC para llamadas a procedimientos remotos.

* Módulos:
  -  logging: Proporciona una forma de configurar y usar registradores.
  - flask: Un micro framework web para Python.
    - grpc: Un framework RPC de alto rendimiento.
    catalog_pb2_grpc: Código gRPC generado a partir del archivo catalog.proto.
    catalog_pb2: Código gRPC generado a partir del archivo catalog.proto.
    concurrent.futures: Proporciona una interfaz de alto nivel para ejecutar llamadas de forma asíncrona.

* Funciones:
    - start_grpc_server(): Inicia el servidor gRPC con los servicios definidos.
    - login(): Endpoint HTTP para el inicio de sesión de un peer. Agrega la IP del peer y los archivos compartidos al diccionario peers.
    - index(): Endpoint HTTP para listar todos los peers conectados y sus archivos compartidos.
    - search(): Endpoint HTTP para buscar un archivo específico entre los peers conectados.
    - logout(): Endpoint HTTP para el cierre de sesión de un peer. Elimina la IP del peer del diccionario peers.
    - descargar(): Endpoint HTTP para iniciar la descarga de un archivo desde un peer específico utilizando gRPC.
      
* Clases:
  
  CatalogServicer: Implementa los servicios gRPC definidos en catalog.proto.
  
        - Search: Busca archivos.
        - Download: Maneja solicitudes de descarga de archivos.
        - Upload: Maneja solicitudes de subida de archivos.
  
  Variables Globales:
  
    - app: Instancia de la aplicación Flask.
    - peers: Diccionario para almacenar los peers conectados y sus archivos compartidos.
      
* Uso:
    Ejecuta el script para iniciar el servidor web Flask y el servidor gRPC. Usa los endpoints HTTP proporcionados para interactuar con el sistema P2P.
 
* para las pruebas POST "aun en construccion"

//para login
{
    "user": "peer1",
    "password": "per1234",
    "ip": "127.0.0.1",
    "url": "http://localhost",
    "port": "5001",
    "archivos": "file1.txt,file2.txt,file3.txt"
}

//para index
{
    "ip": "127.0.0.1",
    "url": "http://localhost:5001"
}

//para search
{
  "archivo": "file1.txt"
}



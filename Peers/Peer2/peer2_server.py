import grpc
from concurrent import futures
import os
import sys
import json

# Agregar el directorio padre al path para importar los módulos de gRPC
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from gRPC import peer_pb2, peer_pb2_grpc


# Clase que implementa los métodos de PeerService
class PeerService(peer_pb2_grpc.PeerServiceServicer):
    FILES_PATH = "" # Directorio donde se almacenan los archivos

    def __init__(self):
        with open("config.json") as f:
            data = json.load(f)
            self.files = os.listdir(data['files_path'])  # Lista de archivos disponibles en el peer
            PeerService.FILES_PATH = data['files_path']
        
    # Método para manejar la solicitud de subida de archivos
    def UploadFile(self, request, context):
        filename = request.filename
        # Implementación para manejar la carga del archivo
        if filename in self.files:
            return peer_pb2.FileResponse(success=False, message="Archivo ya existe")
        self.files.append(filename)
        return peer_pb2.FileResponse(success=True, message="Archivo cargado correctamente")

    # Método para manejar la solicitud de descarga de archivos
    def DownloadFile(self, request, context):
        filename = request.filename
        filepath = os.path.join(PeerService.FILES_PATH, filename)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as file:
                while chunk := file.read(1024):  # Leer el archivo en chunks de 1 KB
                    yield peer_pb2.FileChunk(content=chunk)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Archivo no encontrado.: {filepath}')

# Función para iniciar el servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    peer_pb2_grpc.add_PeerServiceServicer_to_server(PeerService(), server)
    server.add_insecure_port('[::]:5002')  # Escuchar en el puerto 5002
    server.start()
    print("gRPC Peer Server ejecutandose en el puerto 5002...")
    print(f"Archivos listos desde: {os.path.abspath(PeerService.FILES_PATH)}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

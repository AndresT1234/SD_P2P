import grpc
import peer_pb2
import peer_pb2_grpc
import os

DOWNLOAD_PATH = "../files/"  # Directorio donde se almacenan los archivos descargados

# Función para descargar archivos de un peer
def download_file(peer_address, filename):
    # Conectar al peer en la dirección indicada (IP:puerto)
    channel = grpc.insecure_channel(peer_address)
    stub = peer_pb2_grpc.PeerServiceStub(channel)
    
    # Crear una solicitud de archivo
    request = peer_pb2.FileRequest(filename=filename)
    
    # Realizar la descarga del archivo en chunks
    try:
        response = stub.DownloadFile(request)
        with open(os.path.join(DOWNLOAD_PATH, f"downloaded_{filename}"), 'wb') as f:
            for chunk in response:
                f.write(chunk.content)
        print(f"Archivo {filename} descargado exitosamente.")
    except grpc.RpcError as e:
        print(f"Error al descargar el archivo: {e.details()}")

if __name__ == "__main__":
    peer_address = 'localhost:50051'  # Dirección del peer al que conectarse
    filename = 'image1.png'  # Archivo a descargar
    download_file(peer_address, filename)

from concurrent import futures
import logging
import grpc
import catalog_pb2_grpc , catalog_pb2

class CatalogServicer(catalog_pb2_grpc.CatalogServicer):

    def __init__(self):
        self.peers_files = {}
        
    def Search(self, request, context):
        archivo_buscado = request.filename
        resultados = []
        for peer_url, peer_info in self.peers_files.items():
            if archivo_buscado in peer_info["files"]:
                resultados.append(peer_url)
        return catalog_pb2.SearchResult(files=resultados)

    def Download(self, request, context):
        filename = request.filename
        try:
            return catalog_pb2.DownloadResponse(filename)
        except FileNotFoundError:
            context.set_details(f'Archivo {filename} no encontrado.')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return catalog_pb2.DownloadResponse()

    def Upload(self, request, context):
        filename = request.filename
        peer_url = context.peer() 
        
        try:
            if peer_url not in self.peers_files:
                self.peers_files[peer_url] = []
            self.peers_files[peer_url].append(filename)
            return catalog_pb2.UploadResponse(message="Archivo subido exitosamente.")
        
        except Exception as e:
            context.set_details(f'Error subiendo archivo: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return catalog_pb2.UploadResponse(message="Error subiendo archivo.")
        
    
def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    catalog_pb2_grpc.add_CatalogServicer_to_server(catalog_pb2_grpc.CatalogServicer(), server)
    server.add_insecure_port(f'[::]:{50051}')
    print("Server running in port 50051")
    server.start()
    logging.info(f"gRPC Server iniciado en puerto {50051}")
    server.wait_for_termination() 


if __name__ == "__main__":
    start_grpc_server()   



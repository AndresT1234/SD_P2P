from concurrent import futures
import logging
import grpclib
import grpc
import catalog_pb2, catalog_pb2_grpc

#servicios gRPC
class CatalogServicer(catalog_pb2_grpc.CatalogServicer):  

    def Download(self, request, context):
        filename = request.filename
        try:
            return catalog_pb2.DownloadResponse(filename)
        except FileNotFoundError:
            context.set_details(f'Archivo {filename} no encontrado.')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return catalog_pb2.DownloadResponse()
    
#servidor gRPC  
def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    catalog_pb2_grpc.add_CatalogServicer_to_server(catalog_pb2_grpc.CatalogServicer(), server)
    server.add_insecure_port(f'[::]:{50051}')
    print("Server running in port 50051")
    server.start()
    logging.info(f"gRPC Server iniciado en puerto {50051}")
    server.wait_for_termination() 
    
#funcion para descargar archivos
def download_file(filename, peer_url):
  channel = grpclib.insecure_channel(peer_url) 
  cliente = catalog_pb2_grpc.CatalogStub(channel)
  request = catalog_pb2.DownloadRequest(filename=filename)
  try:
    response = cliente.Download(request)
    with open(f"downloaded_{filename}", 'wb') as f:
      f.write(response.file_data)
    print(f"Downloaded '{filename}' from {peer_url}")
  except grpc.RpcError as e:
    print(f"Error downloading: {e.details()}")



if __name__ == "__main__":
    #servidor gRPC
    start_grpc_server()   




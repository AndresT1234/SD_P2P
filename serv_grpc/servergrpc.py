from concurrent import futures
import logging
import grpclib
import grpc

from proto import catalog_pb2_grpc, catalog_pb2

#servicios gRPC
class CatalogServicer(catalog_pb2_grpc.CatalogServicer):  
    def Download(self, request, context):
        filename = request.filename
        try:
            with open(filename, 'rb') as f:
                file_data = f.read()
            return catalog_pb2.DownloadResponse(file_data=file_data)
        except FileNotFoundError:
            context.set_details(f"Archivo {filename} no encontrado.")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return catalog_pb2.DownloadResponse()
    
#servidor gRPC  
def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    catalog_pb2_grpc.add_CatalogServicer_to_server(CatalogServicer(), server)
    server.add_insecure_port(f'[::]:{50051}')
    print("gRPC server iniciado en el puerto 50051")
    server.start()
    logging.info(f"gRPC Server iniciado en puerto {50051}")
    server.wait_for_termination() 
    

if __name__ == "__main__":
    #servidor gRPC
    start_grpc_server()




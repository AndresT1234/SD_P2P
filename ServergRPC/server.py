from concurrent import futures
import logging
from flask import json
import grpc
import catalog_pb2
import catalog_pb2_grpc

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
def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    catalog_pb2_grpc.add_CatalogServicer_to_server(catalog_pb2_grpc.CatalogServicer(), server)
    server.add_insecure_port(f'[::]:{50051}')
    print("gRPC server iniciado en el puerto 50051")
    server.start()
    logging.info(f"gRPC Server iniciado en puerto {50051}")
    server.wait_for_termination() 

#guardar peers
def guardarpeer(peer_info):
    config_file = 'config.json'
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
    except FileNotFoundError:
        config_data = {}

    if 'peers' not in config_data:
        config_data['peers'] = []

        config_data['peers'].append(peer_info)

    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=4)

if __name__ == "__main__":
    server()
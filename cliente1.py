import grpclib
import catalog_pb2
import catalog_pb2_grpc

def run():
    channel = grpclib.Channel('localhost:50051')
    stub = catalog_pb2_grpc.CatalogServicerStub(channel)
    request = catalog_pb2.SearchRequest(filename="mi_archivo.txt")
    response = stub.Search(request)
    print(response.files)

if __name__ == '__main__':
    run()
import grpclib
from grpc_serv import catalog_pb2, catalog_pb2_grpc

def search_file(filename):
  channel = grpclib.Channel('localhost:50051')
  cliente = catalog_pb2_grpc.CatalogServicerStub(channel)
  request = catalog_pb2.SearchRequest(filename=filename)
  response = cliente.Search(request)
  print(f"Peers with '{filename}': {response.files}")

if __name__ == '__main__':
  search_file("file1.txt")
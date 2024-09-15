import grpc
import grpclib
from grpc_serv import catalog_pb2, catalog_pb2_grpc

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

if __name__ == '__main__':
  filename = "fila1.txt"
  peer_url = "http://localhost:50052"
  download_file(filename, peer_url)
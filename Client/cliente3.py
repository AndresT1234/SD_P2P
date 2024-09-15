import grpclib
from grpc_serv import catalog_pb2, catalog_pb2_grpc

def upload_file(filename, file_content):
  channel = grpclib.insecure_channel('localhost:50053')  
  cliente = catalog_pb2_grpc.CatalogStub(channel)
  request = catalog_pb2.UploadRequest(filename=filename, content=file_content)
  response = cliente.Upload(request)
  print(response.message)

if __name__ == '__main__':
  filename = "document.pdf"
  with open(filename, 'rb') as f:
    file_content = f.read()
  upload_file(filename, file_content)
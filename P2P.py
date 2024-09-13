import logging
from flask import Flask, request, jsonify
import grpc
import catalog_pb2_grpc
import catalog_pb2
from concurrent import futures
import os
import secrets

app = Flask(__name__)

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

peers = {}
gRPC_PORT = os.getenv('GRPC_PORT', '50051')
FLASK_PORT = os.getenv('FLASK_PORT', '5000')

# Iniciar servidor gRPC
def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    catalog_pb2_grpc.add_CatalogServicer_to_server(CatalogServicer(), server)
    server.add_insecure_port(f'[::]:{gRPC_PORT}')
    server.start()
    logging.info(f"gRPC Server iniciado en puerto {gRPC_PORT}")

# Implementar los servicios gRPC
class CatalogServicer(catalog_pb2_grpc.CatalogServicer):
    def __init__(self):
        self.peers_files = {}

    def Search(self, request, context):
        archivo_buscado = request.filename
        if archivo_buscado in self.files:
            return catalog_pb2.SearchResult(files=[archivo_buscado])
        else:
            return catalog_pb2.SearchResult(files=[])

    def Download(self, request, context):
        filename = request.filename
        try:
            with open(f'./{filename}', 'rb') as f:
                file_data = f.read()
            return catalog_pb2.DownloadResponse(file_data=file_data)
        except FileNotFoundError:
            context.set_details(f'Archivo {filename} no encontrado.')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return catalog_pb2.DownloadResponse()

    def Upload(self, request, context):
        filename = request.filename
        file_data = request.file_data
        peer_url = context.peer() 
        
        try:
            
            with open(f'./{filename}', 'wb') as f:
                f.write(file_data)
             
            if peer_url not in self.peers_files:
                self.peers_files[peer_url] = []
            self.peers_files[peer_url].append(filename)
            
            return catalog_pb2.UploadResponse(message="Archivo subido exitosamente.")
        except Exception as e:
            context.set_details(f'Error subiendo archivo: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return catalog_pb2.UploadResponse(message="Error subiendo archivo.")
        
# Endpoint para login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')
    ip = data.get('ip')
    
    if not user or not password or not ip:
        return jsonify({"Error": "Faltan datos (user, password o ip)"}), 400
    
    url = f"http://localhost:{ip}"
    token = secrets.token_urlsafe(16)
    
    if url in peers:
        logging.info(f"Peer ya se encuentra conectado: {url}") 
        return jsonify({"message": "Peer ya se encuentra conectado"}), 400
    else:
        peers[url] = {"user": user, "token": token, "files": []}
        logging.info(f"Peer conectado correctamente en: {url}")
        return jsonify({"estado": "OK", "token": token}), 200

# Endpoint para index
@app.route('/index', methods=['POST'])
def index():
    data = request.get_json()
    peer_url = data.get('url')

    if not peer_url:
        return jsonify({"error": "Falta la url del peer"}), 400
    
    peer_info = peers.get(peer_url)
    
    if peer_info:
        return jsonify({
            "nombre": peer_info.get("user"),
            "url": peer_url,
            "files": peer_info.get("files", [])
        }), 200
    else:
        return jsonify({"error": "Peer no encontrado"}), 404

# Endpoint para search
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    archivo_buscado = data.get('archivo')
    
    if not archivo_buscado:
        return jsonify({"error": "Falta el nombre del archivo a buscar"}), 400
    
    for url, info in peers.items():
        archivos = info.get("files", [])
        if archivo_buscado in archivos:
            return jsonify({"url": url}), 200
    
    return jsonify({"mensaje": "Archivo no encontrado"}), 404

# Endpoint para logout
@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "Falta la url del peer"}), 400

    if url in peers:
        del peers[url]
        logging.info(f"Peer desconectado: {url}")
        return jsonify({"mensaje": f"Peer {url} desconectado correctamente."}), 200
    else:
        return jsonify({"error": "URL no encontrada"}), 404

# Endpoint para descargar archivos
@app.route('/descargar', methods=['GET'])
def descargar():
    data = request.get_json()
    archivo_a_descargar = data.get('archivo')
    url_peer = data.get('url')

    if url_peer not in peers:
        return jsonify({"error": "Peer no encontrado"}), 404

    peer_port = url_peer.split(":")[2]
    with grpc.insecure_channel(f'{url_peer.split(":")[1]}:{peer_port}') as channel:
        stub = catalog_pb2_grpc.CatalogStub(channel)
        try:
            response = stub.Download(catalog_pb2.DownloadRequest(filename=archivo_a_descargar))
            with open(f'./descargado_{archivo_a_descargar}', 'wb') as f:
                f.write(response.file_data)
            return jsonify({"mensaje": "Descarga completada"}), 200
        except grpc.RpcError as e:
            return jsonify({"error": f"Error en la descarga: {e.details()}"}), 500

if __name__ == "__main__":
    start_grpc_server()
    app.run(port=FLASK_PORT, debug=True)
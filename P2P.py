import logging
from flask import Flask, request, jsonify
import grpc
import catalog_pb2_grpc
import catalog_pb2
from concurrent import futures
import os
import secrets

app = Flask(__name__)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

peers = {}
gRPC_PORT = os.getenv('GRPC_PORT', '50051')
FLASK_PORT = os.getenv('FLASK_PORT', '5000')


def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    catalog_pb2_grpc.add_CatalogServicer_to_server(CatalogServicer(), server)
    server.add_insecure_port(f'[::]:{gRPC_PORT}')
    print("Server running in port 50051")
    server.start()
    logging.info(f"gRPC Server iniciado en puerto {gRPC_PORT}")


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
        
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')
    ip = data.get('ip')
    url = data.get('url')
    port = data.get('port')
    files = data.get('archivos')

    if not user or not password or not url or not port or not files or not ip:
        return jsonify({"Error": "Faltan datos (user, password, url, port o files)"}), 400

    full_url = f"{url}:{port}"
    token = secrets.token_urlsafe(6)

    peer_key = (full_url, ip)

    if peer_key in peers:
        logging.info(f"Peer ya se encuentra conectado: {full_url}")
        return jsonify({"message": "Peer ya se encuentra conectado"}), 400
    
    peers[peer_key] = {"user": user, "token": token, "files": [files]}

    logging.info(f"Peer conectado correctamente en: {full_url}")
    return jsonify({"estado": "OK", "token": token}), 200

# Endpoint para index
@app.route('/index', methods=['POST'])
def index():
    data = request.get_json()
    ip = data.get('ip')
    url = data.get('url')

    if not ip or not url:
        return jsonify({"error": "Faltan datos (ip o url)"}), 400

    peer_key = (url, ip)

    peer_info = peers.get(peer_key)

    if peer_info:
        response = {
            "nombre": peer_info.get("user"),
            "files": peer_info.get("files", [])
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "Peer no encontrado"}), 404

# Endpoint para search
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    archivo_buscado = data.get('archivo')
    
    if not archivo_buscado:
        return jsonify({"error": "Falta el nombre del archivo a buscar"}), 400
    
    resultados = []
    for (url, ip), info in peers.items():
        archivos = info.get("files", [])
        for archivo in archivos:
            archivos_list = archivo.split(',')
            if archivo_buscado in archivos_list:
                resultados.append({"url": url, "ip": ip, "nombre": info.get("user")})
    
    if resultados:
        return jsonify({"peers": resultados}), 200
    else:
        return jsonify({"mensaje": "Archivo no encontrado"}), 404

# Endpoint para logout
@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    ip = data.get('ip')
    url = data.get('url')

    if not ip or not url:
        return jsonify({"error": "Faltan datos (ip o url)"}), 400

    peer_key = (url, ip)

    if peer_key in peers:
        del peers[peer_key]
        logging.info(f"Peer desconectado: {peer_key}")
        return jsonify({"mensaje": f"Peer {peer_key} desconectado correctamente."}), 200
    else:
        return jsonify({"error": "Peer no encontrado"}), 404

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
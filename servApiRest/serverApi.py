import logging
from flask import Flask, request, jsonify
import secrets
import grpc
from proto import catalog_pb2_grpc, catalog_pb2

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
peers = {}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')
    ip = data.get('ip')
    port = data.get('port')
    files = data.get('archivos')

    if not user or not password or not port or not files or not ip:
        return jsonify({"Error": "Faltan datos (user, password, url, port o files)"}), 400

    full_url = f"http.//localhost:{port}"
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
    
# Endpoint grpc para descargar
@app.route('/descargar', methods=['POST'])
def descargar():
    data = request.get_json()
    archivo_a_descargar = data.get('archivo')
    url_peer = data.get('url')

    if not archivo_a_descargar or not url_peer:
        return jsonify({"error": "Faltan datos (archivo o url)"}), 400

    peer_key = (url_peer, data.get('ip'))

    if peer_key not in peers:
        return jsonify({"error": "Peer no encontrado"}), 404

    peer_port = url_peer.split(":")[2]
    peer_ip = url_peer.split(":")[1]

    # Conectar a gRPC server del peer
    with grpc.insecure_channel(f'{peer_ip}:{peer_port}') as channel:
        stub = catalog_pb2_grpc.CatalogStub(channel)
        try:
            response = stub.Download(catalog_pb2.DownloadRequest(filename=archivo_a_descargar))
            if response.file_data:
                file_name = f'descargado_{archivo_a_descargar}'
                with open(file_name, 'wb') as f:
                    f.write(response.file_data)
                logging.info(f"Archivo descargado exitosamente: {archivo_a_descargar}")
                return jsonify({"estado": "Descargado", "archivo": file_name}), 200
            else:
                return jsonify({"error": "Archivo no encontrado"}), 404
        except grpc.RpcError as e:
            logging.error(f"Error al descargar {archivo_a_descargar}: {str(e)}")
            return jsonify({"error": "Error en la descarga"}), 500
        
if __name__ == "__main__":
    app.run(port=5000, debug=True) 



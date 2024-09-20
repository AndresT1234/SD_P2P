import logging
from flask import Flask, request, jsonify
import secrets

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
        return jsonify({"Error": "Faltan datos (user, password, ip,port o files)"}), 400

    full_url = f"http://{ip}:{port}"
    token = secrets.token_urlsafe(6)
    peer_key = (full_url)

    if peer_key in peers:
        logging.info(f"Peer ya se encuentra conectado: {full_url}")
        return jsonify({"message": "Peer ya se encuentra conectado"}), 400
    
    peers[peer_key] = {"user": user, "token": token, "files": [files]}

    logging.info(f"Peer conectado correctamente en: {full_url}\n")
    logging.info(f"Peers conectados: \n{peers}\n")
    return jsonify({"estado": "OK", "token": token}), 200


# Endpoint para index
@app.route('/index', methods=['GET'])
def index():

    all_files = []
    for peer in peers.values():
        all_files.extend(peer.get("files", []))

    if all_files:
        return jsonify({"files": all_files}), 200
    else:
        return jsonify({"error": "No hay archivos"}), 404
    

# Endpoint para search
@app.route('/search', methods=['GET'])
def search():
    data = request.get_json()
    archivo_buscado = data.get('archivo')
    
    if not archivo_buscado:
        return jsonify({"error": "Falta el nombre del archivo a buscar"}), 400
    
    resultados = []
    for url , info in peers.items():
        archivos = info.get("files", [])
        for archivo in archivos:
            files_string = ','.join(archivo)
            archivos_list = files_string.split(',')
            if archivo_buscado in archivos_list:
                resultados.append({"url": url, "nombre": info.get("user")})
    
    if resultados:
        return jsonify({"peers": resultados}), 200
    else:
        return jsonify({"mensaje": "Archivo no encontrado"}), 404

# Endpoint para logout
@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "Faltan datos (url)"}), 400

    peer_key = (url)

    if peer_key in peers:
        del peers[peer_key]
        logging.info(f"Peer desconectado: {peer_key}")
        return jsonify({"mensaje": f"Peer {peer_key} desconectado correctamente."}), 200
    else:
        return jsonify({"error": "Peer no encontrado"}), 404
    

@app.route('/loadfiles', methods=['PUT'])
def loadfiles():
    data = request.get_json()
    ip = data.get('ip')
    port = data.get('port')
    files = data.get('archivos')

    if not port or not files or not ip:
        return jsonify({"Error": "Faltan datos (ip, port o files)"}), 400

    full_url = f"http://{ip}:{port}"
    peer_key = (full_url, ip)

    if peer_key not in peers:
        logging.info(f"Peer no está conectado: {full_url}")
        return jsonify({"message": "Peer no está conectado"}), 400

    peers[peer_key] = {"files": [files]}

    return jsonify({"estado": "OK"}), 200
    
        
if __name__ == "__main__":
    app.run(host= 'localhost', port=5000, debug=True)

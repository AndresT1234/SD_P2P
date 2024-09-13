import logging
from flask import Flask, request, jsonify


app= Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

peers = {}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    ip = data.get('ip')
    archivos = data.get('archivos')

    if not ip or not archivos:
        return jsonify({"Error": "Faltan datos (ip o archivos)"}), 400

    peers[ip] = {"archivos": archivos}
    
    logging.info(f"Peer conectados: {peers}")

    return jsonify({"mensaje": f"Peer {ip} conectado exitosamente."}), 200



@app.route('/index', methods=['POST'])
def index():
    return jsonify(peers), 200


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    archivo_buscado = data.get('archivos')
    
    if not archivo_buscado:
        return jsonify({"error": "Falta el nombre del archivo a buscar"}), 400
    
    for ip, info in peers.items():
        archivos = info.get("archivos")
        if archivo_buscado in archivos.split(", "):
            return jsonify({"ip": ip}), 200
    
    return jsonify({"mensaje": "Archivo no encontrado"}), 404


@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    ip = data.get('ip')
    
    if not ip:
        return jsonify({"error": "Falta la ip del peer"}), 400

    if ip in peers:
        del peers[ip]
        logging.info(f"Peer conectados: {peers}")
        return jsonify({"mensaje": f"Peer {ip} desconectado correctamente."}), 200
    else:
        return jsonify({"error": "IP no encontrada"}), 404



if __name__ == "__main__":
    app.run(debug=True)   
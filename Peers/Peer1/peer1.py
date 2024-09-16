import requests
import json

DOWNLOAD_PATH = "../files" 

class Peer1:

    API_URL = "http://127.0.0.1:5000"

    def __init__(self):

        with open("config.json") as f:
            data = json.load(f)
            self.user = data['user']
            print(self.user)
            self.password = data['password']
            self.ip = data['ip']
            self.port = data['port']
            self.files = data['archivos']
            self.peers = {}
    
    def login(self, user, password, ip, port, files):
        if not user or not password or not port or not files or not ip:
            return {"Error": "Faltan datos (user, password, url, port o files)"}, 400

        full_url = f"http://127.0.0.1:5000/login"
        peer_key = (full_url, ip)

        if peer_key in self.peers:
            return {"message": "Peer ya se encuentra conectado"}, 400

        response = requests.post(full_url, json={"user": user, "password": password, "ip": ip, "port": port, "archivos": files})

        if response.status_code == 200:
            token = response.json().get('token')
            if token:
                self.peers[peer_key] = {"user": user, "token": token, "files": [files]}
                return {"estado": "OK", "token": token}, 200
            else:
                return {"Error": "No se recibió token en la respuesta"}, 400
        else:
            return {"Error": "Falló la conexión con el servidor"}, response.status_code
        
    def index(self, ip, url):
        if not ip or not url:
            return {"error": "Faltan datos (ip o url)"}, 400

        response = requests.post("http://127.0.0.1:5000/index", json={"ip": ip, "url": url})

        if response.status_code == 200:
            response = response.json()
            return response, 200
        else:
            return {"error": "Peer no encontrado"}, 404

    def search(self, archivo_buscado):
        if not archivo_buscado:
            return {"error": "Falta el nombre del archivo a buscar"}, 400

        response = requests.post("http://127.0.0.1:5000/search", json={"archivo": archivo_buscado})

        if response.status_code == 200:
            response = response.json()
            return response, 200
        else:
            return {"error": "No se encontraron resultados"}, 404
    
    def logout(self, ip, url):
        if not ip or not url:
            return {"error": "Faltan datos (ip o url)"}, 400

        response = requests.post("http://127.0.0.1:5000/logout", json={"ip": ip, "url": url})

        if response.status_code == 200:
            response = response.json()
            return response, 200
        else:
            return {"error": "Peer no encontrado"}, 404
        

def main():
    peer = Peer1()
    result = peer.login(peer.user, peer.password, peer.ip, peer.port, peer.files)
    result1 = peer.index(peer.ip, "http://127.0.0.1:5001")
    result2 = peer.search("file1.txt")
    result3 = peer.logout(peer.ip, "http://127.0.0.1:5001")
    print(result)
    print(result1)
    print(result2)
    print(result3)

if __name__ == "__main__":
    main()
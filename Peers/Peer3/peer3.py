import requests
import json

class Peer3:
    def __init__(self):
        with open("config.json") as f:
            data = json.load(f)
            self.user = data['user']
            print(self.user)
            self.password = data['password']
            self.ip = data['ip']
            self.port = data['port']
            self.files = data['archivos']
            self.api_url = data['api_url']
            self.peers = {}
            
    

    def login(self, user, password, ip, port, files, api_url):
        if not user or not password or not port or not files or not ip or not api_url:
            return {"Error": "Faltan datos (user, password, url, port, files o api_url)"}, 400

        peer_key = (api_url, ip)

        if peer_key in self.peers:
            return {"message": "Peer ya se encuentra conectado"}, 400

        response = requests.post(f"{api_url}/login", json={"user": user, "password": password, "ip": ip, "port": port, "archivos": files})

        if response.status_code == 200:
            token = response.json().get('token')
            if token:
                self.peers[peer_key] = {"user": user, "token": token, "files": [files]}
                return {"estado": "OK", "token": token}, 200
            else:
                return {"Error": "No se recibió token en la respuesta"}, 400
        else:
            return {"Error": "Falló la conexión con el servidor"}, response.status_code
        

    def index(self, ip, url, api_url):
        if not ip or not url or not api_url:
            return {"error": "Faltan datos (ip, url o api_url)"}, 400

        response = requests.post(f"{api_url}/index", json={"ip": ip, "url": url})

        if response.status_code == 200:
            response = response.json()
            return response, 200
        else:
            return {"error": "Peer no encontrado"}, 404


    def search(self, archivo_buscado, api_url):
        if not archivo_buscado:
            return {"error": "Falta el nombre del archivo a buscar"}, 400
        if not api_url:
            return {"error": "Falta la url del api"}, 400

        response = requests.post(f"{api_url}/search", json={"archivo": archivo_buscado})

        if response.status_code == 200:
            response = response.json()
            return response, 200
        else:
            return {"error": "No se encontraron resultados"}, 404
    

    def logout(self, ip, url, api_url):
        if not ip or not url or not api_url:
            return {"error": "Faltan datos (ip, url o api_url)"}, 400

        response = requests.post(f"{api_url}/logout", json={"ip": ip, "url": url})

        if response.status_code == 200:
            response = response.json()
            return response, 200
        else:
            return {"error": "Peer no encontrado"}, 404
        

def main():
    peer = Peer3()
    result = peer.login(peer.user, peer.password, peer.ip, peer.port, peer.files, peer.api_url)
    result1 = peer.index(peer.ip, "http://127.0.0.1:5001", peer.api_url)
    result2 = peer.search("file1.txt", peer.api_url)
    #result3 = peer.logout(peer.ip, "http://127.0.0.1:5001")
    print(result)
    print(result1)
    print(result2)
    #print(result3)

if __name__ == "__main__":
    main()

    
import requests
import json
import sys

class Peer4:
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
    peer = Peer4()

    #Verificamos que se haya pasado un parametro
    if len(sys.argv) < 1:
        print("Uso: python script.py <funcion>")
        sys.exit(1)

    #Obtenemos el primer parametro
    parametro1 = sys.argv[1]

    #Ejecutamos la funcion correspondiente
    if parametro1 == "/login":
        login_response = peer.login(peer.user, peer.password, peer.ip, peer.port, peer.files, peer.api_url)
        print("Login response:", login_response)

    elif parametro1 == "/index":
        index_response = peer.index(peer.ip, f"http://{peer.ip}:{peer.port}", peer.api_url)
        print("Index response:", index_response)
    
    elif parametro1 == "/logout":
        logout_response = peer.logout(peer.ip, f"http://{peer.ip}:{peer.port}", peer.api_url)
        print("Logout response:", logout_response)
    
    elif parametro1 == "/search":
        #Obtenemos el segundo parametro
        parametro2 = sys.argv[2]
        search_response = peer.search(parametro2, peer.api_url)
        print("Search response:", search_response)

    #En caso de que el comando no exista
    else:
        print("Error en el comando")


if __name__ == "__main__":
    main()
    
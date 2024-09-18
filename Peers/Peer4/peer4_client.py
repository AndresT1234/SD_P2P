import requests
import json
import sys
import os

# Agregar el directorio padre al path para importar los módulos de gRPC
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from gRPC import peer_pb2, peer_pb2_grpc


class Peer4:
    DOWNLOAD_PATH = "" # Directorio donde se almacenan los archivos descargados

    def __init__(self):
        with open("config.json") as f:
            data = json.load(f)
            self.user = data['user']
            print(self.user)
            self.password = data['password']
            self.ip = data['ip']
            self.port = data['port']
            self.files = os.listdir(data['files_path'])
            Peer4.DOWNLOAD_PATH = data['files_path_download']
            self.api_url = data['api_url']
            
    
    def login(self, user, password, ip, port, files, api_url):
        if not user or not password or not port or not files or not ip or not api_url:
            return {"Error": "Faltan datos (user, password, url, port, files o api_url)"}, 400

        else:
            response = requests.post(f"{api_url}/login", json={"user": user, "password": password, "ip": ip, "port": port, "archivos": files})
            return response.json(), response.status_code
        

    def index(self, ip, url, api_url):
        if not ip or not url or not api_url:
            return {"error": "Faltan datos (ip, url o api_url)"}, 400

        response = requests.get(f"{api_url}/index", json={"ip": ip, "url": url})

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

        response = requests.get(f"{api_url}/search", json={"archivo": archivo_buscado})

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
        

def download_file(peer_address, filename):
    # Conectar al peer en la dirección indicada (IP:puerto)
    channel = peer_pb2_grpc.grpc.insecure_channel(peer_address)
    stub = peer_pb2_grpc.PeerServiceStub(channel)
    
    # Crear una solicitud de archivo
    request = peer_pb2.FileRequest(filename=filename)
    
    # Realizar la descarga del archivo en chunks
    try:
        response = stub.DownloadFile(request)
        with open(os.path.join(Peer4.DOWNLOAD_PATH, f"downloaded_{filename}"), 'wb') as f:
            for chunk in response:
                f.write(chunk.content)
        print(f"Archivo {filename} descargado exitosamente.")

        # Cargar los archivos en el servidor
        responseLoadFiles = load_files()
        print(responseLoadFiles)
    except peer_pb2_grpc.grpc.RpcError as e:
        print(f"Error al descargar el archivo: {e.details()}")


def load_files():
    with open("config.json") as f:
        data = json.load(f)
        files = os.listdir(data['files_path'])
        ip = data['ip']
        port = data['port']
        api_url = data['api_url']
    
    response = requests.put(f"{api_url}/loadfiles", json={"ip": ip, "port": port, "archivos": files})
        
    if response.status_code == 200:
            return {"estado": "OK", "message": "archivos cargados correctamente"}, 200
    else:
        return {"Error": "Falló cargando los archivos"}, response.status_code


def main():
    peer = 4()

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

    elif parametro1 == "/download":
        #Obtenemos el segundo parametro
        peer_address = sys.argv[2] #Direccion del peer al que conectarse
        filename = sys.argv[3] #Archivo a descargar

        download_file(peer_address, filename)

    #En caso de que el comando no exista
    else:
        print("Error en el comando")


if __name__ == "__main__":
    main()
import requests
import sys

API_URL = "http://localhost:5000"  # URL del API

#Funciones que consumen el API
def login(peer_info):
    response = requests.post(f"{API_URL}/login", json=peer_info)
    return response.json()

def index(peer_info):
    response = requests.post(f"{API_URL}/index", json=peer_info)
    return response.json()

def logout(peer_info):
    response = requests.post(f"{API_URL}/logout", json=peer_info)
    return response.json()

def search(peer_info):
    response = requests.post(f"{API_URL}/search", json=peer_info)
    return response.json()


#Inicio del programa
if __name__ == "__main__":
    
    #Verificamos que se haya pasado un parametro
    if len(sys.argv) < 1:
        print("Uso: python script.py <funcion>")
        sys.exit(1)

    #Obtenemos el primer parametro
    parametro1 = sys.argv[1]
    
    #Ejecutamos la funcion correspondiente
    if parametro1 == "/login":
        peer_info = {"user": "peer1", "password":"unaClav3","ip":"127.0.0.1","port": "5001", "archivos": "archivo1.txt, archivo2.txt"}
        login_response = login(peer_info)
        print("Login response:", login_response)

    elif parametro1 == "/index":
        peer_info = {"ip":"127.0.0.1","url": "localhost:5001"}
        index_response = index(peer_info)
        print("Index response:", index_response)

    elif parametro1 == "/logout":
        peer_info = {"ip":"127.0.0.1","url": "localhost:5001"}
        logout_response = logout(peer_info)
        print("Logout response:", logout_response)

    elif parametro1 == "/search":
        #Obtenemos el segundo parametro
        parametro2 = sys.argv[2]
        peer_info = {"archivo":parametro2}
        search_response = search(peer_info)
        print("Search response:", search_response)

    #En caso de que el comando no exista
    else:
        print("Error en el comando")

    
import requests
import sys

API_URL = "http://localhost:5000"  # URL del API

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

if __name__ == "__main__":
    
    if len(sys.argv) < 1:
        print("Uso: python script.py <funcion>")
        sys.exit(1)

    parametro1 = sys.argv[1]
    

    if parametro1 == "/login":
        peer_info = {"user": "peer2", "password":"otraClav3","ip":"127.0.0.1","port": "5002", "archivos": "archivo1.txt, archivo2.txt"}
        login_response = login(peer_info)
        print("Login response:", login_response)

    elif parametro1 == "/index":
        peer_info = {"ip":"127.0.0.1","url": "localhost:5002"}
        index_response = index(peer_info)
        print("Index response:", index_response)

    elif parametro1 == "/logout":
        peer_info = {"ip":"127.0.0.1","url": "localhost:5002"}
        logout_response = logout(peer_info)
        print("Logout response:", logout_response)

    elif parametro1 == "/search":
        parametro2 = sys.argv[2]
        peer_info = {"archivo":parametro2}
        search_response = search(peer_info)
        print("Search response:", search_response)

    else:
        print("Error en el comando")

    #search_result = search_file("archivo1.txt")
    #print("Search result:", search_result)

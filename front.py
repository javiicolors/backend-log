import requests
from getpass import getpass

BASE_URL = "http://127.0.0.1:8000"  # URL base de tu backend de FastAPI

def register_user():
    print("\n=== Registro de Nuevo Usuario ===")
    username = input("Nombre de usuario: ")
    email = input("Correo electrónico: ")
    password = getpass("Contraseña: ")
    
    response = requests.post(f"{BASE_URL}/users/", json={
        "username": username,
        "email": email,
        "password": password
    })
    
    if response.status_code == 200:
        print("Registro exitoso.")
    else:
        print("Error:", response.json().get("detail"))

def login():
    print("\n=== Inicio de Sesión ===")
    username = input("Nombre de usuario: ")
    password = getpass("Contraseña: ")

    response = requests.post(f"{BASE_URL}/login/", json={
        "username": username,
        "password": password
    })
    
    if response.status_code == 200:
        print("Inicio de sesión exitoso.")
        return True
    else:
        print("Error:", response.json().get("detail"))
        return False

def main():
    while True:
        print("\n=== Menú ===")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")

        choice = input("Seleccione una opción: ")
        
        if choice == "1":
            if login():
                break  # Sale del loop si el login es exitoso
        elif choice == "2":
            register_user()
        elif choice == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()

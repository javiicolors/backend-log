#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 18:26:57 2024

@author: javiicolors
"""

import requests
from getpass import getpass

# Cambia esta URL por la URL de tu backend desplegado
# BASE_URL = "http://127.0.0.1:8000"  # Localhost para pruebas
BASE_URL = "https://backend-log-afjt.onrender.com"

user_id = 00

def register_user():
    """Función para registrar un nuevo usuario."""
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
        print("Error:", response.json().get("detail", "Error desconocido"))

def login():
    """Función para iniciar sesión."""
    print("\n=== Inicio de Sesión ===")
    username = input("Nombre de usuario: ")
    password = getpass("Contraseña: ")

    response = requests.post(f"{BASE_URL}/login/", json={
        "username": username,
        "password": password
    })

    if response.status_code == 200:
        print("Inicio de sesión exitoso.")
        return response.json()["user_id"]  # Devuelve el ID del usuario
    else:
        print("Error:", response.json().get("detail", "Error desconocido"))
        return None

def download_files(user_id):
    """Función para gestionar las descargas."""
    print("\n=== Descargas ===")
    available_files = ["archivo1.txt", "archivo2.pdf", "imagen1.png", "salir"]

    while True:
        print("\nArchivos disponibles para descargar:")
        for i, file in enumerate(available_files, 1):
            print(f"{i}. {file}")

        choice = input("Seleccione un archivo para descargar (número): ")

        try:
            choice = int(choice)
            if 1 <= choice <= len(available_files):
                selected_file = available_files[choice - 1]
                if selected_file.lower() == "salir":
                    print("Saliendo de la sección de descargas.")
                    break

                # Registrar la descarga en el backend
                response = requests.post(f"{BASE_URL}/downloads/", json={
                    "user_id": user_id,
                    "filename": selected_file
                })

                if response.status_code == 200:
                    print(f"Descarga registrada: {selected_file}")
                else:
                    print("Error al registrar la descarga:", response.text)
            else:
                print("Opción no válida.")
        except ValueError:
            print("Ingrese un número válido.")

def main():
    """Menú principal del programa."""
    while True:
        print("\n=== Menú ===")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")

        choice = input("Seleccione una opción: ")

        if choice == "1":
            user_id = login()
            if user_id:
                download_files(user_id)  # Llamada al menú de descargas
                break  # Sale del loop si el usuario accedió y terminó
        elif choice == "2":
            register_user()
        elif choice == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()


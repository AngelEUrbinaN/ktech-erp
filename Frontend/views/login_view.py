import customtkinter as ctk
from tkinter import messagebox
import requests
from config.api_config import API_URL

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, callback_login_exitoso):
        super().__init__(parent)
        self.callback_login_exitoso = callback_login_exitoso
        self.pack(fill="both", expand=True)
        self.crear_interfaz()

    def crear_interfaz(self):
        ktech = ctk.CTkLabel(self, text="KTech ERP", font=ctk.CTkFont(size=26, weight="bold"))
        ktech.pack(pady=(40, 5))
        title = ctk.CTkLabel(self, text="Iniciar Sesión", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=(5, 30))

        self.correo_entry = ctk.CTkEntry(self, placeholder_text="Correo", width=300)
        self.correo_entry.pack(pady=10)

        self.contrasena_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=300)
        self.contrasena_entry.pack(pady=10)

        login_button = ctk.CTkButton(self, text="Iniciar sesión", command=self.intentar_login)
        login_button.pack(pady=20)

    def intentar_login(self):
        correo = self.correo_entry.get()
        contrasena = self.contrasena_entry.get()

        if not correo or not contrasena:
            messagebox.showwarning("Campos requeridos", "Completa todos los campos.")
            return

        try:
            response = requests.post(f"{API_URL}/iniciar_sesion", json={
                "correo": correo,
                "contrasena": contrasena
            })

            if response.status_code == 200:
                data = response.json()
                print("Respuesta JSON:", response.json())
                if data.get("success") and "departamento_id" in data:
                    departamento_id = data["departamento_id"]
                    self.callback_login_exitoso(departamento_id)
                else:
                    messagebox.showerror("Error", "Inicio de sesión inválido. Verifica tus credenciales.")
            else:
                messagebox.showerror("Error", f"Error de servidor: código {response.status_code}")
        except Exception as e:
            print("Error durante login:", e)
            messagebox.showerror("Error", f"No se pudo conectar con el servidor:\n{e}")

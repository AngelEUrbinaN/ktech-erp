import customtkinter as ctk
from views.login_view import LoginView
from main import KTechERP

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Login - KTech ERP")
    root.geometry("400x300")
    root.resizable(False, False)

    def iniciar_erp(departamento_id):
        root.withdraw()
        app = KTechERP(departamento_id)
        app.mainloop()
        root.destroy()

    login = LoginView(root, iniciar_erp)
    root.mainloop()
import flet as ft
import httpx

class inicio(ft.Container):
    def __init__(self, on_login_success):
        super().__init__(expand=True)
        self.on_login_success = on_login_success

        self.bgcolor = "#3f3965"
        self.xcolor = "#000000"

        self.color1 = ft.colors.PURPLE_700
        self.color2 = ft.colors.PURPLE_400
        self.color_text = self.xcolor

        self.username = ft.TextField(
            label="Usuario", width=300,
            text_style=ft.TextStyle(color=self.color_text),
            border_color=self.color2, focused_border_color=self.color1, cursor_color=self.color1
        )
        self.password = ft.TextField(
            label="Contraseña", width=300, password=True, can_reveal_password=True,
            text_style=ft.TextStyle(color=self.color_text),
            border_color=self.color2, focused_border_color=self.color1, cursor_color=self.color1
        )

        login_btn = ft.ElevatedButton(
            text="Iniciar Sesión", width=300,
            bgcolor=self.color1, color=self.color_text,
            on_click=self.on_login
        )

        linea_gradiante = ft.Container(
            height=3, width=300, border_radius=20,
            gradient=ft.SweepGradient(
                center=ft.alignment.center,
                colors=[
                    ft.colors.RED, ft.colors.ORANGE, ft.colors.YELLOW, ft.colors.GREEN,
                    ft.colors.CYAN, ft.colors.BLUE, ft.colors.PURPLE, ft.colors.RED,
                ]
            )
        )

        crear_usuario_btn = ft.Container(
            content=ft.TextButton(
                text="Crear usuario",
                on_click=lambda _: self.mostrar_crear_usuario(),
                style=ft.ButtonStyle(color=self.color_text),
            ),
            width=300,
            padding=ft.padding.all(2),
            border_radius=10,
            gradient=linea_gradiante.gradient,
        )

        self.login_ui = ft.Container(
            bgcolor=self.bgcolor,
            content=ft.Column(
                controls=[
                    ft.Text("Bienvenido", size=32, weight="bold", color=self.color_text),
                    ft.Text("Por favor, ingresa tus datos", size=16, color=self.color_text),
                    self.username,
                    self.password,
                    login_btn,
                    ft.Text("o", color=self.color_text, size=20),
                    linea_gradiante,
                    crear_usuario_btn,
                ],
                alignment="center",
                spacing=20,
                horizontal_alignment="center"
            ),
            expand=True,
            alignment=ft.alignment.center
        )

        self.crear_usuario_ui = self.vista_crear_usuario()

        self.content = self.login_ui  

    def on_login(self, e):
        if self.username.value and self.password.value:
            data = {
                "usuario": self.username.value,
                "contraseña": self.password.value
            }
            try:
                response = httpx.post("http://localhost:8000/login", json=data)
                if response.status_code == 200:
                    print("Inicio de sesión exitoso")
                    self.on_login_success()
                else:
                    print("Error:", response.json()["detail"])
            except Exception as ex:
                print("Error al conectar con el backend:", ex)
        else:
            print("Faltan datos")


    def mostrar_crear_usuario(self):
        self.content = self.crear_usuario_ui
        self.update()

    def volver_al_login(self, e=None):
        self.content = self.login_ui
        self.update()

    def guardar_usuario(self, e):
        if all([self.email.value, self.new_username.value, self.new_password.value, self.finca_name.value]):
            data = {
                "correo": self.email.value,
                "usuario": self.new_username.value,
                "contraseña": self.new_password.value,
                "finca": self.finca_name.value
            }
            try:
                response = httpx.post("http://localhost:8000/registro", json=data)
                if response.status_code == 200:
                    print("Usuario creado con éxito")
                    self.volver_al_login()
                else:
                    try:
                        error_detail = response.json().get("detail", "Error desconocido")
                    except Exception:
                        error_detail = response.text or "Respuesta no válida del servidor"
                    print("Error:", error_detail)
            except Exception as ex:
                print("Error al conectar con el backend:", ex)




    def vista_crear_usuario(self):
        self.email = ft.TextField(
            label="Correo electrónico", width=300,
            text_style=ft.TextStyle(color=self.color_text),
            border_color=self.color2, focused_border_color=self.color1, cursor_color=self.color1
        )
        self.new_username = ft.TextField(
            label="Nombre de usuario", width=300,
            text_style=ft.TextStyle(color=self.color_text),
            border_color=self.color2, focused_border_color=self.color1, cursor_color=self.color1
        )
        self.new_password = ft.TextField(
            label="Contraseña", width=300, password=True, can_reveal_password=True,
            text_style=ft.TextStyle(color=self.color_text),
            border_color=self.color2, focused_border_color=self.color1, cursor_color=self.color1
        )
        self.finca_name = ft.TextField(
            label="Nombre de la finca", width=300,
            text_style=ft.TextStyle(color=self.color_text),
            border_color=self.color2, focused_border_color=self.color1, cursor_color=self.color1
        )

        guardar_btn = ft.ElevatedButton(
            text="Guardar", width=300,
            bgcolor=self.color1, color=self.color_text,
            on_click=self.guardar_usuario
        )

        volver_btn = ft.TextButton(
            text="Volver", on_click=self.volver_al_login,
            style=ft.ButtonStyle(color=self.color_text)
        )

        return ft.Container(
            bgcolor=self.bgcolor,
            content=ft.Column(
                controls=[
                    ft.Text("Crear nuevo usuario", size=28, weight="bold", color=self.color_text),
                    self.email,
                    self.new_username,
                    self.new_password,
                    self.finca_name,
                    guardar_btn,
                    volver_btn
                ],
                alignment="center",
                spacing=20,
                horizontal_alignment="center"
            ),
            expand=True,
            alignment=ft.alignment.center
        )

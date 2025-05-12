import flet as ft

class Login(ft.View):
    def __init__(self, parent_page, route, on_click):
        super().__init__() 
        self.padding = ft.Padding(left=50, top=50, right=50, bottom=0)
        self.parent_page = parent_page
        self.route = route
        self.on_submit = on_click
        
        
    def build(self):
        idTextField = ft.TextField(
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            width = 300,
            autofocus=True,
            on_submit= lambda _: pinTextField.focus()
        )

        pinTextField = ft.TextField(
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            password=True, 
            can_reveal_password=True,        
            width = 300,
            autofocus=False,
            on_submit=self.on_submit
        )

        return ft.Column(
            controls=[
                ft.Text("ID User", size=30, ), 
                idTextField,
                ft.Text("PIN", size=30,), 
                pinTextField, 
            ], 
            spacing=20,
            horizontal_alignment="left",
            alignment="center",
        )
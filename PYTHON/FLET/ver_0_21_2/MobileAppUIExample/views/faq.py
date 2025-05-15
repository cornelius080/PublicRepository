import flet as ft

class Faq(ft.View):
    def __init__(self, parent_page, route, go_to_view_home):
        super().__init__()
        self.parent_page = parent_page
        self.route = route
        self.go_to_view_home = go_to_view_home
        self.scroll = ft.ScrollMode.ALWAYS
        self.bgcolor = ft.colors.GREEN_900        


    def chips_on_click(self, e):
        self.snackbar.content = ft.Text(f"{e.control.label.value} VIEW - NOT IMPLEMENTED YET")
        self.snackbar.open = True        
        self.snackbar.update()

    def build_exp_panel(self, header: str, content: str):
        col = ft.Column([], horizontal_alignment="center")
        for i in range(10):
            col.controls.append(
                ft.Chip(
                    label=ft.Text(content,),
                    bgcolor=ft.colors.GREEN_600,
                    on_click=self.chips_on_click,
                )
            )

        return ft.ExpansionPanel(
            bgcolor = ft.colors.GREEN_400,  
            can_tap_header=True,
            header=ft.Text(header, style=ft.TextStyle(color=ft.colors.WHITE)),
            content=col,                      
        )

    def build(self):
        self.snackbar = ft.SnackBar(
            content=ft.Text(""),
            duration=1000,
        )
        self.parent_page.overlay.append(self.snackbar)

        row1 = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK, icon_color=ft.colors.WHITE, icon_size=30,
                    on_click=self.go_to_view_home,
                ),
                ft.Text("Frequently Asked Questions", style=ft.TextStyle(size=20,italic=True, color=ft.colors.WHITE)),
            ],
        )
        row2 = ft.Row(
            controls=[
                ft.Text("Hi Jhon, how can we help you?", style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)),
            ],
        )
        
        panel1 = self.build_exp_panel(header=" Card block and fraud report", content="CONTENT_1")
        panel2 = self.build_exp_panel(header=" Current account and payment cards", content="CONTENT_2")
        panel3 = self.build_exp_panel(header=" Loans", content="CONTENT_3",)
        panel4 = self.build_exp_panel(header=" Investments and consulting", content="CONTENT_4")
        panel5 = self.build_exp_panel(header=" Protection policy", content="CONTENT_5",)

        return ft.Container(           
            content=ft.Column(
                [              
                    row1,
                    row2,
                    ft.ExpansionPanelList(
                        divider_color=ft.colors.GREEN_900,
                        controls=[
                            panel1,
                            panel2,
                            panel3,
                            panel4,
                            panel5,
                        ],
                    ),
                ],
            )
            
        )
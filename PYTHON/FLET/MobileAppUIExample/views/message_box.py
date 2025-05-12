import flet as ft
from transactions.bank_transactions import BankTransactions

class MessageBox(ft.View):
    def __init__(self, parent_page, route, go_to_view_home):
        super().__init__()
        self.parent_page = parent_page
        self.route = route
        self.go_to_view_home = go_to_view_home
        self.bgcolor = ft.colors.GREEN_900
        self.trans = BankTransactions(50).transactions

    def chips_info_on_click(self, e):
        self.messages.content = self.info_content      
        self.update()

    def chips_movements_on_click(self, e):
        self.messages.content = self.movements_content
        self.update()

    def transactions_on_click(self, e, idx):
        self.bs_content.controls=[
            ft.Row(
                controls=[
                    ft.Text("Details", style=ft.TextStyle(size=18, italic=True, weight=ft.FontWeight.BOLD)),
                    ft.Text(f"ID: {self.trans[idx]['transaction_id']}", style=ft.TextStyle(size=18)),
                ],
                alignment="spaceBetween",
            ),
            ft.Divider(),
            ft.Text(f"{self.trans[idx]['date']}", style=ft.TextStyle(size=18)),
            ft.Text(f"Type: {self.trans[idx]['type']}", style=ft.TextStyle(size=18)),
            ft.Text(f"Amount: {self.trans[idx]['amount']}", style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
        ]   
        if len(self.trans[idx]['company'])>0:     
            self.bs_content.controls.append(
                ft.Text(f"Company: {self.trans[idx]['company']}", style=ft.TextStyle(size=18, italic=True)))
        self.bs.open = True
        self.bs.update()
    
    def info_on_click(self, e):
        self.bs_content.controls=[
            ft.Text(f"{e.control.content.value}\nSome other detail here", style=ft.TextStyle(size=18)),
        ]        
        self.bs.open = True
        self.bs.update()

    def build_info_content(self):              
        lv = ft.ListView(expand=True)
        for i in range(0, 15):
            lv.controls.append(
                ft.Column(
                    controls=[
                        ft.Container(
                            content = ft.Text(f"Info {i+1}", style=ft.TextStyle(size=18)),
                            on_click = self.info_on_click,
                        ),
                        ft.Divider(),                   
                ])                              
            )
        return lv
    
    def build_movements_content(self):    
        lv = ft.ListView(expand=True)

        for idx, trans in enumerate(self.trans):
            lv.controls.append(
                ft.Column(
                    controls=[
                        ft.Container(
                            content= ft.Column(
                                controls=[
                                    ft.Text(f"{trans['date'].split(' ')[0]}", style=ft.TextStyle(size=14)),
                                    ft.Row(
                                        controls=[
                                            ft.Text(f"{trans['type']}", style=ft.TextStyle(size=18)),
                                            ft.Text(f"{trans['amount']}", style=ft.TextStyle(size=18), weight=ft.FontWeight.BOLD),                                     
                                        ],
                                        alignment="spaceBetween"
                                    ),
                                ]
                            ),
                            on_click = lambda e, idx=idx: self.transactions_on_click(e, idx),
                        ),
                        ft.Divider(),                   
                ])                              
            )
        return lv

    def build(self):
        self.bs_content = ft.Column(tight=True, controls=[])
        self.bs = ft.BottomSheet(
            content=ft.Container(
                padding=ft.Padding(top=20, bottom=10, left=20, right=20),
                content=self.bs_content,                
            ),
        )
        self.parent_page.overlay.append(self.bs)

        self.info_content = self.build_info_content()
        self.movements_content = self.build_movements_content()
        self.messages = ft.Container(
            padding = ft.Padding(top=20, bottom=20, left=20, right=20),
            height = self.parent_page.window_height * 0.8,
            width = self.parent_page.window_width * 0.8,
            border_radius = ft.BorderRadius(top_left=20, top_right=20, bottom_left=0, bottom_right=0),
            bgcolor = ft.colors.WHITE,
            content = self.movements_content,
        )

        return ft.Container(    
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.IconButton(icon=ft.icons.ARROW_BACK, 
                                          icon_color=ft.colors.WHITE, icon_size=30, on_click=self.go_to_view_home,
                            ),                
                            ft.Text("Message Box", style=ft.TextStyle(size=20, italic=True, color=ft.colors.WHITE)),
                        ],
                    ), 
                    ft.Row(
                        [
                            ft.Container(width=14),
                            ft.Chip(
                                label=ft.Text("Movements", ),
                                on_click=self.chips_movements_on_click,
                            ),
                            ft.Chip(
                                label=ft.Text("Info",),
                                on_click=self.chips_info_on_click,
                            ),
                        ],
                    ), 
                    ft.Row([self.messages], alignment = "center"),                    
                ],
            )
        )
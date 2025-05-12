import flet as ft
from transactions.bank_transactions import BankTransactions

class Movements(ft.View):
    def __init__(self, route, parent_page, go_to_view_home):
        super().__init__()
        self.padding = 0
        self.bgcolor = ft.colors.GREEN_900
        self.route = route
        self.parent_page = parent_page
        self.go_to_view_home = go_to_view_home
        self.iban_number = "GB33BUKB20201555555555"
        self.trans = BankTransactions(50).transactions

    def copy_to_clipboard(self, e):
        self.parent_page.set_clipboard(self.iban_number)
        self.snackbar.content = ft.Text(f"{self.iban_number} copied to clipboard")
        self.snackbar.open = True        
        self.snackbar.update()

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

    def build_movements_content(self):    
        lv = ft.ListView(expand=True, padding=20, spacing=5)

        for idx, trans in enumerate(self.trans):
            lv.controls.append(
                ft.Column(
                    spacing=5,
                    controls=[
                        ft.Container(
                            padding = 10,
                            border = ft.border.all(1, ft.colors.GREEN_200),
                            border_radius=ft.BorderRadius(top_left=20, top_right=20, bottom_left=20, bottom_right=20),
                            bgcolor=ft.colors.LIGHT_GREEN_100,
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
        self.snackbar = ft.SnackBar(
            content=ft.Text(""),
            duration=1000,
        )
        self.parent_page.overlay.append(self.snackbar)

        self.bs_content = ft.Column(tight=True, controls=[])
        self.bs = ft.BottomSheet(
            content=ft.Container(
                padding=ft.Padding(top=20, bottom=10, left=20, right=20),
                content=self.bs_content,                
            ),
        )
        self.parent_page.overlay.append(self.bs)

        self.movements_content = self.build_movements_content()

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [ 
                            ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=ft.colors.WHITE, icon_size=26,on_click=self.go_to_view_home),  
                            ft.Text("Bank Account ***672", style=ft.TextStyle(size=16, italic=True, color=ft.colors.WHITE)), 
                            ft.Container(width=26),
                            ft.Text("Balance", style=ft.TextStyle(size=16, color=ft.colors.WHITE)),  
                            ft.Icon(ft.icons.BALANCE, color=ft.colors.WHITE, size=26,),                  
                        ],
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                bgcolor=ft.colors.WHITE,
                                border_radius = ft.BorderRadius(top_left=20, top_right=20, bottom_left=20, bottom_right=20),
                                padding=ft.Padding(top=10, bottom=10, left=20, right=20),
                                content=ft.Column(
                                    [
                                        ft.Text("Available", style=ft.TextStyle(size=16, color=ft.colors.BLACK)),
                                        ft.Text("€ 19325.71", style=ft.TextStyle(size=16, italic=True, color=ft.colors.BLACK)),
                                    ],
                                    horizontal_alignment="center", alignment = "center",
                                ),
                            ),
                            ft.Container(
                                bgcolor=ft.colors.WHITE,
                                border_radius = ft.BorderRadius(top_left=20, top_right=20, bottom_left=20, bottom_right=20),
                                padding=ft.Padding(top=10, bottom=10, left=20, right=20),
                                content=ft.Column(
                                    [
                                        ft.Text("Account", style=ft.TextStyle(size=16, color=ft.colors.BLACK)),
                                        ft.Text("€ 19336.27", style=ft.TextStyle(size=16, italic=True, color=ft.colors.BLACK)),
                                    ],
                                    horizontal_alignment="center", alignment = "center",
                                ),                                  
                            ),                                                
                        ],
                        alignment = ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    ft.Container(height=5),                    
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text(f"IBAN\n{self.iban_number}", style=ft.TextStyle(size=16, italic=True, color=ft.colors.BLACK)),
                                        ft.ElevatedButton("COPY", 
                                            bgcolor=ft.colors.GREEN_900,
                                            color=ft.colors.WHITE,
                                            tooltip="Copy to clipboard",
                                            on_click=self.copy_to_clipboard,
                                        ),
                                    ],
                                    alignment = ft.MainAxisAlignment.SPACE_EVENLY,
                                ),
                                bgcolor=ft.colors.WHITE,
                                padding=ft.Padding(top=10, bottom=10, left=20, right=20),
                                width=.8*self.parent_page.window_width,
                                border_radius=ft.BorderRadius(top_left=50, top_right=50, bottom_left=50, bottom_right=50),
                            ),
                        ],
                        alignment = ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                height = self.parent_page.window_height * 0.6,
                                width = self.parent_page.window_width * 0.8,
                                border_radius = ft.BorderRadius(top_left=20, top_right=20, bottom_left=20, bottom_right=20),
                                bgcolor = ft.colors.WHITE,
                                content = self.movements_content,
                            ),
                        ], 
                        alignment = "center",
                    ),
                ]
            ),
        )
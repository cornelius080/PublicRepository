import flet as ft

class Home(ft.View):
    def __init__(self, parent_page, route, go_to_view_message_box, go_to_view_faq, go_to_view_cards, go_to_view_other, go_to_view_movements):
        super().__init__()  
        self.parent_page = parent_page
        self.padding = 0
        self.vertical_alignment = "bottom"
        self.parent_page = parent_page
        self.route = route 
        self.go_to_view_message_box = go_to_view_message_box     
        self.go_to_view_faq = go_to_view_faq
        self.go_to_view_cards = go_to_view_cards  
        self.go_to_view_other = go_to_view_other
        self.go_to_view_movements = go_to_view_movements

    def build_ext_card_content(self):
        self.lv = ft.ListView(
            spacing=20, 
            padding=ft.Padding(top=30, bottom=30, left=20, right=20), 
            auto_scroll=False,
        )

        for i in range(0, 4):
            leadingIcon=ft.Icon(ft.icons.CREDIT_CARD_OUTLINED)
            if i==0:
                leadingIcon=ft.Icon(ft.icons.ACCOUNT_BALANCE)
                title = "Bank Account"
                subtitle = "1111-1111-1111-1111"
                color = None
            elif i==1:
                title = "Debit Card"
                subtitle = "2222-2222-2222-2222"
                color = ft.colors.WHITE
            elif i==2:
                title = "Credit Card"
                subtitle = "3333-3333-3333-3333"
                color = None
            else:
                leadingIcon=ft.Icon(ft.icons.EURO)
                title = "Loan"
                subtitle = "4444-4444-4444-4444"
                color = ft.colors.WHITE
            self.lv.controls.append(
                ft.Card(
                    color=ft.colors.SECONDARY_CONTAINER,
                    height=120,
                    elevation=50,
                    content=ft.Column(
                        controls=[
                            ft.ListTile(
                                leading=leadingIcon,
                                title=ft.Text(title),
                                subtitle=ft.Text(subtitle),
                                trailing=ft.IconButton(
                                    icon=ft.icons.KEYBOARD_ARROW_RIGHT,  
                                    on_click=self.go_to_view_movements,  
                                    data=i,                           
                                ),
                            ),                            
                        ],
                        alignment="center",
                    )                   
                )
            )

        return self.lv

    def build(self):
        self.appbar = self.parent_page.appbar
        self.appbar.leading = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.MAIL, 
                    icon_size=30, 
                    icon_color=ft.colors.WHITE,
                    on_click=self.go_to_view_message_box,
                )
            ]
        )
        self.appbar.actions = [
            ft.IconButton(
                icon=ft.icons.LOCAL_PHONE, 
                icon_size=30, 
                icon_color=ft.colors.WHITE, 
                on_click=self.go_to_view_faq,
            ),
        ]

        self.navigation_bar = self.parent_page.navigation_bar
        self.navigation_bar.selected_index = 0

        extCard = ft.Card(
            color=ft.colors.PRIMARY,
            width=350,
            height=447,
            elevation = 10,
            content = self.build_ext_card_content(),
        )

        return ft.Container(
            width=self.parent_page.window_width,
            padding=ft.padding.only(top=10, left=20, right=20, bottom=15),
            content=extCard,
        )
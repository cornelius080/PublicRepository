import flet as ft

class Other(ft.View):
    def __init__(self, parent_page: ft.Page, exit_from_app, go_to_view_home, go_to_view_cards, go_to_view_message_box):
        super().__init__()
        self.parent_page = parent_page
        self.exit_from_app = exit_from_app
        self.go_to_view_home = go_to_view_home
        self.go_to_view_cards = go_to_view_cards
        self.go_to_view_message_box = go_to_view_message_box
        self.scroll=ft.ScrollMode.AUTO

    def show_bs(self, e):
        self.bs.open = True
        self.bs.update()

    def close_bs(self, e):
        self.bs.open = False
        self.bs.update()

    def augmented_row_on_click(self, e):
        self.snackbar.content = ft.Text(f"{e.control.content.value} VIEW - NOT IMPLEMENTED YET")
        self.snackbar.open = True        
        self.snackbar.update()        

    def build_augmented_row(self, icon, text_value: str):
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(icon),
                        ft.Container(content = ft.Text(text_value), 
                                     on_click=self.augmented_row_on_click),
                    ]
                ),     
                ft.Divider(),    
            ],
            tight=True,
        )

    def build_category_column(self, category_name: str, category_items: list):
        col = ft.Column(
            tight=True,
            horizontal_alignment="left",
            controls=[
                ft.Text(category_name, theme_style="LABEL_SMALL", italic=True, 
                        color=ft.colors.GREY_900,
                ),
            ],
        )
        
        for item in category_items:
            col.controls.append(
                self.build_augmented_row(item[0], item[1])
            )
        
        return col

    def build(self):
        self.snackbar = ft.SnackBar(
            content=ft.Text(""),
            duration=1000,
        )
        self.parent_page.overlay.append(self.snackbar)

        self.appbar = self.parent_page.appbar
        self.appbar.leading = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.MAIL, icon_size=30, icon_color=ft.colors.WHITE,
                    on_click=self.go_to_view_message_box,
                )
            ]
        )
        self.appbar.actions = [
            ft.IconButton(
                icon=ft.icons.POWER_SETTINGS_NEW, icon_size=30, icon_color=ft.colors.WHITE,
                on_click = self.show_bs
            ),
        ]

        self.bs = ft.BottomSheet(
            content=ft.Container(
                padding=50,
                content=ft.Column(
                    tight=True,
                    controls=[
                        ft.Text("Are you sure you want to close the app?"),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="No", 
                                    on_click = self.close_bs
                                ),
                                ft.ElevatedButton(
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,  #text color
                                        bgcolor=ft.colors.PRIMARY,  #background color
                                    ),
                                    text="Yes", 
                                    on_click = self.exit_from_app
                                ),
                            ], 
                            alignment = "center"
                        ),                
                    ],
                ),
            ),
        )
        self.parent_page.overlay.append(self.bs)

        col_general = self.build_category_column("General", 
                                         [
                                             [ft.icons.PERSON, "PROFILE"], 
                                             [ft.icons.EVENT_NOTE, "MEMO"], 
                                             [ft.icons.FOLDER_OPEN, "DOC"],
                                             [ft.icons.CONTACT_PAGE, "RUBRIC"],
                                             [ft.icons.CHECKLIST_RTL, "PERMISSIONS"],
                                         ]                                          
        )
        col_banking = self.build_category_column("Banking services", 
                                         [
                                             [ft.icons.ACCOUNT_BALANCE, "OTHER BANKS"], 
                                             [ft.icons.PIE_CHART, "BUDGET"], 
                                             [ft.icons.SHOPPING_CART, "BUYING"],
                                             [ft.icons.BORDER_COLOR, "REMOTE SIGNATURE"],
                                             [ft.icons.WORK, "INVESTMENTS"],
                                             [ft.icons.TOKEN, "MOBILE TOKEN"],
                                         ]                                          
        )
        col_products = self.build_category_column("Products", 
                                         [
                                             [ft.icons.BEACH_ACCESS, "POLICIES"], 
                                             [ft.icons.SSID_CHART, "TRADING"], 
                                             [ft.icons.EURO, "LOAN"],
                                             [ft.icons.REAL_ESTATE_AGENT, "PROPERTY MORTGAGE"],
                                             [ft.icons.CREDIT_CARD, "CREDIT CARD"],
                                         ]                                          
        )
        col_contacts = self.build_category_column("Contacts", 
                                         [
                                             [ft.icons.SUPPORT_AGENT, "PERSONAL OPERATOR"], 
                                             [ft.icons.LOCAL_PHONE, "CONTACT US"], 
                                             [ft.icons.LOCATION_ON, "FIND US"],
                                         ]                                          
        )
        col_settings = self.build_category_column("Settings", 
                                         [
                                             [ft.icons.KEY, "PIN"], 
                                             [ft.icons.NOTIFICATIONS, "PUSH NOTIFICATIONS"], 
                                             [ft.icons.DESCRIPTION, "ONLINE DOCUMENTS"],
                                             [ft.icons.PRIVACY_TIP, "PRIVACY"],
                                             [ft.icons.INFO, "GENERAL CONDITIONS"],
                                         ]                                          
        )

        return ft.Container(          
            content=ft.Column(
                controls=[
                    col_general,
                    col_banking,
                    col_products,
                    col_contacts,
                    col_settings,
                ],
                tight=True,
                horizontal_alignment="left",
                spacing=30,
            ),
        )
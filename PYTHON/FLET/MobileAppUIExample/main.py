import flet as ft
from views_handler import views_manager, nav_bar_on_change

def main(page: ft.Page):    
    def route_change(route):        
        page.views.clear()
        page.views.append(
            # returns a dictionary of views with keys corresponding to their routes
            views_manager(page)[page.route]
        )        
        page.update()
    
    page.appbar = ft.AppBar( 
        title = ft.Column(
            [
                ft.CircleAvatar(
                    content=ft.Text("JS"),
                    radius=30,
                ),
                ft.Text(
                    "John Smith", 
                    style=ft.TextStyle(
                        size=20,
                        italic=True, 
                        color=ft.colors.WHITE,
                    )
                ),
            ],
            spacing=0,
            #alignment="center",
            horizontal_alignment="center",
        ),
        center_title = True,
        toolbar_height = 0.17 * page.window_height,
        bgcolor = ft.colors.PRIMARY,
        # leading_width=150,
        # leading=ft.Row(
        #     controls=self.leading_controls
        # ),            
        # actions=self.actions_controls,
    )

    page.navigation_bar = ft.NavigationBar(       
        elevation=20, 
        indicator_color=ft.colors.WHITE,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Home",),    
            ft.NavigationDestination(icon=ft.icons.LIST, label="Other",),
        ],
        on_change=lambda e: nav_bar_on_change(page, e),
    )


    page.theme = ft.Theme(color_scheme_seed = ft.colors.GREEN) #BLUE_200
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window_height = 700
    page.window_width = 400
    page.window_left = 990
    page.window_resizable = False
    page.window_maximizable = False
    page.title = "Mobile App UI Example"

    page.on_route_change = route_change
    page.go("/")    

ft.app(target=main, assets_dir="assets")

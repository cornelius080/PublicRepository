import flet as ft
import time

class Welcome(ft.View):
    def __init__(self, parent_page, route, on_click):
        super().__init__()  
        self.padding = 0
        self.parent_page = parent_page
        self.route = route
        self.login_on_click = on_click    
        self.updating = None    
                

    def update_layout(self):
        """
        Updates the layout by incrementally changing the progress bar value and updating the background color of the 
        top container and the login button every 10% of progress.

        This function iterates from 0 to 100, updating the progress bar's value and sleeping for 0.05 seconds 
        between each increment. When the progress reaches a multiple of 10, it changes the background color of 
        the top container and the login button based on a predefined list of green shades. After reaching 100%, 
        it resets the progress.
        """
        colors = [ft.colors.GREEN_50, ft.colors.GREEN_100, ft.colors.GREEN_200, ft.colors.GREEN_300, ft.colors.GREEN_400, ft.colors.GREEN_500, ft.colors.GREEN_600, ft.colors.GREEN_700, ft.colors.GREEN_800, ft.colors.GREEN_900]

        val=0
        while val < 101:
            if not self.updating:
                break
            else:
            #if self.pb in self.controls:    
                self.pb.value = val * 0.01
                #update container bgcolor every 10%
                mod = val % 10
                if mod == 0.0:
                    self.topContainer.bgcolor = colors[int(val/10) - 1]
                    self.loginButton.style = ft.ButtonStyle(bgcolor=colors[int(val/10) - 1])
                #update val value
                val += 1
                if val == 100:
                    val=0
                #update the page
                self.update()
                time.sleep(0.05)

    def did_mount(self):
        self.updating = True
        self.update_layout()

    def will_unmount(self):
        self.updating = False

    def build(self):
        self.topContainer = ft.Container(
            bgcolor=ft.colors.GREEN, 
            width=self.parent_page.window_width,
            height=self.parent_page.window_height * 0.25,
        )
        self.pb = ft.ProgressBar()
        self.loginButton=ft.FilledButton(text="LOGIN", on_click = self.login_on_click)

        return ft.Column(
            controls=[
                self.topContainer, 
                self.pb, 
                ft.Row(
                    [
                        ft.Container(
                            content=self.loginButton,
                            padding=ft.padding.only(top=120),
                        )
                    ], 
                    alignment="center",
                    vertical_alignment="end",
                )
            ], 
            spacing=0,
        )
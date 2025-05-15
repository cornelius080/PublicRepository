import flet as ft
from create_new_db_UI import Create_New_Db_UI
from view_db_UI import View_Db_UI


def main(page: ft.Page):
    def show_bottom_sheet(e):
        bottom_sheet.open = True
        bottom_sheet.update()

    def close_bottom_sheet(e):
        bottom_sheet.open = False
        bottom_sheet.update()

    def new_database_on_click(e):
        page_content.controls=[Create_New_Db_UI()]
        page.update()
    
    def view_database_on_click(e):
        global selected_file
        page_content.controls=[View_Db_UI(selected_file)]
        page.update()

    def pick_files_result(e: ft.FilePickerResultEvent):
        global selected_file
        if e.files:
            page_content.controls = [
                ft.Container(height=10),
                ft.TextField(
                    label = "Selected File",
                    value = "\\\\".join(map(lambda f: f.path, e.files)),
                    read_only = True,
                    height=40,
                    border_color = ft.colors.BLUE_500,
                ),
            ]
            page_content.update()
            selected_file = "\\\\".join(map(lambda f: f.path, e.files))


    bottom_sheet = ft.BottomSheet(
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
                                    on_click = close_bottom_sheet
                                ),
                                ft.ElevatedButton(
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,  #text color
                                        bgcolor=ft.colors.PRIMARY,  #background color
                                    ),
                                    text="Yes", 
                                    on_click = lambda _: page.window_destroy(),
                                ),
                            ], 
                            alignment = "center"
                        ),                
                    ],
                ),
            ),
        )
    page.overlay.extend([bottom_sheet])
    
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)

    menubar = ft.MenuBar(
        expand=True,
        style=ft.MenuStyle(
            alignment=ft.alignment.top_left,
            bgcolor=ft.colors.BLUE,
        ),
        controls=[
            ft.SubmenuButton(
                menu_style=ft.MenuStyle(bgcolor=ft.colors.BLUE_50,),
                content=ft.Text("File",),
                controls=[
                    ft.SubmenuButton(
                        menu_style=ft.MenuStyle(bgcolor=ft.colors.BLUE_50,),
                        leading=ft.Icon(ft.icons.ARCHIVE),
                        content=ft.Text("Database",),
                        controls=[
                            ft.MenuItemButton(
                                        content=ft.Text("New"),
                                        leading=ft.Icon(ft.icons.NOTE_ADD),
                                        on_click=new_database_on_click,
                            ),
                            ft.MenuItemButton(
                                        content=ft.Text("Open"),
                                        leading=ft.Icon(ft.icons.FILE_OPEN),
                                        on_click=lambda _: pick_files_dialog.pick_files(dialog_title="Select a database file"),
                            ),
                        ],
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Quit", ),
                        leading=ft.Icon(ft.icons.EXIT_TO_APP),
                        on_click=show_bottom_sheet,
                    ),
                ],
            ),
            ft.SubmenuButton(
                content = ft.MenuItemButton(
                        content=ft.Text("View", ),
                        leading=ft.Icon(ft.icons.SEARCH, color = ft.colors.BLACK),
                        on_click=view_database_on_click,
                ),
            ),
        ],
    )

    
    page.title = "Sqlite3 CRUD"
    page.scroll = ft.ScrollMode.AUTO
    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE)
    page.theme_mode = ft.ThemeMode.LIGHT       
    page_content= ft.Column([], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    page.add(
        ft.Column(
            [
                ft.Row([menubar]),
                page_content,
                pick_files_dialog,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )        
    )

    global selected_file
    selected_file = None

ft.app(target=main, assets_dir="\assets")

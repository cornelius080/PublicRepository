import flet as ft

def main(page: ft.Page):
    def CalculateAspectRatio(aspectRatio: str):
        index = aspectRatio.find(":")
        num = int(aspectRatio[ : index])
        den = int(aspectRatio[index+1 : ])
        return num / den

    def pick_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            global video_list

            videoFullname = ", ".join(map(lambda f: f.path, e.files))
            videoFullname = videoFullname.split(", ")

            video_list = []
            for video in videoFullname:
                video_list.append(ft.VideoMedia(video))

    def Show_Settings():
        cont.content = settingsContainer
        page.update()

    def On_Change_Navigation_Rail(e):
        if e.control.selected_index == 0:
            global video_list

            if len(video_list) > 0:
                cont.content=ft.Video(
                    expand = True,
                    playlist = video_list,
                    aspect_ratio = CalculateAspectRatio(settings["aspect ratio"]),
                    filter_quality = settings["filter quality"],
                    autoplay = settings["autoplay"],
                    muted = settings["muted"],
                )
            else:
                cont.content = None

            page.update()
        if e.control.selected_index == 1:
            Show_Settings()
        if e.control.selected_index == 2:
            cont.content = None
            e.control.selected_index = None
            page.update()

    def On_Change_Switch_Autoplay(e):
        settings["autoplay"] = e.control.value

    def On_Change_Switch_Muted(e):
        settings["muted"] = e.control.value

    def On_Change_Radio_FilterQuality(e):
        settings["filter quality"] = e.control.value

    def On_Change_Dropdown_AspectRatio(e):
        settings["aspect ratio"] = e.control.value

   
    switch_autoplay = ft.Switch(
        label="AUTOPLAY", label_position=ft.LabelPosition.LEFT, label_style = ft.TextStyle(size=18, italic=True), value=False, on_change=On_Change_Switch_Autoplay,
    )
    switch_muted = ft.Switch(
        label="MUTED", label_position=ft.LabelPosition.LEFT, label_style = ft.TextStyle(size=18, italic=True), value=False, on_change=On_Change_Switch_Muted,
    )
    rg_filterQuality = ft.RadioGroup(on_change=On_Change_Radio_FilterQuality, content=ft.Row([
                                            ft.Text("FILTER QUALITY", italic=True, size=18),
                                            ft.Radio(value="low", label="Low"),
                                            ft.Radio(value="medium", label="Medium"),
                                            ft.Radio(value="high", label="High")
                                            ]
                        )
    )
    rg_filterQuality.value = "medium"
    dd_aspectRatio = ft.Dropdown(
        on_change = On_Change_Dropdown_AspectRatio,
        width=100,
        options=[
            ft.dropdown.Option("16:9"),
            ft.dropdown.Option("21:9"),
            ft.dropdown.Option("4:3"),
            ft.dropdown.Option("9:16"),
            ft.dropdown.Option("1:1"),
        ],
    )
    dd_aspectRatio.value = "16:9"
    
    settingsContainer = ft.Container(content=ft.Column(
        [switch_autoplay, switch_muted, rg_filterQuality, 
        ft.Row([ft.Text("ASPECT RATIO", italic=True, size=18), dd_aspectRatio]), ft.Row([ft.Text("", size=18)]), 
        ], 
        horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )
    )
    
    pick_file_dialog = ft.FilePicker(on_result=pick_file_result)
    page.overlay.extend([pick_file_dialog])
    rail = ft.NavigationRail(
        #selected_index=0,
        #extended=True,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.icons.VIDEO_FILE, text="Open Video File", tooltip = "Select video file", on_click=lambda _: pick_file_dialog.pick_files(allow_multiple=True, 
            allowed_extensions=["mp4", "avi", "mpeg", "mov", "wmv", "mkv", "flv", "f4v", "3gp", "WebM"],
            )
        ),
        label_type=ft.NavigationRailLabelType.ALL,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.VIDEO_LIBRARY_OUTLINED,
                selected_icon=ft.Icon(ft.icons.VIDEO_LIBRARY),
                label_content=ft.Text("Player"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.VIDEO_SETTINGS_OUTLINED,
                selected_icon=ft.Icon(ft.icons.VIDEO_SETTINGS),
                label_content=ft.Text("Settings"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.CANCEL_PRESENTATION_OUTLINED,
                selected_icon=ft.Icon(ft.icons.CANCEL_PRESENTATION),
                label_content=ft.Text("Clear All"),
            ),
        ],
        on_change=On_Change_Navigation_Rail,
    )

    cont = ft.Container(margin=50, padding=20, expand = True,
        #border=ft.border.all(3, ft.colors.RED),
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                cont,
            ],
            expand=True,
        )
    )

    page.window_maximized = True
    #page.scroll = ft.ScrollMode.AUTO
    page.title = "VIDEO PLAYER"
    page.update()


    global video_list
    video_list = []

    settings = {"autoplay": switch_autoplay.value, "muted": switch_muted.value, 
                "filter quality": rg_filterQuality.value, "aspect ratio": dd_aspectRatio.value
    }    

ft.app(target=main, assets_dir="assets")


import flet as ft

def main(page: ft.Page):
    def route_change(route):        
        page.views.clear()
        page.views.append(top_view)

        if page.route == "/video":
            page.views.append(video_view)

        page.update()


    def view_pop(view):     
        if page.route == "/video":
            page.go("/")

    
    def Add_New_Item(e):
        # THE NEW ITEM CONSISTS OF A LIST TILE: EACH LIST TILE IS CONSTITUTED BY A LEADING CHECKBOX, A TITLE, A SUBTITLE AND A TRAILING ICON BUTTON TO ELIMINATE THE ITEM

        global addedItemsCount        
        videoNameExist = False

        items = ft.ListTile(
                leading=ft.Checkbox(value=False,),
                trailing = ft.IconButton(icon= ft.icons.DELETE, tooltip="DELETE ITEM", 
                    on_click=On_Click_Delete_Item,)
        )

        if len(videoNameTextField.value) > 0:
            if len(urlTextField.value) > 0:                
                for control in itemsCollection.controls:
                    if control.title.value == videoNameTextField.value:
                        page.snack_bar = ft.SnackBar(ft.Text("VIDEO NAME ALREADY EXISTS! PLEASE CHANGE IT!"))
                        page.snack_bar.open = True
                        page.update()
                        videoNameExist = True
                        break
                if videoNameExist == False:     
                    items.trailing.data = addedItemsCount
                    items.title = ft.Text(videoNameTextField.value)
                    items.subtitle = ft.Text(urlTextField.value)
                    itemsCollection.controls.append(items)
                    addedItemsCount += 1

                    #print("NEW ITEM ADDED WITH DATA: ", items.trailing.data)
            else:
                page.snack_bar = ft.SnackBar(ft.Text("PLEASE ADD VIDEO URL!"))
                page.snack_bar.open = True
                page.update()
        else:
            if len(urlTextField.value) > 0:
                items.trailing.data = addedItemsCount
                items.title = ft.Text("")
                items.subtitle = ft.Text(urlTextField.value)
                itemsCollection.controls.append(items)
                addedItemsCount += 1

        urlTextField.value = ""
        videoNameTextField.value = ""
        page.close_dialog()
        page.update()


    def On_Click_Close_Dialog(e):
        urlTextField.value = ""
        videoNameTextField.value = ""
        page.close_dialog()


    def On_Click_Open_Dialog(e):
        dlg_modal = ft.AlertDialog(
            modal=True,
            title = urlTextField,
            content = videoNameTextField,
            actions=[
                ft.TextButton("CLOSE", on_click = On_Click_Close_Dialog),
                ft.TextButton("ADD", on_click = Add_New_Item),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()
        

    def On_Click_Delete_Item(e):
        selected_index = None
        count = 0
        for control in itemsCollection.controls:
            if control.trailing.data == e.control.data:
                selected_index = count
                break
            count += 1

        removed = itemsCollection.controls.pop(selected_index)

        # ONLY FOR DEBUG PURPOSES
        # print("SELECTED INDEX IS: ", selected_index)
        # print("DATA IS: ", e.control.data)
        # print("DELETED ITEM IS: ", removed.title)
        # print("NEW LIST OF ITEMS")
        # for control in itemsCollection.controls:
        #     print(control.title)
        # print("\n\n")

        page.snack_bar = ft.SnackBar(ft.Text("DELETED ITEM!"), duration=3000)
        page.snack_bar.open = True
        page.update()


    def On_Click_Select_All(e):
        if e.control.data: #CASE: DESELECT ALL
            if len(itemsCollection.controls)>0:
                e.control.icon = ft.icons.SELECT_ALL
                e.control.tooltip = "SELECT ALL"
                e.control.data = False

                # DEACTIVATE ALL CHECKBOXES
                for control in itemsCollection.controls:
                    control.leading.value = False
        else: #CASE: SELECT ALL
            if len(itemsCollection.controls)>0:
                e.control.icon = ft.icons.DESELECT
                e.control.tooltip = "DESELECT ALL"
                e.control.data = True

                # ACTIVATE ALL CHECKBOXES
                for control in itemsCollection.controls:
                    control.leading.value = True
        page.update()


    def On_Click_Play(e):
        selected_items = []
        video_list = []
        for control in itemsCollection.controls:
            if control.leading.value == True:
                selected_items.append({"name":control.title.value, "url":control.subtitle.value})
                video_list.append(ft.VideoMedia(control.subtitle.value))
        
        if len(selected_items)==0:
            page.snack_bar = ft.SnackBar(ft.Text("PLEASE SELECT AT LEAST ONE ITEM!"), duration=3000)
            page.snack_bar.open = True
            page.update()
        else:            
            video_container.content =ft.Video(
                    expand = True,
                    playlist = video_list,
                    aspect_ratio = 16/9,
                    filter_quality = ft.FilterQuality.HIGH,
                    autoplay = False,
                    muted = False,
            )
            
            page.go("/video")    


    ###############
    ###############
    # TOP VIEW
    ###############
    ###############
    urlTextField = ft.TextField(label="URL", prefix_icon=ft.icons.HTTP)
    videoNameTextField = ft.TextField(label="Video Name", prefix_icon=ft.icons.ONDEMAND_VIDEO)

    addButton = ft.IconButton(icon=ft.icons.ADD, tooltip="ADD NEW VIDEO", on_click = On_Click_Open_Dialog)
    selectAllButton = ft.IconButton(icon= ft.icons.SELECT_ALL, tooltip="SELECT ALL", on_click=On_Click_Select_All, data=False)

    itemsCollection = ft.ListView(expand=1, spacing=1, padding=20, auto_scroll=False)
    card = ft.Card(height = 400, content= itemsCollection, expand=True,)

    playButton = ft.ElevatedButton(icon=ft.icons.PLAY_CIRCLE, text="PLAY SELECTED VIDEO", 
        on_click=On_Click_Play)

    row1 = ft.Row(
        [addButton, selectAllButton,],
        #expand=True,
        alignment=ft.MainAxisAlignment.END,
    )
    row2 = ft.Row(
        [card],
        #expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
    )
    row3 = ft.Row(
        [playButton],
        #expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    top_view = ft.View("/", controls=[ft.Column([row1, row2, row3])],)


    ###############
    ###############
    # VIDEO VIEW
    ###############
    ###############
    video_container = ft.Container(margin=10, padding=20, expand = True, width=1000,
        #border=ft.border.all(3, ft.colors.RED), 
    )

    playedVideoUrl = ft.TextField(label="URL", prefix_icon=ft.icons.HTTP, width=1000)
    playedVideoName = ft.TextField(label="Video Name", prefix_icon=ft.icons.ONDEMAND_VIDEO, width=1000)

    video_view = ft.View("/video", 
        controls=[ft.Column(
                            [video_container, playedVideoName, playedVideoUrl], 
                            expand=True, horizontal_alignment = ft.CrossAxisAlignment.CENTER
                    ),
        ],
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
    )
    video_view.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ARROW_BACK, 
        on_click=lambda _: page.go("/"), tooltip = "BACK TO MAIN PAGE")
    

    ###############
    ###############
    # PAGE
    ###############
    ###############
    page.window_maximized = True
    page.scroll = ft.ScrollMode.AUTO
    page.title = "WEB VIDEO PLAYER"
    page.theme = ft.Theme(color_scheme_seed = ft.colors.BLUE_200)
    page.theme_mode = "system" #system, light, dark
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


    ###############
    ###############
    # VARIABLES
    ###############
    ###############
    global addedItemsCount
    addedItemsCount = 0

ft.app(target=main, assets_dir="assets")

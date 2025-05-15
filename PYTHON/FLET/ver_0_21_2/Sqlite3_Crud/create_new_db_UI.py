import flet as ft
from database_manager import DbManager

#class Create_New_Db_UI(ft.UserControl):
class Create_New_Db_UI(ft.Control):
    def __init__(self,):
        """
        Constructor for the Create_New_Db_UI class.

        Initializes the UI control and sets the database manager.
        """
        super().__init__()
        self.db_manager = DbManager()

    def check_specifications(self):
        """
        Checks if all the required specifications have been defined before creating a new database.

        It checks the database name, table names and field names and data types.

        If any of the required specifications are not defined, it returns False and updates the snackbar with the appropriate error message.

        If all the required specifications are defined, it returns True.

        :return: True if all the required specifications are defined, False otherwise.
        """
        if self.tf_db_name.value == "": # database name
            self.snackbar.content = ft.Text(f"Database Name not defined!", color=ft.Colors.RED)
            self.snackbar.open = True        
            self.snackbar.update()
            return False
        for i, tab in enumerate(self.table_tabs.tabs): # table name
            if tab.content.controls[1].controls[0].value == "": 
                self.snackbar.content = ft.Text(f"Table {i+1} Name not defined!", color=ft.Colors.RED)
                self.snackbar.open = True        
                self.snackbar.update()
                return False
            list_view = tab.content.controls[2].content
            for j, container in enumerate(list_view.controls):
                col = container.content
                if col.controls[1].controls[0].value == "": 
                    self.snackbar.content = ft.Text(f"Table {i+1} - Field {j+1} Name not defined!", color=ft.Colors.RED)
                    self.snackbar.open = True        
                    self.snackbar.update()
                    return False
                if col.controls[1].controls[1].value == None: 
                    self.snackbar.content = ft.Text(f"Table {i+1} - Field {j+1} DataType not defined!", color=ft.Colors.RED)
                    self.snackbar.open = True        
                    self.snackbar.update()
                    return False
        return True

    def create_database(self, e):
        """
        Handles the click event of the "Create Database" button.

        Checks if all the required specifications have been defined before creating a new database.

        If all the required specifications are defined, it creates a new database with the given specifications.

        :param e: The event object associated with the button click.
        """
        if self.check_specifications():
            database_param = {
                "url": self.tf_db_name.value,
                "tables": [],
            }
            # iteration across tables
            for i, tab in enumerate(self.table_tabs.tabs):
                table_param = {
                    "name": tab.content.controls[1].controls[0].value,
                    "fields": [],
                }
                # iteration across fields
                list_view = tab.content.controls[2].content
                for j, container in enumerate(list_view.controls):
                    col = container.content
                    table_param["fields"].append( 
                        {
                            "name": col.controls[1].controls[0].value,
                            "data_type": col.controls[1].controls[1].value,
                            "nullable": col.controls[2].controls[0].value,
                            "unique": col.controls[2].controls[1].value,
                            "primary_key": col.controls[2].controls[2].value,
                        }
                    )
                    ################################
                    # ONLY FOR DEBUG PURPOSES
                    ################################
                    # print(f"Unique:  {col.controls[2].controls[1].value}")
                    ################################
                database_param["tables"].append(table_param)

            self.db_manager.create_database(database_param["url"], database_param["tables"])


    def give_info_about_db_datatypes(self, e):
        """
        Handles the change event of the datatype dropdown.

        Updates the tooltip of the datatype dropdown with the docstring of the selected datatype.

        :param e: The event object associated with the dropdown change.
        """
        e.control.tooltip = f"{self.db_manager.get_datatype_docstring(e.control.value)}"
        self.update()

    def switch_field_attributes_on_change(self, e):
        """
        Handles the change event of the field attributes switches.

        When a field attribute switch is changed, it updates the other switches according to the rules of a database.

        For example, if the primary key switch is turned on, all other switches (nullable, unique) are turned off.

        :param e: The event object associated with the switch change.
        """
        tab_index = e.control.data[0]
        field_index = e.control.data[1]
        
        current_tab = self.table_tabs.tabs[tab_index]
        list_view = current_tab.content.controls[2].content
        current_field = list_view.controls[field_index].content

        switch_nullable = current_field.controls[2].controls[0]
        switch_unique = current_field.controls[2].controls[1]
        switch_primary_key = current_field.controls[2].controls[2]

        if e.control.label == "Nullable" and e.control.value == True:
            switch_unique.value = False
            switch_unique.update()
            switch_primary_key.value = False
            switch_primary_key.update()
        if e.control.label == "Unique" and e.control.value == True:
            switch_nullable.value = False
            switch_nullable.update()
            switch_primary_key.value = False
            switch_primary_key.update()
        if e.control.label == "Primary Key" and e.control.value == True:    
            switch_nullable.value = False
            switch_nullable.update()
            switch_unique.value = False
            switch_unique.update()        

    def design_tables_specs_layout(self, e, i):
        """
        Handles the change event of the "Number of fields" slider of the Table Specification tab.

        Updates the content of the "Table Specification" tab with the given number of fields. The fields are represented as a list of "Field Name" and "Data Type" textfields, and three switches: "Nullable", "Unique", and "Primary Key".

        :param e: The event object associated with the slider change.
        :param i: The index of the current table in the "Tables" tab.
        """
        self.button_create_db.visible = False
        
        current_tab = self.table_tabs.tabs[i] 
        list_view = current_tab.content.controls[2].content
        list_view.controls.clear()
        for j in range(int(e.control.value)):
            list_view.controls.append(  
                ft.Container(
                    border=ft.border.all(1, ft.Colors.BLUE_500),
                    border_radius=10,
                    margin=0,
                    padding=20,
                    content=ft.Column(
                        [
                            ft.Text(f"Field {j+1}", italic = True, size=16, weight=ft.FontWeight.BOLD),
                            ft.Row(
                                [
                                    ft.TextField(label="Field Name", expand=True, height=40,border_color = ft.Colors.BLUE_500, tooltip="Name of the column"),
                                    ft.Dropdown(
                                        border_color = ft.Colors.BLUE_500,
                                        content_padding = 8,
                                        width= 150,
                                        height=40,
                                        label="Data Type",
                                        tooltip="Data type of the column",
                                        options=[
                                            ft.dropdown.Option(type) for type in self.db_manager.get_generic_camel_case_types()
                                        ],
                                        on_change=self.give_info_about_db_datatypes,
                                    ),
                                ],
                            ),
                            ft.Row(
                                [
                                    ft.Switch(
                                        label="Nullable", label_style=ft.TextStyle(size=16), data=[i,j],
                                        tooltip="If TRUE, the column can contain NULL values, i.e. absent or unknown. It is not mandatory to provide a value for that column.",
                                        track_color={
                                            ft.MaterialState.DEFAULT: ft.Colors.BLUE_50,
                                            ft.MaterialState.SELECTED: ft.Colors.BLUE_500,
                                        },
                                        thumb_color={
                                            ft.MaterialState.DEFAULT: ft.Colors.BLUE_500,
                                            ft.MaterialState.SELECTED: ft.Colors.BLUE_50,
                                        },
                                        value=True,
                                        on_change=self.switch_field_attributes_on_change,
                                    ), 
                                    ft.Switch(
                                        label="Unique", label_style=ft.TextStyle(size=16), data=[i,j],
                                        tooltip="If TRUE, the column values are unique, that is, no duplicates are allowed (e.g., phone numbers or emails); if TRUE can contain ONLY ONE NULL value. NULL and PRIMARY_KEY are switched to FALSE.",
                                        track_color={
                                            ft.MaterialState.DEFAULT: ft.Colors.BLUE_50,
                                            ft.MaterialState.SELECTED: ft.Colors.BLUE_500,
                                        },
                                        thumb_color={
                                            ft.MaterialState.DEFAULT: ft.Colors.BLUE_500,
                                            ft.MaterialState.SELECTED: ft.Colors.BLUE_50,
                                        },
                                        on_change=self.switch_field_attributes_on_change,
                                    ), 
                                    ft.Switch(
                                        label="Primary Key", label_style=ft.TextStyle(size=16), data=[i,j],
                                        tooltip = "If TRUE, the column values must be unique and not NULL (e.g., a progressive integer);  if PRIMARY_KEY is set to TRUE, NULL and UNIQUE are switched to FALSE, considering that a UNIQUE column admits even a single NULL value.",
                                        track_color={
                                            ft.MaterialState.DEFAULT: ft.Colors.BLUE_50,
                                            ft.MaterialState.SELECTED: ft.Colors.BLUE_500,
                                        },
                                        thumb_color={
                                            ft.MaterialState.DEFAULT: ft.Colors.BLUE_500,
                                            ft.MaterialState.SELECTED: ft.Colors.BLUE_50,
                                        },
                                        on_change=self.switch_field_attributes_on_change,
                                    ),
                                ],
                            ),
                        ],
                    ),
                )                   
            
            
            
            )
            
        self.button_create_db.visible = True
        self.update()

    def design_tabs_layout(self, e):
        """
        Handles the change event of the "Number of Tables" slider of the Database Specification tab.

        Updates the content of the "Database Specification" tab with the given number of tables. The tables are represented as a list of tabs, each containing a "Table Name" textfield and a "Number of Fields" textfield, and a list view representing the fields of the table.

        :param e: The event object associated with the slider change.
        """
        self.table_tabs.tabs.clear()
        for i in range(int(e.control.value)):
            self.table_tabs.tabs.append(
                ft.Tab(
                    icon= ft.Icons.TABLE_VIEW, text=f"Table {i+1}", 
                    content = ft.Column(
                        spacing=5,
                        controls=[
                            ft.Container(height=1),
                            ft.Row(
                                [
                                    ft.TextField(label="Table Name", expand=True, height=40, border_color = ft.Colors.BLUE_500),
                                    ft.TextField(label="Number of Fields", width=150, height=40, border_color=ft.Colors.BLUE_500, keyboard_type=ft.KeyboardType.NUMBER, on_submit=lambda e, i=i: self.design_tables_specs_layout(e,i),),              
                                ],
                            ),
                            ft.Container(
                                margin=0,
                                padding=ft.Padding(0, 8, 158, 5),
                                height = 420,
                                content=ft.ListView(
                                    spacing=10,
                                    controls=[],
                                )
                            ),
                        ],
                    ),
                ),
            )
        self.update()

    def save_file_result(self, e):
        """
        Handles the result of the file picker dialog for the database name.

        If a path is returned, it makes the "Create Database" button visible and sets the database name to the selected path.

        :param e: The event object associated with the result of the file picker dialog.
        """
        if e.path:
            self.controls[0].controls[0].controls[2].visible = True
            self.tf_db_name.value = e.path
            self.update()

    def build(self):
        """
        Builds the UI for creating a new database.

        This method creates a FilePicker and a Column with several components, including a TextField for the database name, a Tab with the table specifications, and a Button to create the database.
        The method also sets the initial state of the UI components.

        :return: A Column object containing the UI for creating a new database.
        """
        self.snackbar = ft.SnackBar(content=ft.Text(""),)

        save_file_dialog = ft.FilePicker(on_result=self.save_file_result)

        self.tf_db_name = ft.TextField(label="Database Name", read_only=True, expand=True, height=40,border_color = ft.Colors.BLUE_500)   
        self.table_tabs = ft.Tabs(selected_index=0, animation_duration=10, divider_color=ft.Colors.BLUE_500, unselected_label_color=ft.Colors.BLUE_500, tabs=[],)
        self.button_create_db = ft.ElevatedButton(
            "CREATE DB", bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE, 
            visible=False, on_click=self.create_database, 
        )

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "SAVE WITH NAME", bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE,
                            on_click=lambda _: save_file_dialog.save_file(
                                dialog_title="Save Database with Name", 
                            ),
                        ),
                        self.tf_db_name,
                        ft.TextField(label="Number of Tables", width=150, height=40, border_color=ft.Colors.BLUE_500, keyboard_type=ft.KeyboardType.NUMBER, visible=False, on_submit=self.design_tabs_layout,),              
                    ],
                ),
                ft.Container(alignment=ft.alignment.center, height = 530, 
                             content=self.table_tabs,),
                self.button_create_db,
                self.snackbar,
                save_file_dialog,
            ],
            horizontal_alignment="center",
            spacing = 20,
        )
import flet as ft
from database_manager import DbManager


class DB_Column_Container(ft.Control):
    def __init__(self, field_info: dict, button: ft.ElevatedButton = None):
        """
        Constructor for the DB_Column_Container class.

        Parameters:
            field_info (dict): a dictionary containing information about a column in a database table.
            button (ft.ElevatedButton, optional): the button associated with the column container. Defaults to None.
        """
        super().__init__()
        self.field_info = field_info
        self.__button = button

    def get_column_name(self):
        """Returns the name of the column in the database table."""
        return self.field_info["name"]
    
    def get_column_type(self):
        """Returns the SQLAlchemy data type of the column in the database table."""
        return self.field_info["type"]
    
    def get_column_value(self):
        """Returns the value of the text field in the column container, which represents a column in the database table."""
        return self.__text_field.value

    def isNullable(self):
        """Returns whether the column in the database table is nullable or not."""
        return self.__nullable_checkbox.value

    def textfield_isEmpty(self):
        """Returns whether the text field in the column container is empty or not."""
        isEmpty = False
        if self.__text_field.value == "":
            isEmpty = True
        return isEmpty
    
    def set_textfield_border_color(self, color):
        """Sets the border color of the text field in the column container to the given color."""
        self.__text_field.border_color = color
        self.__text_field.update()

    def textfield_on_change(self, e):
        """Called when the text field in the column container changes its value.

        If the text field is not empty, the button associated with the column container is made visible.
        Otherwise, the button is made invisible.
        """
        if e.control.value != "" and self.__button is not None:
            self.__button.visible = True
            self.__button.update()
        elif e.control.value == "" and self.__button is not None:
            self.__button.visible = False
            self.__button.update()

    def expand_container(self):
        """Expands the column container, making the additional information and the text field visible.
        Also changes the icon of the expand button to an up arrow.
        """
        self.__visible_column.visible = True
        self.__expand_button.icon = ft.Icons.ARROW_DROP_UP
        self.update()

    def collapse_container(self):
        """Collapses the column container, hiding the additional information and the text field.
        Also changes the icon of the expand button to a down arrow.
        """
        self.__visible_column.visible = False
        self.__expand_button.icon = ft.Icons.ARROW_DROP_DOWN
        self.update()

    def expand_button_on_click(self, e):
        """
        Toggles the visibility of the column container and updates the expand button icon.

        If the visible column is currently visible, this function will collapse the container,
        hiding the additional information and changing the expand button icon to a down arrow.
        If the visible column is not visible, it will expand the container, making the additional
        information visible and changing the expand button icon to an up arrow.

        :param e: The event object associated with the button click.
        """
        if self.__visible_column.visible:
            self.collapse_container()
        else:
            self.expand_container()

    def build(self):
        """
        Constructs and returns a Flet Container that represents the UI for a database column.

        This method initializes and configures the UI components necessary to display a 
        database column's details, including an expand button, checkboxes for nullable and 
        primary key attributes, and a text field for entering new values. The components are 
        organized within a visible column that can be toggled between expanded and collapsed 
        states.

        The container returned contains:
        - A header with the column name and an expand button.
        - An expandable section with details about the column type, nullable status, primary 
        key status, and a text field for new values.

        :return: A Flet Container object encapsulating the column's UI elements.
        """
        self.__expand_button = ft.IconButton(
            ft.Icons.ARROW_DROP_DOWN,
            icon_color=ft.Colors.WHITE,
            on_click = self.expand_button_on_click,
        )
        
        self.__nullable_checkbox = ft.Checkbox(label="Nullable", value=self.field_info["nullable"], disabled=True,)
        
        self.__text_field = ft.TextField(
            label="New Value", height=40, border_color = ft.Colors.BLUE_500,
            on_change=self.textfield_on_change,
        )        

        self.__visible_column = ft.Column(
            [
                ft.Row(
                        [
                            ft.Text(
                                self.field_info["type"], 
                                style=ft.TextStyle(italic=True, decoration=ft.TextDecoration.UNDERLINE),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            self.__nullable_checkbox,
                            ft.Checkbox(label="Primary Key", value=self.field_info["primary_key"], disabled=True,),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row([self.__text_field,],),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            visible=False,
        )         
        
        return ft.Container(
            width=300,
            border=ft.border.all(1, ft.Colors.BLUE_500),
            content=ft.Column(
                [
                    ft.Container(
                        padding=ft.padding.only(left=5, right=0, top=0, bottom=0),
                        bgcolor=ft.Colors.BLUE_500,
                        content=ft.Row(
                            [
                                ft.Text(self.field_info["name"], style=ft.TextStyle(color=ft.Colors.WHITE)),
                                self.__expand_button,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ),
                    ft.Container(content=self.__visible_column,),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )


class Update_Record_Dialog(ft.Control):
    def __init__(self, table_name: str, row_index: int, columns: list, on_update_callback):
        """
        Creates an Update_Record_Dialog.

        Parameters:
            table_name (str): The name of the table of which the record is being updated.
            row_index (int): The index of the record in the table.
            columns (list): A list of dictionaries. Each dictionary contains the information of a field in the table,
                with the following keys:
                    'name': the name of the field
                    'type': the type of the field
                    'nullable': whether the field can contain NULL values or not
                    'primary_key': whether the field is a primary key or not
            on_update_callback (function): a callback function that is called when the user clicks the "Update Record" button.
                the callback function takes no arguments.
        """
        super().__init__()
        self.table_name = table_name
        self.row_index = row_index
        self.columns = columns
        self.on_update_callback = on_update_callback


    def check_required_fields_completion(self):
        """ 
        This function is used to check if all the required fields of a record have been filled in when updating a record.
        It checks all the rows in the column except the last two, which are the buttons to update or cancel the update.
        If a field is required (checkbox is not checked) and the textfield is empty, the function returns False and the textfield border is set to red.
        If a field is required (checkbox is not checked) and the textfield is not empty, the function returns True and the textfield border is set to white.
        If a field is not required (checkbox is checked), the function returns True.
        """
        isCompleted = True

        for row in self.rows[:-2]:
            checkbox = row.controls[1]
            textfield = row.controls[2]
            if not checkbox.value and textfield.value == "":
                isCompleted = False   
                textfield.border_color = ft.Colors.RED   
            elif not checkbox.value and not textfield.value == "":
                textfield.border_color = ft.Colors.WHITE 
            textfield.update()  

        return isCompleted
    
    def get_new_record_specs(self):
        """
        This function is used to collect all the new values of a record, when updating a record.
        It goes through all the rows in the column except the last two, which are the buttons to update or cancel the update.
        For each row, if the textfield of the row is not empty, the function adds the text of the row as a key and the value of the textfield as a value to the dictionary.
        The dictionary is then returned.
        """
        new_record = {}

        for row in self.rows[:-2]:
            text = row.controls[0]
            textfield = row.controls[2]

            if len(textfield.value) > 0:
                new_record.update({text.value: textfield.value})
        
        return new_record

   
    def update_record(self, e):
        """
        Handles the update of a record in the database.

        This function first checks if all required fields are completed. If they are,
        it retrieves the new record specifications. If the record has been updated, 
        it closes the dialog, updates the UI, and triggers the on_update_callback 
        with the new record data.

        :param e: The event object associated with the button click.
        :return: A dictionary representing the updated record if successful, 
                or None if the required fields are not completed.
        """
        new_record = None
        if self.check_required_fields_completion():
            new_record = self.get_new_record_specs()

            # if data are updated, data are send
            if new_record:                
                # Close the dialog
                self.controls[0].open = False
                self.update()

                self.on_update_callback(new_record)

        return new_record


    def build(self):
        """
        Builds the UI for updating a record in the database.

        This function creates an AlertDialog with a title that shows the name of the table and the index of the record to be updated.
        The content of the dialog is a column of widgets, each representing a field in the record. The widgets are:
        - Text: The name of the field.
        - Checkbox: Whether the field can be NULL or not.
        - TextField: The current value of the field.

        The function then adds an ElevatedButton to the column, labeled "Update Record", which is used to trigger the update of the record.

        The function returns the AlertDialog.

        :return: The AlertDialog.
        """
        self.rows = []
        for column in self.columns:
            self.rows.append(
                ft.Row(
                    [
                        ft.Text(value=column["name"], style=ft.TextStyle(color=ft.Colors.WHITE), overflow=ft.TextOverflow.ELLIPSIS, width = 300,),
                        ft.Checkbox(label="NULL", value=column["nullable"], disabled=True, width=100,),
                        ft.TextField(label=column["type"], border_color = ft.Colors.WHITE, height=40, width=350, ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            )
        self.rows.extend(
            [
                ft.Container(height=40), 
                ft.ElevatedButton("Update Record", bgcolor=ft.Colors.WHITE, color=ft.Colors.BLUE_500, on_click=self.update_record,),
            ]
        )

        
        return ft.AlertDialog(
            open=True,
            bgcolor=ft.Colors.BLUE_500,
            title=ft.Text(f"Updating values of {self.table_name} record #{self.row_index}", style=ft.TextStyle(color=ft.Colors.WHITE), text_align="center",),
            content=ft.Container(
                width=800,
                content=ft.Column(
                    controls=self.rows,
                    horizontal_alignment="center",
                    scroll=ft.ScrollMode.ALWAYS,
                ), 
            ),         
        )


class View_Db_UI(ft.Control):
    def __init__(self, db_name: str):
        """
        Constructor for the View_Db_UI class.

        Parameters:
            db_name (str): The name of the database to view.

        Initializes the UI control and sets the database to view.
        """
        super().__init__()
        self.db_manager = DbManager()
        self.db_name = db_name

    def show_tables_specs_layout(self, e):
        """
        Toggle the visibility of the column specifications layout for the currently selected table.
        Also toggle the icon of the button to show/hide the column specifications layout.
        """        
        self.columns_specs_layout.visible = not self.columns_specs_layout.visible

        if e.control.icon == ft.Icons.ARROW_DROP_DOWN: 
            e.control.icon = ft.Icons.ARROW_DROP_UP
        else:
            e.control.icon = ft.Icons.ARROW_DROP_DOWN

        self.update()

    
    def check_required_fields_completion(self):
        """
        Checks if all required fields are completed.

        A required field is a field that is not nullable. If a required field is empty, the function returns False and the textfield border color is set to red.
        If a required field is not empty, the function returns True and the textfield border color is set to blue.
        
        :return: True if all required fields are completed, False otherwise.
        """
        isCompleted = True

        for column_container in self.db_columns_container:
            if not column_container.isNullable() and column_container.textfield_isEmpty():
                isCompleted = False
                column_container.set_textfield_border_color(ft.Colors.RED)
                column_container.expand_container()
            elif not column_container.isNullable() and not column_container.textfield_isEmpty():
                column_container.set_textfield_border_color(ft.Colors.BLUE_500)                

        return isCompleted
    

    def get_new_record_specs(self):
        """
        Gets the new record specifications from the UI.

        :return: A dictionary with the new record specifications. The keys are the column names and the values are the values of the textfields in the UI.
        """
        new_record = {}
        for column_container in self.db_columns_container:
            name = column_container.get_column_name()
            value = column_container.get_column_value()
            if len(value) > 0:
                new_record.update({name: value})
        
        return new_record


    def add_new_rec_on_click(self, e):
        """
        Handles the click event of the "Add New Record" button.

        First checks if all required fields are completed. If they are, it retrieves the new record specifications.
        Then it inserts the new record into the database and updates the data table content in the UI.
        
        :param e: The event object associated with the button click.
        """
        if self.check_required_fields_completion():
            if self.get_new_record_specs():
                # get the index of the selected table
                dd = self.controls[0].controls[0].content.controls[0].content.controls[1].controls[1]
                index = [table["name"] for table in self.db_structure].index(dd.value)

                # insert new value into the database
                self.db_manager.create_connection(self.db_name)
                self.db_manager.insert_new_record(table_name=dd.value, record=self.get_new_record_specs())            

                # update the data table content
                self.db_manager.create_connection(self.db_name)

                self.controls[0].controls[1].content.controls[0].controls = [
                    self.build_data_table_UI(
                        columns=self.db_structure[index]["fields"], 
                        table_content=self.db_manager.read_from_table(table_name=dd.value)
                    )
                ]

                # closing all column containers
                for column_container in self.db_columns_container:
                    column_container.collapse_container()
                
                self.update()           

    
    def tf_search_value_on_change(self, e):
        """
        Handles the change event of the search textfield.

        Retrieves the table name from the dropdown, updates the data table content with the result of the search and updates the UI.

        :param e: The event object associated with the textfield change.
        """
        #get the index of the selected table
        dd = self.controls[0].controls[0].content.controls[0].content.controls[1].controls[1]
        index = [table["name"] for table in self.db_structure].index(dd.value)

        # update the data table content
        self.db_manager.create_connection(self.db_name)

        self.controls[0].controls[1].content.controls[0].controls = [
            self.build_data_table_UI(
                columns=self.db_structure[index]["fields"], 
                table_content=self.db_manager.search_values_into_table(table_name=dd.value, search_key=e.control.value)
            )
        ]

        self.update()        
        

    def dd_table_on_change(self, e):
        """
        Handles the change event of the table dropdown.

        Empties the textfield, updates the column containers with all fields specs, updates the data table content with the selected table and updates the UI.

        :param e: The event object associated with the dropdown change.
        """
        # empty the textfield
        tf = self.controls[0].controls[0].content.controls[0].content.controls[0].controls[1]
        tf.value = ""

        #get the index of the selected table
        index = [table["name"] for table in self.db_structure].index(e.control.value)
        
        # update the column containers with all fields specs
        self.db_columns_container = [DB_Column_Container(column) for column in self.db_structure[index]["fields"]]
        self.columns_specs_layout.controls[1].controls = self.db_columns_container

        # update the data table content
        self.db_manager.create_connection(self.db_name)

        self.controls[0].controls[1].content.controls[0].controls = [
            self.build_data_table_UI(
                columns=self.db_structure[index]["fields"], 
                table_content=self.db_manager.read_from_table(table_name=self.db_structure[index]["name"])
            )
        ]
        
        self.update()


    def edit_record_on_click(self, e, row_index):
        """
        Handles the click event for editing a record.

        This function retrieves the selected table and record index, and
        opens an Update_Record_Dialog for the user to update the record. 
        Once the record is updated, it uses a callback to handle the 
        updated record, updating the database and the data table content 
        in the UI.

        :param e: The event object associated with the button click.
        :param row_index: The index of the record to be edited in the 
                        current table.
        """

        def handle_updated_record(self, table_name, row_index, new_record):
            """
            Handles the update of a record in the database.

            This function updates the database record with the new values and
            then updates the data table content in the UI.

            :param table_name: The name of the table in which the record is being updated.
            :param row_index: The index of the record to be updated in the table.
            :param new_record: A dictionary with the new values of the record.
            """
            # update database record
            self.db_manager.create_connection(self.db_name)
            self.db_manager.update_record(table_name, row_index, new_record)           

            # update the data table content
            self.db_manager.create_connection(self.db_name)

            self.controls[0].controls[1].content.controls[0].controls = [
                self.build_data_table_UI(
                    columns=self.db_structure[index]["fields"], 
                    table_content=self.db_manager.read_from_table(table_name=dd.value)
                )
            ]
            
            self.update()   

        
        # Get the table name and the index
        dd = self.controls[0].controls[0].content.controls[0].content.controls[1].controls[1]
        index = [table["name"] for table in self.db_structure].index(dd.value)           

        update_dialog = Update_Record_Dialog(
            table_name=dd.value,
            row_index=row_index,
            columns=self.db_structure[index]["fields"],
            on_update_callback=lambda new_record: handle_updated_record(self, dd.value, row_index, new_record)
        )

        # Show the dialog
        self.page.dialog = update_dialog
        self.page.update()


    def delete_record_on_click(self, e, row_index):
        """
        Handles the click event for deleting a record.

        This function retrieves the selected table and record index, deletes the record from the database, and
        then updates the data table content in the UI.

        :param e: The event object associated with the button click.
        :param row_index: The index of the record to be deleted in the current table.
        """
        #get the selected table
        dd = self.controls[0].controls[0].content.controls[0].content.controls[1].controls[1]
        index = [table["name"] for table in self.db_structure].index(dd.value)  

        # update database record
        self.db_manager.create_connection(self.db_name)
        self.db_manager.delete_record(dd.value, row_index)           

        # update the data table content
        self.db_manager.create_connection(self.db_name)

        self.controls[0].controls[1].content.controls[0].controls = [
            self.build_data_table_UI(
                columns=self.db_structure[index]["fields"], 
                table_content=self.db_manager.read_from_table(table_name=dd.value)
            )
        ]
        
        self.update()   



    def build_data_table_UI(self, columns: list, table_content: list):
        """
        Builds a data table UI based on the given columns and table content.

        :param columns: A list of dictionaries containing the column names and types.
        :param table_content: A list of lists containing the table content.
        :return: A DataTable object that displays the content of the table.
        """
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text(column["name"]), tooltip=column["type"]) 
                for column in columns
            ],            
            rows=[
                ft.DataRow([ft.DataCell(ft.Text(str(elem))) for elem in row])
                for row in table_content
            ],
            horizontal_lines=ft.BorderSide(width=1, color=ft.Colors.BLUE_500),
            heading_row_color=ft.Colors.BLUE_500,
        )

        # add a column with the edit and delete buttons
        data_table.columns.append(ft.DataColumn(label=ft.Text("")))
        for i in range(len(data_table.rows)):
            data_table.rows[i].cells.append(
                ft.DataCell(
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT, tooltip="Edit Record",
                                on_click=lambda e, row_index=i: self.edit_record_on_click(e, row_index+1),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE, tooltip="Delete Record",
                                on_click=lambda e, row_index=i: self.delete_record_on_click(e, row_index+1),
                            ),                        
                        ]
                    ),
                )
            )
        return data_table


    def build(self):
        """
        Builds the UI for viewing a database.

        This function first creates a connection to the selected database and then
        inspects the database structure and reads the content of the first table.

        It creates a column of widgets for each column in the first table, with the
        column name, the data type, nullable status, primary key status, and a text field
        for entering new values.

        It then creates a DataTable that displays the content of the first table and adds
        buttons for editing and deleting records.

        Finally, it creates a column with the widgets and the DataTable and returns it.

        :return: A Column object containing the UI for viewing the database.
        """
        if self.db_name:
            self.db_manager.create_connection(self.db_name)
            self.db_structure = self.db_manager.inspect_database()
            self.table_content = self.db_manager.read_from_table(self.db_structure[0]["name"])

            self.db_columns_container = [DB_Column_Container(column) for column in self.db_structure[0]["fields"]]
           
            self.columns_specs_layout = ft.Column(
                [
                    ft.Divider(color=ft.Colors.BLUE_500),
                    ft.Row(controls=self.db_columns_container, wrap=True),
                    ft.Row(
                        [
                            ft.ElevatedButton("Add New Record",bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE, on_click=self.add_new_rec_on_click),
                        ], 
                        alignment=ft.MainAxisAlignment.END,
                    ),                      
                ], 
                visible=False, spacing=0)

            return ft.Column(
                scroll=ft.ScrollMode.ALWAYS,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=5,
                        border=ft.border.all(1, ft.Colors.BLUE_500),  
                        content=ft.Column(
                            [
                                ft.Container(
                                    gradient=ft.LinearGradient(
                                        Colors=[ft.Colors.BLUE_500,  ft.Colors.WHITE],
                                        begin=ft.Alignment(-1, -1), 
                                        end=ft.Alignment(0.3, 1),
                                    ),
                                    content=ft.Column(
                                        [
                                            ft.Row(
                                                    [
                                                        ft.Text(self.db_name, size=14, weight="bold", color=ft.Colors.BLACK),
                                                        ft.TextField(
                                                            label="Search Value", prefix_icon=ft.Icons.SEARCH,  
                                                            border_color = ft.Colors.BLUE_500, height=40, 
                                                            on_change = self.tf_search_value_on_change,
                                                        ),
                                                    ],
                                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.IconButton(ft.Icons.ARROW_DROP_DOWN, icon_color=ft.Colors.WHITE, icon_size=40,tooltip="More details", on_click=self.show_tables_specs_layout),
                                                    ft.Dropdown(
                                                        height=40,
                                                        content_padding=8,
                                                        prefix_icon=ft.Icons.TABLE_VIEW, 
                                                        label="Select Table", 
                                                        value = self.db_structure[0]["name"],  
                                                        border_color = ft.Colors.BLUE_500,
                                                        options=[ft.dropdown.Option(table["name"]) for table in self.db_structure],
                                                        on_change = self.dd_table_on_change,
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            ),
                                        ],
                                        spacing=1,
                                    ),
                                ),
                                self.columns_specs_layout,                                
                            ],
                            spacing = 1,
                        ),            
                    ),

                    ft.Container(
                        border=ft.border.all(1, ft.Colors.BLUE_500),  
                        padding = 5,
                        content=ft.Column(
                            [
                                ft.Row(
                                    [self.build_data_table_UI(columns=self.db_structure[0]["fields"], table_content=self.table_content)],
                                    scroll=ft.ScrollMode.ADAPTIVE,
                                )
                            ],
                            scroll=ft.ScrollMode.ALWAYS,
                        )
                    ),
                ],
            )            
        else:
            return ft.SnackBar(open=True, content=ft.Text("Select a database with FILE > DATABASE > OPEN"))
        
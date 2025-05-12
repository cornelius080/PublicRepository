# Sqlite3 CRUD (Flet App)

The Sqlite3 CRUD application, which allows you to create, view, update, and delete records in a SQLite database.

## Usage

To run the application, execute the following command in your terminal or command prompt:

```
python main.py
```
or
```
flet run [app_directory]
flet run --web [app_directory]
```

## API

The application uses the following classes and functions:

### `create_new_db_UI.py`

- `Create_New_Db_UI`: A Flet UserControl that provides a user interface for creating a new SQLite database.

### `database_manager.py`

- `DbManager`: A class that provides methods for creating, connecting to, and managing a SQLite database.
  - `get_camel_case_types()`: Returns a list of camel case data types in SQLAlchemy.
  - `get_upper_case_types()`: Returns a list of upper case data types in SQLAlchemy.
  - `get_generic_camel_case_types()`: Returns a list of generic camel case data types in SQLAlchemy.
  - `get_datatype_docstring(datatype)`: Returns the docstring of the given data type.
  - `create_database(db_name, tables)`: Creates a new SQLite database with the given name and tables.
  - `create_connection(db_name)`: Creates a connection to the specified SQLite database.
  - `close_connection()`: Closes the connection to the database and disposes of the engine.
  - `inspect_database()`: Inspects the database and returns a list of dictionaries that represent the tables in the database.
  - `read_from_table(table_name)`: Reads all records from the specified table.
  - `search_values_into_table(table_name, search_key)`: Searches for records in the specified table that match the search key.
  - `convert_record(engine, table_name, record)`: Converts a record's field values from strings to their appropriate data types based on the column definitions in the database table.
  - `insert_new_record(table_name, record)`: Inserts a new record into the specified table.
  - `update_record(table_name, rowid, updated_values)`: Updates a record in the specified table based on the ROWID and a dictionary of new values.
  - `delete_record(table_name, rowid)`: Deletes a record from the specified table based on the ROWID.
  - `cast_value(value, value_type)`: Converts a value in string to an object of the appropriate SQLAlchemy data type.

### `view_db_UI.py`

- `DB_Column_Container`: A Flet UserControl that represents a column in a database table.
- `Update_Record_Dialog`: A Flet UserControl that provides a dialog for updating a record in a database table.
- `View_Db_UI`: A Flet UserControl that provides a user interface for viewing and interacting with a SQLite database.
  - `show_tables_specs_layout(e)`: Toggles the visibility of the column specifications layout for the currently selected table.
  - `check_required_fields_completion()`: Checks if all required fields are completed.
  - `get_new_record_specs()`: Gets the new record specifications from the UI.
  - `add_new_rec_on_click(e)`: Handles the click event of the "Add New Record" button.
  - `tf_search_value_on_change(e)`: Handles the change event of the search textfield.
  - `dd_table_on_change(e)`: Handles the change event of the table dropdown.
  - `edit_record_on_click(e, row_index)`: Handles the click event for editing a record.
  - `delete_record_on_click(e, row_index)`: Handles the click event for deleting a record.
  - `build_data_table_UI(columns, table_content)`: Builds a data table UI based on the given columns and table content.
  - `build()`: Builds the UI for viewing a database.






import sqlalchemy as db
from datetime import datetime, date

class DbManager():
    all_types = [name for name in db.types.__dict__ if not name.startswith('_')]
    types = [name for name in all_types if name[0].isupper()]

    def __init__(self):
        """
        Initializes the DbManager object.
        
        Sets the engine and connection to None. They will be set later when a database connection is established.
        """
        self.engine = None
        self.connection = None

    def get_camel_case_types(self) -> list:
        """
        Returns a list of camel case datatypes in SQLAlchemy.
        
        This list includes types that start with an uppercase letter but are not entirely uppercase.
        These types are commonly used in a database context. The returned list does not cover all the camel case datatypes available in SQLAlchemy, but a subset that is most relevant for 
        common database operations.
        https://docs.sqlalchemy.org/en/21/core/type_basics.html
        """

        return [name for name in DbManager.types if not name.isupper()]
    
    def get_upper_case_types(self) -> list:
        """Returns a list of upper case datatypes in SQLAlchemy. This list consists of some generic types that are most commonly used in a database. The returned list does not include all upper case datatypes in SQLAlchemy, but a subset of them. The list is as follows: [BINARY, BLOB, BOOLEAN, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, JSON, LARGE_BINARY, NUMERIC, PICKLE_TYPE, REAL, SMALLINTEGER, STRING, TEXT, TIME, TIMESTAMP, UNICODE, VARCHAR]
        https://docs.sqlalchemy.org/en/21/core/type_basics.html"""
        return [name for name in DbManager.types if name.isupper()]
    
    def get_generic_camel_case_types(self) -> list:
        """Returns a list of generic camel case datatypes in SQLAlchemy. This list consists of some basic types that are most commonly used in a database. The returned list does not include all camel case datatypes in SQLAlchemy, but a subset of them. The list is as follows: [BigInteger, Boolean, Date, DateTime, Double, Float, Integer, LargeBinary, SmallInteger, String, Text].
        https://docs.sqlalchemy.org/en/21/core/type_basics.html"""
        camel = self.get_camel_case_types()
        #[BigInteger, Boolean, Date, DateTime, Double, Float, Integer, LargeBinary, SmallInteger, String, Text]
        return [
            camel[i] for i in [0,1,3,4,5,7,9,11,17,18,19] 
        ]
    
    def get_datatype_docstring(self, datatype) -> str:
        """Returns the docstring of the given datatype.
        
        Parameters:
            datatype (str): the name of the datatype to look up
        """
        return getattr(db.types, datatype).__doc__
    
    def create_database(self, db_name: str, tables: list):
        """
        Creates a new database with the given name and tables.

        Parameters:
            db_name (str): the name of the database to create
            tables (list): a list of dictionaries describing the tables to create
                each dictionary must have the following keys:
                    'name': the name of the table
                    'fields': a list of dictionaries describing the fields of the table
                        each dictionary must have the following keys:
                            'name': the name of the field
                            'data_type': the type of the field (must be a valid SQLAlchemy type)
                            'nullable': if the field can be nullable (default is False)
                            'unique': if the field must be unique (default is False)
                            'primary_key': if the field is a primary key (default is False)
        """
        # create the connection
        self.create_connection(db_name)

        # create a table with some fields inside
        metadata = db.MetaData() 
        for table in tables:
            columns = []

            for field in table['fields']:
                column_type = getattr(db, field['data_type'])()  
                
                kwargs = {}     
                kwargs.update([
                    ('nullable', field.get('nullable')),
                    ('unique', field.get('unique')),
                    ('primary_key', field.get('primary_key')),
                ])
        
                columns.append(db.Column(field['name'], column_type, **kwargs))

            db.Table(table['name'], metadata, *columns)
        
        metadata.create_all(self.engine)

        # close the connection
        self.close_connection()
    

    def create_connection(self, db_name: str):
        """
        Creates a connection to the specified database.

        Args:
            db_name (str): the name of the database

        Returns:
            None

        Notes:
            The database name should be a valid path to a SQLite database file.
            If the database file does not exist, it will be created.
            The connection to the database is stored in the `self.connection` attribute.
        """
        dburl = "sqlite:///" + db_name.replace('\\', '\\\\')

        # create an engine to connect to the database
        self.engine = db.create_engine(dburl)
        self.connection = self.engine.connect() 

    def close_connection(self):
        """
        Closes the connection to the database and disposes of the engine.

        This method should be called when you are finished with the database and
        want to release any resources associated with the connection and engine.
        """
        self.connection.close()
        self.engine.dispose()

    def close_all_connections(self):
        """
        Closes all connections to the database and disposes of the engine.

        This method is a shortcut to calling :meth:`close_connection` and
        :meth:`close_connection` on all connections and the engine.
        """
        self.engine.dispose()

    def inspect_database(self) -> list:
        """
        Inspects the database and returns a list of dictionaries that represent the tables in the database.
        Each dictionary contains the name of the table and a list of fields (columns) in that table.
        The fields are represented as dictionaries with the following keys:

        - name: the name of the field
        - type: the type of the field
        - nullable: whether the field can contain NULL values
        - default: the default value of the field
        - primary_key: whether the field is a primary key

        :return: a list of dictionaries that represent the tables in the database
        """
        db_structure = []
        if self.engine is not None:
            inspector = db.inspect(self.engine)

            tables = inspector.get_table_names() # list of string
            #get_columns(table) -> list(dict{'name': , 'type': , 'nullable':, 'default': , 'primary_key': })
            db_structure = [{'name': table, 'fields': inspector.get_columns(table)} for table in tables]

        return db_structure
    
    def read_from_table(self, table_name: str) -> list:
        """
        Reads all records from the specified table.

        This function generates a SQL query to read all records from the specified table.
        It returns a list of records.

        :param table_name: The name of the table to read from.
        :return: A list of records from the table.
        """
        result = []
        if self.engine is not None:
            with self.connection as conn:
                result = conn.execute(db.text(f'SELECT * FROM {table_name}')).fetchall() #list

        return result
    
    def search_values_into_table(self, table_name: str, search_key: str) -> list:        
        """
        Searches for records in the specified table that match the search key.

        This function generates a SQL query to search for the search_key across 
        all columns of the specified table. It returns a list of records that 
        contain the search_key in any column.

        :param table_name: The name of the table to search within.
        :param search_key: The value to search for within table columns.
        :return: A list of records that match the search key.
        """
        result = []
        if self.engine is not None:
            inspector = db.inspect(self.engine)
            columns_names = [column['name'] for column in inspector.get_columns(table_name)]
            like_conditions = [f"{column} LIKE '%{search_key}%'" for column in columns_names]
            search_key = " OR ".join(like_conditions)

            with self.connection as conn:
                result = conn.execute(db.text(f'SELECT * FROM {table_name} WHERE {search_key}')).fetchall() #list

            return result
    

    def convert_record(self, engine: db.Engine, table_name: str, record: dict):        
        """
        Converts a record's field values from strings to their appropriate data types
        based on the column definitions in the database table.

        This function uses SQLAlchemy's inspector to determine the data types of 
        columns in the specified table and converts the input record's values 
        accordingly. Supported conversions include boolean, date, and datetime types.

        :param engine: A SQLAlchemy engine object for the database connection.
        :param table_name: The name of the table for which the record is being converted.
        :param record: A dictionary representing a record with field names as keys
                    and string values to be converted.
        :return: A dictionary with the same keys as the input record, but with 
                values converted to their appropriate data types.
        """

        def string_to_boolean(input_string: str) -> bool:
            mapping = {"true": True, "false": False}
            return mapping.get(input_string.lower(), None)
        
        def sting_to_time(time_str: str) -> datetime.time:
            if len(time_str) == 2:  # "12"
                time_str = "2000-01-01T" + time_str + ":00"
            elif len(time_str) == 5 and '.' in time_str:  # "12.30"
                time_str = "2000-01-01T" + time_str.replace('.', ':')
            elif len(time_str) == 5 and ':' in time_str:  # "12:30"
                time_str = "2000-01-01T" + time_str
            return datetime.fromisoformat(time_str).time()


        inspector = db.inspect(engine)
        
        columns = inspector.get_columns(table_name) # list of dict
        columns_types = {col['name']: col['type'] for col in columns}
        record_types = {name: columns_types[name] for name in record.keys()}

        converted_record = {}
        for key, value in record_types.items():
            #print(f"{key}: {value} --- {type(value)}")
            if type(value) is db.sql.sqltypes.BOOLEAN:
                converted_record.update({key: string_to_boolean(record[key])})
            elif type(value) is db.sql.sqltypes.DATE:
                converted_record.update({key: date.fromisoformat(record[key])})
            elif type(value) is db.sql.sqltypes.DATETIME:
                converted_record.update({key: datetime.fromisoformat(record[key])})
            else:
                converted_record.update({key: record[key]})

        return converted_record


    def insert_new_record(self, table_name: str, record: dict):
        """
        Insert a new record into a specified table. Record is a dictionary with columns names as keys and their values as values (strings)

        :param table_name: The name of the table in which the record will be inserted.
        :param record: A dictionary with the columns as keys and the values as strings.
        """
        if self.engine is not None:
            # convert some record values (from string to boolean, date or datetime)
            converted_record = self.convert_record(self.engine, table_name, record)  

            # define the query
            columns = ", ".join(converted_record.keys())  # Ottieni i nomi delle colonne
            placeholders = ", ".join([f":{key}" for key in converted_record.keys()])
            query = db.text(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")

            with self.connection as conn:
                # execute the query 
                conn.execute(query,converted_record)
                conn.commit()

    
    def update_record(self, table_name: str, rowid: int, updated_values: dict):        
        """
        Updates a record in a specified table based on the ROWID and a dictionary of new values.

        :param table_name: The name of the table in which the record will be updated.
        :param rowid: The ROWID of the record to be updated.
        :param updated_values: A dictionary with the columns as keys and the new values as values (strings).
        """
        if self.engine is not None:
            converted_values = self.convert_record(self.engine, table_name, updated_values)

            # Create the list of columns to update (exclude ROWID)
            set_clause = ", ".join([f"{col} = :{col}" for col in converted_values.keys()])
            
            # Define the query of update
            query = db.text(f"UPDATE {table_name} SET {set_clause} WHERE ROWID = :rowid")

            # Add the ROWID to the dictionary
            converted_values.update({'rowid': rowid})


            with self.connection as conn:
                conn.execute(query, converted_values)
                conn.commit()  
    
    def delete_record(self, table_name: str, rowid: int):
        """
        Deletes a record from a specified table based on the ROWID and restructures
        the table to maintain its integrity. The operation involves removing the 
        record, copying the table structure, creating a new table, transferring 
        data, and renaming the new table to replace the original.

        :param table_name: The name of the table from which the record will be deleted.
        :param rowid: The ROWID of the record to be deleted.
        """
        if self.engine is not None:
            with self.connection.begin():
                ####################################
                # Remove one record from the table
                delete_query = db.text(f"DELETE FROM {table_name} WHERE ROWID = :rowid")
                # Execute the query passing the parameter :rowid in base 1
                self.connection.execute(delete_query, {"rowid": rowid})

                ################################
                # Copy of the original table
                # Step 1: Get the structure of the original table
                columns_query = db.text(f"PRAGMA table_info({table_name})")
                columns = self.connection.execute(columns_query).fetchall()        

                # Step 2: Create the new table
                create_table_query = f"CREATE TABLE {table_name}_new ("

                for column in columns:
                    column_name = column[1]  # column name
                    column_type = column[2]  # column type
                    notnull = column[3]      # NULL (true or false)
                    default_value = column[4] # default value
                    primary_key = column[5]  # PRIMARY KEY (true or false)
                    
                    # Add the column definition to the query
                    column_definition = f"{column_name} {column_type}"

                    if notnull:
                        column_definition += " NOT NULL"
                    
                    if default_value is not None:
                        column_definition += f" DEFAULT {default_value}"
                    
                    if primary_key:
                        column_definition += " PRIMARY KEY"
                    
                    create_table_query += column_definition + ", "

                # Remove last comma
                create_table_query = create_table_query.rstrip(", ") + ")"
                self.connection.execute(db.text(create_table_query))

                # Step 3: Copy data from the original table to the new table
                copy_data_query = db.text(f"INSERT INTO {table_name}_new SELECT * FROM {table_name}")
                self.connection.execute(copy_data_query)

                # Step 4: Delete original table
                drop_query = db.text(f"DROP TABLE {table_name}")
                self.connection.execute(drop_query)

                # Step 5: Rename new table
                alter_query = db.text(f"ALTER TABLE {table_name}_new RENAME TO {table_name}")
                self.connection.execute(alter_query)
            


    def cast_value(self, value: str, value_type: str):
        """
        Converte un valore in stringa in un oggetto SQLAlchemy 
        di tipo appropriato in base al tipo specificato.
        
        :param value: il valore in stringa
        :param value_type: il tipo di dato da utilizzare per la conversione
        :return: l'oggetto convertito se il tipo di dato è supportato, 
                 None altrimenti
        """
        # Mappa i tipi di dato a classi SQLAlchemy
        type_mapping = {
            "INT": db.Integer,
            "FLOAT": db.Float,
            "STRING": db.String,
            # Aggiungi altri tipi se necessario
        }

        # Controlla se il tipo specificato è nella mappa
        if value_type in type_mapping:
            # Converte il valore in base al tipo
            try:
                return type_mapping[value_type](value)
            except ValueError as e:
                print(f"Errore nel casting del valore: {e}")
                return None
        else:
            print(f"Tipo di dato '{value_type}' non supportato.")
            return None

import argparse
import json
import sqlite3
from faker import Faker
import os
from datetime import datetime

# Initialize the Faker library
fake = Faker()

def create_database(db_name, schema):
    """
    Create the SQLite database based on the schema.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for table_name, table_schema in schema["tables"].items():
        columns = table_schema["columns"]
        column_definitions = []
        
        # Create columns based on the schema
        for column_name, column_type in columns.items():
            column_definitions.append(f"{column_name} {column_type}")
        
        # Check if foreign keys exist
        if "foreign_keys" in table_schema:
            for fk_name, fk_details in table_schema["foreign_keys"].items():
                ref_table, ref_column = fk_details["references"].split("(")
                ref_column = ref_column.rstrip(")")

                # Add foreign key constraint
                column_definitions.append(f"FOREIGN KEY ({fk_name}) REFERENCES {ref_table}({ref_column})")
        
        # Create table SQL
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)});"
        cursor.execute(create_table_sql)

    conn.commit()
    conn.close()

def generate_seed_data(table_name, table_schema, num_rows=5):
    """
    Generate realistic seed data for a table based on the schema.
    """
    seed_data = []
    columns = table_schema["columns"]
    
    for _ in range(num_rows):
        row = []
        for column_name, column_type in columns.items():
            if "TEXT" in column_type:
                row.append(fake.text(max_nb_chars=200))  # Text data
            elif "INTEGER" in column_type:
                row.append(fake.random_int(min=1, max=100))  # Integer data
            elif "TIMESTAMP" in column_type:
                row.append(fake.date_this_decade())  # Date data
            elif "BOOLEAN" in column_type:
                row.append(fake.boolean())  # Boolean data
        seed_data.append(tuple(row))
    
    return seed_data

def insert_seed_data(db_name, table_name, table_schema, seed_data):
    """
    Insert the generated seed data into the database.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    columns = table_schema["columns"]
    column_names = ", ".join(columns.keys())
    placeholders = ", ".join(["?" for _ in columns])

    insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders});"
    cursor.executemany(insert_sql, seed_data)

    conn.commit()
    conn.close()

def generate_database(db_name, schema_file):
    """
    Main function to generate database, create tables, and insert seed data.
    """
    # Load schema from the JSON file
    if not os.path.exists(schema_file):
        print(f"Error: The schema file '{schema_file}' does not exist.")
        return
    
    with open(schema_file, "r") as file:
        schema = json.load(file)

    # Step 1: Create the database and tables
    create_database(db_name, schema)

    # Step 2: Generate and insert seed data
    for table_name, table_schema in schema["tables"].items():
        seed_data = generate_seed_data(table_name, table_schema)
        insert_seed_data(db_name, table_name, table_schema, seed_data)
        print(f"Inserted {len(seed_data)} rows into table: {table_name}")

    print(f"Database '{db_name}' has been generated successfully with seed data.")

def main():
    parser = argparse.ArgumentParser(description="Generate a testable database based on a schema JSON file.")
    parser.add_argument("schema", help="The JSON schema file defining the database schema.")
    parser.add_argument("db_name", help="The name of the SQLite database to be created.")
    
    args = parser.parse_args()

    # Generate the database with the schema and seed data
    generate_database(args.db_name, args.schema)

if __name__ == "__main__":
    main()

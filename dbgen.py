import json
import random
import sqlite3
import os
from datetime import datetime
from faker import Faker

# Initialize Faker
fake = Faker()

# Function to read schema from a JSON file
def read_schema(schema_file):
    with open(schema_file, 'r') as file:
        schema = json.load(file)
    return schema


# Function to generate the SQL commands for creating tables
def generate_create_table_sql(table_name, table_schema):
    columns = table_schema['columns']
    foreign_keys = table_schema.get('foreign_keys', {})
    
    column_definitions = []
    for column_name, column_type in columns.items():
        column_definitions.append(f"{column_name} {column_type}")
    
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
    create_table_sql += ",\n".join(column_definitions)
    
    # Add foreign keys if they exist
    for column_name, fk in foreign_keys.items():
        create_table_sql += f",\nFOREIGN KEY ({column_name}) REFERENCES {fk['references']}"
    
    create_table_sql += "\n);"
    
    return create_table_sql


# Function to generate meaningful seed data for a table
def generate_seed_data(table_name, table_schema, num_rows=10):
    columns = table_schema['columns']
    seed_data = []
    
    for _ in range(num_rows):
        row = {}
        for column_name, column_type in columns.items():
            if 'TEXT' in column_type:
                if 'email' in column_name:
                    row[column_name] = fake.email()
                elif 'name' in column_name:
                    row[column_name] = fake.name()
                else:
                    row[column_name] = fake.text(max_nb_chars=50)  # Text for generic fields
            elif 'INTEGER' in column_type:
                row[column_name] = random.randint(1, 100)  # Random integer for IDs or quantity
            elif 'TIMESTAMP' in column_type:
                row[column_name] = str(fake.date_this_decade())  # Random date within the last decade
        seed_data.append(row)
    
    return seed_data


# Function to insert meaningful seed data into the database
def insert_seed_data(cursor, table_name, seed_data):
    columns = seed_data[0].keys()
    column_names = ', '.join(columns)
    placeholders = ', '.join(['?' for _ in columns])
    
    insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    
    for row in seed_data:
        values = tuple(row.values())
        cursor.execute(insert_sql, values)


# Function to generate schema, seed data, and create the database
def generate_database(schema, db_name="test_database.db"):
    if os.path.exists(db_name):
        os.remove(db_name)
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Generate tables
    for table_name, table_schema in schema['tables'].items():
        create_sql = generate_create_table_sql(table_name, table_schema)
        cursor.execute(create_sql)
        print(f"Table {table_name} created.")
    
    # Generate and insert seed data
    for table_name, table_schema in schema['tables'].items():
        seed_data = generate_seed_data(table_name, table_schema, num_rows=5)
        insert_seed_data(cursor, table_name, seed_data)
        print(f"Seed data inserted for table {table_name}.")
    
    conn.commit()
    conn.close()
    print(f"Database {db_name} has been generated and populated with seed data.")


def main():
    # Path to schema file (could be JSON or any other format)
    schema_file = 'schema.json'

    # Read the schema
    schema = read_schema(schema_file)

    # Generate the database based on the schema
    generate_database(schema, db_name='test_database.db')


if __name__ == '__main__':
    main()

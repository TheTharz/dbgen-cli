# Database Schema Generator with Seed Data

This tool helps you generate a real-world testable database schema based on a JSON definition. It allows you to create tables, define relationships, and automatically populate the database with meaningful seed data using the **Faker** library for realistic data generation.

## Features

- **Schema Creation**: Define your database schema in a JSON file and automatically create tables.
- **Foreign Key Support**: Define relationships between tables with foreign keys.
- **Seed Data Generation**: Automatically generate meaningful seed data using the **Faker** library for realistic values (e.g., names, emails, timestamps).
- **SQLite Database**: Generates an SQLite database that can be easily tested and used for real-world applications.

## Requirements

- Python 3.x
- **Faker** library (for generating meaningful data)
- SQLite (pre-installed with Python)

### Install Dependencies

To use this tool, first install the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

Where the `requirements.txt` file contains:

```
Faker
```

## How to Use

1. **Create the Schema JSON File**

   Define your database schema in a JSON file. Here's an example schema (`schema.json`):

   ```json
   {
     "tables": {
       "users": {
         "columns": {
           "id": "INTEGER PRIMARY KEY",
           "name": "TEXT NOT NULL",
           "email": "TEXT UNIQUE NOT NULL",
           "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
         }
       },
       "posts": {
         "columns": {
           "id": "INTEGER PRIMARY KEY",
           "title": "TEXT NOT NULL",
           "content": "TEXT",
           "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
           "user_id": "INTEGER"
         },
         "foreign_keys": {
           "user_id": {
             "references": "users(id)"
           }
         }
       }
     }
   }
   ```

2. **Run the Script**

   After saving your schema definition to a JSON file, run the script to generate the database and seed data:

   ```bash
   python generate_db.py
   ```

3. **Verify the Database**

   After running the script, a database file (e.g., `test_database.db`) will be created in your project directory. You can open this file using any SQLite database viewer (e.g., DB Browser for SQLite) to inspect the tables and seed data.

## Customizing the Seed Data

You can customize the number of rows generated for each table by modifying the `num_rows` parameter in the `generate_seed_data` function. Currently, it generates 5 rows by default.

```python
seed_data = generate_seed_data(table_name, table_schema, num_rows=10)
```

This will generate 10 rows instead of the default 5.

## Example Output

For the sample `users` table, you might see something like this:

| id  | name          | email                     | created_at          |
| --- | ------------- | ------------------------- | ------------------- |
| 1   | John Doe      | john.doe@example.com      | 2022-02-14 10:22:15 |
| 2   | Jane Smith    | jane.smith@example.com    | 2023-06-21 09:33:01 |
| 3   | Charlie Brown | charlie.brown@example.com | 2021-08-19 14:05:32 |

For the `posts` table:

| id  | title                  | content               | created_at          | user_id |
| --- | ---------------------- | --------------------- | ------------------- | ------- |
| 1   | Introduction to Python | This is an intro post | 2021-03-04 11:22:00 | 1       |
| 2   | Advanced SQL Tutorial  | Learn advanced SQL    | 2022-05-15 12:10:33 | 2       |
| 3   | Web Development Basics | A guide to web dev    | 2023-01-10 13:01:15 | 3       |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork the project, make improvements, and create pull requests. If you have any bug reports or feature requests, please open an issue on GitHub.

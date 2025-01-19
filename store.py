#*********************************************************************************************
# FILE   NAME:    store.py
# PROJ   NAME:    uOttaHack 7 - deepcode-challenge
# DESCRIPTION:    Store the parsed data in a MySQL database.
#
# HOW TO USE:     $ python store.py
#
#
# Contributors:
# - Zechen Zhou     zzhou186@uottawa.ca
# - Benjamin Sam    bsam079@uottawa.ca
#
#
# REVISION HISTORY
# YYYY/MMM/DD     Author                       Comments
# 2025 JAN 18     Zechen Zhou, Benjamin Sam    creation
#
#
#
#*********************************************************************************************

import mysql.connector
from mysql.connector import Error
import os
import dotenv
import parser
from dotenv import load_dotenv
from parser import parse_file
from sqlalchemy import create_engine
import pandas as pd

"""
Create a database by executing a sql file
"""
def create_db(schema_fname):
    db_connection, cursor = get_database_connection()
    
    with open(schema_fname) as f:
        sql_commands = f.read()

    # Split the SQL commands (if there are multiple statements in the file)
    sql_commands = sql_commands.split(';')

    # Execute each SQL command
    for command in sql_commands:
        if command.strip():  # Skip empty commands
            try:
                cursor.execute(command)
                db_connection.commit()  # Commit if necessary
            except mysql.connector.Error as err:
                print(f"Error executing command: {err}")
                db_connection.rollback()  # Rollback if error occurs

    # Close the cursor and connection
    close_database_connection(db_connection, cursor)


"""
Establish a connection to the MySQL database using environment variables.
"""
def get_database_connection():
    # Load the .env file
    load_dotenv()

    try:
        # Access the environment variables
        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")

        # Connect to the MySQL database
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        # Create a cursor object
        cursor = db_connection.cursor()

        return db_connection, cursor
    

    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None, None


"""
Close the cursor and database connection.
"""
def close_database_connection(db_connection, cursor):
    if cursor:
        cursor.close()
    if db_connection:
        db_connection.close()


def insert_all_data():
    table_name = "ALLINFO"

    # Load the .env file
    load_dotenv()

    try:
        # Access the environment variables
        db_host = os.getenv("DB_HOST")
        username = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        port = "3306"
    
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None, None
    
    # Define connection details
    engine = create_engine(f"mysql+pymysql://{username}:{password}@localhost/{db_name}")

    conn = engine.connect()

    df = parser.parse_file("sample.txt", parser.CAN_SKIP_SAMPLE_TXT)
    df.to_sql(table_name, conn, if_exists="append", index=False)
    

"""
Insert parsed data into table "DOMAINS".
"""
def insert_domains_data(input_file):
    # Parse the file
    parsed_lines = parse_file(input_file, skip_on_error=True)

    parsed_data = [
        (
            line.tld,
            line.ip,
            line.routable,
        )
        for line in parsed_lines
        if line is not None
    ]

    table_name = "DOMAINS"
    db_connection, cursor = get_database_connection()

    if not db_connection or not cursor:
        print("Unable to connect to the database.")
        return

    try:
        # Prepare the SQL INSERT query
        insert_query = f"""
        INSERT INTO {table_name} 
        (domain_name, ip_address, routable) 
        VALUES (%s, %s, %s)
        """

        # Execute the query for each parsed line
        cursor.executemany(insert_query, parsed_data)

        # Commit the transaction
        db_connection.commit()
        print(f"Successfully inserted {cursor.rowcount} rows into {table_name}.")

    except Error as e:
        print(f"Error inserting data: {e}")
        db_connection.rollback()  # Rollback in case of an error

    finally:
        close_database_connection(db_connection, cursor)

if __name__ == "__main__":
    create_table_sql_path = "./create.sql"
    breach_data_path = "./sample.txt"

    # Create tables in MySQL database
    # create_db(create_table_sql_path)

    # Insert parsed data into database
    # insert_domains_data(breach_data_path)

    insert_all_data()


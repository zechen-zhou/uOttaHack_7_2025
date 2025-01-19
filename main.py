#*********************************************************************************************
# FILE   NAME:    main.py
# PROJ   NAME:    uOttaHack 7 - deepcode-challenge
# DESCRIPTION:    The main orchestrator to run the tasks sequentially
#
# HOW TO USE:     $ python main.py
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

import subprocess
import mysql.connector
import os
import dotenv
from dotenv import load_dotenv

def create_db(schema_fname):
    # Load the .env file
    load_dotenv()

    # Access the environment variables
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    # Print the values (for testing purposes)
    print(f"Host: {db_host}, User: {db_user}, Password: {db_password}, Database: {db_name}")

    # Connect to the MySQL database
    db_connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    # Create a cursor object
    cursor = db_connection.cursor()
    
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
    cursor.close()
    db_connection.close()

def run_parse_store():
    print("###########################")
    print("Running parse_store.py ...\n")
    subprocess.run(["python", "parse_store.py"], check=True)

def run_enrich_data():
    print("###########################")
    print("Running enrich_data.py ...\n")
    subprocess.run(["python", "enrich_data.py"], check=True)


if __name__ == "__main__":
    create_table_sql_path = "./create.sql"

    # Create tables in MySQL database
    create_db(create_table_sql_path)

    print("###############################################")
    print("Starting the breach data processing pipeline...\n")

    # Step 1: Parse and store data
    # run_parse_store()

    # Step 2: Enrich stored data
    # run_enrich_data()
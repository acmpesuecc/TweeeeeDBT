import psycopg2import psycopg2import psycopg2

import os

from dotenv import load_dotenvimport osimport os



load_dotenv(dotenv_path='../.env')from dotenv import load_dotenvfrom dotenv import load_dotenv



# other users make a .env file and fill it 

DB_CONFIG = {

        'dbname': os.getenv('POSTGRES_DB', 'tweedbt'),load_dotenv(dotenv_path='../.env')load_dotenv(dotenv_path='../.env')

        'user': os.getenv('POSTGRES_USER', 'mayurshadhidhar'),

        'password': os.getenv('POSTGRES_PASSWORD', ''),

        'host': os.getenv('POSTGRES_HOST', '127.0.0.1'),

        'port': os.getenv('POSTGRES_PORT', '5432')# other users make a .env file and fill it # other users make a .env file and fill it 

        }

# Connection detailsDB_CONFIG = {DB_CONFIG = {

conn = psycopg2.connect(**DB_CONFIG)

# Create a cursor        'dbname': os.getenv('POSTGRES_DB', 'tweedbt'),        'dbname': os.getenv('POSTGRES_DB', 'tweedbt'),

cur = conn.cursor()

        'user': os.getenv('POSTGRES_USER', 'mayurshadhidhar'),        'user': os.getenv('POSTGRES_USER', 'mayurshadhidhar'),

# Run a simple query

cur.execute('SELECT version();')        'password': os.getenv('POSTGRES_PASSWORD', ''),        'password': os.getenv('POSTGRES_PASSWORD', ''),



# Fetch the result        'host': os.getenv('POSTGRES_HOST', '127.0.0.1'),        'host': os.getenv('POSTGRES_HOST', '127.0.0.1'),

result = cur.fetchone()

print(f"PostgreSQL version: {result[0]}")        'port': os.getenv('POSTGRES_PORT', '5432')        'port': os.getenv('POSTGRES_PORT', '5432')



# Close the cursor and connection        }        }

cur.close()

conn.close()# Connection details# Connection details

conn = psycopg2.connect(**DB_CONFIG)conn = psycopg2.connect(**DB_CONFIG)

# Create a cursor# Create a cursor

cur = conn.cursor()cur = conn.cursor()



# Run a simple query# Run a simple query

cur.execute('SELECT version();')cur.execute("SELECT version();")



# Fetch the result# Fetch and print result

result = cur.fetchone()db_version = cur.fetchone()

print(f"PostgreSQL version: {result[0]}")print("Connected to:", db_version)



# Close the cursor and connection# Always close!

cur.close()cur.close()

conn.close()conn.close()

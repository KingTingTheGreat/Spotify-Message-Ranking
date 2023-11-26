from dotenv import load_dotenv
import os
import oracledb

load_dotenv()

# not the actual production table name
PRODUCTION_TABLE = 'user_data'

ORACLE_USERNAME = os.environ['ORACLE_DATABASE_ADMIN_USERNAME']
ORACLE_PASSWORD = os.environ['ORACLE_DATABASE_ADMIN_PASSWORD']
ORACLE_DSN = os.environ['ORACLE_DATABASE_DSN']
ORACLE_WALLET_LOCATION = os.environ['ORACLE_DATABASE_WALLET_LOCATION']
ORACLE_WALLET_PASSWORD = os.environ['ORACLE_DATABASE_WALLET_PASSWORD']


def connect() -> oracledb.Connection:
    """ returns a connection to database """
    try:
        print('Connecting to Oracle Database...')
        connection = oracledb.connect(
            user=ORACLE_USERNAME,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN,
            wallet_location=ORACLE_WALLET_LOCATION,
            wallet_password=ORACLE_WALLET_PASSWORD
        )
    except oracledb.DatabaseError as e:
        print('Failed to connect to Oracle Database')
        print("The database returned the following error:", e)
        return None
    print('Successfully connected to Oracle Database')
    return connection 


# returns data from database
def print_table_names() -> None:
    """ prints names of tables in database """
    with connect().cursor() as cursor:
        cursor.execute("SELECT table_name FROM user_tables")
        tables = cursor.fetchall()
        print(tables)

def get_rows(table_name:str):
    with connect().cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        for row in data:
            yield row

def print_table(table_name:str) -> None:
    """ prints the data in the table """
    for row in get_rows(table_name):
        print(row)

def print_column_names(table_name:str) -> None:
    """ prints the column names of the table """
    with connect().cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [i[0] for i in cursor.description]
        print(columns)

def num_rows(table_name:str) -> int:
    """ returns the number of rows in the table """
    with connect().cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        return count
    
def contains(table_name:str, phone_number:str) -> bool:
    """ returns boolean indicating if input phone number is in database"""
    with connect().cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name} WHERE PHONENUMBER = '{phone_number}'")
        result = cursor.fetchone()
        if result is None:
            return False
        else:
            return True


# edits the database
def clear_table(table_name:str) -> None:
    """ clears the table """
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {table_name}")
        connection.commit()

def add_to_table(table_name:str, phone_number:str, auth_code:str) -> None:
    """ adds a phone number and auth code to the table """
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO {table_name} (PHONENUMBER, AUTHCODE) VALUES ('{phone_number}', '{auth_code}')")
        connection.commit()

def remove_from_table(table_name:str, phone_number:str) -> None:
    """ removes entry from the table with PHONENUMBER phone_number """
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name} WHERE PHONENUMBER = '{phone_number}'")
        connection.commit()

if __name__ == '__main__':
    print_table(PRODUCTION_TABLE)
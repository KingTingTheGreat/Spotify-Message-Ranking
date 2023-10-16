import os
import time
import datetime
import oracledb
from dotenv import load_dotenv

load_dotenv()

TABLE_NAME = 'user_data'

ORACLE_USERNAME = os.getenv('ORACLE_DATABASE_ADMIN_USERNAME')
ORACLE_PASSWORD = os.getenv('ORACLE_DATABASE_ADMIN_PASSWORD')
ORACLE_DSN = os.getenv('ORACLE_DATABASE_DSN')
ORACLE_WALLET_LOCATION = os.getenv('ORACLE_DATABASE_WALLET_LOCATION')
ORACLE_WALLET_PASSWORD = os.getenv('ORACLE_DATABASE_WALLET_PASSWORD')

def count_users(connection:oracledb.Connection) -> int:
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        count = cursor.fetchone()[0]
        return count

def connect_to_database():
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
        return  
    print('Successfully connected to Oracle Database')
    return connection

if __name__ == '__main__':
    connection = connect_to_database()

    data = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Number of users: {count_users(connection)}"
    print(data)

    with open('log.txt', 'a') as f:
        f.write(data + '\n')

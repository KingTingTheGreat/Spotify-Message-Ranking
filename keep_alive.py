import datetime
import oracledb
from database_functions import num_rows, PRODUCTION_TABLE

if __name__ == '__main__':
    num_users = num_rows(PRODUCTION_TABLE)

    data = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Number of users: {num_users}"
    print(data)

    with open('log.txt', 'a') as f:
        f.write(data + '\n')

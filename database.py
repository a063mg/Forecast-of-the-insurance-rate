import sqlite3
DB_NAME = 'users.db'


def init_user_table():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {'Users'}(
        user_id INTEGER PRIMARY KEY NOT NULL, 
        first_name TEXT, 
        last_name TEXT,
        username TEXT,
        city TEXT,
        risks TEXT,
        number_of_clinics TEXT
    );""")

    connect.commit()
    connect.close()


def delete_table():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS Users;")
    connect.commit()
    connect.close()


def insert(insert_values, table='Users'):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    columns = ", ".join(insert_values.keys())
    placeholders = ", ".join("?" * len(insert_values.keys()))
    values = tuple(insert_values.values())
    sql_insert_command = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"
    cursor.execute(sql_insert_command, values)
    connect.commit()
    connect.close()


def update_user_info(user_id, new_values, table='Users'):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    columns_equal = [f"{column}=?" for column, value in new_values.items()]
    placeholders = ", ".join(columns_equal)
    values = tuple(new_values.values())
    sql_update_command = f"UPDATE {table} SET {placeholders} WHERE user_id = {user_id};"
    cursor.execute(sql_update_command, values)
    connect.commit()
    connect.close()


def get_user_values(user_id, columns, table='Users'):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    column_names = ", ".join(columns)
    get_user_sql_command = f"SELECT {column_names} FROM {table} WHERE user_id = {user_id};"
    cursor.execute(get_user_sql_command)
    rows = cursor.fetchall()
    connect.close()
    return dict(zip(columns, rows[0]))


def user_exists(user_id):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    if_exists_sql_command = f"SELECT user_id FROM Users WHERE user_id = {user_id} LIMIT 1;"
    cursor.execute(if_exists_sql_command)
    row = cursor.fetchall()
    connect.close()
    return not row == []


def add_user(user_id, values):
    if not user_exists(user_id):
            insert(values)
    elif get_user_values(user_id, values.keys()) != values:
            update_user_info(user_id, values)


def update_user(user_id, new_values):
    if user_exists(user_id):
        if get_user_values(user_id, new_values.keys()) != new_values:
            update_user_info(user_id, new_values)
            return "Done"
        else:
            return "Nothing changed"
    else:
        return "User not found"

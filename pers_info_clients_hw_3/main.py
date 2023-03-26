import psycopg2

def drop_table_db(conn):
    with conn.cursor() as cur:

        cur.execute("""
            SELECT EXISTS(
            SELECT FROM pg_tables
            WHERE tablename  = 'phones');
        """)

        check_phones = cur.fetchone()

        if check_phones == (True,):
            cur.execute("""
                DROP TABLE Phones;
            """)

        cur.execute("""
            SELECT EXISTS(
            SELECT FROM pg_tables
            WHERE tablename  = 'clients');
        """)

        check_clients = cur.fetchone()

        if check_clients == (True,):
            cur.execute("""
                DROP TABLE Clients;
            """)
        conn.commit()
    return 'Таблицы Clients и Phones удалены.'

def create_db(conn):
    with conn.cursor() as cur:

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Clients (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR (40) NOT NULL,
                last_name VARCHAR (40) NOT NULL,
                email VARCHAR (40) NOT NULL UNIQUE 
            );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Phones (
                phone VARCHAR (40) UNIQUE,
                client_id INTEGER NOT NULL REFERENCES Clients (id)
            );
        """)

        conn.commit()
    return 'Таблицы Clients и Phones созданы.'

def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:

        id = []
        cur.execute("""
            SELECT email FROM Clients;
        """)

        all_emails = cur.fetchall()

        if (email,) in all_emails:
            print('Внимание! Клиент с таким email уже существует.')
        else:
            cur.execute("""
                INSERT INTO Clients (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id;
            """, (first_name, last_name, email))

            id = cur.fetchone()

        cur.execute("""
            SELECT phone FROM Phones;
        """)
        all_phones = cur.fetchall()

        if phone is not None and (phone,) not in all_phones:
            cur.execute("""
                INSERT INTO Phones (phone, client_id) VALUES (%s, %s);
            """, (phone, id))
            conn.commit()

        elif phone is not None and phone in all_phones:
            print('Внимание! Клиент с таким телефоном уже существует.')

    return id[0]

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:

        cur.execute("""
            SELECT id FROM Clients;
        """)
        all_ids = cur.fetchall()

        cur.execute("""
        SELECT phone FROM Phones;
        """)
        all_phones = cur.fetchall()

        if (client_id,) in all_ids and (phone,) not in all_phones:
            cur.execute("""
                INSERT INTO Phones (phone, client_id) VALUES (%s, %s);
            """, (phone, client_id))
            conn.commit()
        elif (phone,) in all_phones:
            print('Внимание! Клиент с таким телефоном уже существует.')
        else:
            print('Внимание! Такого клиента ещё не существует.')

        return 'Функция добавления номера выполнена.'


def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:

        cur.execute("""
            SELECT id FROM Clients;
        """)
        all_ids = cur.fetchall()
        if (client_id,) in all_ids:
            if first_name is not None:
                cur.execute("""
                    UPDATE Clients SET first_name=%s WHERE id=%s;
                """, (first_name, client_id))
                conn.commit()

            if last_name is not None:
                cur.execute("""
                    UPDATE Clients SET last_name=%s WHERE id=%s;
                """, (last_name, client_id))
                conn.commit()

            if email is not None:
                cur.execute("""
                    SELECT email FROM Clients;
                """)
                all_emails = cur.fetchall()
                if (email,) in all_emails:
                    print('Внимание! Клиент с таким email уже существует.')
                else:
                    cur.execute("""
                        UPDATE Clients SET emaiL=%s WHERE id=%s;
                    """, (email, client_id))
                    conn.commit()
        else:
            print('Внимание! Такого клиента ещё не существует.')

    return 'Функция обновления данных о клиенте выполнена.'


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:

        cur.execute("""
            SELECT client_id FROM Phones;
        """)
        all_ids = cur.fetchall()

        cur.execute("""
            SELECT phone FROM Phones;
        """)
        all_phones = cur.fetchall()

        if (client_id,) in all_ids and (phone,) in all_phones:
            cur.execute("""
                DELETE FROM Phones WHERE phone=%s;
            """, (phone,))
            conn.commit()
        else:
            print('Внимание! Такого телефона ещё не существует.')

    return 'Функция удаления номера выполнена.'


def delete_client(conn, client_id):
    with conn.cursor() as cur:

        cur.execute("""
            SELECT client_id FROM Phones;
        """)
        all_client_ids = cur.fetchall()

        if (client_id,) in all_client_ids:
            cur.execute("""
                DELETE FROM Phones WHERE client_id=%s;
            """, (client_id,))
            conn.commit()

        cur.execute("""
            SELECT id FROM Clients;
        """)
        all_ids = cur.fetchall()

        if (client_id,) in all_ids:
            cur.execute("""
                DELETE FROM Clients WHERE id=%s;
            """, (client_id,))
            conn.commit()
        else:
            print('Внимание! Такого клиента не существует.')

    return 'Функция удаления клиента выполнена.'

def view_all(conn):
    with conn.cursor() as cur:

        cur.execute("""
            SELECT * FROM Clients;
        """)
        all_clients = cur.fetchall()
        for client in all_clients:
            print(f"""id - {client[0]}, имя - {client[1]}, фамилия - {client[2]}, емейл - {client[3]}.""")

        cur.execute("""
            SELECT * FROM Phones;
        """)
        all_phones = cur.fetchall()
        for phones in all_phones:
            print(f"""Телефон - {phones[0]}, id клиента в таблице Clients - {phones[1]}.""")

    return 'Функция просмотра всего содержимого таблиц выполнена.'

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):

    with conn.cursor() as cur:
        if first_name is not None and last_name is not None:
            cur.execute("""
                SELECT id FROM Clients WHERE (first_name=%s AND last_name=%s); 
            """, (first_name, last_name))
            requested_id = cur.fetchall()[0]
            print(f"""Искомый id - {requested_id[0]}""")

        if email is not None:
            cur.execute("""
                SELECT id FROM Clients WHERE email=%s; 
            """, (email,))
            requested_id = cur.fetchall()[0]
            print(f"""Искомый id - {requested_id[0]}""")

        if phone is not None:
            cur.execute("""
                SELECT id FROM Phones WHERE phone=%s; 
            """, (phone,))
            requested_id = cur.fetchall()[0]
            print(f"""Искомый id - {requested_id[0]}""")

    return 'Функция поиска id клиента выполнена.'

with psycopg2.connect(database="db_pers_info_clients_hw_3", user="postgres", password="postgres") as conn:
    print(drop_table_db(conn))
    print(create_db(conn))

    clients_list = [
        ['Ivan', 'Ivanov', 'ii@mail.ru', '89999999999', '89999999997', '89999979997'],
        ['Petr', 'Petrov', 'pp@mail.ru', '89999999998'],
        ['Alla','Petrova', 'ap@mail.ru']
    ]

    for client in clients_list:
        if len(client) == 4:
            print(add_client(conn, client[0], client[1], client[2], client[3]))

        elif len(client) > 4:
            result = add_client(conn, client[0], client[1], client[2], client[3])
            print(result)
            position = 4
            for el in client[4:]:
                print(add_phone(conn, result, client[position]))
                position += 1

        else:
            print(add_client(conn, client[0], client[1], client[2]))

    print(change_client(conn, 2, last_name ='Sidorov'))
    print(delete_phone(conn, 1, '89999999999'))
    print(delete_client(conn, 3))

    print(view_all(conn))

    print(find_client(conn, 'Ivan', 'Ivanov'))
    print(find_client(conn, email='pp@mail.ru'))
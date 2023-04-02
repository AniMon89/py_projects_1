import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE IF EXISTS Phones;
        """)

        cur.execute("""
            DROP TABLE IF EXISTS Clients;
        """)

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
                client_id INTEGER NOT NULL REFERENCES Clients (id) ON DELETE CASCADE
            );
        """)

        conn.commit()
    return 'Таблицы Clients и Phones созданы.'

def add_client(conn, first_name:str, last_name:str, email:str, phone=None):
    with conn.cursor() as cur:

        if find_client(conn, email=email):
            return ['Внимание! Клиент с таким email уже существует.']

        else:
            cur.execute("""
                INSERT INTO Clients (first_name, last_name, email) 
                VALUES (%s, %s, %s) 
                RETURNING id;
                """,
                (first_name, last_name, email)
            )

        id = cur.fetchone()
        if phone is not None:
            function_add_phone = add_phone(conn, id, phone)
            if function_add_phone == 'Внимание! Клиент с таким телефоном уже существует.':
                conn.rollback()
                return ['Внимание! Клиента добавить не удалось из-за некорректно введённых данных.']

        conn.commit()
    return 'Клиент успешно добавлен.', id[0]

def add_phone(conn, client_id: int, phone:str):
    with conn.cursor() as cur:

        if find_client(conn, phone=phone):
            return 'Внимание! Клиент с таким телефоном уже существует.'

        cur.execute("""
        SELECT first_name, last_name from Clients
            WHERE id = %s
            """,
            (client_id,)
        )

        if not cur.fetchone():
            return 'Внимание! Такого клиента ещё не существует.'

        else:
            cur.execute("""
                INSERT INTO Phones (phone, client_id) VALUES (%s, %s);
                """,
                (phone, client_id)
             )
            conn.commit()
    return 'Функция добавления номера выполнена успешно.'


def change_client(conn, client_id: int, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:

        cur.execute("""
               SELECT first_name, last_name from Clients
                   WHERE id = %s
                   """,
                    (client_id,)
                )

        if not cur.fetchone():
            return 'Внимание! Такого клиента ещё не существует.'

        else:

            if email is not None:
                cur.execute("""
                    SELECT id from Clients
                    WHERE email = %s
                    """,
                    (email,)
                )

                if not cur.fetchone():
                    cur.execute("""
                        UPDATE Clients SET emaiL=%s WHERE id=%s;
                        """,
                        (email, client_id)
                    )
                    conn.commit()

                else:
                    return 'Внимание! Клиент с таким email уже существует. Перепроверьте данные и попробуйте снова.'

            if first_name is not None:
                cur.execute("""
                    UPDATE Clients SET first_name=%s WHERE id=%s;
                    """,
                    (first_name, client_id)
                )
                conn.commit()

            if last_name is not None:
                cur.execute("""
                    UPDATE Clients SET last_name=%s WHERE id=%s;
                """, (last_name, client_id))
            conn.commit()

    return 'Функция обновления данных о клиенте успешно выполнена.'


def delete_phone(conn, client_id: int, phone: str):
    with conn.cursor() as cur:

        cur.execute("""
            DELETE FROM Phones 
            WHERE phone=%s and client_id= %s
            RETURNING *;
            """,
            (phone, client_id)
        )

        if not cur.fetchone():
            return 'Внимание! Такого телефона ещё не существует.'

        conn.commit()
    return 'Функция удаления номера успешно выполнена.'


def delete_client(conn, client_id: int):
    with conn.cursor() as cur:

        cur.execute("""
            DELETE FROM Clients 
            WHERE id=%s
            RETURNING * ;
            """,
            (client_id,)
        )

        if not cur.fetchall():
            return 'Внимание! Такого клиента не существует.'

        conn.commit()
    return 'Функция удаления клиента успешно выполнена.'


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:

        if first_name is None:
            first_name = '%'
        if last_name is None:
            last_name = '%'
        if email is None:
            email = '%'

        client_list = [first_name, last_name, email]

        new_str = ''

        if phone is not None:
            new_str = ' AND phone = %s::text'
            client_list.append(phone)
        request = f"""
        SELECT
        email,
        first_name,
        last_name,
        CASE
            WHEN ARRAY_AGG(phone) = '{{Null}}' THEN ARRAY[]::TEXT[]
            ELSE ARRAY_AGG(phone)
        END Phones
        FROM Clients
        LEFT JOIN Phones ON Clients.id = Phones.client_id
        WHERE first_name ILIKE %s AND last_name ILIKE %s AND email ILIKE %s{new_str}
        GROUP BY email, first_name, last_name;
        """

        cur.execute(
            request,
            client_list
        )

        return cur.fetchall()
with psycopg2.connect(database="db_pers_info_clients_hw_3", user="postgres", password="postgres") as conn:

    print(create_db(conn))

    clients_list = [
        ['Ivan', 'Ivanov', 'ii@mail.ru', '89999999999', '89999999997', '89999979997'],
        ['Petr', 'Petrov', 'pp@mail.ru', '89999999998'],
        ['Alla','Petrova', 'ap@mail.ru', '89999899998']
    ]

    for client in clients_list:
        if len(client) == 4:
            print(add_client(conn, client[0], client[1], client[2], client[3])[0])

        elif len(client) > 4:
            result = add_client(conn, client[0], client[1], client[2], client[3])

            if type(result[-1]) == int:
                print(result[0])
                position = 4
                for el in client[4:]:
                    print(add_phone(conn, result[-1], client[position]))
                    position += 1

            else:
                 print('Внимание! Добавить номер(а) не получилось, так как клиент не был добавлен.')
        else:
            print(add_client(conn, client[0], client[1], client[2])[0])

    print(change_client(conn,2, last_name='Sidorov', email='ap@mail.ru'))

    print(delete_phone(conn, 1, '89999999999'))

    print(delete_client(conn, 3))

    print(find_client(conn, 'Ivan', 'Ivanov'))

    print(find_client(conn, email='pp@mail.ru'))

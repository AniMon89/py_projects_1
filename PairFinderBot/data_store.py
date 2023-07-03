import psycopg2


class BotDB:
    def __init__(self):
        with open('password_postgres.txt', 'r') as file_object:
            password_postgres = file_object.read().strip()

        self.conn = psycopg2.connect(database='PairFinderBotDB', user='postgres', password=password_postgres)

    def close(self):
        try:
            self.conn.close()
        except psycopg2.InterfaceError:
            pass

    def drop_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                        DROP TABLE IF EXISTS Viewed;
                    """)
            cur.execute("""
                        DROP TABLE IF EXISTS Liked;
                    """)
            cur.execute("""
                DROP TABLE IF EXISTS Profiles;
            """)

            cur.execute("""
                DROP TABLE IF EXISTS Worksheets;
            """)

            self.conn.commit()
        return 'Функция drop_db выполнена.'

    def create_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Profiles (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL UNIQUE 
                );
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS Worksheets (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR (40) NOT NULL,
                    user_id INTEGER NOT NULL UNIQUE
                );
            """)

            cur.execute("""
                        CREATE TABLE IF NOT EXISTS Viewed (
                            profile_id INTEGER REFERENCES Profiles (id),
                            worksheet_id INTEGER REFERENCES Worksheets (id),
                            CONSTRAINT pk_viewed PRIMARY KEY (profile_id,worksheet_id)
                        );
                    """)

            cur.execute("""
                        CREATE TABLE IF NOT EXISTS Liked (
                            profile_id INTEGER REFERENCES Profiles (id),
                            worksheet_id INTEGER REFERENCES Worksheets (id),
                            CONSTRAINT pk_liked PRIMARY KEY (profile_id, worksheet_id)
                        );
                    """)

            self.conn.commit()
        return 'Функция create_db выполнена.'

    def add_profile(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                       SELECT id
                       FROM Profiles
                       WHERE  user_id = %s
                       """,
                        (user_id,)
                        )
            id_profile = cur.fetchone()
            if not id_profile:
                cur.execute("""
                           INSERT INTO Profiles (user_id) 
                           VALUES (%s) 
                           RETURNING id;
                           """,
                            (user_id,)
                            )
                identifier = cur.fetchone()[0]
                self.conn.commit()
                return identifier

            else:
                # self.close()
                return id_profile[0]

    def add_worksheet(self, name, user_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                       SELECT id
                       FROM Worksheets
                       WHERE name = %s and user_id = %s
                       """,
                        (name, user_id,)
                        )
            id_worksheet = cur.fetchone()
            if not id_worksheet:
                cur.execute("""
                           INSERT INTO Worksheets (name, user_id) 
                           VALUES (%s, %s) 
                           RETURNING id;
                           """,
                            (name, user_id,)
                            )
                identifier = cur.fetchone()[0]
                self.conn.commit()
                return identifier

            else:
                return id_worksheet[0]

    def add_viewed(self, profile_id, worksheet_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                        SELECT worksheet_id
                        FROM Viewed
                        WHERE profile_id = %s
                        """,
                        (profile_id,)
                        )
            list_worksheets = cur.fetchall()

            if (worksheet_id,) in list_worksheets:
                return 'Данные анкеты для данного пользователя были уже ранее добавленны.'

            else:
                cur.execute("""
                            INSERT INTO Viewed (profile_id, worksheet_id) 
                            VALUES (%s, %s);
                            """,
                            (profile_id, worksheet_id,)
                            )

                self.conn.commit()
                return 'Данные анкеты для данные пользователя были успешно добавленны.'

    def add_liked(self, profile_id, worksheet_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                        SELECT worksheet_id
                        FROM Liked
                        WHERE profile_id = %s
                        """,
                        (profile_id,)
                        )
            list_worksheets = cur.fetchall()

            if (worksheet_id,) in list_worksheets:
                return 'Данные анкеты для данного пользователя были уже ранее добавленны.'

            else:
                cur.execute("""
                            INSERT INTO Liked (profile_id, worksheet_id) 
                            VALUES (%s, %s);
                            """,
                            (profile_id, worksheet_id,)
                            )

                self.conn.commit()
                return 'Данные анкеты для данного пользователя были успешно добавленны.'

    def get_liked(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                        SELECT
                            Worksheets.name,
                            Worksheets.user_id
                        FROM 
                            Profiles
                        INNER JOIN Liked ON Liked.profile_id = Profiles.id 
                        INNER JOIN Worksheets ON Liked.worksheet_id = Worksheets.id
                        WHERE Profiles.user_id = %s;
                        """,
                        (user_id,)
                        )
            list_liked_worksheets = cur.fetchall()
            if list_liked_worksheets:
                return list_liked_worksheets
            else:
                return False

    def get_worksheet(self, user_id, worksheet_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                        SELECT
                            Worksheets.user_id
                        FROM 
                            Profiles
                        INNER JOIN Viewed ON Viewed.profile_id = Profiles.id 
                        INNER JOIN Worksheets ON Viewed.worksheet_id = Worksheets.id
                        WHERE Profiles.user_id = %s;
                        """,
                        (user_id,)
                        )
            list_viewed_worksheets = cur.fetchall()
            if list_viewed_worksheets:
                if (worksheet_id,) in list_viewed_worksheets:
                    return True
                else:
                    return False
            else:
                return False
            

if __name__ == '__main__':
    pair_finder_bot_db = BotDB()
    print(pair_finder_bot_db.drop_db())
    print(pair_finder_bot_db.create_db())
    pair_finder_bot_db.close()

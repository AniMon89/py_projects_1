import psycopg2

def drop_db(conn):
    with conn.cursor() as cur:

        cur.execute("""
            DROP TABLE IF EXISTS TracksCollections;
        """)

        cur.execute("""
            DROP TABLE IF EXISTS ArtistsAlbums;
        """)

        cur.execute("""
            DROP TABLE IF EXISTS GenresArtists;
        """)

        cur.execute("""
            DROP TABLE IF EXISTS Collections;
        """)

        cur.execute("""
            DROP TABLE IF EXISTS Tracks;
        """)

        cur.execute("""
            DROP TABLE IF EXISTS Albums;
        """)

        cur.execute("""
            DROP TABLE IF EXISTS Genres;
        """)

        cur.execute("""
            DROP TABLE IF EXISTS Artists;
        """)

        conn.commit()

    return 'Функция drop_db выполнена.'

def create_db(conn):
    with conn.cursor() as cur:

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Genres (
	            id SERIAL PRIMARY KEY,
	            genre_name VARCHAR(60) NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Artists (
	            id SERIAL PRIMARY KEY,
	            artist_name VARCHAR(60) NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS GenresArtists (
	            genre_id INTEGER REFERENCES Genres (id),
	            artist_id INTEGER REFERENCES Artists (id),
	            CONSTRAINT pk_ga PRIMARY KEY (genre_id, artist_id)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Albums (
	            id SERIAL PRIMARY KEY,
	            album_title VARCHAR(60) NOT NULL,
	            album_year INTEGER NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ArtistsAlbums (
	            artist_id INTEGER REFERENCES Artists (id),
	            album_id INTEGER REFERENCES Albums (id),
	            CONSTRAINT pk_aa PRIMARY KEY (artist_id,album_id)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Tracks (
	            id SERIAL PRIMARY KEY,
	            track_name VARCHAR(60) NOT NULL,
	            duration_minutes FLOAT NOT NULL,
	            album_id INTEGER NOT NULL REFERENCES Albums (id)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Collections (
	            id SERIAL PRIMARY KEY,
	            collection_name VARCHAR(60) NOT NULL,
	            collection_year INTEGER NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS TracksCollections (
	            track_id INTEGER REFERENCES Tracks (id),
	            collection_id INTEGER REFERENCES Collections (id),
	            CONSTRAINT pk_tc PRIMARY KEY (track_id,collection_id)
            );
        """)

        conn.commit()
    return 'Функция create_db выполнена.'

def add_genre(conn, genre_name):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id
            FROM Genres
            WHERE genre_name = %s
            """,
            (genre_name,)
            )
        id_genre = cur.fetchone()
        if not id_genre:
            cur.execute("""
                INSERT INTO Genres (genre_name) 
                VALUES (%s) 
                RETURNING id;
                """,
                (genre_name,)
                )
            id = cur.fetchone()[0]
            conn.commit()
            return id

        else:
            return id_genre[0]


def add_artist(conn, artist_name):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id
            FROM Artists
            WHERE artist_name = %s
            """,
            (artist_name,)
            )

        if not cur.fetchone():
            cur.execute("""
                INSERT INTO Artists (artist_name) 
                VALUES (%s) 
                RETURNING id;
                """,
                (artist_name,)
                )
            id = cur.fetchone()[0]
            conn.commit()
            return id
        else:
            return 'Такой исполнитель уже существует.'

def add_conn_genre_artist(conn, genre_id, artist_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT genre_id
            FROM GenresArtists
            WHERE artist_id = %s
            """,
            (artist_id,)
            )
        list_genres = cur.fetchall()

        if list_genres and (genre_id,) in list_genres:
            return 'Связь между артистом и жанром уже была создана.'

        else:
            cur.execute("""
                INSERT INTO GenresArtists (genre_id, artist_id) 
                VALUES (%s, %s);
                """,
                (genre_id, artist_id,)
                )

            conn.commit()
            return 'Связь между артистом и жанром успешно создана.'

def add_album(conn, album_title, album_year):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id
            FROM Albums
            WHERE album_title = %s AND album_year = %s;
            """,
            (album_title, album_year,)
            )
        id_album = cur.fetchone()
        if not id_album:
            cur.execute("""
                INSERT INTO Albums (album_title, album_year) 
                VALUES (%s, %s) 
                RETURNING id;
                """,
                (album_title, album_year,)
                )
            id = cur.fetchone()[0]
            conn.commit()
            return id
        else:
            return id_album[0]

def add_conn_artist_album(conn, artist_id, album_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT album_id
            FROM ArtistsAlbums
            WHERE artist_id = %s
            """,
            (artist_id,)
            )
        list_albums = cur.fetchall()

        if list_albums and (album_id,) in list_albums:
            return 'Связь между артистом и альбомом уже была создана.'

        else:
            cur.execute("""
                INSERT INTO ArtistsAlbums (artist_id, album_id) 
                VALUES (%s, %s);
                """,
                (artist_id, album_id,)
                )

            conn.commit()
            return 'Связь между артистом и альбомом успешно создана.'

def add_track(conn, track_name, duration_minutes, album_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id
            FROM Tracks
            WHERE track_name = %s AND duration_minutes = %s AND album_id = %s;
            """,
            (track_name, duration_minutes, album_id,)
            )
        id_track = cur.fetchone()
        if not id_track:
            cur.execute("""
                INSERT INTO Tracks (track_name, duration_minutes, album_id) 
                VALUES (%s, %s, %s) 
                RETURNING id;
                """,
                (track_name, duration_minutes, album_id,)
                )
            id = cur.fetchone()[0]
            conn.commit()
            return id

        else:
            return id_track[0]

def add_collection(conn, collection_name, collection_year):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id
            FROM Collections
            WHERE collection_name = %s AND collection_year = %s;
            """,
            (collection_name, collection_year,)
            )
        id_collection = cur.fetchone()
        if not id_collection:
            cur.execute("""
                INSERT INTO Collections (collection_name, collection_year) 
                VALUES (%s, %s) 
                RETURNING id;
                """,
                (collection_name, collection_year,)
                )
            id = cur.fetchone()[0]
            conn.commit()
            return id

        else:
            return id_collection[0]

def add_conn_track_collection(conn, track_id, collection_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT collection_id
            FROM TracksCollections
            WHERE track_id = %s
            """,
            (track_id,)
            )
        list_collections = cur.fetchall()

        if list_collections and (collection_id,) in list_collections:
            return 'Связь между треком и сборником уже была создана.'

        else:
            cur.execute("""
                INSERT INTO TracksCollections (track_id, collection_id) 
                VALUES (%s, %s);
                """,
                (track_id, collection_id,)
                )

            conn.commit()
            return 'Связь между треком и сборником успешно создана.'


with psycopg2.connect(database='DB_homework_2', user='postgres', password='HK87jgdddkl579') as conn:

    list_music = [
        ['Imagine Dragons',
            ['поп-рок', 'альтернативный рок', 'инди-поп', 'электропоп', 'инди-рок', 'синти-поп'],
            [['Evolve', 2017,
                ['Believer', 3.38, ['She Playing Hella Hard', 2021], ['Hits Of All Time', 2021], ['10`s Best Of', 2021]]
            ],
             ['Night Visions', 2013,
                ['Demons', 2.95, ['Hits Of All Time', 2021]]
            ]
            ]
        ],
        ['Rixton',
            ['Поп', 'R&B', 'поп-рок'],
            [['Let The Road', 2014,
                ['Me and my broken heart', 3.22, ['Throwback Hits', 2020]]
            ]
            ]
        ],
        ['Maroon 5',
            ['поп-рок', 'фанк-рок', 'голубоглазый соул', 'софт-рок', 'неосоул', 'данс-поп', 'альтернативный рок'],
            [['JORDI', 2021,
                ['Memories', 3.15, ['Hits 2020', 2020], ['Hits Of All Time', 2021]]
            ],
             ['Singles', 2015,
                ['Payphone', 3.87, ['10`s Best Of', 2021], ['Hits Of All Time', 2021]],
                ['This love', 3.42, ['She Playing Hella Hard', 2021]],
                ['Sugar', 3.88, ['Hits Of All Time', 2021]],
                ['Animals', 3.83, ['Hits Of All Time', 2021]]
             ],
             ['Songs about Jane', 2002,
                 ['Sunday morning', 4.05, ['2021 Mega Hits', 2021]]
             ]
            ]
        ],
        ['Wiz Khalifa',
            ['хип-хоп'],
            [['Singles', 2015,
                ['Payphone', 3.87, ['10`s Best Of', 2021]]
            ]
            ]
        ],
        ['Camila Cabello',
            ['поп', 'R&B', 'латино'],
            [['The Shawn Mendes foundation playlist', 2020,
                ['Senorita', 3.18, ['10`s Best Of', 2021]]
            ]
            ]
        ],
        ['Shawn Mendes',
            ['поп', 'фолк-поп', 'поп-рок'],
            [['The Shawn Mendes foundation playlist', 2020,
                ['Senorita', 3.18, ['10`s Best Of', 2021]]
            ],
             ['Shawn Mendes', 2018,
                 ['Lost in Japan', 3.35, ['2021 Mega Hits', 2021]]
             ]
            ]

        ],
        ['One Republic',
            ['поп-рок', 'поп', 'альтернативный рок'],
            [['Human', 2021,
                ['Rescue me', 2.65, ['Best Clean Hits', 2021]]
            ],
            ['Dreaming Out Loud', 2007,
                ['Apologize', 3.47, ['2021 Mega Hits', 2021]]
            ]
            ]
        ],
        ['Thirty Seconds to Mars',
            ['альтернативный рок', 'хард-рок'],
            [['AMERICA', 2018,
                ['Walk on water', 3.08, ['10`s Best Of', 2021]],
                ['From yesterday', 4.12, ['Rock Hits', 2022]]
            ],
            ['A Beautiful Lie', 2005,
                ['The kill (bury me)', 3.87, ['Rock Now', 2020], ['Rock Hits', 2022]]
            ]
            ]
        ],
        ['Panic! At The Disco',
            ['поп-рок', 'поп-панк', 'джаз-фьюжн', 'барокко-поп', 'альтернативный рок', 'дэнс-рок', 'эмо-поп', 'синти-панк', 'поп'],
            [['Pray for The Wicked', 2018,
                ['High hopes', 3.2, ['100 Greatest 10s: The Best Songs of Last Decade', 2019]]
            ]
            ]
        ]
    ]

    print(drop_db(conn))
    print(create_db(conn))

    for artis in list_music:
        art = add_artist(conn, artis[0])
        print(art)
        for i in range(len(artis[1])):
            gen = add_genre(conn, artis[1][i])
            print(gen)
            if type(art) == int:
                print(add_conn_genre_artist(conn, gen, art))
        for al in artis[2]:
            alb = add_album(conn, al[0], al[1])
            print(alb)
            if type(art) == int:
                print(add_conn_artist_album(conn, art, alb))
            for tr in al[2:]:
                trc = add_track(conn, tr[0], tr[1], alb)
                print(trc)
                for c in tr[2:]:
                    col = add_collection(conn, c[0], c[1])
                    print(col)
                    print(add_conn_track_collection(conn, trc, col))





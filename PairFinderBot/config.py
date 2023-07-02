with open('community_token.txt', 'r') as file_object:
    community_token = file_object.read().strip()

with open('access_token.txt', 'r') as file_object:
    access_token = file_object.read().strip()

db_url_object = "postgresql+psycopg2://student:student@localhost/student_diplom"

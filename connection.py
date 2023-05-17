import urllib

from cryptography.fernet import Fernet
from sqlalchemy import create_engine

def decrypt():
    key =b'tNsks1dfIttOKmLbHphIWKzfDaLqYSGs8quEA4LSS4s='
    encrypted_password=b'gAAAAABkB2xmPCjwojs1_LDvve89CFmuRak1dO7Ec5tdv8qBGiaMgLzVA4xN6GUbtnB_upzoX9IUIEnl2ggqAQxZghh4CCCUPQ=='
    fernet=Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password)
    return decrypted_password.decode()

dbpw=decrypt()
def get_db_connection():
    encoded_password = urllib.parse.quote(dbpw, safe='')
    connection_string = f"postgresql://postgres:{encoded_password}@localhost:5432/GPA"
    engine=create_engine(connection_string)
    conn=engine.connect()
    # conn = psycopg2.connect(
    #     host="localhost",
    #     database="GPA",
    #     user="postgres",
    #     password=dbpw
    # )

    return conn


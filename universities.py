import psycopg2
import pandas as pd
from connection import get_db_connection

def universityList(country):
    try:
        conn = get_db_connection()
        query = "select distinct(university_name) from universities u inner join countries c on" \
                " u.country_id=c.country_id where c.country_name = %s"
        print("country is ",country)
        values=(country,)
        df = pd.read_sql_query(query,conn,params=values)
        return df.reset_index(drop=True) if not df.empty else None

    except(Exception ,psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.close()
        # engine.dispose()
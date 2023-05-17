import psycopg2
import pandas as pd
from connection import get_db_connection

def countries_list():
    # return df2.reset_index(drop=True) if not df2.empty else None
    try:
        conn = get_db_connection()
        query = "select country_name from countries"
        df = pd.read_sql_query(query,conn)
        print(df)

        return df.reset_index(drop=True) if not df.empty else None

    except(Exception ,psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.close()
        # engine.dispose()
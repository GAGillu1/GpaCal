import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

from connection import get_db_connection
from sqlalchemy import create_engine

def slate_log(slateid,scale,gpa):
    try:
        conn = get_db_connection()
        query = "INSERT INTO slatelog(slateid, universityscale, gpa)	VALUES (%s, %s, %s) "
        values = (slateid, scale, gpa)
        #cur.execute(query)
        #print(cur.query)
        conn.execute(query, values)

        #df = pd.read_sql_query(query, conn,params=values)

        #
        # return df.reset_index(drop=True) if not df.empty else None

    except(Exception, SQLAlchemyError) as error:
        print(error)
    finally:
        conn.close()

slate_log(8978 ,'Anna University Coimbatore', 3.57)
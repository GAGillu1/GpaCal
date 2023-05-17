import psycopg2
import pandas as pd
from connection import get_db_connection


def slatelog():
    try:
        conn = get_db_connection()
        df=pd.read_excel('slate.xlsx')

        #hallticket=df['HallTicket']
        cur = conn.cursor()
        print(1)
        for i in range(0,len(df)):
            print(2)
            id = int(df.iloc[i]['SlateID'])
            uni = str(df.iloc[i]['University/Scale Used'])
            gpa = float(df.iloc[i]['GPA'])
            print(3)
            query = "Insert into slatelog(slateId,universityscale,GPA) values(%s,%s,%s)"
            print(4)
            values=(id,uni,gpa)
            print(5)
            cur.execute(query, values)
            print(6)
            conn.commit()






    except(Exception ,psycopg2.DatabaseError) as error:
        print(error)

    finally:
        cur.close()
        conn.close()
        # engine.dispose()



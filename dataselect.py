import psycopg2
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine


def selectdata(university,country):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="GPA",
            user="postgres",
            password="Ap26ae3726@123"
        )
        cur = conn.cursor()
        query = "SELECT u.university_name, t.grade, t.scales, t.usgrade FROM countries c INNER JOIN universities u ON c.country_id = u.country_id INNER JOIN caltab t ON u.uid = t.university_id WHERE c.country_name =%s AND u.university_name = %s"
        values = (university,country)


        cur.execute(query, values)
        print(cur.query)
        df = pd.read_sql_query(query,conn, params=values)
        print(df)
        #
        # engine = create_engine('postgresql://postgres:@localhost:5432/GPA')
        #
        # query = "SELECT c.country_name, u.university_name, t.grade, t.scales, t.usgrade \
        #          FROM countries c \
        #          INNER JOIN universities u ON c.country_id = u.country_id \
        #          INNER JOIN caltab t ON u.uid = t.university_id \
        #          WHERE c.country_name = %s AND u.university_name = %s"
        #
        # params = (country, university)
        #
        # with engine.connect() as conn:
        #     df = pd.read_sql_query(query, con=conn, params=params)
        # print(df)

    except(Exception ,psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
        # engine.dispose()



country='India'
university='Anna University'

selectdata(country,university)
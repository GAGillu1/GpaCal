import psycopg2
import pandas as pd
from connection import get_db_connection


def filtered_scale(country, university):
    # df2 = df[(df['Country'] == country) & (df['University'] == university)]
    # logger.debug(df2)
    # return df2.reset_index(drop=True) if not df2.empty else None
    try:
        conn = get_db_connection()
        query = "SELECT u.university_name, t.grade, t.scales, t.usgrade FROM countries c INNER JOIN universities u ON c.country_id = u.country_id INNER JOIN caltab t ON u.uid = t.university_id WHERE c.country_name =%s AND u.university_name = %s"
        values = (country,university)
        df = pd.read_sql_query(query,conn, params=values)
        print(df)
        return df.reset_index(drop=True) if not df.empty else None
        #
        # engine = create_engine('postgresql://postgres:@localhost:5432/GPA')
        #
        # query = "SELECT c.country_n ame, u.university_name, t.grade, t.scales, t.usgrade \
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
        conn.close()
        # engine.dispose()


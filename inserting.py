import pandas as pd
import psycopg2


conn = psycopg2.connect(
    host="localhost",
    database="GPA",
    user="postgres",
    password="Ap26ae3726@123"
)

# df=pd.read_excel("universities.xlsx")
# with conn.cursor() as cur:
#     for index, row in df.iterrows():
#         print(row['university_name'])
#         cur.execute("INSERT INTO universities (university_name, country_id) VALUES (%s,%s)",
#                     (row['university_name'],row['country_id']))
#
#     conn.commit()
#
# # close the cursor and connection
# cur.close()
# conn.close()


df=pd.read_excel(r"cal_insertion.xlsx")
with conn.cursor() as cur:
    for index,row in df.iterrows():
        print(row['University'])
        cur.execute("INSERT INTO caltab (university_id, grade, scales, usgrade, status) VALUES (%s, %s, %s, %s, %s)",
                    (row['University'],row['Grade'],row['Scale'],row['US Grade'],'Y'))
        #print(cur.query)
        conn.commit()

# df=pd.read_excel("Count.xlsx")
# with conn.cursor() as cur:
#     for index,row in df.iterrows():
#         cur.execute("INSERT INTO countries (country_id, country_name) VALUES (%s, %s)",
#                     (row['ID'],row['Country']))
#         #print(cur.query)
#         conn.commit()

cur.close()
conn.close()


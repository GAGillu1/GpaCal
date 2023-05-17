import psycopg2
import pandas as pd

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="GPA",
    user="postgres",
    password="Ap26ae3726@123"
)

# Execute SELECT query and save result to a pandas dataframe
df = pd.read_sql_query("SELECT * FROM universities", conn)

# Save dataframe to an Excel file
df.to_excel("D:/Enr/universities.xlsx",index=False)

# Close database connection
conn.close()

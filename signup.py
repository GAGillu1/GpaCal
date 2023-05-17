import bcrypt
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="GPA",
    user="postgres",
    password=""
)

# Get the username and password from the user
username = input("Enter a username: ")
password = input("Enter a password: ")

# Hash the password with bcrypt
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

query="INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password)


print("User created successfully")

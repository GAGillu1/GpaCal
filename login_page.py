import bcrypt
from flask import Flask, render_template, session, redirect, request
#
# # Hash a password
# password = b"mypassword"
# salt = bcrypt.gensalt()
# hashed_password = bcrypt.hashpw(password, salt)
# print(hashed_password)
#
# # Verify a password
# password_to_check = b"mypassword"
# if bcrypt.checkpw(password_to_check, hashed_password):
#     print("Password matched")
# else:
#     print("Password did not match")
import os
cwd = os.getcwd()

app = Flask(__name__, template_folder=cwd)


@app.route('/loginpage',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(------('index'))
    return

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(----('index'))





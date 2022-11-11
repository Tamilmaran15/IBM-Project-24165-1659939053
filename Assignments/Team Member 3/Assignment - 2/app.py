from flask import Flask
from flask import request, redirect, url_for, render_template
import ibm_db

app = Flask(__name__)
app.config['DEBUG'] = True
db_connection = ibm_db.connect(
    "DATABASE=bludb;QUERYTIMEOUT=1;CONNECTTIMEOUT=10;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=./DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=tmd97608;PWD=gIHgu7Xf3D3sEjCd", "", "")


@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        sql_query = f"INSERT INTO User (username, email, roll_no, password) VALUES('{data['username']}', '{data['email']}', '{data['roll_no']}', '{data['password']}')"
        ibm_db.exec_immediate(db_connection, sql_query)
        return redirect(url_for("login"))
    if request.method == "GET":
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        sql_query = f"SELECT password from User WHERE username = '{data['username']}'"
        result = ibm_db.exec_immediate(db_connection, sql_query)
        value = ibm_db.fetch_tuple(result)
        if value[0] == data["password"]:
            return redirect(url_for("welcome"))
        else:
            return "<p style=color:red;>Invalid Credentials</p>"
    if request.method == "GET":
        return render_template("signin.html")


@app.route("/welcome", methods=["GET"])
def welcome():
    return "<h1 style=color:green;>Welcome!!!!!</h1>"

if __name__ == '__main__':
    app.run()
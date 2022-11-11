from flask import Flask
from flask import request, redirect, url_for, render_template
import ibm_db

app = Flask(__name__)
app.config['DEBUG'] = True
db_connection = ibm_db.connect(
    "DATABASE=bludb;QUERYTIMEOUT=1;CONNECTTIMEOUT=10;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;SECURITY=SSL;SSLServerCertificate=./DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=sxg37729;PWD=zyC2lEpY0GuQiGZP", "", "")


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
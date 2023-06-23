from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL
import os
from train_main import train_main

app = Flask(__name__)
mysql = None
user_dir = "users"


def init_app(app, dat_name):
    host = ""
    user = ""
    password = ""
    db = ""
    with open(dat_name, "r") as f:
        for line in f:
            if line.startswith("host"):
                host = line.split(":")[1].strip()
            elif line.startswith("user"):
                user = line.split(":")[1].strip()
            elif line.startswith("password"):
                password = line.split(":")[1].strip()
            elif line.startswith("db"):
                db = line.split(":")[1].strip()
            else:
                raise Exception("Invalid dat file format")

        app.config["MYSQL_HOST"] = host
        app.config["MYSQL_USER"] = user
        app.config["MYSQL_PASSWORD"] = password
        app.config["MYSQL_DB"] = db
        mysql = MySQL(app)

    return app, mysql


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]

    cur = mysql.connection.cursor()
    cur.execute("START TRANSACTION")
    try:
        cur.execute("SELECT * FROM users WHERE username = %s FOR UPDATE", (username,))
        existing_user = cur.fetchone()
        if existing_user:
            cur.execute("ROLLBACK")
            cur.close()
            return render_template(
                "login.html",
                error_message="Username already exists. Please choose a different username.",
            )

        cur.execute(
            "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
            (name, username, password),
        )
        cur.execute("COMMIT")
    except Exception as e:
        cur.execute("ROLLBACK")
        print(str(e))
    finally:
        cur.close()

    return redirect("/")


@app.route("/signin", methods=["POST"])
def signin():
    username = request.form["username"]
    password = request.form["password"]

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    if user and user[3] == password:
        session["user_id"] = user[0]
        session["username"] = user[1]
        # get folder name in data forlder
        dir_list = os.listdir("data")
        # check if dir_list has a entry name ".DS_Store"
        if ".DS_Store" in dir_list:
            dir_list.remove(".DS_Store")

        return render_template(
            "submit_code.html", user_name=session["username"], datasets=dir_list
        )
    else:
        error_message = "Invalid username or password"
        return render_template("login.html", error_message=error_message)


@app.route("/submit_code", methods=["POST"])
def submit_code():
    model_code = request.form["modelcode"]
    precode = request.form["precode"]
    data_name = request.form["dataset"]
    user_name = session["username"]
    user_sav_dir = os.path.join(user_dir, data_name, user_name)
    # Check directory "user_name" exists
    # If not, create directory "user_name"
    if not os.path.exists(user_sav_dir):
        os.makedirs(user_sav_dir)
    # Write model_code to file "user_name/model.py"
    if os.path.exists(user_sav_dir + "/model.py"):
        os.remove(user_sav_dir + "/model.py")
    with open(user_sav_dir + "/model.py", "w") as f:
        f.write(model_code)
    # Write precode to file "user_name/precode.py"
    if precode != "":
        if os.path.exists(user_sav_dir + "/precode.py"):
            os.remove(user_sav_dir + "/precode.py")
        with open(user_sav_dir + "/precode.py", "w") as f:
            f.write(precode)
    # Run train_main.py
    acc = 0
    if precode == "":
        acc = train_main(model_path=user_name + "/model.py", data_name=data_name)
    else:
        acc = train_main(
            model_path=user_name + "/model.py",
            preproc_path=user_name + "/precode.py",
            data_name=data_name,
        )

    user_id = session["user_id"]
    cur = mysql.connection.cursor()
    cur.execute("START TRANSACTION")
    try:
        cur.execute(
            "INSERT INTO performance (user_id, data_name, accuracy) VALUES (%s, %s, %s)",
            (user_id, data_name, acc),
        )
        cur.execute("COMMIT")
    except Exception as e:
        cur.execute("ROLLBACK")
        error_message = "Error in submitting code"
        return render_template("submit_code.html", error_message=error_message)

    finally:
        cur.close()

    return redirect("/")


@app.route("/delete_code", methods=["POST"])
def delete_code():
    user_name = session["deleteName"]
    data_name = request.form["deleteDataset"]
    user_sav_dir = os.path.join(user_dir, data_name, user_name)
    # Check directory "user_name" exists
    if os.path.exists(user_sav_dir + "/model.py"):
        os.remove(user_sav_dir + "/model.py")
    # Write precode to file "user_name/precode.py"
    if os.path.exists(user_sav_dir + "/precode.py"):
        os.remove(user_sav_dir + "/precode.py")

    return redirect("/")


if __name__ == "__main__":
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    app.secret_key = "super secret key"
    app.config["SESSION_TYPE"] = "filesystem"
    app, mysql = init_app(app, "auth.dat")
    app.run()

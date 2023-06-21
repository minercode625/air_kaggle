from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = None


def init_app(app, dat_name):
    # Init from dat file
    # dat file config:
    # host: localhost
    # user: root
    # password: password
    # db: db_name
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
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cur.fetchone()
    if existing_user:
        cur.close()
        return render_template(
            "login.html",
            error_message="Username already exists. Please choose a different username.",
        )

    cur.execute(
        "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
        (name, username, password),
    )
    mysql.connection.commit()
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
        return redirect("/submit_code")
    else:
        error_message = "Invalid username or password"
        return render_template("login.html", error_message=error_message)


@app.route("/submit_code")
def submit_code():
    if "user_id" in session:
        return render_template("submit_code.html")
    else:
        return redirect("/")


if __name__ == "__main__":
    app.secret_key = "super secret key"
    app.config["SESSION_TYPE"] = "filesystem"
    app, mysql = init_app(app, "auth.dat")
    app.run()

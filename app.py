from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

# SECRET KEY

app.secret_key = "megacoat123"

# LOGIN USERNAME & PASSWORD

USERNAME = "admin"
PASSWORD = "1234"

# HOME PAGE

@app.route("/", methods=["GET", "POST"])
def index():

    conn = sqlite3.connect("pistonrod.db")
    cur = conn.cursor()

    results = []

    if request.method == "POST":

        search = request.form["search"]

        cur.execute("""

        SELECT * FROM pistonrod

        WHERE
        part_no LIKE ?
        OR application LIKE ?
        OR plant LIKE ?

        """, ('%' + search + '%',
              '%' + search + '%',
              '%' + search + '%'))

        results = cur.fetchall()

    conn.close()

    return render_template(
        "index.html",
        results=results,
        logged_in=session.get("logged_in")
    )

# LOGIN PAGE

@app.route("/login", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:

            session["logged_in"] = True

            return redirect("/")

        else:

            error = "Invalid Username or Password"

    return render_template("login.html", error=error)

# LOGOUT

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# ADD PART

@app.route("/add", methods=["GET", "POST"])
def add():

    if not session.get("logged_in"):
        return redirect("/login")

    if request.method == "POST":

        data = (
            request.form["sr_no"],
            request.form["part_no"],
            request.form["rev_date"],
            request.form["application"],
            request.form["total_length"],
            request.form["plating_length"],
            request.form["chrome_before"],
            request.form["chrome_after"],
            request.form["nickel"],
            request.form["piston_end"],
            request.form["plant"],
            request.form["identification"]
        )

        conn = sqlite3.connect("pistonrod.db")
        cur = conn.cursor()

        cur.execute("""

        INSERT INTO pistonrod
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)

        """, data)

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")

# DELETE PART

@app.route("/delete/<part_no>")
def delete(part_no):

    if not session.get("logged_in"):
        return redirect("/login")

    conn = sqlite3.connect("pistonrod.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM pistonrod WHERE part_no=?", (part_no,))

    conn.commit()
    conn.close()

    return redirect("/")

# EDIT PART

@app.route("/edit/<part_no>", methods=["GET", "POST"])
def edit(part_no):

    if not session.get("logged_in"):
        return redirect("/login")

    conn = sqlite3.connect("pistonrod.db")
    cur = conn.cursor()

    if request.method == "POST":

        data = (
            request.form["rev_date"],
            request.form["application"],
            request.form["total_length"],
            request.form["plating_length"],
            request.form["chrome_before"],
            request.form["chrome_after"],
            request.form["nickel"],
            request.form["piston_end"],
            request.form["plant"],
            request.form["identification"],
            part_no
        )

        cur.execute("""

        UPDATE pistonrod

        SET
        rev_date=?,
        application=?,
        total_length=?,
        plating_length=?,
        chrome_before=?,
        chrome_after=?,
        nickel=?,
        piston_end=?,
        plant=?,
        identification=?

        WHERE part_no=?

        """, data)

        conn.commit()
        conn.close()

        return redirect("/")

    cur.execute("SELECT * FROM pistonrod WHERE part_no=?", (part_no,))
    row = cur.fetchone()

    conn.close()

    return render_template("edit.html", row=row)

if __name__ == "__main__":
    app.run(debug=True)
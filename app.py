from flask import Flask, render_template, request, redirect, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "megacoat123"

USERNAME = "admin"
PASSWORD = "1234"
EXCEL_FILE = "rods.xlsx"


def load_data():
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = df.fillna("")
        return df

    return pd.DataFrame()


@app.route("/", methods=["GET", "POST"])
def index():
    df = load_data()
    results = []

    if request.method == "POST":
        search = request.form["search"].strip()

        results = df[
            df.astype(str).apply(
                lambda row: row.str.contains(search, case=False, na=False).any(),
                axis=1
            )
        ].values.tolist()

    return render_template(
        "index.html",
        results=results,
        logged_in=session.get("logged_in")
    )


@app.route("/check")
def check():
    if not os.path.exists(EXCEL_FILE):
        return "ERROR: rods.xlsx file not found on server"

    df = load_data()
    return f"Excel found. Total rows: {len(df)} Columns: {list(df.columns)}"


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


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/add")
def add():
    if not session.get("logged_in"):
        return redirect("/login")

    return "Add/Edit/Delete is temporarily disabled because Excel is the main data source."


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "megacoat123"

USERNAME = "admin"
PASSWORD = "1234"
EXCEL_FILE = "rods.xlsx"

def load_data():
    if not os.path.exists(EXCEL_FILE):
        return pd.DataFrame()

    df = pd.read_excel(EXCEL_FILE)
    df = df.fillna("")
    return df

@app.route("/", methods=["GET", "POST"])
def index():
    df = load_data()
    results = []

    if request.method == "POST":
        search = request.form["search"].strip()

        if search:
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
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect("/")
        else:
            error = "Invalid Username or Password"

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, session, send_from_directory
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "megacoat123"

USERNAME = "admin"
PASSWORD = "1234"

PART_FILE = "rods.xlsx"
REJECTION_FILE = "rejection_data.xlsx"


def load_parts():
    if os.path.exists(PART_FILE):
        df = pd.read_excel(PART_FILE)
        df = df.fillna("")
        return df
    return pd.DataFrame()


@app.route("/", methods=["GET", "POST"])
def index():
    df = load_parts()
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


@app.route("/daily_rejection")
def daily_rejection():
    if not os.path.exists(REJECTION_FILE):
        return "rejection_data.xlsx file not found"

    df = pd.read_excel(
        REJECTION_FILE,
        sheet_name="May-2026 Report",
        header=None
    )

    rejection_row_index = df[df.apply(
        lambda row: row.astype(str).str.strip().eq("Rejection Qty").any(),
        axis=1
    )].index[0]

    rework_row_index = df[df.apply(
        lambda row: row.astype(str).str.strip().eq("Rework Qty").any(),
        axis=1
    )].index[0]

    dates = []
    rejection_qty = []
    rework_qty = []

    for col in range(df.shape[1]):
        date_value = df.iloc[1, col]
        parsed_date = pd.to_datetime(date_value, errors="coerce")

        if pd.notna(parsed_date):
            dates.append(parsed_date.strftime("%d-%m"))

            rejection_value = df.iloc[rejection_row_index, col]
            rework_value = df.iloc[rework_row_index, col]

            rejection_qty.append(0 if pd.isna(rejection_value) else float(rejection_value))
            rework_qty.append(0 if pd.isna(rework_value) else float(rework_value))

    return render_template(
        "daily_rejection.html",
        dates=dates,
        rejection_qty=rejection_qty,
        rework_qty=rework_qty
    )


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

    return "Add/Edit/Delete System Coming Soon"


@app.route("/viewpdf/<path:filename>")
def view_pdf(filename):
    return send_from_directory(
        "static/docs",
        filename,
        mimetype="application/pdf"
    )


@app.route("/check")
def check():
    df = load_parts()
    return f"Parts Excel found. Total rows: {len(df)}"


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, session
import pandas as pd
import os

app = Flask(__name__)

app.secret_key = "megacoat123"

USERNAME = "admin"
PASSWORD = "1234"

PART_FILE = "rods.xlsx"
REJECTION_FILE = "rejection_data.xlsx"

COLUMNS = [
    "Sr No",
    "Part No",
    "Rev Date",
    "Application",
    "Total Length",
    "Plating Length",
    "Chrome Before",
    "Chrome After",
    "Nickel",
    "Piston End",
    "Plant",
    "Identification"
]


def load_parts():

    if os.path.exists(PART_FILE):

        df = pd.read_excel(PART_FILE)

        df = df.fillna("")

        return df

    return pd.DataFrame(columns=COLUMNS)


def save_parts(df):

    df.to_excel(PART_FILE, index=False)


@app.route("/", methods=["GET", "POST"])
def index():

    df = load_parts()

    results = []

    if request.method == "POST":

        search = request.form["search"].strip()

        results = df[
            df.astype(str).apply(
                lambda row: row.str.contains(
                    search,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        ].values.tolist()

    return render_template(
        "index.html",
        results=results,
        logged_in=session.get("logged_in")
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

    return render_template(
        "login.html",
        error=error
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
def add():

    if not session.get("logged_in"):

        return redirect("/login")

    if request.method == "POST":

        df = load_parts()

        new_row = {
            "Sr No": request.form["sr_no"],
            "Part No": request.form["part_no"],
            "Rev Date": request.form["rev_date"],
            "Application": request.form["application"],
            "Total Length": request.form["total_length"],
            "Plating Length": request.form["plating_length"],
            "Chrome Before": request.form["chrome_before"],
            "Chrome After": request.form["chrome_after"],
            "Nickel": request.form["nickel"],
            "Piston End": request.form["piston_end"],
            "Plant": request.form["plant"],
            "Identification": request.form["identification"]
        }

        df = pd.concat(
            [df, pd.DataFrame([new_row])],
            ignore_index=True
        )

        save_parts(df)

        return redirect("/")

    return render_template("add.html")


@app.route("/edit/<part_no>", methods=["GET", "POST"])
def edit(part_no):

    if not session.get("logged_in"):

        return redirect("/login")

    df = load_parts()

    df["Part No"] = df["Part No"].astype(str)

    row_data = df[df["Part No"] == str(part_no)]

    if row_data.empty:

        return "Part not found"

    index = row_data.index[0]

    if request.method == "POST":

        df.at[index, "Sr No"] = request.form["sr_no"]
        df.at[index, "Part No"] = request.form["part_no"]
        df.at[index, "Rev Date"] = request.form["rev_date"]
        df.at[index, "Application"] = request.form["application"]
        df.at[index, "Total Length"] = request.form["total_length"]
        df.at[index, "Plating Length"] = request.form["plating_length"]
        df.at[index, "Chrome Before"] = request.form["chrome_before"]
        df.at[index, "Chrome After"] = request.form["chrome_after"]
        df.at[index, "Nickel"] = request.form["nickel"]
        df.at[index, "Piston End"] = request.form["piston_end"]
        df.at[index, "Plant"] = request.form["plant"]
        df.at[index, "Identification"] = request.form["identification"]

        save_parts(df)

        return redirect("/")

    row = df.loc[index].to_dict()

    return render_template(
        "edit.html",
        row=row
    )


@app.route("/delete/<part_no>")
def delete(part_no):

    if not session.get("logged_in"):

        return redirect("/login")

    df = load_parts()

    df["Part No"] = df["Part No"].astype(str)

    df = df[df["Part No"] != str(part_no)]

    save_parts(df)

    return redirect("/")


@app.route("/daily_rejection")
def daily_rejection():

    if not os.path.exists(REJECTION_FILE):

        return "rejection_data.xlsx file not found"

    df = pd.read_excel(
        REJECTION_FILE,
        sheet_name="May-2026 Report",
        header=None
    )

    defect_names = [
        "Dent",
        "Black mark",
        "CUT MARK",
        "GD",
        "PD",
        "PH (Major)",
        "OD U/S",
        "OD O/S",
        "Gala - M",
        "Gala - P",
        "BUSH PLATING",
        "HEX",
        "MC",
        "MD",
        "RM",
        "CK/LM"
    ]

    yesterday = (
        pd.Timestamp.today().normalize()
        - pd.Timedelta(days=1)
    )

    selected_col = None

    for col in range(df.shape[1]):

        value = df.iloc[1, col]

        parsed_date = pd.to_datetime(
            value,
            errors="coerce"
        )

        if pd.notna(parsed_date):

            if parsed_date.normalize() == yesterday:

                selected_col = col

                break

    if selected_col is None:

        return "Yesterday date column not found in Excel"

    latest_date = pd.to_datetime(
        df.iloc[1, selected_col]
    ).strftime("%d-%m-%Y")

    defects = []

    values = []

    for defect in defect_names:

        found = False

        for row in range(df.shape[0]):

            row_text = " ".join(
                map(str, df.iloc[row].tolist())
            )

            if defect.lower().replace(" ", "") in row_text.lower().replace(" ", ""):

                try:

                    qty = float(df.iloc[row, selected_col])

                except:

                    qty = 0

                defects.append(defect)

                values.append(qty)

                found = True

                break

        if not found:

            defects.append(defect)

            values.append(0)

    combined = list(zip(defects, values))

    combined.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return render_template(
        "daily_rejection.html",
        defects=[x[0] for x in combined],
        values=[x[1] for x in combined],
        latest_date=latest_date
    )


@app.route("/check")
def check():

    df = load_parts()

    return f"Parts Excel found. Total rows: {len(df)}"


if __name__ == "__main__":

    app.run(debug=True)
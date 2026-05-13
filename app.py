from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Read Excel File
df = pd.read_excel('rods.xlsx')

@app.route('/', methods=['GET', 'POST'])

def index():

    results = []

    if request.method == 'POST':

        search = request.form['search']

        results = df[
            df.astype(str)
            .apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
        ].values.tolist()

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
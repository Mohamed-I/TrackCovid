from flask import Flask, render_template
import csv
app = Flask(__name__)


@app.route('/')
def coronavirse():

    countries = ['South Sudan', 'CAR', 'Chad', 'Sudan', 'Libya', 'Eritrea', 'Ethiopia', 'Egypt']
    with open('sorted_date.csv') as f:
        new_data = list(csv.reader(f))
        return render_template('home.html', new_data=new_data, countries=countries)


@app.template_filter()
def numberFormat(value):
    return format(int(value), ',d')


if __name__ == "__main__":
    app.run(debug=True)

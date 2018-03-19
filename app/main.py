from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route('/')
def main_page():
    r = requests.get('https://www.cinemacity.ro/ro/data-api-service/v1/quickbook/10107/film-events/in-cinema/1823/at-date/2018-03-19?attr=&lang=ro_RO')
    data = r.json()
    return render_template('index.html', films=data['body']['films'])


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

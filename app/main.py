from flask import Flask, render_template, g
import couchdbkit
import requests
import config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(config)


def connect_db():
    server = couchdbkit.Server(app.config['COUCHDB_URL'])
    return server.get_or_create_db(app.config['COUCHDB_DATABASE'])


def init_db():
    db = connect_db()
    loader = couchdbkit.loaders.FileSystemDocsLoader('_design')
    loader.sync(db, verbose=True)


@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    """Closes the database at the end of the request."""


@app.route('/')
def main_page():
    current_day = datetime.now().strftime("%Y-%m-%d")
    try:
        data = g.db.get(current_day)
    except couchdbkit.exceptions.ResourceNotFound:
        r = requests.get('https://www.cinemacity.ro/ro/data-api-service/v1/quickbook/10107/film-events/in-cinema/1823/at-date/{}?attr=&lang=ro_RO'.format(current_day))
        data = r.json()
        data['_id'] = current_day
        g.db.save_doc(data)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

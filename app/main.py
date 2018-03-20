from flask import Flask, render_template, g
from flask_bootstrap import Bootstrap
import couchdbkit
import requests
import config
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(config)


def get_day_as_id():
    return datetime.now().strftime("%Y-%m-%d")


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
    app.jinja_env.cache = {}
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    """Closes the database at the end of the request."""


@app.route('/')
@app.route('/date/<date>')
def main_page(date=get_day_as_id()):
    current_day = get_day_as_id()
    if date == get_day_as_id():
        current_time = datetime.now().strftime("%H:%M")
    else:
        current_time = 0
    try:
        data = g.db.view('parse_docs/get_showings', startkey=["{}".format(date)], endkey=["{}".format(date), {}])
    except couchdbkit.exceptions.ResourceNotFound:
        pass

    return render_template('movies.html', movies=data, time=current_time)


@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

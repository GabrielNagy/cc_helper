from flask import Flask, render_template, g, abort, request
from flask_bootstrap import Bootstrap
import couchdbkit
import config
from datetime import datetime, timedelta
from dateutil import parser
from htmlmin.main import minify


app = Flask(__name__)
Bootstrap(app)
app.config.from_object(config)


def get_day_as_id():
    return datetime.now().strftime("%Y-%m-%d")


def get_time_as_id():
    return datetime.now().strftime("%H:%M")


def connect_db():
    server = couchdbkit.Server(app.config['COUCHDB_URL'])
    return server.get_or_create_db(app.config['COUCHDB_DATABASE'])


def init_db():
    db = connect_db()
    loader = couchdbkit.loaders.FileSystemDocsLoader('_design')
    loader.sync(db, verbose=True)


@app.errorhandler(410)
def gone(e):
    return render_template('410.html'), 410


@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    app.jinja_env.cache = {}
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    """Closes the database at the end of the request."""


@app.after_request
def response_minify(response):
    """
    minify html response to decrease site traffic
    """
    if response.content_type == u'text/html; charset=utf-8':
        response.set_data(
            minify(response.get_data(as_text=True))
        )

        return response
    return response


@app.route('/')
def main_page():
    date = request.args.get('date', get_day_as_id())
    time = request.args.get('time', get_time_as_id())
    current_date = get_day_as_id()
    if date != current_date and not request.args.get('time'):
        time = "0"
    try:
        day_object = g.db.get(date)
    except couchdbkit.exceptions.ResourceNotFound:
        abort(404)
    data = g.db.list('parse_docs/parse_categories', 'parse_docs/get_showings', startkey=["{}".format(date), "{}".format(time)], endkey=["{}".format(date), {}])
    if date < current_date:
        abort(410)
    next_date = datetime.strftime(parser.parse(date) + timedelta(days=1), "%Y-%m-%d")
    prev_date = datetime.strftime(parser.parse(date) - timedelta(days=1), "%Y-%m-%d")
    return render_template('movies.html', movies=data, time=time, current_date=current_date, date=date, next_date=next_date, prev_date=prev_date)


@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

import couchdbkit

try:
    from app.config import COUCHDB_URL, COUCHDB_DATABASE
except ImportError:
    from config import COUCHDB_URL, COUCHDB_DATABASE


if __name__ == "__main__":
    server = couchdbkit.Server(COUCHDB_URL)
    db = server.get_or_create_db(COUCHDB_DATABASE)

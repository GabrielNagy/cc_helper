import couchdbkit
import os

try:
    from app.config import COUCHDB_URL, COUCHDB_DATABASE
except ImportError:
    from config import COUCHDB_URL, COUCHDB_DATABASE


if __name__ == "__main__":
    server = couchdbkit.Server(COUCHDB_URL)
    db = server.get_or_create_db(COUCHDB_DATABASE)
    couchdbkit.designer.push(os.path.join(os.path.dirname(__file__), '_design/parse_docs'), db)

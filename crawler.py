from logzero import logger, setup_logger
import sys
import couchdbkit
import requests
from app.config import COUCHDB_URL, COUCHDB_DATABASE, JSON_PREFIX
from datetime import datetime, timedelta

logger = setup_logger(logfile="/var/log/cc_crawl.log")

if __name__ == "__main__":
    server = couchdbkit.Server(COUCHDB_URL)
    db = server.get_or_create_db(COUCHDB_DATABASE)

    current_day = datetime.now()

    while True:
        try:
            parsed_date = current_day.strftime("%Y-%m-%d")
            r = requests.get(JSON_PREFIX + parsed_date)  # request json data for parsed date
            api_data = r.json()
            db_data = db.get(parsed_date)
            # print "Found date " + parsed_date + " in db."
            logger.info("Found date " + parsed_date + " in db.")
            # if date found in db, check for equality with api data
            # only replace films because events disappear as time passes and we tend to lose useful data
            if api_data['body'] != db_data['body'] and parsed_date != datetime.now().strftime("%Y-%m-%d"):
                logger.warning("API data different from DB data. Overwriting with newer data.")
                db_data['body'] = api_data['body']
                db[parsed_date] = db_data
            else:
                logger.info("API data equal to DB data. Not changing anything.")
        except couchdbkit.exceptions.ResourceNotFound:
            if not api_data['body']['films'] or len(api_data['body']['films']) == 0:
                logger.info("Reached parse limit on date " + parsed_date + ". Nothing more to fetch.")
                break
            api_data['_id'] = parsed_date
            db.save_doc(api_data)
            logger.info("Saved doc with date " + parsed_date + ".")
        finally:
            current_day += timedelta(days=1)

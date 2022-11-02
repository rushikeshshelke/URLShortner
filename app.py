import os

from flask import Flask
from dotenv import load_dotenv
from commonLibs.initialiseLogging import InitialiseLogging
from commonLibs.globalVariables import GlobalVariables
from routes import routes
from pymongo import MongoClient

load_dotenv()
InitialiseLogging().setupLogging()
GlobalVariables.LOGGER.info("URL-Shortner app")
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.register_blueprint(routes.pages)
client = MongoClient(os.environ.get("MONGODB_URI"))
app.db = client.get_database(os.environ.get("DATABASE_NAME"))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT")),debug=True)
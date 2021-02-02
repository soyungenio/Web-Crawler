import os

postgres_host = os.environ.get('POSTGRES_HOST')
postgres_login = os.environ.get('POSTGRES_USER')
postgres_psw = os.environ.get('POSTGRES_PASSWORD')
postgres_db = os.environ.get('POSTGRES_DB')

DB_URL = "postgres://{}:{}@{}/{}".format(postgres_login, postgres_psw, postgres_host, postgres_db)
POOL_RECYCLE = 800
TRACK_MODIFICATIONS = False

HOST = "http://localhost/"

CRAWLER_DEPTH = 3
SITE_FOlDER = "sites/"
SITE_FOLDER_NAME = "site"
SITE_FIlENAME = "site.zip"

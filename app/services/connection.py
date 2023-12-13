from mysqlclientpy import DB
from app.utils.env import Env

mail_db = DB(
    host=Env.get_secure('MAIL_DB_HOST'),
    user=Env.get_secure('MAIL_DB_USER'),
    password=Env.get_secure('MAIL_DB_PASSWORD'),
    database=Env.get_secure('MAIL_DB_DATABASE')
)



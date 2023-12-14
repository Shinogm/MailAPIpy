from mysqlclientpy import DB
from app.utils.env import Env

mail_db = DB(
    host=Env.get_secure('HOST_DB'),
    user=Env.get_secure('USER_DB'),
    password=Env.get_secure('PASS_DB'),
    database=Env.get_secure('NAME_DB')
)



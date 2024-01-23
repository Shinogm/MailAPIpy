from app.services.connection import mail_db
from fastapi import HTTPException
from app.utils import auth, perms
from enum import Enum

class LOGIN(Enum):
    OK = 'OK'
    INVALID_PASSWORD = 'INVALID_PASSWORD'

def verify_password(password: str, email: str, token: str):
    perm = perms.get_perm_id(LOGIN.OK.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')

    user_db = mail_db.fetch_one(
        sql='SELECT * FROM users WHERE email = %s',
        params=(email,)
    )
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    try:
        import bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), user_db['password'].encode('utf-8')):
        #password == user_db['password']:
            return True
        else:
            print(f'{user_db["password"]} != {password}')
            return False
    except:
        raise HTTPException(status_code=404, detail='User not found')

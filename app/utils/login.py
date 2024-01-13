from app.services.connection import mail_db
from fastapi import HTTPException

def verify_password(password: str, email: str):
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
    
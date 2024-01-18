from fastapi import HTTPException
from app.utils import auth, perms
from app.enums.users.permissions import USERS
from app.services.connection import mail_db

async def get_users(token: str):
    perm = perms.get_perm_id(USERS.READ.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')

    users = mail_db.fetch_all('SELECT BIN_TO_UUID(id) as id, name, email, plan_id FROM users')

    return {
        'message': 'Users fetched successfully',
        'data': users
    }

async def get_one_user(token: str, user_id: str):
    perm = perms.get_perm_id(USERS.READ.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')

    user_db = mail_db.fetch_one(
        sql='SELECT BIN_TO_UUID(id) as id, name, email FROM users WHERE id = UUID_TO_BIN(%s)',
        params=(user_id,)
    )

    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    return {
        'message': 'User fetched successfully',
        'data': user_db
    }
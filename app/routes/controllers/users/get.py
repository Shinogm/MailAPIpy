from fastapi import HTTPException
from app.utils import auth, perms
from app.enums.users.permissions import USERS
from app.services.connection import mail_db

async def get_users(token: str):
    perm = perms.get_perm_id(USERS.READ.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')

    users = mail_db.fetch_all('SELECT BIN_TO_UUID(id) as id, name, email FROM users')

    return {
        'message': 'Users fetched successfully',
        'data': users
    }
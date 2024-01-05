from fastapi import HTTPException
from app.utils import auth, perms
from app.enums.users.permissions import USERS
from app.services.connection import mail_db

async def delete_user_where_id(token: str, id: str):
    perm = perms.get_perm_id(USERS.DELETE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')

    try:
        mail_db.execute(
            sql='DELETE FROM users WHERE id = UUID_TO_BIN(%s)',
            params=(id,)
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al eliminar el usuario')

    return {
        'message': 'User deleted successfully',
    }
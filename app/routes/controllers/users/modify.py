from app.models.users import UserUpdate
from fastapi import HTTPException, Depends
from app.utils import auth, perms
from app.enums.users.permissions import USERS
from app.services.connection import mail_db
import bcrypt

async def modify_user(
    token: str,
    id: str,
    user: UserUpdate = Depends(UserUpdate.as_form)
):
    perm = perms.get_perm_id(USERS.UPDATE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')
    try:
        user_db = mail_db.fetch_one(
            sql='SELECT * FROM users WHERE id = UUID_TO_BIN(%s)',
            params=(id,)
        )

        if not user_db:
            raise HTTPException(status_code=404, detail='No existe el usuario')

        mail_db.update(
            table='users',
            data={
                'name': user.name if user.name is not None else user_db['name'],
                'email': user.email if user.email is not None else user_db['email'],
                'password': bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()) if user.password is not None else user_db['password']
            },
            where=f'id = UUID_TO_BIN("{id}")'
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al modificar el usuario')

    return {
        'message': 'User modified successfully',
    }

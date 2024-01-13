from app.models.users import User
from fastapi import HTTPException, Depends
from app.utils import auth, perms
from app.enums.users.permissions import USERS
from app.services.connection import mail_db
import bcrypt

async def create_user(token: str, user: User = Depends(User.as_form)):
    perm = perms.get_perm_id(USERS.CREATE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')

    try:
         mail_db.insert(
            table='users',
            data={
                'name': user.name,
                'email': user.email,
                'password': bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al crear el usuario')
    
    return {
        'message': 'User created successfully',
        'user': user
    }
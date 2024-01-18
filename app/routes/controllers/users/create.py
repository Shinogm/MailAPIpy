from app.models.users import User
from fastapi import HTTPException, Depends
from app.utils import auth, perms
from app.enums.users.permissions import USERS
from app.services.connection import mail_db
import bcrypt

async def get_plans(token: str, plan_id: int | None = None ):
    perm = perms.get_perm_id(USERS.READ.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')

    if plan_id is not None:
        plan = mail_db.fetch_one(
            sql='SELECT * FROM plans WHERE id = %s',
            params=(plan_id,)
        )
        if plan is None:
            raise HTTPException(status_code=404, detail='El plan no existe')
        return {
            'message': 'Plan fetched successfully',
            'plan': plan
        }

    plans = mail_db.fetch_all('SELECT * FROM plans')

    return {
        'message': 'Plans fetched successfully',
        'data': plans
    }


async def create_user(token: str, plan_id: int, user: User = Depends(User.as_form)):
    perm = perms.get_perm_id(USERS.CREATE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')

    if plan_id not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail='El plan no existe')

    try:
         user_id  = mail_db.insert(
            table='users',
            data={
                'name': user.name,
                'email': user.email,
                'password': bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()),
                'plan_id': plan_id
            }
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al crear el usuario')
    return {
        'message': 'User created successfully',
        'user': user,
        'user_id': user_id
    }
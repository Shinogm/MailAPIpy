from fastapi import HTTPException
from app.services.connection import mail_db
from app.utils import auth, perms

async def assing_plan(user_id: str, plan_id: int):
    user_db = mail_db.fetch_one(
        sql='SELECT BIN_TO_UUID(id) as id, name, email FROM users WHERE id = UUID_TO_BIN(%s)',
        params=(user_id,)
    )
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    plan_db = mail_db.fetch_one(
        sql='SELECT id, name, price FROM plans WHERE id = %s',
        params=(plan_id,)
    )
    if not plan_db:
        raise HTTPException(status_code=404, detail='Plan not found')
    get_assing_plan = mail_db.fetch_one(
        sql='SELECT id FROM user_plan WHERE user_id = UUID_TO_BIN(%s)',
        params=(user_id,)
    )
    if get_assing_plan:
        raise HTTPException(status_code=400, detail='El usuario ya tiene un plan asignado')
    try:
        mail_db.execute(
            sql='INSERT INTO user_plan (user_id, plan_id) VALUES (UUID_TO_BIN(%s), %s)',
            params=(user_id, plan_id)
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al asignar el plan')
    return {
        'message': f'Plan {plan_db} assigned successfully to {user_db["name"]}',
        'plan_id': plan_id,
        'user_id': user_id
    }

async def get_user_plan(user_id: str | None = None, plan_id: int | None = None):

    if plan_id is not None:
        try:

            get_all_users_plan_with_plan_id = mail_db.fetch_all(
                sql='SELECT BIN_TO_UUID(id) as id, name, email, plan_id FROM users WHERE plan_id = %s',
                params=(plan_id,)
            )

            if not get_all_users_plan_with_plan_id:
                raise HTTPException(status_code=404, detail='No hay usuarios con ese plan')

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail='Ocurrio un error al obtener los usuarios con ese plan')

        return {
            'message': f'Usuarios con el plan {plan_id} obtenidos exitosamente',
            'data': get_all_users_plan_with_plan_id
        }

    user_db = mail_db.fetch_one(
        sql='SELECT BIN_TO_UUID(id) as id, name, email, plan_id FROM users WHERE id = UUID_TO_BIN(%s)',
        params=(user_id,)
    )
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    try:
        plan_db =  mail_db.fetch_one(
            sql='SELECT * FROM plans WHERE id = %s',
            params=(user_db["plan_id"],)
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al obtener el plan del usuario')

    return {
        'message': f'Plan {plan_db} get successfully to user {user_db["name"]}',
        'plan_id': plan_db['id'],
        'user_id': user_id
    }

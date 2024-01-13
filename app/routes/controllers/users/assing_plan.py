from fastapi import HTTPException
from app.services.connection import mail_db
from app.utils import auth, perms
from app.enums.folders.folder_perm import FOLDER_PERM

async def assing_plan(user_id: str, plan_id: int):
    user_db = mail_db.fetch_one(
        sql='SELECT BIN_TO_UUID(id) as id, name, email FROM users WHERE id = UUID_TO_BIN(%s)',
        params=(user_id,)
    )
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')
    try:
        mail_db.insert(
            'user_plans',
            {
                'user_id': user_id,
                'plan_id': plan_id
            }
        )
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al asignar el plan')
    
    return {
        'message': 'Plan assigned successfully',
        'plan_id': plan_id,
        'user_id': user_id
    }
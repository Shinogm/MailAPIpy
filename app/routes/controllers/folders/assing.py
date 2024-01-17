from fastapi import HTTPException
from app.services.connection import mail_db
from app.utils import auth, perms
from app.enums.folders.folder_perm import FOLDER_PERM

async def get_all_user_assing_folders(token: str, user_id: str):
    perm = perms.get_perm_id(FOLDER_PERM.FOLDER_ASSIGN.value)

    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')

    user_db = mail_db.fetch_one(
        sql='SELECT BIN_TO_UUID(id) as id, name, email FROM users WHERE id = UUID_TO_BIN(%s)',
        params=(user_id,)
    )

    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    folders = mail_db.fetch_all(
        sql='SELECT * FROM folders WHERE id IN (SELECT folder_id FROM user_folders WHERE user_id = UUID_TO_BIN(%s))',
        params=(user_id,)
    )

    return {
        'message': 'Folders fetched successfully',
        'data': folders
    }
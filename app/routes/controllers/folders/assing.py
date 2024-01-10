from fastapi import HTTPException, Depends
from app.models.folder import CreateFolder
from app.services.connection import mail_db
from app.utils import auth, perms
from app.enums.folders.folder_perm import FOLDER_PERM

#user id is BIN
async def assing_folder(token: str, folder_id: int, user_id: int):
    perm = perms.get_perm_id(FOLDER_PERM.FOLDER_ASSIGN.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')

    user_db = mail_db.fetch_one(
        sql='SELECT * FROM users WHERE id = %s',
        params=(user_id,)
    )

    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    try:
        mail_db.insert(
            'user_folders',
            {
                'user_id': user_id,
                'folder_id': folder_id
            }
        )
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al asignar la carpeta')
    
    return {
        'message': 'Folder assigned successfully',
        'folder_id': folder_id,
        'user_id': user_id
    }

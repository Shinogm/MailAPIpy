from fastapi import HTTPException, Depends
from app.models.folder import CreateFolder
from app.services.connection import mail_db
from app.utils import auth, perms
from app.enums.folders.folder_perm import FOLDER_PERM

async def create_folder(token: str, user_id: str, folder: CreateFolder = Depends(CreateFolder.as_form)):
    perm = perms.get_perm_id(FOLDER_PERM.FOLDER_CREATE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')
    user_db = mail_db.fetch_one(
        sql='SELECT BIN_TO_UUID(id) as id, name, email FROM users WHERE id = UUID_TO_BIN(%s)',
        params=(user_id,)
    )
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')
    try:
        folder_id = mail_db.insert(
            'folders',
            {
                'name': folder.name
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al crear la carpeta')

    try:
        assing = mail_db.execute(
            sql='INSERT INTO user_folders (user_id, folder_id) VALUES (UUID_TO_BIN(%s), %s)',
            params=(user_id, folder_id)
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al asignar la carpeta')
    return {
        'message': 'Folder created successfully',
        'folder': folder,
        'user_id': user_id,
        'assing': assing
        }


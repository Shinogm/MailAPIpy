from fastapi import HTTPException, Depends
from app.models.folder import CreateFolder
from app.services.connection import mail_db
from app.utils import auth, perms
from app.enums.folders.folder_perm import FOLDER_PERM

async def create_folder(token: str,folder: CreateFolder = Depends(CreateFolder.as_form)):
    perm = perms.get_perm_id(FOLDER_PERM.FOLDER_CREATE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')

    try:
        mail_db.insert(
            'folders',
            {
                'name': folder.name
            }
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al crear la carpeta')

    return {
        'message': 'Folder created successfully',
        'folder': folder,
        }


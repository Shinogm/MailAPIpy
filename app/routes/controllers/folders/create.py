from fastapi import HTTPException, Depends
from app.models.folder import CreateFolder
from app.services.connection import mail_db


async def create_folder(folder: CreateFolder = Depends(CreateFolder.as_form), user_id: int | None = None):

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
        'folder': folder
        }


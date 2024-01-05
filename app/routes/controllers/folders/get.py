from fastapi import HTTPException, Depends
from app.services.connection import mail_db

async def get_folders():
    try:
        folders = mail_db.fetch_all(
        sql='SELECT * FROM folders'
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al obtener las carpetas')

    return {
        'message': 'Folders obtained successfully',
        'folders': folders
    }

async def get_folder(id: int):
    try:
        folder = mail_db.fetch_one(
            sql='SELECT * FROM folders WHERE id = %s',
            params=(id,)
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al obtener la carpeta')

    return {
        'message': 'Folder obtained successfully',
        'folder': folder
    }
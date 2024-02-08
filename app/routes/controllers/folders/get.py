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

async def get_folder(id: int, user_id: str):
    user_db = mail_db.fetch_one(
        sql='SELECT * FROM users WHERE id = UUID_TO_BIN(%s)',
        params=(user_id,)
    )
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    folder_db = mail_db.fetch_one(
        sql='SELECT * FROM folders WHERE id = %s',
        params=(id,)
    )
    if not folder_db:
        raise HTTPException(status_code=404, detail='Folder not found')
    
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
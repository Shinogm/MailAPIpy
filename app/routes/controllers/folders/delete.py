from fastapi import HTTPException
from app.services.connection import mail_db

async def delete_folder(id: int, user_id: str):
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
        mail_db.execute(
            sql='DELETE FROM folders WHERE id = %s',
            params=(id,)
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al eliminar la carpeta')

    return {
        'message': 'Folder deleted successfully',
        'folder_id': id
        }
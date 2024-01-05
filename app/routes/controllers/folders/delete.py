from fastapi import HTTPException, Depends
from app.services.connection import mail_db

async def delete_folder(id: int):
    
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
        'folder_id': folder_db
        }
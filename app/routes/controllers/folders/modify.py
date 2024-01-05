from fastapi import HTTPException, Depends
from app.models.folder import UpdateFolder
from app.services.connection import mail_db

async def modify_folder(id: int, folder: UpdateFolder = Depends(UpdateFolder.as_form)):
    folder_db = mail_db.fetch_one(
        sql='SELECT * FROM folders WHERE id = %s',
        params=(id,)
    )
    if not folder_db:
        raise HTTPException(status_code=404, detail='Folder not found')
    try:
        mail_db.update(
            table='folders',
            data={
                'name': folder.name if folder.name is not None else folder_db['name']
            },
            where=f'id = {id}'
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al modificar la carpeta')

    return {
        'message': 'Folder modified successfully',
        'folder_id': folder_db
        }

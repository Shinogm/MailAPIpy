from fastapi import HTTPException
from app.services.connection import mail_db
from app.utils import auth, perms
from app.enums.contacts.contact_perm import CONTACTPERM

async def assing_contacts_in_user_folder(user_id: str, folder_id: int, contact_id: str):
    contact_db = mail_db.fetch_one(
            sql='SELECT * FROM contacts WHERE id = %s',
            params=(contact_id,)
        )
    
    if not contact_db:
        raise HTTPException(status_code=404, detail='Contact not found')
    
    user_db = mail_db.fetch_one(
            sql='SELECT * FROM users WHERE id = UUID_TO_BIN(%s)',
            params=(user_id,)
        )
    
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')
    
    folder_db = mail_db.fetch_one(
            sql='SELECT * FROM folders WHERE id = %s',
            params=(folder_id,)
        )
    
    if not folder_db:
        raise HTTPException(status_code=404, detail='Folder not found')
    
    try:
        mail_db.execute(
            sql='INSERT INTO user_folder_contact (user_id, folder_id, contact_id) VALUES (UUID_TO_BIN(%s), %s, %s)',
            params=(user_id, folder_id, contact_id)
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al asignar el contacto')
    
    return {
        'message': 'Contact assigned successfully',
        'user_id': user_id,
        'folder_id': folder_id,
        'contact_id': contact_id
    }
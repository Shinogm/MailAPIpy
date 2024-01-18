from fastapi import HTTPException, Depends
from app.models.contacts import Contact
from app.services.connection import mail_db
from datetime import date

async def create_contact(folder_id: int, user_id: str, contact: Contact = Depends(Contact.as_form)):

    user_db = mail_db.fetch_one(
        sql='SELECT BIN_TO_UUID(id) as id, name, email FROM users WHERE id = UUID_TO_BIN(%s)',
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
        contact_id = mail_db.insert(
            'contacts',
            {
                'name': contact.name,
                'phone': contact.phone,
                'email': contact.email,
                'birthday': contact.birthday_data
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al crear el contacto')

    try:
        assing_contact = mail_db.execute(
            sql='INSERT INTO contacts_in_user_folder (user_id, folder_id, contact_id) VALUES (UUID_TO_BIN(%s), %s, %s)',
            params=(user_id, folder_id, contact_id)
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al asignar el contacto')

    return {
        'message': 'Contact created successfully',
        'data': f'se asigno el contacto {contact.name} al usuario {user_db["name"]} en la carpeta {folder_db["name"]} su id asignado es {assing_contact}',
        }

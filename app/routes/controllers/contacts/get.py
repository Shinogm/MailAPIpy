from fastapi import HTTPException, Depends
from app.models.contacts import Contact
from app.services.connection import mail_db

async def get_contacts():
    try:
        contacts = mail_db.fetch_all(
            sql='SELECT * FROM contacts'
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al obtener los contactos')
    return {
        'message': 'Contacts retrieved successfully',
        'contacts': [Contact(**contact) for contact in contacts]
    }

async def get_contact(id: int):
    try:
        contact = mail_db.fetch_one(
            sql='SELECT * FROM contacts WHERE id = %s',
            params=(id,)
        )
    except Exception as e:
        print(e)

        raise HTTPException(status_code=500, detail='Ocurrio un error al obtener el contacto')
    if not contact:
        raise HTTPException(status_code=404, detail='Contact not found')
    return {
        'message': 'Contact retrieved successfully',
        'contact': Contact(**contact)
    }
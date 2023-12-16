from fastapi import HTTPException, Depends
from app.models.contacts import Contact
from app.services.connection import mail_db
from datetime import date

async def create_contact(contact: Contact = Depends(Contact.as_form)):
    try:
        mail_db.insert(
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
    return {
        'message': 'Contact created successfully',
        'contact': contact
        }

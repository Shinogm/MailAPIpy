from fastapi import HTTPException
from app.models.contacts import Contact
from app.services.connection import mail_db


async def create_contact(contact: Contact):
    try:
        mail_db.insert(
            table='contacts',
            data={
                'name': contact.name,
                'last_name': contact.last_name,
                'phone': contact.phone,
                'email': contact.email,
                'birthday': contact.birthday
            }
            )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    return {
        'message': 'Contact created successfully',
        'contact': contact
        }

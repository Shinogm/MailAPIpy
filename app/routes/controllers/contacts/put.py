from fastapi import HTTPException, Depends
from app.models.contacts import Contact
from app.services.connection import mail_db

async def update_contact(contact_id: int, contact: Contact = Depends(Contact.as_form)):

    try:
        contact_db = mail_db.fetch_one(
            sql='SELECT * FROM contacts WHERE id = %s',
            params=(contact_id,)
        )
        if not contact_db:
            raise HTTPException(status_code=404, detail='Contact not found')
        
        mail_db.update(
            table='contacts',
            data={
                'name': contact.name if contact.name is not None else contact_db['name'],
                'last_name': contact.last_name if [contact.last_name] is not None else contact_db['last_name'],
                'phone': contact.phone if contact.phone is not None else contact_db['phone'],
                'email': contact.email if contact.email is not None else contact_db['email'],
                'birthday': contact.birthday if contact.birthday is not None else contact_db['birthday']
            },
            where=f'id = {contact_id}'
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

    return {
        'message': 'Contact updated successfully',
        'contact_id': contact_id
        }
from fastapi import HTTPException, Depends
from app.models.contacts import ContactUpdate
from app.services.connection import mail_db

async def update_contact(contact_id: int, contact: ContactUpdate = Depends(ContactUpdate.as_form)):

    contact_db = mail_db.fetch_one(
        sql='SELECT * FROM contacts WHERE id = %s',
        params=(contact_id,)
    )

    if not contact_db:
        raise HTTPException(status_code=404, detail='Contact not found')

    try:

        contact_udp = mail_db.update(
            table='contacts',
            data={
                'name': contact.name if contact.name is not None else contact_db['name'],
                'phone': contact.phone if contact.phone is not None else contact_db['phone'],
                'email': contact.email if contact.email is not None else contact_db['email'],
                'birthday': contact.birthday_data if contact.birthday_data is not None else contact_db['birthday']
            },
            where=f'id = {contact_id}'
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

    return {
        'message': 'Contact updated successfully',
        'contact_id': contact_udp
        }
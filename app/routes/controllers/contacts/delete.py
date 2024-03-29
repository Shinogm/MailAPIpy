from app.services.connection import mail_db
from fastapi import HTTPException

async def delete_contact(contact_id: int):

    contact_db = mail_db.fetch_one(
        sql='SELECT * FROM contacts WHERE id = %s',
        params=(contact_id,)
    )
    if not contact_db:
        raise HTTPException(status_code=404, detail='Contact not found')

    try:
        mail_db.execute(
            sql='DELETE FROM contacts WHERE id = %s',
            params=(contact_id,)
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al eliminar el contacto')

    return {
        'message': 'Contact deleted successfully',
        'contact_id': contact_db
        }

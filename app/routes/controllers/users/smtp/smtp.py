from app.utils.email.models.send import SmtpConfig
from fastapi import HTTPException
from app.services.connection import mail_db
from app.utils import auth, perms
from app.routes.controllers.users.smtp.enums.smtp_enum import SMTPERMISSION

async def set_smpt_config(token: str, smtp_config: SmtpConfig, user_id: str):
    perm = perms.get_perm_id(SMTPERMISSION.CREATE_SERVER.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='No tienes permisos para realizar esta acción')
    user_db = mail_db.fetch_one(
        sql='SELECT * FROM users WHERE id = UUID_TO_BIN(%s)',
        params=(user_id,)
    )
    if not user_db:
        raise HTTPException(status_code=404, detail='No existe el usuario')

    try:
        mail_db.insert(
            table='user_email_smtp',
            data={
                'user_id': user_id,
                'smtp_server': smtp_config.smtp_server,
                'port': smtp_config.port,
                'user_name': smtp_config.user_name,
                'user_password': smtp_config.user_password
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al modificar el usuario')

    return {
        'message': 'SMTP config set successfully',
        'smtp_config': smtp_config,
        'user_id': user_id
    }
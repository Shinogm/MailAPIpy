from fastapi import APIRouter
from app.utils.email.sendmail import send_email
from app.routes.controllers.users.smtp.smtp import set_smpt_config

router = APIRouter(prefix='/email', tags=['email'])

router.post('/send')(send_email)
router.post('/users/smtp')(set_smpt_config)
from fastapi import APIRouter
from app.utils.email.sendmail import send_email

router = APIRouter(prefix='/email', tags=['email'])

router.post('/send')(send_email)
from fastapi import APIRouter
from app.routes.controllers.contacts import create, get

router = APIRouter(prefix='/contact', tags=['contacts'])

router.post('/create')(create.create_contact)
router.get('/get')(get.get_contacts)
router.get('/getone/{id}')(get.get_contact)


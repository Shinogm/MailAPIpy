from fastapi import APIRouter
from app.routes.controllers.contacts import create, get, delete, put, assing_contacts

router = APIRouter(prefix='/contact', tags=['contacts'])

router.post('/create')(create.create_contact)
router.get('/get')(get.get_contacts)
router.get('/getone/{id}')(get.get_contact)
router.delete('/delete/{id}')(delete.delete_contact)
router.put('/update/{id}')(put.update_contact)
router.post('/assing')(assing_contacts.assing_contacts_in_user_folder)

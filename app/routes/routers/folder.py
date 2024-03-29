from fastapi import APIRouter
from app.routes.controllers.folders import create, get, delete, modify, assing

router = APIRouter(prefix='/folder', tags=['folders'])

router.post('/create')(create.create_folder)
router.get('/get')(get.get_folders)
router.delete('/delete/{id}')(delete.delete_folder)
router.put('/update/{id}')(modify.modify_folder)
router.get('/get/{id}')(get.get_folder)
router.get('/assing/{user_id}')(assing.get_all_user_assing_folders)
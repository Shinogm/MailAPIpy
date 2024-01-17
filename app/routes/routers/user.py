from fastapi import APIRouter
from app.routes.controllers.users import create, get, delete, modify, assing_plan
from app.utils.login import verify_password
router = APIRouter(prefix='/user', tags=['users'])

router.post('/create')(create.create_user)
router.get('/get')(get.get_users)
router.delete('/delete')(delete.delete_user_where_id)
router.put('/modify')(modify.modify_user)
router.get('/get_one')(get.get_one_user)
router.post('/login')(verify_password)
router.post('/assing_plan')(assing_plan.assing_plan)
router.delete('/unassing_plan')(assing_plan.unassing_plan)

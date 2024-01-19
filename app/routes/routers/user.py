from fastapi import APIRouter
from app.routes.controllers.users import create, get, delete, modify, assing_plan
from app.utils.login import verify_password
router = APIRouter(prefix='/user', tags=['users'])

router.get('/get_plans')(create.get_plans)
router.get('/get_user_plan')(assing_plan.get_user_plan)
router.get('/get')(get.get_users)
router.get('/get_one')(get.get_one_user)
router.post('/create')(create.create_user)
router.post('/login')(verify_password)
router.delete('/delete')(delete.delete_user_where_id)
router.put('/modify')(modify.modify_user)
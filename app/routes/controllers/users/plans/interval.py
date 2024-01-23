from fastapi import HTTPException
from app.services.connection import mail_db
from app.utils import auth, perms
from app.routes.controllers.users.plans.enums.plans import PLANS
import time
import threading

class Interval:
    def __init__(self, interval, action, *args):
        self.interval = interval
        self.action = action
        self.args = args
        self.stop_event = threading.Event()
        thread = threading.Thread(target=self.__set_interval)
        thread.start()

    def __set_interval(self):
        next_time = time.time() + self.interval
        while not self.stop_event.wait(next_time - time.time()):
            next_time += self.interval
            self.action(*self.args)

    def cancel(self):
        self.stop_event.set()



async def update_plan_not_paid(paid: str | None = None):
    user_db = mail_db.fetch_all(
        sql='SELECT * FROM users',
    )
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')
    for user in user_db:
        if user['is_paid'] == PLANS.PAID.value:
            try:
                mail_db.execute(
                    sql='UPDATE users SET is_paid = %s WHERE id = %s',
                    params=(PLANS.PAID.value, user['id'])
                )
            except Exception as e:
                print(e)
                raise HTTPException(status_code=500, detail='Ocurrio un error al actualizar el plan del usuario')
            return {
                'message': f'Plan {PLANS.PAID.value} assigned successfully to {user["name"]}',
                'plan_id': PLANS.PAID.value,
                'user_id': user['id']
            }

        if (paid is not None) and (user['is_paid'] == PLANS.NOT_PAID.value):
            try:
                mail_db.execute(
                    sql='UPDATE users SET is_paid = %s WHERE id = %s',
                    params=(PLANS.NOT_PAID.value, user['id'])
                )
            except Exception as e:
                print(e)
                raise HTTPException(status_code=500, detail='Ocurrio un error al actualizar el plan del usuario')
            return {
                'message': f'Plan {PLANS.NOT_PAID.value} assigned successfully to {user["name"]}',
                'plan_id': PLANS.NOT_PAID.value,
                'user_id': user['id']
            }

async def execute_interval():
    interval = Interval(2, update_plan_not_paid, 'payment')
    print('Intervalo ejecutado')
    return interval
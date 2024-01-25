import stripe
from fastapi import HTTPException
from app.services.connection import mail_db
from app.utils.env import Env

stripe.api_key = Env.get_secure('KEY_STRIPE')

async def receive_users_payments(user_id: str):
    user = mail_db.fetch_one(
        sql='SELECT * FROM users WHERE id = UUID_TO_BIN(%s)',
        params=(user_id,)
    )

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    get_plan = mail_db.fetch_one(
        sql='SELECT * FROM plans WHERE id = %s',
        params=(user['plan_id'],)
    )

    if not get_plan:
        raise HTTPException(status_code=404, detail='Plan not found')


    try:
        stripe_customer = stripe.Customer.create(
          
        )


        user_update_payment = mail_db.update(
            table='users',
            data={
                'is_paid': 1
            },
            where=f'id = UUID_TO_BIN("{user_id}")'
        )

        return {
            'message': 'User has a plan',
            'user': user
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al obtener los datos del usuario')


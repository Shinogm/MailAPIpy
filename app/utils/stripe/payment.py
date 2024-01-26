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

    user_is_pay = mail_db.fetch_one(
        sql='SELECT * FROM users WHERE id = UUID_TO_BIN(%s) AND is_paid = 1',
        params=(user_id,)
    )

    if user_is_pay:
        raise HTTPException(status_code=400, detail='User is pay')

    try:
        create_product = stripe.Product.create(
            name = get_plan['name'],
            type='service'
        )

        create_price = stripe.Price.create(
            product = create_product['id'],
            unit_amount = get_plan['price'],
            currency = 'mxn',
            recurring = {
                'interval': 'month'
            }
        )

        create_subscription = stripe.Subscription.create(
            customer = user['stripe_customer_id'],
            items = [
                {
                    'price': create_price['id']
                }
            ],
        )

        user_subscription_payment_verify = stripe.Subscription.retrieve(
            create_subscription['id']
        )

    

        if user_subscription_payment_verify['status'] != 'active':
            raise HTTPException(status_code=400, detail='Payment not verified')
        else:


            user_update_payment = mail_db.update(
                table='users',
                data={
                    'is_paid': 1
                },
                where=f'id = UUID_TO_BIN("{user_id}")'
            )

            return {
                'message': 'User has a plan',
                'user': user,
                'user_subscription_payment_verify': user_subscription_payment_verify,
                'user_update_payment': user_update_payment
            }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Ocurrio un error al obtener los datos del usuario')


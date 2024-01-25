from app.services.fastapi import App
from app.routes.routers import contact, user, folder, mail
from app.models.static_dir import StaticDir
from app.routes.controllers.users.plans.interval import execute_interval

def main():
    app = App(
    routers=[
        user.router,
        folder.router,
        contact.router,
        mail.router

    ],
    static_dirs=[
        StaticDir(name='public', path='public')
    ]
    ).get_app()

    return app
if __name__ == '__main__':
    app = main()
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=3001)


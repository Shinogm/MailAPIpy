from app.services.fastapi import App
from app.routes.routers import contact
from app.models.static_dir import StaticDir

app = App(
    routers=[
        #status.router,
        contact.router
    ],
    static_dirs=[
        StaticDir(name='public', path='public')
    ]
    
).get_app()

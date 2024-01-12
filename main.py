from app.services.fastapi import App
from app.routes.routers import contact, user, folder
from app.models.static_dir import StaticDir

def main():
    app = App(
    routers=[
        contact.router,
        user.router,
        folder.router

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

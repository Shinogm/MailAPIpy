from app.services.fastapi import App
from app.routes.routers import contact
from app.models.static_dir import StaticDir
def main():
    app = App(
    routers=[
        contact.router,
        
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

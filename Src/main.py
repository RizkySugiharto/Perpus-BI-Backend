from fastapi import FastAPI
from Src.routers import auth, accounts, books, loans, members
from Src.database import create_db_and_tables
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:80",
        "http://localhost:5500",
        "https://perpus-bi-admin.vercel.app",
        "http://perpus-bi-admin.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event('startup')
def on_startup():
    create_db_and_tables()

@app.get('/')
async def root():
    return {'Hello': 'World!'}

app.include_router(auth.router, tags=['authentication'])
app.include_router(accounts.router, tags=['account'])
app.include_router(members.router, tags=['members'])
app.include_router(books.router, tags=['book'])
app.include_router(loans.router, tags=['loan'])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[os.path.dirname(os.path.abspath(__file__))],
        reload_excludes=[
            "*/.git/*",
            "*/__pycache__/*",
            "*.pyc",
            "*/.pytest_cache/*",
            "*/.vscode/*",
            "*/.idea/*"
        ],
        reload_delay=1,
        reload_includes=["*.py"]
    )
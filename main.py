from fastapi import FastAPI
from db.db import engine, Base
from api.routes import router
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="X-Ray Analysis API",
    description="AI-powered X-Ray diagnosis system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
   
   return {

    "message": "Welcome to X-Ray Analysis API",
    "docs": "/docs"


   }

@app.get("/health")
async def health_check():
    try:
        with engine.connect() as connection:
           connection.execute(text("SELECT  1"))
        

        return {
            "status": "healthy",
            "database": "connected",
            "message": "PostgreSQL connected successfully"
        }
        
    except Exception as e:
     return {
            "status": "unhealthy", 
            "database": "disconnected",
            "error": str(e)
        }



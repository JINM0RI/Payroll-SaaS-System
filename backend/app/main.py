from fastapi import FastAPI
from .database import engine, Base
from .auth.routes import router as auth_router
from .payroll.routes import router as payroll_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Payroll SaaS Backend Running"}

app.include_router(payroll_router, prefix="/payroll", tags=["Payroll"])

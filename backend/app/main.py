
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .auth.routes import router as auth_router
from .payroll.routes import router as payroll_router
from .employees.routes import router as employee_router
from app.dashboard.routes import router as dashboard_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Payroll SaaS Backend Running"}

app.include_router(payroll_router, prefix="/payroll", tags=["Payroll"])

app.include_router(employee_router)
app.include_router(dashboard_router)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserLogin, Token
from .utils import hash_password, verify_password, create_access_token
from ..auth.dependencies import get_current_user
from ..auth.dependencies import get_current_user_optional

router = APIRouter()

@router.post("/register")
def register(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    email = data.get("email")
    password = data.get("password")
    admin_password = data.get("admin_password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Missing fields")

    user_count = db.query(User).count()

    # FIRST USER → NO AUTH REQUIRED
    if user_count == 0:
        role = "admin"

    # USERS EXIST → AUTH REQUIRED
    else:
        if not current_user or current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")

        if not admin_password:
            raise HTTPException(status_code=400, detail="Admin password required")

        # verify admin password again
        if not verify_password(admin_password, current_user.password_hash):
            raise HTTPException(status_code=401, detail="Admin password incorrect")

        role = "user"

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=email,
        password_hash=hash_password(password),
        role=role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/user-count")
def get_user_count(db: Session = Depends(get_db)):
    count = db.query(User).count()
    return {"count": count}
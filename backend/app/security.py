from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Fake user authentication for now
def get_current_user(db: Session = Depends(get_db)):

    # for demo we assume admin user
    user = db.query(User).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def RequirePrivilege(permission: str):

    def checker(current_user: User = Depends(get_current_user)):

        permissions = current_user.role.permissions.split(",")

        if permission not in permissions:
            raise HTTPException(status_code=403, detail="Permission denied")

        return current_user

    return checker
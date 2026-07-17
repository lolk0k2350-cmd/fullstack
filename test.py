from app.database import SessionLocal
from app.models.user import User, UserRole

db = SessionLocal()

try:
    user = db.query(User).filter(User.email == "string@com").first()

    if user is None:
        raise RuntimeError("User not found")

    user.role = UserRole.ADMIN.value
    db.commit()
finally:
    db.close()

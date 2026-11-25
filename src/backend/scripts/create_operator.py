
from getpass import getpass

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Operator
from app.services.security import hash_password


VALID_ROLES = {"OPERATOR", "SUPERVISOR", "ADMIN"}


def create_operator():
    print("\n=== Create Operator Account ===\n")

    email = input("Email: ").strip().lower()
    role = input("Role (OPERATOR/SUPERVISOR/ADMIN): ").strip().upper()

    if not email or "@" not in email:
        print("Invalid email address.")
        return

    if role not in VALID_ROLES:
        print("Invalid role.")
        return

    password = getpass("Password: ")
    confirmation = getpass("Confirm password: ")

    if password != confirmation:
        print("Passwords do not match.")
        return

    if len(password) < 12:
        print("Password must be at least 12 characters.")
        return

    db = SessionLocal()

    try:
        existing = db.execute(
            select(Operator).where(Operator.email == email)
        ).scalar_one_or_none()

        if existing:
            print("An account with that email already exists.")
            return

        operator = Operator(
            email=email,
            password_hash=hash_password(password),
            role=role,
            is_active=True,
        )

        db.add(operator)
        db.commit()

        print("\nAccount created successfully!")
        print(f"Email: {operator.email}")
        print(f"Role: {operator.role}")
        print(f"ID: {operator.id}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_operator()

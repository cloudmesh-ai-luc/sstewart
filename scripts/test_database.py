
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Operator


def main():
    db = SessionLocal()

    try:
        operator = Operator(
            email="migration-test@example.com",
            password_hash="temporary-test-hash",
            role="ADMIN",
        )

        db.add(operator)
        db.commit()
        db.refresh(operator)

        print(f"Created operator: {operator.id}")

        saved_operator = db.scalar(
            select(Operator).where(
                Operator.email == "migration-test@example.com"
            )
        )

        print(f"Retrieved operator: {saved_operator.email}")
        print(f"Role: {saved_operator.role}")

        db.delete(saved_operator)
        db.commit()

        print("CRUD test passed!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()

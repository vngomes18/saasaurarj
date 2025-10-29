import sys, os

# Ensure project root is on sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app, db, User


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/set_role.py <email> <role>")
        print("role: admin | user")
        sys.exit(1)

    email = sys.argv[1]
    role = sys.argv[2].lower()
    if role not in ("admin", "user"):
        print("Invalid role:", role)
        sys.exit(2)

    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print("User not found:", email)
            sys.exit(3)

        user.role = role
        db.session.commit()
        print(f"Updated {email} role to {role}")


if __name__ == "__main__":
    main()
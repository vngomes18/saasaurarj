import sys, os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app, db, User, Empresa


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/set_empresa_plan.py <user_email> <plan_tier>")
        print("plan_tier: free | freepremium | premium")
        sys.exit(1)

    email = sys.argv[1]
    plan = sys.argv[2].lower()
    if plan not in ("free", "freepremium", "premium"):
        print("Invalid plan tier:", plan)
        sys.exit(2)

    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print("User not found:", email)
            sys.exit(3)
        empresa = Empresa.query.filter_by(nome=user.empresa).first()
        if not empresa:
            print("Empresa not found for:", user.empresa)
            sys.exit(4)

        empresa.plan_tier = plan
        db.session.commit()
        print(f"Updated Empresa '{empresa.nome}' to {plan}")


if __name__ == "__main__":
    main()
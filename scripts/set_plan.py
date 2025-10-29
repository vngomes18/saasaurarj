import sys, os
# Ensure project root is on sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app, db, User, get_user_settings, update_user_settings


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/set_plan.py <email> <plan_tier>")
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

        update_user_settings(user.id, plan_tier=plan)
        print(f"Updated {email} to {plan}")


if __name__ == "__main__":
    main()
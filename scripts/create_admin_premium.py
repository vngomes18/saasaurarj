import sys
import os

# Garantir que o diretório raiz do projeto esteja no PYTHONPATH
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app, db, User, Empresa


def main():
    if len(sys.argv) < 5:
        print("Usage: python scripts/create_admin_premium.py <email> <username> <empresa_nome> <password>")
        print("Example: python scripts/create_admin_premium.py admin.premium@example.com adminpremium 'Empresa Premium' Admin@12345")
        return

    email = sys.argv[1].strip()
    username = sys.argv[2].strip()
    empresa_nome = sys.argv[3].strip()
    password = sys.argv[4].strip()

    with app.app_context():
        # Garantir empresa com plano premium
        empresa = Empresa.query.filter_by(nome=empresa_nome).first()
        if not empresa:
            empresa = Empresa(nome=empresa_nome, plan_tier='premium')
            db.session.add(empresa)
            db.session.commit()
            print(f"Created company '{empresa_nome}' with premium plan.")
        else:
            if empresa.plan_tier != 'premium':
                empresa.plan_tier = 'premium'
                db.session.commit()
                print(f"Updated company '{empresa_nome}' to premium plan.")
            else:
                print(f"Company '{empresa_nome}' already premium.")

        # Criar usuário admin vinculado à empresa
        user = User.query.filter_by(email=email).first()
        if user:
            print(f"User with email {email} already exists (role={user.role}, empresa_id={user.empresa_id}).")
        else:
            user = User(
                username=username,
                email=email,
                empresa=empresa.nome,
                empresa_id=empresa.id,
                role='admin'
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"Created admin user {email} for company '{empresa_nome}'.")

        print("Done.")


if __name__ == '__main__':
    main()
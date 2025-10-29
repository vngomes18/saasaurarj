import os
import sys

# Ensure project root in path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app, db, User, Empresa


def main():
    with app.app_context():
        # Criar Empresas a partir de nomes únicos existentes
        nomes = db.session.execute(db.text("SELECT DISTINCT empresa FROM \"user\""))
        count_created = 0
        for row in nomes:
            nome = row[0]
            if not nome:
                continue
            existing = Empresa.query.filter_by(nome=nome).first()
            if not existing:
                emp = Empresa(nome=nome, plan_tier='free', billing_status='active')
                db.session.add(emp)
                count_created += 1
        db.session.commit()
        print(f"Empresas criadas: {count_created}")

        # Vincular users a empresa_id
        updated = 0
        users = User.query.all()
        for u in users:
            emp = Empresa.query.filter_by(nome=u.empresa).first()
            if emp:
                # Adiciona coluna empresa_id se existir no modelo
                if hasattr(u, 'empresa_id'):
                    setattr(u, 'empresa_id', emp.id)
                    updated += 1
        db.session.commit()
        print(f"Users atualizados com empresa_id: {updated}")


if __name__ == '__main__':
    main()
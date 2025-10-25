import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

# Fonte (SQLite) e destino (Postgres)
SQLITE_URL = "sqlite:///instance/saas_sistema.db"
load_dotenv()
POSTGRES_URL = os.getenv("DATABASE_URL")

# Ordem para respeitar chaves estrangeiras comuns do app
TABLE_ORDER = [
    "user",
    "user_settings",
    "produto",
    "cliente",
    "fornecedor",
    "compra",
    "item_compra",
    "venda",
    "item_venda",
    "produto_auxiliar",
    "nota_fiscal",
    "ticket_suporte",
    "resposta_ticket",
]


def reflect_tables(engine: Engine, table_names):
    metadata = MetaData()
    tables = {}
    for name in table_names:
        # No SQLite não há schema; no Postgres usamos public
        schema = "public" if engine.url.get_backend_name().startswith("postgresql") else None
        tables[name] = Table(name, metadata, autoload_with=engine, schema=schema)
    return tables


def main():
    if not POSTGRES_URL:
        raise RuntimeError("DATABASE_URL não encontrado nas variáveis de ambiente (.env)")

    src_engine = create_engine(SQLITE_URL)
    dst_engine = create_engine(POSTGRES_URL)

    src_tables = reflect_tables(src_engine, TABLE_ORDER)
    dst_tables = reflect_tables(dst_engine, TABLE_ORDER)

    with src_engine.connect() as src_conn, dst_engine.begin() as dst_tx:
        try:
            for table_name in TABLE_ORDER:
                src_table = src_tables[table_name]
                dst_table = dst_tables[table_name]

                rows = src_conn.execute(select(src_table)).mappings().all()
                if not rows:
                    print(f"Tabela {table_name}: 0 registros (nada a copiar)")
                    continue

                pk_cols = [c.name for c in dst_table.primary_key.columns]
                copiados = 0
                for r in rows:
                    payload = dict(r)
                    if pk_cols:
                        stmt = pg_insert(dst_table).values(payload).on_conflict_do_nothing(index_elements=pk_cols)
                    else:
                        stmt = pg_insert(dst_table).values(payload).on_conflict_do_nothing()
                    dst_tx.execute(stmt)
                    copiados += 1
                print(f"Tabela {table_name}: tentados {copiados} registros (duplicatas ignoradas)")

            print("Migração concluída com sucesso.")
        except SQLAlchemyError as e:
            raise


if __name__ == "__main__":
    main()


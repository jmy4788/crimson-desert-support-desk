from __future__ import annotations

from collections.abc import Generator

from fastapi import Request
from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine


def normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgres://"):
        return "postgresql+psycopg://" + database_url[len("postgres://") :]
    if database_url.startswith("postgresql://"):
        return "postgresql+psycopg://" + database_url[len("postgresql://") :]
    return database_url


def create_db_engine(database_url: str):
    normalized_url = normalize_database_url(database_url)
    connect_args = {"check_same_thread": False} if normalized_url.startswith("sqlite") else {}
    return create_engine(normalized_url, connect_args=connect_args)


def ensure_search_index(engine) -> None:
    if engine.dialect.name != "sqlite":
        return
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(
                    entity_type,
                    entity_key,
                    title,
                    body,
                    platforms,
                    updated_at UNINDEXED,
                    locale UNINDEXED
                )
                """
            )
        )


def init_database(engine) -> None:
    SQLModel.metadata.create_all(engine)
    ensure_search_index(engine)


def reset_database(engine) -> None:
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    ensure_search_index(engine)


def get_session(request: Request) -> Generator[Session, None, None]:
    with Session(request.app.state.engine) as session:
        yield session

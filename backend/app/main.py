from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings
from app.database import create_db_engine, init_database
from app.routers import admin, doctor, faq, health, issues, patches, search
from app.services.seed import database_is_empty, seed_database


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    engine = create_db_engine(settings.database_url)
    init_database(engine)

    if settings.auto_seed_on_start and settings.seed_path.exists() and database_is_empty(engine):
        seed_database(engine, settings.seed_path)

    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.state.settings = settings
    app.state.engine = engine
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router, prefix=settings.api_prefix)
    app.include_router(patches.router, prefix=settings.api_prefix)
    app.include_router(issues.router, prefix=settings.api_prefix)
    app.include_router(faq.router, prefix=settings.api_prefix)
    app.include_router(search.router, prefix=settings.api_prefix)
    app.include_router(doctor.router, prefix=settings.api_prefix)
    app.include_router(admin.router, prefix=settings.api_prefix)
    return app


app = create_app()


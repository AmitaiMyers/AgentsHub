"""FastAPI dependencies shared by the REST API and the web pages."""
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from agentshub.config import Settings
from agentshub.db import Database


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def db_session(request: Request) -> Iterator[Session]:
    database: Database = request.app.state.database
    with database.transaction() as db:
        yield db


DB = Annotated[Session, Depends(db_session)]
AppSettings = Annotated[Settings, Depends(get_settings)]

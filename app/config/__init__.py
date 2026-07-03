import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from dotenv import load_dotenv

from .constant import allConstant


load_dotenv()


def build_database_uri():
    database_url = os.getenv("DATABASE_URL") or os.getenv("DIRECT_URL")
    if database_url:
        return normalize_database_uri(database_url)

    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "rungta_employee")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    return "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        user,
        password,
        host,
        port,
        database,
    )


def normalize_database_uri(database_url):
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    parsed = urlsplit(database_url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    if parsed.hostname and parsed.hostname.endswith(".supabase.co"):
        query.setdefault("sslmode", "require")

    return urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urlencode(query),
            parsed.fragment,
        )
    )


class Config:
    SQLALCHEMY_DATABASE_URI = build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_MASK_SWAGGER = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", "60")
    )
    JWT_REFRESH_TOKEN_EXPIRES_DAYS = int(
        os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", "30")
    )


__all__ = ["Config", "allConstant", "build_database_uri"]

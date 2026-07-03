from app.utils.exceptions import AppError


def abort_app_error(namespace, exc):
    if isinstance(exc, AppError):
        namespace.abort(exc.status_code, exc.message)
    raise exc


import re

from sqlalchemy.exc import DataError, IntegrityError

from app.extensions import db
from app.utils.exceptions import BadRequestError, ConflictError


UNIQUE_FIELD_RE = re.compile(r"Key \((?P<field>[^)]+)\)=")


class BaseRepository:
    model = None

    def list_all(self):
        return self.model.query.order_by(self.model.id).all()

    def get_by_id(self, record_id):
        return db.session.get(self.model, record_id)

    def add(self, entity):
        db.session.add(entity)
        return entity

    def delete(self, entity):
        db.session.delete(entity)

    def commit(self):
        try:
            db.session.commit()
        except IntegrityError as exc:
            db.session.rollback()
            raise ConflictError(format_integrity_error(exc))
        except DataError as exc:
            db.session.rollback()
            raise BadRequestError("Invalid data: {}".format(exc.orig))


def format_integrity_error(exc):
    message = str(exc.orig)
    match = UNIQUE_FIELD_RE.search(message)
    if match:
        field_name = match.group("field").replace("_", " ")
        return "The {} is already exists, Check the data and try again".format(
            field_name
        )

    return "Duplicate or invalid data"

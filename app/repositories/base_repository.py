from sqlalchemy.exc import DataError, IntegrityError

from app.extensions import db
from app.utils.exceptions import BadRequestError, ConflictError


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
            raise ConflictError("Duplicate or invalid data: {}".format(exc.orig))
        except DataError as exc:
            db.session.rollback()
            raise BadRequestError("Invalid data: {}".format(exc.orig))


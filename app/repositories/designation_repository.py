from app.models import Designation

from .base_repository import BaseRepository


class DesignationRepository(BaseRepository):
    model = Designation


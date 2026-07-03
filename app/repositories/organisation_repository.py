from app.models import Organisation

from .base_repository import BaseRepository


class OrganisationRepository(BaseRepository):
    model = Organisation


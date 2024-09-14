from typing import Any
from django.db.models import Manager

class bookmarkManager(Manager):
    def secure_url(self, url: str):
        pass

    def validate_icon(self, icon):
        pass

    def create(self, **kwargs: Any) -> Any:
        return super().create(**kwargs)
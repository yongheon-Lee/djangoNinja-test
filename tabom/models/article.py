from typing import Any, List

from django.db import models

from tabom.models.base_model import BaseModel


class Article(BaseModel):
    title = models.CharField(max_length=255)
    my_likes: List[Any]  # to_attr에 정의했던 필드 추가

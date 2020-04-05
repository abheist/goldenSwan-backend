import uuid

from django.contrib.auth import get_user_model
from django.db import models


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), blank=False, unique=True)
    slug = models.SlugField(max_length=120)
    title = models.CharField(blank=False, null=False)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

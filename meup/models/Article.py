import uuid

from django.contrib.auth import get_user_model
from django.db import models


class Article(models.Model):
    slug = models.SlugField(max_length=120, blank=False, null=False, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(blank=False, null=False, max_length=100)
    subtitle = models.CharField(max_length=140, blank=True)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    published = models.BooleanField(blank=False, default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

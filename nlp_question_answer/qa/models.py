from django.db import models


class Pages(models.Model):
    url = models.URLField()
    title = models.TextField()
    h1 = models.TextField()
    h2 = models.TextField()
    h3 = models.TextField()
    h4 = models.TextField()
    h5 = models.TextField()
    p = models.TextField()
    div = models.TextField()
    dt = models.DateTimeField(auto_now=True)

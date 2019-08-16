from django.db import models

# Create your models here.

class URL(models.Model):
    url = models.URLField(max_length=300)
    hashed_url = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return "URL: " + self.url + "  Hashed: " + self.hashed_url
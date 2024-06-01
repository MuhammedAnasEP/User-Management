from django.db import models

# Create your models here.

class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.IntegerField()
    email = models.EmailField(unique=True)
    web = models.URLField(blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
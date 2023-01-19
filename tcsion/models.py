from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email=models.EmailField()
    message=models.TextField()
    def __str__(self):
        return self.first_name
class NewsLetter(models.Model):
    email=models.EmailField(unique=True)
    def __str__(self):
        return self.email

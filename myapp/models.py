from django.db import models

# Create your models here.
class profile(models.Model):
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()

    def __str__(self):
        return self.gender

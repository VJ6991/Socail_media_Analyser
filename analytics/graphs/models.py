from django.db import models

class Graph(models.Model):
    date=models.DateField()
    name=models.CharField(max_length=60)
    gender=models.CharField(max_length=40)
    age=models.IntegerField()
    country=models.CharField(max_length=60)
    likes=models.IntegerField()
    Views=models.IntegerField()

    def __str__(self):
        return self.name

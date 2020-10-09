from django.db import models

# Create your models here.
class Question(models.Model):
    kind = models.CharField(max_length=1, default='0')
    question = models.CharField(max_length=1023, default='none')
    A = models.CharField(max_length=511, default='none')
    B = models.CharField(max_length=511, default='none')
    C = models.CharField(max_length=511, default='none')
    D = models.CharField(max_length=511, default='none')
    answer = models.CharField(max_length=2, default='0')
    difficulty = models.IntegerField(max_length=1, default=-1)

    no = models.IntegerField(default=0)

    wrong = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
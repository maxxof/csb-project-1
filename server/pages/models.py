from django.db import models

from django.contrib.auth.models import User

# Create your models here.
# class User(models.Model):
# 	username = models.TextField()
# 	password = models.TextField()

class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	balance = models.IntegerField()

from django.db import models

# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class client(models.Model):
    name = models.CharField(max_length=50)
    account = models.CharField(max_length=50)
    cloud = models.CharField(max_length=20)
    api_id = models.CharField(max_length=50)
    api_key = models.CharField(max_length=50)
    user = models.ForeignKey(user, on_delete=models.CASCADE)


class check(models.Model):
    date = models.DateField(max_length=50)
    method = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    detail = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    product = models.CharField(max_length=50)
    manager = models.CharField(max_length=50)
    cli = models.ForeignKey(client, on_delete=models.CASCADE)

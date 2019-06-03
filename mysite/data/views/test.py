from django.db.models import QuerySet
from data import models
name = 'bubble'
user_info = models.user.objects.filter(name=name)
print("In Line17:%s" % user_info)
for i in user_info:
    print(i)
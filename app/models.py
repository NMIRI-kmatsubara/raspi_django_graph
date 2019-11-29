from django.db import models
from django.utils import timezone
# Create your models here.


class Raspi_data(models.Model):
    data1 = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)

from django.db import models

# Create your models here.
class Motion_status(models.Model):
    cmdPos = models.FloatField()
    actPos = models.FloatField()
    cmdVel = models.FloatField()


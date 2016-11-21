from django.db import models

# Create your models here.

class stockportfolio(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    name = models.CharField(max_length=10)
    exchange = models.CharField(max_length=10)
    close = models.DecimalField(decimal_places=2, max_digits=8)
    volume = models.DecimalField(decimal_places=2, max_digits=20)
    strategy = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


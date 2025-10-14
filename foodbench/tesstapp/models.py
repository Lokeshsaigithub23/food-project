from django.db import models

# Create your models here.
from django.db import models

class restaurant(models.Model):
    name=models.CharField(max_length=100)
    image=models.URLField()
    location=models.CharField(max_length=100)
    rating=models.FloatField()
    def __str__(self):
        return self.name

class fooditem(models.Model):
    restaurant=models.ForeignKey(restaurant,on_delete=models.CASCADE,related_name='menu')
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=5, decimal_places=2)
    image=models.URLField()
    description=models.TextField()
    
    def __str__(self):
        return self.name
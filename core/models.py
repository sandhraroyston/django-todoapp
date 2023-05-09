from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Task(models.Model):
    STATUS=(
        ('done','done'),
        ('pending','pending')
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=150)
    desc=models.TextField(null=True,blank=True)
    date=models.DateTimeField()
    status=models.CharField(max_length=20,choices=STATUS,null=True,blank=True)
    def __str__(self):
        return self.title

    def remaining_days(self):
        remaining = (self.date.date() - datetime.now().date()).days
        return remaining
    class Meta:
        ordering = ["-status"]

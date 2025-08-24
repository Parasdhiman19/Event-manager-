from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime

# Create your models here.

class EmailOpt(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    def is_expired(self):
     return self.created_at < timezone.now() - datetime.timedelta(minutes=5)
class MyUser(AbstractUser):
  subscription_active = models.BooleanField(default=False)
  
  def can_create_event(self):
    return self.subscription_active 
  
  




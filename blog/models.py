from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key = True)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.comment[0:13] + "..." + " by " + self.user.username 

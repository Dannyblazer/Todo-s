from django.db import models
from users.models import Account

# Create your models here.
class BlogPost(models.Model):
    title           = models.CharField(max_length=50, null=False, blank=False)
    subTitle        = models.CharField(max_length=50, null=False, blank=False)
    body            = models.TextField(max_length=5000, null=False, blank=False)
    dateCreated     = models.DateTimeField(auto_now_add=True, verbose_name="date created")
    author          = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    def __str__(self): # Two string function
        return self.title


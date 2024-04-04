from django.db import models

# Create your models here.
class BlogPost(models.Model):
    title           = models.CharField(max_length=50, null=False, blank=False)
    body            = models.TextField(max_length=5000, null=False, blank=False)
    subTitle        = models.CharField(max_length=50, null=False, blank=False)
    dateCreated     = models.DateTimeField(auto_now_add=True, verbose_name="date created")
    
    def __str__(self):
        return self.title


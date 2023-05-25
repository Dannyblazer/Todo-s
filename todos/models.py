from django.db import models

# Create your models here.
class Todo(models.Model):
    # user = models.ForeignKey
    content = models.CharField(max_length=50, unique=False)
    timer   = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    priority = models.CharField(max_length=25, unique=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.content



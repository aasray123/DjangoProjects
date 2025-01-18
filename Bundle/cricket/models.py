from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GameGroup(models.Model):
    group_name = models.CharField(max_length = 128, unique = True)
    users_active = models.ManyToManyField(User, related_name='online_in_groups', blank = True)
    
    def __str__(self):
        return self.group_name
    

class Score(models.Model):
    group = models.ForeignKey(GameGroup, related_name="points", on_delete=models.CASCADE)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    isBatter = models.BooleanField()
    score = models.IntegerField()
    event = models.IntegerField()

    def __str__(self):
        return f'{self.author.username} : {self.isBatter} : {self.score} : {self.event}'
    
    class Meta:
        ordering = ['-event']

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    follows = models.ManyToManyField('self',related_name='followed_by',
                                    symmetrical=False,blank=True)
    bio = models.TextField(default='No Bio',blank=True)
    profile_image = models.ImageField(default='default_profile.png')
    linkedin_id=models.CharField(max_length=120,blank=True,null=True,default='s')
    instagram_id=models.CharField(max_length=120,blank=True,null=True,default='s')
    telegram_id=models.CharField(max_length=120,blank=True,null=True,default='s')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username
    
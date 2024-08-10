from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save,sender=User)
def post_save_create_profile(sender,instance,created,**kwargs): 
    if created:
        #Profile.objects.create(user=instance)
        user_profile=Profile(user=instance)
        user_profile.save()
        #Each user should follow him/herself
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

#post_save.connect(post_save_create_profile,sender=User) => without the decorator        


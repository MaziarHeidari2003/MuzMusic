from django.db import models
# Create your models here.

choices=[('music','music'),('programming','programming'),('life','life'),('studies','studies')]
class Maziar(models.Model):
    title=models.CharField(max_length=120)
    content=models.TextField()
    category=models.CharField(max_length=40,choices=choices,default='music')
    image_file=models.ImageField(null=True,blank=True)
    video_file=models.FileField(null=True,blank=True)
    audio_file=models.FileField(null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
from django.db import models
from django.core.validators import URLValidator
from django.contrib.auth.models import User
from django.dispatch import receiver
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.CharField(max_length=350) 
    profile_pic = models.ImageField(upload_to='ProfilePicture/')
    profile_avatar = models.ImageField(upload_to='AvatorPicture/')
    date = models.DateTimeField(auto_now_add=True, null= True)  
    
    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile():
        self.save()

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Project(models.Model):
    title = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = 'projects/')
    description = models.TextField(max_length=1000)
    link=models.TextField(validators=[URLValidator()],null=True)
    profile = models.ForeignKey(User,on_delete=models.CASCADE, null=True)   
    design=models.PositiveIntegerField(choices=list(zip(range(1,11),range(1, 11))), default=1)
    userbility = models.PositiveIntegerField(choices=list(zip(range(1, 11), range(1, 11))), default=1)
    content=models.PositiveIntegerField(choices=list(zip(range(1, 11), range(1, 11))), default=1)
    
    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    @classmethod
    def search_project(cls, name):
        pro = Project.objects.filter(title__icontains = name)
        return pro 

class Review(models.Model):
    design = models.IntegerField(default=0)
    usability = models.IntegerField(default=0)
    content = models.IntegerField(default=0)
    average = models.IntegerField(default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def save_review(self):
        self.save()

    def delete_review(self):
        self.delete()

class Comments (models.Model):
    post = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    comment_post = models.CharField(max_length=150)
    author = models.ForeignKey(User,related_name='commenter' , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

class Likes(models.Model):
    user_liked = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liked')
    liked_post = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='likes')

    def save_like(self):
        self.save()
    
    def __str__(self):
        return self.user_liked 
                                                          
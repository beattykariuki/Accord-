from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.CharField(max_length=350) 
    profile_pic = models.ImageField(upload_to='ProfilePicture/')
    profile_avatar = models.ImageField(upload_to='AvatorPicture/')
    date = models.DateTimeField(auto_now_add=True, null= True)  

    def __str__(self):
        return self.profile.user
        
class Image(models.Model):
    image = models.ImageField(upload_to ='pictsagram/')
    image_caption = models.CharField(max_length=700)
    tag_someone = models.CharField(max_length=50,blank=True)
    imageuploader_profile = models.ForeignKey(User, on_delete=models.CASCADE,null='True', blank=True)
    image_likes = models.ManyToManyField(User, default=False, blank=True, related_name='likes')
    date = models.DateTimeField(auto_now_add=True, null= True)

    def __str__(self):
        return self.image_caption
    
    @property
    def count_likes(self):
        likes = self.likes.count()

    def like(self,photo):
        if self.mylikes.filter(photo=photo).count() == 0:
            Likes(photo=photo, User=self().save)

class Comments (models.Model):

    post = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    comment_post = models.CharField(max_length=150)
    author = models.ForeignKey(User,related_name='commenter' , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

class Likes(models.Model):
    user_liked = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes')
    liked_post = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name='likes')

    def save_like(self):
        self.save()
    
    def __str__(self):
        return self.user_liked

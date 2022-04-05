from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.
class Profile(models.Model):
    profile =models.ImageField(upload_to ='photos/',blank=True)
    bio =models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(blank=True, max_length=120)

    def __str__(self):

        return self.bio

    def save_profile(self):
        self.save()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

   
    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()


    @classmethod
    def filter_profile_by_id(cls,profile):
      profile =cls.objects.filter(id__in=profile) 
      return profile      





class Image(models.Model):
    name =models.CharField(max_length=60)
    caption=models.CharField(max_length=200)
    image =models.ImageField(upload_to ='photos/',blank=True)
    likes =models.IntegerField(default=0)
    dislikes=models.IntegerField(default=0)
    pub_date=models.DateTimeField(auto_now_add=True)
    profile =models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)

    def __str__(self):

        return self.name

    class Meta:
        ordering = ['name'] 

    def save_profile(self):
        self.save() 


    @classmethod    
    def delete_image(cls,id):
        image =cls.objects.filter(image_id=id).delete()
        return image      

    @classmethod
    def update_caption(cls,image_id,caption):
        caption = cls.objects.filter(id=image_id).update(caption =caption) 
        return caption 

    
    @classmethod
    def filter_by_profile(cls,profile) :
        
        images =cls.objects.filter(profile__in=profile) 
        return images  

    @classmethod     
    def  search_image_by_name(cls,search_term):
        images =cls.objects.filter(name__icontains=search_term)   
        return images  
        


class Preference(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image =models.ForeignKey(Image,on_delete=models.CASCADE)
    value =models.IntegerField()
    date =models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.user) + ':' + str(self.image) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "image", "value")

    def save_preference(self):
        self.save()   

class Comments(models.Model):
    comment = models.TextField(max_length = 300)
    image = models.ForeignKey(Image,null=True, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    comment_date = models.DateTimeField(auto_now_add=True) 
    
    
    class Meta:
        ordering = ["-comment_date"]


    def __str__(self):
        return f'{self.user.name} Image'

    

class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'

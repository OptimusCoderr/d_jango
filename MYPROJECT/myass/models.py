from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.
class User(AbstractUser):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True, null=True)
    bio=models.TextField(null=True)

    avatar=models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]


class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model): #The Room database was created
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)#if you set_null you need to set that null to be true unless an error will be
    name= models.CharField(max_length=200)
    description= models.TextField(null=True, blank=True)# Null to true means that the Text field can be left empty
    participants= models.ManyToManyField(
        User, related_name='participants',blank=True)
    update= models.DateTimeField(auto_now=True)#auto_now takes a snapshot of every thing we save
    created= models.DateTimeField(auto_now_add=True)# auto_now_add a snapshot of when it was created firstly

    class Meta:
        ordering=['-update','-created']#ORDERING
    
    def __str__(self):#__str__ is a string representation
        return self.name
    



class Message(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    room= models.ForeignKey(Room, on_delete=models.CASCADE)#CASCADE means when a room is deleted othe children gets deleted
    body= models.TextField()
    update= models.DateTimeField(auto_now=True)#auto_now takes a snapshot of every thing we save
    created= models.DateTimeField(auto_now_add=True)# auto_now_add a snapshot of when it was created firstly

    class Meta:
        ordering=['-update','-created'] 
    
    def __str__(self):#__str__ is a string representation
        return self.body[0:50]


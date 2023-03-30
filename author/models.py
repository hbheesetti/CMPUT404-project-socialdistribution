from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid
from django.db.models import Q
from django.urls import reverse
from django.conf import settings


defaultfrd = []
# Create your models here.
class Author(models.Model):
    id = models.CharField(primary_key=True, editable=False, default= uuid.uuid4, max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  #1-1 with django user
    friends = models.CharField(blank=False, default=defaultfrd, max_length=1000)
    displayName = models.CharField(max_length=50, blank=False)  # displayed name of author
    profileImage = models.URLField(editable=True,blank=True, max_length=500) # profile image of author, optional
    url = models.URLField(editable=False, max_length=500)  # url of author profile
    host = models.URLField(editable=False, max_length=500, default="https://sociallydistributed.herokuapp.com/")  # host server
    github = models.URLField(max_length=500, default="", blank=True)  # Github url field

    # make it pretty
    def __str__(self):
        return self.displayName + " (" + str(self.id) + ")"
    
    # return type of model
    @staticmethod
    def get_api_type():
        return 'author'
    
    def get_absolute_url(self):
        # get the url for a single author
        url = reverse('authors:detail', args=[str(self.id)])
        url = settings.APP_NAME + url
        self.url = url if url.endswith('/') else url + '/'
        self.save()
        return self.url
    
    def update_fields_with_request(self, request):
        self.url = request.build_absolute_uri(self.get_absolute_url())
        self.host = request.build_absolute_uri('/') 
        self.save()
    
    # return the author public ID
    def get_public_id(self):
        self.get_absolute_url()
        return (self.url)[:-1] or str(self.id)   
    
    def follower_to_object(self):
        return {"type":"author",
            "id":self.id,
            "url":self.url,
            "host":self.host,
            "displayName":self.displayName,
            "github":self.github,
            "profileImage":self.profileImage
        }
        
class Inbox(models.Model):
    id = models.CharField(primary_key=True, editable=False, default= uuid.uuid4, max_length=255)
    author = models.ForeignKey(Author, related_name="inbox", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(blank=True, null=True,max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')
    published = models.DateTimeField(auto_now_add=True, editable=False)  # date published

    def __str__(self):
        return self.id
    
    @staticmethod
    def get_api_type():
        return 'inbox'
    
    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        ordering = ['-published']

class FollowRequest(models.Model):
    actor = models.CharField(blank=False,  max_length=1000, editable=False)
    object = models.CharField(blank=False, max_length=1000, editable=False)
    summary = models.CharField(max_length=255, default = '')
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('actor','object')
    
    @staticmethod
    def get_api_type():
        return 'Follow'
    
    def get_summary(self):
        summary  = self.actor.displayName + " wants to follow " + self.object.displayName
        return summary
    
    def __str__(self):
        return f'{self.actor} follow {self.object}'

class Node(models.Model):   
    id = models.CharField(primary_key=True, editable=False, default= uuid.uuid4, max_length=255) 
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=30)
    name = models.CharField(max_length=255, default='Node')
    is_active = models.BooleanField(default=False)
    url = models.URLField(editable=False, default='https://sociallydistributed.herokuapp.com/', max_length=500)
    # objects = MyNodeManager()

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'Node' 

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid

from django.urls import reverse

APP_NAME = 'http://127.0.0.1:8000'

# Create your models here.
class Author(models.Model):
    id = models.CharField(primary_key=True, editable=False, default= uuid.uuid4, max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  #1-1 with django user
    friends = models.ManyToManyField('self',blank=True, symmetrical=True)  # M-M with django
    displayName = models.CharField(max_length=50, blank=False)  # displayed name of author
    profileImage = models.URLField(editable=True,blank=True, max_length=500) # profile image of author, optional
    url = models.URLField(editable=False, max_length=500)  # url of author profile
    host = models.URLField(editable=False, max_length=500)  # host server

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
        return url[:-1] if url.endswith('/') else url 
    
    def update_fields_with_request(self, request):
        self.url = request.build_absolute_uri(self.get_absolute_url())
        self.host = request.build_absolute_uri('/') 
        self.save()
    
    # return the author public ID
    def get_public_id(self):
        if not self.url: 
            self.url = self.get_absolute_url()
            self.save()
        return (APP_NAME+self.url) or str(self.id)   
    
    class Meta:
        ordering = ['displayName']

class Inbox(models.Model):
    id = models.CharField(primary_key=True, editable=False, default= uuid.uuid4, max_length=255)
    author = models.ForeignKey(Author, related_name="inbox", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(blank=True, null=True,max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.id
    
    @staticmethod
    def get_api_type():
        return 'inbox'
    
    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        
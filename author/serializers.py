import uuid
from django.urls import reverse
from rest_framework import serializers, exceptions
from .models import *
from django.http import HttpResponse
import client
from Remote.Authors import *

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    url = serializers.URLField(source="get_absolute_url",read_only=True)
    displayName = serializers.CharField(default = 'x')
    
    @staticmethod
    def _upcreate(validated_data):
        author = Author.objects.create(**validated_data)   
        return author
    @staticmethod
    def extract_and_upcreate_author(author, author_id = None):
        print("in upcreate")
        updated_author= None
        if author_id:
            try:
                return Author.objects.get(id=author_id)
            except Author.DoesNotExist:
                
                raise exceptions.ValidationError("Author does not exist")
        try:
            print("AUTHOR ID", author["id"])
            id = author["id"].split("/")[-1]
            updated_author = Author.objects.get(id=id)
        except Author.DoesNotExist:
           # response,code = check_author(id)
           # print(code)
           # if code == 200:
               # updated_author = Author(response)

           #decoupled
            author = clean_author(author)
      
            #print(Author.objects.get(**author))
            #Done so same authro can comment multiple times, not sure if 100% working tho
            updated_authorr = Author(**author)
            updated_author = updated_authorr
            updated_authorr.delete()
            updated_author.save()
            print("updated author saved")
        if not updated_author:
            print("no author", updated_author)
            raise exceptions.ValidationError("Author does not exist")
        else:
            return updated_author
    
    def to_representation(self, instance):
        id = instance.get_public_id()
        return {
            **super().to_representation(instance),
            'id': id
        }
        
    class Meta:
        model = Author
        fields = [
            'type', 
            'id', 
            'url',
            'host',
            'displayName',
            'github',
            'profileImage',
        ]

class FollowRequestSerializer(serializers.ModelSerializer):
    #to_user = serializers.CharField(default = 'x')
    type = serializers.CharField(default="Follow",source="get_api_type",read_only=True)
    summary = serializers.CharField(source="get_summary", read_only=True)

    actor = AuthorSerializer(required=False)
    object = AuthorSerializer(required=False)

    print("DELETING")
    #FollowRequest.objects.all().delete()

    def create(self,validated_data):
        print("in follow req create")
        actor = validated_data["actor"]
        object = validated_data["object"]
        if actor in object.friends.all():
            print("already friends")
            return "already friends"
        if FollowRequest.objects.filter(actor=actor,object=object).exists():
            print("already sent")
            return "already sent"
        if actor==object:
            return "same"
        else:
            return FollowRequest.objects.create(actor=actor,object=object)
    
    # https://www.django-rest-framework.org/api-guide/serializers/
    def to_internal_value(self, data):
        print("to_internal_value")
        actor = AuthorSerializer.extract_and_upcreate_author(author=self.context["actor_"])
        object = Author.objects.get(id=self.context["object_id"])

        # Perform the data validation.
        if not actor:
            raise serializers.ValidationError({
                'actor': 'This field is required.'
            })
        if not object:
            raise serializers.ValidationError({
                'object': 'This field is required.'
            })
        
        return {
            'object': object,
            'actor': actor
        }
        
    class Meta:
        model = FollowRequest
        fields = ['type','summary','actor', 'object']
        
class InboxSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="inbox",source="get_api_type",read_only=True)

    def to_representation(self, instance):
        serializer = self.context["serializer"]
        rep = super().to_representation(instance)
        rep['content_object'] = serializer(instance)
        return rep

    class Meta:
        model = Inbox
        fields = ['type', 'author', 'content_type', 'object_id' ,'content_object']









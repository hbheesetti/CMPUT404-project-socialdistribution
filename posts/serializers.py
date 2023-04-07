from rest_framework import serializers
from .models import *
from .models import Post
from author.serializers import AuthorSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_base64.fields import Base64ImageField
from Remote.Post import clean_post 

class PostSerializer(WritableNestedModelSerializer):
    type = serializers.CharField(default="post",source="get_api_type",read_only=True)
    id = serializers.CharField(source="get_public_id", read_only=True)
    count = serializers.IntegerField(read_only=True, default=0)
    comments = serializers.URLField(source="get_comments_source", read_only=True)
    commentsSrc = serializers.JSONField(read_only=True)
    author = AuthorSerializer(required=False)
    source = serializers.URLField(source="get_source", read_only=True, max_length=500)  # source of post
    origin = serializers.URLField(source="get_origin", read_only=True, max_length=500)  # origin of post
    categories = serializers.CharField(max_length=300, default="")
    
    def create(self, validated_data):
        print("validated post data",validated_data)
        try:
            print("POST TRY BLOCK")
            validated_data = clean_post(validated_data)
            print("valid",validated_data )
            post = Post(**validated_data)
        except Exception as e:
            print(e)
            print("POST SERIALIZER ELSE")
            author = AuthorSerializer.extract_and_upcreate_author(None, author_id=self.context["author_id"])
            #maybe pop the authors in this?***
            validated_data.pop('authors')
            post = Post.objects.create(**validated_data, author = author)
        return post

    def to_internal_value(self, data):
        print("to_internal_value")
        if not ("id" in data): return data
        data["author"] = AuthorSerializer.extract_and_upcreate_author(data['author'])
        if type(data["categories"]) is list:
            data["categories"] = ','.join(data["categories"])                

        return {
            'id': data["id"],
            'type': data["type"],
            'categories': data["categories"],
            'author': data["author"],
            'contentType': data["contentType"],
            'content': data["content"],
            'visibility': data["visibility"],
            'comments': data["comments"],
            'description': data["description"],
            'origin': data["origin"],
            'published': data["published"],
            "source": data["source"],
            "title": data["title"],
            "unlisted": data["unlisted"], 
            'count': 0,
            'is_github': False,
            'commentsSrc': {}
            
        }
    def to_representation(self, instance):
        print("to_representation")
        print(instance)
        id = instance.get_public_id()
        comments_list = Comment.objects.filter(post=instance).order_by('-published')[0:5]
        categories_list = instance.categories.split(",")
        if categories_list == ['']:
            categories_list = []
        commentsSrc = [CommentSerializer(comment,many=False).data for comment in comments_list]
        return {
            **super().to_representation(instance),
            'id': id,
            'commentsSrc': commentsSrc,
            'categories': categories_list,
            'count': len(commentsSrc)
        }
            
    class Meta:
        model = Post
        fields = [
            'type', 
            'title', 
            'id', 
            'source', 
            'origin', 
            'description',
            'contentType',
            'content',
            'author',
            'categories',
            'count',
            'comments',
            'commentsSrc',
            'published',
            'visibility',
            'unlisted',
            #'is_github'
        ]

class CommentSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="comment",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    author = AuthorSerializer()
  
    def create(self, validated_data):
        author = validated_data["author"]
        #id = validated_data.pop('id') if validated_data.get('id') else None
        comment = validated_data["comment"]
        
       # if not id:
        #    id = self.context["id"]
        comment = Comment.objects.create(author = author,  comment = comment, post=validated_data["post"])
        comment.save()

        return comment
    
    def to_internal_value(self, data):
        print("to_internal_value")
        author = AuthorSerializer.extract_and_upcreate_author(self.context["author"])
        print("OBJECT",self.context["object"])
        post = self.context["object"]
        print("reached internal value")
        print("AUTHOR HERE",author)

        print("POST",post)
  
        # object = Author.objects.get(id=self.context["object"])
       
        comment = self.context["comment"]

        # Perform the data validation.
        if not author:
            raise serializers.ValidationError({
                'author': 'This field is required.'
            })
        if not post:
            raise serializers.ValidationError({
                'post': 'This field is required.'
            })
        if not comment:
            raise serializers.ValidationError({
                'comment': 'This field is required.'
            })
       
        
        return {
            'author': author,
            'comment':comment,
            'post': post,
        }

    class Meta:
        model = Comment
        fields = [
            'id',
            'type', 
            'author',
            'comment',
            'contentType',
            'published',
           
        ]
    
class LikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="like",source="get_api_type",read_only=True)
    author = AuthorSerializer(required=True)
    summary = serializers.CharField(source="get_summary", read_only=True)

    def create(self, validated_data):
        # author = AuthorSerializer.extract_and_upcreate_author(validated_data, author_id=self.context["author_id"])
        print("create a like")
        author = validated_data["author"]
        if Like.objects.filter(author=author, object=validated_data.get("object")).exists():
            return "already liked"
        else:
            like = Like.objects.create(**validated_data)
            like.save()
            print("successful")
            return like
    
    def to_internal_value(self, data):
        print("to_internal_value")
        author = AuthorSerializer.extract_and_upcreate_author(self.context["author"])
        # object = Author.objects.get(id=self.context["object"])
        object = self.context["object"]

        # Perform the data validation.
        if not author:
            raise serializers.ValidationError({
                'author': 'This field is required.'
            })
        if not object:
            raise serializers.ValidationError({
                'object': 'This field is required.'
            })
        
        return {
            'object': object,
            'author': author
        }
    
    class Meta:
        model = Like
        fields = [
            "summary",
            "type",
            "author",
            "object",
        ]

class ImageSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="post",source="get_api_type",read_only=True)
    id = serializers.CharField(source="get_public_id", read_only=True)
    count = serializers.IntegerField(read_only=True, default=0)
    comments = serializers.URLField(source="get_comments_source", read_only=True)
    commentsSrc = serializers.JSONField(read_only=True)
    author = AuthorSerializer(required=False)
    source = serializers.URLField(source="get_source", read_only=True, max_length=500)  # source of post
    origin = serializers.URLField(source="get_origin", read_only=True, max_length=500)  # origin of post
    categories = serializers.CharField(max_length=300, default="")
    image = Base64ImageField()
    
    def create(self, validated_data):
        print("validating image data ", validated_data)
        try:
            print("in the try block")
            validated_data = clean_post(validated_data)
            print("valid",validated_data)
            author = AuthorSerializer.extract_and_upcreate_author(None, author_id=self.context["author_id"])
            # validated_data.pop('authors')
            post = Post.objects.create(**validated_data, author = author)
        except Exception as e:
            print("image post serializer except")
            print(e)
            if not author:
                raise serializers.ValidationError({
                    'author': 'This field is required.'
                })
            if not post:
                raise serializers.ValidationError({
                    'post': 'This field is required.'
                })
        return post
    
    def to_representation(self, instance):
        print("to_representation")
        print(instance)
        id = instance.get_public_id()
        comments_list = Comment.objects.filter(post=instance).order_by('-published')[0:5]
        categories_list = instance.categories.split(",")
        if categories_list == ['']:
            categories_list = []
        commentsSrc = [CommentSerializer(comment,many=False).data for comment in comments_list]
        return {
            **super().to_representation(instance),
            'id': id,
            'commentsSrc': commentsSrc,
            'categories': categories_list,
            'count': len(commentsSrc)
        }

    class Meta:
        model = Post
        fields = [
            'type', 
            'title', 
            'id', 
            'source', 
            'origin', 
            'description',
            'contentType',
            'image',
            'author',
            'categories',
            'count',
            'comments',
            'commentsSrc',
            'published',
            'visibility',
            'unlisted',
            #'is_github'
        ]
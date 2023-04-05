import json
from django.db import IntegrityError
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from author.pagination import *
from posts.serializers import *
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from client import *
from django.core.paginator import Paginator
from social.pagination import CustomPagination
from posts.github.utils import get_github_activities
from Remote.Authors import *

custom_parameter = openapi.Parameter(
    name='custom_param',
    in_=openapi.IN_QUERY,
    description='A custom parameter for the POST request',
    type=openapi.TYPE_STRING,
    required=True,
)

GetAuthorsExample={
    200: openapi.Response(
        description='Success response',
        examples={
            'application/json': {
  "count": 2,
  "next": 'null',
  "previous": 'null',
  "results": [
    {
      "type": "author",
      "id": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
      "url": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
      "host": "",
      "displayName": "LaraCroft",
      "github": "",
      "profileImage": ""
    },
    {
      "type": "author",
      "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
      "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
      "host": "",
      "displayName": "TomHardy",
      "github": "",
      "profileImage": ""
    }
  ]
}
        }
    )
}




OneAuthor = {
    200: openapi.Response(
        description='Success response',
        examples={
            'application/json': {
  "type": "author",
  "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
  "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
  "host": "",
  "displayName": "TomHardy",
  "github": "",
  "profileImage": ""
}
        }
    )
}

OneAuthorUpdated = {
    200: openapi.Response(
        description='Successfully updated/added author',
        examples={
            'application/json': {
  "type": "author",
  "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
  "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
  "host": "",
  "displayName": "TomHardyUpdated",
  "github": "",
  "profileImage": ""
}
        }
    )
}

FollowersGet = {
    200: openapi.Response(
        description='Sucessfully retrieve followers',
        examples={'application/json': {
  "type": "followers",
  "items": [
    {
      "type": "author",
      "id": "cfd9d228-44df-4a95-836f-c0cb050c7ad6",
      "url": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
      "host": "",
      "displayName": "LaraCroft",
      "github": "",
      "profileImage": ""
    }
  ]
}}
    )
}

InboxPOST = {
    200: openapi.Response(
        description='Sucessfully rPost to inbox',
        examples={'application/json': {
  "request": {
    "type": "Follow",
    "actor": {
      "id": "cfd9d228-44df-4a95-836f-c0cb050c7ad6"
    },
    "object": {
      "id": "971fa387-b101-4276-891f-d970f2cf0cad"
    }
  },
  "saved": {
    "author": "971fa387-b101-4276-891f-d970f2cf0cad",
    "content_type": 6,
    "object_id": 1
  }
}}
    )
}

InboxGet = {
    200: openapi.Response(
        description='Sucessfully retrieve Inbox',
        examples={'application/json': {
  "count": 1,
  "next": 'null',
  "previous":'null',
  "results": {
    "type": "inbox",
    "author": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
    "items": [
      {
        "type": "Follow",
        "summary": "LaraCroft wants to follow TomHardyUpdated",
        "actor": {
          "type": "author",
          "id": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
          "url": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
          "host": "",
          "displayName": "LaraCroft",
          "github": "",
          "profileImage": ""
        },
        "object": {
          "type": "author",
          "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
          "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
          "host": "",
          "displayName": "TomHardyUpdated",
          "github": "",
          "profileImage": ""
        }
      }
    ]
  }
}}
    )
}


class AuthorsListView(APIView, PageNumberPagination):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(responses= GetAuthorsExample,operation_summary="List of Authors registered")
    def get(self, request):
        
        """
        Get the list of authors on our website
        """
        content = {

            'user':str(request.user),

            'auth': str(request.auth)
        }
        
        # create a list of our own authors
        authors = Author.objects.filter(host=(settings.HOST_NAME))
        serializer = AuthorSerializer(authors, many=True)
        data_list = serializer.data
        # get remote authors and add to list
        # yoshi = getNodeAuthors_Yoshi()
        # for yoshi_author in yoshi:
        #     data_list.append(yoshi_author)
        #social_distro = getNodeAuthors_social_distro()
        #for social_distro_author in social_distro:
        #    data_list.append(social_distro_author)

        # paginate + send
        return Response(ViewPaginatorMixin.paginate(self,object_list=data_list, type="authors", page=int(self.request.GET.get('page', 1)), size=int(self.request.GET.get('size', 50))))

# made the foreign author getter a helper function instead to work with inbox
def get_foreign_authors(pk_a):
    print("getting foreign")
    try:
        # get yoshi's author at node
        author_json, status_code = getNodeAuthor_Yoshi(pk_a)
        if status_code == 200:
            # author_dict = json.loads(author_json)
            # author = Author(id = author_json['authorId'], displayName= author_json['displayname'], url=author_json['url'], profileImage=author_json['profileImage'], github=author_json['github'], host=author_json['host'])
            return Response(author_json)
        # get social distro's authors and format their data to our style
        else:
            author_json, status_code = getNodeAuthor_social_distro(pk_a)
            if status_code == 200:
                """# formatting (theirs is nonetype while ours is empty string)
                if author_json['profileImage'] == None:
                    profileImage = ''
                if author_json['github'] == None:
                    github = ''
                author = Author(id = pk_a, displayName= author_json['displayName'], url=author_json['url'], profileImage=profileImage, github=github, host=author_json['host'])"""
                return Response(author_json)
                
    except:
        error_msg = "Author id not found"
        return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
    
class AuthorView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # properly configure the author's displayname in data
    def validate(self, data):
        try:
            if 'displayName' not in data:
                # if the displayname is not part of the data, add it from the author data
                data['displayName'] = Author.objects.get(displayName=data['displayName']).weight
            return data 
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(responses = OneAuthor, operation_summary="Finds Author by iD")
    def get(self, request, pk_a):

        """
        Get a particular author searched by AuthorID
        """
        # first, try to get local author
        try:
            author = Author.objects.get(pk=pk_a)
        # if local author isn't there, see if it's from remote
        except Author.DoesNotExist:
            author, found = getRemoteAuthorsById(pk_a)
            if found == True:
                return Response(author, status=status.HTTP_200_OK)
            else:
                error_msg = "Author id not found"
                return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        # return the data
        serializer = AuthorSerializer(author,partial=True)
        return  Response(serializer.data)
    
    @swagger_auto_schema(responses = OneAuthorUpdated, operation_summary="Update a particular Authors profile",request_body=openapi.Schema( type=openapi.TYPE_STRING,description='A raw text input for the PUT request', example={
                'displayName': 'TomHardyUpdated'
            }))
    def post(self, request, pk_a):
        """
        Update the authors profile
        """
        # get the author, 404 if not found
        try:
            author = Author.objects.get(pk=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

        # serialize author  
        serializer = AuthorSerializer(author,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class FollowersView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorSerializer

    # The get function is called witha  get request. The function is called by using 
    # ://authors/authors/{AUTHOR_ID}/followers/ to get a list of followers
    # or call using ://authors/authors/{AUTHOR_ID}/followers/foreign_author_id/ to check if foriegn author is following author
    #Implement later after talking to group 
    
    # @swagger_auto_schema(method ='get',responses=response_schema_dict,operation_summary="List of Followers")
    @swagger_auto_schema(responses=FollowersGet, operation_summary="List of Followers")
    def get(self, request, pk_a, pk=None):
        # grab main author
        try:
            author = Author.objects.get(id=pk_a)
            # author = Author.objects.get(id=request.data["author_id"])
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        # If url is /authors/authors/author_id/followers/
        # add local followers to the list of followers
        if pk == None:
            followers = author.friends.all()
            followers_list = []
            for follower in followers:
                try: 
                    follower_author = Author.objects.get(id=follower.id)
                except Author.DoesNotExist:
                    error_msg = "Follower id not found"
                    return Response(error_msg, status=status.HTTP_404_NOT_FOUND) 
                followers_list.append(AuthorSerializer(follower_author).data)

            items = {"type": "followers",
                    "items": followers_list
            }

            return Response(items, status=200)
        # else If url is /authors/authors/author_id/followers/foreign_author_id    
        # add foreign followers to the list of followers
        else:
            try:
                follower = Author.objects.get(id=pk)
            # follower = Author.objects.get(id=request.data["foreign_author_id"])
            except Author.DoesNotExist:
                error_msg = "Foreign Author id not found"
                return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

            friends = author.friends.all()
            if follower in friends:
                serializer = AuthorSerializer(follower,partial=True)
                #returns the follower
                return  Response(serializer.data)
            else:
                #if the follower is not apart of the followers list return empty{}
                return Response({})
            

    #For this we need nothing in the content field only the url with the author id of the person that is being followed by foreign author id 
    #call using ://authors/authors/{AUTHOR_ID}/followers/foreign_author_id/
    #Implement later after talking to group 
    @swagger_auto_schema(responses = OneAuthorUpdated, operation_summary="Add to followers",request_body=openapi.Schema( type=openapi.TYPE_STRING,description='A raw text input for the PUT request'))
    def put(self, request, pk_a, pk):
        try:
            author = Author.objects.get(id=pk_a)
            # author = Author.objects.get(id=request.data["author_id"])
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

        try:
            new_follower = Author.objects.get(id=pk)
            # new_follower = Author.objects.get(id=request.data["foreign_author_id"])
        except Author.DoesNotExist:
            error_msg = "Follower id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

        followers = author.friends
        followers.add(new_follower)
        author.save()
        try: 
            follow = FollowRequest.objects.get(actor=new_follower,object=author)
            Inbox.objects.get(object=follow).delete()
        except:
            pass

        # return the new list of followers
        return Response(new_follower.follower_to_object())

    #For the delete request we need nothing in the content field only the url with the author id of the person that is being followed by foreign author id
    #Implement later after talking to group 
    # @swagger_auto_schema(method ='get',responses=response_schema_dict,operation_summary="Delete Follower")
    @swagger_auto_schema(operation_summary="Delete followers in the request")
    def delete(self, request, pk_a, pk):
        try:
            author = Author.objects.get(id=pk_a)
            # author = Author.objects.get(id=request.data["author_id"])
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

        try:
            removed_follower = Author.objects.get(id=pk)
            # removed_follower = Author.objects.get(id=request.data["foreign_author_id"])
        except Author.DoesNotExist:
            error_msg = "Follower id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

        followers = author.friends
        followers.remove(removed_follower)
        author.save()
        
        # return the new list of followers
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GitHubView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk_a):
        author = get_object_or_404(Author,pk=pk_a)

        github_posts = get_github_activities(author.github, author)

        serializer = PostSerializer(github_posts,many=True)

        return Response(serializer.data)        

#request_body=openapi.Schema( type=openapi.TYPE_STRING,description='A raw text input for the POST request'))
class FriendRequestView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FollowRequestSerializer
    
    def post(self,request,pk_a):
        try:
            actor = Author.objects.get(id=pk_a)
            displaynameto = request.data['displayName']
            displaynamefrom=actor.displayName
            objects = Author.objects.filter(displayName = displaynameto)[0]

            if FollowRequest.objects.filter(actor=actor, object=objects).exists():
                return Response("You've already sent a request to this user", status=status.HTTP_400_BAD_REQUEST)
            if actor==objects:
                return Response("You cannot follow yourself!", status=status.HTTP_400_BAD_REQUEST)
            
            type = "Follow"
            summary = displaynamefrom + " wants to follow " + displaynameto
            follow = FollowRequest(summary=summary,actor=actor, object=objects)
            follow.save()
            serializer = FollowRequestSerializer(follow)
            return Response(serializer.data)
        
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
                
    def delete(self, request, pk_a):
        try:
            author = Author.objects.get(id=pk_a)
            # author = Author.objects.get(id=request.data["author_id"])
        except Author.DoesNotExist:
            error_msg = "Author not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        try:
            actor_id = request["actor_id"][-1] if request["actor_id"].endswith('/') else request["actor_id"]
            actor_id = actor_id.split('/')[-1]
            print("actor id is", actor_id)
            actor_author = Author.objects.get(id=actor_id)
            # author = Author.objects.get(id=request.data["author_id"])
        except Author.DoesNotExist:
            error_msg = "Actor author sent not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        FollowRequest.objects.filter(object=author,actor=actor_author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ViewRequests(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FollowRequestSerializer
    # @permission_classes([IsAuthenticated])
    def get(self,request,pk_a):
        """
        Get the list of Follow requests for the current Author
        """
        try:    
            Object = Author.objects.get(id=pk_a)
            displaynamefrom=Object.displayName

            requests = FollowRequest.objects.filter(object = Object)
            serializer = FollowRequestSerializer(requests,many=True)
            return Response(serializer.data)
        
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

class InboxSerializerObjects:
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def serialize_inbox_objects(self, item, context={}):
        # return the serializer data of all objects in inbox
        object_model = item.content_type.model_class()
        if object_model is Post:
            serializer = PostSerializer
        elif object_model is Like:
            serializer = LikeSerializer
        elif object_model is Comment:
            serializer = CommentSerializer
        elif object_model is FollowRequest:
            serializer = FollowRequestSerializer
        return serializer(item.content_object, context=context).data
    
    def deserialize_objects(self, data, pk_a):
        # return serializer of objects to be added to inbox (so we get the object)
        # print(data)
        type1 = data["type"]
        print(type1)
        obj = None

        if type1 is None:
            raise exceptions
        if type1 == Post.get_api_type():
            try:
                obj = Post.objects.get(id=(data["id"].split("/")[-1]))
            except Post.DoesNotExist:
                try:
                    # handle image posts
                    if "image/" in data["contentType"]:
                        print(data["content"])
                        # make a mutable version of the querydict so that we can use
                        # our special image field
                        data = data.copy()
                        data = handle_image(data)
                        print(data['image'])
                        serializer = ImageSerializer
                    # normal post
                    else:
                        print("post serrializer")
                        serializer = PostSerializer
                    print("got to send part")
                    context={}
                    # try:
                    #     author = data["author"]
                    #     if author["host"]== 'https://bigger-yoshi.herokuapp.com/api/':
                    #         new_data = {}
                    # except:
                    new_data = data
                    try: 
                        print('trying to get commentsSrc')
                        if new_data["commentsSrc"]:
                            print("commentsSrc in new data")
                            del new_data["commentsSrc"]
                    except: 
                        pass
                    
                    # print("new data", new_data)
                    # new_data["authors"] = data["sentTo"]
                    try: 
                        print('trying to get authors')
                        if new_data["authors"]:
                            print("authors in new data")
                            del new_data["authors"]
                    except: 
                        pass
                    print("new data", new_data)
                    # new_data["authors"] = data["sentTo"]
                    return serializer(data=new_data, context=context, partial=True)

                except:
                    print("image exception")
                    error_msg = "Post not found"
                    return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        elif type1 == Like.get_api_type():
            # TODO: Add a check to see if the author liked that object before, then just return obj
            print("its a like")
            serializer = LikeSerializer
            author = data.get("author")
            obj = data.get("object")
            context={'object': obj, 'author':author}
            return serializer(data={}, context=context, partial=True)
            # context={'author_id': data["author_id"]}
        elif type1 == Comment.get_api_type():
            serializer = CommentSerializer
            author = data.get("author")
            comment = data.get("comment")
            object = data.get("object")
           # context={'author': author,'id':data["id"].split("/")[-1]}
            context={'author': author, 'object':object,'comment':comment}
        elif type1 == FollowRequest.get_api_type() or type1 == "follow":
            print("deser follow")
            serializer = FollowRequestSerializer
            actor = data.get("actor")
            context={'object_id': pk_a, 'actor_':actor}
            return serializer(data={}, context=context, partial=True)
        print("finish")
        if obj is not None:
            return obj
        else:
            return serializer(data={}, context=context, partial=True)
    
class Inbox_list(APIView, InboxSerializerObjects, PageNumberPagination):
    """
        URL: author/auhor_id/inbox
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses = InboxGet, operation_summary="Get all the objects in the inbox")
    def get(self, request, pk_a):
        # GET all objects in inbox, only need auth in request

        author = get_object_or_404(Author,pk=pk_a)
        inbox_data = author.inbox.all()
        serializer = InboxSerializer(data=inbox_data, context = {"serializer":self.serialize_inbox_objects}, many=True)
        serializer.is_valid()
        data = self.get_items(pk_a, serializer.data)
        # TODO: Fix pagination
        return Response(data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(responses = InboxPOST, operation_summary="Post a new object to the inbox",request_body=openapi.Schema( type=openapi.TYPE_STRING,description='A raw text input for the POST request', example = {
        "type": "Follow",
        "actor":{"id":"cfd9d228-44df-4a95-836f-c0cb050c7ad6"},
        "object":{"id":"971fa387-b101-4276-891f-d970f2cf0cad"}
        }))
    def post(self, request, pk_a):
        """
            POST a new object to inbox
            request: 
            1. If the object is from a foreign author and not in database: a full object (Like, Author, Comment) with mandatory fields required, TYPE, id, author.
            2. If object in database: TYPE, id.
        """
        try:
            # print("in Post")
            author = Author.objects.get(pk=pk_a, host=settings.HOST_NAME)
            print("found author locally")
        except Author.DoesNotExist:
            print("couldnt find author in foreign or local")
            return Response("Author not Found", status=status.HTTP_404_NOT_FOUND)
        
        #issue here
        print("deserialize")
        serializer = self.deserialize_objects(self.request.data, pk_a)
        # Case 1: friend author is outside the server, we create all these objects in our database (not sure)
        try:
            if serializer.is_valid():
                item = serializer.save()
                print("IS VALID")
                if item=="already liked":
                    return Response("Post Already Liked!", status=status.HTTP_400_BAD_REQUEST)
                if item == "already sent":
                    return Response("You've already sent a request to this user!", status=status.HTTP_400_BAD_REQUEST)
                if item == "same":
                    return Response("You cannot send a follow request to yourself!", status=status.HTTP_400_BAD_REQUEST)
                if item == "already friends":
                    return Response("You already follow them!", status=status.HTTP_400_BAD_REQUEST)
                if hasattr(item, 'update_fields_with_request'):
                    item.update_fields_with_request(request)
            else:
                print("serilizer is not valid")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as e:
            item = serializer   
        inbox_item = Inbox(content_object=item, author=author)
        inbox_item.save()
        return Response({'request': self.request.data, 'saved': model_to_dict(inbox_item)})
    
    @swagger_auto_schema(operation_summary="Delete all the objects in the inbox")
    def delete(self, request, pk_a):
        # GET all objects in inbox, only need auth in request
        try: 
            author = get_object_or_404(Author,pk=pk_a)
            author.inbox.all().delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response("Post does not exist",status=status.HTTP_404_NOT_FOUND)
    
    
    def get_items(self,pk_a,data):
        # helper function 
        
        dict = {"type":"inbox", "author": settings.APP_NAME + '/authors/' + pk_a }
        items = []
        for item in data:
            items.append(item["content_object"])

        dict["items"] = items
        return(dict) 
    
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAuthor(request, displayName):
    """
    Details of particular author
    """
    authorList = getRemoteAuthorsDisplayName(displayName)
    try:
        author = Author.objects.get(displayName=displayName, host=settings.HOST_NAME)
        serializer = AuthorSerializer(author,partial=True)
        authorList.append(serializer.data)
    except Author.DoesNotExist:
        return Response(authorList)
    return Response(authorList)

class registerNode(APIView):
    def post(self, request):
        """Register a django user to make them a Node"""
        '''In the data provide "username":"the username they chose", 
        "email":"Their email they provided", 
        "password":"Their Password",
        "url":"url to their site"
        
          '''
        #   {"username":"jacob_node1", 
        # "email":"jacob@node1", 
        # "password":"jacobs_node1",
        # "url":"url to their site"}

        id_ = str(uuid.uuid4())
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        application_url = request.data['url']
        try:
            #create a new user object
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()
            node = Node(user=user, id = id_, name= 'Node', url=application_url)
            node.save()
            return Response("created", status=status.HTTP_201_CREATED)
        except IntegrityError as e: 
            print(e)
            return Response("display name already in use", status=status.HTTP_400_BAD_REQUEST)